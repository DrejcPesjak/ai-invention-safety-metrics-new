#!/usr/bin/env python3
"""Synthetic edit generators, implemented VERBATIM from the dependency research
dossier's `recipe_taxonomy[*].weight_update_equation` (gen_art_research_1).

Every generator takes the parent's residual-write matrices (float32 [d, d_in],
in the archive's catalog order) plus their layer indices and a measured refusal
direction r, and returns a NEW list of edited matrices.  Nothing here touches
activations or runs a forward pass.

Recipe -> equation provenance
  R1     W <- W - r_hat (r_hat^T W)                       (rank-one projection)
  R2v2   W_l <- W_l - w_l (W_l r_hat) r_hat^T, w_l Gaussian over depth (mlabonne)
  R2p    per-component kernel w_c(l), max_weight may exceed 1 (Heretic)
  R3     MPOA exact row-norm-preserving four-step
  R4     ORBA Householder H = I - 2 u u^T   (reflection; the falsification target)
  R4g    ORBA geodesic at lambda = 1        (rotation onto the complement)
  R5a    Gabliteration P = R(R^T R + lam I)^-1 R^T, alpha_l position-weighted
  R5b    OBLITERATUS rank-k  W <- (I - U_k U_k^T) W
  band   R1 restricted to a contiguous layer band  (the pooled statistic's blind spot)
  head   R1 restricted to the columns of the top 25% of attention heads
  sub    R1 with a uniform sub-unit weight w  (isolates 'incomplete' from 'non-uniform')
Benign controls (matched Frobenius delta, must NOT be flagged)
  noise  W <- W + sigma * N(0, 1)
  rand1  rank-one projection along a RANDOM direction
  lora   W <- W + B A, rank 16, scaled to the matched delta
"""

from __future__ import annotations

import numpy as np
import torch


def _unit(v: torch.Tensor) -> torch.Tensor:
    return v / v.norm()


def bf16_roundtrip(mats):
    """Quantise to bfloat16 and back, i.e. exactly what happens when an edited
    checkpoint is SAVED to disk.

    This is load-bearing, not cosmetic.  An exact rank-one projection computed in
    float32 leaves the annihilated direction at machine zero (log10 e ~ -12), but
    every real abliterated checkpoint on the Hub is stored in bfloat16, and that
    round-trip puts energy back along the direction: the archived in-house root
    scores W05 = -4.5917, and rebuilding it in float32 WITHOUT the round-trip
    gives -12.24.  The archived 'scar depth' is therefore set by the STORAGE
    DTYPE, not by the edit; comparing a float32 synthetic against bfloat16 real
    checkpoints would make every synthetic trivially detectable.
    """
    return [W.to(torch.bfloat16).to(torch.float32) for W in mats]


def _rank1_project(W: torch.Tensor, r: torch.Tensor, w: float = 1.0) -> torch.Tensor:
    """W <- W - w * r (r^T W).  w=1 is the exact projection; w>1 over-subtracts."""
    return W - w * torch.outer(r, r @ W)


def _fro(W: torch.Tensor) -> float:
    return float(W.norm())


# ---------------------------------------------------------------------------
def edit_uniform(mats, layers, r, *, weight: float = 1.0):
    """R1 / sub-unit-weight: same weight on every layer."""
    return [_rank1_project(W, r, weight) for W in mats]


def edit_band(mats, layers, r, *, lo: int, hi: int, weight: float = 1.0):
    """R1 restricted to layers [lo, hi)."""
    return [_rank1_project(W, r, weight) if lo <= l < hi else W.clone()
            for W, l in zip(mats, layers)]


def edit_gaussian(mats, layers, r, *, peak: float, spread: float):
    """mlabonne v2: w_l = exp(-(l - peak)^2 / (2 spread^2)), peak weight 1."""
    out = []
    for W, l in zip(mats, layers):
        w = float(np.exp(-((l - peak) ** 2) / (2.0 * spread ** 2)))
        out.append(_rank1_project(W, r, w))
    return out


def edit_heretic(mats, layers, kinds, r, *, L: int,
                 attn=(1.46, 0.55, 0.05, 0.35), mlp=(0.92, 0.40, 0.02, 0.30)):
    """R2p: per-component kernel (max_weight, max_weight_position, min_weight,
    min_weight_distance), chosen SEPARATELY per component; max_weight may exceed
    1, which over-subtracts and FLIPS the sign of the component along r_hat.

    NOTE (stated in the output): Heretic's FLOAT direction index interpolates
    between two per-layer difference-of-means directions.  Those require
    activations, which this artifact does not run, so the interpolation is not
    reproduced -- a single measured direction is used for every layer.  The
    depth-weighted, per-component, >1-weight structure IS reproduced.
    """
    out = []
    for W, l, kind in zip(mats, layers, kinds):
        mx, pos, mn, dist = attn if kind == "attn" else mlp
        rel = l / max(L - 1, 1)
        # triangular kernel: mx at `pos`, falling to `mn` at distance `dist`
        w = mx - (mx - mn) * min(abs(rel - pos) / max(dist, 1e-6), 1.0)
        out.append(_rank1_project(W, r, float(w)))
    return out


def edit_per_head(mats, layers, kinds, r, *, n_heads: int, top_frac: float = 0.25):
    """R4-class partial surgery: R1 applied only to the columns of the top
    `top_frac` of attention heads (mlp matrices untouched)."""
    out = []
    for W, l, kind in zip(mats, layers, kinds):
        if kind != "attn" or W.shape[1] % n_heads != 0:
            out.append(W.clone())
            continue
        hd = W.shape[1] // n_heads
        # "top" heads by the head-block's alignment with r (deterministic, weights-only)
        align = [float((r @ W[:, h * hd:(h + 1) * hd]).pow(2).sum()) for h in range(n_heads)]
        order = np.argsort(align)[::-1]
        chosen = order[: max(1, int(round(top_frac * n_heads)))]
        E = W.clone()
        for h in chosen:
            sl = slice(int(h) * hd, (int(h) + 1) * hd)
            E[:, sl] = _rank1_project(W[:, sl], r)
        out.append(E)
    return out


def _orthonormal_with(r: torch.Tensor, k: int, seed: int = 0) -> torch.Tensor:
    """(k, d) orthonormal basis whose first row is r."""
    d = r.shape[0]
    g = torch.Generator().manual_seed(seed)
    M = torch.randn(k, d, generator=g)
    M[0] = r
    Q, _ = torch.linalg.qr(M.T.double())
    Q = Q.T.to(torch.float32)
    if float(Q[0] @ r) < 0:
        Q = -Q
    return Q


def edit_rank_k(mats, layers, r, *, k: int, seed: int = 0):
    """R5b / OBLITERATUS: W <- (I - U_k U_k^T) W."""
    U = _orthonormal_with(r, k, seed=seed)
    return [W - U.T @ (U @ W) for W in mats]


def edit_mpoa(mats, layers, r, *, alpha: float = 1.0):
    """R3 MPOA, exact four-step, row norms preserved to machine precision."""
    out = []
    for W in mats:
        rn = W.norm(dim=1, keepdim=True).clamp_min(1e-12)
        Wh = W / rn
        p = r @ Wh                                   # (d_in,)
        Wa = Wh - alpha * torch.outer(r, p)
        Wa = Wa / Wa.norm(dim=1, keepdim=True).clamp_min(1e-12)
        out.append(Wa * rn)
    return out


def edit_orba_householder(mats, layers, r):
    """R4 v3: H = I - 2 u u^T.  The component along u is FLIPPED, not removed,
    so the operator is an ISOMETRY and leaves NO null direction.  Pre-registered
    prediction P3: both the pooled and the windowed statistic MISS this."""
    return [_rank1_project(W, r, 2.0) for W in mats]


def edit_orba_geodesic(mats, layers, r):
    """R4 v4 at lambda = 1: w' = w + (cos theta - 1)(w.u)u with theta = pi/2,
    i.e. the refusal component is rotated exactly onto the orthogonal complement.
    Algebraically identical to R1; reported so the equivalence is explicit."""
    return [_rank1_project(W, r, 1.0) for W in mats]


def edit_gabliteration(mats, layers, r, *, k: int = 3, lam: float = 0.1,
                       alpha_base: float = 0.9, beta: float = 0.4, L: int = 28,
                       seed: int = 0):
    """R5a: P = R(R^T R + lam I)^-1 R^T; alpha_l = alpha_base(1 + beta(1 - |xi_l|)),
    xi_l = (2l - L - 1)/(L - 1)."""
    U = _orthonormal_with(r, k, seed=seed).double()          # (k, d), orthonormal
    G = U @ U.T                                              # = I_k
    P = (U.T @ torch.linalg.inv(G + lam * torch.eye(k, dtype=torch.float64)) @ U)
    P = P.to(torch.float32)
    out = []
    for W, l in zip(mats, layers):
        xi = (2 * l - L - 1) / max(L - 1, 1)
        a = alpha_base * (1 + beta * (1 - abs(xi)))
        out.append(W - a * (P @ W))
    return out


# ---------------------------------------------------------------------------
# benign controls at MATCHED Frobenius delta
# ---------------------------------------------------------------------------
def _match_delta(base_mats, edited_mats):
    return [_fro(a - b) for a, b in zip(base_mats, edited_mats)]


def control_noise(mats, deltas, *, seed: int = 0):
    g = torch.Generator().manual_seed(seed)
    out = []
    for W, dl in zip(mats, deltas):
        N = torch.randn(W.shape, generator=g)
        N = N * (dl / max(float(N.norm()), 1e-12))
        out.append(W + N)
    return out


def control_random_rank1(mats, deltas, *, d: int, seed: int = 0):
    g = torch.Generator().manual_seed(seed)
    u = _unit(torch.randn(d, generator=g))
    out = []
    for W, dl in zip(mats, deltas):
        D = torch.outer(u, u @ W)
        s = dl / max(float(D.norm()), 1e-12)
        out.append(W - s * D)
    return out


def control_lora(mats, deltas, *, rank: int = 16, seed: int = 0):
    g = torch.Generator().manual_seed(seed)
    out = []
    for W, dl in zip(mats, deltas):
        B = torch.randn(W.shape[0], rank, generator=g)
        A = torch.randn(rank, W.shape[1], generator=g)
        D = B @ A
        out.append(W + D * (dl / max(float(D.norm()), 1e-12)))
    return out
