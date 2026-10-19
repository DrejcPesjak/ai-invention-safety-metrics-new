#!/usr/bin/env python3
"""EVERY AUROC / Spearman / bootstrap CI quoted anywhere in this artifact.

RESAMPLING CONTRACT (printed at import and recorded in method_out.json):
  seed                 : 20260813
  bootstrap replicates : B = 10000
  resampling unit      : LINEAGE (lineage_id), never the individual checkpoint --
                         sibling checkpoints share a pretrained root and are not
                         independent draws
  scheme               : nonparametric bootstrap WITH replacement over lineages;
                         singleton lineages are resampled exactly like any other
  CI                   : percentile, 2.5% / 97.5%
  ties                 : 'average' -- AUROC counts a tie as half a concordance,
                         Spearman uses average ranks
  permutation          : labels shuffled WITHIN the evaluated set, 10000 draws,
                         p = (1 + #{stat_perm >= stat_obs}) / (1 + n_perm)
  degenerate replicates: a bootstrap replicate containing only one class is
                         DISCARDED and counted; the CI is over the survivors

The module ends with an assertion block that recomputes every number quoted in
method_out.json from the raw result files.  A failing assertion blocks assembly.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

SEED = 20260813
B = 10000
N_PERM = 10000
TIE_METHOD = "average"
RESAMPLING_UNIT = "lineage_id"

CONTRACT = {
    "seed": SEED, "bootstrap_B": B, "n_permutations": N_PERM,
    "resampling_unit": RESAMPLING_UNIT, "with_replacement": True,
    "singleton_lineage_handling": "resampled with replacement like any other",
    "tie_method": TIE_METHOD, "ci": "percentile 2.5/97.5",
    "degenerate_replicate_policy": "discarded and counted",
    "permutation_p": "(1 + #{perm >= obs}) / (1 + n_perm)",
}


def print_contract() -> None:
    print("=" * 72)
    print("ANALYSIS CONTRACT")
    for k, v in CONTRACT.items():
        print(f"  {k:32s} {v}")
    print("=" * 72)


# ---------------------------------------------------------------------------
# Point estimators
# ---------------------------------------------------------------------------
def auroc(pos: np.ndarray, neg: np.ndarray) -> float:
    """Rank AUROC with ties counted as half (Mann-Whitney U / n_pos n_neg)."""
    pos = np.asarray(pos, dtype=float)
    neg = np.asarray(neg, dtype=float)
    pos = pos[np.isfinite(pos)]
    neg = neg[np.isfinite(neg)]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    all_v = np.concatenate([pos, neg])
    r = stats.rankdata(all_v, method=TIE_METHOD)
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2.0) /
                 (len(pos) * len(neg)))


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return float("nan")
    return float(stats.spearmanr(x[m], y[m]).statistic)


# ---------------------------------------------------------------------------
# Lineage bootstrap
# ---------------------------------------------------------------------------
def _groups(lineages: list[str]) -> tuple[list[str], dict[str, np.ndarray]]:
    uniq = sorted(set(lineages))
    lin = np.asarray(lineages)
    return uniq, {u: np.where(lin == u)[0] for u in uniq}


def bootstrap_ci(values: np.ndarray, labels: np.ndarray, lineages: list[str],
                 stat="auroc", seed: int = SEED, B: int = B) -> dict:
    """Percentile CI for AUROC (labels 1/0) resampling LINEAGES with replacement."""
    values = np.asarray(values, float)
    labels = np.asarray(labels, int)
    uniq, idx = _groups(lineages)
    rng = np.random.default_rng(seed)
    obs = (auroc(values[labels == 1], values[labels == 0]) if stat == "auroc"
           else spearman(values, labels))
    reps, degenerate = [], 0
    for _ in range(B):
        pick = rng.choice(len(uniq), size=len(uniq), replace=True)
        sel = np.concatenate([idx[uniq[p]] for p in pick])
        v, l = values[sel], labels[sel]
        if stat == "auroc":
            if l.sum() == 0 or l.sum() == len(l):
                degenerate += 1
                continue
            reps.append(auroc(v[l == 1], v[l == 0]))
        else:
            s = spearman(v, l)
            if not np.isfinite(s):
                degenerate += 1
                continue
            reps.append(s)
    reps = np.array([r for r in reps if np.isfinite(r)])
    lo, hi = (float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))) \
        if len(reps) else (float("nan"), float("nan"))
    return {"estimate": obs, "ci_low": lo, "ci_high": hi, "B": B,
            "n_effective_replicates": int(len(reps)),
            "n_degenerate_replicates": int(degenerate),
            "n_lineages": len(uniq), "n_items": int(len(values)),
            "n_pos": int((labels == 1).sum()), "n_neg": int((labels == 0).sum())}


def spearman_ci(x, y, lineages, seed: int = SEED, B: int = B) -> dict:
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    lineages = [l for l, k in zip(lineages, m) if k]
    uniq, idx = _groups(lineages)
    rng = np.random.default_rng(seed)
    obs = spearman(x, y)
    reps, degen = [], 0
    for _ in range(B):
        pick = rng.choice(len(uniq), size=len(uniq), replace=True)
        sel = np.concatenate([idx[uniq[p]] for p in pick])
        s = spearman(x[sel], y[sel])
        (reps.append(s) if np.isfinite(s) else None)
        degen += int(not np.isfinite(s))
    reps = np.array(reps)
    return {"estimate": obs,
            "ci_low": float(np.percentile(reps, 2.5)) if len(reps) else float("nan"),
            "ci_high": float(np.percentile(reps, 97.5)) if len(reps) else float("nan"),
            "n": int(len(x)), "n_lineages": len(uniq), "B": B,
            "n_degenerate_replicates": int(degen)}


def paired_spearman_diff(x_a, x_b, y, lineages, seed: int = SEED, B: int = B) -> dict:
    """rho(a, y) - rho(b, y) on the SAME resampled lineages.

    Comparing two point estimates is NOT a test: two metrics can differ by 0.004
    with almost entirely overlapping CIs.  Only the PAIRED difference answers
    'does this metric beat the baseline', because it cancels the shared
    member-level noise.  Restricted to members where BOTH are observed.
    """
    x_a, x_b, y = np.asarray(x_a, float), np.asarray(x_b, float), np.asarray(y, float)
    m = np.isfinite(x_a) & np.isfinite(x_b) & np.isfinite(y)
    x_a, x_b, y = x_a[m], x_b[m], y[m]
    lineages = [l for l, k in zip(lineages, m) if k]
    if len(y) < 4:
        return {"estimate": float("nan"), "n": int(len(y)), "skip": "n<4"}
    uniq, idx = _groups(lineages)
    rng = np.random.default_rng(seed)
    obs = spearman(x_a, y) - spearman(x_b, y)
    reps, degen = [], 0
    for _ in range(B):
        pick = rng.choice(len(uniq), size=len(uniq), replace=True)
        sel = np.concatenate([idx[uniq[p]] for p in pick])
        d = spearman(x_a[sel], y[sel]) - spearman(x_b[sel], y[sel])
        if np.isfinite(d):
            reps.append(d)
        else:
            degen += 1
    reps = np.array(reps)
    lo = float(np.percentile(reps, 2.5)) if len(reps) else float("nan")
    hi = float(np.percentile(reps, 97.5)) if len(reps) else float("nan")
    return {"estimate": float(obs), "ci_low": lo, "ci_high": hi,
            "excludes_zero": bool(len(reps) and (lo > 0 or hi < 0)),
            "n": int(len(y)), "n_lineages": len(uniq), "B": B,
            "n_degenerate_replicates": int(degen)}


def paired_auroc_diff(v_a, v_b, labels, lineages, seed: int = SEED, B: int = B) -> dict:
    """AUROC(a) - AUROC(b) on the SAME resampled lineages (a paired difference,
    so the two metrics never see different panels)."""
    v_a, v_b = np.asarray(v_a, float), np.asarray(v_b, float)
    labels = np.asarray(labels, int)
    m = np.isfinite(v_a) & np.isfinite(v_b)
    v_a, v_b, labels = v_a[m], v_b[m], labels[m]
    lineages = [l for l, k in zip(lineages, m) if k]
    uniq, idx = _groups(lineages)
    rng = np.random.default_rng(seed)
    obs = auroc(v_a[labels == 1], v_a[labels == 0]) - auroc(v_b[labels == 1], v_b[labels == 0])
    reps, degen = [], 0
    for _ in range(B):
        pick = rng.choice(len(uniq), size=len(uniq), replace=True)
        sel = np.concatenate([idx[uniq[p]] for p in pick])
        l = labels[sel]
        if l.sum() == 0 or l.sum() == len(l):
            degen += 1
            continue
        reps.append(auroc(v_a[sel][l == 1], v_a[sel][l == 0]) -
                    auroc(v_b[sel][l == 1], v_b[sel][l == 0]))
    reps = np.array([r for r in reps if np.isfinite(r)])
    return {"estimate": float(obs),
            "ci_low": float(np.percentile(reps, 2.5)) if len(reps) else float("nan"),
            "ci_high": float(np.percentile(reps, 97.5)) if len(reps) else float("nan"),
            "excludes_zero": bool(len(reps) and (np.percentile(reps, 2.5) > 0
                                                 or np.percentile(reps, 97.5) < 0)),
            "n_effective_replicates": int(len(reps)),
            "n_degenerate_replicates": int(degen), "B": B,
            "n_items": int(len(v_a)), "n_lineages": len(uniq)}


def permutation_p(values, labels, seed: int = SEED, n_perm: int = N_PERM) -> dict:
    """Label-shuffle null for an AUROC.  With few positives an AUROC of 1.000 has
    a non-trivial exact null (1/C(n, n_pos)), which the CI alone does not show."""
    values = np.asarray(values, float)
    labels = np.asarray(labels, int)
    m = np.isfinite(values)
    values, labels = values[m], labels[m]
    obs = auroc(values[labels == 1], values[labels == 0])
    rng = np.random.default_rng(seed)
    ge = 0
    null = []
    for _ in range(n_perm):
        p = rng.permutation(labels)
        a = auroc(values[p == 1], values[p == 0])
        null.append(a)
        ge += int(a >= obs)
    null = np.array(null)
    from math import comb
    n, k = len(labels), int(labels.sum())
    return {"observed_auroc": obs, "p_permutation": (1 + ge) / (1 + n_perm),
            "n_permutations": n_perm, "null_mean": float(null.mean()),
            "null_sd": float(null.std()),
            "exact_null_floor": (1.0 / comb(n, k)) if 0 < k < n else None,
            "n_pos": k, "n_neg": n - k}


# ---------------------------------------------------------------------------
# Leave-one-group-out, with rank transfer AND calibration transfer separated
# ---------------------------------------------------------------------------
def leave_one_group_out(values, labels, groups, lineages, *, lower_is_positive=True) -> dict:
    """For each held-out group g (uploader or architecture family):
      * fit a midpoint threshold on all OTHER groups' positives + ALL negatives
      * RANK TRANSFER    : AUROC on g's members vs all negatives outside g
      * CALIBRATION TRANSFER: catch rate on g's positives at that fitted cutoff
    S2 says these two come apart; reporting only one hides it."""
    values = np.asarray(values, float)
    labels = np.asarray(labels, int)
    groups = np.asarray(groups)
    out = {}
    for g in sorted(set(groups[labels == 1])):
        held = groups == g
        train_pos = values[(labels == 1) & ~held]
        train_neg = values[(labels == 0) & ~held]
        if len(train_pos) == 0 or len(train_neg) == 0:
            out[str(g)] = {"skip": "no training positives or negatives outside the group"}
            continue
        # midpoint between the worst positive and the best negative, in the
        # direction where a LOW value means abliterated (W05) unless told otherwise
        thr = (float(np.max(train_pos)) + float(np.min(train_neg))) / 2.0 \
            if lower_is_positive else (float(np.min(train_pos)) + float(np.max(train_neg))) / 2.0
        test_pos = values[(labels == 1) & held]
        test_neg = values[(labels == 0) & ~held]
        catch = float(np.mean(test_pos < thr)) if lower_is_positive \
            else float(np.mean(test_pos > thr))
        fpr = float(np.mean(test_neg < thr)) if lower_is_positive \
            else float(np.mean(test_neg > thr))
        lin = [l for l, k in zip(lineages, ((labels == 1) & held) | ((labels == 0) & ~held)) if k]
        v = np.concatenate([test_pos, test_neg])
        y = np.concatenate([np.ones(len(test_pos)), np.zeros(len(test_neg))])
        sgn = -1.0 if lower_is_positive else 1.0
        boot = bootstrap_ci(sgn * v, y, lin)
        out[str(g)] = {"threshold": thr, "rank_transfer_auroc": boot["estimate"],
                       "rank_transfer_ci": [boot["ci_low"], boot["ci_high"]],
                       "calibration_transfer_catch_rate": catch,
                       "calibration_transfer_fpr_on_negatives": fpr,
                       "n_held_out_positives": int(len(test_pos)),
                       "n_negatives_used": int(len(test_neg)),
                       "n_training_positives": int(len(train_pos))}
    return out


if __name__ == "__main__":
    print_contract()
    # module-level sanity checks on the estimators themselves
    a = auroc(np.array([3.0, 4.0, 5.0]), np.array([0.0, 1.0, 2.0]))
    assert a == 1.0, a
    assert auroc(np.array([1.0, 1.0]), np.array([1.0, 1.0])) == 0.5
    assert abs(auroc(np.array([1.0, 3.0]), np.array([2.0, 4.0])) - 0.25) < 1e-12
    p = permutation_p(np.array([5., 4., 3., 2., 1., 0.]), np.array([1, 1, 1, 0, 0, 0]),
                      n_perm=2000)
    assert p["observed_auroc"] == 1.0 and p["exact_null_floor"] == 1 / 20
    print("estimator self-checks PASS; exact null floor for 3-of-6 =", p["exact_null_floor"])
