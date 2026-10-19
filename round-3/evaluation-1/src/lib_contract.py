#!/usr/bin/env python3
"""The analysis contract. Printed and echoed into numbers.json BEFORE any number.

Nothing in this module reads data. It only declares, in one place, every
analytic choice that the recomputation makes, so that a reader can check the
choices against the numbers rather than reverse-engineer them.
"""

from __future__ import annotations

import os as _os

# The production values. A smoke run may shrink them via the AII_* environment
# variables below; whatever is actually used is echoed into numbers.json's
# contract block, so a shrunken run can never be mistaken for a full one.
SEED = 20260813
B_BOOT = int(_os.environ.get("AII_B_BOOT", 10000))
B_POWER = int(_os.environ.get("AII_B_POWER", 2000))
N_POWER_SIMS = int(_os.environ.get("AII_N_POWER_SIMS", 2000))
N_POWER_SIMS_NSWEEP = int(_os.environ.get("AII_N_POWER_SIMS_NSWEEP", 400))
SKIP_JUDGE = _os.environ.get("AII_SKIP_JUDGE", "0") == "1"

JUDGE_MODEL = "google/gemini-3.1-flash-lite"
JUDGE_TEMPERATURE = 0.0
JUDGE_HARD_STOP_USD = 0.90

TOL_RHO = 0.005      # absolute tolerance for rho / AUROC comparisons
TOL_CI = 0.01        # absolute tolerance for CI bounds

# The seven white-box candidates the falsifier is stated over. metric_spec.py
# declares 53 metrics and NO candidate list, so this set is an ANALYSIS-TIME
# choice made here, not a pre-registered one. It is the union of the five
# abliteration-scar weight metrics' two behavioural leads (W01, W04), the three
# activation quantities the draft quotes (A01, A02, A22) and the two remaining
# scar metrics that the draft reports behaviourally (W02, W05).
SEVEN_WHITEBOX = [
    "W01_abl_suppression_depth",
    "W02_abl_direction_consistency",
    "W04_abl_isolation",
    "W05_abl_min_layer_energy",
    "A01_ams_sigma",
    "A02_ams_concept_cosine",
    "A22_alpha_50",
]

WEIGHT_SCAR = ["W01_abl_suppression_depth", "W02_abl_direction_consistency",
               "W03_abl_gap_vs_random", "W04_abl_isolation",
               "W05_abl_min_layer_energy"]

BASELINE_POSTHOC = "B09_greedy_refusal_rate_harmful"
BASELINE_PRESPEC = "B01_logit_gap_harmful"

TARGETS = ["harmful_refusal_rate", "xstest_overrefusal_rate"]

CONTRACT = {
    "seed": SEED,
    "rng": "numpy.random.default_rng(seed); one generator per bootstrap family, "
           "each generator's seed is logged in numbers.json under contract.rng_seeds",
    "B_bootstrap": B_BOOT,
    "B_power": B_POWER,
    "n_power_sims": N_POWER_SIMS,
    "resampling_scheme": (
        "Cluster bootstrap over LINEAGES: at each of the B resamples, n_lineage "
        "lineages are drawn WITH replacement, where n_lineage equals the observed "
        "number of eligible lineages for that cell, and every member of a drawn "
        "lineage is carried into the resample (a lineage drawn twice contributes "
        "all of its members twice)."
    ),
    "singleton_rule": (
        "Of the 23 lineages on the panel, 9 contribute exactly one member. A "
        "singleton contributes its single member whenever it is drawn, contributes "
        "zero within-cluster variance, and is NEVER dropped. Degenerate resamples "
        "(a resample in which the statistic is undefined -- fewer than 4 distinct "
        "usable members, a constant metric column, or, for AUROC, all members of "
        "one class) are REDRAWN with a fresh draw, capped at 100 attempts; the "
        "count of redraws and of resamples abandoned after 100 attempts is reported."
    ),
    "spearman_tie_handling": (
        "RANK-AVERAGE, explicitly: scipy.stats.rankdata(method='average') on each "
        "vector, then Pearson on the ranks. NOT position-based tie-breaking. "
        "Reason, stated because it is load-bearing rather than pedantic: this "
        "project's own iteration-1 re-analysis found that position-based tie "
        "breaking FLIPPED the sign of a reported correlation, from rho = -0.20 to "
        "rho = +0.105."
    ),
    "auroc_tie_convention": (
        "AUROC = Mann-Whitney U / (n_pos * n_neg) computed from rank-average ranks, "
        "so an exact tie between a positive and a negative is credited 0.5. The "
        "number of tied (positive, negative) pairs actually encountered is reported "
        "for every AUROC."
    ),
    "base_model_exclusion": (
        "Members with member_class == 'base' use the PLAIN renderer, so their "
        "behavioural readout is not comparable to the chat-rendered members. They "
        "are EXCLUDED from every behaviour correlation (Sec 5.2, paired "
        "differences, power, attenuation) and INCLUDED in the weights-arm AUROC "
        "(Sec 5.1), which touches no behavioural number. The surviving n is printed "
        "at every table."
    ),
    "nan_policy": (
        "PAIRWISE DELETION. A22_alpha_50 is null on 37/44 members and "
        "A18_decision_depth on 22/44. A cell is computed over the members for which "
        "BOTH the metric and the target are present; that n is printed for every "
        "cell and is never silently absorbed. A cell with fewer than 4 usable "
        "members is reported as UNRECOMPUTABLE rather than as a number."
    ),
    "aggregation_units": (
        "MEMBER level (one row per checkpoint) and LINEAGE level (one row per "
        "lineage, the metric and the target each averaged over that lineage's "
        "eligible members). Both are reported for every cell; the lineage is the "
        "resampling unit at both levels."
    ),
    "ci_method": "percentile bootstrap, 2.5th and 97.5th percentiles of the resample distribution",
    "no_new_inference": (
        "No model weights are loaded and no forward pass is run anywhere in this "
        "artifact. The only new compute that leaves the machine is LLM re-judging "
        "of ALREADY-ARCHIVED generations, cached and capped."
    ),
    "seven_whitebox_candidates": SEVEN_WHITEBOX,
    "seven_whitebox_provenance": (
        "ANALYSIS-TIME choice made in lib_contract.py. metric_spec.py declares 53 "
        "metrics and no candidate list, no falsifier and no analysis plan, so this "
        "set is NOT pre-registered and must not be described as such."
    ),
    "baseline_posthoc": BASELINE_POSTHOC,
    "baseline_prespecified": BASELINE_PRESPEC,
}
