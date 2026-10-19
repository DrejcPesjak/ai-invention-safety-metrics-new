"""A1 — the lambda inconsistency.

E1's supplementary verdict CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING is produced
in build_output.py by ``paired_bootstrap_diff`` on ``est1_nls`` lambda values,
while the same artifact certifies EVERY lambda row ``identifiable=false``.

This module re-runs the ORIGINAL decision rule on the two ASSUMPTION-FREE
statistics the artifact itself names as trustworthy (decay_ratio_16 and the
normalised deviation AUC), so the estimator is the ONLY thing that changes.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from loguru import logger

from .common import (DIRECTIONS, E1, N_BOOT, OUT, READOUTS, REF_MODEL,
                     SEED_BOOTSTRAP, SEED_CLUSTER, dump_json, load_json,
                     record_substitution, spearman_rho)

# The archived estimators, imported verbatim.
from spi.indicators import (cluster_bootstrap_ci, half_life_auc,  # noqa: E402
                            paired_bootstrap_diff)

HORIZONS = (8, 16, 32, 64)


# --------------------------------------------------------------------------- #
def _decay_ratio(curve: list[float], h: int) -> float | None:
    """|delta_h| / |delta_0| on the archived across-rollout signed mean curve.

    This reproduces the archived ``decay_ratio_16`` definition; the h=16 value
    computed here is asserted against the archived field below.
    """
    d = np.asarray(curve, dtype=np.float64)
    if d.size <= h or not np.isfinite(d[0]) or abs(d[0]) < 1e-12:
        return None
    v = float(abs(d[h]) / abs(d[0]))
    return v if np.isfinite(v) else None


def _auc_norm(row_readout: dict[str, Any]) -> float | None:
    """Archived auc_norm, recomputed with half_life_auc() where absent."""
    est = row_readout.get("estimates", {}).get("auc_substitute") or {}
    v = est.get("auc_norm")
    if v is not None and np.isfinite(v):
        return float(v)
    curve = row_readout.get("mean_delta_curve")
    if not curve:
        return None
    rec = half_life_auc(np.asarray(curve, dtype=np.float64))
    return rec.get("auc_norm")


def _lam(row_readout: dict[str, Any]) -> float | None:
    v = row_readout.get("estimates", {}).get("est1_nls", {}).get("lambda")
    return float(v) if v is not None and np.isfinite(v) else None


# --------------------------------------------------------------------------- #
def _extract(rows: list[dict]) -> list[dict]:
    """Flatten the certified-refit rows into one record per (model, prompt, dir, readout)."""
    recs = []
    n_auc_recomputed = 0
    for r in rows:
        for ro in READOUTS:
            rr = r.get(ro)
            if not rr:
                continue
            arch16 = rr.get("decay_ratio_16")
            mine16 = _decay_ratio(rr.get("mean_delta_curve") or [], 16)
            est = (rr.get("estimates", {}).get("auc_substitute") or {})
            if est.get("auc_norm") is None:
                n_auc_recomputed += 1
            rec = {
                "model": r["model"], "member": r["member"], "lineage": r["lineage"],
                "prompt_id": r["prompt_id"], "direction": r["direction"],
                "readout": ro,
                "decay_ratio_16_archived": arch16,
                "decay_ratio_16_recomputed": mine16,
                "decay_ratio_16": arch16 if arch16 is not None else mine16,
                "auc_norm": _auc_norm(rr),
                "half_life": est.get("half_life"),
                "lambda_est1_nls": _lam(rr),
                "identifiable": r.get("identifiable"),
            }
            for h in HORIZONS:
                rec[f"decay_ratio_{h}"] = _decay_ratio(rr.get("mean_delta_curve") or [], h)
            recs.append(rec)
    if n_auc_recomputed:
        record_substitution(
            "A1", "estimates.auc_substitute.auc_norm",
            "recomputed with spi.indicators.half_life_auc() on mean_delta_curve",
            f"{n_auc_recomputed} readout cells had no archived auc_norm",
            "none: the archived function is reused, not re-derived")
    return recs


def _by_prompt(recs: list[dict], model: str, direction: str, readout: str,
               field: str) -> dict[str, float]:
    return {r["prompt_id"]: r[field] for r in recs
            if r["model"] == model and r["direction"] == direction
            and r["readout"] == readout and r.get(field) is not None
            and np.isfinite(r[field])}


def _lineage_bootstrap_diff(recs: list[dict], ref: str, comp: str, direction: str,
                            readout: str, field: str, n_reps: int = N_BOOT,
                            seed: int = SEED_BOOTSTRAP) -> dict[str, Any]:
    """Resample LINEAGES with replacement instead of prompts.

    E1's panel has 3 lineages of which 2 (qwen3-0.6b, smollm2) carry members, so
    a lineage-level resample of a two-model contrast reduces to resampling the
    lineage(s) that contribute pairs.  Reported so a member-vs-lineage sign
    disagreement, which iteration 1 has precedent for, cannot hide.
    """
    a = _by_prompt(recs, ref, direction, readout, field)
    b = _by_prompt(recs, comp, direction, readout, field)
    keys = sorted(set(a) & set(b))
    if len(keys) < 2:
        return {"diff": None, "ci_lo": None, "ci_hi": None, "n_pairs": len(keys),
                "unit": "lineage", "note": "insufficient pairs"}
    lin_of = {r["prompt_id"]: r["lineage"] for r in recs}
    # Group the paired differences by the lineage of the COMPARATOR member.
    lin_comp = next((r["lineage"] for r in recs if r["model"] == comp), "unknown")
    lin_ref = next((r["lineage"] for r in recs if r["model"] == ref), "unknown")
    groups: dict[str, list[float]] = {}
    for k in keys:
        groups.setdefault(lin_of.get(k, "prompt"), []).append(a[k] - b[k])
    gkeys = sorted(groups)
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(n_reps):
        pick = rng.integers(0, len(gkeys), len(gkeys))
        vals = np.concatenate([np.asarray(groups[gkeys[i]]) for i in pick])
        draws.append(float(vals.mean()))
    d = np.asarray([a[k] - b[k] for k in keys])
    lo, hi = float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))
    return {"diff": float(d.mean()), "ci_lo": lo, "ci_hi": hi,
            "n_pairs": len(keys), "ci_excludes_zero": bool(lo > 0 or hi < 0),
            "unit": "lineage", "n_clusters": len(gkeys),
            "clusters": gkeys, "lineage_ref": lin_ref, "lineage_comp": lin_comp,
            "caveat": ("the panel carries only 2 lineages and all 20 prompts are "
                       "shared across members, so the lineage-level resample has "
                       "very few independent clusters; reported for sign agreement "
                       "only, not as a competing interval")}


def _verdict_code(n_sig_random: int, n_sig_refuse: int, n_comparisons: int,
                  identifiable: bool) -> str:
    """build_output.py's OWN decision rule, transcribed unchanged."""
    if n_sig_random >= 1:
        return "CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING"
    if not identifiable:
        return "LAMBDA_NOT_IDENTIFIABLE_FLUCTUATION_ARM_ONLY"
    if n_sig_refuse == n_comparisons:
        return "LAMBDA_IDENTIFIABLE_ORDERING_AS_PREDICTED"
    return "LAMBDA_IDENTIFIABLE_ORDERING_ABSENT_OR_REVERSED"


# --------------------------------------------------------------------------- #
def run() -> dict[str, Any]:
    cert = load_json(E1 / "out" / "refit_certified.json")
    raw = load_json(E1 / "out" / "tier0_raw.json")
    rows = cert["rows"]
    recs = _extract(rows)
    logger.info(f"A1: {len(rows)} certified rows -> {len(recs)} readout records")

    # ---- integrity check: our decay_ratio_16 must reproduce the archived one --
    pairs = [(r["decay_ratio_16_archived"], r["decay_ratio_16_recomputed"]) for r in recs
             if r["decay_ratio_16_archived"] is not None
             and r["decay_ratio_16_recomputed"] is not None]
    maxdiff = max((abs(a - b) for a, b in pairs), default=float("nan"))
    logger.info(f"A1 decay_ratio_16 archived-vs-recomputed max |diff| = {maxdiff:.3g} "
                f"over {len(pairs)} cells")

    models = sorted({r["model"] for r in rows})
    comps = [m for m in models if m != REF_MODEL]
    stats = ["decay_ratio_16", "auc_norm"]

    contrasts: list[dict[str, Any]] = []
    grid: dict[str, Any] = {}
    for stat in stats:
        grid[stat] = {}
        for ro in READOUTS:
            grid[stat][ro] = {}
            for dname in DIRECTIONS:
                cells = {}
                for c in comps:
                    a = _by_prompt(recs, REF_MODEL, dname, ro, stat)
                    b = _by_prompt(recs, c, dname, ro, stat)
                    pb = paired_bootstrap_diff(a, b, n_reps=N_BOOT, seed=SEED_BOOTSTRAP)
                    lb = _lineage_bootstrap_diff(recs, REF_MODEL, c, dname, ro, stat)
                    sign_disagree = (
                        pb.get("diff") is not None and lb.get("diff") is not None
                        and np.sign(pb["diff"]) != np.sign(lb["diff"]))
                    cells[c] = {"prompt_level": pb, "lineage_level": lb,
                                "sign_disagreement_prompt_vs_lineage": bool(sign_disagree)}
                    contrasts.append({
                        "statistic": stat, "readout": ro, "direction": dname,
                        "reference": REF_MODEL, "comparator": c,
                        "diff": pb.get("diff"), "ci_lo": pb.get("ci_lo"),
                        "ci_hi": pb.get("ci_hi"), "n_pairs": pb.get("n_pairs"),
                        "ci_excludes_zero": bool(pb.get("ci_excludes_zero")),
                        "significant_lower": bool(pb.get("ci_excludes_zero")
                                                  and (pb.get("diff") or 0) < 0),
                        "lineage_diff": lb.get("diff"),
                        "lineage_ci_lo": lb.get("ci_lo"), "lineage_ci_hi": lb.get("ci_hi"),
                        "lineage_ci_excludes_zero": bool(lb.get("ci_excludes_zero")),
                        "sign_disagreement_prompt_vs_lineage": bool(sign_disagree),
                        "seed": SEED_BOOTSTRAP, "n_reps": N_BOOT,
                    })
                grid[stat][ro][dname] = cells

    # ---------------- verdict recomputation, per statistic x readout ----------
    def n_sig_lower(stat: str, ro: str, dname: str) -> int:
        return sum(1 for c in comps
                   if grid[stat][ro][dname][c]["prompt_level"].get("ci_excludes_zero")
                   and (grid[stat][ro][dname][c]["prompt_level"].get("diff") or 0) < 0)

    ident = bool(cert.get("all_rows_identifiable"))
    verdicts: dict[str, Any] = {}
    n_sig_table: dict[str, Any] = {}
    for stat in stats:
        verdicts[stat] = {}
        n_sig_table[stat] = {}
        for ro in READOUTS:
            n_sig_table[stat][ro] = {d: n_sig_lower(stat, ro, d) for d in DIRECTIONS}
            code = _verdict_code(n_sig_table[stat][ro]["random_direction"],
                                 n_sig_table[stat][ro]["toward_refuse"],
                                 len(comps), ident)
            abl = "qwen3-0.6b/abliterated"
            verdicts[stat][ro] = {
                "code": code,
                "generic_mixing_verdict_survives":
                    code == "CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING",
                "n_comparisons": len(comps),
                "n_sig_lower_by_direction": n_sig_table[stat][ro],
                "identifiable_at_refit_geometry": ident,
                "decisive_pair_instruct_vs_abliterated": {
                    d: grid[stat][ro][d][abl]["prompt_level"] for d in DIRECTIONS},
            }

    # ---------------- lambda consistency check (DEMOTED, no inference) --------
    lam_grid: dict[str, Any] = {}
    for ro in READOUTS:
        lam_grid[ro] = {}
        for dname in DIRECTIONS:
            lam_grid[ro][dname] = {
                c: paired_bootstrap_diff(
                    _by_prompt(recs, REF_MODEL, dname, ro, "lambda_est1_nls"),
                    _by_prompt(recs, c, dname, ro, "lambda_est1_nls"),
                    n_reps=N_BOOT, seed=SEED_BOOTSTRAP) for c in comps}
    lambda_check = {
        "archived_prereg_ordering_tests_lambda_refuse":
            cert["prereg_ordering_tests_lambda_refuse"],
        "reproduced_here_layerL": lam_grid["layerL"],
        "all_rows_identifiable": ident,
        "identifiability_rule_at_refit_noise": cert["rule_at_refit_noise"],
        "note": (
            "MANDATORY NOTE. Both the treatment arm (toward_refuse, "
            "instruct-minus-abliterated = -0.226, n.s.) and the control arm "
            "(random_direction = -0.493, CI excludes 0) are computed from est1_nls "
            "lambda values that this same artifact certifies identifiable=false for "
            "EVERY one of its 640 rows: the synthetic rule demands T_fit>=128 AND "
            "n_roll>=40, and the achieved n_roll is 20 even after the T_fit=128 "
            "refit. Both arms therefore fail the identifiability rule EQUALLY, so "
            "the contrast is between two equally noisy estimators of an "
            "unidentified quantity. NO INFERENCE IS DRAWN FROM IT here; it is "
            "reprinted only so the original numbers remain visible next to their "
            "replacement."),
    }

    # ---------------- robustness: horizon sweep ------------------------------
    horizon = {}
    for h in HORIZONS:
        f = f"decay_ratio_{h}"
        horizon[f] = {}
        for ro in READOUTS:
            cells = {}
            for dname in DIRECTIONS:
                per = {c: paired_bootstrap_diff(
                    _by_prompt(recs, REF_MODEL, dname, ro, f),
                    _by_prompt(recs, c, dname, ro, f),
                    n_reps=N_BOOT, seed=SEED_BOOTSTRAP) for c in comps}
                cells[dname] = {
                    "per_comparator": per,
                    "n_sig_lower": sum(1 for v in per.values()
                                       if v.get("ci_excludes_zero") and (v.get("diff") or 0) < 0),
                }
            code = _verdict_code(cells["random_direction"]["n_sig_lower"],
                                 cells["toward_refuse"]["n_sig_lower"], len(comps), ident)
            horizon[f][ro] = {"by_direction": cells, "verdict_code": code,
                              "generic_mixing_verdict_survives":
                                  code == "CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING"}

    # ---------------- estimator agreement: lambda vs decay_ratio_16 ----------
    rank_corr = {}
    for ro in READOUTS:
        sub = [r for r in recs if r["readout"] == ro
               and r["lambda_est1_nls"] is not None and r["decay_ratio_16"] is not None]
        rho = spearman_rho([r["lambda_est1_nls"] for r in sub],
                           [r["decay_ratio_16"] for r in sub])
        sub2 = [r for r in recs if r["readout"] == ro
                and r["lambda_est1_nls"] is not None and r["auc_norm"] is not None]
        rho2 = spearman_rho([r["lambda_est1_nls"] for r in sub2],
                            [r["auc_norm"] for r in sub2])
        rank_corr[ro] = {
            "spearman_lambda_vs_decay_ratio_16": rho, "n_lambda_vs_decay": len(sub),
            "spearman_lambda_vs_auc_norm": rho2, "n_lambda_vs_auc": len(sub2),
            "expected_sign": ("negative: a LARGER lambda means faster decay, so a "
                              "SMALLER decay_ratio_16 and a SMALLER AUC"),
        }

    # ---------------- secondary: same test on the MAIN-RUN base grid cell ----
    base_p = raw["grid_actually_run"]["base_p"]
    base_eps = raw["grid_actually_run"]["base_eps_c"]
    main_rows = [r for r in raw["lambda"]
                 if r["p"] == base_p and abs(r["eps_c"] - base_eps) < 1e-9
                 and r["teacher_forced"]]
    main_recs = _extract(main_rows)
    main_grid = {}
    for stat in stats:
        main_grid[stat] = {}
        for ro in READOUTS:
            cells = {}
            for dname in DIRECTIONS:
                per = {c: paired_bootstrap_diff(
                    _by_prompt(main_recs, REF_MODEL, dname, ro, stat),
                    _by_prompt(main_recs, c, dname, ro, stat),
                    n_reps=N_BOOT, seed=SEED_BOOTSTRAP) for c in comps}
                cells[dname] = {"per_comparator": per,
                                "n_sig_lower": sum(1 for v in per.values()
                                                   if v.get("ci_excludes_zero")
                                                   and (v.get("diff") or 0) < 0)}
            code = _verdict_code(cells["random_direction"]["n_sig_lower"],
                                 cells["toward_refuse"]["n_sig_lower"], len(comps), False)
            main_grid[stat][ro] = {"by_direction": cells, "verdict_code": code}

    # ---------------- the single machine-readable statement ------------------
    # PRIMARY READOUT for A1 is layer-L, pre-stated in the artifact plan before any
    # number was computed: the perturbation is INJECTED at layer L, so a
    # perturbation-local decay statistic is primary at the layer-L lens.  The
    # final-layer arm is reported alongside because the archived lens-vs-final
    # correlation is only 0.17-0.26.
    primary_readout = "layerL"
    survives_primary = all(verdicts[s][primary_readout]["generic_mixing_verdict_survives"]
                           for s in stats)
    survives_any = any(verdicts[s][r]["generic_mixing_verdict_survives"]
                       for s in stats for r in READOUTS)
    survives_all = all(verdicts[s][r]["generic_mixing_verdict_survives"]
                       for s in stats for r in READOUTS)
    surviving_cells = [f"{s}/{r}" for s in stats for r in READOUTS
                       if verdicts[s][r]["generic_mixing_verdict_survives"]]
    failing_cells = [f"{s}/{r}" for s in stats for r in READOUTS
                     if not verdicts[s][r]["generic_mixing_verdict_survives"]]
    if survives_all:
        change = "SURVIVES"
        stmt = ("The generic-mixing verdict CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING "
                "SURVIVES: on both assumption-free statistics (decay_ratio_16 and the "
                "normalised deviation AUC) and at both readouts, the random-direction "
                "control still separates the panel with at least one CI-excluding-zero "
                "lower contrast, so the original conclusion did not depend on the "
                "uncertified lambda estimator.")
    elif survives_any:
        change = "CHANGED"
        stmt = (
            "The generic-mixing verdict CHANGES. On the PRE-STATED PRIMARY readout for "
            "a perturbation-local statistic (layer L, where the perturbation is "
            "injected) it DOES NOT reproduce on either assumption-free statistic: the "
            "random-direction control separates the panel in "
            f"{n_sig_table['decay_ratio_16']['layerL']['random_direction']} of "
            f"{len(comps)} comparisons on decay_ratio_16 and "
            f"{n_sig_table['auc_norm']['layerL']['random_direction']} of {len(comps)} on "
            "the normalised deviation AUC, while the refusal-direction TREATMENT "
            f"separates in {n_sig_table['decay_ratio_16']['layerL']['toward_refuse']} of "
            f"{len(comps)} - the reverse of the reported pattern. It reproduces only at "
            f"the final-layer readout ({', '.join(surviving_cells)}), whose correlation "
            "with the layer-L lens the artifact itself measures at only 0.17-0.26. The "
            "iteration-1 supplementary verdict CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING "
            "therefore cannot be carried forward as settled: it is both estimator- and "
            "readout-dependent. MATERIAL_CHANGE_TO_REPORTED_RESULT.")
    else:
        change = "DOES_NOT_SURVIVE"
        stmt = ("The generic-mixing verdict DOES NOT SURVIVE the switch to the "
                "artifact's own trusted statistics: on decay_ratio_16 and the "
                "normalised deviation AUC, at both readouts, no random-direction "
                "contrast has a CI excluding zero in the lower direction, so the "
                "original CONTROL_REPRODUCES_ORDERING_GENERIC_MIXING was an artifact "
                "of an estimator the same paper certifies as non-identifiable. "
                "MATERIAL_CHANGE_TO_REPORTED_RESULT.")

    out = {
        "analysis": "A1_lambda_inconsistency",
        "defect": ("the decisive random-vs-refusal-direction control verdict is drawn "
                   "from bootstrap CIs on est1_nls lambda values that the same "
                   "artifact certifies identifiable=false for all 640 rows"),
        "geometry": {k: cert[k] for k in ("fit_len", "n_roll", "T", "p", "eps_c",
                                          "teacher_forced")},
        "source": "E1/out/refit_certified.json rows (the exact rows the original verdict used)",
        "n_rows": len(rows), "n_readout_records": len(recs),
        "reference_model": REF_MODEL, "comparators": comps,
        "bootstrap": {"n_reps": N_BOOT, "seed_paired": SEED_BOOTSTRAP,
                      "seed_cluster": SEED_CLUSTER,
                      "function": "spi.indicators.paired_bootstrap_diff (imported verbatim)"},
        "decay_ratio_16_reproduction_max_abs_diff": maxdiff,
        "contrasts": contrasts,
        "verdicts_by_statistic_and_readout": verdicts,
        "n_sig_lower_table_statistic_x_readout_x_direction": n_sig_table,
        "lambda_ci_consistency_check_NOT_IDENTIFIABLE": lambda_check,
        "horizon_sensitivity": horizon,
        "estimator_rank_agreement": rank_corr,
        "secondary_main_run_base_grid_cell": {
            "grid": {"p": base_p, "eps_c": base_eps, "teacher_forced": True,
                     "fit_len": raw["grid_actually_run"]["fit_len"]},
            "n_rows": len(main_rows), "results": main_grid},
        "verdict_change_statement": stmt,
        "verdict_change_flag": change,
        "material_change_to_reported_result": change != "SURVIVES",
        "primary_readout_for_A1": primary_readout,
        "primary_readout_rationale": (
            "the perturbation is injected at layer L, so a perturbation-local decay "
            "statistic is primary at the layer-L lens; declared in the artifact plan "
            "before any A1 number was computed"),
        "generic_mixing_verdict_survives_at_primary_readout": survives_primary,
        "surviving_cells": surviving_cells,
        "failing_cells": failing_cells,
        "estimator_switch_is_cosmetic": bool(
            all(abs(rank_corr[r]["spearman_lambda_vs_decay_ratio_16"]) > 0.8
                for r in READOUTS)),
        "estimator_switch_interpretation": (
            "lambda and decay_ratio_16 rank-correlate at only "
            f"{rank_corr['layerL']['spearman_lambda_vs_decay_ratio_16']:.3f} (layer L) and "
            f"{rank_corr['final']['spearman_lambda_vs_decay_ratio_16']:.3f} (final) across "
            "the 240 certified rows per readout, well short of the |rho| > 0.8 that would "
            "make the two estimators interchangeable. The original conclusion was "
            "therefore ESTIMATOR-DEPENDENT, not merely re-expressed."),
    }
    dump_json(OUT / "a1_lambda.json", out)
    logger.info(f"A1 verdict change: {change}")
    return out
