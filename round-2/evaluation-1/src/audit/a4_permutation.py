"""A4 — the n=4 correlations.

SPI rho = -0.20 against supervised baselines +0.40 on four models was reported as
if directional.  With n = 4 there are 4! = 24 orderings, so the smallest
attainable two-sided p is 2/24 = 0.0833: nothing at this panel size can be
significant at 0.05 two-sided.  This module enumerates the exact null.
"""

from __future__ import annotations

from itertools import permutations
from typing import Any

import numpy as np
from loguru import logger

from .common import E1, E3, OUT, dump_json, load_json, spearman_rho

PANEL_MAP = {  # E1 model key -> E3 member key
    "qwen3-0.6b/base": "qwen3_base",
    "qwen3-0.6b/instruct": "qwen3_instruct",
    "qwen3-0.6b/abliterated": "qwen3_abliterated",
    "smollm2/base": "smollm2_base",
}
FLOOR_RATE = 0.05


def spearman_e1(a: list[float], b: list[float]) -> float:
    """E1/build_output.py's OWN spearman, transcribed verbatim.

    It ranks with ``np.argsort(np.argsort(x))``, which breaks ties by ARRAY
    POSITION rather than averaging them.  The archived rho values (-0.20, +0.40)
    are products of this function, so reproducing them requires it.
    """
    pair = [(x, y) for x, y in zip(a, b)
            if x is not None and y is not None and np.isfinite(x) and np.isfinite(y)]
    if len(pair) < 3:
        return float("nan")
    x = np.array([p[0] for p in pair], dtype=float)
    y = np.array([p[1] for p in pair], dtype=float)
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    if rx.std() < 1e-12 or ry.std() < 1e-12:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def exact_spearman_null(x: list[float], y: list[float],
                        rho_fn=spearman_rho) -> dict[str, Any]:
    """Enumerate every permutation of y against x; exact null of Spearman rho."""
    n = len(x)
    obs = rho_fn(x, y)
    null = sorted(rho_fn(x, list(p)) for p in permutations(y))
    a = np.asarray(null)
    n_perm = len(null)
    p_two = float((np.abs(a) >= abs(obs) - 1e-12).sum() / n_perm)
    p_hi = float((a >= obs - 1e-12).sum() / n_perm)
    p_lo = float((a <= obs + 1e-12).sum() / n_perm)
    rho_max = float(a.max())
    p_floor_two = float((np.abs(a) >= rho_max - 1e-12).sum() / n_perm)
    p_floor_one = float((a >= rho_max - 1e-12).sum() / n_perm)
    return {
        "n": n, "n_permutations": n_perm, "rho_observed": obs,
        "p_two_sided_exact": p_two,
        "p_one_sided_greater_exact": p_hi,
        "p_one_sided_less_exact": p_lo,
        "p_floor_two_sided": p_floor_two,
        "p_floor_one_sided": p_floor_one,
        "max_attainable_rho": rho_max,
        "significant_at_0.05_two_sided": bool(p_two < 0.05),
        "any_result_can_be_significant_at_0.05_two_sided": bool(p_floor_two < 0.05),
        "null_distribution_rho": [float(v) for v in null],
    }


def exact_paired_rho_difference(x_a: list[float], x_b: list[float],
                                y: list[float], rho_fn=spearman_rho) -> dict[str, Any]:
    """Exact permutation null of (rho_A - rho_B) over the same 24 orderings of y."""
    obs = rho_fn(x_a, y) - rho_fn(x_b, y)
    null = sorted(rho_fn(x_a, list(p)) - rho_fn(x_b, list(p))
                  for p in permutations(y))
    a = np.asarray(null)
    p_two = float((np.abs(a) >= abs(obs) - 1e-12).sum() / a.size)
    mx = float(np.abs(a).max())
    return {"statistic": "rho_SPI - rho_baseline", "observed": obs,
            "n_permutations": int(a.size), "p_two_sided_exact": p_two,
            "p_floor_two_sided": float((np.abs(a) >= mx - 1e-12).sum() / a.size),
            "max_attainable_abs_difference": mx,
            "significant_at_0.05_two_sided": bool(p_two < 0.05),
            "null_distribution": [float(v) for v in null]}


def run() -> dict[str, Any]:
    raw = load_json(E1 / "out" / "tier0_raw.json")
    an3 = load_json(E3 / "results" / "analysis.json")

    models = sorted(raw["provisional_spi"]["spi_by_model"])
    spi = [raw["provisional_spi"]["spi_by_model"][m] for m in models]
    truth = [raw["ground_truth"][m]["harmful_refusal_rate"]["p"] for m in models]
    dm_auroc = [raw["per_model_meta"][m]["diff_means"]["auroc"] for m in models]
    r0_margin = [raw["per_model_meta"][m]["observable_sanity"]["margin"] for m in models]

    predictors = {
        "SPI_label_free": spi,
        "supervised_diff_means_AUROC": dm_auroc,
        "supervised_r0_margin": r0_margin,
    }
    # PRIMARY: E1's own rank function, so the archived rho values reproduce exactly.
    tests = {k: exact_spearman_null(v, truth, spearman_e1)
             for k, v in predictors.items()}
    paired = {
        f"SPI_minus_{b}": exact_paired_rho_difference(spi, predictors[b], truth,
                                                      spearman_e1)
        for b in ("supervised_diff_means_AUROC", "supervised_r0_margin")}

    # ---- tie sensitivity: E1's rank function breaks ties by ARRAY POSITION ----
    archived = {
        "spearman_spi_vs_harmful_refusal": -0.19999999999999998,
        "spearman_baseline_diffmeans_auroc_vs_harmful_refusal": 0.39999999999999997,
        "spearman_baseline_r0_margin_vs_harmful_refusal": 0.39999999999999997,
    }
    tie_corrected = {k: exact_spearman_null(v, truth, spearman_rho)
                     for k, v in predictors.items()}
    n_tied = len(truth) - len(set(truth))
    tie_block = {
        "archived_values_from_E1_method_out": archived,
        "reproduced_with_E1_rank_function": {
            "SPI": tests["SPI_label_free"]["rho_observed"],
            "diff_means_AUROC": tests["supervised_diff_means_AUROC"]["rho_observed"],
            "r0_margin": tests["supervised_r0_margin"]["rho_observed"]},
        "reproduces_exactly": bool(
            abs(tests["SPI_label_free"]["rho_observed"] - archived[
                "spearman_spi_vs_harmful_refusal"]) < 1e-9
            and abs(tests["supervised_diff_means_AUROC"]["rho_observed"] - archived[
                "spearman_baseline_diffmeans_auroc_vs_harmful_refusal"]) < 1e-9),
        "n_tied_truth_values": n_tied,
        "tied_members": [m for m, t in zip(models, truth)
                         if list(truth).count(t) > 1],
        "tie_corrected_average_rank": {
            k: tie_corrected[k]["rho_observed"] for k in predictors},
        "tie_corrected_exact_tests": tie_corrected,
        "finding": (
            "E1's spearman() ranks with np.argsort(np.argsort(x)), which breaks ties by "
            "ARRAY POSITION instead of averaging them. The harmful refusal rate has a "
            f"TIE: {n_tied + 1} of the 4 members share the value 0.000 "
            "(qwen3-0.6b/abliterated and smollm2/base). The reported rho = -0.20 is "
            "therefore an artefact of the alphabetical order in which those two tied "
            "members happen to sit; with conventional average ranks the same data give "
            f"rho = {tie_corrected['SPI_label_free']['rho_observed']:+.3f}, a SIGN FLIP. "
            "This is a second, independent reason the -0.20 cannot carry a directional "
            "claim, on top of the n = 4 power floor."),
    }

    # ---- (c) incapacity-floor count ---------------------------------------
    e3_gt = {r["member"]: r for r in an3["ground_truth_repaired_scorer"]}
    floor_rows = []
    for m, t in zip(models, truth):
        e3key = PANEL_MAP.get(m)
        e3row = e3_gt.get(e3key, {})
        deg = e3row.get("degenerate_rate_overall")
        rel = e3row.get("reliable_flag")
        unreliable = bool(rel is False) or bool(deg is not None and deg >= 0.30)
        floor_rows.append({
            "model": m, "e3_member": e3key,
            "harmful_refusal_rate_E1": t,
            "at_or_near_refusal_floor": bool(t <= FLOOR_RATE),
            "E3_degenerate_rate_overall": deg,
            "E3_reliable_flag": rel,
            "E3_flagged_unreliable": unreliable,
            "E3_plain_harmful_refusal_repaired_scorer":
                (e3row.get("plain_harmful_refusal") or {}).get("rate"),
            "counts_above_floor": bool(t > FLOOR_RATE and not unreliable),
        })
    n_above = sum(1 for r in floor_rows if r["counts_above_floor"])

    e3_floor = an3.get("incapacity_floor_by_scorer", {}).get("repaired_judge", {})

    # ---- (d) rewrite -------------------------------------------------------
    t_spi = tests["SPI_label_free"]
    t_dm = tests["supervised_diff_means_AUROC"]
    t_r0 = tests["supervised_r0_margin"]
    corrected = (
        f"On this four-model panel SPI did not order the models by measured harmful "
        f"refusal rate (Spearman rho = {t_spi['rho_observed']:.2f}, exact two-sided "
        f"p = {t_spi['p_two_sided_exact']:.3f} over all 4! = 24 orderings). The two "
        f"supervised baselines ordered it no better than chance either "
        f"(diff-in-means AUROC rho = {t_dm['rho_observed']:.2f}, p = "
        f"{t_dm['p_two_sided_exact']:.3f}; r_0 margin rho = {t_r0['rho_observed']:.2f}, "
        f"p = {t_r0['p_two_sided_exact']:.3f}). The smallest two-sided p attainable at "
        f"n = 4 is {t_spi['p_floor_two_sided']:.4f} (one-sided "
        f"{t_spi['p_floor_one_sided']:.4f}), so NO result on this panel - a perfect "
        f"ordering included - could reach 0.05 two-sided. Moreover only "
        f"{n_above} of 4 members sits above the refusal / incapacity floor, so a rank "
        f"correlation here is an instruct-vs-rest contrast, not a graded ranking. Two "
        f"of the four members are TIED at a refusal rate of 0.000, and the -0.20 is "
        f"produced by a rank function that breaks that tie by array position; with "
        f"average ranks the same data give rho = "
        f"{tie_corrected['SPI_label_free']['rho_observed']:+.2f}. No ordering claim, in "
        f"either direction, is supported at this panel size.")

    numbers_to_drop = [
        {"quantity": "SPI Spearman rho = -0.20 vs harmful refusal rate",
         "only_support": "the n=4 rank correlation",
         "recommendation": "REPORT_QUALITATIVELY",
         "why": ("reportable only as 'did not order the panel', never as a negative "
                 "effect size or as evidence that SPI is worse than the baselines")},
        {"quantity": "supervised diff-in-means AUROC rho = +0.40",
         "only_support": "the n=4 rank correlation",
         "recommendation": "REPORT_QUALITATIVELY",
         "why": "exact two-sided p = %.3f, above the 0.083 floor" % t_dm["p_two_sided_exact"]},
        {"quantity": "supervised r_0 margin rho = +0.40",
         "only_support": "the n=4 rank correlation",
         "recommendation": "REPORT_QUALITATIVELY",
         "why": "same panel, same floor"},
        {"quantity": "'both baselines BEAT the label-free method'",
         "only_support": "the sign difference between rho = -0.20 and rho = +0.40",
         "recommendation": "DROP",
         "why": ("the paired exact permutation test of rho_SPI - rho_baseline has "
                 "p_floor = %.3f, so the comparison cannot be significant at any "
                 "outcome" % paired["SPI_minus_supervised_diff_means_AUROC"]["p_floor_two_sided"])},
        {"quantity": "any directional implication drawn from the SPI-vs-baseline gap",
         "only_support": "the n=4 correlation",
         "recommendation": "DROP",
         "why": "three of four members sit at or near the refusal / incapacity floor"},
    ]

    out = {
        "analysis": "A4_n4_correlations",
        "defect": ("SPI rho = -0.20 vs supervised baselines +0.40 on four models is "
                   "reported as if directional, and a one-directional implication is "
                   "drawn from it"),
        "panel": models,
        "values": {"spi": dict(zip(models, spi)),
                   "harmful_refusal_rate": dict(zip(models, truth)),
                   "diff_means_auroc": dict(zip(models, dm_auroc)),
                   "r0_margin": dict(zip(models, r0_margin))},
        "rank_function": ("E1/build_output.py spearman(), transcribed verbatim "
                          "(argsort ranks, ties broken by array position)"),
        "exact_permutation_tests": tests,
        "paired_rho_difference_tests": paired,
        "tie_sensitivity": tie_block,
        "p_floor_two_sided": t_spi["p_floor_two_sided"],
        "p_floor_one_sided": t_spi["p_floor_one_sided"],
        "no_result_can_be_significant_at_n4": not t_spi[
            "any_result_can_be_significant_at_0.05_two_sided"],
        "incapacity_floor": {
            "floor_rate_threshold": FLOOR_RATE,
            "per_member": floor_rows,
            "n_above_floor": n_above,
            "n_effective": n_above + 1 if n_above < 4 else 4,
            "n_effective_definition": ("members above the floor plus the pooled "
                                       "at-floor group they are contrasted against"),
            "E3_incapacity_floor_block": e3_floor,
            "statement": (
                f"n_above_floor = {n_above} of 4. A rank correlation over a panel where "
                f"{4 - n_above} of 4 members sit at or near the refusal / incapacity "
                "floor is an instruct-vs-rest contrast, not a graded ranking: the "
                "at-floor members have no measurable rank ordering among themselves, so "
                "the correlation is determined almost entirely by where the one "
                "above-floor member lands."),
        },
        "corrected_claim_text": corrected,
        "numbers_to_drop": numbers_to_drop,
    }
    dump_json(OUT / "a4_permutation.json", out)
    logger.info(f"A4: rho_SPI={t_spi['rho_observed']:.3f} p2={t_spi['p_two_sided_exact']:.4f} "
                f"floor={t_spi['p_floor_two_sided']:.4f}; n_above_floor={n_above}")
    return out
