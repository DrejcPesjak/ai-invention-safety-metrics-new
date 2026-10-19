#!/usr/bin/env python3
"""Build full_data_out.json: the artifact rows plus the selected measurement corpora.

Run with `uv run data.py` (the workspace has a pyproject.toml and .venv, so uv
resolves the project environment; there is no PEP-723 inline header, per aii-python).

This is the single assembler. It emits two families of dataset blocks:

  A. ARTIFACT BLOCKS -- the plan's actual deliverable, read from results/ (produced by
     src/s0..s5). One example per external_score / panel_checkpoint / lineage /
     split_assignment / coverage_stat / rule / prereg_statement row.

  B. MEASUREMENT-CORPUS BLOCKS -- one example per PROMPT, from the 10 HF corpora
     selected out of the 16 pinned in temp/datasets/. These exist because the coverage
     report's headline is that 65 of 66 panel checkpoints have no external safety
     number at all, so iteration 3 must measure them in-house; these are the
     instruments it will measure them with. Selection rationale and the 6 rejections
     are recorded in metadata.corpus_selection.

Every example carries metadata_fold (the split of its lineage, or 'na') so an
iteration-3 script can filter the whole artifact to one side with one predicate.
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
RESULTS, LOGS, DATASETS = HERE / "results", HERE / "logs", HERE / "temp" / "datasets"
LOGS.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "data.log"), rotation="30 MB", level="DEBUG")

RETRIEVAL_DATE = date.today().isoformat()
# Cap on any single free-text field copied into metadata_source_fields.
FIELD_CAP = 600

# --------------------------------------------------------------------------
# CORPUS SELECTION. 16 sources were pinned; these 10 are kept.
#
# The selection criterion is what the artifact actually needs: an instrument for
# each of the two safety sub-axes the hypothesis requires (harm-refusal AND
# over-refusal), preference for corpora that match an instrument already present in
# our external rows, and no bulk that buys nothing.
#
# files: (filename stem under temp/datasets/, split label)
# prompt_key / label_key: which column is the prompt and which is the label, read
# from the actual files (see logs/data.log for the column dump).
# --------------------------------------------------------------------------
CORPORA = [
    {
        "name": "xstest_v2",
        "hf_repo": "natolambert/xstest-v2-copy",
        "url": "https://huggingface.co/datasets/natolambert/xstest-v2-copy",
        "upstream": "XSTest v2 (Roettger et al., NAACL 2024, arXiv:2308.01263)",
        "axis": "SAFETY_OVERREFUSAL + SAFETY_HARM (250 safe / 200 unsafe contrast)",
        "why": (
            "THE instrument named by BLANKET_REFUSER_DISQUALIFICATION. Also the only "
            "corpus here that ships per-item HUMAN refusal annotations for all five "
            "reference models, which reproduce every cell of the paper's Table 1 total "
            "row exactly, and so let iteration 3 calibrate a refusal classifier "
            "against human labels instead of guessing at one."
        ),
        "files": [("full_natolambert_xstest-v2-copy_default_prompts", "prompts"),
                  ("full_natolambert_xstest-v2-copy_default_llama2orig", "annotated_llama2orig"),
                  ("full_natolambert_xstest-v2-copy_default_llama2new", "annotated_llama2new"),
                  ("full_natolambert_xstest-v2-copy_default_mistralguard", "annotated_mistralguard"),
                  ("full_natolambert_xstest-v2-copy_default_mistralinstruct", "annotated_mistralinstruct"),
                  ("full_natolambert_xstest-v2-copy_default_gpt4", "annotated_gpt4")],
        "prompt_key": "prompt",
        "label_key": "final_label",
        # The bare `prompts` split carries no refusal annotation (final_label is ""),
        # because nothing has been generated for it yet; its informative label is the
        # XSTest prompt type. The four annotated splits DO carry final_label.
        "label_key_by_split": {"prompts": "type"},
    },
    {
        "name": "or_bench_hard_1k",
        "hf_repo": "bench-llm/or-bench",
        "url": "https://huggingface.co/datasets/bench-llm/or-bench",
        "upstream": "OR-Bench (Cui et al., ICML 2025, arXiv:2405.20947), hard-1k subset",
        "axis": "SAFETY_OVERREFUSAL",
        "why": (
            "Second, independent over-refusal instrument, and the hard subset is the one "
            "that separates models: seemingly-toxic but actually-safe prompts. A single "
            "over-refusal instrument would make the disqualification rule an artefact of "
            "XSTest's ten prompt types."
        ),
        "files": [("full_bench-llm_or-bench_or-bench-hard-1k_train", "train")],
        "prompt_key": "prompt",
        "label_key": "category",
    },
    {
        "name": "wildguard_test",
        "hf_repo": "walledai/WildGuardTest",
        "url": "https://huggingface.co/datasets/walledai/WildGuardTest",
        "upstream": "WildGuard (Han et al., NeurIPS D&B 2024, arXiv:2406.18495)",
        "axis": "SAFETY_HARM + SAFETY_OVERREFUSAL (harmful / unharmful, adversarial flag)",
        "why": (
            "Instrument match: WildGuard is the grader behind the ONLY non-circular "
            "external safety rows this artifact has (the Qwen3-4B-SafeRL card's "
            "'Safety Rate (WildGuard)' and 'Refusal (WildGuard)'). Measuring in-house on "
            "WildGuard's own test set is the closest we can get to a like-for-like "
            "comparison with a published number."
        ),
        "files": [("full_walledai_WildGuardTest_default_train", "train")],
        "prompt_key": "prompt",
        "label_key": "label",
    },
    {
        "name": "harmbench_direct_request",
        "hf_repo": "swiss-ai/harmbench",
        "url": "https://huggingface.co/datasets/swiss-ai/harmbench",
        "upstream": "HarmBench (Mazeika et al., ICML 2024, arXiv:2402.04249), DirectRequest",
        "axis": "SAFETY_HARM",
        "why": (
            "The canonical harm-refusal behaviour set, with functional and semantic "
            "category labels for per-category breakdowns. Pinned via the ungated "
            "swiss-ai mirror because walledai/HarmBench is gated."
        ),
        "files": [("full_swiss-ai_harmbench_DirectRequest_test", "test"),
                  ("full_swiss-ai_harmbench_DirectRequest_val", "val")],
        "prompt_key": "Behavior",
        "label_key": "SemanticCategory",
    },
    {
        "name": "advbench",
        "hf_repo": "kelly8tom/advbench_orig",
        "url": "https://huggingface.co/datasets/kelly8tom/advbench_orig",
        "upstream": "AdvBench harmful behaviors (Zou et al., arXiv:2307.15043)",
        "axis": "SAFETY_HARM",
        "why": (
            "The most-reused harmful-behaviour set in the jailbreak literature, so an "
            "in-house number on it is the most comparable to published work. Ships the "
            "affirmative 'target' string, which is what prefix-attack and refusal-"
            "direction work conditions on. Ungated mirror of the gated walledai/AdvBench."
        ),
        "files": [("full_kelly8tom_advbench_orig_default_train", "train")],
        "prompt_key": "Behavior",
        "label_key": "BehaviorID",
    },
    {
        "name": "jbb_behaviors",
        "hf_repo": "JailbreakBench/JBB-Behaviors",
        "url": "https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors",
        "upstream": "JailbreakBench (Chao et al., NeurIPS D&B 2024, arXiv:2404.01318)",
        "axis": "SAFETY_HARM + SAFETY_OVERREFUSAL (100 harmful + 100 matched benign)",
        "why": (
            "The only corpus here with 100 harmful behaviours and 100 deliberately "
            "MATCHED benign ones, which is exactly the paired design the blanket-refuser "
            "rule needs: the same model, the same topics, both sides measured."
        ),
        "files": [("full_JailbreakBench_JBB-Behaviors_behaviors_harmful", "harmful"),
                  ("full_JailbreakBench_JBB-Behaviors_behaviors_benign", "benign")],
        "prompt_key": "Goal",
        "label_key": "Category",
    },
    {
        "name": "do_not_answer",
        "hf_repo": "LibrAI/do-not-answer",
        "url": "https://huggingface.co/datasets/LibrAI/do-not-answer",
        "upstream": "Do-Not-Answer (Wang et al., EACL Findings 2024, arXiv:2308.13387)",
        "axis": "SAFETY_HARM",
        "why": (
            "A risk taxonomy (5 areas / 12 harm types) rather than a flat list, so "
            "refusal can be broken down by harm type. Also ships six reference models' "
            "responses with harmfulness and action labels, which is a second source of "
            "human-labelled refusal behaviour alongside XSTest."
        ),
        "files": [("full_LibrAI_do-not-answer_default_train", "train")],
        "prompt_key": "question",
        "label_key": "types_of_harm",
    },
    {
        "name": "beavertails_evaluation",
        "hf_repo": "PKU-Alignment/BeaverTails-Evaluation",
        "url": "https://huggingface.co/datasets/PKU-Alignment/BeaverTails-Evaluation",
        "upstream": "BeaverTails (Ji et al., NeurIPS D&B 2023, arXiv:2307.04657)",
        "axis": "SAFETY_HARM",
        "why": (
            "700 prompts balanced over 14 harm categories -- the most category-balanced "
            "harm set here, which matters because refusal rates are strongly "
            "category-dependent and an unbalanced set silently measures topic mix."
        ),
        "files": [("full_PKU-Alignment_BeaverTails-Evaluation_default_test", "test")],
        "prompt_key": "prompt",
        "label_key": "category",
    },
    {
        "name": "toxigen_annotated",
        "hf_repo": "toxigen/toxigen-data",
        "url": "https://huggingface.co/datasets/toxigen/toxigen-data",
        "upstream": "ToxiGen (Hartvigsen et al., ACL 2022, arXiv:2203.09509), annotated split",
        "axis": "SAFETY_HARM (implicit toxicity, human-scored)",
        "why": (
            "Instrument match: google/gemma-2-2b-it has a PUBLISHED ToxiGen number in "
            "this artifact (48.32). ToxiGen is therefore the one corpus where an "
            "in-house measurement can be checked against an external row for the same "
            "checkpoint -- a validity check on the whole in-house fallback."
        ),
        "files": [("full_toxigen_toxigen-data_annotated_test", "test")],
        "prompt_key": "text",
        "label_key": "toxicity_human",
    },
    {
        "name": "aegis_safety_test",
        "hf_repo": "walledai/AegisSafetyTest",
        "url": "https://huggingface.co/datasets/walledai/AegisSafetyTest",
        "upstream": "NVIDIA Aegis AI Content Safety (Ghosh et al., arXiv:2404.05993)",
        "axis": "SAFETY_HARM + SAFETY_OVERREFUSAL (Safe / Unsafe, 3 annotators)",
        "why": (
            "Small (359) but carries THREE independent annotator labels per prompt, so "
            "it supplies annotator-disagreement structure the other corpora do not. "
            "Kept over the 33k-row Aegis-2.0 training set, which is bulk for this "
            "purpose."
        ),
        "files": [("full_walledai_AegisSafetyTest_prompts_train", "train")],
        "prompt_key": "prompt",
        "label_key": "labels",
    },
]

REJECTED = [
    {"hf_repo": "allenai/real-toxicity-prompts", "n_rows": 99442,
     "why_rejected": "99k web sentence PREFIXES for open-ended continuation, not "
                     "instructions. The artifact measures refusal to an instruction; a "
                     "truncated news sentence cannot be refused. Also 69 MB, the single "
                     "largest pinned file, for no usable measurement."},
    {"hf_repo": "nvidia/Aegis-AI-Content-Safety-Dataset-2.0", "n_rows": 33416,
     "why_rejected": "A 33k guard-model TRAINING corpus. walledai/AegisSafetyTest is the "
                     "same taxonomy in evaluation form and is kept instead."},
    {"hf_repo": "walledai/SaladBench", "n_rows": 26518,
     "why_rejected": "21k of its 26k rows are attack-ENHANCED and defense-enhanced "
                     "rewrites. Iteration 3 measures single-turn refusal, so jailbreak "
                     "templates would confound the refusal rate with attack success. "
                     "HarmBench and JBB already cover the plain-request harm axis."},
    {"hf_repo": "bench-llms/or-bench-toxic-all", "n_rows": 22911,
     "why_rejected": "OR-Bench's TOXIC half, redundant with HarmBench/AdvBench/JBB on "
                     "the harm axis. What OR-Bench uniquely contributes here is its "
                     "over-refusal half, which is kept as or_bench_hard_1k."},
    {"hf_repo": "open-llm-leaderboard/contents", "n_rows": 4576,
     "why_rejected": "Not a prompt corpus. It is a SCORE table, and it is already "
                     "represented row-by-row in the external_score block; shipping it "
                     "twice in two shapes would invite double counting."},
    {"hf_repo": "open-llm-leaderboard-old/contents", "n_rows": 7260,
     "why_rejected": "Same as above, for leaderboard v1."},
]


def load(name: str):
    return json.loads((RESULTS / name).read_text())


def rows_of(stem: str) -> list[dict]:
    path = DATASETS / f"{stem}.json"
    if not path.exists():
        raise FileNotFoundError(f"pinned corpus missing: {path}")
    text = path.read_text()
    if len(text.strip()) < 10:
        # The HF download helper can leave a truncated 2-byte "[" behind when a shard
        # write races or a parquet shard comes back empty. Fail loudly here rather than
        # letting a silently-empty corpus ship as "0 prompts".
        raise ValueError(
            f"pinned corpus {path.name} is truncated ({len(text)} bytes) -- re-download "
            f"that split before rebuilding"
        )
    blob = json.loads(text)
    rows = blob if isinstance(blob, list) else blob["examples"]
    if not rows:
        raise ValueError(f"pinned corpus {path.name} parsed to zero rows")
    return rows


def as_text(v) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return ", ".join(str(x) for x in v)
    return str(v)


def build_corpus_blocks() -> tuple[list[dict], list[dict]]:
    """One example per PROMPT row. Returns (blocks, per-corpus stats)."""
    blocks, stats = [], []
    for spec in CORPORA:
        examples: list[dict] = []
        for stem, split in spec["files"]:
            rows = rows_of(stem)
            if rows:
                logger.debug(f"{spec['name']}/{split} columns: {list(rows[0].keys())}")
            label_key = spec.get("label_key_by_split", {}).get(split, spec["label_key"])
            for i, r in enumerate(rows):
                prompt = as_text(r.get(spec["prompt_key"]))
                if not prompt.strip():
                    continue
                ex = {
                    "input": prompt,
                    "output": as_text(r.get(label_key)) or "UNLABELLED",
                    "metadata_row_kind": "measurement_prompt",
                    "metadata_fold": "na",
                    "metadata_corpus": spec["name"],
                    "metadata_hf_repo": spec["hf_repo"],
                    "metadata_source_url": spec["url"],
                    "metadata_split": split,
                    "metadata_row_index": i,
                    "metadata_label_field": label_key,
                    "metadata_axis": spec["axis"],
                    "metadata_retrieval_date": RETRIEVAL_DATE,
                    # Everything the source row carries except the prompt itself, so a
                    # downstream script can re-derive any per-category breakdown without
                    # re-downloading. Nested dicts are dropped; flat lists such as Aegis'
                    # three annotator labels are kept. Long free-text fields are capped:
                    # do-not-answer ships six reference-model responses per row and the
                    # XSTest annotated splits ship a full completion, which together
                    # accounted for ~20 MB of the file before capping. The reference
                    # completion is carried separately and once, not twice.
                    "metadata_source_fields": {
                        k: (v[:FIELD_CAP] + f"...[truncated from {len(v)} chars]"
                            if isinstance(v, str) and len(v) > FIELD_CAP else v)
                        for k, v in r.items()
                        if k not in (spec["prompt_key"], "completion")
                        and not isinstance(v, dict)
                    },
                }
                if spec["name"] == "xstest_v2":
                    # XSTest v2 = 250 SAFE prompts (10 types x 25) + 200 unsafe contrast
                    # prompts (8 'contrast_*' types x 25). Over-refusal is defined on the
                    # SAFE half ONLY, so the flag is precomputed rather than left to a
                    # downstream string test that could silently invert the rule.
                    t = str(r.get("type", ""))
                    ex["metadata_xstest_type"] = t
                    ex["metadata_xstest_is_safe_item"] = not t.startswith("contrast_")
                    if r.get("completion"):
                        c = r["completion"]
                        ex["metadata_reference_completion"] = (
                            c[:FIELD_CAP] + f"...[truncated from {len(c)} chars]"
                            if len(c) > FIELD_CAP else c
                        )
                if spec["name"] == "jbb_behaviors":
                    ex["metadata_jbb_is_harmful"] = split == "harmful"
                if spec["name"] == "wildguard_test":
                    ex["metadata_is_adversarial"] = bool(r.get("adversarial"))
                examples.append(ex)
        blocks.append({"dataset": f"measurement_corpus__{spec['name']}", "examples": examples})
        stats.append({
            "corpus": spec["name"], "hf_repo": spec["hf_repo"], "url": spec["url"],
            "upstream": spec["upstream"], "axis": spec["axis"],
            "why_selected": spec["why"], "n_prompts": len(examples),
            "splits": [s for _, s in spec["files"]],
        })
        logger.info(f"corpus {spec['name']:26s} {len(examples):>6d} prompts")
    return blocks, stats


def main() -> None:
    panel = load("panel_resolved.json")
    split = load("split_assignments.json")
    prereg = load("split_prereg.json")
    cap_rows = load("capability_rows.json")
    cap_flagged = load("capability_flagged_rows.json")
    curated = load("curated_card_rows.json")
    coverage = load("coverage_stats.json")
    needs = load("in_house_measurement_list.json")
    rules = load("rules.json")
    census = load("safety_source_census.json")
    helm_overlap = load("helm_overlap.json")
    helm_ref = load("helm_reference_rows.json")
    card_scan = load("card_scan.json")

    fold = {l["lineage_id"]: l["split"] for l in split["lineages"]}
    ck_lineage = {x["hf_repo_id"]: x["lineage_id"] for x in panel}

    def f_for(lineage_id: str | None) -> str:
        return fold.get(lineage_id or "", "na")

    blocks: list[dict] = []

    def block(name: str, examples: list[dict]) -> None:
        if examples:
            blocks.append({"dataset": name, "examples": examples})
            logger.info(f"block  {name:26s} {len(examples):>6d} rows")

    # ---- A. artifact blocks ----------------------------------------------
    block("external_score", [{
        "input": f"{r['checkpoint_id']} | {r['benchmark']} | {r['metric_name']}",
        "output": f"{r['value']}",
        "metadata_row_kind": "external_score",
        "metadata_fold": f_for(r.get("lineage_id") or ck_lineage.get(r["checkpoint_id"])),
        "metadata_payload": r,
    } for r in cap_rows + curated])

    # Leaderboard rows the source itself marked Flagged: withheld from the score set
    # but shipped so the exclusion is auditable rather than silent.
    block("external_score_withheld_flagged", [{
        "input": f"{r['checkpoint_id']} | {r['benchmark']} | {r['metric_name']} | FLAGGED",
        "output": f"{r['value']}",
        "metadata_row_kind": "external_score_withheld_flagged",
        "metadata_fold": f_for(r.get("lineage_id")),
        "metadata_payload": r,
    } for r in cap_flagged])

    block("panel_checkpoint", [{
        "input": x["hf_repo_id"],
        "output": ("IN_PANEL_LE_4.2B" if x["in_panel_le_4p2b"]
                   else f"EXCLUDED:{x['panel_exclusion_reason']}"),
        "metadata_row_kind": "panel_checkpoint",
        "metadata_fold": f_for(x["lineage_id"]),
        "metadata_payload": x,
    } for x in panel])

    block("lineage", [{
        "input": l["lineage_id"],
        "output": (f"{l['architecture_family']} | hard_case={l['has_hard_case']} | "
                   f"{l['size_bucket']} | {l['n_members']} members "
                   f"({l['n_members_in_panel_le_4p2b']} in panel)"),
        "metadata_row_kind": "lineage",
        "metadata_fold": l["split"],
        "metadata_payload": {k: v for k, v in l.items() if k not in ("split", "split_reason")},
    } for l in split["lineages"]])

    block("split_assignment", [{
        "input": l["lineage_id"],
        "output": l["split"],
        "metadata_row_kind": "split_assignment",
        "metadata_fold": l["split"],
        "metadata_payload": {
            "lineage_id": l["lineage_id"], "split": l["split"],
            "split_reason": l["split_reason"],
            "stratum": [l["architecture_family"], l["has_hard_case"], l["size_bucket"]],
            "sha256_lineage_seed": l["hash"], "seed": split["seed"],
            "member_checkpoint_ids": [m["checkpoint_id"] for m in l["members"]],
            "n_members_in_panel_le_4p2b": l["n_members_in_panel_le_4p2b"],
        },
    } for l in split["lineages"]])

    cov = [{
        "input": f"{s['scope']} | {s['key']} | {s['stat']}",
        "output": (f"{s['value']}" if s["denominator"] is None
                   else f"{s['value']}/{s['denominator']}"),
        "metadata_row_kind": "coverage_stat",
        "metadata_fold": "na",
        "metadata_payload": s,
    } for s in coverage]
    for s in census:
        cov.append({
            "input": f"source_overlap | {s['source']} | panel checkpoints named in full text",
            "output": f"{s['n_panel_checkpoints_named_in_document']}/{s['n_panel_checkpoints_total']}",
            "metadata_row_kind": "coverage_stat", "metadata_fold": "na",
            "metadata_payload": {
                "scope": "source_overlap", "key": s["source"],
                "stat": "n_panel_checkpoints_named_in_document",
                "value": s["n_panel_checkpoints_named_in_document"],
                "denominator": s["n_panel_checkpoints_total"],
                "note": (f"full text scanned ({s['document_chars']} chars) from "
                         f"{s['document_fetched']}; metric would have been: "
                         f"{s['primary_metric_and_polarity']}"),
                "detail": s,
            },
        })
    for s in helm_overlap:
        cov.append({
            "input": f"source_overlap | {s['source']} | panel checkpoints evaluated",
            "output": f"{s['n_panel_checkpoints_present']}/{s['n_panel_checkpoints_total']}",
            "metadata_row_kind": "coverage_stat", "metadata_fold": "na",
            "metadata_payload": {
                "scope": "source_overlap", "key": s["source"],
                "stat": "n_panel_checkpoints_present",
                "value": s["n_panel_checkpoints_present"],
                "denominator": s["n_panel_checkpoints_total"],
                "note": (f"source evaluates {s['n_models_source_evaluates']} models in "
                         f"total over run groups {s['run_groups']}"),
                "detail": s,
            },
        })
    block("coverage_stat", cov)

    block("in_house_measurement_required", [{
        "input": n["checkpoint_id"],
        "output": ",".join(n["axes_requiring_in_house_measurement"]),
        "metadata_row_kind": "in_house_measurement_required",
        "metadata_fold": f_for(n["lineage_id"]),
        "metadata_payload": n,
    } for n in needs])

    block("rule", [{
        "input": r["rule_id"],
        "output": r.get("disqualify_if") or r["predicate"][:200],
        "metadata_row_kind": "rule", "metadata_fold": "na", "metadata_payload": r,
    } for r in rules])

    block("prereg_statement", [{
        "input": "PRE_REGISTRATION_OF_FROZEN_SPLIT",
        "output": (f"frozen {prereg['frozen_at_utc']} | seed {prereg['seed']} | "
                   f"{prereg['n_dev']} dev / {prereg['n_heldout']} heldout | "
                   f"sha256 {prereg['split_file_sha256']}"),
        "metadata_row_kind": "prereg_statement", "metadata_fold": "na",
        "metadata_payload": prereg,
    }])

    block("helm_reference_non_panel", [{
        "input": f"{r['source']} | {r['model_as_named_by_source']} | {r['run_group']} | {r['metric_name']}",
        "output": f"{r['value']}",
        "metadata_row_kind": "helm_reference_non_panel", "metadata_fold": "na",
        "metadata_payload": r,
    } for r in helm_ref])

    block("model_card_scan", [{
        "input": r["checkpoint_id"],
        "output": (f"{len(r['hits'])} safety-keyword-near-numeric candidate hits; "
                   f"card {r['card_chars']} chars; HTTP {r['http_status']}"),
        "metadata_row_kind": "model_card_scan",
        "metadata_fold": f_for(ck_lineage.get(r["checkpoint_id"])),
        "metadata_payload": r,
    } for r in card_scan])

    n_artifact = sum(len(b["examples"]) for b in blocks)

    # ---- B. measurement corpora ------------------------------------------
    corpus_blocks, corpus_stats = build_corpus_blocks()
    blocks.extend(corpus_blocks)
    n_prompts = sum(s["n_prompts"] for s in corpus_stats)

    n_rows = sum(len(b["examples"]) for b in blocks)
    hs = {s["stat"]: s for s in coverage}
    metadata = {
        "name": "external safety/capability ground truth + frozen lineage split + "
                "in-house measurement corpora (iteration 2)",
        "version": "2.0.0",
        "built_utc": datetime.now(timezone.utc).isoformat(),
        "retrieval_date": RETRIEVAL_DATE,
        "n_rows": n_rows,
        "n_artifact_rows": n_artifact,
        "n_measurement_prompts": n_prompts,
        "row_kinds": {b["dataset"]: len(b["examples"]) for b in blocks},
        "panel_provenance": {
            "source": "iteration-1 frozen panel manifest, reused across runs",
            "path": ("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/"
                     "gen_art/gen_art_dataset_1/full_data_out.json -> "
                     "datasets[dataset='panel_manifest']"),
            "n_checkpoints_in_frozen_manifest": len(panel),
            "n_lineages_in_frozen_manifest": len({x["lineage_id"] for x in panel}),
            "n_checkpoints_le_4p2b": sum(1 for x in panel if x["in_panel_le_4p2b"]),
            "n_lineages_le_4p2b": len({x["lineage_id"] for x in panel if x["in_panel_le_4p2b"]}),
            "correction_to_the_plan": (
                "The plan described the frozen panel as '137 checkpoints / 93 lineages'. "
                "The manifest actually holds 160 checkpoints over 105 lineages; the <=4.2B "
                "restriction leaves 66 checkpoints over 34 lineages. No rebuild was needed "
                "-- the frozen manifest was found and used as-is -- but its counts are "
                "reported as measured, not as the plan remembered them."
            ),
            "param_count_correction": (
                "The manifest's own param_count was derived from on-disk bytes and "
                "double-counts repos that ship both .safetensors and a duplicate .pth/.bin "
                "copy (meta-llama/Llama-3.2-1B reads 2.47B there vs 1.24B in the safetensors "
                "header). Every checkpoint was therefore re-resolved from the HF Hub; "
                "param_count_manifest is kept alongside and param_manifest_disagrees flags "
                "the 27 disagreements."
            ),
        },
        "headline_coverage": {
            "n_checkpoints_le_4p2b": hs["n_checkpoints_le_4p2b"]["value"],
            "n_lineages_le_4p2b": hs["n_lineages_le_4p2b"]["value"],
            "checkpoints_with_any_external_SAFETY_number":
                f"{hs['n_checkpoints_with_ge1_ANY_SAFETY']['value']}/"
                f"{hs['n_checkpoints_with_ge1_ANY_SAFETY']['denominator']}",
            "lineages_with_any_external_SAFETY_number":
                f"{hs['n_lineages_with_ge1_ANY_SAFETY']['value']}/"
                f"{hs['n_lineages_with_ge1_ANY_SAFETY']['denominator']}",
            "checkpoints_with_external_OVER_REFUSAL_number":
                f"{hs['n_checkpoints_with_ge1_SAFETY_OVERREFUSAL']['value']}/"
                f"{hs['n_checkpoints_with_ge1_SAFETY_OVERREFUSAL']['denominator']}",
            "checkpoints_with_any_external_CAPABILITY_number":
                f"{hs['n_checkpoints_with_ge1_CAPABILITY']['value']}/"
                f"{hs['n_checkpoints_with_ge1_CAPABILITY']['denominator']}",
            "n_checkpoints_requiring_in_house_safety_measurement":
                hs["n_checkpoints_requiring_in_house_safety_measurement"]["value"],
            "published_safety_benchmarks_with_ZERO_panel_overlap": [
                s["source"] for s in census if s["n_panel_checkpoints_named_in_document"] == 0
            ] + [s["source"] for s in helm_overlap if s["n_panel_checkpoints_present"] == 0],
            "verdict": (
                "The external-ground-truth axis is COVERAGE-LIMITED at this scale. Ten "
                "published safety benchmarks plus HELM Safety v1.0.0 and AIR-Bench 2024 "
                "were checked programmatically and every one of them names ZERO of the 66 "
                "panel checkpoints. The only external safety numbers that exist are stated "
                "on two model cards (Qwen3-4B-SafeRL, Gemma 2 IT 2B). The hypothesis's "
                "documented fallback -- two in-house refusal rates, harmful-prompt refusal "
                "and XSTest-style harmless-but-alarming refusal, with the R4 evaluator "
                "system prompt in force -- therefore becomes PRIMARY for the uncovered "
                "checkpoints, which is why the 10 measurement corpora are shipped here "
                "rather than left to be re-sourced. Capability, by contrast, is dense: the "
                "Open LLM Leaderboard covers roughly half the panel and is the confound "
                "control."
            ),
        },
        "split": {
            "seed": split["seed"],
            "frozen_at_utc": prereg["frozen_at_utc"],
            "split_file_sha256": prereg["split_file_sha256"],
            "n_dev": split["n_dev"], "n_heldout": split["n_heldout"],
            "heldout_fraction": round(split["n_heldout"] / split["n_lineages_total"], 4),
            "families_absent_from_dev": split["families_absent_from_dev"],
            "forced_heldout_families": split["forced_heldout_families"],
            "forced_dev_lineages": split["forced_dev_lineages"],
            "rule_text": split["rule_text"],
        },
        "rules": [r["rule_id"] for r in rules],
        "corpus_selection": {
            "n_pinned": 16,
            "n_selected": len(CORPORA),
            "criterion": (
                "An instrument for BOTH safety sub-axes the hypothesis needs (harm-refusal "
                "and over-refusal), preference for corpora whose grader or metric already "
                "appears in our external rows so an in-house number can be checked against "
                "a published one, category structure for per-harm breakdowns, and no bulk "
                "that buys no measurement."
            ),
            "selected": corpus_stats,
            "rejected": REJECTED,
        },
        "caches": {
            "cache/cards/": "verbatim README.md of every panel checkpoint",
            "cache/helm/": "HELM Safety + AIR-Bench schema and group JSON",
            "cache/safety_sources/": "full text of the 10 published safety benchmark documents",
            "cache/*.parquet": "Open LLM Leaderboard v1/v2 contents snapshots",
            "temp/datasets/": "all 16 pinned HF datasets, including the 6 not selected",
        },
    }

    out = {"metadata": metadata, "datasets": blocks}
    (HERE / "full_data_out.json").write_text(json.dumps(out, indent=1))
    logger.info(f"Wrote full_data_out.json: {n_rows} rows over {len(blocks)} blocks "
                f"({n_artifact} artifact rows + {n_prompts} measurement prompts)")


if __name__ == "__main__":
    main()
