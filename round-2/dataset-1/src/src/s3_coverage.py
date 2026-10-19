#!/usr/bin/env python3
"""Stage 3: the coverage report.

Merges the capability rows (s1), the HELM/AIR-Bench overlap census (s2b), the
published-safety-benchmark census (s2c) and the curated model-card rows (s2d) into
one honest account of what external ground truth actually exists for the <=4.2B
panel, broken down by axis, architecture family, size bucket and revision match,
at BOTH checkpoint and lineage level (iteration 3 bootstraps over lineages, so the
two counts are not interchangeable).

Also emits the machine-readable list of checkpoints that will REQUIRE in-house
measurement because no external safety number exists for them.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent.parent
RESULTS, LOGS = HERE / "results", HERE / "logs"
LOGS.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "s3_coverage.log"), rotation="30 MB", level="DEBUG")

SAFETY_AXES = ("SAFETY_HARM", "SAFETY_OVERREFUSAL", "SAFETY_OTHER")


def size_bucket(params: int) -> str:
    if params < 1_000_000_000:
        return "<1B"
    if params < 2_000_000_000:
        return "1-2B"
    return "2-4.2B"


def arch_family(rec: dict) -> str:
    """Architecture family for stratification.

    Derived from the config model_type where the Hub exposes one, falling back to
    the lineage's own model_type, then to the lineage owner. Kept coarse on purpose:
    it is a stratification key, not a taxonomy.
    """
    mt = rec.get("model_type")
    if mt:
        return str(mt)
    return "unknown:" + rec["lineage_id"].split("/")[0].lower()


def main() -> None:
    panel = [x for x in json.loads((RESULTS / "panel_resolved.json").read_text())
             if x["in_panel_le_4p2b"]]
    by_id = {x["hf_repo_id"]: x for x in panel}

    # Fill missing model_type from a same-lineage sibling before stratifying, so a
    # quantised/gated repo does not become its own singleton family.
    lin_mt: dict[str, str] = {}
    for x in panel:
        if x.get("model_type"):
            lin_mt.setdefault(x["lineage_id"], x["model_type"])
    for x in panel:
        if not x.get("model_type") and x["lineage_id"] in lin_mt:
            x["model_type"] = lin_mt[x["lineage_id"]]
            x["model_type_source"] = "INFERRED_FROM_LINEAGE_SIBLING"

    rows = (json.loads((RESULTS / "capability_rows.json").read_text())
            + json.loads((RESULTS / "curated_card_rows.json").read_text()))
    panel_rows = [r for r in rows if r["checkpoint_id"] in by_id]
    off_panel = sorted({r["checkpoint_id"] for r in rows if r["checkpoint_id"] not in by_id})
    logger.info(f"{len(rows)} external_score rows; {len(panel_rows)} attach to a "
                f"<=4.2B panel checkpoint; off-panel augmentation checkpoints: {off_panel}")

    axes_by_ckpt: dict[str, set] = defaultdict(set)
    axes_by_lineage: dict[str, set] = defaultdict(set)
    for r in panel_rows:
        axes_by_ckpt[r["checkpoint_id"]].add(r["axis"])
        axes_by_lineage[by_id[r["checkpoint_id"]]["lineage_id"]].add(r["axis"])

    lineages = sorted({x["lineage_id"] for x in panel})
    stats: list[dict] = []

    def add(scope: str, key: str, stat: str, value, denom=None, note: str = "") -> None:
        stats.append({"scope": scope, "key": key, "stat": stat, "value": value,
                      "denominator": denom, "note": note})

    add("panel", "ALL", "n_checkpoints_le_4p2b", len(panel))
    add("panel", "ALL", "n_lineages_le_4p2b", len(lineages))
    add("panel", "ALL", "n_external_score_rows_attached_to_panel", len(panel_rows))

    for axis in ("CAPABILITY",) + SAFETY_AXES:
        n = sum(1 for c in panel if axis in axes_by_ckpt[c["hf_repo_id"]])
        nl = sum(1 for l in lineages if axis in axes_by_lineage[l])
        add("panel", "ALL", f"n_checkpoints_with_ge1_{axis}", n, len(panel))
        add("panel", "ALL", f"n_lineages_with_ge1_{axis}", nl, len(lineages))

    any_safety_c = [c["hf_repo_id"] for c in panel
                    if axes_by_ckpt[c["hf_repo_id"]] & set(SAFETY_AXES)]
    any_safety_l = [l for l in lineages if axes_by_lineage[l] & set(SAFETY_AXES)]
    add("panel", "ALL", "n_checkpoints_with_ge1_ANY_SAFETY", len(any_safety_c), len(panel))
    add("panel", "ALL", "n_lineages_with_ge1_ANY_SAFETY", len(any_safety_l), len(lineages))

    for stat, ctr in (("revision_match", Counter(r["revision_match"] for r in panel_rows)),
                      ("source_type", Counter(r["source_type"] for r in panel_rows)),
                      ("axis", Counter(r["axis"] for r in panel_rows))):
        for k, v in sorted(ctr.items()):
            add("rows", k, f"n_rows_by_{stat}", v, len(panel_rows))

    for dim, fn in (("architecture_family", arch_family),
                    ("size_bucket", lambda x: size_bucket(x["param_count_resolved"]))):
        groups: dict[str, list] = defaultdict(list)
        for c in panel:
            groups[fn(c)].append(c)
        for g, members in sorted(groups.items()):
            ids = [m["hf_repo_id"] for m in members]
            add(dim, g, "n_checkpoints", len(ids))
            add(dim, g, "n_with_ge1_CAPABILITY",
                sum(1 for i in ids if "CAPABILITY" in axes_by_ckpt[i]), len(ids))
            add(dim, g, "n_with_ge1_ANY_SAFETY",
                sum(1 for i in ids if axes_by_ckpt[i] & set(SAFETY_AXES)), len(ids))
            add(dim, g, "n_with_ge1_SAFETY_OVERREFUSAL",
                sum(1 for i in ids if "SAFETY_OVERREFUSAL" in axes_by_ckpt[i]), len(ids))

    # Per-source overlap, measured not asserted.
    for blob, label in ((RESULTS / "capability_source_overlap.json", "capability"),
                        (RESULTS / "helm_overlap.json", "helm")):
        for s in json.loads(blob.read_text()):
            add("source_overlap", s["source"], "n_panel_checkpoints_present",
                s["n_panel_checkpoints_present"], s["n_panel_checkpoints_total"],
                f"source evaluates {s['n_models_source_evaluates']} models in total")
    for s in json.loads((RESULTS / "safety_source_census.json").read_text()):
        add("source_overlap", s["source"], "n_panel_checkpoints_named_in_document",
            s["n_panel_checkpoints_named_in_document"], s["n_panel_checkpoints_total"],
            f"full text scanned ({s['document_chars']} chars); "
            f"metric would have been: {s['primary_metric_and_polarity']}")

    # Checkpoints that iteration 3 must measure in-house, and on which axes.
    needs = []
    for c in panel:
        have = axes_by_ckpt[c["hf_repo_id"]]
        missing = [a for a in ("SAFETY_HARM", "SAFETY_OVERREFUSAL") if a not in have]
        if missing:
            needs.append({
                "checkpoint_id": c["hf_repo_id"],
                "lineage_id": c["lineage_id"],
                "member_class": c["member_class"],
                "architecture_family": arch_family(c),
                "param_count": c["param_count_resolved"],
                "size_bucket": size_bucket(c["param_count_resolved"]),
                "axes_already_covered_externally": sorted(have),
                "axes_requiring_in_house_measurement": missing,
                "weight_format": c.get("weight_format", "SAFETES/UNKNOWN"),
            })
    add("panel", "ALL", "n_checkpoints_requiring_in_house_safety_measurement", len(needs), len(panel))

    (RESULTS / "coverage_stats.json").write_text(json.dumps(stats, indent=1))
    (RESULTS / "in_house_measurement_list.json").write_text(json.dumps(needs, indent=1))

    hs = next(s for s in stats if s["stat"] == "n_checkpoints_with_ge1_ANY_SAFETY")
    logger.info(f"HEADLINE safety coverage: {hs['value']}/{hs['denominator']} checkpoints "
                f"= {100 * hs['value'] / hs['denominator']:.1f}%")
    ls = next(s for s in stats if s["stat"] == "n_lineages_with_ge1_ANY_SAFETY")
    logger.info(f"HEADLINE lineage-level safety coverage: {ls['value']}/{ls['denominator']} "
                f"= {100 * ls['value'] / ls['denominator']:.1f}%")
    cs = next(s for s in stats if s["stat"] == "n_checkpoints_with_ge1_CAPABILITY")
    logger.info(f"Capability coverage: {cs['value']}/{cs['denominator']} "
                f"= {100 * cs['value'] / cs['denominator']:.1f}%")
    orr = next(s for s in stats if s["stat"] == "n_checkpoints_with_ge1_SAFETY_OVERREFUSAL")
    logger.info(f"Over-refusal coverage (reported SEPARATELY, never folded into "
                f"'safety coverage'): {orr['value']}/{orr['denominator']}")
    logger.info(f"{len(needs)} checkpoints require in-house safety measurement")


if __name__ == "__main__":
    main()
