#!/usr/bin/env python3
"""Step 4 -- assemble the five delivered datasets into one data_out.json.

Blocks
  1  edit_manifest           recipe-labelled sub-4.2B edited checkpoints + their parents
  2a sft_benign              oasst1 benign single-turn pairs
  2b fluency_wikitext        wikitext-2-raw-v1 test paragraphs
  2c heldout_benign_prompts  dolly-15k prompts, disjoint from 2a
  3  hub_scan_pool           ranked, costed metadata-only scan pool

Nothing here touches weights or runs a model. The coverage report in
metadata.dataset_meta.coverage is a deliverable, not commentary.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipes  # noqa: E402
from hub_common import ABLIT_RE, ROOT  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "assemble.log", rotation="30 MB", level="DEBUG")

ABLIT = re.compile(ABLIT_RE)
# Quantised / re-packaged uploads are derivatives of someone else's edit, not
# distinct recipes, and their cards describe the quantisation rather than the
# edit. The separator class is deliberately broad ([-_.]) -- `..._mlx` and
# `...-exl3-6.0bpw` both slipped through an earlier narrower version.
QUANT = re.compile(
    r"(?i)([-_.](mlx|gguf|awq|gptq|exl2|exl3|onnx|bnb|mflux)\b|^(mlx|gguf)-|[-_.](4bit|8bit|3bit|6bit|w4a16|w8a8|int4|int8|fp8|nf4|bpw)\b|\b(gguf|awq|gptq)\b|\d+\.?\d*bpw)"
)
CEILING_MANIFEST = 4.2e9
CEILING_POOL = 4.0e9
COLLECTED_AT = date.today().isoformat()

# Step-1d self-audit. Three independent 10-row samples were read by hand against
# the raw cards (`audit_sample.py <seed>`) on the FINAL labeller. Reported as
# found, including the failures.
HAND_CHECK = {
    "protocol": "audit_sample.py draws 10 random non-parent manifest rows per seed and prints the assigned class, the rule that fired and the raw card; each was read and judged by hand against the card.",
    "seeds": [20260813, 7, 42],
    "n_checked": 30,
    "n_survived": 27,
    "survival_rate": 0.9,
    "failures": [
        {
            "repo_id": "0utsideness/gemma-3-270m-it-heretic-refusal-plugin-trial99-test",
            "assigned": "R2_NORM_PRESERVING_PROJECTED",
            "objection": "a Heretic model whose card embeds a tool config dump; R2 fired on a COMMENT about row-magnitude preservation rather than a method claim. R4 is the more informative label.",
        },
        {
            "repo_id": "UnfilteredAI/DAN-Qwen3-1.7B",
            "assigned": "R6_BEHAVIOURAL_SFT_UNCENSORED",
            "objection": "the class is probably right for this uploader, but the quoted span is marketing copy ('raw, unfiltered intelligence'), not a statement that a fine-tune produced the behaviour.",
        },
        {
            "repo_id": "dalatexcoder/Rice-Cracker-Qwen3.5-0.8B-Abliterated-Base",
            "assigned": "R4_PARTIAL_LAYER_OR_PER_HEAD",
            "objection": "the card says it is a finetune OF a heretic model, so the recipe is INHERITED from the parent rather than applied here; a derivative class (R7-like) would be more accurate.",
        },
    ],
    "failure_mode": "all three are the same shape -- an inherited-or-implied recipe, or evidence quoted from a config dump / marketing line instead of a method claim. None is a case of the labeller inventing a mechanism the card does not mention.",
    "bugs_found_and_fixed_during_auditing": [
        "R6 window was 120 chars, so a markdown URL between the verb and the object under-called real fine-tunes to UNKNOWN (widened to 300).",
        "R6 verb list had no LEADING word boundary, so 'trained' matched inside `from_pretrained(...)` in usage snippets and quoted a code block as evidence.",
        "bare 'unfiltered' was an R6 trigger; it also means an unfiltered training CORPUS, and was labelling a pedagogy study as an uncensoring fine-tune. It now only counts next to explicit censorship language.",
        "the quantised-re-upload filter missed `..._mlx` and `...-exl3-6.0bpw`, admitting re-packaged derivatives whose cards describe quantisation rather than the edit.",
    ],
}

ITER2_ABLITERATED = [
    "huihui-ai/Huihui-Qwen3-0.6B-abliterated-v2",
    "huihui-ai/Huihui-Qwen3-1.7B-abliterated-v2",
    "Goekdeniz-Guelmez/Josiefied-Qwen3-4B-Instruct-2507-gabliterated-v2",
    "huihui-ai/Qwen2.5-0.5B-Instruct-abliterated",
    "huihui-ai/Llama-3.2-1B-Instruct-abliterated",
    "huihui-ai/Qwen2.5-1.5B-Instruct-abliterated",
    "huihui-ai/Llama-3.2-3B-Instruct-abliterated",
    "Goekdeniz-Guelmez/Josiefied-Qwen2.5-3B-Instruct-abliterated-v1",
]

WEIGHT_EXT = {
    "safetensors": re.compile(r"(?i)\.safetensors$"),
    "bin": re.compile(r"(?i)\.bin$"),
    "gguf": re.compile(r"(?i)\.gguf$"),
}


def as_list(v) -> list[str]:
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    return [x for x in v if isinstance(x, str)]


def weight_bytes(files: list[dict] | None) -> tuple[dict, int]:
    """Per-format sums, so the safetensors/bin double-count stays visible."""
    per = {k: 0 for k in WEIGHT_EXT}
    for f in files or []:
        for k, pat in WEIGHT_EXT.items():
            if pat.search(f["rfilename"]):
                per[k] += f.get("size_bytes") or 0
    return per, sum(per.values())


# Bytes per element, for turning on-disk safetensors size into an INDEPENDENT
# parameter-count estimate. Needed because the Hub's safetensors index is not
# always right: samuelcardillo/Qwen3-Coder-Next-Opus-4.6-Reasoning-Distilled
# reports safetensors.total = 6,208,256 while shipping 159 GB of shards, and
# two 35B checkpoints report 664,944. Trusting the index alone silently admits
# 32-35B models into a sub-4B pool, so the ceiling is enforced twice.
DTYPE_BYTES = {
    "F64": 8, "I64": 8, "F32": 4, "I32": 4, "U32": 4,
    "F16": 2, "BF16": 2, "I16": 2, "U16": 2,
    "F8_E4M3": 1, "F8_E5M2": 1, "I8": 1, "U8": 1, "BOOL": 1,
    "F4": 0.5, "U4": 0.5, "I4": 0.5,
}


def implied_params_from_bytes(dtypes: dict | None, safetensors_bytes: int) -> float | None:
    """Params implied by on-disk size, using the repo's own declared dtypes.

    The dtype KEYS stay trustworthy even when the counts are wrong, so the
    widest declared dtype gives a conservative (i.e. smallest) implied count.
    """
    if not safetensors_bytes:
        return None
    widths = [DTYPE_BYTES[d] for d in (dtypes or {}) if d in DTYPE_BYTES]
    w = max(widths) if widths else 2.0  # bf16 is the overwhelming default
    return safetensors_bytes / w


def exceeds_ceiling_by_bytes(dtypes: dict | None, safetensors_bytes: int, ceiling: float) -> bool:
    """True when on-disk size cannot be reconciled with the ceiling.

    The 2x slack absorbs repos that ship a duplicate copy of the weights (a
    consolidated file alongside shards, or an extra adapter). It is far tighter
    than the discrepancies this exists to catch, which run to 10^4.
    """
    implied = implied_params_from_bytes(dtypes, safetensors_bytes)
    return implied is not None and implied > 2 * ceiling


def param_count(enum_row: dict, det: dict) -> tuple[int | None, str | None]:
    """Hub safetensors index first; analytic config estimate only as a last resort."""
    if enum_row.get("st_total"):
        return int(enum_row["st_total"]), "hub_safetensors_index"
    cfg = (det or {}).get("config") or {}
    h, L, V = cfg.get("hidden_size"), cfg.get("num_hidden_layers"), cfg.get("vocab_size")
    inter = cfg.get("intermediate_size")
    if all(isinstance(x, int) for x in (h, L, V)) and isinstance(inter, int):
        # 4*h^2 attn + 3*h*inter MLP per layer, + tied-ish embeddings
        est = L * (4 * h * h + 3 * h * inter) + 2 * h * V
        return int(est), "config_estimate"
    return None, None


def chat_evidence(enum_row: dict, det: dict) -> tuple[bool, str]:
    """is_chat_model + WHICH test fired, in descending order of directness.

    The Hub's parsed `config.tokenizer_config` does not always carry
    chat_template even when the repo has one (checked: the iter-2 member
    Josiefied-Qwen3-4B-…-gabliterated-v2 falls through to the id token), so the
    separate `chat_template.jinja` file is used as a second direct test. It is
    free: it comes from the file list already fetched for the size columns.
    """
    tc = enum_row.get("tokenizer_config") or {}
    if tc.get("chat_template") is not None:
        return True, "chat_template_in_tokenizer_config"
    names = {f["rfilename"] for f in ((det or {}).get("files") or [])}
    if "chat_template.jinja" in names or "chat_template.json" in names:
        return True, "chat_template_file_in_repo"
    if re.search(r"(?i)(instruct|-it\b|_it\b|chat|sft|dpo|rlhf)", enum_row["repo_id"]):
        return True, "id_token"
    return False, "no_chat_template_and_no_id_token"


# ------------------------------------------------------------------ block 1 --
def build_manifest(enum: dict[str, dict], det: dict[str, dict]) -> tuple[list[dict], dict]:
    harvest = re.compile(
        ABLIT_RE + r"|(heretic|lorablated|josiefied|amoral|unfiltered|unalign)"
    )

    over_ceiling, rows, by_id = [], [], {}
    n_index_rejected = 0
    for rid, e in enum.items():
        n = e.get("st_total") or 0
        id_hit = bool(harvest.search(rid))
        card = (det.get(rid) or {}).get("readme")
        card_hit = bool(card and ABLIT.search(card))
        if not (id_hit or card_hit):
            continue
        if n and n > CEILING_MANIFEST:
            over_ceiling.append(
                {
                    "repo_id": rid,
                    "param_count_hub": int(n),
                    "downloads": e.get("downloads"),
                    "reason": "param_count_hub above the 4.2e9 manifest ceiling",
                }
            )
            continue
        if not n:
            continue
        if QUANT.search(rid):
            continue  # quantised re-uploads are derivatives, not distinct recipes
        d = det.get(rid) or {}
        per_fmt_pre, _ = weight_bytes(d.get("files"))
        if exceeds_ceiling_by_bytes(e.get("st_parameters"), per_fmt_pre["safetensors"], CEILING_MANIFEST):
            over_ceiling.append(
                {
                    "repo_id": rid,
                    "param_count_hub": int(n),
                    "total_safetensors_bytes": per_fmt_pre["safetensors"],
                    "implied_params_from_bytes": int(
                        implied_params_from_bytes(e.get("st_parameters"), per_fmt_pre["safetensors"])
                    ),
                    "downloads": e.get("downloads"),
                    "reason": "the Hub safetensors index reports a sub-ceiling parameter count that the on-disk safetensors size contradicts; the size-implied count is used instead and it is over the ceiling",
                }
            )
            n_index_rejected += 1
            continue
        parents = as_list(e.get("card_base_model")) or as_list(
            ((d.get("config") or {}).get("_name_or_path"))
        )
        cls, rule, ev = recipes.label(card, parents)
        pc, pcsrc = param_count(e, d)
        per_fmt, total_w = weight_bytes(d.get("files"))
        is_chat, chat_ev = chat_evidence(e, d)
        rows.append(
            {
                "repo_id": rid,
                "revision_sha": d.get("sha") or e.get("sha"),
                "collected_at": COLLECTED_AT,
                "uploader": rid.split("/")[0],
                "declared_parent": parents[0] if parents else None,
                "declared_parents_all": parents,
                "is_parent": False,
                "recipe_class": cls,
                "label_rule": rule,
                "recipe_evidence": ev,
                "evidence_source": "model_card" if ev else None,
                "evidence_url": f"https://huggingface.co/{rid}/blob/{d.get('sha') or e.get('sha')}/README.md"
                if ev
                else None,
                "recipe_declared": rule not in ("no_card", "no_method_statement"),
                "param_count_hub": pc,
                "param_count_source": pcsrc,
                "param_dtypes": e.get("st_parameters"),
                "architectures": e.get("architectures"),
                "model_type": e.get("model_type"),
                "files": d.get("files"),
                "weight_bytes_by_format": per_fmt,
                "total_weight_bytes": total_w,
                "downloads": e.get("downloads"),
                "likes": e.get("likes"),
                "license": e.get("card_license"),
                "repo_id_contains_abliteration_string": bool(ABLIT.search(rid)),
                "card_declares_abliteration": card_hit,
                "is_chat_model": is_chat,
                "chat_evidence": chat_ev,
                "is_iter2_class_member": rid in ITER2_ABLITERATED,
                "status": d.get("status", "ok"),
                "last_modified": e.get("last_modified"),
                "found_by": e.get("found_by"),
                "notes": None,
            }
        )
        by_id[rid] = rows[-1]

    # ---- parents as their own rows, so the H3 head-to-head has matched pairs
    parent_rows, pairs = [], []
    wanted: set[str] = set()
    for r in rows:
        for p in r["declared_parents_all"]:
            if p in enum and p not in by_id:
                wanted.add(p)
    for p in sorted(wanted):
        e = enum[p]
        n = e.get("st_total") or 0
        if not n or n > CEILING_MANIFEST:
            continue
        d = det.get(p) or {}
        pc, pcsrc = param_count(e, d)
        per_fmt, total_w = weight_bytes(d.get("files"))
        is_chat, chat_ev = chat_evidence(e, d)
        parent_rows.append(
            {
                "repo_id": p,
                "revision_sha": d.get("sha") or e.get("sha"),
                "collected_at": COLLECTED_AT,
                "uploader": p.split("/")[0],
                "declared_parent": None,
                "declared_parents_all": as_list(e.get("card_base_model")),
                "is_parent": True,
                "recipe_class": None,
                "label_rule": "is_parent",
                "recipe_evidence": None,
                "evidence_source": None,
                "evidence_url": None,
                "recipe_declared": False,
                "param_count_hub": pc,
                "param_count_source": pcsrc,
                "param_dtypes": e.get("st_parameters"),
                "architectures": e.get("architectures"),
                "model_type": e.get("model_type"),
                "files": d.get("files"),
                "weight_bytes_by_format": per_fmt,
                "total_weight_bytes": total_w,
                "downloads": e.get("downloads"),
                "likes": e.get("likes"),
                "license": e.get("card_license"),
                "repo_id_contains_abliteration_string": bool(ABLIT.search(p)),
                "card_declares_abliteration": False,
                "is_chat_model": is_chat,
                "chat_evidence": chat_ev,
                "is_iter2_class_member": False,
                "status": d.get("status", "ok"),
                "last_modified": e.get("last_modified"),
                "found_by": e.get("found_by"),
                "notes": "added as the declared parent of at least one edited row",
            }
        )
    have = {r["repo_id"] for r in rows} | {r["repo_id"] for r in parent_rows}
    for r in rows:
        for p in r["declared_parents_all"]:
            if p in have and p != r["repo_id"]:
                pairs.append({"child": r["repo_id"], "parent": p, "recipe_class": r["recipe_class"]})
                break

    all_rows = rows + parent_rows
    for i, r in enumerate(all_rows):
        r["row_id"] = f"manifest_{i:04d}"

    cls_counts: dict[str, int] = {c: 0 for c in recipes.CLASSES}
    for r in rows:
        cls_counts[r["recipe_class"]] = cls_counts.get(r["recipe_class"], 0) + 1
    uploaders = sorted({r["uploader"] for r in rows})
    id_leak = sum(1 for r in rows if r["repo_id_contains_abliteration_string"])
    status_counts: dict[str, int] = {}
    for r in all_rows:
        status_counts[r["status"]] = status_counts.get(r["status"], 0) + 1

    cov = {
        "n_manifest_rows": len(all_rows),
        "n_edited_rows": len(rows),
        "n_parent_rows": len(parent_rows),
        "n_distinct_uploaders": len(uploaders),
        "uploaders": uploaders,
        "rows_per_recipe_class": cls_counts,
        "n_unknown": cls_counts[recipes.UNKNOWN],
        "unknown_fraction": round(cls_counts[recipes.UNKNOWN] / max(1, len(rows)), 4),
        "n_populated_recipe_classes": sum(
            1 for c, n in cls_counts.items() if n and c != recipes.UNKNOWN
        ),
        "empty_recipe_classes": [
            c for c, n in cls_counts.items() if not n and c != recipes.UNKNOWN
        ],
        "n_recipe_declared": sum(1 for r in rows if r["recipe_declared"]),
        "n_recipe_undeclared": sum(1 for r in rows if not r["recipe_declared"]),
        "n_repo_id_contains_abliteration_string": id_leak,
        "repo_id_leak_fraction_of_true_positives": round(id_leak / max(1, len(rows)), 4),
        "n_card_declares_abliteration": sum(1 for r in rows if r["card_declares_abliteration"]),
        "n_complete_parent_child_pairs": len(pairs),
        "parent_child_pairs": pairs,
        "n_iter2_class_members_present": sum(1 for r in rows if r["is_iter2_class_member"]),
        "n_over_ceiling_near_misses": len(over_ceiling),
        "n_rejected_hub_index_contradicted_by_bytes": n_index_rejected,
        "status_counts": status_counts,
        "hand_check": HAND_CHECK,
        "empty_class_finding": (
            "R5_SPECTRAL_CASCADE_DCT is EMPTY, and that is a finding about the Hub rather "
            "than a gap in the harvest. The plan expected it from OBLITERATUS's "
            "'spectral_cascade' mode, but the OBLITERATUS README fetched into "
            "evidence/obliteratus_readme.md contains ZERO occurrences of 'spectral', "
            "'frequency', 'Fourier' or 'DCT'; its documented profiles are basic / advanced / "
            "aggressive / surgical / optimized / inverted, built on diff-in-means, SVD and "
            "whitened SVD. No sub-4.2B checkpoint declaring a frequency-domain recipe was "
            "found. Any H1 arm that needs a spectral recipe is UNRUNNABLE at this scale."
        ),
        "diversity_floors": {
            "uploaders_required": 5,
            "uploaders_achieved": len(uploaders),
            "uploaders_met": len(uploaders) >= 5,
            "recipe_classes_required": 4,
            "recipe_classes_achieved": sum(
                1 for c, n in cls_counts.items() if n and c != recipes.UNKNOWN
            ),
            "recipe_classes_met": sum(1 for c, n in cls_counts.items() if n and c != recipes.UNKNOWN)
            >= 4,
            "rows_required": 25,
            "rows_met": len(rows) >= 25,
        },
    }
    return all_rows, {"coverage": cov, "over_ceiling_candidates": over_ceiling[:200]}


# ------------------------------------------------------------------ block 3 --
def build_pool(enum: dict[str, dict], det: dict[str, dict], manifest_ids: set[str]) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    n_index_rejected_pool: list[str] = []
    for rid, e in enum.items():
        n = e.get("st_total") or 0
        if not n or n > CEILING_POOL:
            continue
        if QUANT.search(rid):
            continue
        d = det.get(rid)
        if d is None or d.get("status") != "ok":
            continue
        per_fmt, _ = weight_bytes(d.get("files"))
        if exceeds_ceiling_by_bytes(e.get("st_parameters"), per_fmt["safetensors"], CEILING_POOL):
            n_index_rejected_pool.append(rid)
            continue
        card = d.get("readme")
        pc, pcsrc = param_count(e, d)
        id_hit = bool(ABLIT.search(rid))
        card_hit = bool(card and ABLIT.search(card))
        is_chat, chat_ev = chat_evidence(e, d)
        rows.append(
            {
                "repo_id": rid,
                "revision_sha": d.get("sha") or e.get("sha"),
                "collected_at": COLLECTED_AT,
                "downloads": e.get("downloads"),
                "likes": e.get("likes"),
                "param_count_hub": pc,
                "param_count_source": pcsrc,
                "architecture": (e.get("architectures") or [None])[0],
                "model_type": e.get("model_type"),
                "license": e.get("card_license"),
                "total_safetensors_bytes": per_fmt["safetensors"],
                "card_text_sha256": d.get("readme_sha256"),
                "card_char_len": len(card) if card else 0,
                "declares_abliteration": id_hit or card_hit,
                "repo_id_contains_abliteration_string": id_hit,
                "is_chat_model": is_chat,
                "chat_evidence": chat_ev,
                "in_edit_manifest": rid in manifest_ids,
            }
        )

    declared = [r for r in rows if r["declares_abliteration"]]
    nd_chat = [r for r in rows if not r["declares_abliteration"] and r["is_chat_model"]]
    nd_base = [r for r in rows if not r["declares_abliteration"] and not r["is_chat_model"]]
    for g in (nd_chat, nd_base, declared):
        g.sort(key=lambda r: -(r["downloads"] or 0))

    ordered = nd_chat + nd_base + declared
    cum = 0
    for i, r in enumerate(ordered, 1):
        r["scan_rank"] = i
        r["stratum"] = (
            "declared"
            if r["declares_abliteration"]
            else ("non_declaring_chat" if r["is_chat_model"] else "non_declaring_base")
        )
        cum += r["total_safetensors_bytes"] or 0
        r["cumulative_bytes"] = cum
        r["row_id"] = f"pool_{i:05d}"

    sizes = sorted(r["total_safetensors_bytes"] or 0 for r in ordered)

    def q(p):
        return sizes[min(len(sizes) - 1, int(p * len(sizes)))] if sizes else 0

    dls = [r["downloads"] or 0 for r in ordered]
    deciles = []
    for k in range(1, 11):
        idx = min(len(ordered), int(len(ordered) * k / 10)) - 1
        if idx >= 0:
            deciles.append(round(ordered[idx]["cumulative_bytes"] / 1e9, 2))

    cov = {
        "n_pool_rows": len(ordered),
        "n_rejected_hub_index_contradicted_by_bytes": len(n_index_rejected_pool),
        "rejected_hub_index_examples": n_index_rejected_pool[:20],
        "n_rows_with_zero_safetensors_bytes": sum(
            1 for r in ordered if not r["total_safetensors_bytes"]
        ),
        "scan_pool_target_met": len(ordered) >= 400,
        "target_rows": 600,
        "strata_achieved": {
            "declared": len(declared),
            "non_declaring_chat": len(nd_chat),
            "non_declaring_base": len(nd_base),
        },
        "strata_floors": {"declared": 60, "non_declaring_chat": 250, "non_declaring_base": 60},
        "strata_floors_met": {
            "declared": len(declared) >= 60,
            "non_declaring_chat": len(nd_chat) >= 250,
            "non_declaring_base": len(nd_base) >= 60,
        },
        "scan_order": "non-declaring chat by descending 30-day downloads, then non-declaring base, then declared last",
        "size_distribution_bytes": {
            "min": sizes[0] if sizes else 0,
            "median": q(0.5),
            "p90": q(0.9),
            "max": sizes[-1] if sizes else 0,
        },
        "total_gigabytes": round(cum / 1e9, 2),
        "cumulative_gigabytes_by_decile": deciles,
        "download_range": {"min": min(dls) if dls else 0, "max": max(dls) if dls else 0},
        "chat_stratum_caveat": "is_chat_model is inferred, not declared. Two tests are direct (chat_template inside the Hub-parsed tokenizer_config, or a chat_template.jinja/.json file in the repo) and one is weak (an instruct/chat/it token in the repo id). Rows in the non_declaring_base stratum with chat_evidence='no_chat_template_and_no_id_token' are therefore PRESUMED base, and a chat model that ships neither signal would land there wrongly. Use chat_evidence to decide how much weight the stratum label can carry.",
        "chat_evidence_counts": {
            k: sum(1 for r in ordered if r["chat_evidence"] == k)
            for k in {r["chat_evidence"] for r in ordered}
        },
    }
    return ordered, cov


def main() -> None:
    enum_raw = json.loads((ROOT / "results" / "enumerated.json").read_text())["models"]
    enum = {m["repo_id"]: m for m in enum_raw}
    det = {d["repo_id"]: d for d in json.loads((ROOT / "results" / "details.json").read_text())}
    corp = json.loads((ROOT / "results" / "corpora.json").read_text())
    logger.info(f"enum {len(enum)}, details {len(det)}")

    manifest, m_meta = build_manifest(enum, det)
    logger.info(f"manifest rows: {len(manifest)}; coverage {m_meta['coverage']['diversity_floors']}")
    pool, p_cov = build_pool(enum, det, {r["repo_id"] for r in manifest})
    logger.info(f"pool rows: {len(pool)}; strata {p_cov['strata_achieved']}")

    ev_docs = {}
    for name, meta in recipes.EVIDENCE_DOCS.items():
        f = ROOT / "evidence" / f"{name}.md"
        if f.exists():
            ev_docs[name] = {
                **meta,
                "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                "bytes": f.stat().st_size,
                "local_path": f"evidence/{name}.md",
            }

    datasets = [
        {
            "dataset": "edit_manifest",
            "examples": [
                {
                    "input": r["repo_id"],
                    "output": r["recipe_class"] if r["recipe_class"] else "PARENT",
                    "metadata_fold": "edit_manifest",
                    "metadata_block": "1",
                    "metadata_row_id": r["row_id"],
                    "metadata_features": r,
                }
                for r in manifest
            ],
        },
        {
            "dataset": "sft_benign",
            "examples": [
                {
                    "input": r["instruction"],
                    "output": r["response"],
                    "metadata_fold": "sft_benign",
                    "metadata_block": "2a",
                    "metadata_row_id": f"sft_{i:05d}",
                    "metadata_features": r,
                }
                for i, r in enumerate(corp["sft"]["rows"])
            ],
        },
        {
            "dataset": "fluency_wikitext",
            "examples": [
                {
                    "input": r["text"],
                    "output": "",
                    "metadata_fold": "fluency_wikitext",
                    "metadata_block": "2b",
                    "metadata_row_id": f"wiki_{i:05d}",
                    "metadata_features": r,
                }
                for i, r in enumerate(corp["wikitext"]["rows"])
            ],
        },
        {
            "dataset": "heldout_benign_prompts",
            "examples": [
                {
                    "input": r["prompt"],
                    "output": "",
                    "metadata_fold": "heldout_benign_prompts",
                    "metadata_block": "2c",
                    "metadata_row_id": f"held_{i:05d}",
                    "metadata_features": r,
                }
                for i, r in enumerate(corp["heldout"]["rows"])
            ],
        },
        {
            "dataset": "hub_scan_pool",
            "examples": [
                {
                    "input": r["repo_id"],
                    "output": "declared" if r["declares_abliteration"] else "not_declared",
                    "metadata_fold": "hub_scan_pool",
                    "metadata_block": "3",
                    "metadata_row_id": r["row_id"],
                    "metadata_features": r,
                }
                for r in pool
            ],
        },
    ]

    out = {
        "metadata": {
            "title": "Labelled Edit-Recipe Model Manifest + laundering corpora + Hub scan pool",
            "collected_at": COLLECTED_AT,
            "empty_output_note": "fluency_wikitext and heldout_benign_prompts are unlabelled by design -- a perplexity paragraph and a generation prompt have no target. The plan specifies output=null; the schema requires a string, so they carry \"\". An empty output in those two folds is intentional, not a missing value.",
            "scope_guard": "DATA ONLY. No model weights were downloaded, no forward pass was run, nothing was trained, no detector statistic (W01-W05) was computed and no AUROC is reported. Parameter counts come from the Hub's safetensors index; file sizes from the Hub file index.",
            "dataset_meta": {
                "blocks": {
                    "1_edit_manifest": {
                        "source": "Hugging Face Hub model listings + model cards",
                        "ceiling_params": CEILING_MANIFEST,
                        "recipe_class_vocabulary": recipes.CLASSES,
                        "labelling_precedence": [r[1] for r in recipes.RULES],
                        "evidence_documents": ev_docs,
                        **m_meta,
                    },
                    "2a_sft_benign": corp["sft"]["meta"],
                    "2b_fluency_wikitext": corp["wikitext"]["meta"],
                    "2c_heldout_benign_prompts": corp["heldout"]["meta"],
                    "3_hub_scan_pool": {
                        "source": "Hugging Face Hub model listings",
                        "ceiling_params": CEILING_POOL,
                        **p_cov,
                    },
                },
                "coverage": {
                    "block_1": m_meta["coverage"],
                    "block_2": {
                        "sft_benign": {
                            "n": corp["sft"]["meta"]["n_final"],
                            "license": corp["sft"]["meta"]["license"],
                            "source": corp["sft"]["meta"]["source_repo"],
                            "revision": corp["sft"]["meta"]["source_revision"],
                            "n_dropped_safety_topic": corp["sft"]["meta"]["n_dropped_safety_topic"],
                            "n_dropped_duplicate_instruction": corp["sft"]["meta"][
                                "n_dropped_duplicate_instruction"
                            ],
                        },
                        "fluency_wikitext": {
                            "n": corp["wikitext"]["meta"]["n_final"],
                            "license": corp["wikitext"]["meta"]["license"],
                            "source": corp["wikitext"]["meta"]["source_repo"],
                            "revision": corp["wikitext"]["meta"]["source_revision"],
                            "token_stats_gpt2": corp["wikitext"]["meta"]["token_stats_gpt2"],
                        },
                        "heldout_benign_prompts": {
                            "n": corp["heldout"]["meta"]["n_final"],
                            "license": corp["heldout"]["meta"]["license"],
                            "source": corp["heldout"]["meta"]["source_repo"],
                            "revision": corp["heldout"]["meta"]["source_revision"],
                            "n_dropped_exact_match_vs_2a": corp["heldout"]["meta"][
                                "n_dropped_exact_match_vs_2a"
                            ],
                            "n_dropped_5gram_jaccard_ge_0.5_vs_2a": corp["heldout"]["meta"][
                                "n_dropped_5gram_jaccard_ge_0.5_vs_2a"
                            ],
                        },
                    },
                    "block_3": p_cov,
                },
            },
        },
        "datasets": datasets,
    }

    p = ROOT / "data_out.json"
    p.write_text(json.dumps(out))
    logger.info(f"wrote {p} ({p.stat().st_size / 1e6:.1f} MB)")
    for d in datasets:
        logger.info(f"  {d['dataset']}: {len(d['examples'])} examples")


if __name__ == "__main__":
    main()
