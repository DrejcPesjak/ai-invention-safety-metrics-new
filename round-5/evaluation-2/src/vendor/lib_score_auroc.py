#!/usr/bin/env python3
"""Tie-aware AUROC, transcribed from the iteration-3 archive (`lib_score.auroc`).

Kept in its own module so the held-out AUROC profile computed for the new roots is
byte-for-byte the same estimator the archive used for root A -- otherwise the
"AUROC saturates" comparison across hosts would confound estimator with host.
"""

from __future__ import annotations

import numpy as np


def auroc(pos, neg) -> float:
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    x = np.concatenate([pos, neg])
    order = np.argsort(x, kind="mergesort")
    xs = x[order]
    rr = (np.arange(len(xs)) + 1.0)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[j + 1] == xs[i]:
            j += 1
        if j > i:
            rr[i:j + 1] = rr[i:j + 1].mean()
        i = j + 1
    r2 = np.empty_like(rr)
    r2[order] = rr
    n1, n0 = len(pos), len(neg)
    return float((r2[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
