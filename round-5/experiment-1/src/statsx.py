#!/usr/bin/env python3
"""Estimators.  Every AUROC carries an explicit orientation; every rate carries
its interval and the method that produced it."""

from __future__ import annotations

import numpy as np


def auroc_raw(scores: np.ndarray, labels: np.ndarray) -> float:
    """P(score_pos > score_neg) + 0.5 P(tie).  HIGHER score = positive."""
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels).astype(int)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    order = np.argsort(np.concatenate([pos, neg]), kind="mergesort")
    ranks = np.empty(len(order), dtype=float)
    srt = np.concatenate([pos, neg])[order]
    i = 0
    while i < len(srt):
        j = i
        while j + 1 < len(srt) and srt[j + 1] == srt[i]:
            j += 1
        ranks[order[i:j + 1]] = 0.5 * (i + j) + 1.0
        i = j + 1
    rp = ranks[: len(pos)].sum()
    return float((rp - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def auroc_oriented(scores, labels, *, lower_is_positive: bool) -> dict:
    """Both the raw and the oriented value, with the orientation named."""
    raw = auroc_raw(scores, labels)
    orient = "lower_is_positive" if lower_is_positive else "higher_is_positive"
    oriented = (1.0 - raw) if lower_is_positive else raw
    return {"auroc_oriented": oriented, "auroc_raw": raw, "orientation": orient,
            "n_pos": int(np.sum(np.asarray(labels) == 1)),
            "n_neg": int(np.sum(np.asarray(labels) == 0))}


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float, float]:
    """(point, lo, hi) Wilson score interval for a binomial proportion."""
    if n == 0:
        return (float("nan"), 0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def bootstrap_auroc_diff(scores_a, scores_b, labels, groups, *, n_boot: int = 10000,
                         lower_is_positive: bool = True, seed: int = 0) -> dict:
    """Paired bootstrap of AUROC(a) - AUROC(b), resampling GROUPS (lineages)."""
    rng = np.random.default_rng(seed)
    sa, sb = np.asarray(scores_a, float), np.asarray(scores_b, float)
    y = np.asarray(labels).astype(int)
    g = np.asarray(groups)
    uniq = np.unique(g)
    idx_by_g = {u: np.where(g == u)[0] for u in uniq}
    obs = (auroc_oriented(sa, y, lower_is_positive=lower_is_positive)["auroc_oriented"]
           - auroc_oriented(sb, y, lower_is_positive=lower_is_positive)["auroc_oriented"])
    diffs = []
    for _ in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        ii = np.concatenate([idx_by_g[u] for u in pick])
        yy = y[ii]
        if yy.sum() == 0 or yy.sum() == len(yy):
            continue
        d = (auroc_oriented(sa[ii], yy, lower_is_positive=lower_is_positive)["auroc_oriented"]
             - auroc_oriented(sb[ii], yy, lower_is_positive=lower_is_positive)["auroc_oriented"])
        if np.isfinite(d):
            diffs.append(d)
    diffs = np.array(diffs)
    if len(diffs) == 0:
        return {"observed": obs, "ci_low": float("nan"), "ci_high": float("nan"),
                "n_effective_resamples": 0, "n_groups": int(len(uniq)),
                "ci_method": "paired percentile bootstrap over groups"}
    return {"observed": float(obs),
            "ci_low": float(np.percentile(diffs, 2.5)),
            "ci_high": float(np.percentile(diffs, 97.5)),
            "n_effective_resamples": int(len(diffs)),
            "n_groups": int(len(uniq)),
            "frac_gt0": float((diffs > 0).mean()),
            "ci_method": "paired percentile bootstrap over groups (2.5/97.5)"}


def permutation_auroc(scores, labels, *, n_perm: int = 1000, lower_is_positive: bool = True,
                      seed: int = 0) -> dict:
    """Label-shuffle null.  Reports the exact floor 1/(n_perm+1), never 'p<0.001'."""
    rng = np.random.default_rng(seed)
    s = np.asarray(scores, float)
    y = np.asarray(labels).astype(int)
    obs = auroc_oriented(s, y, lower_is_positive=lower_is_positive)["auroc_oriented"]
    null = np.empty(n_perm)
    for i in range(n_perm):
        null[i] = auroc_oriented(s, rng.permutation(y),
                                 lower_is_positive=lower_is_positive)["auroc_oriented"]
    ge = int((null >= obs).sum())
    return {"observed": float(obs), "n_perm": int(n_perm),
            "p_value": float((ge + 1) / (n_perm + 1)),
            "p_floor": float(1.0 / (n_perm + 1)),
            "null_q95": float(np.percentile(null, 95)),
            "null_max": float(null.max()), "null_mean": float(null.mean())}


def spearman(x, y) -> float:
    x, y = np.asarray(x, float), np.asarray(y, float)
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])
