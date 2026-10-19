#!/usr/bin/env python3
"""W5 - reporting fidelity (block: fidelity)."""

from __future__ import annotations

import collections
import re
from typing import Any

from loguru import logger

from lib_arch import Resolver, prov, wilson95

FITTED_THRESHOLD = -2.7415117804288127
ROUNDED_THRESHOLD = -2.742
WARNING_BAND = [
    ("rinna/japanese-gpt-neox-small", -2.6138786066870305),
    ("stabilityai/stablelm-3b-4e1t", -2.5150000000000000),
]
PARAM_CEILING = 4.2e9
# Eligibility rule, pre-declared here before it is applied.
ELIGIBILITY_RULE = {
    "n_layers_min": 8,
    "hidden_size_min": 128,
    "param_ceiling_from_tensor_bytes": PARAM_CEILING,
    "exclude_name_or_tag_patterns": [
        r"tiny-random", r"test[-_]?fixture", r"\bdummy\b", r"\bstub\b",
        r"speculator", r"\bdraft\b", r"eagle", r"medusa",
        r"gptq", r"awq", r"bnb", r"4bit", r"8bit", r"int4", r"int8", r"mlx", r"gguf",
    ],
    "rationale_layer_floor": (
        "W05 is a MINIMUM over per-layer write energies. A 2-layer stub gives a 2-term minimum and a "
        "1-layer draft head gives a 1-term minimum; the order statistic is degenerate there, so the "
        "statistic is not defined on such repos and they do not belong in a specificity denominator."
    ),
}


def _reason_bucket(err: str | None) -> str:
    if not err:
        return "other"
    e = err.lower()
    if "conv1d" in e or "transpos" in e:
        return "Conv1D-transposed"
    if "gptq" in e or "bnb" in e or "quant" in e or "awq" in e:
        return "quantized GPTQ/bnb"
    if "config" in e:
        return "bad config"
    return "other"


def run_w5(res: Resolver) -> dict[str, Any]:
    logger.info("W5: reporting fidelity")
    scan = res.read_jsonl("A2", "results/scan*.jsonl", "**/scan*.jsonl")
    m2 = res.read_json("A2", "full_method_out.json")
    numbers = res.read_json("A5", "numbers.json")
    enum = res.read_json("A2", "results/scan_enumeration.json")
    if scan is None or m2 is None or numbers is None:
        return {"status": "UNAVAILABLE", "reason": "scan.jsonl / method_out / numbers.json not resolvable"}

    md2 = m2["metadata"]

    # ---------------- M5.1 counts generated from rows ----------------
    controls = [r for r in scan if r.get("control_class")]
    noncontrol = [r for r in scan if not r.get("control_class")]
    status_all = collections.Counter(r["status"] for r in scan)
    status_nc = collections.Counter(r["status"] for r in noncontrol)
    unresolved_nc = [r for r in noncontrol if r["status"] == "UNRESOLVED"]
    unresolved_all = [r for r in scan if r["status"] == "UNRESOLVED"]
    reasons = collections.Counter(_reason_bucket(r.get("error")) for r in unresolved_nc)

    archived_breakdown = md2.get("scan_status_breakdown", {})
    archived_unres_reasons = md2.get("scan_unresolved_reasons", {})
    archived_unres_total = (
        sum(archived_unres_reasons.values()) if isinstance(archived_unres_reasons, dict) else None
    )
    discrepancy = {
        "recomputed_unresolved_non_control": len(unresolved_nc),
        "recomputed_unresolved_all_rows": len(unresolved_all),
        "value_in_A2_metadata_scan_status_breakdown": archived_breakdown.get("UNRESOLVED"),
        "value_implied_by_A2_scan_unresolved_reasons_sum": archived_unres_total,
        "value_quoted_in_A2_README_summary": 65,
        "adjudication": None,
        "reason_histogram_recomputed": dict(reasons),
        "reason_histogram_archived": archived_unres_reasons,
    }
    rec = len(unresolved_nc)
    stale: list[str] = []
    for label, val in [
        ("A2 metadata.scan_status_breakdown.UNRESOLVED", archived_breakdown.get("UNRESOLVED")),
        ("A2 metadata.scan_unresolved_reasons (sum)", archived_unres_total),
        ("A2 README / artifact summary ('65 UNRESOLVED')", 65),
    ]:
        if val is not None and val != rec:
            stale.append(f"{label} = {val}")
    discrepancy["adjudication"] = (
        f"The unresolved count recomputed from the rows of scan.jsonl is {rec} "
        f"(non-control rows; {len(unresolved_all)} counting controls). "
        + (f"STALE: {'; '.join(stale)}." if stale else "All archived transcriptions agree with the rows.")
    )

    model_type_counts = collections.Counter(
        (r.get("model_type") or "UNKNOWN") for r in noncontrol if r["status"] == "OK"
    )
    mlx14b = [
        r["repo"] for r in scan
        if re.search(r"mlx", r["repo"], re.I) and re.search(r"4bit|4-bit", r["repo"], re.I)
    ]
    if not mlx14b:
        mlx14b = [r["repo"] for r in scan if re.search(r"14b", r["repo"], re.I)]

    counts = {
        "total_rows": len(scan),
        "control_rows": len(controls),
        "non_control_rows": len(noncontrol),
        "control_class_breakdown": dict(collections.Counter(r["control_class"] for r in controls)),
        "status_breakdown_all_rows": dict(status_all),
        "status_breakdown_non_control": dict(status_nc),
        "completed_scanned_non_control": status_nc.get("OK", 0),
        "attempted_non_control": len(noncontrol),
        "expected_shape_from_archives": {"rows": 270, "controls": 20, "attempted": 250, "completed": 160},
        "matches_expected_shape": (
            len(scan) == 270 and len(controls) == 20 and len(noncontrol) == 250
            and status_nc.get("OK", 0) == 160
        ),
        "unresolved_discrepancy": discrepancy,
        "model_type_composition": dict(model_type_counts),
        "fourteen_b_mlx_4bit_repos_admitted": mlx14b,
        "enumeration": enum.get("counts") if isinstance(enum, dict) and "counts" in enum else (
            {k: v for k, v in enum.items() if isinstance(v, int)} if isinstance(enum, dict) else None
        ),
        "provenance": prov("A2/results/scan.jsonl", "all rows", len(scan)),
    }

    # ---------------- M5.2 threshold and boundary facts ----------------
    wb = numbers["W05_boundary"]
    ok_nc = [r for r in noncontrol if r["status"] == "OK" and r.get("W05_abl_min_layer_energy") is not None]
    n_below_rounded = sum(1 for r in ok_nc if r["W05_abl_min_layer_energy"] <= ROUNDED_THRESHOLD)
    n_below_full = sum(1 for r in ok_nc if r["W05_abl_min_layer_energy"] <= FITTED_THRESHOLD)
    pos_ctrl = [r for r in controls if r.get("control_class") in ("positive", "abliterated_positive")]
    pos_hits_full = sum(
        1 for r in pos_ctrl
        if r.get("W05_abl_min_layer_energy") is not None
        and r["W05_abl_min_layer_energy"] <= FITTED_THRESHOLD
    )
    pos_hits_round = sum(
        1 for r in pos_ctrl
        if r.get("W05_abl_min_layer_energy") is not None
        and r["W05_abl_min_layer_energy"] <= ROUNDED_THRESHOLD
    )
    margin = wb["separating_margin_log10"]
    boundary = {
        "panel_boundary_full_precision": FITTED_THRESHOLD,
        "panel_boundary_rounded": ROUNDED_THRESHOLD,
        "rounding_breaks_defining_member": True,
        "defining_member": wb["abliterated_max"]["checkpoint"],
        "defining_member_W05": wb["abliterated_max"]["value"],
        "positive_control_at_full_precision": f"{pos_hits_full}/{len(pos_ctrl)}",
        "positive_control_at_rounded": f"{pos_hits_round}/{len(pos_ctrl)}",
        "abliterated_region_correct_statement": (
            f"-2.742 is the abliterated MAXIMUM ({wb['abliterated_max']['checkpoint']}); the true "
            f"MINIMUM is {wb['abliterated_min']['value']:.4f} "
            f"({wb['abliterated_min']['checkpoint']})."
        ),
        "abliterated_max": wb["abliterated_max"],
        "abliterated_min": wb["abliterated_min"],
        "separating_margin_log10": margin,
        "margin_carried_by": {
            "abliterated_side": wb["abliterated_max"]["checkpoint"],
            "non_abliterated_side": wb["lowest_non_abliterated"]["checkpoint"],
            "values": [wb["abliterated_max"]["value"], wb["lowest_non_abliterated"]["value"]],
            "note": "the margin is the gap between the abliterated MAXIMUM and the lowest "
            "non-abliterated member",
        },
        "nearest_non_abliterated_neighbour": wb["lowest_non_abliterated"],
        "single_member_family_note": (
            "Boundary-adjacent checkpoints come from single-member families: "
            f"olmo n={wb['architecture_family_sizes'].get('olmo')}, "
            f"gpt_neox n={wb['architecture_family_sizes'].get('gpt_neox')}."
        ),
        "architecture_family_sizes": wb["architecture_family_sizes"],
        "warning_band_neighbours": [
            {
                "repo": repo,
                "W05": val,
                "distance_below_boundary_log10": FITTED_THRESHOLD - val,
                "distance_in_margin_widths": (FITTED_THRESHOLD - val) / margin,
            }
            for repo, val in WARNING_BAND
        ],
        "n_scanned_below_rounded_threshold": n_below_rounded,
        "n_scanned_below_full_precision_threshold": n_below_full,
        "provenance": prov("A5/numbers.json", "W05_boundary", margin),
    }

    # ---------------- M5.3 AUROC orientation ----------------
    wa = numbers["weights_auroc"]
    orientation = {
        "convention_string": (
            "Every AUROC in this paper is reported ORIENTED: the sign of the statistic is fixed in "
            "advance by its definition (W05 and W04 are lower-is-abliterated; W01, W02 and W03 are "
            "higher-is-abliterated) and the raw, unoriented value is printed beside it. An oriented "
            "AUROC of 1.000 on a lower-is-positive statistic corresponds to a raw AUROC of 0.000."
        ),
        "rows": [
            {
                "metric_id": k,
                "auroc_oriented": v["auroc_oriented"],
                "auroc_raw": v["auroc"],
                "orientation": v["orientation"],
                "ci95_oriented": v["ci95_oriented"],
                "ci95_raw": v["ci95"],
                "n_tied_pairs": v["n_tied_pairs"],
                "n_pos": v["n_pos"],
                "n_neg": v["n_neg"],
                "provenance": prov("A5/numbers.json", f"weights_auroc.{k}", v["auroc_oriented"]),
            }
            for k, v in wa.items()
        ],
    }

    # ---------------- M5.4 weights table [min, max] ----------------
    cd = numbers["classwise_distribution"]
    wrows: list[dict[str, Any]] = []
    for stat in ["W01_abl_suppression_depth", "W02_abl_direction_consistency",
                 "W03_abl_gap_vs_random", "W04_abl_isolation", "W05_abl_min_layer_energy"]:
        block = cd.get(stat, {})
        for cls, v in block.items():
            if cls == "_all" or not isinstance(v, dict) or "median" not in v:
                continue
            wrows.append({
                "statistic": stat, "class": cls, "n": v["n"],
                "median": v["median"], "min": v["min"], "max": v["max"],
                "provenance": prov("A5/numbers.json", f"classwise_distribution.{stat}.{cls}", v["median"]),
            })
    flagged_overlaps = []
    w01 = cd["W01_abl_suppression_depth"]
    if w01["base"]["max"] > w01["abliterated"]["min"]:
        flagged_overlaps.append({
            "statistic": "W01_abl_suppression_depth",
            "statement": f"base W01 max {w01['base']['max']:.3f} OVERLAPS abliterated min "
                         f"{w01['abliterated']['min']:.3f}",
            "overlap_width": w01["base"]["max"] - w01["abliterated"]["min"],
        })
    w02 = cd["W02_abl_direction_consistency"]
    if abs(w02["base"]["max"] - w02["abliterated"]["median"]) < 1e-9:
        flagged_overlaps.append({
            "statistic": "W02_abl_direction_consistency",
            "statement": f"base W02 max {w02['base']['max']:.3f} EQUALS the abliterated median "
                         f"{w02['abliterated']['median']:.3f}",
            "overlap_width": 0.0,
        })
    weights_table = {
        "rows": wrows,
        "never_median_alone": True,
        "flagged_overlaps": flagged_overlaps,
        "archived_overlap_records": numbers["classwise_overlaps"],
        "W03_random_directions": {
            "correct_value": 256,
            "value_to_correct_in_draft": 64,
            "provenance": prov("A1/full_method_out.json", "metadata.run_meta.n_random_directions", 256),
        },
        "positive_control_disambiguation": {
            "unedited_instruct_W01": 0.6239,
            "unedited_instruct_repo": "Qwen/Qwen3-0.6B-Instruct",
            "unedited_base_W01": 0.6281,
            "unedited_base_repo": "Qwen/Qwen3-0.6B-Base",
            "injected_control_post_value_W01": 4.869,
            "abliterated_W05_minimum": -4.8204,
            "adjacency_flag": "REWORDING_REQUIRED",
            "why": "4.869 (an injected-control W01, a positive log10 ratio) and -4.82 (the abliterated "
            "W05 MINIMUM, a negative log10 energy) are different statistics with opposite signs. Placed "
            "in neighbouring clauses they read as the same number.",
            "suggested_rewrite": (
                "The injected rank-one control lifts W01 from 0.624 to 4.869 on Qwen3-0.6B-Instruct. "
                "Separately - and in a different statistic - the panel's abliterated members occupy the "
                "W05 range [-4.820, -2.742]. Do not state these in adjacent clauses."
            ),
        },
    }

    # ---------------- M5.5 eligibility denominator ----------------
    excl_counts: collections.Counter = collections.Counter()
    exclusion_list: list[dict[str, Any]] = []
    eligible: list[dict] = []
    scanned_ok = [r for r in noncontrol if r["status"] == "OK"]
    have_struct = all(("n_layers" in r and "hidden_size" in r) for r in scanned_ok)
    name_re = re.compile("|".join(ELIGIBILITY_RULE["exclude_name_or_tag_patterns"]), re.I)
    for r in scanned_ok:
        why: list[str] = []
        nl, hs, tb = r.get("n_layers"), r.get("hidden_size"), r.get("tensor_bytes")
        if nl is not None and nl < ELIGIBILITY_RULE["n_layers_min"]:
            why.append("n_layers<8")
        if hs is not None and hs < ELIGIBILITY_RULE["hidden_size_min"]:
            why.append("hidden_size<128")
        if tb is not None and (tb / 2.0) > PARAM_CEILING:
            why.append("tensor bytes imply >4.2B at bf16")
        if name_re.search(r["repo"]):
            why.append("name/tag identifies a fixture, speculator/draft head or quantized re-upload")
        if why:
            for w in why:
                excl_counts[w] += 1
            exclusion_list.append({"repo": r["repo"], "criteria": why,
                                   "n_layers": nl, "hidden_size": hs, "tensor_bytes": tb})
        else:
            eligible.append(r)
    hits_elig = sum(1 for r in eligible if r["W05_abl_min_layer_energy"] <= FITTED_THRESHOLD)
    hits_raw = sum(1 for r in scanned_ok if r["W05_abl_min_layer_energy"] <= FITTED_THRESHOLD)
    elo, ehi = wilson95(hits_elig, len(eligible)) if eligible else (None, None)
    rlo, rhi = wilson95(hits_raw, len(scanned_ok))
    eligibility = {
        "rule_declared_before_application": ELIGIBILITY_RULE,
        "applicable": have_struct,
        "fallback_used": not have_struct,
        "fallback_note": None if have_struct else
        "n_layers/hidden_size absent from some scan rows; fell back to card/tag/repo-name exclusion only.",
        "n_raw": len(scanned_ok),
        "n_excluded_by_each_criterion": dict(excl_counts),
        "n_excluded_rows": len(exclusion_list),
        "n_eligible": len(eligible),
        "hits_eligible": hits_elig,
        "fp_rate_eligible_PRIMARY": hits_elig / len(eligible) if eligible else None,
        "wilson95_eligible_PRIMARY": [elo, ehi],
        "fp_rate_raw_SECONDARY": hits_raw / len(scanned_ok) if scanned_ok else None,
        "wilson95_raw_SECONDARY": [rlo, rhi],
        "raw_secondary_row_as_quoted": "0/160 [0, 0.023]",
        "exclusion_list": exclusion_list,
        "layer_count_floor": ELIGIBILITY_RULE["n_layers_min"],
        "layer_count_floor_justification": ELIGIBILITY_RULE["rationale_layer_floor"],
        "layer_count_histogram": dict(collections.Counter(r.get("n_layers") for r in scanned_ok)),
        "both_denominators_reported": True,
    }

    # ---------------- M5.6 threshold brittleness ----------------
    def hits_at(thr: float, pop: list[dict]) -> int:
        return sum(1 for r in pop if r["W05_abl_min_layer_energy"] <= thr)

    coarse = []
    t = -2.4
    while t >= -3.0001:
        coarse.append({"threshold": round(t, 4),
                       "hits_raw_160": hits_at(t, scanned_ok),
                       "hits_eligible": hits_at(t, eligible)})
        t -= 0.1
    fine = []
    first_fp = None
    tt = -3.0
    while tt <= -2.3999:
        h = hits_at(tt, scanned_ok)
        fine.append({"threshold": round(tt, 4), "hits_raw_160": h})
        if h > 0 and first_fp is None:
            first_fp = round(tt, 4)
        tt += 0.01
    # As the threshold is raised from -3.0 toward -2.4 the FIRST repo caught is the one with the
    # most negative W05 in the scanned population, since a hit is W05 <= threshold.
    tripping = None
    if scanned_ok:
        first = min(scanned_ok, key=lambda r: r["W05_abl_min_layer_energy"])
        tripping = {
            "repo": first["repo"],
            "W05": first["W05_abl_min_layer_energy"],
            "model_type": first.get("model_type"),
            "n_layers": first.get("n_layers"),
            "is_eligible": first in eligible,
            "distance_above_fitted_threshold_log10":
                first["W05_abl_min_layer_energy"] - FITTED_THRESHOLD,
        }
    brittleness = {
        "coarse_sweep_step_0.1": coarse,
        "fine_sweep_step_0.01_first_false_positive_threshold": first_fp,
        "smallest_shift_to_first_false_positive": (
            abs(FITTED_THRESHOLD - first_fp) if first_fp is not None else None
        ),
        "repo_that_trips_it": tripping,
        "statement": "the threshold is panel-fitted and was never validated out of panel.",
        "sweep_population": "the 160 completed non-control scan rows (raw) and the eligible subset",
    }

    # ---------------- M5.7 claim map ----------------
    pf = numbers["preregistration_fidelity"]
    claim_rows = []
    for r in pf["rows"]:
        claim_rows.append({
            "claim_text_in_draft": r["claim"],
            "status": r["verdict"],
            "artifact_file": (r.get("recorded_in") or "").split(",")[0].strip() or None,
            "line_or_key": (r.get("recorded_in") or ""),
            "corrected_wording": r.get("corrected_wording"),
        })
    vc = pf["verdict_counts"]
    total = sum(vc.values())
    claim_map = {
        "rows": claim_rows,
        "verdict_counts": vc,
        "total": total,
        "totals_sum_to_12": total == 12,
        "expected_counts": {"SUPPORTED": 4, "PLAN-ONLY": 2, "UNSUPPORTED": 6},
        "counts_match_expected": vc == {"SUPPORTED": 4, "PLAN-ONLY": 2, "UNSUPPORTED": 6},
        "reservation_rule": (
            "'pre-registered' is reserved for what metric_spec.py (sha 544ff994) actually stamps - 53 "
            "metric declarations and nothing else; everything else is 'planned' or 'stated in advance "
            "in the plan document'."
        ),
        "metric_spec_sha256": pf["metric_spec_sha256"],
        "n_metrics_declared": pf["n_metrics_declared"],
        "sha_matches_draft_claim": pf.get("metric_spec_sha_matches_draft_claim"),
    }

    return {
        "status": "OK",
        "counts_from_rows": counts,
        "threshold_and_boundary_facts": boundary,
        "auroc_orientation": orientation,
        "weights_table_minmax": weights_table,
        "eligibility_denominator": eligibility,
        "threshold_brittleness": brittleness,
        "claim_map": claim_map,
    }
