#!/usr/bin/env python3
"""analyse2 -- the windowed statistic W05w plus everything iteration 5 adds.

`wstats.py` (copied VERBATIM from the iteration-4 archive) stays the reference
estimator: it defines W01-W05 and W05w and it is what the reproduction gates are
run against.  This module adds a single-pass routine that returns, in addition
to exactly those numbers,

  * the pooled bottom-8 eigenvectors (Arm 3 needs a SUBSPACE, not one vector),
  * a per-window random-direction NULL (Arm 2), computed from one shared
    ensemble of unit directions so that the null is paired across windows and
    across models,
  * the three arithmetic quantities e_W(v1), e_W(r), cos^2(theta) and their
    residual (Arm 4),
  * per-window principal angles / subspace-discovery scalars when the removed
    subspace R is known by construction.

`gate_identity()` asserts that analyse2's W01-W05 and every W05w(k) equal the
vendored `wstats.analyse` values, so the extra machinery is provably a superset
and not a re-implementation with its own arithmetic.

Numerics rules carried over from the archive and NOT to be re-derived:
  * every Gram is accumulated in float32, in catalog order (layer, attn before
    mlp, then name); float32 summation is not associative and lam[0] on an
    abliterated checkpoint sits ~5 orders below the trace.
  * energies used for anything the windowed statistic is compared against are
    recomputed in float64 (`_energies64`).
  * W01 and W04 are NON-LOAD-BEARING: they are emitted, never gated on.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path

import numpy as np
import scipy.linalg as sla
import torch
from safetensors import safe_open

import wstats as WS

EPS = 1e-12

# ---------------------------------------------------------------------------
# dtype-preserving loader
# ---------------------------------------------------------------------------
# wstats.load_write_matrices casts every matrix to float32 at load.  That is
# correct for SCORING, but the Arm B kernels must be applied to -- and stored
# back at -- the checkpoint's native precision (bf16 on every real Hub
# checkpoint and on the archived in-house root).  Skipping the cast turns a
# complete projection from W05 = -4.59 into W05 = -12.7.  So the loader below
# reproduces wstats' catalog EXACTLY and only differs in keeping the dtype.


def build_catalog(path: Path, d: int, L: int, mt: str) -> list[tuple[Path, str, int, str]]:
    """The archive's residual-write catalog, in the archive's sort order."""
    shards = sorted(path.glob("*.safetensors"))
    if not shards:
        raise RuntimeError("no shards")
    catalog: list[tuple[Path, str, int, str]] = []
    for sh in shards:
        with safe_open(str(sh), framework="pt", device="cpu") as f:
            for name in f.keys():
                kind = WS.classify_tensor(name)
                if kind is None:
                    continue
                m = WS.LAYER_RE.search(name)
                if m is None:
                    continue
                shape = f.get_slice(name).get_shape()
                if len(shape) != 2 or shape[0] != d:
                    continue
                catalog.append((sh, name, int(m.group(1)), kind))
    n_expected = 2 * L
    if len(catalog) < 0.8 * n_expected:
        raise RuntimeError(f"UNRESOLVED architecture: {len(catalog)} write matrices, "
                           f"expected ~{n_expected} (d={d}, L={L}, {mt})")
    catalog.sort(key=lambda c: (c[2], 0 if c[3] == "attn" else 1, c[1]))
    return catalog


def load_native(path: Path, d: int, L: int, mt: str
                ) -> tuple[list[torch.Tensor], list[int], list[str], list[str]]:
    """(mats at NATIVE dtype, layers, kinds, names) -- same order as wstats."""
    catalog = build_catalog(path, d, L, mt)
    handles = {sh: safe_open(str(sh), framework="pt", device="cpu")
               for sh in {c[0] for c in catalog}}
    mats, layers, kinds, names = [], [], [], []
    for sh, name, layer, kind in catalog:
        W = handles[sh].get_tensor(name)
        Wf = W.to(torch.float32)
        fro2 = float((Wf * Wf).sum())
        del Wf
        if fro2 <= 0 or not np.isfinite(fro2):
            del W
            continue
        mats.append(W)
        layers.append(layer)
        kinds.append(kind)
        names.append(name)
    del handles
    return mats, layers, kinds, names


def to_f32(mats: list[torch.Tensor]) -> list[torch.Tensor]:
    return [W.to(torch.float32) for W in mats]


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def unit64(v: torch.Tensor) -> torch.Tensor:
    v = v.to(torch.float64)
    return v / (v.norm() + EPS)


def seed_from(*parts) -> int:
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()
    return int(h[:8], 16) % (2 ** 31)


def _energy_block(mats: list[torch.Tensor], U: torch.Tensor, d: int) -> np.ndarray:
    """e(u_j, W_m) for every direction j and matrix m -> (n_dirs, n_mat).

    The dtype is kept at float32, matching the vendored estimator exactly: the
    archive concatenates per-matrix float32 energy arrays and takes a float32
    quantile for W03, and promoting to float64 here shifts W03 by ~5e-9.
    """
    out = np.empty((U.shape[0], len(mats)), dtype=np.float32)
    for m, W in enumerate(mats):
        fro2 = float((W * W).sum())
        proj = U @ W
        e = (proj * proj).sum(dim=1) / (fro2 / d)
        out[:, m] = e.numpy()
        del proj, e
    return out


def _fro2_list(mats: list[torch.Tensor]) -> np.ndarray:
    return np.array([float((W * W).sum()) for W in mats], dtype=np.float64)


def _norm_cdf(z):
    """Standard normal CDF (float64), scalar or array."""
    t = torch.as_tensor(z, dtype=torch.float64)
    return (0.5 * (1.0 + torch.erf(t / np.sqrt(2.0)))).numpy()


# ---------------------------------------------------------------------------
# subspace machinery (Arm 3)
# ---------------------------------------------------------------------------
def principal_angles(V: np.ndarray, R: np.ndarray) -> np.ndarray:
    """Ascending principal angles (radians) between the column spans of V and R."""
    Qv = np.linalg.qr(np.asarray(V, dtype=np.float64))[0]
    Qr = np.linalg.qr(np.asarray(R, dtype=np.float64))[0]
    s = np.linalg.svd(Qv.T @ Qr, compute_uv=False)
    s = np.clip(s, -1.0, 1.0)
    return np.arccos(s[::-1])


def subspace_discovery(V: np.ndarray, R: np.ndarray) -> dict:
    """SD = sum cos^2(theta) / dim(R), plus the angles in degrees."""
    th = principal_angles(V, R)
    q = R.shape[1]
    sd = float((np.cos(th) ** 2).sum() / q)
    return {"angles_deg": [float(np.degrees(t)) for t in th],
            "max_angle_deg": float(np.degrees(th.max())) if len(th) else 0.0,
            "SD": sd, "dim_R": int(q), "dim_V": int(V.shape[1])}


def energy_subspace(mats: list[torch.Tensor], R: torch.Tensor, d: int) -> np.ndarray:
    """e_R(W) = ||R^T W||_F^2 / (||W||_F^2/d) / dim(R), float64."""
    q = R.shape[1]
    Rd = R.to(torch.float64)
    out = np.empty(len(mats), dtype=np.float64)
    for i, W in enumerate(mats):
        Wd = W.to(torch.float64)
        fro2 = float((Wd * Wd).sum())
        pr = Rd.T @ Wd
        out[i] = float((pr * pr).sum()) / (fro2 / d) / q
        del Wd, pr
    return out


# ---------------------------------------------------------------------------
# THE routine
# ---------------------------------------------------------------------------
@torch.no_grad()
def analyse2(mats: list[torch.Tensor], layers: list[int], d: int, L: int, *,
             ks: tuple[int, ...] = (2, 4, 6, 8), n_random: int = 256, seed: int = 0,
             keep_profiles: bool = True,
             null_n: int = 512, null_seed: int = 1234,
             r: torch.Tensor | None = None,
             R_basis: torch.Tensor | None = None,
             n_bottom: int = 8,
             subset_null_k: int | None = 4, subset_null_S: int = 32,
             subset_null_seed: int = 99) -> dict:
    """Vendored W01-W05 + W05w(k) + per-window nulls + derivation + subspace."""
    t0 = time.time()
    if not mats:
        raise RuntimeError("no residual-write matrices")
    n_mat = len(mats)

    # ---------------- per-layer Grams (float32, archive order) ----------------
    layer_gram: dict[int, torch.Tensor] = {}
    for W, l in zip(mats, layers, strict=True):
        g = WS._gram(W)
        if l in layer_gram:
            layer_gram[l] += g
        else:
            layer_gram[l] = g
        del g
    present = sorted(layer_gram)

    # ---------------- pooled (BASELINE, vendored arithmetic) ----------------
    A = torch.zeros(d, d, dtype=torch.float32)
    for l in present:
        A += layer_gram[l]
    evals, evecs = torch.linalg.eigh(A.double())
    lam = np.clip(evals.numpy(), 1e-30, None)
    v1_64 = evecs[:, 0].clone()
    V_bottom = evecs[:, :n_bottom].numpy().copy()          # Arm 3
    v1 = v1_64.to(torch.float32)
    del A, evals, evecs

    g = torch.Generator(device="cpu").manual_seed(seed)
    R = torch.randn(n_random, d, generator=g).to(torch.float32)
    R = R / R.norm(dim=1, keepdim=True)
    U = torch.cat([v1.unsqueeze(0), R], dim=0)
    E = _energy_block(mats, U, d)                          # (1 + n_random, n_mat)
    e_v1 = E[0].astype(np.float64)
    # matrix-major flatten, so the concatenation order matches the vendored
    # `np.concatenate([e_rand_per_matrix])` exactly (quantiles are order-free,
    # but keeping the order identical removes one degree of freedom).
    e_rand = np.ascontiguousarray(E[1:].T).reshape(-1)
    del R, U, E
    out = WS._stats_from(lam, e_v1, e_rand, v1.numpy())
    out.pop("v1", None)
    del e_rand

    e64 = WS._energies64(mats, v1_64, d)
    out["e_v1_f64_min"] = float(e64.min())
    out["W05_f64"] = float(np.log10(max(e64.min(), 1e-300)))
    out["W05_f32_minus_f64"] = out["W05_abl_min_layer_energy"] - out["W05_f64"]
    out["hidden_size"] = d
    out["n_layers"] = L
    out["n_write_matrices"] = n_mat
    out["layer_of_matrix"] = [int(x) for x in layers]
    out["lam_second"] = float(lam[1])
    out["lam_max"] = float(lam[-1])
    out["fro2"] = [float(x) for x in _fro2_list(mats)]

    # ---------------- the shared NULL ensemble (Arm 2) ----------------
    gn = torch.Generator(device="cpu").manual_seed(null_seed)
    Un = torch.randn(null_n, d, generator=gn).to(torch.float32)
    Un = Un / Un.norm(dim=1, keepdim=True)
    E_null = _energy_block(mats, Un, d).astype(np.float64)   # (null_n, n_mat)
    del Un
    L10_null = np.log10(np.maximum(E_null, 1e-300))
    del E_null
    out["null_n"] = int(null_n)
    out["null_seed"] = int(null_seed)
    out["null_pooled_mu"] = float(L10_null.min(axis=1).mean())
    out["null_pooled_sd"] = float(L10_null.min(axis=1).std(ddof=1))

    # ---------------- ARM 4: derivation numbers ----------------
    if r is not None:
        r64 = unit64(r)
        e_r64 = WS._energies64(mats, r64, d)
        cos2 = float(torch.dot(v1_64, r64).item() ** 2)
        resid = e64 - e_r64 * cos2
        rel = resid / np.maximum(e64, 1e-300)
        i_arg = int(np.argmin(e64))
        i_max = int(np.argmax(np.abs(resid)))
        out["derivation"] = {
            "cos2_theta": cos2,
            "abscos_v1_r": float(abs(torch.dot(v1_64, r64).item())),
            "log10_min_e_r": float(np.log10(max(e_r64.min(), 1e-300))),
            "max_abs_residual": float(np.abs(resid).max()),
            "max_abs_rel_residual": float(np.abs(rel).max()),
            "argmax_residual_matrix": i_max,
            "argmin_matrix": i_arg,
            "e_W_v1_at_argmin": float(e64[i_arg]),
            "e_W_r_at_argmin": float(e_r64[i_arg]),
            "residual_at_argmin": float(resid[i_arg]),
            "rel_residual_at_argmin": float(rel[i_arg]),
            "e_W_v1": [float(x) for x in e64],
            "e_W_r": [float(x) for x in e_r64],
        }
    else:
        out["derivation"] = None

    # ---------------- ARM 3: subspace discovery on the pooled Gram ----------
    if R_basis is not None:
        Rb = R_basis.to(torch.float64)
        q = int(Rb.shape[1])
        sd_by_j = {}
        for j in range(1, n_bottom + 1):
            sd_by_j[str(j)] = subspace_discovery(V_bottom[:, :j], Rb.numpy())
        # j_star = the SMALLEST bottom-j eigenspace that CONTAINS R.
        #
        # Two corrections to the naive reading, both load-bearing.  (a) Principal
        # angles are symmetric and there are only min(j, q) of them, so for j < q
        # "all angles small" merely says V_j sits inside R -- it is vacuously true
        # for the leading eigenvectors of an edited model and says nothing about
        # containment of R.  j is therefore required to be at least q.  (b) "the
        # LARGEST j with small angles" is degenerate, because containment in V_j
        # implies containment in every larger V; the smallest such j is the
        # informative one and is the effective dimension of the edited subspace as
        # read from the bottom of the spectrum.
        j_star = 0
        for j in range(min(q, n_bottom), n_bottom + 1):
            s = sd_by_j[str(j)]
            if s["max_angle_deg"] <= 25.0 and s["SD"] >= 0.9:
                j_star = j
                break
        eR = energy_subspace(mats, Rb, d)
        out["subspace"] = {
            "dim_R": q,
            "SD_at_dimR": sd_by_j[str(min(q, n_bottom))]["SD"],
            "j_star": int(j_star),
            "sd_by_j": sd_by_j,
            "log10_min_e_R": float(np.log10(max(eR.min(), 1e-300))),
            "log10_mean_e_R": float(np.log10(max(eR.mean(), 1e-300))),
            "e_R": [float(x) for x in eR],
        }
    else:
        out["subspace"] = None
    # the bottom eigenvectors are needed by callers (Arm 3 surrogates) but must
    # never reach a JSON row; the leading underscore marks them for stripping.
    out["_V_bottom"] = V_bottom
    out["_v1_64"] = v1_64.numpy()

    # ---------------- windowed (OUR METHOD) + per-window nulls -------------
    lay_arr = np.asarray(layers)
    Lp = max(present) + 1
    w_by_k: dict[str, dict] = {}
    for k in tuple(ks) + (L,):
        key = "L" if k >= L else str(k)
        if key in w_by_k:
            continue
        wins = WS.windows_for(Lp, min(k, Lp))
        prev_v1 = None
        rows = []
        for (s, e) in wins:
            Aw = torch.zeros(d, d, dtype=torch.float32)
            n_mat_win = 0
            for l in present:
                if s <= l < e:
                    Aw += layer_gram[l]
                    n_mat_win += int((lay_arr == l).sum())
            ev, evec = torch.linalg.eigh(Aw.double())
            lw = np.clip(ev.numpy(), 1e-30, None)
            vw = evec[:, 0].clone()
            Vw_bottom = evec[:, :n_bottom].numpy().copy()
            del Aw, ev, evec
            idx = [i for i in range(n_mat) if s <= layers[i] < e]
            ews = WS._energies64([mats[i] for i in idx], vw, d)
            obs = float(np.log10(max(ews.min(), 1e-300)))
            cosv = None if prev_v1 is None else float(abs(torch.dot(vw, prev_v1)))
            prev_v1 = vw
            rank = int((lw > lw[-1] * (d * np.finfo(np.float64).eps)).sum())

            # per-window null: min over THIS window's matrices, per null direction
            nullw = L10_null[:, idx].min(axis=1)
            mu, sd = float(nullw.mean()), float(nullw.std(ddof=1))
            z = (obs - mu) / sd if sd > 0 else float("nan")
            p_emp = float((1 + int((nullw <= obs).sum())) / (len(nullw) + 1))
            p_par = float(_norm_cdf(z)) if np.isfinite(z) else float("nan")

            row = {
                "win_start": int(s), "win_end": int(e), "k": int(min(k, Lp)),
                "n_matrices": int(n_mat_win),
                "log10_e_min": obs,
                "log10_e_mean": float(np.log10(max(ews.mean(), 1e-300))),
                "cos_to_prev_v1": cosv,
                "lam_min": float(lw[0]), "lam_second": float(lw[1]),
                "lam_max": float(lw[-1]),
                "rank_numerical": rank, "d": int(d),
                "full_rank": bool(rank == d),
                "eig_gap_log10": float(np.log10(max(lw[1], 1e-300) / max(lw[0], 1e-300))),
                "null_mu": mu, "null_sd": sd,
                "null_q01": float(np.quantile(nullw, 0.01)),
                "null_q05": float(np.quantile(nullw, 0.05)),
                "null_min": float(nullw.min()),
                "z_win": z, "p_win_empirical": p_emp, "p_win_parametric": p_par,
            }
            if R_basis is not None:
                row["subspace_win"] = subspace_discovery(Vw_bottom[:, :max(1, R_basis.shape[1])],
                                                         R_basis.to(torch.float64).numpy())
            rows.append(row)
        logs = np.array([r_["log10_e_min"] for r_ in rows])
        coss = [r_["cos_to_prev_v1"] for r_ in rows if r_["cos_to_prev_v1"] is not None]
        nw = len(rows)
        p_emp_min = float(min(r_["p_win_empirical"] for r_ in rows))
        p_par_min = float(min(r_["p_win_parametric"] for r_ in rows))
        z_min = float(min(r_["z_win"] for r_ in rows))
        w_by_k[key] = {
            "k": int(min(k, Lp)),
            "n_windows": nw,
            "W05w": float(logs.min()),
            "argmin_window": [rows[int(logs.argmin())]["win_start"],
                              rows[int(logs.argmin())]["win_end"]],
            "consistency_c": float(min(coss)) if coss else 1.0,
            "mean_cos": float(np.mean(coss)) if coss else 1.0,
            "min_rank": int(min(r_["rank_numerical"] for r_ in rows)),
            "all_full_rank": bool(all(r_["full_rank"] for r_ in rows)),
            "z_min": z_min,
            "W05w_cal": z_min,
            "p_min_empirical": p_emp_min,
            "p_min_parametric": p_par_min,
            "p_sidak_empirical": float(1.0 - (1.0 - p_emp_min) ** nw),
            "p_bonf_empirical": float(min(1.0, p_emp_min * nw)),
            "p_sidak_parametric": float(1.0 - (1.0 - p_par_min) ** nw),
            "p_bonf_parametric": float(min(1.0, p_par_min * nw)),
            "p_empirical_floor": float(1.0 / (null_n + 1)),
            "profile": rows if keep_profiles else [],
        }
    out["windowed"] = w_by_k

    # ------------- the LAYER-SUBSET null (Arm 2, corrected) ----------------
    # The random-DIRECTION null above answers "is v1_win an unusual direction?",
    # and the answer is trivially yes for every model, edited or not: v1_win is
    # the MINIMISING eigenvector, not a random draw.  Measured on the unedited
    # host parent, z_min = -186 at k=2.  A null that rejects the negative
    # control is not a calibration, and that is reported as a finding rather
    # than repaired quietly.
    #
    # The null the multiple-window hazard actually needs is over WINDOWS, not
    # directions: given this model's own matrices, how deep does the window
    # statistic go for an ARBITRARY set of k layers?  Sampling S random k-subsets
    # gives that reference distribution F, and because the contiguous windows are
    # n_w draws from the same statistic, the exact multiple-window correction is
    # p = 1 - (1 - F(obs))^n_w.  A depth-LOCALISED edit lands in the tail of F; a
    # GLOBAL edit does not, because every k-subset sees it equally.
    if subset_null_k is not None and len(present) > subset_null_k:
        kk = int(subset_null_k)
        key = "L" if kk >= L else str(kk)
        if key in w_by_k:
            rng = np.random.default_rng(subset_null_seed)
            vals = []
            for _ in range(int(subset_null_S)):
                # an unrestricted draw: contiguous subsets stay in the null, which
                # is what makes it the reference distribution for a contiguous window
                sub = sorted(rng.choice(present, size=kk, replace=False).tolist())
                Aw = torch.zeros(d, d, dtype=torch.float32)
                for l in sub:
                    Aw += layer_gram[l]
                ev, evec = torch.linalg.eigh(Aw.double())
                vw = evec[:, 0].clone()
                del Aw, ev, evec
                idx = [i for i in range(n_mat) if layers[i] in sub]
                ews = WS._energies64([mats[i] for i in idx], vw, d)
                vals.append(float(np.log10(max(ews.min(), 1e-300))))
            vals = np.sort(np.asarray(vals))
            obs = w_by_k[key]["W05w"]
            nw = w_by_k[key]["n_windows"]
            F = float((1 + int((vals <= obs).sum())) / (len(vals) + 1))
            mu, sd = float(vals.mean()), float(vals.std(ddof=1))
            z = (obs - mu) / sd if sd > 0 else float("nan")
            out["subset_null"] = {
                "k": kk, "S": int(subset_null_S), "seed": int(subset_null_seed),
                "n_windows": nw,
                "null_mean": mu, "null_sd": sd,
                "null_min": float(vals.min()), "null_q05": float(np.quantile(vals, 0.05)),
                "observed_W05w": obs,
                "F_obs_empirical": F,
                "z_subset": z,
                "p_multiwindow_empirical": float(1.0 - (1.0 - F) ** nw),
                "p_multiwindow_parametric": float(
                    1.0 - (1.0 - float(_norm_cdf(z))) ** nw) if np.isfinite(z) else float("nan"),
                "p_empirical_floor": float(1.0 / (int(subset_null_S) + 1)),
                "null_values": [float(v) for v in vals],
            }
        else:
            out["subset_null"] = None
    else:
        out["subset_null"] = None

    out["wall_clock_s"] = time.time() - t0
    del layer_gram, L10_null
    return out


# ---------------------------------------------------------------------------
# identity gate against the vendored estimator
# ---------------------------------------------------------------------------
def gate_identity(mats: list[torch.Tensor], layers: list[int], d: int, L: int,
                  ks: tuple[int, ...] = (2, 4, 6, 8)) -> dict:
    """analyse2 must equal wstats.analyse on every vendored number."""
    a = WS.analyse(mats, layers, d, L, ks=ks, keep_profiles=False)
    b = analyse2(mats, layers, d, L, ks=ks, keep_profiles=False, null_n=32,
                 subset_null_k=None)
    keys = ["W01_abl_suppression_depth", "W02_abl_direction_consistency",
            "W03_abl_gap_vs_random", "W04_abl_isolation",
            "W05_abl_min_layer_energy", "W05q10_abl_p10_layer_energy", "W05_f64"]
    deltas = {k: abs(float(a[k]) - float(b[k])) for k in keys}
    for kk in a["windowed"]:
        deltas[f"W05w[{kk}]"] = abs(a["windowed"][kk]["W05w"] - b["windowed"][kk]["W05w"])
        deltas[f"c[{kk}]"] = abs(a["windowed"][kk]["consistency_c"]
                                 - b["windowed"][kk]["consistency_c"])
    return {"deltas": deltas, "max_delta": max(deltas.values()),
            "PASS": bool(max(deltas.values()) <= 1e-12)}


def read_config(path: Path):
    return WS.read_config(path)
