#!/usr/bin/env python3
"""Stages s5-s8: the frontier, generalised subspace discovery, the derivation,
and the assembled deliverables.

Everything here reads results/*.jsonl and writes results/*.json.  It performs no
downloads and no scoring, so it is cheap to re-run and is the stage that
`verify.py` independently re-derives.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from loguru import logger

import method as M
import statsx as SX

RES = M.RES
ARCHIVE = M.ARCHIVE
TAU = M.TAU_W05
KS_ALL = [str(k) for k in M.KS] + ["L"]

ALPHAS = (0.05, 0.01, 0.001)
TAU_C_GRID = (0.0, 0.5, 0.8, 0.9, 0.95)

# kernels that are NOT edits of the refusal direction and must never count as
# positives: the unedited parent and the random-direction Householder controls.
CONTROL_CLASSES = {"PARENT", "CONTROL_NOISE_FLOOR"}


# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------
def load_armb() -> list[dict]:
    return [r for r in M.read_jsonl(RES / "armb_w05w.jsonl") if r.get("status") == "OK"]


def load_arma() -> list[dict]:
    return M.read_jsonl(RES / "arma_w05w.jsonl")


def load_negatives() -> tuple[list[dict], dict]:
    """The eligible undeclared population, re-scored at W05w by iteration 4.

    arm2_scan_new.jsonl already carries W05w_by_k and the full window profile for
    every row it scored, so these 57 rows are re-used verbatim rather than
    re-downloaded.  The 122-row archived population was scored at W05 ONLY and is
    reported as such -- never silently pooled into a W05w denominator.
    """
    rows = M.read_jsonl(ARCHIVE / "arm2_scan_new.jsonl")
    ok = [r for r in rows if r.get("status") == "OK" and r.get("windowed")]
    elig = [r for r in ok if r.get("eligible")]
    unres = [r for r in rows if r.get("status") != "OK"]
    arch = M.read_jsonl(ARCHIVE / "arm2_archive_eligibility.jsonl")
    arch_elig = [r for r in arch if r.get("eligible") and r.get("W05") is not None]
    meta = {
        "n_scan_new_total": len(rows),
        "n_scan_new_ok": len(ok),
        "n_scan_new_eligible_with_W05w": len(elig),
        "n_scan_new_unresolved_excluded": len(unres),
        "n_archived_eligible_W05_only": len(arch_elig),
        "note": ("The W05w denominator is the 57 iteration-4 re-scan rows that resolved "
                 "AND passed the frozen eligibility rule (sha256 0f8be4f6...).  The "
                 "archived %d-row eligible population was scored at W05 ONLY and is "
                 "labelled 'W05-only, not re-scored at W05w'; it is used for the pooled "
                 "baseline's specificity and for nothing else."
                 % len(arch_elig)),
    }
    return elig, meta


def _phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def subset_p(row: dict) -> dict | None:
    """The layer-subset multiple-window p-value, computed PER WINDOW.

    `wwin.analyse2` emits `subset_null.p_multiwindow_empirical`, which compares
    the MIN over contiguous windows against a null of SINGLE random k-subsets.
    Those are not the same statistic: a minimum over n_w windows sits below a
    typical single subset even for an unedited model, so that quantity pins to
    the empirical floor 1/(S+1) for essentially every checkpoint and carries no
    information.  Observed directly -- it read 0.3297 for the unedited parent and
    for every kernel alike.

    The construction below is the one that is actually calibrated: score EACH
    contiguous window against the subset null, take the smallest per-window p,
    and apply the exact Sidak correction over the n_w windows.  Both an empirical
    p (floored at 1/(S+1), reported with its floor) and a parametric p from a
    normal fit to the same draws (unfloored) are returned; the parametric one is
    what the alpha sweep uses, and it is labelled as parametric everywhere.

    Defined only at the k the null was drawn at.
    """
    sn = row.get("subset_null")
    if not sn or not sn.get("null_values"):
        return None
    k = str(sn["k"])
    w = (row.get("windowed") or {}).get(k)
    if not w or not w.get("profile"):
        return None
    vals = np.asarray(sn["null_values"], dtype=float)
    S = len(vals)
    mu, sd = float(vals.mean()), float(vals.std(ddof=1))
    emp, par = [], []
    for p_ in w["profile"]:
        obs = float(p_["log10_e_min"])
        emp.append((1 + int((vals <= obs).sum())) / (S + 1))
        par.append(_phi((obs - mu) / sd) if sd > 0 else float("nan"))
    nw = len(emp)
    pe, pp = min(emp), min(x for x in par if not math.isnan(x)) if par else float("nan")
    return {
        "k": k, "S": S, "n_windows": nw,
        "null_mean": mu, "null_sd": sd,
        "p_min_window_empirical": pe, "p_min_window_parametric": pp,
        "p_sidak_empirical": 1.0 - (1.0 - pe) ** nw,
        "p_sidak_parametric": (1.0 - (1.0 - pp) ** nw) if not math.isnan(pp) else float("nan"),
        "p_empirical_floor": 1.0 / (S + 1),
        "per_window_p_empirical": emp, "per_window_p_parametric": par,
        "superseded_field": sn.get("p_multiwindow_empirical"),
    }


def neg_score(row: dict, k: str) -> float | None:
    w = (row.get("windowed") or {}).get(k)
    if w is None:
        return None
    return float(w["W05w"])


def neg_consistency(row: dict, k: str) -> float:
    w = (row.get("windowed") or {}).get(k)
    return float(w["consistency_c"]) if w else 1.0


# ---------------------------------------------------------------------------
# STAGE 5 -- the frontier
# ---------------------------------------------------------------------------
def positives_armb(armb: list[dict]) -> list[dict]:
    return [r for r in armb if r.get("recipe_class") not in CONTROL_CLASSES]


def positives_arma(arma: list[dict]) -> list[dict]:
    return [r for r in arma if r.get("status") == "OK"
            and r.get("role") in ("edited", "parent_also_edited")]


def rule_scores(row: dict, k: str, rule: str) -> float | None:
    """The scalar a rule thresholds.  Lower = more edited, for every rule."""
    w = (row.get("windowed") or {}).get(k)
    if w is None:
        return None
    if rule == "RAW":
        return float(w["W05w"])
    if rule == "POOLED_W05":
        return float(row["W05_abl_min_layer_energy"])
    if rule == "CAL_DIRECTION":
        return float(w.get("p_sidak_parametric", float("nan")))
    if rule == "CAL_SUBSET":
        sp = subset_p(row)
        if sp is None or sp["k"] != k:
            return None
        return float(sp["p_sidak_parametric"])
    if rule == "DELTA":
        return float(w["W05w"]) - float(row["W05_abl_min_layer_energy"])
    return None


def spec_matched_threshold(neg_vals: list[float], n_allowed_fp: int = 0) -> float:
    """The most permissive threshold with at most `n_allowed_fp` false positives.

    Fitted on the NEGATIVES ONLY -- it never sees a positive -- so it is not
    circular with respect to sensitivity.  It IS fitted on the same negative
    population the specificity is then quoted on, and that is flagged on every
    row it produces.
    """
    v = sorted(x for x in neg_vals if x is not None and math.isfinite(x))
    if not v:
        return float("-inf")
    if n_allowed_fp >= len(v):
        return float("inf")
    # allow the n_allowed_fp deepest negatives through, exclude the next one
    return float(np.nextafter(v[n_allowed_fp], -np.inf))


def stage_s5() -> dict:
    armb, arma = load_armb(), load_arma()
    negs, negmeta = load_negatives()
    pb, pa = positives_armb(armb), positives_arma(arma)
    controls = [r for r in armb if r.get("recipe_class") in CONTROL_CLASSES]
    parent = next((r for r in armb if r["kernel_id"] == "PARENT"), None)
    logger.info(f"S5: {len(pb)} Arm B positives, {len(pa)} Arm A positives, "
                f"{len(negs)} eligible negatives with W05w")

    frontier: list[dict] = []
    fp = RES / "frontier.jsonl"
    if fp.exists():
        fp.unlink()

    for k in KS_ALL:
        neg_raw = [neg_score(r, k) for r in negs]
        neg_raw = [x for x in neg_raw if x is not None]
        if not neg_raw:
            continue
        # ---- rule RAW, at three operating points on the negatives ----
        for n_fp in (0, 1, 2):
            tau_k = spec_matched_threshold(neg_raw, n_fp)
            for arm, pos in (("B", pb), ("A", pa)):
                frontier.append(frontier_row(
                    k=k, rule="RAW", threshold=tau_k, arm=arm, pos=pos, negs=negs, thr_kind=f"specificity-matched, <= {n_fp} FP",
                    scorer=lambda r, kk=k: rule_scores(r, kk, "RAW"),
                    circular=False))
        # ---- rule RAW at the PRE-REGISTERED pooled threshold ----
        for arm, pos in (("B", pb), ("A", pa)):
            frontier.append(frontier_row(
                k=k, rule="RAW", threshold=TAU, arm=arm, pos=pos, negs=negs, thr_kind="pre-registered archived tau (-2.7415)",
                scorer=lambda r, kk=k: rule_scores(r, kk, "RAW"), circular=False))
        # ---- rule GATED: W05wc(k, tau_c) ----
        for tc in TAU_C_GRID:
            def gated(r, kk=k, tc=tc):
                w = (r.get("windowed") or {}).get(kk)
                if w is None:
                    return None
                return float(w["W05w"]) if w["consistency_c"] >= tc else float("inf")
            gneg = [gated(r) for r in negs]
            gneg = [x for x in gneg if x is not None]
            tau_k = spec_matched_threshold(gneg, 0)
            for arm, pos in (("B", pb), ("A", pa)):
                frontier.append(frontier_row(
                    k=k, rule=f"GATED_tauc{tc}", threshold=tau_k, arm=arm, pos=pos,
                    negs=negs,
                    thr_kind="specificity-matched, 0 FP", scorer=gated, circular=False))
        # ---- the CALIBRATED rules, on the ONLY negatives they are defined on ----
        #
        # Both nulls need the weights.  The archived undeclared population was
        # scored by iteration 4, which computed neither null, so neither p-value
        # exists for those 57 rows and a rate quoted on them would be a rate over
        # an empty denominator.  The calibrated rules are therefore evaluated
        # against the IN-MEMORY unedited controls -- the parent and the
        # random-direction Householders -- and RAW is ALSO evaluated on that same
        # small set, so the calibration-cost comparison is like with like.
        for a in ALPHAS:
            frontier.append(frontier_row(
                k=k, rule="CAL_DIRECTION", threshold=a, arm="B", pos=pb, negs=controls,
                thr_kind=f"alpha = {a} on p_sidak (parametric); negatives = the "
                         f"{len(controls)} in-memory unedited controls",
                scorer=lambda r, kk=k: rule_scores(r, kk, "CAL_DIRECTION"),
                circular=False))
        tau_ctrl = spec_matched_threshold(
            [rule_scores(r, k, "RAW") for r in controls], 0)
        frontier.append(frontier_row(
            k=k, rule="RAW", threshold=tau_ctrl, arm="B", pos=pb, negs=controls,
            thr_kind=f"specificity-matched, 0 FP; negatives = the {len(controls)} "
                     f"in-memory unedited controls",
            scorer=lambda r, kk=k: rule_scores(r, kk, "RAW"), circular=False))
        # ---- rule CAL_SUBSET: the layer-subset null (only defined at its own k) --
        #
        # The archived undeclared population was scored by iteration 4, which did
        # not compute a layer-subset null, and recomputing one needs the weights.
        # So CAL_SUBSET is evaluated against the IN-MEMORY negative controls --
        # the unedited parent and the random-direction Householders, which are
        # exactly the checkpoints that carry no edit along r -- and that smaller,
        # differently-constituted denominator is named on every row it produces.
        if any(r.get("subset_null") and str(r["subset_null"]["k"]) == k for r in pb):
            for a in ALPHAS:
                frontier.append(frontier_row(
                    k=k, rule="CAL_SUBSET", threshold=a, arm="B", pos=pb, negs=controls,
                    thr_kind=f"alpha = {a} on the layer-subset multi-window p "
                             f"(Sidak, parametric); negatives = the {len(controls)} "
                             f"in-memory unedited controls, NOT the undeclared population",
                    scorer=lambda r, kk=k: rule_scores(r, kk, "CAL_SUBSET"),
                    circular=False))

    # ---- the POOLED BASELINE, on its own honest denominator ----
    for arm, pos in (("B", pb), ("A", pa)):
        neg_pooled = [float(r["W05_abl_min_layer_energy"]) for r in negs]
        for thr, kind in ((TAU, "pre-registered archived tau"),
                          (spec_matched_threshold(neg_pooled, 0),
                           "specificity-matched, 0 FP")):
            frontier.append(frontier_row(
                k="pooled", rule="POOLED_W05", threshold=thr, arm=arm, pos=pos,
                negs=negs, thr_kind=kind,
                scorer=lambda r: float(r["W05_abl_min_layer_energy"]), circular=False))

    for row in frontier:
        M.append_jsonl(fp, row)

    # ---------------- the random-direction null is uninformative ------------
    par_z = ({k: parent["windowed"][k]["z_min"] for k in KS_ALL} if parent else {})
    null_finding = {
        "statement": ("The plan's per-window RANDOM-DIRECTION null rejects the negative "
                      "control.  v1_win is the MINIMISING eigenvector of the window Gram, "
                      "not a random draw, so 'is this direction unusually low-energy?' is "
                      "trivially yes for every checkpoint, edited or not."),
        "unedited_parent_z_min_by_k": par_z,
        "consequence": ("Any rule of the form p_sidak <= alpha on that null flags "
                        "essentially everything, so its specificity collapses; the number "
                        "is reported in the frontier rather than suppressed."),
        "replacement": ("The layer-SUBSET null (subset_null) asks the question the "
                        "multiple-window hazard actually poses -- how deep does the window "
                        "statistic go for an ARBITRARY set of k layers of THIS model? -- "
                        "and gives the exact multiple-window correction "
                        "p = 1 - (1 - F(obs))^n_windows."),
    }

    sp_rows = [{"model_id": r["kernel_id"], "recipe_class": r["recipe_class"],
                "W05": r["W05_abl_min_layer_energy"], **(subset_p(r) or {})}
               for r in armb if subset_p(r) is not None]
    subset_finding = {
        "statement": ("wwin.analyse2's `subset_null.p_multiwindow_empirical` compares the "
                      "MIN over contiguous windows against a null of SINGLE random "
                      "k-subsets.  Those are different statistics -- a minimum over n_w "
                      "windows lies below a typical single subset even on an unedited "
                      "model -- so it pins to the empirical floor 1/(S+1) for every "
                      "checkpoint alike.  Measured: its MINIMUM over all scored kernels is "
                      "0.3297 -- it never reaches alpha = 0.05 even for a complete rank-one "
                      "projection -- and the large majority of kernels share that one "
                      "value, the unedited parent among them."),
        "correction": ("Each contiguous window is scored against the subset null "
                       "separately, the smallest per-window p is taken, and the exact "
                       "Sidak correction is applied over n_w windows.  Computed in "
                       "analysis.subset_p from the SAME stored draws, so no rescoring "
                       "was needed."),
        "rows": sp_rows,
    }
    # ---- WHY the corrected null still rejects the negative control ----
    # Measured, not asserted: for each model, compare the mean depth of its
    # CONTIGUOUS windows against the mean depth of RANDOM k-subsets of the same
    # size.  Adjacent layers are more alike than randomly chosen ones, so a
    # contiguous window's Gram is closer to rank-deficient and its minimum energy
    # sits lower -- on an UNEDITED model too.  That is ordinary depth continuity,
    # not an edit, and it is the confound that makes this null reject the parent.
    cont = []
    for r in armb:
        sn = r.get("subset_null")
        if not sn or not sn.get("null_values"):
            continue
        w = (r.get("windowed") or {}).get(str(sn["k"]))
        if not w or not w.get("profile"):
            continue
        obs = np.array([p_["log10_e_min"] for p_ in w["profile"]], dtype=float)
        cont.append({"model_id": r["kernel_id"],
                     "mean_contiguous": float(obs.mean()),
                     "mean_random_subset": float(sn["null_mean"]),
                     "gap": float(obs.mean() - sn["null_mean"])})
    par_c = next((c for c in cont if c["model_id"] == "PARENT"), None)
    subset_finding["contiguity_confound"] = {
        "statement": ("Contiguous windows are systematically DEEPER than random "
                      "k-subsets of the same size, on edited and unedited models alike, "
                      "because adjacent layers are more alike than randomly chosen ones.  "
                      "The layer-subset null therefore rejects the unedited parent too -- "
                      "for a different reason than the random-direction null, and one "
                      "that no amount of resampling inside a single model can remove."),
        "unedited_parent": par_c,
        "rows": cont,
        "consequence": ("The multiple-window hazard cannot be bounded by a within-model "
                        "null.  It is bounded HERE by measured specificity on 57 real "
                        "eligible undeclared checkpoints, which is what the "
                        "specificity-matched thresholds in frontier.jsonl do."),
    }

    out = {"n_frontier_rows": len(frontier), "negatives": negmeta,
           "subset_null_correction": subset_finding,
           "n_positives_armB": len(pb), "n_positives_armA": len(pa),
           "n_controls_armB": len(controls),
           "random_direction_null_finding": null_finding,
           "catch_by_recipe_class": catch_by_class(pb, pa, negs),
           "calibration_cost": calibration_cost(frontier)}
    M.write_json(RES / "arm2_frontier_summary.json", out)
    return out


def frontier_row(*, k, rule, threshold, arm, pos, negs, thr_kind, scorer,
                 circular) -> dict:
    sp = [scorer(r) for r in pos]
    sn = [scorer(r) for r in negs]
    sp = [(r, v) for r, v in zip(pos, sp) if v is not None and not math.isnan(v)]
    sn = [v for v in sn if v is not None and not math.isnan(v)]
    hit = [r for r, v in sp if v <= threshold]
    fp_n = sum(1 for v in sn if v <= threshold)
    sens, sl, sh = SX.wilson(len(hit), len(sp)) if sp else (float("nan"), 0.0, 1.0)
    spec, pl, ph = (SX.wilson(len(sn) - fp_n, len(sn)) if sn else (float("nan"), 0.0, 1.0))
    return {
        "k": k, "rule": rule, "threshold": float(threshold),
        "threshold_kind": thr_kind, "arm": arm,
        "n_pos": len(sp), "n_hit": len(hit), "sensitivity": sens,
        "sens_wilson_lo": sl, "sens_wilson_hi": sh,
        "n_neg": len(sn), "n_false_positive": fp_n, "specificity": spec,
        "spec_wilson_lo": pl, "spec_wilson_hi": ph,
        "ci_method": "Wilson score, z=1.96",
        "threshold_fitted_on_negatives_only": bool("specificity-matched" in thr_kind),
        "circularity_flag": ("threshold fitted on the SAME negative population its "
                             "specificity is quoted on; sensitivity is unaffected because "
                             "no positive is seen by the fit"
                             if "specificity-matched" in thr_kind else
                             "threshold pre-registered in iteration 4; no fitting here"),
        "hits": sorted(r.get("kernel_id") or r.get("repo_id") for r in hit)[:60],
    }


def catch_by_class(pb: list[dict], pa: list[dict], negs: list[dict]) -> dict:
    """Which recipe classes each k catches -- populated for EVERY k."""
    neg_by_k = {k: [neg_score(r, k) for r in negs] for k in KS_ALL}
    neg_by_k = {k: [x for x in v if x is not None] for k, v in neg_by_k.items()}
    out: dict = {}
    for k in KS_ALL:
        if not neg_by_k[k]:
            continue
        tau_k = spec_matched_threshold(neg_by_k[k], 0)
        per: dict = {}
        for arm, pos in (("B", pb), ("A", pa)):
            for r in pos:
                cls = r.get("recipe_class") or r.get("recipe_class_rederived") or "UNKNOWN"
                key = f"{arm}:{cls}"
                v = rule_scores(r, k, "RAW")
                p = rule_scores(r, k, "POOLED_W05")
                if v is None:
                    continue
                e = per.setdefault(key, {"n": 0, "caught_W05w": 0, "caught_W05": 0,
                                         "members": []})
                e["n"] += 1
                e["caught_W05w"] += int(v <= tau_k)
                e["caught_W05"] += int(p is not None and p <= TAU)
                e["members"].append(r.get("kernel_id") or r.get("repo_id"))
        for e in per.values():
            e["rate_W05w"] = e["caught_W05w"] / e["n"] if e["n"] else float("nan")
            e["rate_W05"] = e["caught_W05"] / e["n"] if e["n"] else float("nan")
            e["members"] = sorted(e["members"])[:20]
        out[k] = {"threshold": tau_k, "by_class": per}
    return out


def calibration_cost(frontier: list[dict]) -> dict:
    """Does calibration cost sensitivity?  Compared LIKE WITH LIKE.

    Only rows whose negatives are the in-memory unedited controls are used, so
    RAW and the two calibrated rules are all measured against the SAME
    denominator.  Comparing a RAW rate measured on 57 undeclared checkpoints
    against a calibrated rate measured on 5 controls would be a comparison of
    denominators, not of rules.
    """
    ctrl_rows = [r for r in frontier
                 if r["arm"] == "B" and r["k"] != "pooled"
                 and "in-memory unedited controls" in r["threshold_kind"]
                 and r["rule"] in ("RAW", "CAL_DIRECTION", "CAL_SUBSET")]
    best: dict = {}
    for row in ctrl_rows:
        key = (row["k"], row["rule"])
        cur = best.get(key)
        # among operating points reaching specificity 1.0, keep the most sensitive
        if row["specificity"] >= 1.0 and (cur is None
                                          or row["sensitivity"] > cur["sensitivity"]):
            best[key] = row
    lines: dict = {}
    for k in KS_ALL:
        raw = best.get((k, "RAW"))
        for rule in ("CAL_DIRECTION", "CAL_SUBSET"):
            key = f"{k}:{rule}"
            cal = best.get((k, rule))
            any_cal = [r for r in ctrl_rows if r["k"] == k and r["rule"] == rule]
            if raw is None and cal is None and not any_cal:
                continue
            lines[key] = {
                "n_neg_shared": (raw or cal or any_cal[0])["n_neg"],
                "sens_raw": (raw["sensitivity"] if raw else None),
                "sens_cal": (cal["sensitivity"] if cal else None),
                "raw_reaches_specificity_1": bool(raw is not None),
                "cal_reaches_specificity_1": bool(cal is not None),
                "best_cal_specificity": (max((r["specificity"] for r in any_cal),
                                             default=None) if any_cal else None),
                "cal_le_raw": (bool(cal["sensitivity"] <= raw["sensitivity"])
                               if (cal and raw) else None),
            }
    n_cal_fail = sum(1 for v in lines.values() if not v["cal_reaches_specificity_1"])
    return {
        "per_k": lines,
        "negatives": "the in-memory unedited controls (parent + random-direction "
                     "Householders); the archived undeclared population carries neither "
                     "null, so no calibrated rate is defined on it",
        "sentence": (
            f"Measured on a shared negative set, {n_cal_fail} of {len(lines)} "
            f"(k, calibrated-rule) cells cannot reach specificity 1.0 at ANY alpha, so "
            f"their sensitivity at matched specificity is 0 while the raw-minimum rule "
            f"still separates.  Where a calibrated rule does reach specificity 1.0 its "
            f"sensitivity is compared against RAW's directly on the same denominator.  "
            f"Calibration costs recall here, and the reason is diagnosed rather than "
            f"asserted: both nulls reject the unedited control, one because v1 is "
            f"extremal by construction and one because contiguous windows are deeper "
            f"than random layer subsets even without an edit."),
    }


# ---------------------------------------------------------------------------
# STAGE 6 -- generalised subspace discovery
# ---------------------------------------------------------------------------
def stage_s6() -> dict:
    armb = load_armb()
    arma = load_arma()
    negs, _ = load_negatives()
    neg_raw = {k: [x for x in (neg_score(r, k) for r in negs) if x is not None]
               for k in KS_ALL}
    tau_by_k = {k: spec_matched_threshold(v, 0) for k, v in neg_raw.items() if v}

    rows, disagreements = [], []
    for r in armb:
        sub = r.get("subspace")
        if not sub:
            rows.append({"model_id": r["kernel_id"], "applicable": False,
                         "reason": "no known removed subspace recorded"})
            continue
        disc = bool(sub["SD_at_dimR"] >= 0.9)
        comp = bool(sub["log10_min_e_R"] <= TAU)
        pred = bool(disc and comp)
        obs_pooled = bool(r["W05_abl_min_layer_energy"] <= TAU)
        best_k, best_v = None, float("inf")
        for k in KS_ALL:
            v = rule_scores(r, k, "RAW")
            if v is not None and v < best_v:
                best_k, best_v = k, v
        obs_win = bool(best_k is not None and best_v <= tau_by_k.get(best_k, TAU))
        row = {
            "model_id": r["kernel_id"], "arm": "B", "applicable": True,
            "recipe_class": r["recipe_class"], "dim_R": sub["dim_R"],
            "SD_at_dimR": sub["SD_at_dimR"], "j_star": sub["j_star"],
            "max_angle_deg": sub["sd_by_j"][str(min(sub["dim_R"], M.N_BOTTOM))]["max_angle_deg"],
            "angles_deg": sub["sd_by_j"][str(min(sub["dim_R"], M.N_BOTTOM))]["angles_deg"],
            "abscos_v1_r": (r.get("derivation") or {}).get("abscos_v1_r"),
            "single_direction_rule_defined": bool(sub["dim_R"] == 1),
            "log10_min_e_R": sub["log10_min_e_R"],
            "discovery_generalised": disc, "completion": comp,
            "predicted_detection": pred,
            "observed_detection_W05": obs_pooled,
            "observed_detection_W05w": obs_win,
            "best_k": best_k, "best_W05w": best_v,
            "W05": r["W05_abl_min_layer_energy"],
        }
        rows.append(row)
        if pred != obs_pooled:
            disagreements.append({**{kk: row[kk] for kk in
                                     ("model_id", "SD_at_dimR", "log10_min_e_R", "W05",
                                      "predicted_detection", "observed_detection_W05")},
                                  "which": "predicted vs observed(W05)"})

    appl = [r for r in rows if r.get("applicable")]
    agree = [r for r in appl if r["predicted_detection"] == r["observed_detection_W05"]]
    table = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    for r in appl:
        p, o = r["predicted_detection"], r["observed_detection_W05"]
        table["TP" if (p and o) else "FP" if (p and not o) else
              "FN" if (not p and o) else "TN"] += 1

    named = {"RANK_K2", "RANK_K4", "RANK_K8", "MPOA_NORMPRESERVING",
             "HERETIC_PERCOMPONENT", "HERETIC_PERCOMPONENT_DEPTHVARY"}
    covered = named & {r["model_id"] for r in appl}

    # ---- Arm A: inapplicable BY CONSTRUCTION, plus the parent-requiring surrogate
    vb_dir = RES / "vbottom"
    surrogate, n_surr_possible = [], 0
    by_repo = {r["repo_id"]: r for r in arma if r.get("status") == "OK"}
    for r in arma:
        if r.get("status") != "OK" or r.get("role") == "parent":
            continue
        par = r.get("declared_parent")
        have = bool(par and par in by_repo
                    and (vb_dir / f"{safe(r['repo_id'])}.npy").exists()
                    and (vb_dir / f"{safe(par)}.npy").exists())
        if par and par in by_repo:
            n_surr_possible += 1
        if not have:
            continue
        try:
            Vc = np.load(vb_dir / f"{safe(r['repo_id'])}.npy")
            Vp = np.load(vb_dir / f"{safe(par)}.npy")
            if Vc.shape[0] != Vp.shape[0]:
                continue
            import wwin as WW
            sd = WW.subspace_discovery(Vc[:, :1], Vp[:, :1])
            surrogate.append({"repo_id": r["repo_id"], "parent": par,
                              "SD_child_v1_vs_parent_v1": sd["SD"],
                              "angle_deg": sd["max_angle_deg"],
                              "recipe_class": r.get("recipe_class_rederived"),
                              "W05": r.get("W05_abl_min_layer_energy")})
        except (OSError, ValueError) as exc:
            logger.warning(f"surrogate failed for {r['repo_id']}: {exc}")

    out = {
        "rule": {
            "generalised_discovery": "SD(dim R) = sum_i cos^2(theta_i) / dim(R) >= 0.9, "
                                     "theta = principal angles between the bottom-j "
                                     "eigenspace of the pooled Gram and the KNOWN removed "
                                     "span R, j = dim(R)",
            "completion": f"log10 min_m e_R(W_m) <= {TAU}, "
                          "e_R(W) = ||R^T W||_F^2 / (||W||_F^2/d) / dim(R)",
            "predicted_detection": "discovery AND completion",
        },
        "rows": rows,
        "n_applicable": len(appl),
        "n_inapplicable": len(rows) - len(appl),
        "agreement_2x2_vs_W05": table,
        "agreement_fraction": len(agree) / len(appl) if appl else float("nan"),
        "disagreements": disagreements,
        "named_kernels_required_by_P8": sorted(named),
        "named_kernels_applicable": sorted(covered),
        "P8_applicability_complete": bool(covered == named),
        "single_direction_rule_undefined_on":
            sorted(r["model_id"] for r in appl if not r["single_direction_rule_defined"]),
        "arm_a": {
            "inapplicable_by_construction": True,
            "reason": ("For a Hub checkpoint the removed direction is UNKNOWN.  It is not "
                       "imputed: a direction estimated from the edited model itself would "
                       "make the discovery test circular.  Arm A rows are therefore "
                       "reported as inapplicable to the parent-free generalised rule."),
            "surrogate_name": "parent-requiring surrogate, NOT the parent-free rule",
            "n_pairs_possible": n_surr_possible,
            "n_pairs_computed": len(surrogate),
            "rows": surrogate,
        },
    }
    M.write_json(RES / "arm3_subspace.json", out)
    logger.info(f"S6: {len(appl)} applicable, agreement "
                f"{out['agreement_fraction']:.3f}, P8 applicability "
                f"{out['P8_applicability_complete']}")
    return out


def safe(s: str) -> str:
    return s.replace("/", "__")


# ---------------------------------------------------------------------------
# STAGE 7 -- the derivation
# ---------------------------------------------------------------------------
def stage_s7() -> dict:
    rows = M.read_jsonl(RES / "derivation.jsonl")
    keep = [r for r in rows if r.get("cos2_theta") is not None]
    agg = []
    for r in keep:
        agg.append({k: r.get(k) for k in
                    ("model_id", "arm", "cos2_theta", "abscos_v1_r", "log10_min_e_r",
                     "max_abs_residual", "max_abs_rel_residual", "argmin_matrix",
                     "argmax_residual_matrix", "e_W_v1_at_argmin", "e_W_r_at_argmin",
                     "residual_at_argmin", "rel_residual_at_argmin",
                     "n_write_matrices", "subspace_log10_min_e_R")})
    at_argmin_abs = [abs(r["residual_at_argmin"]) for r in agg
                     if r.get("residual_at_argmin") is not None]
    at_argmin_rel = [abs(r["rel_residual_at_argmin"]) for r in agg
                     if r.get("rel_residual_at_argmin") is not None]
    # The identity is only TIGHT where discovery holds -- that is the whole
    # content of it.  On the unedited parent cos^2(theta) ~ 1e-4, so the cross
    # term IS the whole of e_W(v1) and the relative residual is ~1.  Quoting a
    # single pooled bound over both regimes would hide exactly the conditional
    # the paper depends on, so both are reported and the conditional one is the
    # one the sentence quotes.
    disc = {r["model_id"] for r in agg
            if r.get("abscos_v1_r") is not None and r["abscos_v1_r"] ** 2 >= 0.9}
    d_abs = [abs(r["residual_at_argmin"]) for r in agg
             if r["model_id"] in disc and r.get("residual_at_argmin") is not None]
    d_rel = [abs(r["rel_residual_at_argmin"]) for r in agg
             if r["model_id"] in disc and r.get("rel_residual_at_argmin") is not None]

    # ---- re-derive the archived pairs as a sanity check ----
    armb = {r["kernel_id"]: r for r in load_armb()}
    checks = []
    for kid, archived in (("UNIFORM_w0.7", -1.1535), ("UNIFORM_w0.85", -1.7488),
                          ("UNIFORM_w1.0", -4.5917), ("PARENT", -1.0098),
                          ("GAUSSIAN_s16", -2.8883), ("GAUSSIAN_s32", -3.9083),
                          ("GAUSSIAN_s64", -4.4729)):
        if kid in armb:
            got = armb[kid]["W05_abl_min_layer_energy"]
            checks.append({"kernel_id": kid, "archived_W05": archived, "recomputed_W05": got,
                           "delta": abs(got - archived), "PASS": bool(abs(got - archived) <= 1e-3)})
    parent_like = []
    for kid, r in armb.items():
        if kid.startswith("GAUSSIAN_s") and not kid.endswith("__fp32store"):
            s = r.get("spread")
            if s is not None and s <= 8:
                parent_like.append({"kernel_id": kid, "spread": s,
                                    "W05": r["W05_abl_min_layer_energy"],
                                    "is_parent_level": bool(
                                        abs(r["W05_abl_min_layer_energy"] + 1.0098) < 0.01)})

    out = {
        "identity": ("e_W(v1) = e_W(r) cos^2(theta) + residual, with "
                     "e_W(u) = ||u^T W||^2 / (||W||_F^2/d), theta the angle between the "
                     "pooled bottom eigenvector v1 and the KNOWN removed direction r.  "
                     "The residual is the cross term; it is measured, not assumed away."),
        "rows": agg,
        "n_models": len(agg),
        "max_abs_residual_at_argmin": max(at_argmin_abs) if at_argmin_abs else None,
        "max_abs_rel_residual_at_argmin": max(at_argmin_rel) if at_argmin_rel else None,
        "max_abs_residual_any_matrix": max(
            (r["max_abs_residual"] for r in agg if r.get("max_abs_residual") is not None),
            default=None),
        "archived_pair_checks": checks,
        "gaussian_spread_le8_parent_level": parent_like,
        "n_models_discovery_holds": len(disc),
        "models_discovery_holds": sorted(disc),
        "discovery_criterion": "cos^2(theta) = <v1, r>^2 >= 0.9",
        "max_abs_residual_at_argmin_where_discovery_holds": max(d_abs) if d_abs else None,
        "max_abs_rel_residual_at_argmin_where_discovery_holds": max(d_rel) if d_rel else None,
    }
    # ---- the residual is not arbitrary: it is sin^2(theta) times an O(1) scale ----
    #
    # At the argmin matrix BOTH e_W(v1) and e_W(r) are at the annihilation floor,
    # so the cross term is the same order as the terms themselves and the RELATIVE
    # residual stays O(1) however well discovery holds.  That is not a failure of
    # the identity, it is what the identity says: the leftover is the energy along
    # the component of v1 orthogonal to r, which is sin^2(theta) times the
    # ordinary (un-annihilated) energy scale, and the ordinary scale is O(1) by the
    # d-normalisation while the annihilated scale is ~1e-5.  Dividing the measured
    # residual by sin^2(theta) recovers that O(1) constant, which is the check.
    ratios = []
    for r in agg:
        if r["model_id"] not in disc or r.get("residual_at_argmin") is None:
            continue
        s2 = 1.0 - float(r["cos2_theta"])
        if s2 > 1e-12:
            ratios.append({"model_id": r["model_id"],
                           "sin2_theta": s2,
                           "residual_at_argmin": r["residual_at_argmin"],
                           "residual_over_sin2": r["residual_at_argmin"] / s2})
    vals = [abs(x["residual_over_sin2"]) for x in ratios]
    out["residual_scaling"] = {
        "law": "residual(argmin) = sin^2(theta) * e_scale, e_scale an O(1) constant "
               "set by the d-normalisation of e(u, W)",
        "rows": ratios,
        "n": len(ratios),
        "max_abs_residual_over_sin2": max(vals) if vals else None,
        "median_abs_residual_over_sin2": float(np.median(vals)) if vals else None,
    }

    X = out["max_abs_residual_at_argmin_where_discovery_holds"]
    Y = out["max_abs_rel_residual_at_argmin_where_discovery_holds"]
    Z = out["residual_scaling"]["max_abs_residual_over_sin2"]
    out["sentence_relative_bound_does_not_hold"] = (
        "The plan expected a small RELATIVE residual.  It does not exist and cannot: at "
        "the argmin matrix both e_W(v1) and e_W(r) sit at the annihilation floor (~1e-5), "
        "so the cross term is the same order as the terms it corrects and the relative "
        f"residual reaches {Y:.2f} even where cos^2(theta) > 0.999.  What IS bounded is "
        "the residual in absolute energy, and it obeys a law rather than a bound: "
        f"|residual| / sin^2(theta) <= {Z:.3f} across the "
        f"{out['residual_scaling']['n']} kernels where discovery holds, i.e. the leftover "
        "is exactly the energy along the part of v1 orthogonal to r.")
    out["sentence"] = (
        f"On the {len(disc)} kernels where discovery holds (cos^2(theta) >= 0.9), the cross "
        f"term at the argmin matrix -- the one that sets W05 -- is at most {X:.3e} in "
        f"absolute terms and {Y:.3e} relative, so detection and completion are the same "
        f"number to within {Y:.3e} whenever discovery holds.  Where discovery FAILS the "
        f"cross term is the whole statistic: over all {len(agg)} kernels the bound is "
        f"{out['max_abs_residual_at_argmin']:.3e} absolute and "
        f"{out['max_abs_rel_residual_at_argmin']:.3e} relative, which is the arithmetic "
        f"reason the conditional cannot be dropped."
        if X is not None else
        (f"no kernel reached cos^2(theta) >= 0.9; over all {len(agg)} scored kernels the "
         f"unconditional bound is {out['max_abs_residual_at_argmin']} absolute"
         if agg else "no model with a known removed direction was scored"))
    M.write_json(RES / "derivation_summary.json", out)
    logger.info(f"S7: {out['sentence'][:140]}")
    return out


# ---------------------------------------------------------------------------
# STAGE 8 -- predictions scorecard, numbers.json, method_out.json, README
# ---------------------------------------------------------------------------
def score_predictions(s5: dict, s6: dict) -> dict:
    armb = {r["kernel_id"]: r for r in load_armb()}
    arma = load_arma()
    negs, _ = load_negatives()
    neg_raw = {k: [x for x in (neg_score(r, k) for r in negs) if x is not None]
               for k in KS_ALL}
    tau_by_k = {k: spec_matched_threshold(v, 0) for k, v in neg_raw.items() if v}
    ks_le8 = [k for k in KS_ALL if k != "L"]

    def best_w05w(kid, ks=None):
        r = armb.get(kid)
        if r is None:
            return None, None
        bk, bv = None, float("inf")
        for k in (ks or ks_le8):
            v = rule_scores(r, k, "RAW")
            if v is not None and v < bv:
                bk, bv = k, v
        return bk, bv

    res = []

    # P1 -- BAND_MID50
    r = armb.get("BAND_MID50")
    if r is None:
        res.append({"id": "P1", "verdict": "UNSCORABLE", "reason": "BAND_MID50 not scored"})
    else:
        bk, bv = best_w05w("BAND_MID50")
        rec = bool(bv is not None and bv <= TAU and r["W05_abl_min_layer_energy"] > TAU)
        res.append({"id": "P1", "predicted": "RECOVERED",
                    "observed": "RECOVERED" if rec else "NOT_RECOVERED",
                    "verdict": "CONFIRMED" if rec else "REFUTED",
                    "numbers": {"W05": r["W05_abl_min_layer_energy"], "tau": TAU,
                                "best_k": bk, "best_W05w": bv}})

    # P2 -- Gaussian spreads with min depth weight < 0.5311
    p2 = []
    for s in (0.5, 1.0, 2.0, 4.0, 8.0):
        kid = f"GAUSSIAN_s{s:g}"
        r = armb.get(kid)
        if r is None:
            continue
        bk, bv = best_w05w(kid)
        p2.append({"kernel_id": kid, "W05": r["W05_abl_min_layer_energy"],
                   "min_depth_weight": r.get("min_depth_weight"),
                   "best_k": bk, "best_W05w": bv,
                   "missed_by_pooled": bool(r["W05_abl_min_layer_energy"] > TAU),
                   "recovered": bool(bv is not None and bv <= TAU)})
    # WHY, measured: a window is only fully inside the edit if the edited band is
    # at least k layers wide.  Below that, every k-window contains an UNEDITED
    # layer, and the minimum over the window is set by that layer -- so windowing
    # cannot help however small k is made, short of k = 1.
    import kernels as _K
    for x in p2:
        s = armb[x["kernel_id"]].get("spread")
        if s is None:
            continue
        wts = _K.w_gaussian(28, M.GAUSSIAN_PEAK, s)
        for thr in (0.5, 0.1):
            x[f"band_width_at_w{thr}"] = int(sum(1 for w in wts if w >= thr))
    allrec = bool(p2) and all(x["recovered"] and x["missed_by_pooled"] for x in p2)
    res.append({"id": "P2", "predicted": "RECOVERED",
                "observed": "RECOVERED" if allrec else "NOT_RECOVERED",
                "verdict": "CONFIRMED" if allrec else ("REFUTED" if p2 else "UNSCORABLE"),
                "numbers": {
                    "per_spread": p2, "tau": TAU,
                    "n_recovered": sum(x["recovered"] for x in p2), "n": len(p2),
                    "mechanism": (
                        "Recovery requires the edited band to be at least k layers wide.  "
                        "The two spreads that are NOT recovered confine the edit to a "
                        "single layer (band width 1 at depth weight >= 0.1), so even the "
                        "narrowest window tested, k = 2, always contains an unedited layer "
                        "and the minimum over the window is set by that layer.  This is not "
                        "a failure of the window statistic; it is the statement that the "
                        "smallest detectable edit width equals the smallest usable k."),
                    "band_width_vs_recovery": {
                        x["kernel_id"]: {"band_width_at_w0.1": x.get("band_width_at_w0.1"),
                                         "recovered": x["recovered"]} for x in p2},
                }})

    # P3 -- Arm A partial-layer class
    pa = positives_arma(arma)
    cls_rows = [r for r in pa if r.get("recipe_class_rederived") == "R_PARTIAL_LAYER"
                or r.get("manifest_class") == "R4_PARTIAL_LAYER_OR_PER_HEAD"]
    if not cls_rows:
        res.append({"id": "P3", "verdict": "UNSCORABLE",
                    "reason": "no Arm A row of class R_PARTIAL_LAYER / "
                              "R4_PARTIAL_LAYER_OR_PER_HEAD completed in the tier that ran",
                    "numbers": {"n_arm_a_positives_scored": len(pa)}})
    else:
        neg_pooled = [float(x["W05_abl_min_layer_energy"]) for x in negs]
        tau_p = spec_matched_threshold(neg_pooled, 0)
        s_w05 = sum(1 for r in cls_rows if r["W05_abl_min_layer_energy"] <= tau_p)
        best = {}
        for k in ks_le8:
            if k not in tau_by_k:
                continue
            best[k] = sum(1 for r in cls_rows
                          if (rule_scores(r, k, "RAW") or 1e9) <= tau_by_k[k])
        bk = max(best, key=best.get) if best else None
        ok = bool(bk is not None and best[bk] > s_w05)
        res.append({"id": "P3", "predicted": "RECOVERED",
                    "observed": "RECOVERED" if ok else "NOT_RECOVERED",
                    "verdict": "CONFIRMED" if ok else "REFUTED",
                    "numbers": {"n_class": len(cls_rows), "n_caught_W05": s_w05,
                                "n_caught_W05w_by_k": best, "best_k": bk,
                                "tau_pooled": tau_p, "tau_by_k": tau_by_k,
                                "members": [r["repo_id"] for r in cls_rows]}})

    # P4 -- sub-unit uniform kernels
    p4 = []
    for w in (0.5, 0.7, 0.85):
        kid = f"UNIFORM_w{w}"
        r = armb.get(kid)
        if r is None:
            continue
        allk = {k: rule_scores(r, k, "RAW") for k in KS_ALL}
        gated_any = False
        for k in KS_ALL:
            wnd = (r.get("windowed") or {}).get(k)
            if wnd is None:
                continue
            for tc in TAU_C_GRID:
                v = wnd["W05w"] if wnd["consistency_c"] >= tc else float("inf")
                gated_any = gated_any or (v <= TAU)
        p4.append({"kernel_id": kid, "W05": r["W05_abl_min_layer_energy"],
                   "W05w_by_k": allk, "min_W05w": min(v for v in allk.values() if v is not None),
                   "detected_any_k_or_tauc": bool(gated_any)})
    notrec = bool(p4) and not any(x["detected_any_k_or_tauc"] for x in p4)
    res.append({"id": "P4", "predicted": "NOT_RECOVERED",
                "observed": "NOT_RECOVERED" if notrec else "RECOVERED",
                "verdict": "CONFIRMED" if notrec else ("REFUTED" if p4 else "UNSCORABLE"),
                "numbers": {"per_w": p4, "tau": TAU}})

    # P5 -- ORBA Householder inside the random-direction control band
    par = armb.get("PARENT")
    hh = armb.get("ORBA_LAM1.0")
    ctrl = [r for r in load_armb() if r.get("recipe_class") == "CONTROL_NOISE_FLOOR"]
    if par is None or hh is None or not ctrl:
        res.append({"id": "P5", "verdict": "UNSCORABLE",
                    "reason": "parent, ORBA_LAM1.0 or the random-direction controls missing"})
    else:
        per_k, ok = {}, True
        for k in KS_ALL:
            pv = rule_scores(par, k, "RAW")
            hv = rule_scores(hh, k, "RAW")
            cd = [abs((rule_scores(c, k, "RAW") or 0.0) - pv) for c in ctrl]
            dh = abs(hv - pv)
            per_k[k] = {"parent_W05w": pv, "orba_W05w": hv, "abs_delta": dh,
                        "control_max_abs_delta": max(cd), "control_deltas": cd,
                        "inside": bool(dh <= max(cd))}
            ok = ok and per_k[k]["inside"]
        worst = max(v["abs_delta"] for v in per_k.values())
        margin = min(abs(v["parent_W05w"] - TAU) for v in per_k.values())
        res.append({"id": "P5", "predicted": "NOT_RECOVERED",
                    "observed": "NOT_RECOVERED" if ok else "RECOVERED",
                    "verdict": "CONFIRMED" if ok else "REFUTED",
                    "numbers": {
                        "per_k": per_k, "n_control_seeds": len(ctrl),
                        "max_abs_delta_any_k": worst,
                        "distance_from_parent_to_tau": margin,
                        "delta_as_fraction_of_margin": worst / margin if margin else None,
                        "scoring_note": (
                            "REFUTED as the rule was pre-registered, and the rule is not "
                            "moved.  What is refuted is the literal band: with only "
                            f"{len(ctrl)} random seeds the control MAXIMUM is a poor "
                            "estimate of the noise band's upper tail, and at k = 4 and "
                            "k = 6 the Householder's deviation exceeds it by a factor of "
                            "about two.  Both quantities are float32 Gram accumulation "
                            f"noise: the largest deviation at any k is {worst:.2e} log "
                            f"units, against a distance of {margin:.3f} log units from the "
                            "parent to the detection threshold, i.e. about "
                            f"{worst / margin:.0e} of the margin.  The substantive claim -- "
                            "an orthogonal similarity leaves the spectrum invariant, so the "
                            "ORBA v3 Householder is invisible at every pooling scope -- is "
                            "unaffected, and T0.5 verifies it as arithmetic on the toy."),
                    }})

    # P6 -- the two ORBA recipes never merged
    ann = armb.get("ORBA_ANNIHILATE")
    if hh is None or ann is None:
        res.append({"id": "P6", "verdict": "UNSCORABLE", "reason": "an ORBA row is missing"})
    else:
        hh_und = all((rule_scores(hh, k, "RAW") or 0.0) > TAU for k in KS_ALL)
        ann_det = bool(ann["W05_abl_min_layer_energy"] <= TAU)
        ok = bool(hh_und and ann_det)
        res.append({"id": "P6", "predicted": "NOT_RECOVERED",
                    "observed": "NOT_RECOVERED" if ok else "RECOVERED",
                    "verdict": "CONFIRMED" if ok else "REFUTED",
                    "numbers": {
                        "householder_lam1_W05w_by_k":
                            {k: rule_scores(hh, k, "RAW") for k in KS_ALL},
                        "householder_lam1_undetected_every_k": hh_und,
                        "annihilate_W05": ann["W05_abl_min_layer_energy"],
                        "annihilate_detected": ann_det, "tau": TAU}})

    # P7 -- does calibration cost sensitivity?
    cc = s5["calibration_cost"]["per_k"]
    cmp_rows = {k: v for k, v in cc.items() if v.get("sens_cal") is not None}
    if not cmp_rows:
        res.append({"id": "P7", "predicted": "NOT_RECOVERED",
                    "observed": "NOT_RECOVERED",
                    "verdict": "CONFIRMED",
                    "numbers": {"per_k": cc,
                                "note": "no calibrated rule reached specificity 1.0 at any "
                                        "alpha at any k, so its sensitivity at matched "
                                        "specificity is 0 -- calibration costs everything, "
                                        "which is the predicted direction in its strongest "
                                        "form"}})
    else:
        ok = all(v["cal_le_raw"] for v in cmp_rows.values())
        res.append({"id": "P7", "predicted": "NOT_RECOVERED",
                    "observed": "NOT_RECOVERED" if ok else "RECOVERED",
                    "verdict": "CONFIRMED" if ok else "REFUTED",
                    "numbers": {"per_k": cc}})

    # P8 -- generalised subspace discovery
    ok = bool(s6["P8_applicability_complete"] and s6["agreement_fraction"] >= 0.80)
    res.append({"id": "P8", "predicted": "RECOVERED",
                "observed": "RECOVERED" if ok else "NOT_RECOVERED",
                "verdict": "CONFIRMED" if ok else "REFUTED",
                "numbers": {"applicability_complete": s6["P8_applicability_complete"],
                            "applicable": s6["named_kernels_applicable"],
                            "required": s6["named_kernels_required_by_P8"],
                            "agreement_fraction": s6["agreement_fraction"],
                            "table": s6["agreement_2x2_vs_W05"],
                            "n_disagreements": len(s6["disagreements"])}})

    by_id = {p["id"]: p for p in M.PREDICTIONS}
    for r in res:
        p = by_id.get(r["id"], {})
        r["statement"] = p.get("statement")
        r["class"] = p.get("class")
        r["scoring_rule"] = p.get("scoring_rule")
    out = {"predictions_sha256": (RES / "predictions_iter5.sha256").read_text().strip()
           if (RES / "predictions_iter5.sha256").exists() else None,
           "results": res,
           "n_confirmed": sum(1 for r in res if r["verdict"] == "CONFIRMED"),
           "n_refuted": sum(1 for r in res if r["verdict"] == "REFUTED"),
           "n_unscorable": sum(1 for r in res if r["verdict"] == "UNSCORABLE")}
    M.write_json(RES / "predictions_outcome.json", out)
    for r in res:
        logger.info(f"  {r['id']}: {r['verdict']}")
    return out


def N(value, *, units="", n=None, ci=None, ci_method=None, source_file="",
      selector="", orientation=None, circular=False, tier=None, note=None) -> dict:
    return {"value": value, "units": units, "n": n, "ci": ci, "ci_method": ci_method,
            "source_file": source_file, "source_row_selector": selector,
            "orientation": orientation, "circularity_flag": circular, "tier": tier,
            "note": note}


def stage_s8(s5: dict, s6: dict, s7: dict) -> dict:
    gates = json.loads((RES / "gates.json").read_text())
    env = json.loads((RES / "s0_env.json").read_text())
    tiers = (json.loads((RES / "arma_tier_status.json").read_text())
             if (RES / "arma_tier_status.json").exists()
             else {"tier_completed": "TIER T1 NOT RUN (Arm A stage did not execute)",
                   "tier_counts": {}, "tier_total": {}, "gb_downloaded": 0.0})
    preds = score_predictions(s5, s6)
    armb, arma = load_armb(), load_arma()
    frontier = M.read_jsonl(RES / "frontier.jsonl")
    negs, negmeta = load_negatives()

    num: dict = {}
    num["tier_completed"] = N(tiers["tier_completed"], source_file="results/arma_tier_status.json",
                              tier=tiers["tier_completed"])
    num["openrouter_spend_usd"] = N(0.0, units="USD", source_file="results/s0_env.json",
                                    note="no prompts, no forward passes, no LLM calls")
    num["n_forward_passes"] = N(0, source_file="results/s0_env.json")

    # gates
    g1, g2, g3 = (gates["G1_wstats_reproduction"], gates["G2_root_rebuild"],
                  gates["G3_kL_identity"])
    num["G1_max_abs_dW05"] = N(g1["max_abs_dW05"], units="log10", source_file="results/gates.json",
                               selector="G1_wstats_reproduction.max_abs_dW05",
                               note=f"tolerance {g1['tol_W05']}, PASS={g1['PASS']}; the "
                                    f"archive's own max |dW05| was {g1['archive_own_max_dW05']:.3e}")
    num["G1_host_parent_dW01"] = N(g1["host_parent_deltas"]["W01_abl_suppression_depth"],
                                   units="log10", source_file="results/gates.json",
                                   note="reported, never gated (float32 Gram floor)")
    num["G2_write_matrix_sha256_match"] = N(g2["write_matrix_sha256_match"],
                                            source_file="results/gates.json",
                                            note=f"rebuilt {g2['write_matrix_sha256_rebuilt']}")
    num["G2_root_dW05"] = N(g2["delta_W05"], units="log10", source_file="results/gates.json",
                            note=f"tolerance {g2['tol_W05']}, PASS={g2['PASS_W05']}")
    num["G3_kL_max_delta_vs_f64"] = N(g3["max_delta_a"], units="log10",
                                      source_file="results/gate_kL.json",
                                      note=f"tolerance {g3['tol_a']}, "
                                           f"PASS={g3['PASS_a_all']}; this is the comparison "
                                           f"that actually tests the window code")
    num["G3_kL_max_delta_vs_f32"] = N(g3["max_delta_b"], units="log10",
                                      source_file="results/gate_kL.json",
                                      note=g3["supersession_statement"])
    num["G3_derived_float32_bound_at_d2048"] = N(
        g3["derivation"]["log10_bound_at_2048"], units="log10",
        source_file="results/gate_kL.json", note=g3["derivation"]["statement"])
    num["G3_PASS_at_iter4_declared_1e-9"] = N(
        g3["PASS_b_all_at_iter4_declared_1e-9"], source_file="results/gate_kL.json",
        note="retained and reported as FAILED at its declared tolerance")

    # headline: recovery on Arm B
    pb = positives_armb(armb)
    ks_le8 = [k for k in KS_ALL if k != "L"]
    missed = [r for r in pb if r["W05_abl_min_layer_energy"] > TAU]
    rec = [r for r in missed
           if min((rule_scores(r, k, "RAW") or 1e9) for k in ks_le8) <= TAU]
    p, lo, hi = SX.wilson(len(rec), len(missed)) if missed else (float("nan"), 0.0, 1.0)
    num["armB_pooled_misses_recovered_by_windowing"] = N(
        p, n=len(missed), ci=[lo, hi], ci_method="Wilson score, z=1.96",
        source_file="results/armb_w05w.jsonl",
        selector="recipe_class not in {PARENT, CONTROL_NOISE_FLOOR} and W05 > tau",
        note=f"{len(rec)} of {len(missed)} kernels that the pooled W05 misses at the "
             f"pre-registered tau = {TAU:.4f} are caught by min_k<=8 W05w(k) at the same "
             f"tau; recovered = {sorted(r['kernel_id'] for r in rec)}")
    num["armB_n_positives"] = N(len(pb), source_file="results/armb_w05w.jsonl")
    num["armB_n_kernels_total"] = N(len(armb), source_file="results/armb_w05w.jsonl")

    for k in KS_ALL:
        for arm in ("B", "A"):
            # the headline sensitivity/specificity pair is quoted on the REAL
            # undeclared population, never on the five in-memory controls
            rows = [r for r in frontier if r["k"] == k and r["rule"] == "RAW"
                    and r["arm"] == arm and r["threshold_kind"].startswith("specificity")
                    and "in-memory unedited controls" not in r["threshold_kind"]]
            if not rows:
                continue
            best = max(rows, key=lambda r: (r["specificity"], r["sensitivity"]))
            num[f"sensitivity_arm{arm}_k{k}"] = N(
                best["sensitivity"], n=best["n_pos"],
                ci=[best["sens_wilson_lo"], best["sens_wilson_hi"]],
                ci_method=best["ci_method"], source_file="results/frontier.jsonl",
                selector=f"k={k}, rule=RAW, arm={arm}, {best['threshold_kind']}",
                circular=best["threshold_fitted_on_negatives_only"],
                tier=tiers["tier_completed"] if arm == "A" else "in-memory")
            num[f"specificity_arm{arm}_k{k}"] = N(
                best["specificity"], n=best["n_neg"],
                ci=[best["spec_wilson_lo"], best["spec_wilson_hi"]],
                ci_method=best["ci_method"], source_file="results/frontier.jsonl",
                selector=f"k={k}, rule=RAW, arm={arm}, {best['threshold_kind']}",
                circular=True, note=negmeta["note"])

    num["negatives_n_eligible_with_W05w"] = N(
        negmeta["n_scan_new_eligible_with_W05w"], source_file="archive/arm2_scan_new.jsonl",
        note=negmeta["note"])
    num["negatives_n_archived_W05_only"] = N(
        negmeta["n_archived_eligible_W05_only"],
        source_file="archive/arm2_archive_eligibility.jsonl",
        note="W05-only, NOT re-scored at W05w")

    num["catch_by_recipe_class"] = N(s5["catch_by_recipe_class"],
                                     source_file="results/arm2_frontier_summary.json",
                                     note="populated for every k")
    num["random_direction_null_rejects_the_negative_control"] = N(
        s5["random_direction_null_finding"]["unedited_parent_z_min_by_k"],
        units="z", source_file="results/arm2_frontier_summary.json",
        note=s5["random_direction_null_finding"]["statement"])
    num["calibration_cost_sentence"] = N(s5["calibration_cost"]["sentence"],
                                         source_file="results/arm2_frontier_summary.json")
    sp = s5["subset_null_correction"]
    par = next((r for r in sp["rows"] if r["model_id"] == "PARENT"), None)
    num["subset_null_p_sidak_unedited_parent"] = N(
        (par or {}).get("p_sidak_parametric"),
        source_file="results/arm2_frontier_summary.json",
        selector="subset_null_correction.rows[model_id=PARENT]",
        note=sp["statement"] + "  " + sp["correction"])
    cc = sp["contiguity_confound"]
    num["contiguity_gap_unedited_parent"] = N(
        (cc["unedited_parent"] or {}).get("gap"), units="log10",
        source_file="results/arm2_frontier_summary.json",
        selector="subset_null_correction.contiguity_confound.unedited_parent.gap",
        note=cc["statement"] + "  " + cc["consequence"])
    loc = {r["model_id"]: r["p_sidak_parametric"] for r in sp["rows"]
           if r["model_id"].startswith(("BAND_", "GAUSSIAN_s2", "GAUSSIAN_s4",
                                        "GAUSSIAN_s8", "UNIFORM_"))
           and not r["model_id"].endswith("__fp32store")}
    num["subset_null_p_sidak_localised_vs_global"] = N(
        loc, source_file="results/arm2_frontier_summary.json",
        note="the layer-subset null separates DEPTH-LOCALISED edits (band, small-spread "
             "Gaussians) from GLOBAL ones (uniform w), which is exactly what a "
             "multiple-window correction should do and what the random-direction null "
             "could not")

    # Arm 3
    num["arm3_agreement_fraction"] = N(
        s6["agreement_fraction"], n=s6["n_applicable"],
        source_file="results/arm3_subspace.json",
        note=f"2x2 = {s6['agreement_2x2_vs_W05']}; "
             f"{s6['n_inapplicable']} kernels inapplicable")
    num["arm3_single_direction_rule_undefined_on"] = N(
        s6["single_direction_rule_undefined_on"], source_file="results/arm3_subspace.json",
        note="these are exactly the kernels on which |cos(v1,r)|>0.9 has no meaning")
    num["arm3_armA_inapplicable_by_construction"] = N(
        True, source_file="results/arm3_subspace.json", note=s6["arm_a"]["reason"])
    num["arm3_armA_surrogate_pairs"] = N(
        s6["arm_a"]["n_pairs_computed"], n=s6["arm_a"]["n_pairs_possible"],
        source_file="results/arm3_subspace.json", note=s6["arm_a"]["surrogate_name"])

    # Arm 4
    num["derivation_max_abs_residual_at_argmin"] = N(
        s7["max_abs_residual_at_argmin"], n=s7["n_models"],
        source_file="results/derivation_summary.json", note=s7["identity"])
    num["derivation_max_rel_residual_at_argmin"] = N(
        s7["max_abs_rel_residual_at_argmin"], n=s7["n_models"],
        source_file="results/derivation_summary.json", note=s7["sentence"])
    num["derivation_max_rel_residual_where_discovery_holds"] = N(
        s7["max_abs_rel_residual_at_argmin_where_discovery_holds"],
        n=s7["n_models_discovery_holds"],
        source_file="results/derivation_summary.json",
        selector="cos^2(theta) >= 0.9",
        note=s7["sentence_relative_bound_does_not_hold"])
    num["derivation_residual_over_sin2_theta"] = N(
        s7["residual_scaling"]["max_abs_residual_over_sin2"],
        n=s7["residual_scaling"]["n"],
        source_file="results/derivation_summary.json",
        selector="residual_scaling.max_abs_residual_over_sin2",
        note=s7["residual_scaling"]["law"] + "  This is the quantity that IS bounded; "
             "the relative residual is not, and the reason is arithmetic, not noise.")

    # baseline head-to-head
    bl = baseline_head_to_head(arma, negs)
    num["baseline_repo_name_regex"] = N(
        bl["baseline_sensitivity"], n=bl["n_pos"],
        ci=[bl["baseline_sens_lo"], bl["baseline_sens_hi"]],
        ci_method="Wilson score, z=1.96", source_file="results/baseline.json",
        note=f"{len(M.BASELINE_TERMS)}-term regex on the repo id alone; "
             f"specificity {bl['baseline_specificity']}.  {bl['term_selection_caveat']}")
    num["baseline_repo_name_regex_frozen8"] = N(
        bl["frozen8"]["sensitivity"], n=bl["n_pos"], ci=bl["frozen8"]["sens_ci"],
        ci_method="Wilson score, z=1.96", source_file="results/baseline.json",
        selector="frozen8", note=bl["frozen8"]["provenance"]
        + f"; specificity {bl['frozen8']['specificity']}")

    # predictions
    num["predictions_scorecard"] = N(
        {r["id"]: r["verdict"] for r in preds["results"]},
        source_file="results/predictions_outcome.json",
        note=f"stamped before scoring, sha256 {preds['predictions_sha256']}")

    M.write_json(RES / "numbers.json", num)
    M.write_json(RES / "baseline.json", bl)
    logger.info(f"S8: numbers.json has {len(num)} entries")
    return {"numbers": num, "predictions": preds, "baseline": bl, "tiers": tiers}


FROZEN8 = ["abliterat", "gabliterat", "obliterat", "uncensor", "decensor",
           "orthogonal", "norm[-_]preserv", "refusal[-_]?(free|removed)"]
FROZEN8_RE = __import__("re").compile("(?i)(" + "|".join(FROZEN8) + ")")


def baseline_head_to_head(arma: list[dict], negs: list[dict]) -> dict:
    """The regex baseline, side by side with our statistic, on the SAME rows.

    Reported under BOTH term sets.  The 11-term list extends the dependency
    dataset's frozen 8-term `repo_id_contains_abliteration_string` feature with
    three edit-tool names, and adding terms is itself a fitting step: a longer
    list can only raise sensitivity and can only lower specificity.  Quoting one
    number would let the choice of terms decide the head-to-head, so the frozen
    8-term feature is reported beside it as the un-extended reference.
    """
    pos = positives_arma(arma)
    hits = [r for r in pos if r.get("baseline_repo_name_regex")]
    fp = [r for r in negs if M.BASELINE_RE.search(r.get("repo") or "")]
    h8 = [r for r in pos if FROZEN8_RE.search(r["repo_id"])]
    f8 = [r for r in negs if FROZEN8_RE.search(r.get("repo") or "")]
    s8v, s8l, s8h = SX.wilson(len(h8), len(pos)) if pos else (float("nan"), 0.0, 1.0)
    c8v, c8l, c8h = (SX.wilson(len(negs) - len(f8), len(negs)) if negs
                     else (float("nan"), 0.0, 1.0))
    sp, sl, sh = SX.wilson(len(hits), len(pos)) if pos else (float("nan"), 0.0, 1.0)
    sc, cl, ch = SX.wilson(len(negs) - len(fp), len(negs)) if negs else (float("nan"), 0.0, 1.0)
    ours = {}
    neg_raw = {k: [x for x in (neg_score(r, k) for r in negs) if x is not None]
               for k in KS_ALL}
    for k in KS_ALL:
        if not neg_raw.get(k) or not pos:
            continue
        tau_k = spec_matched_threshold(neg_raw[k], 0)
        h = [r for r in pos if (rule_scores(r, k, "RAW") or 1e9) <= tau_k]
        v, lo, hi = SX.wilson(len(h), len(pos))
        ours[k] = {"threshold": tau_k, "sensitivity": v, "ci": [lo, hi], "n_hit": len(h)}
    return {
        "definition": f"{len(M.BASELINE_TERMS)}-term case-insensitive regex on the repo id: "
                      + "|".join(M.BASELINE_TERMS),
        "provenance": ("the first 8 terms are the dependency dataset's FROZEN "
                       "repo_id_contains_abliteration_string feature (hub_common.py:31); "
                       "the last 3 are the unambiguous edit-tool names from that dataset's "
                       "own harvest net"),
        "n_pos": len(pos), "n_neg": len(negs),
        "baseline_n_hit": len(hits), "baseline_sensitivity": sp,
        "baseline_sens_lo": sl, "baseline_sens_hi": sh,
        "baseline_n_false_positive": len(fp), "baseline_specificity": sc,
        "baseline_spec_ci": [cl, ch],
        "baseline_hits": sorted(r["repo_id"] for r in hits),
        "baseline_misses": sorted(r["repo_id"] for r in pos
                                  if not r.get("baseline_repo_name_regex")),
        "ours_W05w_by_k": ours,
        "frozen8": {
            "definition": "|".join(FROZEN8),
            "provenance": "the dependency dataset's FROZEN "
                          "repo_id_contains_abliteration_string feature, hub_common.py:31",
            "n_hit": len(h8), "sensitivity": s8v, "sens_ci": [s8l, s8h],
            "n_false_positive": len(f8), "specificity": c8v, "spec_ci": [c8l, c8h],
        },
        "term_selection_caveat": (
            "The 11-term list is the frozen 8 plus three edit-tool names.  Extending a "
            "term list is a fitting step -- it can only raise sensitivity and only lower "
            "specificity -- so the 8-term frozen feature is reported beside it and the "
            "head-to-head should be read against BOTH.  A sibling artifact in this run "
            "found the same effect at Hub scale, with the extended list firing on far "
            "more edited repos than the frozen feature does."),
        "note": ("The baseline is not a strawman: a plain regex on the repo id alone "
                 "solves half the detection task on the Hub (50.5% of declared-edited "
                 "repos, per the dependency dataset).  It is also free and needs no "
                 "weights.  Its weakness is that it is a declaration detector, not an "
                 "edit detector: it cannot fire on an undeclared edit at all."),
    }


def write_method_out(s5: dict, s6: dict, s7: dict, s8: dict) -> None:
    armb, arma = load_armb(), load_arma()
    negs, _ = load_negatives()
    ks_le8 = [k for k in KS_ALL if k != "L"]
    neg_raw = {k: [x for x in (neg_score(r, k) for r in negs) if x is not None]
               for k in KS_ALL}
    tau_by_k = {k: spec_matched_threshold(v, 0) for k, v in neg_raw.items() if v}
    sub_by_id = {r["model_id"]: r for r in s6["rows"] if r.get("applicable")}

    def ex(*, mid, gold, w05, wbyk, cls, extra):
        bk, bv = None, float("inf")
        for k in ks_le8:
            v = wbyk.get(k)
            if v is not None and v < bv:
                bk, bv = k, v
        e = {
            "input": mid,
            "output": gold,
            "predict_baseline_pooled_W05": "EDITED" if (w05 is not None and w05 <= TAU) else "CLEAN",
            "predict_baseline_repo_name_regex": extra.get("regex", "NOT_APPLICABLE"),
            "predict_our_W05w_best_k": ("EDITED" if (bv is not None and bk is not None
                                                     and bv <= tau_by_k.get(bk, TAU))
                                        else "CLEAN"),
            "predict_our_W05w_at_pretau": "EDITED" if bv <= TAU else "CLEAN",
            "metadata_recipe_class": cls,
            "metadata_W05": w05,
            "metadata_W05w_by_k": wbyk,
            "metadata_best_k": bk,
            "metadata_best_W05w": (None if not math.isfinite(bv) else bv),
            "metadata_tau_pooled": TAU,
            "metadata_tau_by_k": tau_by_k,
        }
        e.update(extra.get("meta", {}))
        return e

    ds_b, ds_a, ds_n = [], [], []
    for r in armb:
        wb = {k: rule_scores(r, k, "RAW") for k in KS_ALL}
        sub = sub_by_id.get(r["kernel_id"], {})
        gold = ("CONTROL" if r.get("recipe_class") in CONTROL_CLASSES else "EDITED")
        ds_b.append(ex(mid=r["kernel_id"], gold=gold, w05=r["W05_abl_min_layer_energy"],
                       wbyk=wb, cls=r.get("recipe_class"),
                       extra={"meta": {
                           "metadata_arm": "B_in_memory_kernel",
                           "metadata_dtype_stored": r.get("dtype_stored"),
                           "metadata_dim_R_known": r.get("dim_R_known"),
                           "metadata_SD_at_dimR": sub.get("SD_at_dimR"),
                           "metadata_j_star": sub.get("j_star"),
                           "metadata_discovery_generalised": sub.get("discovery_generalised"),
                           "metadata_completion": sub.get("completion"),
                           "metadata_predicted_detection": sub.get("predicted_detection"),
                           "metadata_abscos_v1_r": (r.get("derivation") or {}).get("abscos_v1_r"),
                           "metadata_subset_null_p_sidak": (subset_p(r) or {}).get(
                               "p_sidak_parametric"),
                           "metadata_consistency_by_k": {
                               k: (r["windowed"].get(k) or {}).get("consistency_c")
                               for k in KS_ALL},
                       }}))
    for r in arma:
        if r.get("status") != "OK":
            ds_a.append({"input": r["repo_id"], "output": "UNRESOLVED",
                         "predict_baseline_pooled_W05": "UNRESOLVED",
                         "predict_baseline_repo_name_regex":
                             "EDITED" if r.get("baseline_repo_name_regex") else "CLEAN",
                         "predict_our_W05w_best_k": "UNRESOLVED",
                         "predict_our_W05w_at_pretau": "UNRESOLVED",
                         "metadata_arm": "A_hub_checkpoint",
                         "metadata_error": r.get("error"),
                         "metadata_tier": r.get("tier"),
                         "metadata_excluded_from_denominators": True})
            continue
        wb = {k: rule_scores(r, k, "RAW") for k in KS_ALL}
        gold = "EDITED" if r.get("role") in ("edited", "parent_also_edited") else "CLEAN"
        ds_a.append(ex(mid=r["repo_id"], gold=gold, w05=r["W05_abl_min_layer_energy"],
                       wbyk=wb, cls=r.get("recipe_class_rederived"),
                       extra={"regex": "EDITED" if r.get("baseline_repo_name_regex") else "CLEAN",
                              "meta": {
                                  "metadata_arm": "A_hub_checkpoint",
                                  "metadata_tier": r.get("tier"),
                                  "metadata_revision": r.get("revision"),
                                  "metadata_role": r.get("role"),
                                  "metadata_uploader": r.get("uploader"),
                                  "metadata_declared_parent": r.get("declared_parent"),
                                  "metadata_archived_W05": r.get("archived_W05"),
                                  "metadata_delta_W05_vs_archive": r.get("delta_W05_vs_archive"),
                                  "metadata_subset_null_p_sidak": (subset_p(r) or {}).get(
                                      "p_sidak_parametric"),
                              }}))
    for r in negs:
        wb = {k: neg_score(r, k) for k in KS_ALL}
        ds_n.append(ex(mid=r["repo"], gold="CLEAN",
                       w05=r["W05_abl_min_layer_energy"], wbyk=wb,
                       cls="UNDECLARED",
                       extra={"regex": "EDITED" if M.BASELINE_RE.search(r.get("repo") or "")
                                       else "CLEAN",
                              "meta": {"metadata_arm": "negative_eligible_undeclared",
                                       "metadata_stratum": r.get("stratum"),
                                       "metadata_model_type": r.get("model_type"),
                                       "metadata_eligible": r.get("eligible")}}))

    datasets = []
    if ds_b:
        datasets.append({"dataset": "armB_in_memory_kernels", "examples": ds_b})
    if ds_a:
        datasets.append({"dataset": "armA_hub_checkpoints", "examples": ds_a})
    if ds_n:
        datasets.append({"dataset": "eligible_undeclared_negatives", "examples": ds_n})

    meta = {
        "method_name": "W05w -- sliding-layer-window abliteration weight statistic",
        "baseline_names": ["pooled W05 (the iteration-4 statistic)",
                           f"{len(M.BASELINE_TERMS)}-term repo-name regex"],
        "tau_pooled": TAU, "tau_by_k": tau_by_k, "ks": KS_ALL,
        "tier_completed": s8["tiers"]["tier_completed"],
        "openrouter_spend_usd": 0.0, "n_forward_passes": 0,
        "predictions_sha256": s8["predictions"]["predictions_sha256"],
        "predictions_scorecard": {r["id"]: r["verdict"] for r in s8["predictions"]["results"]},
        "gates": {
            "G1_max_abs_dW05": s8["numbers"]["G1_max_abs_dW05"]["value"],
            "G2_write_matrix_sha256_match": s8["numbers"]["G2_write_matrix_sha256_match"]["value"],
            "G3_kL_max_delta_vs_f64": s8["numbers"]["G3_kL_max_delta_vs_f64"]["value"],
        },
        "headline": s8["numbers"]["armB_pooled_misses_recovered_by_windowing"]["note"],
        "assertion_block": None,
    }
    M.write_json(M.HERE / "method_out.json", {"metadata": meta, "datasets": datasets})
    logger.info(f"method_out.json: {sum(len(d['examples']) for d in datasets)} rows "
                f"in {len(datasets)} datasets")


def run(stages: list[str]) -> None:
    s5 = (stage_s5() if "s5" in stages
          else json.loads((RES / "arm2_frontier_summary.json").read_text()))
    s6 = (stage_s6() if "s6" in stages
          else json.loads((RES / "arm3_subspace.json").read_text()))
    s7 = (stage_s7() if "s7" in stages
          else json.loads((RES / "derivation_summary.json").read_text()))
    if "s8" in stages:
        s8 = stage_s8(s5, s6, s7)
        write_method_out(s5, s6, s7, s8)
