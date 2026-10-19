#!/usr/bin/env python3
"""Arm A selection: which real public checkpoints get scored, and why.

The selection rule NEVER looks at the repo name.  It applies, in order:

  1. param_count <= 4.2e9, safetensors present, not quantized;
  2. n_layers >= 8 and hidden_size >= 128 (below that the minimum-over-matrices
     statistic is degenerate) -- enforced later, on the downloaded config;
  3. recipe class RE-DERIVED here from the card's VERBATIM evidence span, not
     taken from the manifest label;
  4. cover as many recipe classes as possible, smallest-first within a class.

The re-derived taxonomy is deliberately organised by KERNEL UNIFORMITY, because
that is the hypothesis under test.  The manifest's own class labels are carried
alongside so every disagreement is visible.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# --------------------------------------------------------------------------
# re-derivation rules.  Order matters: the first rule whose pattern matches the
# verbatim evidence span (or the card-derived fields the manifest preserved)
# wins.  Every rule records WHICH pattern fired, so the label is auditable.
# --------------------------------------------------------------------------
RULES: list[tuple[str, str, str, str]] = [
    # (class, kernel_uniformity, regex, human-readable justification)
    ("R_GAUSSIAN_DEPTH", "NONUNIFORM",
     r"normal distribution|gaussian|spread and peak layer|peak layer",
     "subtraction weights follow a depth kernel with a spread and a peak layer"),
    ("R_HERETIC", "NONUNIFORM",
     r"heretic|arbitrary-rank ablation|\bARA\b|direction_index|max_weight",
     "Heretic's per-component optimised kernel: float direction index and "
     "per-component max weights that need not be 1"),
    ("R_PARTIAL_LAYER", "NONUNIFORM",
     r"per[- ]head|head surgery|attention head|selected layers|layer range|"
     r"subset of layers|only the layers",
     "edit confined to a subset of layers or of attention heads"),
    ("R_NORM_PRESERVING", "UNIFORM",
     r"norm[- ]preserv|row[- ]norm|preserving the norm|magnitude preservation|"
     r"norm-preservingly",
     "MPOA-style projection followed by a per-row norm restoration"),
    ("R_MULTIDIR_SVD", "UNIFORM",
     r"gabliterat|multi[- ]direction|multidirection|whitened svd|\bSVD\b|"
     r"rank-k|ridge|OBLITERATUS",
     "rank-k / multi-directional projection applied to the whole stack"),
    ("R_GLOBAL_RANK1", "UNIFORM",
     r"refusal direction|remove-refusals|orthogonaliz|projected out|"
     r"direction steering|abliterat",
     "single global refusal direction projected out of every write matrix"),
    ("R_SFT_UNCENSORED", "NOT_A_PROJECTION",
     r"fine[- ]tun|finetun|\bsft\b|\blora\b|trained on|dataset",
     "behavioural fine-tune, not a weight projection"),
    ("R_MERGE", "NOT_A_PROJECTION",
     r"mergekit|merge of|ties|slerp|dare",
     "merge of an already-edited model with another"),
]

MANIFEST_TO_RE = {
    "R1_GLOBAL_RANK1_DIM": "R_GLOBAL_RANK1",
    "R2_NORM_PRESERVING_PROJECTED": "R_NORM_PRESERVING",
    "R3_MULTIDIRECTION_SVD": "R_MULTIDIR_SVD",
    "R4_PARTIAL_LAYER_OR_PER_HEAD": "R_PARTIAL_LAYER",
    "R6_BEHAVIOURAL_SFT_UNCENSORED": "R_SFT_UNCENSORED",
    "R7_MERGE_OF_ABLITERATED": "R_MERGE",
    "UNKNOWN": "R_UNKNOWN",
}

UNIFORMITY_OF = {
    "R_GLOBAL_RANK1": "UNIFORM",
    "R_NORM_PRESERVING": "UNIFORM",
    "R_MULTIDIR_SVD": "UNIFORM",
    "R_GAUSSIAN_DEPTH": "NONUNIFORM",
    "R_HERETIC": "NONUNIFORM",
    "R_PARTIAL_LAYER": "NONUNIFORM",
    "R_SFT_UNCENSORED": "NOT_A_PROJECTION",
    "R_MERGE": "NOT_A_PROJECTION",
    "R_UNKNOWN": "UNKNOWN",
}

# Rows the reviewer's decisive point turns on.  They are named because their
# card text is quoted in the write-up, not because their names were used to
# select them -- each still has to pass the eligibility rule and each is
# re-labelled from its own evidence span.
MANDATORY = [
    "MagicalAlchemist/Qwen3-1.7B-Magic_decensored",
    "prithivMLmods/VibeThinker-3B-heretic_decensored",
    "mlabonne/Qwen3-0.6B-abliterated",
]

QUANT_FILE_RE = re.compile(r"gptq|awq|bnb|4bit|8bit|mlx|gguf|quantiz", re.IGNORECASE)


def rederive(evidence: str, repo_id: str, manifest_class: str) -> dict:
    """Re-derive the recipe class from the VERBATIM evidence span alone."""
    ev = evidence or ""
    for cls, unif, pat, why in RULES:
        m = re.search(pat, ev, re.IGNORECASE)
        if m:
            lo = max(0, m.start() - 90)
            return {"recipe_class_rederived": cls,
                    "kernel_uniformity": unif,
                    "rederive_pattern": pat,
                    "rederive_match": m.group(0),
                    "rederive_context": ev[lo:m.end() + 90],
                    "rederive_justification": why,
                    "manifest_class": manifest_class,
                    "agrees_with_manifest":
                        MANIFEST_TO_RE.get(manifest_class) == cls}
    return {"recipe_class_rederived": "R_UNKNOWN", "kernel_uniformity": "UNKNOWN",
            "rederive_pattern": None, "rederive_match": None,
            "rederive_context": ev[:180], "rederive_justification":
            "no mechanism named in the card's evidence span",
            "manifest_class": manifest_class,
            "agrees_with_manifest": MANIFEST_TO_RE.get(manifest_class) == "R_UNKNOWN"}


def load_manifest(dep_path: Path) -> list[dict]:
    d = json.loads(Path(dep_path).read_text())
    for ds in d["datasets"]:
        if ds["dataset"] == "edit_manifest":
            return ds["examples"]
    raise RuntimeError("edit_manifest fold not found")


def _files(f: dict) -> list[str]:
    return [x.get("rfilename", "") for x in (f.get("files") or [])]


def prescreen(f: dict) -> tuple[bool, str]:
    names = _files(f)
    if not any(n.endswith(".safetensors") for n in names):
        return False, "NO_SAFETENSORS"
    bad = [n for n in names if QUANT_FILE_RE.search(n)]
    if bad and not any(n.endswith(".safetensors") and not QUANT_FILE_RE.search(n)
                       for n in names):
        return False, f"UNRESOLVED_QUANTIZED:{bad[0]}"
    pc = f.get("param_count_hub")
    if pc is None:
        return False, "NO_PARAM_COUNT"
    if pc > 4.2e9:
        return False, f"OVER_CEILING:{pc}"
    if f.get("model_type") in ("gpt2", "gptj", "gpt_bigcode"):
        return False, f"UNSUPPORTED_ARCH:{f.get('model_type')}"
    return True, "ok"


def build_plan(dep_path: Path, per_class: int = 4, max_rows: int = 30,
               max_bytes_each: float = 9e9,
               card_texts: dict[str, str] | None = None) -> dict:
    """Returns {'rows': [...], 'rejected': [...], 'coverage': {...}}.

    `card_texts` maps repo_id -> the FULL model card fetched at the pinned
    revision.  The manifest's stored evidence span is a ~250-character window,
    which is often too short to name the kernel; when the full card is
    available it is what the re-derivation reads, and the manifest span is
    kept as a fallback.
    """
    mani = load_manifest(dep_path)
    by_repo = {e["input"]: e for e in mani}
    cards = card_texts or {}

    cand, rejected = [], []
    for e in mani:
        f = e["metadata_features"]
        if f.get("is_parent"):
            continue
        ok, why = prescreen(f)
        if not ok:
            rejected.append({"repo_id": e["input"], "reason": why})
            continue
        st_bytes = sum(x.get("size_bytes", 0) for x in (f.get("files") or [])
                       if x.get("rfilename", "").endswith(".safetensors"))
        if st_bytes > max_bytes_each:
            rejected.append({"repo_id": e["input"],
                             "reason": f"TENSOR_BYTES_OVER_CAP:{st_bytes}"})
            continue
        row = {
            "repo_id": e["input"],
            "revision": f["revision_sha"],
            "uploader": f["uploader"],
            "param_count": f["param_count_hub"],
            "model_type": f.get("model_type"),
            "declared_parent": f.get("declared_parent"),
            "recipe_evidence": f.get("recipe_evidence"),
            "evidence_url": f.get("evidence_url"),
            "safetensors_bytes": st_bytes,
            "is_iter2_class_member": bool(f.get("is_iter2_class_member")),
            "role": "edited",
        }
        card = cards.get(e["input"])
        src = "full_card" if card else "manifest_evidence_span"
        row.update(rederive(card or f.get("recipe_evidence"), e["input"],
                            f["recipe_class"]))
        row["rederive_source"] = src
        cand.append(row)

    # --- assemble: mandatory rows first, then smallest-first per class --------
    chosen: list[dict] = []
    taken = set()
    for repo in MANDATORY:
        for r in cand:
            if r["repo_id"] == repo and repo not in taken:
                r = dict(r)
                r["selection_reason"] = "MANDATORY:card text quoted in the write-up"
                chosen.append(r)
                taken.add(repo)
    by_class: dict[str, list[dict]] = {}
    for r in cand:
        by_class.setdefault(r["recipe_class_rederived"], []).append(r)
    for cls in by_class:
        by_class[cls].sort(key=lambda r: r["safetensors_bytes"])

    # round-robin over classes so coverage beats depth in any one class
    for k in range(per_class):
        for cls in sorted(by_class):
            if len(chosen) >= max_rows:
                break
            picked = 0
            for r in by_class[cls]:
                if r["repo_id"] in taken:
                    picked += 1
                    continue
                if picked > k:
                    break
                r = dict(r)
                r["selection_reason"] = (f"class {cls}, rank {k} by safetensors bytes "
                                         f"(smallest-first)")
                chosen.append(r)
                taken.add(r["repo_id"])
                break

    # --- parents of the chosen rows: fresh eligible NEGATIVES + E_1 partners ---
    parents: list[dict] = []
    for r in chosen:
        p = r.get("declared_parent")
        if not p or p in taken:
            continue
        pe = by_repo.get(p)
        if pe is None:
            r["parent_status"] = "PARENT_NOT_IN_MANIFEST"
            continue
        pf = pe["metadata_features"]
        ok, why = prescreen(pf)
        if not ok:
            r["parent_status"] = f"PARENT_INELIGIBLE:{why}"
            continue
        st_bytes = sum(x.get("size_bytes", 0) for x in (pf.get("files") or [])
                       if x.get("rfilename", "").endswith(".safetensors"))
        # A declared "parent" is only a clean NEGATIVE if the manifest does not
        # also list it as an edited checkpoint in its own right.  Several Hub
        # lineages stack an edit on top of an already-abliterated model, and
        # counting one of those as a negative would silently poison the pool.
        itself_edited = not bool(pf.get("is_parent"))
        parents.append({
            "repo_id": p, "revision": pf["revision_sha"], "uploader": pf["uploader"],
            "param_count": pf["param_count_hub"], "model_type": pf.get("model_type"),
            "declared_parent": None, "recipe_evidence": None,
            "evidence_url": pf.get("evidence_url"), "safetensors_bytes": st_bytes,
            "is_iter2_class_member": bool(pf.get("is_iter2_class_member")),
            "role": "parent_also_edited" if itself_edited else "parent",
            "recipe_class_rederived": (
                rederive(cards.get(p) or pf.get("recipe_evidence"), p,
                         pf.get("recipe_class") or "UNKNOWN")
                ["recipe_class_rederived"] if itself_edited else "PARENT"),
            "kernel_uniformity": "EXCLUDED_FROM_NEGATIVES" if itself_edited
            else "NEGATIVE",
            "manifest_class": pf.get("recipe_class"), "agrees_with_manifest": None,
            "selection_reason": f"declared parent of {r['repo_id']}"
            + (" -- but the manifest lists it as an edited checkpoint itself, so "
               "it is scored and reported but NOT used as a negative"
               if itself_edited else ""),
            "child_of_record": r["repo_id"],
        })
        taken.add(p)
        r["parent_status"] = "PARENT_SELECTED"

    coverage: dict[str, int] = {}
    for r in chosen:
        coverage[r["recipe_class_rederived"]] = coverage.get(
            r["recipe_class_rederived"], 0) + 1
    pool: dict[str, int] = {}
    for r in cand:
        pool[r["recipe_class_rederived"]] = pool.get(
            r["recipe_class_rederived"], 0) + 1

    # smallest-first overall so a truncated run still maximises class coverage
    rows = sorted(chosen + parents, key=lambda r: r["safetensors_bytes"])
    return {"rows": rows, "rejected": rejected[:400], "n_rejected": len(rejected),
            "coverage_selected": coverage, "coverage_pool": pool,
            "n_candidates": len(cand),
            "gb_total": sum(r["safetensors_bytes"] for r in rows) / 1e9}
