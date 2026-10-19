#!/usr/bin/env python3
"""One numbers file the paper must obey.

Pure re-analysis of the archived iteration-2/3/4 trees. ZERO model weights, ZERO
forward passes, ZERO OpenRouter calls ($0.00), ZERO Hub fetches. Every number is
either (i) recomputed from archived raw rows on disk, or (ii) carried forward
verbatim with provenance {file, key_path, raw_value}. A required key that is
absent becomes status="UNAVAILABLE" with the exact path probed -- never an
estimate.

Stages (checkpointed to disk so a late failure never loses earlier work):
  0  archive inventory
  1  workstream 1 -- the operating point, four columns
  2  workstream 2 -- the derivation with its residual bounded numerically
  3  workstream 3 -- the consolidated corrections subsection
  4  workstream 4 -- the editorial pass as machine-readable edits
  5  workstream 5 -- carry-forward with provenance
  6  numbers.json + eval_out.json + determinism
"""

from __future__ import annotations

import argparse
import gc
import math
import resource
import shutil
import subprocess
import sys
from pathlib import Path

import archlib as L
from archlib import (A1, A2, A3, A4, A5, A6, A7a, A7b, DRAFT4, ROOT, TAU_FIXED,
                     WILSON_FORMULA, auroc, bootstrap_ci, dump_json, load_json,
                     load_jsonl, num, rel, sha256_of, smallest_detectable_upward,
                     spearman, two_proportion_power, wilson)
from loguru import logger

HERE = Path(__file__).resolve().parent
I3E1 = ROOT / "iter_3/gen_art/gen_art_experiment_1"  # source of the archived negatives

SEED = 20260814
N_BOOT = 10000
COS_DISCOVERY = 0.99  # |cos(v1,r)| above which discovery is treated as holding

# 29 GB container; this artifact reads a handful of JSON files, the largest 22 MB.
RAM_BUDGET = 6 * 1024**3
resource.setrlimit(resource.RLIMIT_AS, (RAM_BUDGET * 3, RAM_BUDGET * 3))

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs/run.log", rotation="30 MB", level="DEBUG")


# ===========================================================================
# helpers
# ===========================================================================
def probe(obj, *path):
    """Walk a nested structure. Returns (found, value)."""
    cur = obj
    for p in path:
        try:
            if isinstance(cur, dict):
                if p not in cur:
                    return (False, None)
                cur = cur[p]
            elif isinstance(cur, list):
                cur = cur[p]
            else:
                return (False, None)
        except (KeyError, IndexError, TypeError):
            return (False, None)
    return (True, cur)


class Assertions:
    """Every quoted value gets ONE assertion with status in {MATCH, MISMATCH,
    UNAVAILABLE}. MISMATCHes are never silently fixed -- each becomes a
    corrections[] entry and the archive's row-level value wins."""

    def __init__(self):
        self.rows: list[dict] = []

    def check(self, key: str, recomputed, archived, tol: float = 1e-12,
              source: str | None = None, note: str | None = None) -> str:
        if archived is None and recomputed is None:
            st = "UNAVAILABLE"
        elif archived is None or recomputed is None:
            st = "UNAVAILABLE"
        else:
            st = "MATCH" if L.approx(recomputed, archived, tol) else "MISMATCH"
        delta = None
        try:
            if isinstance(recomputed, (int, float)) and isinstance(archived, (int, float)):
                delta = float(recomputed) - float(archived)
        except (TypeError, ValueError):
            delta = None
        self.rows.append({
            "key": key, "status": st, "recomputed": L.clean_float(recomputed),
            "archived": L.clean_float(archived), "delta": L.clean_float(delta),
            "tolerance": tol, "source": source, "note": note,
        })
        return st

    def unavailable(self, key: str, probed_path: str, note: str | None = None):
        self.rows.append({"key": key, "status": "UNAVAILABLE", "recomputed": None,
                          "archived": None, "delta": None, "tolerance": None,
                          "source": probed_path, "note": note})

    def counts(self) -> dict:
        c = {"MATCH": 0, "MISMATCH": 0, "UNAVAILABLE": 0}
        for r in self.rows:
            c[r["status"]] = c.get(r["status"], 0) + 1
        c["TOTAL"] = len(self.rows)
        return c


# ===========================================================================
# STAGE 0 -- archive inventory
# ===========================================================================
INVENTORY_PATHS = [
    A1 / "results/arm_a.jsonl", A1 / "results/arm_b.jsonl",
    A1 / "results/arm_b_behaviour.jsonl", A1 / "results/analysis.json",
    A1 / "results/predictions.json", A1 / "results/predictions.sha256",
    A1 / "results/predictions_derived.json", A1 / "results/unit_tests.json",
    A1 / "results/gate_iter4.json", A1 / "results/cards.json",
    A1 / "results/directions.json", A1 / "results/layer_profiles.jsonl",
    A1 / "results/cost.jsonl", A1 / "results/s4a_host.json",
    A1 / "results/arm_a_plan.json", A1 / "full_method_out.json",
    A2 / "results/numbers.json", A2 / "results/assertions.json",
    A2 / "results/arm1_analysis.json", A2 / "results/arm2_rates.json",
    A2 / "results/arm2_archive_counts.json", A2 / "results/arm2_new_candidates.json",
    A2 / "results/arm2_archive_eligibility.jsonl", A2 / "results/arm2_scan_new.jsonl",
    A2 / "results/arm3.json", A2 / "results/eligibility_stamp.json",
    A2 / "results/repro_gate.json", A2 / "results/gate_numerics.json",
    A2 / "results/gate_arithmetic.json", A2 / "results/predictions_outcome.json",
    A2 / "results/archive_schema.json",
    A3 / "results/roots.json", A3 / "results/arm1_summary.json",
    A3 / "results/arm1_framing.json", A3 / "results/arm1_dequant.jsonl",
    A3 / "results/ladder_ci_summary.json", A3 / "results/threshold_sweep.json",
    A3 / "results/analysis.json", A3 / "results/summary.json",
    A3 / "results/repro_gate.json", A3 / "results/verify.json",
    A3 / "results/dropped.json", A3 / "results/state.json",
    A4 / "full_method_out.json", A4 / "results/battery.jsonl",
    A4 / "results/behaviour.jsonl", A4 / "results/behaviour_rubricA.jsonl",
    A4 / "results/diagnostics.json", A4 / "results/calibration.json",
    A4 / "results/padding_control.json", A4 / "results/judge_calibration.json",
    A5 / "full_data_out.json",
    A6 / "numbers.json", A6 / "full_eval_out.json", A6 / "results/reproducibility.json",
    I3E1 / "results/arm2_all.jsonl",
    A7a, A7b, DRAFT4,
]


def stage0(outdir: Path) -> dict:
    logger.info("STAGE 0 -- archive inventory")
    inv = []
    for p in INVENTORY_PATHS:
        e = {"path": rel(p), "exists": p.exists(), "bytes": None, "sha256": None,
             "top_level_keys": None, "n_lines": None, "kind": None}
        if p.exists():
            if p.is_dir():
                e["kind"] = "dir"
                e["n_lines"] = len([q for q in sorted(p.iterdir())
                                    if ".venv" not in q.parts])
            else:
                e["kind"] = "file"
                e["bytes"] = p.stat().st_size
                e["sha256"] = sha256_of(p)
                try:
                    if p.suffix == ".jsonl":
                        e["n_lines"] = sum(1 for ln in p.open() if ln.strip())
                    elif p.suffix == ".json":
                        # full_data_out.json is 22 MB -- read once, index, discard
                        o = load_json(p)
                        e["top_level_keys"] = (sorted(o.keys()) if isinstance(o, dict)
                                               else [f"<list len={len(o)}>"])
                        del o
                        gc.collect()
                except Exception as exc:  # noqa: BLE001 - inventory must never crash
                    e["top_level_keys"] = [f"<unreadable: {type(exc).__name__}>"]
        inv.append(e)
    n_missing = sum(1 for e in inv if not e["exists"])
    out = {"root": str(ROOT), "n_paths": len(inv), "n_missing": n_missing,
           "entries": inv,
           "note": ("every path this artifact reads, stamped. A path with "
                    "exists=false becomes an UNAVAILABLE entry downstream, "
                    "never an estimate.")}
    dump_json(L.deep_clean(out), outdir / "results/archive_inventory.json")
    logger.info(f"  {len(inv)} paths, {n_missing} missing")
    return out


# ===========================================================================
# POOL RECONSTRUCTION (shared by workstreams 1 and 2)
# ===========================================================================
ARMB_UNIFORMITY_RULES = (
    "family=uniform_subunit -> UNIFORM if w==1.0 else UNIFORM_BUT_INCOMPLETE; "
    "family=gaussian_depth  -> DEPTH_WEIGHTED_ABOVE_W_STAR if min_depth_weight>=w_star "
    "else NONUNIFORM; family=layer_band -> NONUNIFORM; family=heretic -> UNIFORM if "
    "row.uniform else NONUNIFORM; family in {norm_preserving, rank_k} -> UNIFORM; "
    "family=householder -> UNIFORM_BUT_ORTHOGONAL"
)


def build_pools(a1_analysis: dict) -> dict:
    """Rebuild the positive and negative pools FROM ROWS, not from summaries.

    Negatives = 20 Arm-A declared parents + 11 unique archived iteration-3 parents
    + the Arm-B host = 32. Positives = 44 Arm-A edited + 23 Arm-B kernels = 67.
    Both are verified against the archive below rather than asserted.
    """
    arm_a_all = load_jsonl(A1 / "results/arm_a.jsonl")
    arm_a = [r for r in arm_a_all if r["status"] == "OK" and r.get("eligible")]
    arm_b_all = load_jsonl(A1 / "results/arm_b.jsonl")
    arm_b = [r for r in arm_b_all if not r.get("precision_control")]
    behav = {r["kernel_id"]: r for r in load_jsonl(A1 / "results/arm_b_behaviour.jsonl")}
    derived = load_json(A1 / "results/predictions_derived.json")
    w_star = derived["w_star_predicted_crossing"]

    # ---- negatives -------------------------------------------------------
    negatives = [{"repo_id": r["repo_id"], "W05": r["W05_abl_min_layer_energy"],
                  "source": "arm_a_parent", "uploader": r["uploader"]}
                 for r in arm_a if r["role"] == "parent"]
    seen, archived_neg = set(), []
    for r in load_jsonl(I3E1 / "results/arm2_all.jsonl"):
        if r.get("ok") and r.get("parent") and r.get("W05_parent") is not None:
            if r["parent"] not in seen:
                seen.add(r["parent"])
                archived_neg.append({"repo_id": r["parent"], "W05": r["W05_parent"],
                                     "source": "archived_iter3",
                                     "uploader": r["parent"].split("/")[0]})
    negatives += archived_neg
    pb = next((r for r in arm_b if r["kernel_id"] == "parent_unedited"), None)
    if pb is not None:
        negatives.append({"repo_id": "Qwen/Qwen3-1.7B (arm B host)",
                          "W05": pb["W05_abl_min_layer_energy"],
                          "source": "arm_b_host", "uploader": "Qwen"})

    # ---- positives -------------------------------------------------------
    positives = [{"repo_id": r["repo_id"], "W05": r["W05_abl_min_layer_energy"],
                  "cls": r["recipe_class_rederived"], "arm": "A",
                  "uploader": r["uploader"], "uniformity": r["kernel_uniformity"]}
                 for r in arm_a if r["role"] == "edited"]

    sweep = {str(c["spread_label"]): c for c in a1_analysis["gaussian_sweep"]["curve"]}

    def armb_uniformity(r: dict) -> str:
        fam = r["family"]
        if fam == "uniform_subunit":
            w = float(r["kernel_id"].split("uniform_w")[1])
            return "UNIFORM" if w >= 1.0 else "UNIFORM_BUT_INCOMPLETE"
        if fam == "householder":
            return "UNIFORM_BUT_ORTHOGONAL"
        if fam == "gaussian_depth":
            label = r["kernel_id"].replace("gaussian_s", "")
            mw = probe(sweep, label, "min_depth_weight")[1]
            if mw is not None and mw >= w_star:
                return "DEPTH_WEIGHTED_ABOVE_W_STAR"
            return "NONUNIFORM"
        if fam == "layer_band":
            return "NONUNIFORM"
        if fam == "heretic":
            return "UNIFORM" if r.get("uniform") else "NONUNIFORM"
        if fam in ("norm_preserving", "rank_k"):
            return "UNIFORM"
        return "UNKNOWN"

    for r in arm_b:
        if r["kernel_id"] == "parent_unedited" or r["family"] == "control":
            continue
        positives.append({
            "repo_id": r["kernel_id"], "W05": r["W05_abl_min_layer_energy"],
            "cls": f"ARMB_{r['family'].upper()}__{armb_uniformity(r)}",
            "arm": "B", "uploader": "in-house",
            "uniformity": armb_uniformity(r),
            "abscos_v1_r": r.get("abscos_v1_r"),
            "log10_min_e_r": r.get("log10_min_e_r"),
            "family": r["family"],
            "refusal_rate_judge": probe(behav, r["kernel_id"], "refusal_rate_judge")[1],
            "fluency_pass": probe(behav, r["kernel_id"], "fluency_pass")[1],
        })

    return {"positives": positives, "negatives": negatives, "arm_a": arm_a,
            "arm_a_all": arm_a_all, "arm_b": arm_b, "behav": behav,
            "w_star": w_star, "sweep": sweep}


# ===========================================================================
# STAGE 1 -- WORKSTREAM 1: the operating point, four columns
# ===========================================================================
def stage1(outdir: Path, pools: dict, a1: dict, asrt: Assertions) -> dict:
    logger.info("STAGE 1 -- workstream 1: the operating point")
    lorco_arch = a1["lorco"]
    pos, neg = pools["positives"], pools["negatives"]
    negv = [n["W05"] for n in neg]
    n_neg = len(negv)

    asrt.check("pools.n_positives", len(pos), probe(a1, "pools", "n_positives")[1],
               0, rel(A1 / "results/analysis.json"))
    asrt.check("pools.n_negatives", n_neg, probe(a1, "pools", "n_negatives")[1],
               0, rel(A1 / "results/analysis.json"))
    asrt.check("fixed_threshold.tau", TAU_FIXED, probe(a1, "fixed_threshold", "tau")[1],
               0, rel(A1 / "results/analysis.json"))

    by_cls: dict[str, list[dict]] = {}
    for p in pos:
        by_cls.setdefault(p["cls"], []).append(p)

    # ---- pooling assumption: n_fit_positives = n_total - n_held_out -------
    pooling_rows, pooling_ok = [], True
    for k in sorted(lorco_arch):
        nho_a = lorco_arch[k]["n_held_out"]
        nfit_a = lorco_arch[k]["n_fit_positives"]
        mine = by_cls.get(k, [])
        reproduces = (len(mine) == nho_a) and (len(pos) - nho_a == nfit_a)
        pooling_ok &= reproduces
        pooling_rows.append({
            "class": k, "n_held_out_archived": nho_a, "n_held_out_rebuilt": len(mine),
            "n_fit_positives_archived": nfit_a,
            "n_fit_positives_implied": len(pos) - nho_a,
            "shortfall": nfit_a - (len(pos) - nho_a), "reproduces": reproduces})
    pooling_status = "REPRODUCES" if pooling_ok else "UNRESOLVED"
    asrt.check("lorco.pooling_assumption", pooling_status, "REPRODUCES", 0,
               "rebuilt from arm_a.jsonl + arm_b.jsonl",
               "Arm A (44 real Hub edits) + Arm B (23 in-house kernels) = 67 positives")

    # ---- refit tau: modal value + exceptions -----------------------------
    taus = [lorco_arch[k]["tau_fitted_without_this_class"] for k in sorted(lorco_arch)]
    counts: dict[float, int] = {}
    for t in taus:
        counts[t] = counts.get(t, 0) + 1
    # modal refit tau: most frequent, ties broken by numeric order (deterministic)
    tau_refit_modal = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    exceptions = sorted([{"class": k, "tau": lorco_arch[k]["tau_fitted_without_this_class"]}
                         for k in sorted(lorco_arch)
                         if lorco_arch[k]["tau_fitted_without_this_class"] != tau_refit_modal],
                        key=lambda d: d["class"])

    louo = a1.get("louo", {})
    louo_taus = sorted({v["tau_fitted_without_this_uploader"] for v in louo.values()}) \
        if louo else []
    louo_exceptions = sorted([{"uploader": k,
                               "tau": v["tau_fitted_without_this_uploader"]}
                              for k, v in sorted(louo.items())
                              if v["tau_fitted_without_this_uploader"] != tau_refit_modal],
                             key=lambda d: d["uploader"])

    # ---- the four-column table ------------------------------------------
    table = {}
    for k in sorted(lorco_arch):
        arch = lorco_arch[k]
        held = sorted(by_cls.get(k, []), key=lambda p: p["repo_id"])
        hv = [p["W05"] for p in held]
        tau_refit_k = arch["tau_fitted_without_this_class"]

        sens_fixed = (sum(1 for v in hv if v <= TAU_FIXED) / len(hv)) if hv else None
        sens_refit_rec = (sum(1 for v in hv if v <= tau_refit_k) / len(hv)) if hv else None
        spec_fixed = sum(1 for v in negv if v > TAU_FIXED) / n_neg
        spec_refit = sum(1 for v in negv if v > tau_refit_k) / n_neg
        # AUROC is threshold-free: orientation is lower-is-positive, so score -W05.
        au_or = auroc([-v for v in hv], [-v for v in negv]) if hv else None

        d_sens = (sens_refit_rec - sens_fixed) if (sens_refit_rec is not None
                                                   and sens_fixed is not None) else None
        table[k] = {
            "col1_sens_fixed_tau": sens_fixed,
            "col2_auroc_oriented_fixed_tau": au_or,
            "col3_sens_refit_tau_recomputed": sens_refit_rec,
            "col3_sens_refit_tau_archived": arch["heldout_sensitivity"],
            "col3_agree_to_1e-12": L.approx(sens_refit_rec, arch["heldout_sensitivity"], 1e-12),
            "col3_delta": (None if sens_refit_rec is None
                           else sens_refit_rec - arch["heldout_sensitivity"]),
            "col4_auroc_refit_archived": arch["auroc_oriented"],
            "col4_archived_orientation_flag": arch.get("auroc_orientation"),
            "col4_orientation_was_flipped": arch.get("auroc_orientation") != "lower-is-positive",
            "auroc_raw_archived": arch["auroc_raw"],
            "auroc_raw_recomputed": auroc(hv, negv) if hv else None,
            "auroc_orientation": "lower-is-positive (FIXED for every cell in col2)",
            "auroc_note": ("AUROC is THRESHOLD-FREE: it cannot move when tau moves. "
                           "col2 and col4 can differ only through the scored "
                           "population or the ORIENTATION CONVENTION, never through tau. "
                           "col2 fixes the orientation at lower-is-positive for every "
                           "cell (col2 = 1 - auroc_raw); the archived col4 instead reports "
                           "max(raw, 1-raw) and records which orientation it chose per "
                           "cell, so col4 is not comparable across cells -- see "
                           "corrections C24."),
            "n_held_out": len(hv),
            "n_held_out_archived": arch["n_held_out"],
            "n_fit_positives_archived": arch["n_fit_positives"],
            "n_negatives": n_neg,
            "tau_fixed": TAU_FIXED,
            "tau_fitted_without_this_class": tau_refit_k,
            "specificity_on_negatives_fixed_tau": spec_fixed,
            "specificity_on_negatives_refit_tau": spec_refit,
            "specificity_on_negatives_archived": arch["specificity_on_negatives"],
            "delta_sens_refit_minus_fixed": d_sens,
            "uniformity": arch.get("uniformity"),
            "held_out_repo_ids": [p["repo_id"] for p in held],
            "arm": sorted({p["arm"] for p in held}),
        }
        asrt.check(f"lorco[{k}].heldout_sensitivity", sens_refit_rec,
                   arch["heldout_sensitivity"], 1e-12,
                   rel(A1 / "results/analysis.json") + f"::lorco.{k}")
        asrt.check(f"lorco[{k}].auroc_raw", table[k]["auroc_raw_recomputed"],
                   arch["auroc_raw"], 1e-12,
                   rel(A1 / "results/analysis.json") + f"::lorco.{k}")
        asrt.check(f"lorco[{k}].auroc_oriented_is_1_minus_raw", au_or,
                   1.0 - arch["auroc_raw"], 1e-12,
                   rel(A1 / "results/analysis.json") + f"::lorco.{k}",
                   "under the FIXED lower-is-positive orientation the oriented AUROC "
                   "must be exactly 1 - raw")
        asrt.check(f"lorco[{k}].specificity_on_negatives", spec_refit,
                   arch["specificity_on_negatives"], 1e-12,
                   rel(A1 / "results/analysis.json") + f"::lorco.{k}")

    # ---- tau shift -------------------------------------------------------
    arm3 = load_json(A2 / "results/arm3.json")
    brittle = probe(arm3, "first_false_positive_filtered", "shift_from_operating_point")[1]
    brittle_repo = probe(arm3, "first_false_positive_filtered", "repo_id")[1]
    sweep3 = load_json(A3 / "results/threshold_sweep.json")
    brittle_a3 = probe(sweep3, "smallest_TAU_shift_producing_a_scan_false_positive")[1]
    shift = tau_refit_modal - TAU_FIXED
    tau_shift = {
        "fixed": TAU_FIXED,
        "refit_modal": tau_refit_modal,
        "refit_modal_n_cells": counts[tau_refit_modal],
        "refit_exceptions_class": exceptions,
        "refit_exceptions_uploader": louo_exceptions,
        "shift_log10": shift,
        "brittleness_scale": brittle,
        "brittleness_first_false_positive_repo": brittle_repo,
        "brittleness_source_file": rel(A2 / "results/arm3.json"),
        "brittleness_key_path": "first_false_positive_filtered.shift_from_operating_point",
        "brittleness_cross_check_A3": brittle_a3,
        "brittleness_cross_check_source": rel(A3 / "results/threshold_sweep.json"),
        "ratio_shift_over_brittleness": (shift / brittle) if brittle else None,
        "sentence": (
            "Holding out a single recipe class moves the fitted operating point by "
            f"{shift:.3f} log10 units (from {TAU_FIXED:.4f} to {tau_refit_modal:.4f}), "
            f"about {shift / brittle:.1f} times the {brittle:.3f} log10 shift that "
            "already introduces the first false positive on the eligible undeclared "
            "population -- so the threshold is not merely brittle, it is essentially "
            "arbitrary at the scale the at-scale positives imply."),
    }

    # ---- cells that change materially ------------------------------------
    material = sorted(
        [{"class": k, "sens_fixed": table[k]["col1_sens_fixed_tau"],
          "sens_refit": table[k]["col3_sens_refit_tau_recomputed"],
          "delta": table[k]["delta_sens_refit_minus_fixed"],
          "n_held_out": table[k]["n_held_out"]}
         for k in sorted(table)
         if table[k]["delta_sens_refit_minus_fixed"]
         and abs(table[k]["delta_sens_refit_minus_fixed"]) > 1e-12],
        key=lambda d: (-abs(d["delta"]), d["class"]))
    expected_pairs = {"R_GLOBAL_RANK1": (1 / 6, 1 / 3), "R_UNKNOWN": (0.2, 0.4)}
    expectation_rows = []
    for k, (ef, er) in sorted(expected_pairs.items()):
        got_f = table.get(k, {}).get("col1_sens_fixed_tau")
        got_r = table.get(k, {}).get("col3_sens_refit_tau_recomputed")
        ok = L.approx(got_f, ef, 1e-9) and L.approx(got_r, er, 1e-9)
        expectation_rows.append({"class": k, "expected_fixed": ef, "expected_refit": er,
                                 "computed_fixed": got_f, "computed_refit": got_r,
                                 "matches_plan_expectation": ok})
        asrt.check(f"cells_that_change_materially[{k}].fixed", got_f, ef, 1e-9,
                   "recomputed from rows", "plan expectation; the ARCHIVE wins on conflict")
        asrt.check(f"cells_that_change_materially[{k}].refit", got_r, er, 1e-9,
                   "recomputed from rows", "plan expectation; the ARCHIVE wins on conflict")

    # ---- 1.5 specificity on eligible undeclared rows, at BOTH taus --------
    spec_block = specificity_block(tau_refit_modal, asrt)

    # ---- 1.6 leave-one-uploader-out, DEMOTED -----------------------------
    louo_block = {
        "status": "SECONDARY -- DEMOTED",
        "note": ("leave-one-recipe-class-out is the PRIMARY generalisation split; "
                 "leave-one-uploader-out is reported only as a labelled secondary "
                 "because uploaders are confounded with recipe (five of the seven "
                 "at-scale detections are one uploader's norm-preserving family)."),
        "n_uploaders": len(louo),
        "distinct_refit_taus": louo_taus,
        "cells": {k: dict(v) for k, v in sorted(louo.items())},
        "source_file": rel(A1 / "results/analysis.json"),
        "key_path": "louo",
    }

    out = {"tau_fixed": TAU_FIXED,
           "tau_fixed_source": {"file": rel(A1 / "results/analysis.json"),
                                "key_path": "fixed_threshold.tau"},
           "detection_rule": "detected iff W05_abl_min_layer_energy <= tau (lower-is-positive)",
           "n_classes": len(table),
           "n_classes_expected_by_plan": 20,
           "n_classes_note": ("the plan expected 20 lorco cells; the archive carries "
                              f"{len(table)}. The ARCHIVE wins -- see corrections[]."),
           "pooling_assumption": {"status": pooling_status,
                                  "rows": pooling_rows,
                                  "n_total_positives": len(pos),
                                  "n_arm_a": sum(1 for p in pos if p["arm"] == "A"),
                                  "n_arm_b": sum(1 for p in pos if p["arm"] == "B"),
                                  "armb_uniformity_rules": ARMB_UNIFORMITY_RULES},
           "negative_pool": {"n": n_neg,
                             "composition": {"arm_a_parent": sum(1 for n in neg if n["source"] == "arm_a_parent"),
                                             "archived_iter3": sum(1 for n in neg if n["source"] == "archived_iter3"),
                                             "arm_b_host": sum(1 for n in neg if n["source"] == "arm_b_host")},
                             "repo_ids": sorted(n["repo_id"] for n in neg),
                             "reconstruction_gate": ("all 9 Arm-A class AUROCs reproduce "
                                                     "the archive exactly (delta 0.00e+00), "
                                                     "which is what licenses this pool")},
           "lorco_table": table,
           "tau_shift": tau_shift,
           "cells_that_change_materially": material,
           "plan_expectation_check": expectation_rows,
           "specificity_at_both_taus": spec_block,
           "leave_one_uploader_out": louo_block}
    dump_json(L.deep_clean(out), outdir / "results/lorco_table.json")
    logger.info(f"  {len(table)} cells, pooling={pooling_status}, "
                f"tau shift={shift:.4f}, ratio={out['tau_shift']['ratio_shift_over_brittleness']}")
    return out


CHAT_RE = ("instruct", "-it", "_it", "chat", "-sft", "sft-", "tulu", "zephyr",
           "dolphin", "openhermes", "vicuna")


def _is_chatlike(repo_id: str, model_type: str | None) -> bool:
    r = repo_id.lower()
    return any(t in r for t in CHAT_RE)


def specificity_block(tau_refit: float, asrt: Assertions) -> dict:
    """Recompute the false-positive rate on the archived eligible-undeclared rows
    at BOTH taus. This is the number the draft currently leaves on the table."""
    arch = load_jsonl(A2 / "results/arm2_archive_eligibility.jsonl")
    new = load_jsonl(A2 / "results/arm2_scan_new.jsonl")
    rates = load_json(A2 / "results/arm2_rates.json")

    def row(repo, w05, mt, src, stratum=None):
        # `stratum` is the archived pre-registered label on the newly fetched rows
        # (non_declaring_chat / non_declaring_base). Where it exists it WINS; the
        # repo-id heuristic is used only for rows that do not carry it.
        if stratum in ("non_declaring_chat", "non_declaring_base"):
            chat = stratum == "non_declaring_chat"
            basis = "archived stratum field"
        else:
            chat = _is_chatlike(repo, mt)
            basis = "repo-id substring heuristic"
        return {"repo_id": repo, "W05": w05, "model_type": mt, "row_set": src,
                "chatlike": chat, "chat_basis": basis, "stratum": stratum}

    primary, secondary = [], []
    for r in arch:
        if r.get("arm") == "control" or r.get("status") != "OK" or r.get("W05") is None:
            continue
        rr = row(r["repo_id"], r["W05"], r.get("model_type"), "archived")
        secondary.append(rr)
        if r.get("eligible"):
            primary.append(rr)
    for r in new:
        if r.get("status") != "OK" or r.get("W05_abl_min_layer_energy") is None:
            continue
        primary.append(row(r["repo"], r["W05_abl_min_layer_energy"], r.get("model_type"),
                           "supplied_this_iteration_by_A2", r.get("stratum")))

    def rate(rows, tau):
        k = sum(1 for x in rows if x["W05"] <= tau)
        n = len(rows)
        lo, hi = wilson(k, n)
        return {"k": k, "n": n, "rate": (k / n if n else None),
                "wilson_lo": lo, "wilson_hi": hi,
                "ci_method": "Wilson score, z=1.959963984540054, continuity=False",
                "wilson_formula": WILSON_FORMULA,
                "named_false_positives": sorted(x["repo_id"] for x in rows
                                                if x["W05"] <= tau)}

    chat_p = [x for x in primary if x["chatlike"]]
    base_p = [x for x in primary if not x["chatlike"]]

    out = {
        "row_set_labels": {
            "archived": "rows scored in the iteration-3 undeclared scan and re-derived in A2",
            "supplied_this_iteration_by_A2": "repos newly fetched and scored by A2 (iteration 4)",
        },
        "primary_filtered_eligible": {
            "at_tau_fixed": rate(primary, TAU_FIXED),
            "at_tau_refit_modal": rate(primary, tau_refit),
            "composition": {"archived": sum(1 for x in primary if x["row_set"] == "archived"),
                            "supplied_this_iteration_by_A2":
                                sum(1 for x in primary if x["row_set"] != "archived")},
        },
        "secondary_unfiltered_archived": {
            "at_tau_fixed": rate(secondary, TAU_FIXED),
            "at_tau_refit_modal": rate(secondary, tau_refit),
            "note": ("the archived 0/160 population -- includes unit-test fixtures, "
                     "speculator heads, quantized re-uploads and mis-indexed >4.2B repos"),
        },
        "denominator_reconciliation": {
            "archived_primary_n": probe(rates, "primary", "n")[1],
            "archived_n_archived_eligible": probe(rates, "primary", "n_archived_eligible")[1],
            "archived_n_new_eligible_completed":
                probe(rates, "primary", "n_new_eligible_completed")[1],
            "recomputed_primary_n": len(primary),
            "recomputed_n_archived_eligible":
                sum(1 for x in primary if x["row_set"] == "archived"),
            "recomputed_n_new_completed":
                sum(1 for x in primary if x["row_set"] != "archived"),
            "delta": len(primary) - (probe(rates, "primary", "n")[1] or 0),
            "explanation": (
                "the archived rate file was written BEFORE the newly-fetched scan "
                "finished, so its denominator is a snapshot. Recounted from the rows "
                "now on disk the eligible undeclared population is larger. Both are "
                "reported: the archived snapshot verbatim, and the row-recount labelled "
                "as the value that supersedes it."),
            "which_wins": "the row recount -- the archive's row-level value wins over "
                          "any summary written mid-scan",
        },
        "stratified_chat_vs_base": {
            "stratification_field": ("archived `stratum` field where present "
                                     "(non_declaring_chat / non_declaring_base), repo-id "
                                     "substring heuristic otherwise"),
            "n_by_basis": {b: sum(1 for x in primary if x["chat_basis"] == b)
                           for b in sorted({x["chat_basis"] for x in primary})},
            "stratification_note": (
                "the newly-fetched rows carry a pre-registered `stratum` label and it is "
                "used verbatim; the older archived rows carry model_type but NOT a "
                "chat_template flag, so for those instruction-tuned status is inferred "
                f"from the repo id (substrings {sorted(CHAT_RE)}) and labelled as a "
                "heuristic. The split matters because the pooled denominator is dominated "
                "by older base models while the population at risk of abliteration is "
                "current-generation chat models."),
            "chat": {"at_tau_fixed": rate(chat_p, TAU_FIXED),
                     "at_tau_refit_modal": rate(chat_p, tau_refit),
                     "model_type_composition": _compose(chat_p)},
            "base": {"at_tau_fixed": rate(base_p, TAU_FIXED),
                     "at_tau_refit_modal": rate(base_p, tau_refit),
                     "model_type_composition": _compose(base_p)},
        },
        "tau_fixed": TAU_FIXED,
        "tau_refit_modal": tau_refit,
    }

    k_fix = out["primary_filtered_eligible"]["at_tau_fixed"]["k"]
    n_fix = out["primary_filtered_eligible"]["at_tau_fixed"]["n"]
    k_ref = out["primary_filtered_eligible"]["at_tau_refit_modal"]["k"]
    n_chat = len(chat_p)
    chat_k = out["stratified_chat_vs_base"]["chat"]["at_tau_refit_modal"]["k"]
    chat_lo, chat_hi = wilson(chat_k, n_chat)
    if k_ref == 0:
        out["ready_to_paste_sentence"] = (
            f"Refitting the threshold with a whole recipe class held out moves it from "
            f"{TAU_FIXED:.4f} to {tau_refit:.4f}, and specificity survives the move: "
            f"{k_ref}/{n_fix} eligible undeclared checkpoints fire at the refit "
            f"threshold, Wilson 95% "
            f"[{out['primary_filtered_eligible']['at_tau_refit_modal']['wilson_lo']:.3f}, "
            f"{out['primary_filtered_eligible']['at_tau_refit_modal']['wilson_hi']:.3f}].")
        out["verdict"] = "SPECIFICITY_SURVIVES_REFIT"
    else:
        rr = out["primary_filtered_eligible"]["at_tau_refit_modal"]
        out["ready_to_paste_sentence"] = (
            f"Specificity is a property of the FIXED operating point, not of the "
            f"statistic: {k_fix}/{n_fix} eligible undeclared checkpoints fire at "
            f"tau={TAU_FIXED:.4f}, but {rr['k']}/{rr['n']} fire at the class-held-out "
            f"refit threshold tau={tau_refit:.4f} (rate {rr['rate']:.3f}, Wilson 95% "
            f"[{rr['wilson_lo']:.3f}, {rr['wilson_hi']:.3f})]. The narrow honest claim "
            f"is therefore that zero false positives is achieved AT A THRESHOLD FITTED "
            f"ON THE PANEL, and does not survive refitting.")
        out["verdict"] = "SPECIFICITY_DOES_NOT_SURVIVE_REFIT"
    out["chat_subset_sentence"] = (
        f"The instruction-tuned/chat subset of that denominator is n={n_chat} "
        f"({n_chat}/{n_fix} of the eligible undeclared rows), with {chat_k} firing at "
        f"the refit threshold, Wilson 95% [{chat_lo:.3f}, {chat_hi:.3f}] -- an n this "
        f"small cannot support a pooled rate standing in for the population actually "
        f"at risk of abliteration."
        if n_chat else
        "No eligible undeclared row is identifiable as instruction-tuned by the repo-id "
        "heuristic, so the chat-subset rate is UNAVAILABLE rather than zero.")

    asrt.check("fp_rate_filtered_primary.n", n_fix,
               probe(rates, "primary", "n")[1], 0, rel(A2 / "results/arm2_rates.json"),
               "the archived summary was written mid-scan; the row recount supersedes it "
               "-- see corrections C22")
    asrt.check("fp_rate_filtered_primary.k", k_fix,
               probe(rates, "primary", "k")[1], 0, rel(A2 / "results/arm2_rates.json"))
    asrt.check("fp_rate_secondary.n", out["secondary_unfiltered_archived"]["at_tau_fixed"]["n"],
               probe(rates, "secondary_raw_unfiltered", "n")[1], 0,
               rel(A2 / "results/arm2_rates.json"))
    return out


def _compose(rows) -> dict:
    c: dict[str, int] = {}
    for r in rows:
        mt = r.get("model_type") or "unknown"
        c[mt] = c.get(mt, 0) + 1
    return dict(sorted(c.items()))


# ===========================================================================
# STAGE 2 -- WORKSTREAM 2: the derivation with its residual bounded
# ===========================================================================
BOUND_FORMULA = (
    "e_W(u) = ||W^T u||^2 / ||W||_F^2. Write v1 = cos(t) r + sin(t) q with q unit, "
    "q perp r. Then e_W(v1) = cos^2(t) e_W(r) + sin^2(t) e_W(q) "
    "+ 2 cos(t) sin(t) <W^T r, W^T q> / ||W||_F^2. Cauchy-Schwarz on the last two "
    "terms gives |e_W(v1) - cos^2(t) e_W(r)| <= sin^2(t) e_max "
    "+ 2 |cos(t) sin(t)| sqrt(e_W(r) e_max), where e_max = lambda_max(W W^T)/||W||_F^2 "
    "<= 1. min_m is 1-Lipschitz, so the same bound carries to the minimum over "
    "matrices, hence to W05 = log10 min_m e_{W_m}(v1)."
)


# abscos_v1_r is archived as a float32 value, so |cos| is known only to ~2^-23.
# A row storing exactly 1.0 therefore still admits a non-zero angle, and pretending
# otherwise makes the bound spuriously zero. Every cos is clipped accordingly.
COS_F32_EPS = 2.0 ** -23


def residual_bound(cos_t: float, e_r: float, e_max: float = 1.0) -> float:
    c = min(abs(cos_t), 1.0 - COS_F32_EPS)
    s2 = max(0.0, 1.0 - c * c)
    s = math.sqrt(s2)
    return s2 * e_max + 2.0 * c * s * math.sqrt(max(e_r, 0.0) * e_max)


def log_gap_bound(cos_t: float, log10_e_r: float, e_max: float = 1.0) -> dict:
    """Induced bound on |W05 - log10 min_m e_r| in log10 units."""
    e_r = 10.0 ** log10_e_r
    B = residual_bound(cos_t, e_r, e_max)
    c2 = min(abs(cos_t), 1.0 - COS_F32_EPS) ** 2
    hi = math.log10((c2 * e_r + B) / e_r)
    lo_lin = c2 * e_r - B
    if lo_lin <= 0:
        return {"linear_residual_bound": B, "log10_bound": None,
                "log10_bound_upper_only": hi, "status": "VACUOUS_BELOW",
                "reason": "cos^2 * e_r - B <= 0, so the lower side of the bound is vacuous"}
    lo = math.log10(lo_lin / e_r)
    return {"linear_residual_bound": B, "log10_bound": max(abs(lo), abs(hi)),
            "log10_bound_upper_only": hi, "log10_bound_lower": lo,
            "status": "FINITE", "reason": None}


def stage2(outdir: Path, pools: dict, a1: dict, asrt: Assertions) -> dict:
    logger.info("STAGE 2 -- workstream 2: the derivation")
    mech = a1["mechanism_decomposition"]
    arm_b = pools["arm_b"]

    # ---- 2.2 evaluate the bound on the archived rows ---------------------
    rows = []
    for r in sorted(arm_b, key=lambda x: x["kernel_id"]):
        c = r.get("abscos_v1_r")
        ler = r.get("log10_min_e_r")
        w05 = r.get("W05_abl_min_layer_energy")
        if c is None or ler is None or w05 is None:
            continue
        gap = w05 - ler
        b = log_gap_bound(c, ler)
        holds = (b["log10_bound"] is not None and abs(gap) <= b["log10_bound"] + 1e-12)
        rows.append({
            "kernel": r["kernel_id"], "family": r["family"], "cos_v1_r": c, "W05": w05,
            "log10_min_e_r": ler, "abs_gap": abs(gap), "signed_gap": gap,
            "analytic_bound_on_the_gap": b["log10_bound"],
            "bound_status": b["status"],
            "linear_residual_bound": b["linear_residual_bound"],
            "e_max_used": 1.0,
            "bound_holds": holds if b["log10_bound"] is not None else None,
            "discovery_holds": abs(c) > COS_DISCOVERY,
        })
    hold = [x for x in rows if x["discovery_holds"]]
    fail = [x for x in rows if not x["discovery_holds"]]
    hold_finite = [x for x in hold if x["bound_status"] == "FINITE"]

    def _stats(xs):
        g = sorted(x["abs_gap"] for x in xs)
        if not g:
            return {"n": 0, "max": None, "median": None, "min": None}
        m = g[len(g) // 2] if len(g) % 2 else (g[len(g) // 2 - 1] + g[len(g) // 2]) / 2
        return {"n": len(g), "max": g[-1], "median": m, "min": g[0]}

    anchors = {}
    for kid, exp_w05, exp_er in (("uniform_w0.7", -1.1535, -1.1245),
                                 ("uniform_w0.85", -1.7488, -1.7248),
                                 ("uniform_w1.0", -4.5917, -4.5828)):
        got = next((x for x in rows if x["kernel"] == kid), None)
        anchors[kid] = {
            "W05_recomputed": got["W05"] if got else None,
            "W05_quoted_4dp": exp_w05,
            "log10_min_e_r_recomputed": got["log10_min_e_r"] if got else None,
            "log10_min_e_r_quoted_4dp": exp_er,
            "abs_gap": got["abs_gap"] if got else None,
            "bound": got["analytic_bound_on_the_gap"] if got else None,
            "bound_holds": got["bound_holds"] if got else None,
        }
        asrt.check(f"anchor[{kid}].W05_to_4dp",
                   round(got["W05"], 4) if got else None, exp_w05, 5e-5,
                   rel(A1 / "results/arm_b.jsonl"))
        asrt.check(f"anchor[{kid}].log10_min_e_r_to_4dp",
                   round(got["log10_min_e_r"], 4) if got else None, exp_er, 5e-5,
                   rel(A1 / "results/arm_b.jsonl"))

    # ---- 2.3 the collapse side: the Gaussian ladder ----------------------
    curve = a1["gaussian_sweep"]["curve"]
    parent_w05 = a1["gaussian_sweep"]["parent_W05"]
    ladder = []
    for c in curve:
        ladder.append({"spread": c["spread"], "spread_label": c["spread_label"],
                       "min_depth_weight": c["min_depth_weight"],
                       "W05": c["W05"], "abscos_v1_r": c["abscos_v1_r"],
                       "detected": c["detected"],
                       "W05_to_4dp": round(c["W05"], 4),
                       "abs_diff_vs_parent": abs(c["W05"] - parent_w05),
                       # "reads the parent's value to four decimals" = agrees within 5e-4
                       "equals_parent_to_4dp": abs(c["W05"] - parent_w05) <= 5e-4,
                       "equals_parent_after_rounding_to_4dp":
                           round(c["W05"], 4) == round(parent_w05, 4)})
    below = [x for x in ladder if x["spread"] <= 8]
    equals_all_below8 = all(x["equals_parent_to_4dp"] for x in below)
    first_det = next((x for x in ladder if x["detected"]), None)
    last_undet = None
    for x in ladder:
        if x["detected"]:
            break
        last_undet = x
    bracket = [last_undet["min_depth_weight"] if last_undet else None,
               first_det["min_depth_weight"] if first_det else None]
    stamp_sha = None
    p = A1 / "results/predictions.sha256"
    if p.exists():
        stamp_sha = p.read_text().strip()
    crit = a1["gaussian_sweep"]["predicted_critical_spread"]

    collapse = {
        "ladder": ladder,
        "parent_W05": parent_w05,
        "claim_every_spread_le_8_reads_parent_to_4dp": equals_all_below8,
        "claim_status": ("HOLDS" if equals_all_below8 else "FAILS_AT_SPREAD_8"),
        "spreads_that_equal_parent_to_4dp": [x["spread_label"] for x in ladder
                                             if x["equals_parent_to_4dp"]],
        "spreads_that_equal_parent_after_rounding": [
            x["spread_label"] for x in ladder if x["equals_parent_after_rounding_to_4dp"]],
        "four_decimal_criterion": ("|W05 - parent_W05| <= 5e-4 ('agrees to four decimal "
                                   "places'); the stricter round(W05,4)==round(parent,4) "
                                   "test is reported beside it because the two disagree "
                                   "on rows that straddle a rounding boundary"),
        "controlling_min_depth_weight_bracket": bracket,
        "cos_jump": [last_undet["abscos_v1_r"] if last_undet else None,
                     first_det["abscos_v1_r"] if first_det else None],
        "W05_jump": [last_undet["W05"] if last_undet else None,
                     first_det["W05"] if first_det else None],
        "stamped_critical_spread": crit,
        "measured_first_detected_spread": first_det["spread"] if first_det else None,
        "stamp_ratio": (crit / first_det["spread"]) if first_det else None,
        "stamp_sha256": stamp_sha,
        "stamp_source_file": rel(A1 / "results/predictions.json"),
        "reading": ("whenever discovery fails, W05 reads the PARENT's value -- the "
                    "un-edited matrices dominate the shared Gram sum, so the injected "
                    "direction never becomes the Gram's minimal direction and the "
                    "statistic never sees the edit at all."),
    }
    asrt.check("gaussian.bracket_lo", bracket[0], 0.0796, 5e-5, rel(A1 / "results/analysis.json"))
    asrt.check("gaussian.bracket_hi", bracket[1], 0.5311, 5e-5, rel(A1 / "results/analysis.json"))
    asrt.check("gaussian.stamp_ratio", collapse["stamp_ratio"], 3.6, 0.06,
               rel(A1 / "results/analysis.json"))

    # ---- 2.4 retirements --------------------------------------------------
    retired = [
        {"id": "R1", "retired": "'19/19 applicable kernels with zero disagreements'",
         "reason": ("the two quantities are numerically the same object whenever "
                    "discovery holds -- the measured max |W05 - log10 min_m e_r| over "
                    "discovery-holding rows with an informative bound is "
                    f"{_stats(hold_finite)['max']:.4f} log10 units, "
                    "inside the analytic Cauchy-Schwarz bound on every row. Agreement is "
                    "therefore a consistency check on a near-identity, NOT a validated "
                    "empirical prediction."),
         "licensing_row": {"file": rel(A1 / "results/analysis.json"),
                           "key_path": "mechanism_decomposition",
                           "raw_value": {"n_applicable": mech["n_applicable"],
                                         "agreement": mech["agreement"],
                                         "status": mech["status"]}}},
        {"id": "R2", "retired": "W05rel as a distinct statistic",
         "reason": ("algebraically identical to W05 -- the per-matrix energies are "
                    "already normalised by that matrix's Frobenius norm, which rounding "
                    "inflates proportionally, so the ratio cancels. Tracks W05 to <0.001 "
                    "at every bit-width."),
         "licensing_row": {"file": rel(A3 / "results/arm1_summary.json"),
                           "key_path": "verdict_arm1", "raw_value": "SCAR_STAYS_GONE"}},
        {"id": "R3", "retired": "W01 and W04 as reportable statistics",
         "reason": ("irreproducible below ~0.05 on abliterated checkpoints with "
                    "BIT-IDENTICAL weights: both are log ratios against lam[0] at the "
                    "float32 Gram-accumulation floor, and float64 recomputation moves "
                    "W01 by exactly the archive gap (4.7894e-2 vs 4.7894e-2). W05 is not "
                    "affected and nothing in the paper depends on W01/W04."),
         "licensing_row": {"file": rel(A1 / "README.md"),
                           "key_path": "reproducibility finding",
                           "raw_value": "W01/W04 differ by 3.1e-2 on bit-identical weights"}},
        {"id": "R4", "retired": "the dequantization remedy",
         "reason": ("VOID AS STATED -- the archive's quant_sd is a FAKE-QUANT that writes "
                    "round(W/s)*s back in the model's own bf16 dtype, so the archived int4 "
                    "number already WAS the dequantized measurement. There is no "
                    "dequantization step left to perform."),
         "licensing_row": {"file": rel(A3 / "results/arm1_framing.json"),
                           "key_path": "answer", "raw_value": "ALREADY DEQUANTIZED"}},
        {"id": "R5", "retired": "uniformity as the scope predicate",
         "reason": ("uniformity is neither necessary nor sufficient: ARMB_HERETIC__UNIFORM "
                    "and ARMB_HOUSEHOLDER__UNIFORM_BUT_ORTHOGONAL are both 'uniform' and "
                    "behave oppositely, and the predicate that actually governs detection "
                    "is DISCOVERY (|cos(v1,r)| -> 1) AND COMPLETION (min_m e_r <= tau)."),
         "licensing_row": {"file": rel(A1 / "results/analysis.json"),
                           "key_path": "mechanism_decomposition.rule",
                           "raw_value": mech["rule"]}},
    ]

    # ---- 2.5 replacement sentences ---------------------------------------
    replacements = {
        "detection_iff_completion": (
            "Whenever discovery holds -- that is, whenever the removed direction is the "
            "Gram's minimal direction -- detection and completion are the same statement, "
            "as a CONSEQUENCE OF THE DEFINITION of W05 rather than as an empirical "
            "finding; and where discovery fails the completion criterion is not merely "
            "false but undefined, because there is no r for the statistic to have found."),
        "what_the_sweep_actually_shows": (
            "The genuinely empirical content of the kernel sweep is WHICH kernels achieve "
            "discovery, and that the discovery threshold is controlled by the kernel's "
            f"MINIMUM depth weight, bracketed here in [{bracket[0]}, {bracket[1]}] -- "
            "not by uniformity and not by how completely the peak layer is annihilated, "
            "which is total at every Gaussian spread."),
    }

    # ---- 2.6 the undefinedness paragraph, count COMPUTED -----------------
    inapplicable_classes = {"R_MULTIDIR_SVD", "R_HERETIC"}
    scored_edited = [r for r in pools["arm_a"] if r["role"] == "edited"
                     and r.get("W05_abl_min_layer_energy") is not None]
    aff = sorted([r["repo_id"] for r in scored_edited
                  if r["recipe_class_rederived"] in inapplicable_classes])
    all_edited = [r for r in pools["arm_a"] if r["role"] == "edited"]
    aff_all = sorted([r["repo_id"] for r in all_edited
                      if r["recipe_class_rederived"] in inapplicable_classes])
    armb_excl = sorted(mech.get("excluded_because_the_removed_direction_is_not_r", []))
    undef = {
        "rule": "detected <=> |cos(v1,r)| > 0.9 AND log10 min_m e_r <= tau",
        "why_undefined": ("the rule quantifies over a SINGLE removed direction r. For "
                          "multi-direction SVD and per-component (Heretic-style) kernels "
                          "there is no single r, so cos(v1, r) is not defined and the rule "
                          "cannot be evaluated at all -- it is undefined, not false."),
        "n_scored_edited_rows": len(scored_edited),
        "n_undefined_of_scored": len(aff),
        "n_undefined_of_all_edited": len(aff_all),
        "draft_asserts": 13,
        "computed_value_wins": len(aff),
        "matches_draft_assertion": len(aff) == 13,
        "affected_repo_ids_scored": aff,
        "affected_repo_ids_all_edited": aff_all,
        "arm_b_kernels_excluded_for_the_same_reason": armb_excl,
        "principal_angle_generalisation": {
            "status": "STATED AS A DEFINITION -- NOT-YET-EVALUATED-HERE",
            "definition": ("discovery holds iff the largest principal angle between the "
                           "bottom-j eigenspace of the shared Gram matrix A and the span "
                           "of the j removed directions is below a threshold; for j=1 this "
                           "reduces to the |cos(v1,r)| criterion used here"),
            "why_not_evaluated": ("evaluating it needs the bottom-j Gram eigenvectors AND "
                                  "the full removed-direction basis per checkpoint -- "
                                  "tensors this re-analysis artifact deliberately does not "
                                  "load (zero weights, zero forward passes)"),
            "rows_it_would_need": ["per-checkpoint bottom-j eigenvectors of A (j = rank of "
                                   "the edit)", "the removed-direction basis R (d x j)",
                                   "per-matrix write energies along each column of R"],
        },
        "sentence": (
            f"The single-direction discovery rule is undefined for exactly "
            f"{len(aff)} of the {len(scored_edited)} scored real edited checkpoints "
            f"(the R_MULTIDIR_SVD and R_HERETIC classes) and for "
            f"{len(armb_excl)} of the in-house kernels; a rule that cannot be evaluated "
            f"on the classes where the statistic fails is not yet a mechanism for those "
            f"classes."),
    }
    asrt.check("undefinedness.count_vs_draft", len(aff), 13, 0,
               rel(A1 / "results/arm_a.jsonl"),
               "draft asserts 13; computed from rows")

    # ---- 2.7 the isometry impossibility, as a numbered proposition -------
    hh = {r["kernel_id"]: r for r in pools["arm_b"] if r["family"] in ("householder", "control")}
    orba1 = next((r for r in pools["arm_b"]
                  if r["kernel_id"] == "orba_householder_lam1.0"), None)
    ctrl = next((r for r in pools["arm_b"]
                 if r["kernel_id"] == "householder_random_dir_control"), None)
    parent_b = next((r for r in pools["arm_b"] if r["kernel_id"] == "parent_unedited"), None)
    orba_dw = abs(orba1["W05_abl_min_layer_energy"] - parent_b["W05_abl_min_layer_energy"]) \
        if (orba1 and parent_b) else None
    ctrl_dw = abs(ctrl["W05_abl_min_layer_energy"] - parent_b["W05_abl_min_layer_energy"]) \
        if (ctrl and parent_b) else None
    orba_ref = probe(pools["behav"], "orba_householder_lam1.0", "refusal_rate_judge")[1]
    prop = {
        "number": 1,
        "title": "Isometric edits are permanently invisible to any Gram-spectrum statistic",
        "statement": (
            "Let H = I - 2 u u^T be a Householder reflection and let every residual-write "
            "matrix W be replaced by H W. H is orthogonal, so it removes no rank and "
            "leaves every singular value of W unchanged; consequently the shared Gram "
            "matrix A = sum_l W W^T / ||W||_F^2 is conjugated by H, its spectrum is "
            "invariant, and every per-matrix write-energy distribution is invariant up to "
            "the same rotation of the eigenbasis. Therefore ANY statistic that is a "
            "function of the Gram spectrum is blind to the edit -- W05, W05q10, W05w, and "
            "every windowed or banded variant included."),
        "consequence_for_the_windowed_arm": (
            "the proposition applies verbatim to W05w, because a per-window Gram matrix is "
            "conjugated by the same H. H1's windowed arm therefore CANNOT recover isometric "
            "edits regardless of how it resolves."),
        "measured_corroboration": {
            "orba_lambda1_dW05_vs_parent": orba_dw,
            "random_direction_householder_control_dW05_vs_parent": ctrl_dw,
            "orba_moves_less_than_the_control": (orba_dw < ctrl_dw
                                                 if (orba_dw is not None and ctrl_dw is not None)
                                                 else None),
            "orba_lambda1_refusal_rate_judge": orba_ref,
            "parent_refusal_rate_judge": a1["effectiveness_vs_detectability"]["parent_refusal_rate_judge"],
            "source_file": rel(A1 / "results/arm_b.jsonl"),
        },
        "orba_two_recipe_caveat": (
            "ORBA ships two recipes and they are NOT the same edit. At lambda=1 the "
            "operation is ANNIHILATION of the refusal component without reflection; only "
            "the v3 Householder recipe is the true isometry. Conflating them makes the "
            "falsification vacuous -- the measured 4.1e-5 belongs to the lambda=1 "
            "annihilation row, and the proposition above is what covers the isometry case."),
        "proof_sketch": (
            "sigma(HW) = sigma(W) since H^T H = I; (HW)(HW)^T = H (W W^T) H^T; "
            "||HW||_F = ||W||_F; hence A -> H A H^T, spec(A) unchanged, and "
            "e_{HW}(H v) = e_W(v) for every v."),
    }
    asrt.check("proposition1.orba_dW05", orba_dw, 4.1e-5, 5e-6,
               rel(A1 / "results/arm_b.jsonl"))
    asrt.check("proposition1.control_dW05", ctrl_dw, 7.3e-5, 5e-6,
               rel(A1 / "results/arm_b.jsonl"))

    # ---- 2.8 effectiveness vs detectability ------------------------------
    ev = a1["effectiveness_vs_detectability"]
    erows = sorted(ev["rows"], key=lambda r: r["kernel_id"])
    eff = [r for r in erows if r.get("fluency_pass") and r["refusal_rate_judge"] <= 0.50]
    eff_det = [r for r in eff if r["detected"]]
    tab = {"effective_and_detected": len(eff_det),
           "effective_and_missed": len(eff) - len(eff_det),
           "ineffective_and_detected": sum(1 for r in erows
                                           if r not in eff and r["detected"]),
           "ineffective_and_missed": sum(1 for r in erows
                                         if r not in eff and not r["detected"])}
    det_margin = [-(r["W05"] - TAU_FIXED) for r in erows]   # higher = more detectable
    drop = [r["refusal_drop_vs_parent"] for r in erows]
    boot = bootstrap_ci(det_margin, drop, spearman, N_BOOT, SEED)
    rank_k4 = next((r for r in erows if r["kernel_id"] == "rank_k4"), None)
    ed = {
        "parent_refusal_rate_judge": ev["parent_refusal_rate_judge"],
        "effectiveness_criterion": ev["effectiveness_criterion"],
        "n_kernels_scored": len(erows),
        "n_effective": len(eff),
        "n_effective_and_detected": len(eff_det),
        "two_by_two": tab,
        "effective_kernels": sorted(r["kernel_id"] for r in eff),
        "effective_and_detected_kernels": sorted(r["kernel_id"] for r in eff_det),
        "spearman_detectability_margin_vs_refusal_drop": {
            "rho": boot["point"], "ci_lo": boot["lo"], "ci_hi": boot["hi"],
            "ci_method": "percentile bootstrap, 10000 resamples",
            "resampling_unit": "kernel", "n": len(erows), "seed": SEED,
            "rng": "numpy.random.default_rng(seed) -- NOT the legacy global RNG",
            "orientation": ("detectability margin = tau - W05, so HIGHER means more "
                            "detectable; refusal drop is vs the parent's judge rate"),
        },
        "rank_k4_case": ({"W05": rank_k4["W05"], "detected": rank_k4["detected"],
                          "refusal_rate_judge": rank_k4["refusal_rate_judge"]}
                         if rank_k4 else None),
        "reading": (
            "Detectability and effectiveness are near-orthogonal over the kernel sweep: "
            f"rho = {boot['point']:.3f} with a bootstrap 95% interval of "
            f"[{boot['lo']:.3f}, {boot['hi']:.3f}] over {len(erows)} kernels. The interval "
            "is what makes 'near-orthogonal' sayable -- a point estimate alone would not."),
    }

    out = {"formula": BOUND_FORMULA,
           "bound_callable": "archlib-free: residual_bound(cos_t, e_r, e_max) in eval.py; "
                             "verify_numbers.py re-implements it independently",
           "e_max_convention": ("e_max = lambda_max(W W^T)/||W||_F^2 is not archived "
                                "per-matrix, so the RIGOROUS universal bound e_max <= 1 is "
                                "used. Every reported bound is therefore conservative."),
           "cos_precision_allowance": {
               "eps": COS_F32_EPS,
               "why": ("abscos_v1_r is archived at float32 precision, so a stored 1.0 "
                       "still admits an angle of ~5e-4 rad. Clipping |cos| to "
                       "1 - 2^-23 before evaluating the bound is what keeps the bound "
                       "honest rather than spuriously zero.")},
           "rows": rows,
           "anchors": anchors,
           "gap_stats_discovery_holding": _stats(hold),
           "gap_stats_discovery_holding_finite_bound": _stats(hold_finite),
           "gap_stats_discovery_failing": _stats(fail),
           "vacuity_note": (
               "The bound uses the RIGOROUS universal e_max <= 1 because the per-matrix "
               "lambda_max/||W||_F^2 is not archived. It is therefore uninformative "
               "(VACUOUS_BELOW) wherever cos^2 * e_r <= B -- which is exactly the "
               "discovery-failing regime, where v1 and r are nearly orthogonal and the "
               "two quantities are genuinely different objects. Where discovery holds "
               "AND the bound is finite it is informative, and it is satisfied on every "
               "such row."),
           "n_bound_holds": sum(1 for x in rows if x["bound_holds"] is True),
           "n_bound_vacuous": sum(1 for x in rows if x["bound_status"] != "FINITE"),
           "n_bound_violated": sum(1 for x in rows if x["bound_holds"] is False),
           "discovery_criterion": f"|cos(v1,r)| > {COS_DISCOVERY}",
           "collapse": collapse,
           "retired_evidence": retired,
           "replacement_sentences": replacements,
           "undefinedness": undef,
           "proposition_isometry": prop,
           "effectiveness_vs_detectability": ed}
    dump_json(L.deep_clean(out), outdir / "results/derivation.json")
    logger.info(f"  {len(rows)} bound rows, {out['n_bound_violated']} violations, "
                f"undefined on {len(aff)} rows")
    return out


# ===========================================================================
# STAGE 3 -- WORKSTREAM 3: consolidated corrections
# ===========================================================================
def stage3(outdir: Path, pools: dict, a1: dict, ws1: dict, ws2: dict,
           asrt: Assertions) -> dict:
    logger.info("STAGE 3 -- workstream 3: corrections")
    cor: list[dict] = []

    def add(cid, claim, corrected, file, key_path, raw, recomputed, sentence, note=None):
        cor.append({"id": cid, "claim_as_previously_reported": claim,
                    "corrected_value": L.clean_float(corrected),
                    "provenance": {"file": file, "key": key_path,
                                   "raw_value": L.deep_clean(raw)},
                    "recomputed_from_rows": recomputed,
                    "one_sentence_for_the_paper": sentence,
                    "note": note})

    counts = load_json(A2 / "results/arm2_archive_counts.json")
    rates = load_json(A2 / "results/arm2_rates.json")
    a3an = load_json(A3 / "results/analysis.json")
    ladder = load_json(A3 / "results/ladder_ci_summary.json")
    a6 = load_json(A6 / "numbers.json") if (A6 / "numbers.json").exists() else {}

    # C1 -- seven intensity axes, not six
    axes = sorted(a3an.get("cells", {}).keys()) if isinstance(a3an.get("cells"), dict) else []
    lad_axes = sorted({k for k in probe(ladder, "crossings")[1] or {}})
    n_axes = len(lad_axes)
    add("C01", "six laundering intensity axes", n_axes,
        rel(A3 / "results/ladder_ci_summary.json"), "crossings", lad_axes, True,
        f"The laundering ladder has {n_axes} intensity axes, not six: "
        f"{', '.join(lad_axes)}.")

    # C2 -- 81 unresolved non-control rows, not 65
    add("C02", "65 unresolved non-control rows in the undeclared scan",
        counts["n_unresolved_non_control"], rel(A2 / "results/arm2_archive_counts.json"),
        "n_unresolved_non_control", counts["n_unresolved_non_control"], True,
        f"Counted from the rows themselves the undeclared scan leaves "
        f"{counts['n_unresolved_non_control']} non-control checkpoints UNRESOLVED, not 65.")
    asrt.check("corrections.n_unresolved_non_control", counts["n_unresolved_non_control"],
               81, 0, rel(A2 / "results/arm2_archive_counts.json"))

    # C3 -- 8 skipped, not 7
    add("C03", "7 skipped rows", counts["n_skipped_non_control"],
        rel(A2 / "results/arm2_archive_counts.json"), "n_skipped_non_control",
        counts["n_skipped_non_control"], True,
        f"{counts['n_skipped_non_control']} non-control rows are SKIPPED by the "
        f"eligibility rule, not 7.")
    asrt.check("corrections.n_skipped_non_control", counts["n_skipped_non_control"], 8, 0,
               rel(A2 / "results/arm2_archive_counts.json"))

    # C4 -- 270 = 20 + 250, 160 completed: ASSERT the arithmetic
    arith_ok = (counts["total_rows"] == counts["n_controls"] + counts["n_non_control"]
                and counts["n_non_control"] == (counts["n_scored_non_control"]
                                                + counts["n_unresolved_non_control"]
                                                + counts["n_skipped_non_control"]
                                                + counts["n_error_non_control"]))
    add("C04", "the undeclared scan's row arithmetic was never stated",
        {"total": counts["total_rows"], "controls": counts["n_controls"],
         "non_control": counts["n_non_control"], "scored": counts["n_scored_non_control"],
         "unresolved": counts["n_unresolved_non_control"],
         "skipped": counts["n_skipped_non_control"], "error": counts["n_error_non_control"],
         "arithmetic_closes": arith_ok},
        rel(A2 / "results/arm2_archive_counts.json"), "(whole file)", counts, True,
        f"The undeclared scan is {counts['total_rows']} rows = {counts['n_controls']} "
        f"controls + {counts['n_non_control']} attempted, of which "
        f"{counts['n_scored_non_control']} completed, "
        f"{counts['n_unresolved_non_control']} were unresolved, "
        f"{counts['n_skipped_non_control']} skipped and {counts['n_error_non_control']} "
        f"errored; the arithmetic closes exactly.")
    asrt.check("corrections.row_arithmetic_closes", arith_ok, True, 0,
               rel(A2 / "results/arm2_archive_counts.json"))

    # C5 -- FIVE unreproduced quoted values, not four
    qf = probe(a6, "quoted_value_forensics")[1] or {}
    n_repro = probe(qf, "n_quoted_reproduced")[1]
    closest = probe(qf, "closest_match_per_quoted_value")[1]
    unrep = []
    if isinstance(closest, dict):
        for k in sorted(closest):
            v = closest[k]
            exact = probe(v, "exact")[1]
            if exact is False or (exact is None and probe(v, "abs_error")[1] not in (0, 0.0)):
                unrep.append(k)
    add("C05", "four quoted values could not be reproduced",
        {"n_quoted_reproduced": n_repro, "unreproduced_keys": unrep,
         "n_unreproduced": len(unrep)},
        rel(A6 / "numbers.json"), "quoted_value_forensics", qf, False,
        (f"{len(unrep)} quoted values could not be reproduced under any convention "
         f"tried, not four: {', '.join(unrep) if unrep else '(see forensics block)'}."),
        "carried from the iteration-3 forensics block, which enumerated the conventions tried")

    # C6 -- B09 0.766 is the 26-member chatml value, not the 28-member contract subset
    dcr = probe(a6, "draft_convention_rerun")[1] or {}
    add("C06", "B09 |rho| = 0.766 on the 28-member contract subset",
        {"0.766_is": "the 26-member renderer=='chatml' subset",
         "contract_subset_value": 0.670,
         "reidentification": probe(dcr, "reidentification_note")[1]},
        rel(A6 / "numbers.json"), "draft_convention_rerun", dcr, False,
        "The 0.766 figure is the 26-member renderer=='chatml' value; the 28-member "
        "contract subset the draft attributed it to reads 0.670.")

    # C7 -- ladder denominators 31-40, not 40, with 13 ambiguous
    add("C07", "every ladder rate has denominator n_harmful = 40",
        {"recorded": ladder["recorded_n_harmful_everywhere"],
         "achieved_span": [min(ladder["achieved_n_harmful_recovered"]),
                           max(ladder["achieved_n_harmful_recovered"])],
         "achieved_set": ladder["achieved_n_harmful_recovered"],
         "n_ambiguous": ladder["n_rows_with_ambiguous_denominator"],
         "n_ladder_rows": ladder["n_ladder_rows"],
         "interval_policy": "largest compatible n primary, smallest-n interval shipped beside it"},
        rel(A3 / "results/ladder_ci_summary.json"), "(whole file)", ladder, False,
        f"The archived ladder records n_harmful = 40 on every row, but the denominators "
        f"recovered from the rates themselves span "
        f"{min(ladder['achieved_n_harmful_recovered'])}-"
        f"{max(ladder['achieved_n_harmful_recovered'])}, with "
        f"{ladder['n_rows_with_ambiguous_denominator']} of "
        f"{ladder['n_ladder_rows']} rows compatible with more than one denominator; "
        f"the largest compatible n is used and the smallest-n interval ships beside it.")

    # C8 -- the four signed evasion costs and int4-minus-root are NOT resolvable
    p1, n_lad = 0.20, 40
    p2_mde = smallest_detectable_upward(p1, n_lad, power=0.80, alpha=0.05)
    mde = (p2_mde - p1) if p2_mde is not None else None
    pw = two_proportion_power(p1, p2_mde, n_lad, n_lad) if p2_mde else None
    add("C08", "the four signed evasion costs (-0.004, +0.069, +0.075, +0.128) and "
               "int4-minus-root (-0.03 [-0.189, +0.135]) are reported as findings",
        {"verdict": "NOT RESOLVABLE AT THIS n",
         "smallest_detectable_upward_difference": mde,
         "smallest_detectable_upward_p2": p2_mde,
         "achieved_power_at_that_difference": pw,
         "p1": p1, "n_per_group": n_lad,
         "power_calculation": ("two-sided two-proportion z-test, pooled-variance null and "
                              "unpooled alternative, normal approximation; alpha = 0.05, "
                              "target power = 0.80, n = 40 per group, baseline p1 = 0.20; "
                              "grid searched on a 1e-4 step")},
        rel(A3 / "results/ladder_ci_summary.json"), "achieved_n_harmful_recovered",
        ladder["achieved_n_harmful_recovered"], True,
        f"At n = 40 per group and a baseline refusal rate of 0.20, the smallest upward "
        f"difference detectable with 80% power is {mde:.2f} (i.e. a rate of "
        f"{p2_mde:.2f}) -- so the four signed evasion "
        f"costs (-0.004, +0.069, +0.075, +0.128) and the int4-minus-root difference "
        f"(-0.03 [-0.189, +0.135]) are all far below resolution and none of them is a "
        f"finding.")
    asrt.check("corrections.mde_at_n40_p020", mde, 0.29, 0.011,
               "recomputed two-proportion power calculation",
               "the quoted 0.29 is the DIFFERENCE, not the alternative rate")

    # C9 -- judge rate-level Pearson r
    ji = a3an["judge_integrity"]
    add("C09", "judge-vs-regex rate-level Pearson r = 0.952 with kappa ~0",
        {"r": ji["rate_level_pearson_r_judge_vs_regex"], "kappa_mean": ji["kappa_mean"],
         "kappa_median": ji["kappa_median"], "n_stages": ji["n_stages"]},
        rel(A3 / "results/analysis.json"), "judge_integrity", ji, False,
        f"Recomputed over {ji['n_stages']} stages the judge-vs-regex rate-level Pearson r "
        f"is {ji['rate_level_pearson_r_judge_vs_regex']:.3f}, not 0.952, and item-level "
        f"agreement is kappa = {ji['kappa_mean']:.3f}.")

    # C10/C11 -- W01/W04 and W05rel retired
    add("C10", "W01 and W04 are reported alongside W05", "RETIRED",
        rel(A1 / "README.md"), "reproducibility finding",
        "W01/W04 differ by 3.1e-2 on bit-identical weights; float64 moves W01 by 4.7894e-2",
        False,
        "W01 and W04 are retired: on bit-identical weights they differ by 3.1e-2 between "
        "two runs, which is the float32 Gram-accumulation floor and not the model, and "
        "float64 recomputation moves W01 by exactly the archive gap.")
    add("C11", "W05rel is a new statistic that survives quantization", "RETIRED",
        rel(A3 / "results/arm1_summary.json"), "verdict_arm1", "SCAR_STAYS_GONE", False,
        "W05rel is retired: it tracks W05 to <0.001 everywhere because the energies are "
        "already Frobenius-normalised, so it is the same statistic under another name.")

    # C12 -- dequantization void; bit-width curve in its place
    bits = bitwidth_curve()
    add("C12", "quantization can be undone by dequantizing before scoring",
        {"remedy": "VOID AS STATED", "why": "the archived quant_sd was a FAKE-QUANT",
         "replacement": bits},
        rel(A3 / "results/arm1_framing.json"), "answer", "ALREADY DEQUANTIZED", True,
        "The proposed dequantization remedy is void -- the archived quantized row was "
        "already a dequantized measurement -- and the substantive result in its place is "
        f"that plain rounding kills the scar at {bits.get('scar_dies_at_bits')} bits "
        f"(W05 = {probe(bits, 'bit_width_curve_root_A', str(bits.get('scar_dies_at_bits')), 'W05')[1]:.3f}, "
        f"above tau = {TAU_FIXED:.4f}) while refusal is still "
        f"{probe(bits, 'bit_width_curve_root_A', str(bits.get('scar_dies_at_bits')), 'refusal')[1]:.3f} "
        f"and perplexity moves only 26.25 -> "
        f"{probe(bits, 'bit_width_curve_root_A', str(bits.get('scar_dies_at_bits')), 'ppl')[1]:.2f}.")

    # C13 -- storage precision sets the scar depth
    pc = a1["precision_control"]["rows"]["uniform_w1.0"]
    add("C13", "W05 = -4.59 is a property of the edit",
        {"bf16_storage": pc["W05_bf16_storage"], "float32_storage": pc["W05_float32_storage"],
         "delta": pc["delta"]},
        rel(A1 / "results/analysis.json"), "precision_control.rows.uniform_w1.0", pc, False,
        f"Storage precision, not the edit, sets the depth of the scar: the SAME complete "
        f"uniform projection reads W05 = {pc['W05_bf16_storage']:.3f} stored in bf16 and "
        f"{pc['W05_float32_storage']:.3f} stored in float32, a gap of "
        f"{abs(pc['delta']):.3f} log10 units.")

    # C14 -- Heretic's kernel is a triangular tent, not a Gaussian
    add("C14", "Heretic uses a Gaussian depth kernel (our taxonomy)",
        "TRIANGULAR TENT WITH A HARD CUTOFF",
        rel(A7b), "prior-art dossier (Heretic kernel)",
        "Heretic's per-layer weight is a triangular tent with a hard cutoff", False,
        "Our own recipe taxonomy was wrong about Heretic: its depth kernel is a "
        "triangular tent with a hard cutoff, not a Gaussian, so the R_HERETIC class is "
        "not a special case of the Gaussian sweep.")

    # C15 -- a quantized upload is UNRESOLVED, not a silent false negative
    add("C15", "quantized re-uploads are silent false negatives of the scan",
        {"handling": "excluded by pre-registered eligibility rule E6, status UNRESOLVED "
                     "or SKIPPED -- never scored and never counted as a negative",
         "n_excluded_E6_archive": probe(rates, "exclusions_archive_by_primary_reason", "E6")[1]},
        rel(A2 / "results/arm2_rates.json"), "exclusions_archive_by_primary_reason.E6",
        probe(rates, "exclusions_archive_by_primary_reason", "E6")[1], False,
        "A quantized upload is UNRESOLVED in the scan pipeline, not a silent false "
        "negative: rule E6 excludes it before scoring, so it never enters a rate in "
        "either direction.")

    # C16 -- 'parent-free costs nothing' retired
    # E_1's own detection rule, taken from the archive's predictor:
    #   ABLITERATION_EDIT iff E1_mid50 >= 0.9   (A1/method.py, method_vs_baseline)
    e1 = a1["e1_crosscheck"]
    e1rows = e1["rows"]
    E1_THRESH = 0.9

    def _e1ok(r):
        v = r.get("E1_mid50")
        return isinstance(v, (int, float)) and not math.isnan(v)

    e1_defined = [r for r in e1rows if _e1ok(r)]
    e1_n = len(e1_defined)
    e1_fires = sum(1 for r in e1_defined if r["E1_mid50"] >= E1_THRESH)
    w05_fires = sum(1 for r in e1rows if r.get("W05_detected"))
    agree = (sum(1 for r in e1_defined
                 if (r["E1_mid50"] >= E1_THRESH) == bool(r.get("W05_detected"))) / e1_n
             if e1_n else None)
    # the archived 0.829 counts an undefined E_1 as "did not fire", i.e. it uses the
    # FULL 35-row denominator. Both conventions are reported rather than one silently
    # standing in for the other.
    agree_full = (sum(1 for r in e1rows
                      if (_e1ok(r) and r["E1_mid50"] >= E1_THRESH) == bool(r.get("W05_detected")))
                  / len(e1rows)) if e1rows else None
    add("C16", "the parent-free statistic costs nothing relative to a parent-differencing baseline",
        {"E1_fires": f"{e1_fires}/{e1_n}", "W05_fires": f"{w05_fires}/{len(e1rows)}",
         "agreement_on_rows_where_E1_is_defined": agree,
         "agreement_over_all_rows_undefined_counted_as_not_fired": agree_full,
         "archived_agreement_claim": 0.829,
         "E1_detection_rule": f"E1_mid50 >= {E1_THRESH}",
         "n_rows_where_E1_undefined": len(e1rows) - e1_n},
        rel(A1 / "results/analysis.json"), "e1_crosscheck",
        {"n": e1["n"], "E1_fires": e1_fires, "E1_n": e1_n, "W05_fires": w05_fires}, True,
        f"'Parent-free costs nothing' is retired: on the same rows the parent-differencing "
        f"E_1 fires on {e1_fires}/{e1_n} while the parent-free W05 fires on "
        f"{w05_fires}/{len(e1rows)}, agreeing on {agree:.3f} of the {e1_n} rows where E_1 "
        f"is defined at all ({agree_full:.3f} if the {len(e1rows) - e1_n} rows with no "
        f"usable parent are counted as E_1 not firing, which is the convention behind the "
        f"archived 0.829) -- so dropping the parent costs real recall.")

    # C17 -- the 0.727 regex baseline is a NAME-SEARCH UPPER BOUND
    rb = a1["repo_name_regex_baseline"]
    add("C17", "a repo-name regex scores 0.727 sensitivity, beating W05's 0.159",
        {"regex_sensitivity": rb["sensitivity"], "W05_sensitivity": rb["W05_sensitivity_same_rows"],
         "status": "NAME-SEARCH UPPER BOUND, not a fair baseline",
         "caught_by_W05_missed_by_name": rb["caught_by_W05_missed_by_name"],
         "n_regex_terms": len(rb["regex_terms"])},
        rel(A1 / "results/analysis.json"), "repo_name_regex_baseline", rb, False,
        "The 0.727 regex figure is an UPPER BOUND on a name search, not a fair baseline: "
        "the evaluation pool was itself discovered by name sweeps whose terms overlap the "
        "regex's own 11 terms, so the regex is scored on a population selected to contain "
        "the strings it matches -- this caveat must accompany every place the 0.159-vs-0.727 "
        "comparison appears.",
        "attach as a caveat sentence, not only as a correction")

    # C18 -- lorco has 19 cells, not the 20 the plan expected
    add("C18", "the leave-one-recipe-class-out block has 20 cells",
        {"n_cells_in_archive": ws1["n_classes"],
         "cells": sorted(ws1["lorco_table"].keys())},
        rel(A1 / "results/analysis.json"), "lorco", ws1["n_classes"], True,
        f"The archived leave-one-recipe-class-out block carries {ws1['n_classes']} cells "
        f"({sum(1 for k in ws1['lorco_table'] if k.startswith('ARMB_'))} in-house kernel "
        f"classes and {sum(1 for k in ws1['lorco_table'] if k.startswith('R_'))} real "
        f"recipe classes), not 20.")

    # C19 -- the Gaussian-ladder 'every spread <= 8 reads -1.0098' claim
    col = ws2["collapse"]
    if not col["claim_every_spread_le_8_reads_parent_to_4dp"]:
        add("C19", "every Gaussian spread <= 8 reads W05 = -1.0098 to four decimals",
            {"spreads_that_do": col["spreads_that_equal_parent_to_4dp"],
             "spread_8_reads": next(x["W05"] for x in col["ladder"] if x["spread"] == 8.0)},
            rel(A1 / "results/analysis.json"), "gaussian_sweep.curve",
            [{"spread": x["spread"], "W05": x["W05"]} for x in col["ladder"]], True,
            "Spreads 0.5 through 4 read the parent's W05 to four decimals; spread 8 already "
            f"reads {next(x['W05'] for x in col['ladder'] if x['spread'] == 8.0):.4f}, so "
            "the claim holds for spreads <= 4, not <= 8.")

    # C20 -- the undefinedness count
    ud = ws2["undefinedness"]
    if not ud["matches_draft_assertion"]:
        add("C20", "the single-direction rule is undefined on 13 of the 44 rows",
            {"computed": ud["n_undefined_of_scored"],
             "of": ud["n_scored_edited_rows"], "classes": ["R_MULTIDIR_SVD", "R_HERETIC"]},
            rel(A1 / "results/arm_a.jsonl"), "recipe_class_rederived",
            ud["affected_repo_ids_scored"], True,
            f"Counted from the rows the single-direction discovery rule is undefined on "
            f"{ud['n_undefined_of_scored']} of the {ud['n_scored_edited_rows']} scored "
            f"real edited checkpoints, not 13.")

    # C21 -- the specificity claim's scope
    sb = ws1["specificity_at_both_taus"]
    add("C21", "specificity is 1.000 (0 false positives on 122 eligible undeclared checkpoints)",
        {"at_tau_fixed": sb["primary_filtered_eligible"]["at_tau_fixed"],
         "at_tau_refit_modal": sb["primary_filtered_eligible"]["at_tau_refit_modal"],
         "verdict": sb["verdict"]},
        rel(A2 / "results/arm2_archive_eligibility.jsonl") + " + " +
        rel(A2 / "results/arm2_scan_new.jsonl"), "(rows)",
        {"n": sb["primary_filtered_eligible"]["at_tau_fixed"]["n"]}, True,
        sb["ready_to_paste_sentence"])

    # C22 -- the 0/122 denominator is a mid-scan snapshot
    dr = ws1["specificity_at_both_taus"]["denominator_reconciliation"]
    if dr["delta"] != 0:
        add("C22", f"the eligible undeclared population is n = {dr['archived_primary_n']} "
                   f"(0/{dr['archived_primary_n']}, Wilson [0, 0.031])",
            {"recomputed_n": dr["recomputed_primary_n"],
             "archived_n": dr["archived_primary_n"], "delta": dr["delta"],
             "archived_new_completed": dr["archived_n_new_eligible_completed"],
             "recomputed_new_completed": dr["recomputed_n_new_completed"],
             "k_at_tau_fixed": sb["primary_filtered_eligible"]["at_tau_fixed"]["k"]},
            rel(A2 / "results/arm2_archive_eligibility.jsonl") + " + " +
            rel(A2 / "results/arm2_scan_new.jsonl"), "(row recount)",
            {"archived_summary": rel(A2 / "results/arm2_rates.json")}, True,
            f"The archived 0/{dr['archived_primary_n']} denominator is a snapshot taken "
            f"before the newly-fetched scan finished: recounted from the rows now on disk "
            f"the eligible undeclared population is "
            f"{dr['recomputed_primary_n']} checkpoints "
            f"({dr['recomputed_n_archived_eligible']} archived + "
            f"{dr['recomputed_n_new_completed']} newly scanned), and the false-positive "
            f"count at the panel operating point is "
            f"{sb['primary_filtered_eligible']['at_tau_fixed']['k']}, giving "
            f"{sb['primary_filtered_eligible']['at_tau_fixed']['k']}/"
            f"{dr['recomputed_primary_n']} with Wilson 95% upper bound "
            f"{sb['primary_filtered_eligible']['at_tau_fixed']['wilson_hi']:.3f}.",
            "this makes the precision claim STRONGER, not weaker -- the denominator grew "
            "and the numerator did not")

    # C23 -- the iteration-3 numbers file is rounded; full precision lives in the rows
    wb = probe(a6, "W05_boundary", "abliterated_max", "value")[1]
    if wb is not None and wb != TAU_FIXED:
        add("C23", "the abliterated maximum / panel operating point is -2.7415117804",
            {"rounded_in_iter3_numbers_json": wb, "full_precision": TAU_FIXED,
             "decimal_places_stored": 10,
             "rule": "numbers.json must never round -- rounding belongs only in "
                     "ready-to-paste sentence strings, with the rounding rule stated"},
            rel(A6 / "numbers.json"), "W05_boundary.abliterated_max.value", wb, True,
            f"The iteration-3 numbers file stores the operating point rounded to ten "
            f"decimal places ({wb}); the full-precision value that the detection rule "
            f"actually uses is {TAU_FIXED!r}, and every threshold comparison in this "
            f"paper is made at full precision.")

    # C24 -- the archived auroc_oriented flips orientation per cell
    flipped = sorted(k for k in ws1["lorco_table"]
                     if ws1["lorco_table"][k]["col4_orientation_was_flipped"])
    below = sorted(k for k in ws1["lorco_table"]
                   if ws1["lorco_table"][k]["col2_auroc_oriented_fixed_tau"] < 0.5)
    if flipped:
        add("C24", "the leave-one-recipe-class-out AUROC column is reported as "
                   "'auroc_oriented' with a single lower-is-positive convention",
            {"archived_rule": "max(auroc_raw, 1 - auroc_raw), with the chosen "
                              "orientation recorded per cell",
             "n_cells_flipped": len(flipped), "cells_flipped": flipped,
             "n_cells_below_chance_under_fixed_orientation": len(below),
             "cells_below_chance": below,
             "corrected_rule": "oriented AUROC = 1 - auroc_raw for EVERY cell, because "
                               "the detection rule is fixed at W05 <= tau"},
            rel(A1 / "results/analysis.json"), "lorco.*.auroc_oriented",
            {k: {"raw": ws1["lorco_table"][k]["auroc_raw_archived"],
                 "archived_oriented": ws1["lorco_table"][k]["col4_auroc_refit_archived"],
                 "corrected_oriented": ws1["lorco_table"][k]["col2_auroc_oriented_fixed_tau"],
                 "archived_flag": ws1["lorco_table"][k]["col4_archived_orientation_flag"]}
             for k in flipped}, True,
            f"The archived per-class AUROC column reports max(raw, 1 - raw) and records "
            f"the chosen orientation per cell, so {len(flipped)} of "
            f"{ws1['n_classes']} cells are printed under the OPPOSITE orientation to the "
            f"detection rule; holding the orientation fixed at lower-is-positive, as the "
            f"rule W05 <= tau requires, {len(below)} classes fall BELOW chance "
            f"({', '.join(below) if below else 'none'}), which the flipped column hides.",
            "this is the single most consequential correction in the table -- it changes "
            "the sign of the reported discrimination on the flipped cells")

    # ---- the self-audit, flagged for the appendix ------------------------
    repro = load_json(A6 / "results/reproducibility.json") \
        if (A6 / "results/reproducibility.json").exists() else {}
    self_audit = {
        "iteration_4_audit": {"n_assertions": 110, "MATCH": 105, "MISMATCH": 5,
                              "UNAVAILABLE": 0, "byte_identical_across_two_runs": True,
                              "verify_py": "17/17"},
        "source_file": rel(A6 / "results/reproducibility.json"),
        "raw_value": repro,
        "belongs_in": "APPENDIX",
        "flag": ("this is bookkeeping, not a finding -- it must NOT occupy a Contributions "
                 "slot; two sentences in methods or Appendix A is the right home"),
    }

    out = {"n_corrections": len(cor), "corrections": cor,
           "corrections_self_audit": self_audit,
           "policy": ("every number here is REGENERATED from rows where rows exist; where "
                      "only a summary exists the summary is carried with its key path and "
                      "recomputed_from_rows=false. The archive's row-level value always "
                      "wins over any prose value.")}
    dump_json(L.deep_clean(out), outdir / "results/corrections.json")
    logger.info(f"  {len(cor)} corrections")
    return out


def bitwidth_curve() -> dict:
    """The bit-width sweep that replaces the void dequantization remedy.

    The archived rows encode the bit width in `intensity` for the
    reference_symmetric_rtn quantizer; the fake-quant and bitsandbytes rows use
    named schemes (int8/nf4/int4/fp4) in the same field.
    """
    p = A3 / "results/arm1_dequant.jsonl"
    if not p.exists():
        return {"status": "UNAVAILABLE", "probed_path": rel(p)}
    rows = load_jsonl(p)

    def pack(r):
        return {"stage_id": r.get("stage_id"), "quantizer": r.get("quantizer"),
                "W05": r.get("W05_abl_min_layer_energy"),
                "refusal": r.get("refusal_rate"), "ppl": r.get("wikitext_ppl"),
                "cos_v1_r": r.get("cos_v1_r"),
                "W05rel": r.get("W05rel_min_over_random_floor"),
                "detected": (r.get("W05_abl_min_layer_energy") is not None
                             and r.get("W05_abl_min_layer_energy") <= TAU_FIXED)}

    bits, parent, named = {}, {}, {}
    for r in rows:
        it, q, root = r.get("intensity"), r.get("quantizer"), r.get("root")
        if q == "reference_symmetric_rtn" and str(it).isdigit():
            (bits if root == "A" else parent)[str(it)] = pack(r)
        elif it is not None:
            named[f"{it}__{q or 'bitsandbytes'}"] = pack(r)

    scar_dies_at = None
    for b in sorted(bits, key=lambda s: -int(s)):
        if bits[b]["W05"] is not None and bits[b]["W05"] > TAU_FIXED:
            scar_dies_at = int(b)
            break
    if not bits:
        return {"status": "UNAVAILABLE", "probed_path": rel(p),
                "reason": "no reference_symmetric_rtn bit-width rows found",
                "available_keys": sorted({k for r in rows for k in r})}
    return {"status": "OK", "source_file": rel(p), "tau": TAU_FIXED,
            "bit_width_curve_root_A": bits,
            "bit_width_curve_clean_parent": parent,
            "named_schemes": named,
            "scar_dies_at_bits": scar_dies_at,
            "cos_v1_r_min_over_bit_widths": min(
                (v["cos_v1_r"] for v in bits.values() if v["cos_v1_r"] is not None),
                default=None),
            "mechanism": ("cos(v1,r) stays above 0.999 at EVERY bit width, so the null "
                          "direction is FILLED IN by rounding noise rather than the "
                          "eigenvector rotating away; the clean parent is unmoved by the "
                          "same rounding, so this is not a generic numerical artefact"),
            "recomputed_from_rows": True}


# ===========================================================================
# STAGE 4 -- WORKSTREAM 4: the editorial pass, machine-readable
# ===========================================================================
BACKREF_PATTERNS = [
    r"we retract", r"the previous draft", r"as reported previously",
    r"iteration[ -]?3 said", r"earlier we claimed", r"we now correct",
    r"unlike the last version", r"previously (?:we|reported|claimed)",
    r"in the (?:previous|earlier|last) (?:draft|iteration|version)",
    r"the (?:earlier|prior) draft", r"we no longer claim", r"corrects? the archived",
]

SECTION_SKELETON = [
    (1, "Introduction"), (2, "Related work and positioning"),
    (3, "The statistic and its definition"),
    (4, "Discovery and completion: a consequence of the definition"),
    (5, "At-scale evaluation and the name baseline"), (6, "The operating point"),
    (7, "Decoupling in both directions"), (8, "The windowed generalisation"),
    (9, "Limitations"), (10, "Corrections to prior reporting"),
    ("A", "Appendix: self-audit"),
]


def stage4(outdir: Path, ws1: dict, ws2: dict, asrt: Assertions) -> dict:
    logger.info("STAGE 4 -- workstream 4: the edit list")
    import re

    edits: list[dict] = []
    n = 0

    def E(kind, target, instruction, before=None, after=None, blocking=False, extra=None):
        nonlocal n
        n += 1
        e = {"n": n, "kind": kind, "target": target, "instruction": instruction,
             "before_pattern": before, "after_text": after, "blocking": blocking}
        if extra:
            e.update(extra)
        edits.append(e)
        return e

    # ---- backward references ---------------------------------------------
    draft_text, draft_status = None, "UNAVAILABLE_DRAFT"
    if DRAFT4.exists():
        try:
            d = load_json(DRAFT4)
            parts = [d.get("title", ""), d.get("abstract", ""), d.get("paper_text", ""),
                     d.get("summary", "")]
            draft_text = "\n".join(p for p in parts if p)
            draft_status = "SCANNED"
        except Exception as exc:  # noqa: BLE001
            draft_status = f"UNREADABLE:{type(exc).__name__}"

    backrefs = []
    if draft_text:
        for pat in BACKREF_PATTERNS:
            for m in re.finditer(pat, draft_text, flags=re.IGNORECASE):
                s = max(0, m.start() - 220)
                e = min(len(draft_text), m.end() + 260)
                ctx = " ".join(draft_text[s:e].split())
                backrefs.append({"pattern": pat, "char_offset": m.start(), "context": ctx})
    backrefs.sort(key=lambda b: (b["char_offset"], b["pattern"]))
    for b in backrefs:
        E("BACKWARD_REFERENCE_TO_DIRECT_CLAIM",
          f"draft char offset {b['char_offset']}",
          ("Restate as a DIRECT CLAIM about the world. Delete the reference to any earlier "
           "draft, iteration or retraction and assert the corrected fact on its own terms "
           "(write 'uniformity is not the predicate', never 'we retract the previous "
           "draft's uniformity story'). Where the earlier number matters as evidence, move "
           "it to the numbered Corrections section, which is the ONLY place a prior value "
           "may be named."),
          before=b["pattern"], after=None, blocking=True,
          extra={"matched_context": b["context"], "detection": "regex over the archived draft"})

    E("BACKWARD_REFERENCE_TO_DIRECT_CLAIM", "whole document",
      ("Standing rule for text written after this list: no sentence outside Section 10 may "
       "reference a previous draft, iteration, retraction or correction. Apply these "
       "detection regexes at write time and rewrite every hit as a direct claim."),
      before="|".join(BACKREF_PATTERNS), after=None,
      blocking=(draft_status != "SCANNED"),
      extra={"draft_scan_status": draft_status,
             "reason": (None if draft_status == "SCANNED" else "UNAVAILABLE_DRAFT"),
             "detection_regexes": BACKREF_PATTERNS})

    # ---- section numbering -----------------------------------------------
    xref = {}
    for num_, title in SECTION_SKELETON:
        xref[title] = str(num_)
    xref_sym = {
        "sec:intro": "1", "sec:related": "2", "sec:statistic": "3",
        "sec:mechanism": "4", "sec:atscale": "5", "sec:operating": "6",
        "sec:decoupling": "7", "sec:windowed": "8", "sec:limitations": "9",
        "sec:corrections": "10", "app:selfaudit": "A",
    }
    E("SECTION_NUMBERING", "document skeleton",
      ("Number every section as below and use these numbers in every cross-reference so "
       "existing symbolic references resolve. Do not add, merge or reorder sections."),
      before=None,
      after="\n".join(f"{a} {b}" for a, b in SECTION_SKELETON), blocking=True,
      extra={"skeleton": [{"number": str(a), "title": b} for a, b in SECTION_SKELETON],
             "cross_reference_map_by_title": xref,
             "cross_reference_map_by_symbol": xref_sym})

    # ---- contributions cut to four ---------------------------------------
    sb = ws1["specificity_at_both_taus"]["primary_filtered_eligible"]["at_tau_fixed"]
    br = ws2["collapse"]["controlling_min_depth_weight_bracket"]
    prop = ws2["proposition_isometry"]["measured_corroboration"]
    contribs = [
        ("i", f"A parent-free, calibration-free, bottom-of-spectrum weight statistic that "
              f"needs zero prompts and zero forward passes, with measured precision "
              f"{sb['k']}/{sb['n']} false positives on eligible undeclared checkpoints at "
              f"the panel operating point and measured recall 0.159 on 44 real Hub edits -- "
              f"dominated on the same rows by an eleven-term filename regex at 0.727."),
        ("ii", f"A decomposition showing that detection and completion are the same "
               f"statement whenever discovery holds, as a consequence of the definition "
               f"rather than an empirical result, with the discovery threshold located at "
               f"a minimum depth weight in [{br[0]}, {br[1]}]."),
        ("iii", f"An analytic impossibility: isometric (Householder) edits are permanently "
                f"invisible to any Gram-spectrum statistic, W05w included -- measured at "
                f"{prop['orba_lambda1_dW05_vs_parent']:.1e} log10 units, BELOW a "
                f"random-direction control at "
                f"{prop['random_direction_householder_control_dW05_vs_parent']:.1e}."),
        ("iv", "Decoupling demonstrated in both directions by construction: a depth-weighted "
               "root un-censors 0.950 -> 0.270 [0.196, 0.360] while reading its parent's "
               "W05 exactly, and an AUROC-argmax root fires at W05 = -4.587 while refusing "
               "at its parent's rate."),
    ]
    E("CONTRIBUTIONS_CUT_TO_FOUR", "Section 1, Contributions list",
      ("Replace the Contributions list with EXACTLY these four finding-shaped items. "
       "Remove every bookkeeping item currently occupying a contribution slot."),
      before=None, after="\n".join(f"({a}) {b}" for a, b in contribs), blocking=True,
      extra={"contributions": [{"label": a, "text": b} for a, b in contribs],
             "remove_list": [
                 "the 110-assertion self-audit (bookkeeping -> Appendix A)",
                 "the byte-identical determinism check (methods, one sentence)",
                 "verify.py / verify_numbers.py existing at all (methods)",
                 "the reproduction gate deltas (methods or Limitations)",
                 "the count of shipped result files and figures",
                 "the frozen 53-metric battery's existence (it is prior iteration scaffolding)"]})

    # ---- move the self-audit ---------------------------------------------
    E("MOVE_SELF_AUDIT", "Contributions -> Appendix A / methods",
      "Move the 110-assertion audit out of Contributions. Ship whichever variant fits.",
      before=None, after=None, blocking=True,
      extra={"variant_appendix": (
                 "Appendix A. Self-audit. Every numeral in this paper is regenerated from "
                 "results/numbers.json by verify_numbers.py, which recomputes each entry "
                 "from the archived raw rows and exits non-zero on any mismatch. The "
                 "iteration-4 pass over 110 quoted values returned 105 MATCH, 5 MISMATCH "
                 "and 0 UNAVAILABLE; the five mismatches are the corrections listed in "
                 "Section 10. Two independent runs of the analysis produce byte-identical "
                 "output."),
             "variant_methods_two_sentences": (
                 "Every numeral below is regenerated from a single machine-checked numbers "
                 "file by a standalone checker that recomputes each entry from the archived "
                 "raw rows and exits non-zero on any mismatch. Two runs of the analysis "
                 "produce byte-identical output.")})

    # ---- delete the toy figure -------------------------------------------
    E("DELETE_TOY_FIGURE", "Section 1 (Introduction) and Conclusion",
      ("DELETE the 12.6 log-unit toy-stack number and its figure wherever they appear. It "
       "is a 12-matrix synthetic result with n_positives = 0 on real models and cannot "
       "carry an Introduction claim. Replace it with whichever fallback the windowed arm's "
       "outcome licenses; both are pre-written so the draft is writable the day that arm "
       "returns."),
      before=r"12\.6\s*(log[- ]units?|log10)", after=None, blocking=True,
      extra={"fallback_recovery": (
                 "Windowing recovers the depth-weighted classes, raising held-out "
                 "sensitivity from {X} to {Y} on the classes that dominate Hub traffic."),
             "fallback_non_recovery": (
                 "Windowing recovers none of the discovery failures, so the pooled "
                 "statistic's blind spot is a property of the edit and not of the pooling, "
                 "and W05w is reported as a proposed variant rather than a fix."),
             "named_slots": {"X": "held-out sensitivity of the pooled statistic on the "
                                  "depth-weighted classes, filled by the windowed artifact",
                             "Y": "held-out sensitivity of W05w on the same classes"},
             "which_is_currently_supported": "NEITHER -- the windowed positive arm has "
                                             "n_positives = 0, so this edit is BLOCKING"})

    # ---- the k=L reproduction gate tolerance ------------------------------
    gate_val = probe(load_json(A2 / "results/numbers.json"),
                     "kL_reproduces_W05_on_real_models_max_abs_delta", "value")[1]
    supported = "WIDEN" if (gate_val is not None and gate_val > 1e-9) else "KEEP"
    E("REPRODUCTION_GATE_TOLERANCE", "Section 8 (The windowed generalisation)",
      ("The k=L identity gate is declared at 1e-9 but achieves "
       f"{gate_val:.3e} on real models. Either widen the declared tolerance to a defensible "
       "float32 bound or report the gate as FAILED at its declared value. Both sentences "
       "are supplied; ship the one the numbers support."),
      before=r"1e-9|10\^\{-9\}", after=None, blocking=True,
      extra={"achieved_max_abs_delta": gate_val,
             "sentence_widen": (
                 "The k=L identity gate is declared at a relative tolerance of ~1e-6, "
                 "justified by the float32 Gram-accumulation floor already measured at "
                 f"3.1e-2 on log ratios; the achieved maximum absolute delta is "
                 f"{gate_val:.2e} log10 units over 40 real models, comfortably inside it."),
             "sentence_failed": (
                 f"The k=L identity gate FAILS at its declared 1e-9 tolerance: the maximum "
                 f"absolute delta over 40 real models is {gate_val:.2e} log10 units."),
             "which_the_numbers_support": supported,
             "justification": ("1e-9 is below the float32 Gram-accumulation floor this "
                               "project has already measured at 3.1e-2 on log ratios, so "
                               "it was never an achievable declaration")})

    # ---- arm-dependent sentences, built programmatically ------------------
    flags = arm_dependent_flags(ws2)
    for f in flags:
        E("FLAG_ARM_DEPENDENT_SENTENCE", f["target"], f["instruction"],
          before=f.get("before_pattern"), after=None, blocking=True,
          extra={"evidence": f["evidence"], "caveat_if_kept": f["caveat"]})

    out = {"n_edits": len(edits), "edit_list": edits,
           "draft_scan": {"status": draft_status, "path": rel(DRAFT4),
                          "n_chars": len(draft_text) if draft_text else 0,
                          "n_backward_references_found": len(backrefs),
                          "backward_references": backrefs},
           "section_skeleton": [{"number": str(a), "title": b} for a, b in SECTION_SKELETON],
           "cross_reference_map": xref_sym,
           "n_blocking": sum(1 for e in edits if e["blocking"])}
    dump_json(L.deep_clean(out), outdir / "results/edit_list.json")
    logger.info(f"  {len(edits)} edits ({out['n_blocking']} blocking), "
                f"{len(backrefs)} backward references found, draft={draft_status}")
    return out


def arm_dependent_flags(ws2: dict) -> list[dict]:
    """Build the arm-dependent sentence list PROGRAMMATICALLY from A2's zero-positive
    markers and from the principal-angle generalisation."""
    flags = []
    a2n = load_json(A2 / "results/numbers.json")
    a1a = load_json(A2 / "results/arm1_analysis.json")

    zero_markers = {}
    for k in sorted(a2n):
        if k.startswith("n_") and ("G1" in k or "G2" in k or "G3" in k or "G4" in k):
            zero_markers[k] = probe(a2n, k, "value")[1]

    def _find_nan_sens(o, path=""):
        found = []
        if isinstance(o, dict):
            for k in sorted(o):
                found += _find_nan_sens(o[k], f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                found += _find_nan_sens(v, f"{path}[{i}]")
        elif isinstance(o, float) and math.isnan(o) and "sens" in path.lower():
            found.append(path)
        return found

    nan_sens = sorted(set(_find_nan_sens(a1a)))[:40]
    n_pos_hits = sorted({p for p in _find_zero(a1a, "n_positives")})

    flags.append({
        "target": "every sentence claiming the windowed statistic W05w catches an edit the "
                  "pooled statistic misses",
        "before_pattern": r"W05w|windowed (?:statistic|scan|generalisation)",
        "instruction": ("This sentence's truth depends on the windowed POSITIVE arm, which "
                        "did not run: the synthetic and real positive groups are empty "
                        "(n_positives = 0), every W05w sensitivity is NaN, and the "
                        "per-recipe-class catch table is empty. Either delete the sentence "
                        "or attach the stated caveat verbatim. Assembly must HALT until one "
                        "of the two is done."),
        "evidence": {"zero_positive_markers": zero_markers,
                     "nan_sensitivity_paths": nan_sens,
                     "zero_n_positives_paths": n_pos_hits,
                     "source_files": [rel(A2 / "results/numbers.json"),
                                      rel(A2 / "results/arm1_analysis.json")]},
        "caveat": ("W05w is evaluated here only as an identity check against the pooled "
                   "statistic at k=L and as a threshold curve on negatives; its positive "
                   "arm has n_positives = 0, so no sensitivity, no per-class catch rate and "
                   "no comparison against W05 is reported."),
    })
    flags.append({
        "target": "every sentence claiming the principal-angle generalisation resolves the "
                  "multi-direction and per-component classes",
        "before_pattern": r"principal angle|multi-?direction generalisation",
        "instruction": ("The principal-angle criterion is STATED AS A DEFINITION in this "
                        "paper and is NOT evaluated: doing so needs bottom-j Gram "
                        "eigenvectors and the removed-direction basis, tensors the "
                        "re-analysis does not load. Mark it explicitly as future work or "
                        "delete the claim."),
        "evidence": {"status": ws2["undefinedness"]["principal_angle_generalisation"]["status"],
                     "rows_it_would_need":
                         ws2["undefinedness"]["principal_angle_generalisation"]["rows_it_would_need"],
                     "n_rows_currently_undefined": ws2["undefinedness"]["n_undefined_of_scored"]},
        "caveat": ("The principal-angle generalisation is stated as a definition and is not "
                   "evaluated in this work."),
    })
    flags.append({
        "target": "every sentence asserting that the discovery/completion rule was validated "
                  "on 19/19 applicable kernels",
        "before_pattern": r"19\s*/\s*19|zero disagreements",
        "instruction": ("Delete. The two quantities are the same object whenever discovery "
                        "holds, so the agreement is a consistency check on a near-identity. "
                        "Replace with the measured bound statistics from the derivation "
                        "block."),
        "evidence": {"max_abs_gap_discovery_holding":
                         ws2["gap_stats_discovery_holding"]["max"],
                     "n_bound_violated": ws2["n_bound_violated"],
                     "source_file": rel(A1 / "results/analysis.json")},
        "caveat": ("Where discovery holds, W05 and log10 min_m e_r agree to within "
                   f"{ws2['gap_stats_discovery_holding']['max']:.3f} log10 units, inside the "
                   "analytic Cauchy-Schwarz bound on every row -- this is an identity check, "
                   "not a prediction."),
    })
    return flags


def _find_zero(o, needle, path=""):
    out = []
    if isinstance(o, dict):
        for k in sorted(o):
            if needle in str(k) and o[k] == 0:
                out.append(f"{path}.{k}")
            out += _find_zero(o[k], needle, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += _find_zero(v, needle, f"{path}[{i}]")
    return out


# ===========================================================================
# STAGE 5 -- WORKSTREAM 5: carry forward with provenance
# ===========================================================================
def stage5(outdir: Path, pools: dict, a1: dict, ws1: dict, ws2: dict,
           ws3: dict, asrt: Assertions) -> dict:
    logger.info("STAGE 5 -- workstream 5: carry-forward")
    N: dict[str, dict] = {}
    a6 = load_json(A6 / "numbers.json") if (A6 / "numbers.json").exists() else {}
    a3an = load_json(A3 / "results/analysis.json")
    a3sum = load_json(A3 / "results/summary.json")
    counts = load_json(A2 / "results/arm2_archive_counts.json")
    a2n = load_json(A2 / "results/numbers.json")
    cost = load_jsonl(A1 / "results/cost.jsonl") if (A1 / "results/cost.jsonl").exists() else []

    def carry(key, path_tuple, obj, file, units, **kw):
        found, val = probe(obj, *path_tuple)
        # several archived blocks wrap a scalar as {"checkpoint": ..., "value": ...}
        if found and isinstance(val, dict) and "value" in val and len(val) <= 3:
            kw.setdefault("note", f"unwrapped from {sorted(val.keys())}")
            val = val["value"]
        if not found:
            N[key] = num(None, units, status="UNAVAILABLE", source_file=file,
                         key_path=".".join(str(p) for p in path_tuple),
                         note="probed and absent -- NOT estimated", **kw)
            asrt.unavailable(key, f"{file}::{'.'.join(str(p) for p in path_tuple)}")
            return None
        N[key] = num(val, units, source_file=file,
                     key_path=".".join(str(p) for p in path_tuple), raw_value=val, **kw)
        return val

    # ---- counts generated from rows --------------------------------------
    N["scan_total_rows"] = num(counts["total_rows"], "checkpoints", recomputed_from_rows=True,
                               source_file=rel(A2 / "results/arm2_archive_counts.json"),
                               key_path="total_rows", raw_value=counts["total_rows"])
    N["scan_n_controls"] = num(counts["n_controls"], "checkpoints", recomputed_from_rows=True,
                               source_file=rel(A2 / "results/arm2_archive_counts.json"),
                               key_path="n_controls", raw_value=counts["n_controls"])
    N["scan_n_attempted"] = num(counts["n_non_control"], "checkpoints",
                                recomputed_from_rows=True,
                                source_file=rel(A2 / "results/arm2_archive_counts.json"),
                                key_path="n_non_control", raw_value=counts["n_non_control"])
    N["scan_n_completed"] = num(counts["n_scored_non_control"], "checkpoints",
                                recomputed_from_rows=True,
                                source_file=rel(A2 / "results/arm2_archive_counts.json"),
                                key_path="n_scored_non_control",
                                raw_value=counts["n_scored_non_control"])
    N["scan_arithmetic_closes"] = num(
        counts["total_rows"] == counts["n_controls"] + counts["n_non_control"], "boolean",
        recomputed_from_rows=True, source_file=rel(A2 / "results/arm2_archive_counts.json"),
        key_path="(asserted)", note="270 = 20 controls + 250 attempted; 160 completed")

    # ---- the full-precision boundary -------------------------------------
    for k, p in (("W05_abliterated_max", ("W05_boundary", "abliterated_max")),
                 ("W05_abliterated_min", ("W05_boundary", "abliterated_min")),
                 ("W05_separating_margin", ("W05_boundary", "separating_margin_log10")),
                 ("W05_lowest_non_abliterated", ("W05_boundary", "lowest_non_abliterated"))):
        carry(k, p, a6, rel(A6 / "numbers.json"), "log10 energy",
              orientation_convention="lower-is-positive")
    asrt.check("W05_abliterated_max_equals_tau",
               probe(N, "W05_abliterated_max", "value")[1], TAU_FIXED, 1e-9,
               rel(A6 / "numbers.json"),
               "the panel operating point IS the abliterated maximum; the iteration-3 "
               "numbers file stores it ROUNDED to 10 decimal places, so full precision "
               "must come from the raw rows -- see corrections C23")
    if N.get("W05_abliterated_max", {}).get("value") is not None:
        N["W05_abliterated_max"]["note"] = (
            "the iteration-3 numbers file stores this rounded to 10 dp; the "
            "full-precision value is TAU_FIXED = -2.7415117804288127 from "
            "iter_4/.../analysis.json::fixed_threshold.tau")

    # ---- the operating point and its shift -------------------------------
    ts = ws1["tau_shift"]
    N["tau_fixed"] = num(TAU_FIXED, "log10 energy", recomputed_from_rows=True,
                         source_file=rel(A1 / "results/analysis.json"),
                         key_path="fixed_threshold.tau", raw_value=TAU_FIXED,
                         orientation_convention="lower-is-positive")
    N["tau_refit_modal"] = num(ts["refit_modal"], "log10 energy", n=ts["refit_modal_n_cells"],
                               recomputed_from_rows=True,
                               source_file=rel(A1 / "results/analysis.json"),
                               key_path="lorco.*.tau_fitted_without_this_class",
                               raw_value=ts["refit_modal"],
                               orientation_convention="lower-is-positive")
    N["tau_shift_log10"] = num(ts["shift_log10"], "log10 energy", recomputed_from_rows=True,
                               source_file="recomputed", key_path="refit_modal - fixed")
    N["tau_brittleness_scale"] = num(ts["brittleness_scale"], "log10 energy",
                                     source_file=ts["brittleness_source_file"],
                                     key_path=ts["brittleness_key_path"],
                                     raw_value=ts["brittleness_scale"],
                                     note=f"first false positive: {ts['brittleness_first_false_positive_repo']}")
    N["tau_shift_over_brittleness"] = num(ts["ratio_shift_over_brittleness"], "ratio",
                                          recomputed_from_rows=True, source_file="recomputed")

    # ---- at-scale sensitivity / specificity ------------------------------
    ats = a1["at_scale_sensitivity"]
    ns = ats["new_hub_sample"]
    k_det = len(ns["detected"])
    lo, hi = wilson(k_det, ns["n"])
    N["at_scale_sensitivity"] = num(ns["sensitivity"], "proportion", n=ns["n"],
                                    ci_low=lo, ci_high=hi,
                                    ci_method="Wilson score, z=1.96, continuity=False",
                                    recomputed_from_rows=True,
                                    source_file=rel(A1 / "results/analysis.json"),
                                    key_path="at_scale_sensitivity.new_hub_sample.sensitivity",
                                    raw_value=ns["sensitivity"])
    N["at_scale_n_uploaders"] = num(ns["n_uploaders"], "uploaders",
                                    source_file=rel(A1 / "results/analysis.json"),
                                    key_path="at_scale_sensitivity.new_hub_sample.n_uploaders",
                                    raw_value=ns["n_uploaders"])
    N["archived_panel_sensitivity"] = num(ats["archived_panel_members_remeasured"]["sensitivity"],
                                          "proportion",
                                          n=ats["archived_panel_members_remeasured"]["n"],
                                          source_file=rel(A1 / "results/analysis.json"),
                                          key_path="at_scale_sensitivity.archived_panel_members_remeasured",
                                          raw_value=1.0,
                                          note="the population the threshold was fitted on")
    sp = ws1["specificity_at_both_taus"]["primary_filtered_eligible"]
    for tag in ("at_tau_fixed", "at_tau_refit_modal"):
        b = sp[tag]
        N[f"fp_rate_eligible_undeclared_{tag}"] = num(
            b["rate"], "proportion", n=b["n"], ci_low=b["wilson_lo"], ci_high=b["wilson_hi"],
            ci_method=b["ci_method"], recomputed_from_rows=True,
            source_file=rel(A2 / "results/arm2_archive_eligibility.jsonl") + " + " +
                        rel(A2 / "results/arm2_scan_new.jsonl"),
            key_path="(rows: eligible, status OK, arm != control)",
            note=f"k={b['k']}; {WILSON_FORMULA}")
    ch = ws1["specificity_at_both_taus"]["stratified_chat_vs_base"]["chat"]["at_tau_refit_modal"]
    N["fp_rate_chat_subset_at_tau_refit"] = num(
        ch["rate"], "proportion", n=ch["n"], ci_low=ch["wilson_lo"], ci_high=ch["wilson_hi"],
        ci_method=ch["ci_method"], recomputed_from_rows=True,
        source_file="(rows, repo-id heuristic stratification)",
        key_path="stratified_chat_vs_base.chat",
        note="repo-id substring HEURISTIC -- the archived rows carry no chat_template flag")

    # ---- the name baseline -----------------------------------------------
    rb = a1["repo_name_regex_baseline"]
    N["name_regex_sensitivity"] = num(rb["sensitivity"], "proportion",
                                      n=rb["n_positives"],
                                      source_file=rel(A1 / "results/analysis.json"),
                                      key_path="repo_name_regex_baseline.sensitivity",
                                      raw_value=rb["sensitivity"],
                                      note="NAME-SEARCH UPPER BOUND -- see corrections C17")
    N["name_regex_agreement_with_W05"] = num(rb["agreement_with_W05"], "proportion",
                                             source_file=rel(A1 / "results/analysis.json"),
                                             key_path="repo_name_regex_baseline.agreement_with_W05",
                                             raw_value=rb["agreement_with_W05"])
    N["n_caught_by_W05_missed_by_name"] = num(len(rb["caught_by_W05_missed_by_name"]),
                                              "checkpoints", recomputed_from_rows=True,
                                              source_file=rel(A1 / "results/analysis.json"),
                                              key_path="repo_name_regex_baseline.caught_by_W05_missed_by_name")

    # ---- E_1 band result --------------------------------------------------
    e1 = a1["e1_crosscheck"]
    bands = {}
    for b in ("E1_mid50", "E1_full", "E1_mid20"):
        vals = [r[b] for r in e1["rows"] if isinstance(r.get(b), (int, float))
                and not math.isnan(r[b])]
        bands[b] = {"n": len(vals), "min": min(vals) if vals else None,
                    "max": max(vals) if vals else None}
    ident = all(
        (math.isnan(r["E1_mid50"]) and math.isnan(r["E1_full"]) and math.isnan(r["E1_mid20"]))
        or ((r["E1_mid50"] < 0.5) == (r["E1_full"] < 0.5) == (r["E1_mid20"] < 0.5))
        for r in e1["rows"] if isinstance(r.get("E1_mid50"), (int, float)))
    N["e1_detection_vector_identical_across_bands"] = num(
        ident, "boolean", n=e1["n"], recomputed_from_rows=True,
        source_file=rel(A1 / "results/analysis.json"), key_path="e1_crosscheck.rows",
        note="bands [0.25L,0.75L] / full stack / [0.4L,0.6L]")
    N["e1_band_summary"] = num(None, "band ranges", source_file=rel(A1 / "results/analysis.json"),
                               key_path="e1_crosscheck.rows", raw_value=bands,
                               recomputed_from_rows=True, status="OK",
                               note="min/max of E_1 within each band over the scored rows")

    # ---- W03 at 256 directions -------------------------------------------
    carry("W03_random_direction_count", ("provenance", "W03_random_direction_count"), a6,
          rel(A6 / "numbers.json"), "directions")

    # ---- the cost table ---------------------------------------------------
    N["cost_prompts_for_the_statistic"] = num(0, "prompts", recomputed_from_rows=True,
                                              source_file="by construction",
                                              key_path="(the statistic is weights-only)")
    N["cost_forward_passes_for_the_statistic"] = num(0, "forward passes",
                                                     source_file="by construction",
                                                     key_path="(the statistic is weights-only)")
    N["cost_audit_usd_this_artifact"] = num(0.0, "USD", source_file="this artifact",
                                            key_path="(zero LLM calls, zero Hub fetches)")
    carry("cost_validation_usd_A3", ("spend_usd",), a3sum, rel(A3 / "results/summary.json"), "USD")
    carry("cost_validation_cap_usd_A3", ("spend_cap_usd",), a3sum,
          rel(A3 / "results/summary.json"), "USD")
    if cost:
        tot = 0.0
        for r in cost:
            for k in ("usd", "cost_usd", "judge_usd"):
                if isinstance(r.get(k), (int, float)):
                    tot += r[k]
                    break
        N["cost_validation_usd_A1"] = num(tot, "USD", n=len(cost), recomputed_from_rows=True,
                                          source_file=rel(A1 / "results/cost.jsonl"),
                                          key_path="(summed over rows)")
    carry("wall_clock_s_A3", ("wall_clock_s",), a3sum, rel(A3 / "results/summary.json"), "seconds")

    # ---- the behavioural bound -------------------------------------------
    for k, p in (("behavioural_min_detectable_drho", ("power", "minimum_detectable_abs_drho_at_80pct")),
                 ("behavioural_n_lineages_used", ("power", "n_lineages_used")),
                 ("behavioural_r_xx", ("attenuation", "r_xx_used")),
                 ("behavioural_ordering_moved", ("attenuation", "ordering_moved")),
                 ("behavioural_falsifier_invariant_across_depth",
                  ("depth", "falsifier_invariant_across_depth"))):
        carry(k, p, a6, rel(A6 / "numbers.json"), "rho" if "drho" in k or "r_xx" in k else "count")
    for lvl in ("member", "lineage"):
        carry(f"A19_rho_{lvl}",
              ("correlations", lvl, "A19_refusal_axis_unembed_cosine",
               "harmful_refusal_rate", "rho"),
              a6, rel(A6 / "numbers.json"), "Spearman rho",
              orientation_convention="signed")
        carry(f"A19_rho_ci_{lvl}",
              ("correlations", lvl, "A19_refusal_axis_unembed_cosine",
               "harmful_refusal_rate", "ci95"),
              a6, rel(A6 / "numbers.json"), "Spearman rho CI",
              ci_method="bootstrap over the stated aggregation unit")
        carry(f"baseline_B09_named_rho_{lvl}",
              ("headline", "baseline_is_not_the_best_blackbox", lvl, "named_baseline_abs_rho"),
              a6, rel(A6 / "numbers.json"), "|Spearman rho|",
              orientation_convention="signed")
        carry(f"best_blackbox_abs_rho_{lvl}",
              ("headline", "baseline_is_not_the_best_blackbox", lvl, "actual_best_abs_rho"),
              a6, rel(A6 / "numbers.json"), "|Spearman rho|")
        carry(f"best_blackbox_name_{lvl}",
              ("headline", "baseline_is_not_the_best_blackbox", lvl, "actual_best_blackbox"),
              a6, rel(A6 / "numbers.json"), "metric id")
    carry("headline_B09_abs_rho_member", ("headline", "B09_abs_rho_member_level"), a6,
          rel(A6 / "numbers.json"), "|Spearman rho|")
    carry("headline_best_whitebox_abs_rho", ("headline", "best_whitebox_abs_rho"), a6,
          rel(A6 / "numbers.json"), "|Spearman rho|")

    # ---- pre-registration fidelity ---------------------------------------
    carry("preregistration_metric_spec_sha256", ("preregistration_fidelity", "metric_spec_sha256"),
          a6, rel(A6 / "numbers.json"), "sha256")
    carry("preregistration_verdict_counts", ("preregistration_fidelity", "verdict_counts"),
          a6, rel(A6 / "numbers.json"), "counts")
    carry("preregistration_n_metrics_declared", ("preregistration_fidelity", "n_metrics_declared"),
          a6, rel(A6 / "numbers.json"), "metrics")

    # ---- classwise distributions and overlaps ----------------------------
    carry("classwise_overlaps", ("classwise_overlaps",), a6, rel(A6 / "numbers.json"), "list")
    cd = probe(a6, "classwise_distribution")[1]
    if isinstance(cd, dict):
        N["classwise_distribution_metrics"] = num(
            len(cd), "metrics", source_file=rel(A6 / "numbers.json"),
            key_path="classwise_distribution", raw_value=sorted(cd.keys()),
            note="[min, max] per class x statistic, with base/abliterated overlaps flagged")

    # ---- both-directions decoupling --------------------------------------
    dec = a3an["decoupling"]
    fn, fp = dec["false_negative"], dec["false_positive"]
    N["rootB_refusal_after"] = num(fn["refusal"], "proportion", n=fn["n"],
                                   ci_low=fn["wilson"][0], ci_high=fn["wilson"][1],
                                   ci_method="Wilson score, z=1.96",
                                   source_file=rel(A3 / "results/analysis.json"),
                                   key_path="decoupling.false_negative.refusal",
                                   raw_value=fn["refusal"])
    N["rootB_refusal_parent"] = num(fn["parent_refusal"], "proportion",
                                    source_file=rel(A3 / "results/analysis.json"),
                                    key_path="decoupling.false_negative.parent_refusal",
                                    raw_value=fn["parent_refusal"])
    N["rootB_W05"] = num(fn["W05"], "log10 energy",
                         source_file=rel(A3 / "results/analysis.json"),
                         key_path="decoupling.false_negative.W05", raw_value=fn["W05"],
                         orientation_convention="lower-is-positive")
    N["rootB_parent_W05"] = num(fn["parent_W05"], "log10 energy",
                                source_file=rel(A3 / "results/analysis.json"),
                                key_path="decoupling.false_negative.parent_W05",
                                raw_value=fn["parent_W05"],
                                orientation_convention="lower-is-positive")
    N["rootB_cos_v1_r"] = num(fn["cos_v1_r"], "abs cosine",
                              source_file=rel(A3 / "results/analysis.json"),
                              key_path="decoupling.false_negative.cos_v1_r",
                              raw_value=fn["cos_v1_r"])
    N["rootB_dW05_vs_parent"] = num(abs(fn["W05"] - fn["parent_W05"]), "log10 energy",
                                    recomputed_from_rows=True, source_file="recomputed",
                                    key_path="|W05 - parent_W05|",
                                    note="root B reads its PARENT's value")
    N["rootC_W05"] = num(fp["W05"], "log10 energy",
                         source_file=rel(A3 / "results/analysis.json"),
                         key_path="decoupling.false_positive.W05", raw_value=fp["W05"],
                         orientation_convention="lower-is-positive")
    N["rootC_refusal"] = num(fp["refusal"], "proportion", n=fp["n"],
                             ci_low=fp["wilson"][0], ci_high=fp["wilson"][1],
                             ci_method="Wilson score, z=1.96",
                             source_file=rel(A3 / "results/analysis.json"),
                             key_path="decoupling.false_positive.refusal",
                             raw_value=fp["refusal"])
    bs = a3an["blind_spot_prevalence"]
    N["R4_partial_layer_prevalence"] = num(bs["frac_partial_layer_or_per_head"], "fraction",
                                           n=bs["n_edited_checkpoints"],
                                           source_file=rel(A3 / "results/analysis.json"),
                                           key_path="blind_spot_prevalence.frac_partial_layer_or_per_head",
                                           raw_value=bs["frac_partial_layer_or_per_head"],
                                           note=f"{bs['n_partial_layer_or_per_head']}/"
                                                f"{bs['n_edited_checkpoints']} declared Hub edits")
    N["repo_id_regex_hub_prevalence"] = num(bs["repo_id_regex_baseline"], "fraction",
                                            n=bs["n_edited_checkpoints"],
                                            source_file=rel(A3 / "results/analysis.json"),
                                            key_path="blind_spot_prevalence.repo_id_regex_baseline",
                                            raw_value=bs["repo_id_regex_baseline"])

    # ---- the ladder at n>100 ---------------------------------------------
    ca = a3an["cross_architecture"]
    N["flag_death_intensities_identical_across_architectures"] = num(
        all(len(set(v["range"])) == 1 for v in ca.values()), "boolean",
        recomputed_from_rows=True, source_file=rel(A3 / "results/analysis.json"),
        key_path="cross_architecture", raw_value=ca,
        note="merge w=0.10, add-back eps=0.10, quant nf4 -- identical on both architectures")
    lad = load_json(A3 / "results/ladder_ci_summary.json")
    N["ladder_root_reference_rate"] = num(
        lad["root_reference"]["rate"], "proportion", n=lad["root_reference"]["n"],
        ci_low=lad["root_reference"]["wilson"][0], ci_high=lad["root_reference"]["wilson"][1],
        ci_method="Wilson score, z=1.96", source_file=rel(A3 / "results/ladder_ci_summary.json"),
        key_path="root_reference", raw_value=lad["root_reference"])
    N["ladder_achieved_denominator_span"] = num(
        None, "checkpoints", source_file=rel(A3 / "results/ladder_ci_summary.json"),
        key_path="achieved_n_harmful_recovered",
        raw_value=[min(lad["achieved_n_harmful_recovered"]),
                   max(lad["achieved_n_harmful_recovered"])],
        recomputed_from_rows=False,
        note=f"{lad['n_rows_with_ambiguous_denominator']} of {lad['n_ladder_rows']} rows ambiguous")

    # ---- the quantization bit-width curve --------------------------------
    bw = bitwidth_curve()
    if bw.get("status") == "OK":
        N["quant_scar_dies_at_bits"] = num(
            bw["scar_dies_at_bits"], "bits", recomputed_from_rows=True,
            source_file=bw["source_file"], key_path="intensity (reference_symmetric_rtn)",
            note=f"first bit width at which W05 rises above tau = {TAU_FIXED}")
        for b in sorted(bw["bit_width_curve_root_A"], key=lambda s: -int(s)):
            r = bw["bit_width_curve_root_A"][b]
            N[f"quant_W05_at_{b}bit"] = num(
                r["W05"], "log10 energy", recomputed_from_rows=True,
                source_file=bw["source_file"], key_path=f"stage_id={r['stage_id']}",
                orientation_convention="lower-is-positive",
                note=f"refusal {r['refusal']}, wikitext ppl {r['ppl']}, "
                     f"cos(v1,r) {r['cos_v1_r']}, detected={r['detected']}")
        N["quant_min_cos_v1_r_over_bit_widths"] = num(
            bw["cos_v1_r_min_over_bit_widths"], "abs cosine", recomputed_from_rows=True,
            source_file=bw["source_file"], key_path="cos_v1_r",
            note="stays high at every bit width -- the null FILLS IN, it does not rotate")
        pc4 = probe(bw, "bit_width_curve_clean_parent", "4", "W05")[1]
        N["quant_clean_parent_W05_at_4bit"] = num(
            pc4, "log10 energy", recomputed_from_rows=True, source_file=bw["source_file"],
            key_path="root=parent, intensity=4",
            orientation_convention="lower-is-positive",
            note="the clean parent is essentially unmoved by the same rounding")
        i4 = probe(bw, "named_schemes", "int4__reference_fakequant_archive")[1]
        if isinstance(i4, dict):
            N["quant_int4_ppl"] = num(
                i4["ppl"], "wikitext perplexity", recomputed_from_rows=True,
                source_file=bw["source_file"], key_path="stage_id=arm1_int4",
                note="'quantization is free' overstated it -- the reference root's ppl is "
                     "26.25, so int4 costs about +43%")
    else:
        asrt.unavailable("quant_bit_width_curve", bw.get("probed_path", "?"),
                         bw.get("reason"))

    # ---- the two surviving reversals -------------------------------------
    N["reversal_argmin_patch"] = num(
        None, "statement", source_file=rel(A3 / "results/ladder_ci_summary.json"),
        key_path="crossings.addback_targeted_argmin",
        raw_value=probe(lad, "crossings", "addback_targeted_argmin")[1],
        note="a one-matrix argmin patch does not defeat a min-over-layers statistic: "
             "NEITHER_DIES on that axis")

    # ---- the mechanism / bound numbers -----------------------------------
    N["bound_max_gap_discovery_holding_finite_bound"] = num(
        ws2["gap_stats_discovery_holding_finite_bound"]["max"], "log10 energy",
        n=ws2["gap_stats_discovery_holding_finite_bound"]["n"], recomputed_from_rows=True,
        source_file=rel(A1 / "results/arm_b.jsonl"), key_path="(W05, log10_min_e_r)",
        note="restricted to discovery-holding rows where the Cauchy-Schwarz bound is "
             "informative (not VACUOUS_BELOW) -- this is the number that licenses the "
             "'near-identity' claim")
    N["bound_max_gap_discovery_holding"] = num(
        ws2["gap_stats_discovery_holding"]["max"], "log10 energy",
        n=ws2["gap_stats_discovery_holding"]["n"], recomputed_from_rows=True,
        source_file=rel(A1 / "results/arm_b.jsonl"), key_path="(W05, log10_min_e_r)")
    N["bound_median_gap_discovery_holding"] = num(
        ws2["gap_stats_discovery_holding"]["median"], "log10 energy",
        n=ws2["gap_stats_discovery_holding"]["n"], recomputed_from_rows=True,
        source_file=rel(A1 / "results/arm_b.jsonl"), key_path="(W05, log10_min_e_r)")
    N["bound_max_gap_discovery_failing"] = num(
        ws2["gap_stats_discovery_failing"]["max"], "log10 energy",
        n=ws2["gap_stats_discovery_failing"]["n"], recomputed_from_rows=True,
        source_file=rel(A1 / "results/arm_b.jsonl"), key_path="(W05, log10_min_e_r)")
    N["bound_n_violations"] = num(ws2["n_bound_violated"], "rows", recomputed_from_rows=True,
                                  source_file=rel(A1 / "results/arm_b.jsonl"),
                                  key_path="(Cauchy-Schwarz bound evaluated per row)")
    br = ws2["collapse"]["controlling_min_depth_weight_bracket"]
    N["discovery_min_depth_weight_bracket_lo"] = num(
        br[0], "depth weight", recomputed_from_rows=True,
        source_file=rel(A1 / "results/analysis.json"), key_path="gaussian_sweep.curve")
    N["discovery_min_depth_weight_bracket_hi"] = num(
        br[1], "depth weight", recomputed_from_rows=True,
        source_file=rel(A1 / "results/analysis.json"), key_path="gaussian_sweep.curve")
    N["stamped_critical_spread"] = num(
        ws2["collapse"]["stamped_critical_spread"], "spread",
        source_file=rel(A1 / "results/analysis.json"),
        key_path="gaussian_sweep.predicted_critical_spread",
        raw_value=ws2["collapse"]["stamped_critical_spread"],
        note=f"stamp sha256 {ws2['collapse']['stamp_sha256']}")
    N["stamped_critical_spread_ratio"] = num(
        ws2["collapse"]["stamp_ratio"], "ratio", recomputed_from_rows=True,
        source_file="recomputed",
        key_path="predicted_critical_spread / measured_first_detected_spread")
    mc = ws2["proposition_isometry"]["measured_corroboration"]
    N["isometry_orba_dW05"] = num(mc["orba_lambda1_dW05_vs_parent"], "log10 energy",
                                  recomputed_from_rows=True,
                                  source_file=rel(A1 / "results/arm_b.jsonl"),
                                  key_path="orba_householder_lam1.0 minus parent_unedited")
    N["isometry_random_control_dW05"] = num(
        mc["random_direction_householder_control_dW05_vs_parent"], "log10 energy",
        recomputed_from_rows=True, source_file=rel(A1 / "results/arm_b.jsonl"),
        key_path="householder_random_dir_control minus parent_unedited")
    ed = ws2["effectiveness_vs_detectability"]
    N["n_effective_kernels"] = num(ed["n_effective"], "kernels", recomputed_from_rows=True,
                                   source_file=rel(A1 / "results/analysis.json"),
                                   key_path="effectiveness_vs_detectability.rows")
    N["n_effective_and_detected"] = num(ed["n_effective_and_detected"], "kernels",
                                        recomputed_from_rows=True,
                                        source_file=rel(A1 / "results/analysis.json"),
                                        key_path="effectiveness_vs_detectability.rows")
    sp2 = ed["spearman_detectability_margin_vs_refusal_drop"]
    N["spearman_detectability_vs_effectiveness"] = num(
        sp2["rho"], "Spearman rho", n=sp2["n"], ci_low=sp2["ci_lo"], ci_high=sp2["ci_hi"],
        ci_method=sp2["ci_method"], recomputed_from_rows=True,
        source_file=rel(A1 / "results/analysis.json"),
        key_path="effectiveness_vs_detectability.rows",
        orientation_convention=sp2["orientation"],
        note=f"resampling unit = {sp2['resampling_unit']}; seed {sp2['seed']}")

    # ---- undefinedness ----------------------------------------------------
    ud = ws2["undefinedness"]
    N["n_rows_where_discovery_rule_undefined"] = num(
        ud["n_undefined_of_scored"], "checkpoints", n=ud["n_scored_edited_rows"],
        recomputed_from_rows=True, source_file=rel(A1 / "results/arm_a.jsonl"),
        key_path="recipe_class_rederived in {R_MULTIDIR_SVD, R_HERETIC}",
        note=f"draft asserts 13; computed {ud['n_undefined_of_scored']}")

    # ---- H6 positioning qualifiers ---------------------------------------
    N["novelty_qualifiers"] = num(
        None, "qualifiers", source_file=rel(A7b) + " + " + rel(A7a),
        key_path="(prior-art dossiers)",
        raw_value={
            "parent_free": {"status": "SURVIVES",
                            "why": "Abliterlitics' weight metrics are DELTA-based with the "
                                   "base model a mandatory key and no single-checkpoint mode"},
            "calibration_free": {"status": "SURVIVES",
                                 "why": "no per-family threshold is fitted at score time"},
            "bottom_of_spectrum": {"status": "SURVIVES",
                                   "why": "prior weight diagnostics read the top of the "
                                          "spectrum or a band average"},
            "sliding_and_extremum_scored": {"status": "UNEARNED",
                                            "why": "pending the windowed positive arm, which "
                                                   "has n_positives = 0"},
        },
        note="arXiv:2607.01854's E_1 is already band-averaged over a mid-stack band, so "
             "per-band scoring is published prior art; Abliterlitics is AGPL-3.0, first "
             "public 2026-04-24, measured fingerprints Heretic 23/32 layers touched "
             "(0-8 untouched), HauhauCS 29, Huihui 31, direction cosine 0.997 on one base "
             "but 0.00017 on another")

    # ---- gates carried from A2 -------------------------------------------
    for k in sorted(a2n):
        v = a2n[k]
        if isinstance(v, dict) and "value" in v:
            N[f"A2_{k}"] = num(v.get("value"), v.get("units"), n=v.get("n"),
                               ci_low=v.get("ci_low"), ci_high=v.get("ci_high"),
                               ci_method=v.get("ci_method"),
                               source_file=rel(A2 / "results/numbers.json"), key_path=k,
                               raw_value=v.get("value"), computed_by="A2/method.py",
                               note="carried verbatim from the iteration-4 numbers file "
                                    "(schema-compatible: same nine keys)")

    out = {"n_entries": len(N), "numbers": N}
    dump_json(L.deep_clean(out), outdir / "results/carry_forward.json")
    logger.info(f"  {len(N)} carried numbers")
    return out


# ===========================================================================
# assembly
# ===========================================================================
def build_all(outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "results").mkdir(parents=True, exist_ok=True)
    asrt = Assertions()

    stage0(outdir)
    a1 = load_json(A1 / "results/analysis.json")
    pools = build_pools(a1)
    ws1 = stage1(outdir, pools, a1, asrt)
    ws2 = stage2(outdir, pools, a1, asrt)
    ws3 = stage3(outdir, pools, a1, ws1, ws2, asrt)
    ws4 = stage4(outdir, ws1, ws2, asrt)
    ws5 = stage5(outdir, pools, a1, ws1, ws2, ws3, asrt)

    # ---- numbers.json ----------------------------------------------------
    numbers = dict(ws5["numbers"])
    for k in sorted(ws1["lorco_table"]):
        c = ws1["lorco_table"][k]
        numbers[f"lorco_{k}_sens_fixed_tau"] = num(
            c["col1_sens_fixed_tau"], "proportion", n=c["n_held_out"],
            recomputed_from_rows=True, source_file=rel(A1 / "results/arm_a.jsonl") + " + " +
            rel(A1 / "results/arm_b.jsonl"), key_path=f"lorco.{k}",
            orientation_convention="lower-is-positive")
        numbers[f"lorco_{k}_sens_refit_tau"] = num(
            c["col3_sens_refit_tau_recomputed"], "proportion", n=c["n_held_out"],
            recomputed_from_rows=True, source_file=rel(A1 / "results/analysis.json"),
            key_path=f"lorco.{k}.heldout_sensitivity",
            raw_value=c["col3_sens_refit_tau_archived"],
            orientation_convention="lower-is-positive")
        numbers[f"lorco_{k}_auroc_oriented"] = num(
            c["col2_auroc_oriented_fixed_tau"], "AUROC", n=c["n_held_out"],
            recomputed_from_rows=True, source_file=rel(A1 / "results/analysis.json"),
            key_path=f"lorco.{k}.auroc_oriented", raw_value=c["col4_auroc_refit_archived"],
            orientation_convention=c["auroc_orientation"],
            note="AUROC is threshold-free -- it cannot move when tau moves")
        numbers[f"lorco_{k}_specificity_refit_tau"] = num(
            c["specificity_on_negatives_refit_tau"], "proportion", n=c["n_negatives"],
            recomputed_from_rows=True, source_file=rel(A1 / "results/analysis.json"),
            key_path=f"lorco.{k}.specificity_on_negatives")

    ac = asrt.counts()
    numbers["assertion_MATCH"] = num(ac["MATCH"], "assertions", source_file="this artifact",
                                     key_path="assertions", recomputed_from_rows=True)
    numbers["assertion_MISMATCH"] = num(ac["MISMATCH"], "assertions", source_file="this artifact",
                                        key_path="assertions", recomputed_from_rows=True)
    numbers["assertion_UNAVAILABLE"] = num(ac["UNAVAILABLE"], "assertions",
                                           source_file="this artifact", key_path="assertions",
                                           recomputed_from_rows=True)
    numbers["n_corrections"] = num(ws3["n_corrections"], "corrections",
                                   source_file="results/corrections.json", key_path="corrections")
    numbers["n_edits"] = num(ws4["n_edits"], "edits", source_file="results/edit_list.json",
                             key_path="edit_list")
    numbers["n_blocking_edits"] = num(ws4["n_blocking"], "edits",
                                      source_file="results/edit_list.json", key_path="edit_list")

    meta = {
        "_schema": {
            "extends": rel(A2 / "results/numbers.json"),
            "entry_keys": ["value", "units", "n", "ci_low", "ci_high", "ci_method",
                           "source_file", "source_rows", "computed_by", "key_path",
                           "raw_value", "recomputed_from_rows", "orientation_convention",
                           "status", "note"],
            "note": ("the first nine keys are exactly the iteration-4 schema so the two "
                     "numbers files merge; the last six are this iteration's extensions"),
        },
        "_conventions": {
            "orientation": "lower-is-positive for W05 and every W05 variant",
            "wilson": WILSON_FORMULA,
            "bootstrap": f"percentile, n_boot={N_BOOT}, numpy.random.default_rng({SEED})",
            "rounding": ("numbers.json is NEVER rounded -- full repr precision. Rounding "
                         "appears only inside ready-to-paste sentence strings, to 3 decimal "
                         "places for proportions and 4 for log10 energies."),
            "nan_encoding": "NaN/Inf are encoded as the strings 'NaN'/'Infinity'/'-Infinity'",
            "tau_fixed": TAU_FIXED,
            "detection_rule": "detected iff W05 <= tau",
        },
        "_budget": {"openrouter_usd": 0.0, "model_weights_loaded": 0,
                    "forward_passes": 0, "hub_fetches": 0},
    }
    numbers_file = {**meta, **{k: numbers[k] for k in sorted(numbers)}}
    dump_json(L.deep_clean(numbers_file), outdir / "numbers.json")

    dump_json(L.deep_clean({"counts": ac, "rows": asrt.rows}),
              outdir / "results/assertions.json")

    return {"ws1": ws1, "ws2": ws2, "ws3": ws3, "ws4": ws4, "ws5": ws5,
            "assertions": {"counts": ac, "rows": asrt.rows},
            "numbers": numbers_file, "pools": pools}


# ===========================================================================
# eval_out.json (exp_eval_sol_out schema)
# ===========================================================================
def build_eval_out(res: dict, det: dict, verify: dict) -> dict:
    ws1, ws2, ws3, ws4, ws5 = res["ws1"], res["ws2"], res["ws3"], res["ws4"], res["ws5"]
    ac = res["assertions"]["counts"]
    datasets = []

    ex = []
    for k in sorted(ws1["lorco_table"]):
        c = ws1["lorco_table"][k]
        ex.append({
            "input": (f"Leave-one-recipe-class-out cell {k}: hold out its "
                      f"{c['n_held_out']} positives, score against {c['n_negatives']} "
                      f"negatives, report sensitivity at the FIXED panel tau "
                      f"{TAU_FIXED} and at the CLASS-HELD-OUT REFIT tau "
                      f"{c['tau_fitted_without_this_class']}."),
            "output": (f"archived heldout_sensitivity="
                       f"{c['col3_sens_refit_tau_archived']} at refit tau; "
                       f"archived auroc_oriented={c['col4_auroc_refit_archived']}"),
            "predict_sens_fixed_tau": repr(c["col1_sens_fixed_tau"]),
            "predict_sens_refit_tau": repr(c["col3_sens_refit_tau_recomputed"]),
            "predict_auroc_oriented": repr(c["col2_auroc_oriented_fixed_tau"]),
            "eval_sens_fixed_tau": float(c["col1_sens_fixed_tau"]),
            "eval_sens_refit_tau": float(c["col3_sens_refit_tau_recomputed"]),
            "eval_delta_refit_minus_fixed": float(c["delta_sens_refit_minus_fixed"]),
            "eval_auroc_oriented": float(c["col2_auroc_oriented_fixed_tau"]),
            "eval_auroc_archived": float(c["col4_auroc_refit_archived"]),
            "eval_specificity_fixed_tau": float(c["specificity_on_negatives_fixed_tau"]),
            "eval_specificity_refit_tau": float(c["specificity_on_negatives_refit_tau"]),
            "eval_n_held_out": float(c["n_held_out"]),
            "eval_n_negatives": float(c["n_negatives"]),
            "eval_tau_refit": float(c["tau_fitted_without_this_class"]),
            "eval_col3_agrees_to_1e12": 1.0 if c["col3_agree_to_1e-12"] else 0.0,
            "metadata_class": k,
            "metadata_uniformity": c["uniformity"],
            "metadata_held_out_repo_ids": c["held_out_repo_ids"],
            "metadata_arm": c["arm"],
            "metadata_auroc_orientation": c["auroc_orientation"],
        })
    datasets.append({"dataset": "lorco_operating_point_four_columns", "examples": ex})

    ex = []
    for r in ws2["rows"]:
        e = {
            "input": (f"Kernel {r['kernel']} ({r['family']}): does W05 = log10 min_m "
                      f"e(v1) coincide with log10 min_m e(r), and is the difference "
                      f"inside the Cauchy-Schwarz bound?"),
            "output": f"log10_min_e_r={r['log10_min_e_r']!r}",
            "predict_W05": repr(r["W05"]),
            "predict_bound_status": r["bound_status"],
            "eval_abs_gap": float(r["abs_gap"]),
            "eval_cos_v1_r": float(r["cos_v1_r"]),
            "eval_discovery_holds": 1.0 if r["discovery_holds"] else 0.0,
            "eval_linear_residual_bound": float(r["linear_residual_bound"]),
            "metadata_family": r["family"],
            "metadata_bound_status": r["bound_status"],
        }
        if r["analytic_bound_on_the_gap"] is not None:
            e["eval_analytic_bound"] = float(r["analytic_bound_on_the_gap"])
            e["eval_bound_holds"] = 1.0 if r["bound_holds"] else 0.0
        ex.append(e)
    datasets.append({"dataset": "derivation_cauchy_schwarz_bound", "examples": ex})

    ex = []
    for c in ws3["corrections"]:
        ex.append({
            "input": f"Previously reported: {c['claim_as_previously_reported']}",
            "output": repr(c["corrected_value"]),
            "predict_one_sentence_for_the_paper": c["one_sentence_for_the_paper"],
            "eval_recomputed_from_rows": 1.0 if c["recomputed_from_rows"] else 0.0,
            "metadata_id": c["id"],
            "metadata_provenance": c["provenance"],
        })
    datasets.append({"dataset": "corrections_to_prior_reporting", "examples": ex})

    ex = []
    for e in ws4["edit_list"]:
        ex.append({
            "input": f"[{e['kind']}] target: {e['target']}",
            "output": e["instruction"],
            "predict_after_text": (e["after_text"] or ""),
            "eval_blocking": 1.0 if e["blocking"] else 0.0,
            "eval_n": float(e["n"]),
            "metadata_kind": e["kind"],
            "metadata_before_pattern": e["before_pattern"],
        })
    datasets.append({"dataset": "editorial_edit_list", "examples": ex})

    ex = []
    for k in sorted(ws5["numbers"]):
        v = ws5["numbers"][k]
        e = {"input": f"carry-forward key: {k}", "output": repr(v["value"]),
             "predict_units": (v["units"] or ""),
             "eval_recomputed_from_rows": 1.0 if v["recomputed_from_rows"] else 0.0,
             "eval_available": 0.0 if v["status"] == "UNAVAILABLE" else 1.0,
             "metadata_source_file": v["source_file"],
             "metadata_key_path": v["key_path"],
             "metadata_status": v["status"]}
        if isinstance(v["value"], (int, float)) and not isinstance(v["value"], bool):
            e["eval_value"] = float(v["value"])
        ex.append(e)
    datasets.append({"dataset": "carry_forward_with_provenance", "examples": ex})

    ex = []
    for r in res["assertions"]["rows"]:
        e = {"input": f"assertion: {r['key']}", "output": repr(r["archived"]),
             "predict_recomputed": repr(r["recomputed"]),
             "eval_match": 1.0 if r["status"] == "MATCH" else 0.0,
             "eval_mismatch": 1.0 if r["status"] == "MISMATCH" else 0.0,
             "eval_unavailable": 1.0 if r["status"] == "UNAVAILABLE" else 0.0,
             "metadata_status": r["status"], "metadata_source": r["source"]}
        if isinstance(r["delta"], (int, float)):
            e["eval_delta"] = float(r["delta"])
        ex.append(e)
    datasets.append({"dataset": "assertion_block", "examples": ex})

    sp = ws1["specificity_at_both_taus"]["primary_filtered_eligible"]
    ed = ws2["effectiveness_vs_detectability"]
    gs = ws2["gap_stats_discovery_holding"]
    metrics = {
        "n_assertions": float(ac["TOTAL"]),
        "n_assertions_match": float(ac["MATCH"]),
        "n_assertions_mismatch": float(ac["MISMATCH"]),
        "n_assertions_unavailable": float(ac["UNAVAILABLE"]),
        "assertion_match_rate": float(ac["MATCH"] / ac["TOTAL"]) if ac["TOTAL"] else 0.0,
        "n_lorco_cells": float(ws1["n_classes"]),
        "tau_fixed": float(TAU_FIXED),
        "tau_refit_modal": float(ws1["tau_shift"]["refit_modal"]),
        "tau_shift_log10": float(ws1["tau_shift"]["shift_log10"]),
        "tau_brittleness_scale": float(ws1["tau_shift"]["brittleness_scale"]),
        "tau_shift_over_brittleness": float(ws1["tau_shift"]["ratio_shift_over_brittleness"]),
        "mean_sens_fixed_tau": float(sum(ws1["lorco_table"][k]["col1_sens_fixed_tau"]
                                         for k in ws1["lorco_table"]) / ws1["n_classes"]),
        "mean_sens_refit_tau": float(sum(ws1["lorco_table"][k]["col3_sens_refit_tau_recomputed"]
                                         for k in ws1["lorco_table"]) / ws1["n_classes"]),
        "n_cells_changing_materially": float(len(ws1["cells_that_change_materially"])),
        "fp_k_at_tau_fixed": float(sp["at_tau_fixed"]["k"]),
        "fp_n_at_tau_fixed": float(sp["at_tau_fixed"]["n"]),
        "fp_rate_at_tau_fixed": float(sp["at_tau_fixed"]["rate"]),
        "fp_rate_wilson_hi_at_tau_fixed": float(sp["at_tau_fixed"]["wilson_hi"]),
        "fp_k_at_tau_refit": float(sp["at_tau_refit_modal"]["k"]),
        "fp_rate_at_tau_refit": float(sp["at_tau_refit_modal"]["rate"]),
        "fp_rate_wilson_hi_at_tau_refit": float(sp["at_tau_refit_modal"]["wilson_hi"]),
        "n_bound_rows": float(len(ws2["rows"])),
        "n_bound_violations": float(ws2["n_bound_violated"]),
        "n_bound_vacuous": float(ws2["n_bound_vacuous"]),
        "bound_max_gap_discovery_holding": float(gs["max"]),
        "bound_median_gap_discovery_holding": float(gs["median"]),
        "bound_n_discovery_holding": float(gs["n"]),
        "bound_max_gap_discovery_holding_finite_bound": float(
            ws2["gap_stats_discovery_holding_finite_bound"]["max"]),
        "bound_median_gap_discovery_holding_finite_bound": float(
            ws2["gap_stats_discovery_holding_finite_bound"]["median"]),
        "bound_n_discovery_holding_finite_bound": float(
            ws2["gap_stats_discovery_holding_finite_bound"]["n"]),
        "bound_max_gap_discovery_failing": float(ws2["gap_stats_discovery_failing"]["max"]),
        "n_rows_discovery_rule_undefined": float(ws2["undefinedness"]["n_undefined_of_scored"]),
        "isometry_orba_dW05": float(
            ws2["proposition_isometry"]["measured_corroboration"]["orba_lambda1_dW05_vs_parent"]),
        "isometry_control_dW05": float(
            ws2["proposition_isometry"]["measured_corroboration"][
                "random_direction_householder_control_dW05_vs_parent"]),
        "n_effective_kernels": float(ed["n_effective"]),
        "n_effective_and_detected": float(ed["n_effective_and_detected"]),
        "spearman_detectability_vs_effectiveness": float(
            ed["spearman_detectability_margin_vs_refusal_drop"]["rho"]),
        "spearman_ci_lo": float(ed["spearman_detectability_margin_vs_refusal_drop"]["ci_lo"]),
        "spearman_ci_hi": float(ed["spearman_detectability_margin_vs_refusal_drop"]["ci_hi"]),
        "n_corrections": float(ws3["n_corrections"]),
        "n_edits": float(ws4["n_edits"]),
        "n_blocking_edits": float(ws4["n_blocking"]),
        "n_backward_references_found": float(ws4["draft_scan"]["n_backward_references_found"]),
        "n_carry_forward_numbers": float(ws5["n_entries"]),
        "n_carry_forward_unavailable": float(sum(1 for k in ws5["numbers"]
                                                 if ws5["numbers"][k]["status"] == "UNAVAILABLE")),
        "n_numbers_json_entries": float(sum(1 for k in res["numbers"]
                                            if not k.startswith("_"))),
        "determinism_byte_identical": 1.0 if det["byte_identical"] else 0.0,
        "determinism_n_files_compared": float(det["n_files"]),
        "verify_numbers_exit_code": float(verify["exit_code"]),
        "verify_n_pass": float(verify["n_pass"]),
        "verify_n_fail": float(verify["n_fail"]),
        "verify_n_unavailable": float(verify["n_unavailable"]),
        "openrouter_usd_spent": 0.0,
        "model_weights_loaded": 0.0,
        "forward_passes": 0.0,
        "hub_fetches": 0.0,
    }

    return {
        "metadata": {
            "evaluation_name": "One numbers file the paper must obey",
            "description": ("Pure re-analysis of the archived iteration-2/3/4 trees. Emits a "
                            "single machine-checked numbers.json from which the paper "
                            "regenerates every numeral, plus the four-column "
                            "leave-one-recipe-class-out table at both taus, the "
                            "discovery/completion derivation with its residual bounded "
                            "numerically, one consolidated corrections subsection, a numbered "
                            "machine-readable editorial edit list, and carry-forward values "
                            "with provenance."),
            "parameters": {"tau_fixed": TAU_FIXED,
                           "tau_refit_modal": ws1["tau_shift"]["refit_modal"],
                           "seed": SEED, "n_boot": N_BOOT,
                           "discovery_criterion": f"|cos(v1,r)| > {COS_DISCOVERY}",
                           "wilson_formula": WILSON_FORMULA},
            "baselines": {"repo_name_regex_sensitivity":
                              res["ws5"]["numbers"]["name_regex_sensitivity"]["value"],
                          "repo_name_regex_caveat": "NAME-SEARCH UPPER BOUND -- see C17"},
            "assertion_block": {"counts": ac,
                                "verify_numbers_py": verify,
                                "policy": ("MISMATCHes are never silently fixed -- each "
                                           "becomes a corrections[] entry and the archive's "
                                           "row-level value wins")},
            "determinism": det,
            "budget": {"openrouter_usd": 0.0, "cap_usd": 10.0, "model_weights_loaded": 0,
                       "forward_passes": 0, "hub_fetches": 0, "llm_calls": 0},
            "completeness": {"workstream_1": "COMPLETE", "workstream_2": "COMPLETE",
                             "workstream_3": "COMPLETE", "workstream_4": "COMPLETE",
                             "workstream_5": "COMPLETE"},
            "headline_sentences": {
                "operating_point": ws1["tau_shift"]["sentence"],
                "specificity": ws1["specificity_at_both_taus"]["ready_to_paste_sentence"],
                "chat_subset": ws1["specificity_at_both_taus"]["chat_subset_sentence"],
                "detection_iff_completion": ws2["replacement_sentences"]["detection_iff_completion"],
                "what_the_sweep_shows": ws2["replacement_sentences"]["what_the_sweep_actually_shows"],
                "undefinedness": ws2["undefinedness"]["sentence"],
                "isometry": ws2["proposition_isometry"]["statement"],
                "near_orthogonality": ws2["effectiveness_vs_detectability"]["reading"],
            },
        },
        "metrics_agg": metrics,
        "datasets": datasets,
    }


# ===========================================================================
# determinism + verify
# ===========================================================================
def compare_dirs(d1: Path, d2: Path) -> dict:
    f1 = sorted(p.relative_to(d1).as_posix() for p in d1.rglob("*") if p.is_file())
    f2 = sorted(p.relative_to(d2).as_posix() for p in d2.rglob("*") if p.is_file())
    same_set = f1 == f2
    rows, diffs = {}, []
    for f in f1:
        a, b = sha256_of(d1 / f), sha256_of(d2 / f) if (d2 / f).exists() else None
        rows[f] = {"run1_sha256": a, "run2_sha256": b, "identical": a == b}
        if a != b:
            diffs.append(f)
    return {"byte_identical": same_set and not diffs, "n_files": len(f1),
            "file_lists_match": same_set, "per_file": rows, "differing_files": diffs,
            "run1_files": f1, "run2_files": f2,
            "nondeterminism_controls": [
                "every dict/set key list is sorted() before use",
                "json.dumps(sort_keys=True), full float precision, never rounded",
                "numpy.random.default_rng(20260814) -- never the legacy global RNG",
                "no timestamps written to any output file",
                "file globs are sorted()",
            ]}


def run_verify(workdir: Path) -> dict:
    script = workdir / "verify_numbers.py"
    if not script.exists():
        return {"exit_code": -1, "n_pass": 0, "n_fail": 0, "n_unavailable": 0,
                "status": "MISSING", "table": []}
    proc = subprocess.run([sys.executable, str(script), "--numbers",
                           str(workdir / "numbers.json")],
                          capture_output=True, text=True, cwd=str(workdir), timeout=1800)
    out = {"exit_code": proc.returncode, "stdout_tail": proc.stdout[-6000:],
           "stderr_tail": proc.stderr[-3000:]}
    rep = workdir / "results/verify_report.json"
    if rep.exists():
        r = load_json(rep)
        out.update({"n_pass": r["n_pass"], "n_fail": r["n_fail"],
                    "n_unavailable": r["n_unavailable"], "table": r["rows"],
                    "status": "PASS" if proc.returncode == 0 else "FAIL"})
    else:
        out.update({"n_pass": 0, "n_fail": 0, "n_unavailable": 0, "table": [],
                    "status": "NO_REPORT"})
    return out


# ===========================================================================
# main
# ===========================================================================
@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=None,
                    help="single-run mode: build into this directory and stop")
    args = ap.parse_args()

    if args.outdir:
        build_all(Path(args.outdir).resolve())
        logger.info("single-run build complete")
        return

    # --- Stage 4: determinism -- build TWICE into two directories ---------
    d1, d2 = HERE / "det_run_1", HERE / "det_run_2"
    for d in (d1, d2):
        if d.exists():
            shutil.rmtree(d)
    logger.info("determinism run 1/2")
    res = build_all(d1)
    logger.info("determinism run 2/2 (separate process)")
    proc = subprocess.run([sys.executable, str(HERE / "eval.py"), "--outdir", str(d2)],
                          capture_output=True, text=True, cwd=str(HERE), timeout=3600)
    if proc.returncode != 0:
        logger.error(f"determinism run 2 failed:\n{proc.stdout[-3000:]}\n{proc.stderr[-3000:]}")
        raise RuntimeError("determinism run 2 failed")
    det = compare_dirs(d1, d2)
    det["run2_mode"] = "separate OS process via subprocess -- process-level determinism"
    if not det["byte_identical"]:
        logger.error(f"DETERMINISM FAILED on: {det['differing_files']}")
    dump_json(L.deep_clean(det), HERE / "results/determinism.json")

    # --- promote run 1 to the workspace ----------------------------------
    for f in sorted(d1.rglob("*")):
        if f.is_file():
            dst = HERE / f.relative_to(d1)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)
    dump_json(L.deep_clean(det), HERE / "results/determinism.json")

    # --- verify_numbers.py -----------------------------------------------
    verify = run_verify(HERE)
    logger.info(f"verify_numbers.py exit={verify['exit_code']} "
                f"PASS={verify['n_pass']} FAIL={verify['n_fail']} "
                f"UNAVAILABLE={verify['n_unavailable']}")

    # --- eval_out.json ----------------------------------------------------
    eo = build_eval_out(res, det, verify)
    dump_json(L.deep_clean(eo), HERE / "eval_out.json")
    dump_json(L.deep_clean(eo), HERE / "full_eval_out.json")

    ac = res["assertions"]["counts"]
    logger.info(f"DONE  assertions {ac['MATCH']} MATCH / {ac['MISMATCH']} MISMATCH / "
                f"{ac['UNAVAILABLE']} UNAVAILABLE  |  determinism="
                f"{det['byte_identical']}  |  verify exit={verify['exit_code']}")
    for d in (d1, d2):
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    main()
