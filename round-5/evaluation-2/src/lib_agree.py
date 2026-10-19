#!/usr/bin/env python3
"""Agreement, interval and multiplicity statistics for the judge-validation evaluation.

Everything here is implemented from the definition rather than pulled from a package,
because the exact variants matter and are argued for in the artifact:

  * `cohens_kappa_multi` -- the full multi-class kappa, NOT the binary special case
    lib_behave.cohens_kappa implements.  The archived kappa of 0.149 is a BINARY
    (refusal-vs-not) kappa against a substring screen; quoting it beside a 3-class
    number without saying so would be a category error.
  * `gwet_ac1` -- the standard fix for the prevalence paradox.  On abliterated stages
    the marginals are near-degenerate (almost nothing is labelled REFUSAL), which
    deflates kappa toward 0 even at 95% raw agreement.  AC1 replaces kappa's
    chance-agreement term with one that does not blow up under skewed marginals.
  * `pabak` -- prevalence-and-bias-adjusted kappa, i.e. 2*p_o - 1, reported so the
    reader can see how much of the kappa/AC1 spread is pure prevalence.
  * `newcombe_diff` -- the hybrid-score interval on a difference of two INDEPENDENT
    proportions.  A Wald interval on a difference where one arm sits at 0.95 and the
    other near 0.27 mis-covers; Newcombe's is the standard fix and is what the
    parent-minus-root-B gap needs.
  * `mcnemar_exact` -- the exact binomial test on PAIRED discordant cells.  The two
    scorers label the SAME items, so an unpaired two-proportion test would be wrong.
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np


# ==========================================================================
# intervals
# ==========================================================================
def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def newcombe_diff(k1: int, n1: int, k2: int, n2: int, z: float = 1.96) -> dict:
    """Newcombe hybrid-score 95% interval on p1 - p2 for INDEPENDENT samples."""
    if n1 == 0 or n2 == 0:
        return {"diff": float("nan"), "lo": float("nan"), "hi": float("nan"),
                "excludes_zero": False, "method": "newcombe_hybrid_score"}
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, z)
    l2, u2 = wilson(k2, n2, z)
    lo = (p1 - p2) - z * math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = (p1 - p2) + z * math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return {"diff": p1 - p2, "lo": max(-1.0, lo), "hi": min(1.0, hi),
            "excludes_zero": bool(lo > 0 or hi < 0), "method": "newcombe_hybrid_score"}


def mcnemar_exact(a: list[int], b: list[int]) -> dict:
    """Exact McNemar on paired binary labels: b01 vs b10 under Binomial(n_disc, 0.5)."""
    assert len(a) == len(b)
    b01 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    b10 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    n = b01 + b10
    if n == 0:
        return {"b01": 0, "b10": 0, "n_discordant": 0, "p_value": 1.0,
                "rate_diff": 0.0, "note": "no discordant pairs"}
    from scipy.stats import binomtest
    p = float(binomtest(min(b01, b10), n, 0.5, alternative="two-sided").pvalue)
    return {"b01": b01, "b10": b10, "n_discordant": n, "p_value": p,
            "rate_diff": float(np.mean(b) - np.mean(a)),
            "note": "exact binomial on paired discordant cells"}


def paired_diff_exact_ci(a: list[int], b: list[int], n_boot: int = 10000,
                         seed: int = 0) -> dict:
    """Paired bootstrap percentile interval on mean(b) - mean(a) over the SAME items."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) == 0:
        return {"diff": float("nan"), "lo": float("nan"), "hi": float("nan"), "n": 0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(a), size=(n_boot, len(a)))
    d = b[idx].mean(axis=1) - a[idx].mean(axis=1)
    return {"diff": float(b.mean() - a.mean()), "lo": float(np.quantile(d, 0.025)),
            "hi": float(np.quantile(d, 0.975)), "n": int(len(a)), "n_boot": n_boot,
            "excludes_zero": bool(np.quantile(d, 0.025) > 0 or np.quantile(d, 0.975) < 0)}


# ==========================================================================
# agreement
# ==========================================================================
def confusion(a: list[str], b: list[str], labels: list[str]) -> list[list[int]]:
    idx = {l: i for i, l in enumerate(labels)}
    M = [[0] * len(labels) for _ in labels]
    for x, y in zip(a, b):
        if x in idx and y in idx:
            M[idx[x]][idx[y]] += 1
    return M


def percent_agreement(a: list[str], b: list[str]) -> float:
    if not a:
        return float("nan")
    return float(np.mean([x == y for x, y in zip(a, b)]))


def cohens_kappa_multi(a: list[str], b: list[str], labels: list[str] | None = None
                       ) -> float:
    """Multi-class Cohen's kappa (unweighted)."""
    if not a:
        return float("nan")
    labels = labels or sorted(set(a) | set(b))
    n = len(a)
    po = percent_agreement(a, b)
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[l] / n) * (cb[l] / n) for l in labels)
    return float((po - pe) / (1 - pe)) if pe < 1 else float("nan")


def gwet_ac1(a: list[str], b: list[str], labels: list[str] | None = None) -> float:
    """Gwet's AC1 -- the prevalence-robust alternative to kappa.

    Chance agreement is 1/(q-1) * sum_l pi_l (1 - pi_l) with pi_l the mean marginal,
    which stays bounded as the marginals become degenerate instead of exploding toward
    p_o the way kappa's product term does.
    """
    if not a:
        return float("nan")
    labels = labels or sorted(set(a) | set(b))
    q = len(labels)
    if q < 2:
        return float("nan")
    n = len(a)
    ca, cb = Counter(a), Counter(b)
    pi = {l: (ca[l] / n + cb[l] / n) / 2.0 for l in labels}
    pe = sum(pi[l] * (1 - pi[l]) for l in labels) / (q - 1)
    po = percent_agreement(a, b)
    return float((po - pe) / (1 - pe)) if pe < 1 else float("nan")


def pabak(a: list[str], b: list[str], n_classes: int = 3) -> float:
    """Prevalence-and-bias-adjusted kappa, generalised to q classes:
    (q*p_o - 1)/(q - 1); reduces to 2*p_o - 1 at q = 2."""
    if not a:
        return float("nan")
    po = percent_agreement(a, b)
    return float((n_classes * po - 1) / (n_classes - 1))


def agreement_block(a: list[str], b: list[str], labels: list[str],
                    weights: list[float] | None = None) -> dict:
    """Every agreement statistic for one scorer pair on one item set."""
    out = {"n": len(a), "percent_agreement": percent_agreement(a, b),
           "cohens_kappa": cohens_kappa_multi(a, b, labels),
           "gwet_ac1": gwet_ac1(a, b, labels),
           "pabak": pabak(a, b, len(labels)),
           "confusion_labels": labels, "confusion": confusion(a, b, labels)}
    if weights is not None and len(weights) == len(a) and sum(weights) > 0:
        w = np.asarray(weights, float)
        agree = np.asarray([x == y for x, y in zip(a, b)], float)
        out["percent_agreement_population_weighted"] = float((w * agree).sum() / w.sum())
    return out


# ==========================================================================
# rate-level agreement
# ==========================================================================
def rate_agreement(x: list[float], y: list[float]) -> dict:
    """Pearson r, Spearman rho, Bland-Altman bias and limits of agreement."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return {"n": int(len(x)), "pearson_r": float("nan"), "spearman_rho": float("nan")}
    from scipy.stats import pearsonr, spearmanr
    pr = pearsonr(x, y)
    sr = spearmanr(x, y)
    d = y - x
    return {"n": int(len(x)),
            "pearson_r": float(pr[0]), "pearson_p": float(pr[1]),
            "spearman_rho": float(sr[0]), "spearman_p": float(sr[1]),
            "mean_signed_delta_bland_altman_bias": float(d.mean()),
            "sd_delta": float(d.std(ddof=1)) if len(d) > 1 else float("nan"),
            "loa_lo": float(d.mean() - 1.96 * d.std(ddof=1)) if len(d) > 1 else float("nan"),
            "loa_hi": float(d.mean() + 1.96 * d.std(ddof=1)) if len(d) > 1 else float("nan"),
            "max_abs_delta": float(np.abs(d).max()),
            "median_abs_delta": float(np.median(np.abs(d)))}


# ==========================================================================
# multiplicity
# ==========================================================================
def holm(pvals: dict[str, float]) -> dict[str, dict]:
    """Holm-Bonferroni step-down over a named family of p-values."""
    items = [(k, v) for k, v in pvals.items() if v is not None and np.isfinite(v)]
    m = len(items)
    items.sort(key=lambda kv: kv[1])
    out, running = {}, 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, max(running, (m - i) * p))
        running = adj
        out[k] = {"p_raw": p, "p_holm": adj, "reject_at_0.05_raw": bool(p < 0.05),
                  "reject_at_0.05_holm": bool(adj < 0.05), "family_size": m}
    for k, v in pvals.items():
        if k not in out:
            out[k] = {"p_raw": v, "p_holm": None, "reject_at_0.05_raw": None,
                      "reject_at_0.05_holm": None, "family_size": m}
    return out
