#!/usr/bin/env python3
"""The eight edit kernels of Arm B.

Every kernel operates on the SAME ordered list of residual-write matrices and,
except where a recipe is defined otherwise, on the SAME refusal direction r
(taken verbatim from the archived in-house root recipe).  The kernel is the
independent variable; the direction is held fixed.  That is the whole design.

Base operation, per matrix at layer l:

    W  <-  W - w_l * outer(r, r @ W)

so the residual energy along r scales exactly as (1 - w_l)^2, layer by layer.
"""

from __future__ import annotations

import math

import torch

EPS = 1e-12


def _unit(r: torch.Tensor, dtype: torch.dtype = torch.float32) -> torch.Tensor:
    r = r.to(dtype)
    return r / (r.norm() + EPS)


@torch.no_grad()
def cast_like(edited: list[torch.Tensor], ref: list[torch.Tensor]) -> list[torch.Tensor]:
    """Store the edited matrices back at the reference matrices' precision.

    This is NOT cosmetic.  The archived in-house recipe (vendored_lib_ablate.
    ablate_sd) writes `(W - outer(r, r@W)).to(sd[k].dtype)`, i.e. it rounds the
    result back to bfloat16, and every real Hub checkpoint is likewise stored in
    bf16.  After a COMPLETE projection the surviving energy along r is therefore
    not zero but bf16 rounding noise, which is exactly why the archived root
    lands at W05 = -4.59 rather than at the -30 floor.  Skipping the cast would
    make Arm B incomparable with both the archive and Arm A.
    """
    return [e.to(r.dtype) for e, r in zip(edited, ref, strict=True)]


def _wdtype(W: torch.Tensor) -> torch.dtype:
    """Work in float32 (what the archived pipeline uses) unless the caller
    handed in float64, in which case the extra precision is deliberate."""
    return torch.float64 if W.dtype == torch.float64 else torch.float32


# --------------------------------------------------------------------------
# depth kernels: layer -> subtraction weight
# --------------------------------------------------------------------------
def w_uniform(L: int, w: float = 1.0) -> list[float]:
    return [float(w)] * L


def w_gaussian(L: int, peak: int, spread: float) -> list[float]:
    """mlabonne v2: subtraction weights follow a normal distribution with a
    given spread and peak layer.  spread = inf degenerates to the uniform edit."""
    if not math.isfinite(spread):
        return [1.0] * L
    if spread <= 0:
        return [1.0 if l == peak else 0.0 for l in range(L)]
    return [float(math.exp(-((l - peak) ** 2) / (2.0 * spread * spread)))
            for l in range(L)]


def w_band(L: int, lo_frac: float = 0.25, hi_frac: float = 0.75) -> list[float]:
    lo, hi = lo_frac * (L - 1), hi_frac * (L - 1)
    return [1.0 if lo <= l <= hi else 0.0 for l in range(L)]


def gaussian_min_weight(L: int, peak: int, spread: float) -> float:
    return min(w_gaussian(L, peak, spread))


def critical_spread(L: int, peak: int, w_star: float) -> float:
    """Smallest spread whose MINIMUM depth weight still reaches w_star.

    min_l w_l = exp(-dmax^2 / (2 s^2)) with dmax = max(peak, L-1-peak).
    Solving for s:  s = dmax / sqrt(2 ln(1/w_star)).
    """
    dmax = max(peak, L - 1 - peak)
    if not (0.0 < w_star < 1.0):
        return float("nan")
    return float(dmax / math.sqrt(2.0 * math.log(1.0 / w_star)))


# --------------------------------------------------------------------------
# the edits
# --------------------------------------------------------------------------
@torch.no_grad()
def edit_projection(mats: list[torch.Tensor], layers: list[int], r: torch.Tensor,
                    weights: list[float]) -> list[torch.Tensor]:
    """(i)/(ii)/(iii)/(vi): W <- W - w_l * outer(r, r@W)."""
    out = []
    for W, lay in zip(mats, layers, strict=True):
        dt = _wdtype(W)
        rf = _unit(r, dt).to(W.device)
        w = float(weights[lay]) if lay < len(weights) else 0.0
        Wf = W.to(dt)
        out.append(Wf if w == 0.0 else (Wf - w * torch.outer(rf, rf @ Wf)))
    return out


@torch.no_grad()
def edit_percomponent(mats: list[torch.Tensor], layers: list[int], kinds: list[str],
                      dirs_per_layer: list[torch.Tensor], direction_index: float,
                      w_attn: float, w_mlp: float) -> list[torch.Tensor]:
    """(iv) Heretic-style: a FLOAT direction index interpolating between the
    per-layer diff-in-means directions, and a per-COMPONENT max weight that may
    exceed 1 (over-subtraction / sign flip on the projected component)."""
    lo = int(math.floor(direction_index))
    hi = min(lo + 1, len(dirs_per_layer) - 1)
    frac = float(direction_index - lo)
    r0 = (1.0 - frac) * dirs_per_layer[lo].float() + frac * dirs_per_layer[hi].float()
    out = []
    for W, _lay, kind in zip(mats, layers, kinds, strict=True):
        dt = _wdtype(W)
        rr = _unit(r0, dt).to(W.device)
        w = w_attn if kind == "attn" else w_mlp
        Wf = W.to(dt)
        out.append(Wf - w * torch.outer(rr, rr @ Wf))
    return out


@torch.no_grad()
def edit_householder(mats: list[torch.Tensor], r: torch.Tensor,
                     lam: float = 1.0) -> list[torch.Tensor]:
    """(v) ORBA: W <- H W with H = I - 2 r r^T, applied identically to every
    write matrix.  H is ORTHOGONAL, so ||HW||_F = ||W||_F and the shared Gram
    A = sum (HW)(HW)^T / ||W||_F^2 = H A H is an orthogonal SIMILARITY: the
    eigenvalues are EXACTLY invariant and v1 -> H v1.  W01, W04, W05 are
    therefore invariant BY CONSTRUCTION, not merely empirically.

    lam < 1 gives the geodesic interpolation W <- cos(t) W + sin(t) H W,
    t = lam * pi/2, used only as the fluency fallback.
    """
    out = []
    for W in mats:
        dt = _wdtype(W)
        rr = _unit(r, dt).to(W.device)
        Wf = W.to(dt)
        HW = Wf - 2.0 * torch.outer(rr, rr @ Wf)
        if lam >= 1.0:
            out.append(HW)
        else:
            t = lam * math.pi / 2.0
            out.append(math.cos(t) * Wf + math.sin(t) * HW)
    return out


@torch.no_grad()
def edit_rank_k(mats: list[torch.Tensor], Q: torch.Tensor) -> list[torch.Tensor]:
    """(vii) uniform rank-k: project out an orthonormal k-dim subspace Q (d, k)
    from the OUTPUT of every write matrix."""
    out = []
    for W in mats:
        dt = _wdtype(W)
        Wf = W.to(dt)
        Qd = Q.to(W.device, dt)
        out.append(Wf - Qd @ (Qd.T @ Wf))
    return out


@torch.no_grad()
def edit_mpoa(mats: list[torch.Tensor], r: torch.Tensor) -> list[torch.Tensor]:
    """(viii) MPOA, the exact norm-preserving four-step: (1) project the refusal
    direction out of the output space, (2) measure the original row norms,
    (3) measure the projected row norms, (4) rescale each row back to its
    original norm.  The edit is uniform across layers and removes the same
    direction, but restores per-row magnitude."""
    out = []
    for W in mats:
        dt = _wdtype(W)
        rr = _unit(r, dt).to(W.device)
        Wf = W.to(dt)
        n0 = Wf.norm(dim=1, keepdim=True)
        P = Wf - torch.outer(rr, rr @ Wf)
        n1 = P.norm(dim=1, keepdim=True)
        out.append(P * (n0 / (n1 + EPS)))
    return out
