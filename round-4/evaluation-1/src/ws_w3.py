#!/usr/bin/env python3
"""W3 - E_1 band sensitivity (block: e1_bands)."""

from __future__ import annotations

from typing import Any

import numpy as np
from loguru import logger

from lib_arch import BOOT_B, Resolver, auroc, lineage_boot_auroc_diff, perm_p_auroc, prov

SEED_W3 = 20260814
BANDS = [
    {"band": [0.25, 0.75], "label": "PRIMARY - our reading of the incumbent's mid-stack"},
    {"band": [0.0, 1.0], "label": "FULL STACK"},
    {"band": [0.4, 0.6], "label": "narrow mid-stack"},
]
INVARIANCE_DEFINITION = (
    "Declared BEFORE computing. INVARIANT iff at ALL three bands: (i) E_1 still detects the "
    "new-uploader positives that W05 misses (E_1 3/3 direction preserved); (ii) E_1 still degrades on "
    "multi-direction rank-k synthetics where W05 is perfect; (iii) the sign of the paired difference on "
    "the 15-pair set is unchanged. If MOVED, name WHICH band drives it and which of (i)-(iii) flipped."
)
SEARCHED_FIELDS = [
    "arm2_pairs.jsonl:{E1,E1_median,E1_min,E1_max,n_matrices,band,band_layers}",
    "arm2_all.jsonl:{same}",
    "full_method_out.json:datasets.arm2_e1_headtohead.metadata_{band,band_layers,n_matrices}",
    "A2/results/ladder_e_v1_profiles (per-layer e_v1 of ladder stages, NOT parent-diff singular values)",
    "glob **/*delta*, **/*spect*, **/*sigma*, **/*e_v1* across A1 and A2",
]


def _pairsets(pairs: list[dict]) -> dict[str, list[dict]]:
    pre12 = [p for p in pairs if p["pair_type"] in ("positive", "negative_instruct_vs_base",
                                                    "negative_uncensored_vs_parent")]
    new3 = [p for p in pairs if p["pair_type"] == "positive_new_uploader"]
    return {
        "pre_declared_12": pre12,
        "extended_15": pre12 + new3,
        "synthetic_inclusive_41": pairs,
    }


def _rows(ps: list[dict]) -> list[dict]:
    out = []
    for p in ps:
        if p.get("E1") is None or p.get("W05_candidate") is None:
            continue
        out.append(
            {
                "E1": float(p["E1"]),
                "W05": float(p["W05_candidate"]),
                "label": 0 if str(p["pair_type"]).startswith("negative") else 1,
                "lineage_id": p.get("lineage_id") or p["candidate"],
                "candidate": p["candidate"],
                "pair_type": p["pair_type"],
                "recipe": p.get("recipe"),
                "is_synthetic": str(p["pair_type"]).endswith("_synthetic"),
            }
        )
    return out


def run_w3(res: Resolver) -> dict[str, Any]:
    logger.info("W3: E_1 band sensitivity")
    raw = res.read_jsonl("A1", "results/arm2_all*.jsonl", "**/arm2*all*.jsonl")
    m1 = res.read_json("A1", "full_method_out.json")
    if raw is None or m1 is None:
        return {"status": "UNAVAILABLE", "reason": "arm2 rows not resolvable"}

    # The assembled arm2_e1_headtohead dataset is the COMPLETE 41-pair set (arm2_all.jsonl holds
    # only the 38 pairs computed inside arm2.py; the 3 new-uploader pairs were resolved by
    # realcheck.py and merged at assembly time).  Source the pair set from the assembled dataset and
    # enrich it with the raw rows where they exist.
    hh = [d for d in m1["datasets"] if d["dataset"] == "arm2_e1_headtohead"][0]["examples"]
    raw_by_cand = {p["candidate"]: p for p in raw}
    pairs_all: list[dict] = []
    for e in hh:
        cand = e["metadata_candidate"]
        r = raw_by_cand.get(cand, {})
        pairs_all.append({
            "parent": e["metadata_parent"],
            "candidate": cand,
            "pair_type": e["metadata_pair_type"],
            "recipe": e["metadata_recipe"],
            "lineage_id": e["metadata_lineage_id"],
            "family": e["metadata_family"],
            "n_matrices": e["metadata_n_matrices"],
            "band": e["metadata_band"],
            "band_layers": e["metadata_band_layers"],
            "band_note": r.get("band_note"),
            "E1": float(e["predict_E1_parent_required"]),
            "W05_candidate": float(e["predict_W05_parent_free"]),
            "E1_min": r.get("E1_min"),
            "E1_max": r.get("E1_max"),
            "E1_median": r.get("E1_median"),
            "source": "arm2_all.jsonl" if cand in raw_by_cand else "assembled arm2_e1_headtohead "
                                                                   "(realcheck-resolved pair)",
        })

    archived_band = pairs_all[0].get("band")
    sets = _pairsets(pairs_all)
    rng = np.random.default_rng(SEED_W3)

    band_rows: list[dict[str, Any]] = []
    for spec in BANDS:
        is_primary = list(spec["band"]) == list(archived_band or [])
        for name, ps in sets.items():
            rows = _rows(ps)
            base = {
                "band": spec["band"],
                "band_label": spec["label"],
                "pairset": name,
                "n_pairs": len(rows),
                "n_positives": sum(r["label"] for r in rows),
                "n_negatives": sum(1 for r in rows if r["label"] == 0),
            }
            if not is_primary:
                base.update(
                    {
                        "band_status": "NOT_RECOMPUTABLE_FROM_ARCHIVE",
                        "reason": "Per-matrix singular-value spectra of dW are NOT archived at layer "
                        "granularity. arm2 rows store only the band-aggregated E_1 (mean/median/min/max) "
                        "for the single band [0.25, 0.75] that was computed at run time. Recomputing "
                        "another band would require re-downloading every parent/candidate pair, which "
                        "this pure re-analysis forbids. No band is approximated by interpolation.",
                        "fields_searched": SEARCHED_FIELDS,
                        "auroc_E1": None,
                        "auroc_W05": None,
                        "paired_diff_W05_minus_E1": None,
                    }
                )
                band_rows.append(base)
                continue

            d = lineage_boot_auroc_diff(
                rows, "W05", "E1", "label", "lineage_id",
                a_higher_pos=False, b_higher_pos=True, rng=rng, b=BOOT_B,
            )
            pv = [r["E1"] for r in rows if r["label"] == 1]
            nv = [r["E1"] for r in rows if r["label"] == 0]
            perm = perm_p_auroc(pv, nv, True, np.random.default_rng(SEED_W3), 10_000)
            base.update(
                {
                    "band_status": "RECOMPUTED_FROM_ARCHIVE",
                    "auroc_E1": d.get("auroc_b"),
                    "auroc_W05": d.get("auroc_a"),
                    "paired_diff_W05_minus_E1": d.get("paired_diff"),
                    "ci_lo": d.get("ci_lo"),
                    "ci_hi": d.get("ci_hi"),
                    "B": BOOT_B,
                    "seed": SEED_W3,
                    "resampling_unit": "lineage",
                    "n_lineages": d.get("n_lineages"),
                    "permutation_p_E1": perm["p_permutation"],
                    "permutation_floor": perm["exact_floor"],
                    "permutation_floor_expr": perm["exact_floor_expr"],
                    "provenance": prov("A1/results/arm2_all.jsonl", f"pairset={name}", d.get("paired_diff")),
                }
            )
            band_rows.append(base)

    # ---------------- M3.2 invariance verdict ----------------
    prim = {r["pairset"]: r for r in band_rows if r["band_status"] == "RECOMPUTED_FROM_ARCHIVE"}
    rows15 = _rows(sets["extended_15"])
    new_up = [r for r in _rows(pairs_all) if r["pair_type"] == "positive_new_uploader"]
    # E_1 detects at the arm-2 operating point: E_1 above the max negative E_1
    negE = [r["E1"] for r in _rows(pairs_all) if r["label"] == 0]
    thrE = max(negE) if negE else None
    e1_catch = sum(1 for r in new_up if thrE is not None and r["E1"] > thrE)
    w05_catch = sum(1 for r in new_up if r["W05"] <= -2.7415117804288127)
    rankk = [r for r in _rows(pairs_all) if r["recipe"] == "rank_k"]
    e1_rankk = [r["E1"] for r in rankk]
    w05_rankk_perfect = all(r["W05"] <= -2.7415117804288127 for r in rankk) if rankk else None
    sign15 = prim.get("extended_15", {}).get("paired_diff_W05_minus_E1")

    checks = {
        "i_E1_detects_new_uploader_positives_W05_misses": {
            "E_1_catches": f"{e1_catch}/{len(new_up)}",
            "W05_catches": f"{w05_catch}/{len(new_up)}",
            "E_1_operating_threshold": thrE,
            "holds": e1_catch == len(new_up) and w05_catch == 0,
            "evaluable_at_bands": ["0.25-0.75 only"],
        },
        "ii_E1_degrades_on_multidirection_rank_k_where_W05_perfect": {
            "E_1_values_on_rank_k": {r["candidate"]: r["E1"] for r in rankk},
            "E_1_range": [min(e1_rankk), max(e1_rankk)] if e1_rankk else None,
            "W05_perfect_on_rank_k": w05_rankk_perfect,
            "holds": bool(e1_rankk and min(e1_rankk) < 0.9 and w05_rankk_perfect),
            "evaluable_at_bands": ["0.25-0.75 only"],
        },
        "iii_sign_of_paired_difference_on_15_pair_set": {
            "paired_diff_W05_minus_E1": sign15,
            "sign": "negative" if (sign15 is not None and sign15 < 0) else
                    ("zero" if sign15 == 0 else "positive"),
            "holds": sign15 is not None and sign15 < 0,
            "evaluable_at_bands": ["0.25-0.75 only"],
        },
    }
    all_hold_primary = all(c["holds"] for c in checks.values())
    verdict = {
        "definition_declared_before_computing": INVARIANCE_DEFINITION,
        "verdict": "UNDETERMINED_INSUFFICIENT_BANDS",
        "verdict_at_primary_band_only": "INVARIANT" if all_hold_primary else "MOVED",
        "why_undetermined": (
            "The verdict is defined over ALL THREE bands. Only the archived [0.25, 0.75] band is "
            "recomputable from the archive; the FULL STACK and [0.4, 0.6] bands would require per-matrix "
            "singular values that were never persisted. Reporting INVARIANT on one band would be "
            "answering a different question than the one declared, so the enum is withheld and the "
            "single-band result is reported explicitly as such."
        ),
        "checks": checks,
        "which_band_drives_it": None,
        "what_would_settle_it": (
            "Re-running arm 2's e1.py with BAND_LO/BAND_HI set to (0.0, 1.0) and (0.4, 0.6). That is a "
            "download + SVD job, not a re-analysis, so it is named as future work rather than "
            "approximated here."
        ),
    }

    # ---------------- M3.3 synthetic dependence ----------------
    rows41 = _rows(pairs_all)
    rows_nosynth = [r for r in rows41 if not r["is_synthetic"]]
    with_syn = lineage_boot_auroc_diff(
        rows41, "W05", "E1", "label", "lineage_id", False, True, np.random.default_rng(SEED_W3), BOOT_B
    )
    without_syn = lineage_boot_auroc_diff(
        rows_nosynth, "W05", "E1", "label", "lineage_id", False, True,
        np.random.default_rng(SEED_W3), BOOT_B,
    )
    synth_flag = {
        "claim": "the only interval excluding zero is the 41-pair paired difference "
        "-0.186 [-0.382, -0.079]",
        "recomputed_with_synthetics": {
            "n_pairs": len(rows41),
            "n_in_house_synthetics": sum(1 for r in rows41 if r["is_synthetic"]),
            "paired_diff": with_syn.get("paired_diff"),
            "ci": [with_syn.get("ci_lo"), with_syn.get("ci_hi")],
            "excludes_zero": with_syn.get("ci_lo") is not None
            and not (with_syn["ci_lo"] <= 0 <= with_syn["ci_hi"]),
        },
        "recomputed_with_synthetics_EXCLUDED": {
            "n_pairs": len(rows_nosynth),
            "paired_diff": without_syn.get("paired_diff"),
            "ci": [without_syn.get("ci_lo"), without_syn.get("ci_hi")],
            "excludes_zero": without_syn.get("ci_lo") is not None
            and not (without_syn["ci_lo"] <= 0 <= without_syn["ci_hi"]),
            "status": without_syn.get("status"),
        },
        "statement": (
            "The interval that excludes zero rests on 26 in-house synthetics whose construction we "
            "control. With those removed the estimate and its interval are reported beside it, so the "
            "reader sees the claim's dependence on our own constructions rather than being told about it."
        ),
    }

    return {
        "status": "OK",
        "seed": SEED_W3,
        "bootstrap_B": BOOT_B,
        "E1_definition": "E_1 = mean over matrices m of sigma_1^2(dW_m) / sum_i sigma_i^2(dW_m), "
        "restricted to a relative-depth band; dW = W_parent - W_candidate over o_proj and down_proj.",
        "archived_band": archived_band,
        "archived_band_note": next((p["band_note"] for p in pairs_all if p.get("band_note")), None),
        "pair_source_note": (
            "The 41-pair set is sourced from the assembled arm2_e1_headtohead dataset. "
            "results/arm2_all.jsonl holds only the 38 pairs computed inside arm2.py; the 3 "
            "new-uploader pairs were resolved by realcheck.py and merged at assembly time. Anyone "
            "recomputing from arm2_all.jsonl alone gets 38 and 12, not 41 and 15."
        ),
        "n_pairs_in_arm2_all_jsonl": len(raw),
        "n_pairs_in_assembled_dataset": len(hh),
        "bands_requested": BANDS,
        "n_bands_recomputable": sum(1 for r in band_rows if r["band_status"] == "RECOMPUTED_FROM_ARCHIVE") // 3,
        "e1_by_band": band_rows,
        "invariance_verdict": verdict,
        "synthetic_dependence_flag": synth_flag,
    }
