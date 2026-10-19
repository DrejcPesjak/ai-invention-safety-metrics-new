#!/usr/bin/env python3
"""Estimators. Every tie convention is explicit; nothing here reads a file."""

from __future__ import annotations

import numpy as np
from scipy.stats import rankdata


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    """Spearman rho with RANK-AVERAGE ties, computed as Pearson on the ranks."""
    if x.size < 4:
        return float("nan")
    rx = rankdata(x, method="average")
    ry = rankdata(y, method="average")
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    dx = float(np.sqrt((rx * rx).sum()))
    dy = float(np.sqrt((ry * ry).sum()))
    if dx == 0.0 or dy == 0.0:
        return float("nan")
    return float((rx * ry).sum() / (dx * dy))


def spearman_rows(A: np.ndarray, Bm: np.ndarray) -> np.ndarray:
    """Row-wise Spearman for two (B, n) matrices. Rank-average ties."""
    ra = rankdata(A, method="average", axis=1)
    rb = rankdata(Bm, method="average", axis=1)
    ra = ra - ra.mean(axis=1, keepdims=True)
    rb = rb - rb.mean(axis=1, keepdims=True)
    num = (ra * rb).sum(axis=1)
    den = np.sqrt((ra * ra).sum(axis=1) * (rb * rb).sum(axis=1))
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, num / den, np.nan)


def auroc_with_ties(pos: np.ndarray, neg: np.ndarray) -> tuple[float, int]:
    """Mann-Whitney U / (n_pos*n_neg) from rank-average ranks (ties credit 0.5).

    Returns (auroc, n_tied_pairs) where n_tied_pairs counts exact (pos, neg)
    value ties actually encountered.
    """
    n_p, n_n = pos.size, neg.size
    if n_p == 0 or n_n == 0:
        return float("nan"), 0
    allv = np.concatenate([pos, neg])
    r = rankdata(allv, method="average")
    u = r[:n_p].sum() - n_p * (n_p + 1) / 2.0
    ties = int((pos[:, None] == neg[None, :]).sum())
    return float(u / (n_p * n_n)), ties


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1.0 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (float(max(0.0, c - h)), float(min(1.0, c + h)))


def cohen_kappa(a: list[str], b: list[str]) -> float:
    labs = sorted(set(a) | set(b))
    idx = {l: i for i, l in enumerate(labs)}
    k = len(labs)
    m = np.zeros((k, k))
    for x, y in zip(a, b):
        m[idx[x], idx[y]] += 1
    n = m.sum()
    if n == 0:
        return float("nan")
    po = np.trace(m) / n
    pe = float((m.sum(axis=0) * m.sum(axis=1)).sum()) / (n * n)
    if pe == 1.0:
        return float("nan")
    return float((po - pe) / (1 - pe))


def pct_ci(v: np.ndarray) -> tuple[float, float]:
    v = v[np.isfinite(v)]
    if v.size < 20:
        return (float("nan"), float("nan"))
    return (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)))


def spearman_brown(r: float, k: float = 2.0) -> float:
    if not np.isfinite(r) or (1 + (k - 1) * r) == 0:
        return float("nan")
    return float(k * r / (1 + (k - 1) * r))


def rho_from_target(rho_target: float) -> float:
    """Gaussian-copula correlation giving a target Spearman rho."""
    return float(2.0 * np.sin(np.pi * rho_target / 6.0))
