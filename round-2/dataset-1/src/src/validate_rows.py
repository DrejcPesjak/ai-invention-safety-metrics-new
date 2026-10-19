#!/usr/bin/env python3
"""Validate full_data_out.json against schema_row_kinds.json.

Two passes:
  1. the envelope + metadata_fold enum, straight from the schema;
  2. each row_kind's metadata_payload against the matching entry in `definitions`,
     which is the part the generic exp_sel_data_out schema cannot check.

Plus artifact-specific invariants that no JSON Schema can express:
  - every external_score row's verbatim_snippet is non-empty and <=300 chars;
  - every external_score value is a finite number;
  - every SAFETY_* row carries an explicit polarity that is not a capability polarity;
  - every lineage appears exactly once in split_assignment and no lineage straddles;
  - the split file's sha256 still matches the pre-registration statement.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft7Validator
from loguru import logger

HERE = Path(__file__).resolve().parent.parent
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

SAFETY_POLARITIES = {"HIGHER_IS_SAFER", "LOWER_IS_SAFER"}


def main() -> int:
    data = json.loads((HERE / "full_data_out.json").read_text())
    schema = json.loads((HERE / "schema_row_kinds.json").read_text())
    errors: list[str] = []

    top = {k: v for k, v in schema.items() if k != "definitions"}
    for e in Draft7Validator(top).iter_errors(data):
        errors.append(f"envelope: {'/'.join(str(p) for p in e.path)}: {e.message}")

    defs = schema["definitions"]
    counts: Counter = Counter()
    for block in data["datasets"]:
        kind = block["dataset"]

        # Measurement-corpus blocks use flat metadata_* fields instead of
        # metadata_payload, so they get their own invariants: a non-empty prompt, a
        # corpus tag, and no accidental score-shaped fields (these are prompts that
        # nothing has been measured on yet, and a stray 'value' would invite a
        # downstream script to treat them as external scores).
        if kind.startswith("measurement_corpus__"):
            corpus = kind.split("measurement_corpus__", 1)[1]
            seen_idx = set()
            for i, ex in enumerate(block["examples"]):
                counts[kind] += 1
                if not ex["input"].strip():
                    errors.append(f"{kind}[{i}]: empty prompt")
                if ex.get("metadata_corpus") != corpus:
                    errors.append(f"{kind}[{i}]: metadata_corpus "
                                  f"{ex.get('metadata_corpus')!r} != {corpus!r}")
                if ex["metadata_fold"] != "na":
                    errors.append(f"{kind}[{i}]: corpus prompts belong to no lineage, "
                                  f"so metadata_fold must be 'na', got {ex['metadata_fold']!r}")
                for bad in ("metadata_value", "metadata_polarity", "metadata_payload"):
                    if bad in ex:
                        errors.append(f"{kind}[{i}]: score-shaped field {bad!r} on a prompt row")
                key = (ex.get("metadata_split"), ex.get("metadata_row_index"))
                if key in seen_idx:
                    errors.append(f"{kind}[{i}]: duplicate (split, row_index) {key}")
                seen_idx.add(key)
            continue

        v = Draft7Validator(defs[kind]) if kind in defs else None
        for i, ex in enumerate(block["examples"]):
            counts[kind] += 1
            p = ex["metadata_payload"]
            if v is not None:
                for e in v.iter_errors(p):
                    errors.append(f"{kind}[{i}]: {'/'.join(str(x) for x in e.path)}: {e.message}")
            if kind == "external_score":
                s = p.get("verbatim_snippet", "")
                if not s or len(s) > 300:
                    errors.append(f"{kind}[{i}] {p.get('checkpoint_id')}: bad verbatim_snippet len={len(s)}")
                if not isinstance(p.get("value"), (int, float)) or not math.isfinite(p["value"]):
                    errors.append(f"{kind}[{i}] {p.get('checkpoint_id')}: non-finite value")
                if p.get("axis", "").startswith("SAFETY_HARM") or p.get("axis") == "SAFETY_OVERREFUSAL":
                    if p.get("polarity") not in SAFETY_POLARITIES:
                        errors.append(
                            f"{kind}[{i}] {p.get('checkpoint_id')}/{p.get('benchmark')}: "
                            f"safety axis with non-safety polarity {p.get('polarity')!r}"
                        )
                    if not p.get("polarity_evidence"):
                        errors.append(
                            f"{kind}[{i}] {p.get('checkpoint_id')}/{p.get('benchmark')}: "
                            "safety row without polarity_evidence"
                        )

    blocks = {b["dataset"]: b["examples"] for b in data["datasets"]}

    # XSTest's safe/unsafe halves are load-bearing: over-refusal is defined on the
    # SAFE half only, so a wrong flag would silently invert the disqualification rule.
    xs = blocks.get("measurement_corpus__xstest_v2", [])
    per_split = Counter((e["metadata_split"], e["metadata_xstest_is_safe_item"]) for e in xs)
    for sp in {e["metadata_split"] for e in xs}:
        n_safe, n_unsafe = per_split[(sp, True)], per_split[(sp, False)]
        if (n_safe, n_unsafe) != (250, 200):
            errors.append(f"xstest_v2/{sp}: {n_safe} safe + {n_unsafe} unsafe, expected 250 + 200")
    lin_ids = [e["metadata_payload"]["lineage_id"] for e in blocks["lineage"]]
    split_ids = [e["metadata_payload"]["lineage_id"] for e in blocks["split_assignment"]]
    if sorted(lin_ids) != sorted(split_ids):
        errors.append("lineage and split_assignment do not cover the same lineage set")
    dup = [k for k, n in Counter(split_ids).items() if n > 1]
    if dup:
        errors.append(f"lineages assigned more than once: {dup}")

    fold_of = {e["metadata_payload"]["lineage_id"]: e["metadata_payload"]["split"]
               for e in blocks["split_assignment"]}
    for b in data["datasets"]:
        for e in b["examples"]:
            lid = e.get("metadata_payload", {}).get("lineage_id")
            if lid and lid in fold_of and e["metadata_fold"] not in (fold_of[lid], "na"):
                errors.append(
                    f"{b['dataset']}: metadata_fold {e['metadata_fold']!r} contradicts the "
                    f"split of lineage {lid} ({fold_of[lid]!r})"
                )

    # The disqualification threshold is grounded in XSTest Table 1; re-derive the
    # grounding straight from the shipped per-item annotations so the rule and the
    # corpus can never drift apart inside the same file.
    rule = next(e["metadata_payload"] for e in blocks["rule"]
                if e["metadata_payload"]["rule_id"] == "BLANKET_REFUSER_DISQUALIFICATION")
    for rep in rule["threshold_grounding"]["reproduced_from_released_per_item_annotations"]:
        sp = "annotated_" + rep["xstest_split"]
        safe = [e for e in xs if e["metadata_split"] == sp and e["metadata_xstest_is_safe_item"]]
        if not safe:
            errors.append(f"rule grounding references xstest split {sp!r}, absent from the corpus")
            continue
        full = sum(1 for e in safe if e["output"] == "2_full_refusal") / len(safe)
        part = sum(1 for e in safe if e["output"] == "3_partial_refusal") / len(safe)
        if abs(full - rep["full_refusal_rate_on_safe"]) > 1e-6 or \
           abs(part - rep["partial_refusal_rate_on_safe"]) > 1e-6:
            errors.append(
                f"rule grounding for {sp} ({rep['full_refusal_rate_on_safe']}, "
                f"{rep['partial_refusal_rate_on_safe']}) disagrees with the shipped "
                f"corpus ({full:.4f}, {part:.4f})"
            )

    prereg = blocks["prereg_statement"][0]["metadata_payload"]
    blob = (HERE / "results" / "split_assignments.json").read_text()
    digest = hashlib.sha256(blob.encode()).hexdigest()
    if digest != prereg["split_file_sha256"]:
        errors.append(
            f"split file has been EDITED since pre-registration: sha256 {digest} != "
            f"{prereg['split_file_sha256']}"
        )

    logger.info(f"rows by kind: {dict(counts)}")
    if errors:
        for e in errors[:40]:
            logger.error(e)
        logger.error(f"{len(errors)} validation error(s)")
        return 1
    logger.info("ALL CHECKS PASSED (envelope, per-row-kind payloads, artifact invariants, "
                "split sha256 vs pre-registration)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
