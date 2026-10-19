#!/usr/bin/env python3
"""The parent-free weight statistic W01-W05, plus the uniformity indices this
artifact adds, computed from an ORDERED list of residual-write matrices.

Semantics are copied from the archived iteration-3 implementations, which are
vendored byte-identically alongside this file:

  vendored_lib_metrics.compute_weights(rn, n_random=256, seed=0)   [Runner path]
  vendored_lib_scan.weights_from_safetensors(path, ...)            [fast path]

Both accumulate  A += (W @ W.T) / ||W||_F^2  over the residual-write matrices in
(layer, attn-before-mlp, name) order -- the order is load-bearing because
float32 summation is not associative and lam[0] on an abliterated checkpoint sits
~5 orders of magnitude below the trace.  eigh runs in float64.

What this module adds over the vendored code:
  * the same statistic on an arbitrary in-memory matrix list, so an in-house
    edit kernel can be applied and scored without writing a checkpoint to disk;
  * the per-LAYER suppressed-energy profile (min/mean over the 2 matrices);
  * three uniformity indices (U_ratio, U_iqr, U_frac);
  * energy along a GIVEN direction r (needed for the closed-form W05(w) check);
  * |cos(v1, r)| for the mechanism check.
"""

from __future__ import annotations

import json
import math
import re
import time
from pathlib import Path

import numpy as np
import torch
from safetensors import safe_open

from vendored_lib_model import ATTN_WRITE_SUFFIX, MLP_WRITE_SUFFIX

EPS = 1e-12

# The archived, panel-fitted detection threshold.  Detect <=> W05 <= TAU.
TAU = -2.7415117804288127

LAYER_RE = re.compile(r"(?:^|\.)(?:layers|h|blocks|block)\.(\d+)\.")

# eligibility floor: below this the minimum-over-matrices statistic is degenerate
MIN_LAYERS = 8
MIN_HIDDEN = 128

QUANT_MARKERS = ("gptq", "awq", "bnb", "bitsandbytes", "mlx", "gguf", "fp8", "int4",
                 "int8", "quanto", "aqlm", "hqq", "eetq", "compressed-tensors")


def classify_tensor(name: str) -> str | None:
    """'attn' | 'mlp' | None -- identical semantics to vendored_lib_scan."""
    if not name.endswith(".weight"):
        return None
    stem = name[: -len(".weight")]
    low = stem.lower()
    leaf = low.rsplit(".", 1)[-1]
    attn_leaves = {s.split(".")[-1] for s in ATTN_WRITE_SUFFIX}
    mlp_leaves = {s.split(".")[-1] for s in MLP_WRITE_SUFFIX}
    if leaf in attn_leaves and ("attn" in low or "attention" in low):
        return "attn"
    if leaf in mlp_leaves and ("mlp" in low or "ffn" in low or "feed" in low):
        return "mlp"
    return None


# --------------------------------------------------------------------------
# config resolution + eligibility
# --------------------------------------------------------------------------
def read_config(path: Path) -> dict:
    cfgp = Path(path) / "config.json"
    if not cfgp.exists():
        raise RuntimeError("no config.json")
    cfg = json.loads(cfgp.read_text())
    tcfg = (cfg.get("text_config") or cfg.get("llm_config")
            or cfg.get("language_config") or cfg)

    def _get(c, keys):
        for k in keys:
            v = c.get(k)
            if isinstance(v, int) and v > 0:
                return v
        return 0

    dk = ("hidden_size", "n_embd", "n_embed", "d_model", "hidden_dim", "model_dim")
    lk = ("num_hidden_layers", "n_layer", "n_layers", "num_layers",
          "num_transformer_layers")
    d, L = _get(tcfg, dk), _get(tcfg, lk)
    if d == 0 or L == 0:
        for v in cfg.values():
            if isinstance(v, dict):
                d = d or _get(v, dk)
                L = L or _get(v, lk)
    mt = str(tcfg.get("model_type") or cfg.get("model_type", "unknown"))
    return {"d": d, "L": L, "model_type": mt, "raw": cfg,
            "quantization_config": cfg.get("quantization_config")}


def eligibility(cfg: dict, file_names: list[str]) -> tuple[bool, str]:
    """Return (eligible, reason).  Applied identically to positives and negatives."""
    low_files = " ".join(f.lower() for f in file_names)
    if cfg.get("quantization_config"):
        return False, "UNRESOLVED_QUANTIZED:quantization_config present in config.json"
    for m in QUANT_MARKERS:
        if m in low_files:
            return False, f"UNRESOLVED_QUANTIZED:file list mentions '{m}'"
    if cfg["d"] <= 0 or cfg["L"] <= 0:
        return False, f"UNRESOLVED_CONFIG:d={cfg['d']} L={cfg['L']}"
    if cfg["model_type"] in ("gpt2", "gptj", "gpt_bigcode"):
        return False, f"UNSUPPORTED_ARCH:transposed Conv1D weights ({cfg['model_type']})"
    if cfg["L"] < MIN_LAYERS:
        return False, f"DEGENERATE:n_layers={cfg['L']} < {MIN_LAYERS}"
    if cfg["d"] < MIN_HIDDEN:
        return False, f"DEGENERATE:hidden_size={cfg['d']} < {MIN_HIDDEN}"
    return True, "ok"


# --------------------------------------------------------------------------
# loading the write matrices in the canonical order
# --------------------------------------------------------------------------
def load_write_matrices(path: Path, device: str = "cpu",
                        dtype: torch.dtype | None = None):
    """(mats, layers, kinds, names, cfg) in canonical (layer, attn<mlp, name) order."""
    path = Path(path)
    cfg = read_config(path)
    d, L = cfg["d"], cfg["L"]
    shards = sorted(path.glob("*.safetensors"))
    if not shards:
        raise RuntimeError("no shards")
    catalog: list[tuple[Path, str, int, str]] = []
    handles = {}
    for sh in shards:
        f = safe_open(str(sh), framework="pt", device="cpu")
        handles[sh] = f
        for name in f.keys():
            kind = classify_tensor(name)
            if kind is None:
                continue
            m = LAYER_RE.search(name)
            if m is None:
                continue
            shape = f.get_slice(name).get_shape()
            if len(shape) != 2 or shape[0] != d:
                continue
            catalog.append((sh, name, int(m.group(1)), kind))
    n_expected = 2 * L
    if len(catalog) < 0.8 * n_expected:
        raise RuntimeError(f"UNRESOLVED architecture: {len(catalog)} write matrices, "
                           f"expected ~{n_expected} (d={d}, L={L}, {cfg['model_type']})")
    catalog.sort(key=lambda c: (c[2], 0 if c[3] == "attn" else 1, c[1]))
    mats, layers, kinds, names = [], [], [], []
    for sh, name, layer, kind in catalog:
        W = handles[sh].get_tensor(name)
        W = W.to(device) if dtype is None else W.to(device, dtype)
        mats.append(W)
        layers.append(layer)
        kinds.append(kind)
        names.append(name)
    del handles
    return mats, layers, kinds, names, cfg


# --------------------------------------------------------------------------
# the statistic
# --------------------------------------------------------------------------
@torch.no_grad()
def stats_from_mats(mats: list[torch.Tensor], layers: list[int], *,
                    n_random: int = 256, seed: int = 0, device: str = "cpu",
                    extra_dirs: dict[str, torch.Tensor] | None = None,
                    accum_dtype: torch.dtype = torch.float32) -> dict:
    """W01-W05 (+W05q10) + per-layer profile + uniformity indices.

    `mats` MUST already be in the canonical accumulation order.
    `extra_dirs` maps a label -> unit direction; per-matrix normalised energy
    along each is returned as e_<label>, which is what the closed-form W05(w)
    prediction and the |cos(v1,r)| mechanism check consume.
    """
    t0 = time.time()
    dev = torch.device(device)
    d = int(mats[0].shape[0])
    A = torch.zeros(d, d, dtype=accum_dtype, device=dev)
    fro2s: list[float] = []
    for W in mats:
        Wf = W.to(dev, torch.float32)
        fro2 = float((Wf * Wf).sum())
        fro2s.append(fro2)
        if fro2 <= 0 or not np.isfinite(fro2):
            continue
        if accum_dtype == torch.float32:
            A += (Wf @ Wf.T) / fro2
        else:
            Wd = Wf.to(accum_dtype)
            A += (Wd @ Wd.T) / fro2
            del Wd
        del Wf

    evals, evecs = torch.linalg.eigh(A.double().cpu())
    lam = np.clip(evals.numpy(), 1e-30, None)
    v1 = evecs[:, 0].to(dev, torch.float32)
    del A, evals, evecs

    g = torch.Generator(device="cpu").manual_seed(seed)
    R = torch.randn(n_random, d, generator=g).to(dev, torch.float32)
    R = R / R.norm(dim=1, keepdim=True)
    labels = list((extra_dirs or {}).keys())
    stack = [v1.unsqueeze(0)]
    for lab in labels:
        u = (extra_dirs[lab]).to(dev, torch.float32)
        u = u / (u.norm() + EPS)
        stack.append(u.unsqueeze(0))
    stack.append(R)
    U = torch.cat(stack, dim=0)

    e_v1, e_rand, keep_layers = [], [], []
    e_extra: dict[str, list[float]] = {lab: [] for lab in labels}
    for W, fro2, lay in zip(mats, fro2s, layers, strict=True):
        if fro2 <= 0 or not np.isfinite(fro2):
            continue
        Wf = W.to(dev, torch.float32)
        proj = U @ Wf
        e = (proj * proj).sum(dim=1) / (fro2 / d)
        e_v1.append(float(e[0]))
        for i, lab in enumerate(labels):
            e_extra[lab].append(float(e[1 + i]))
        e_rand.append(e[1 + len(labels):].cpu().numpy())
        keep_layers.append(int(lay))
        del Wf, proj, e
    del R, U

    e_v1 = np.array(e_v1)
    e_rand_all = np.concatenate(e_rand)
    out = {
        "W01_abl_suppression_depth": float(np.log10(np.median(lam) / lam[0])),
        "W02_abl_direction_consistency": float((e_v1 < 0.1).mean()),
        "W03_abl_gap_vs_random": float(np.log10(
            max(np.quantile(e_rand_all, 0.05), 1e-30) / max(e_v1.mean(), 1e-30))),
        "W04_abl_isolation": float(np.log10(lam[1] / lam[0])),
        "W05_abl_min_layer_energy": float(np.log10(max(e_v1.min(), 1e-30))),
        "W05q10_abl_p10_layer_energy": float(np.log10(
            max(float(np.quantile(e_v1, 0.10)), 1e-30))),
        "lam_min": float(lam[0]),
        "lam_median": float(np.median(lam)),
        "lam_second": float(lam[1]),
        "n_write_matrices": len(e_v1),
        "hidden_size": d,
        "e_v1": [float(x) for x in e_v1],
        "fro2": [float(x) for x in fro2s],
        "accum_dtype": str(accum_dtype),
        "layer_of_matrix": keep_layers,
        "v1": v1.cpu().numpy(),
        "wall_clock_s": time.time() - t0,
    }
    out.update(uniformity(e_v1))
    out["layer_profile"] = layer_profile(e_v1, keep_layers)
    for lab in labels:
        arr = np.array(e_extra[lab])
        out[f"e_{lab}"] = [float(x) for x in arr]
        out[f"log10_min_e_{lab}"] = float(np.log10(max(arr.min(), 1e-30)))
        u = extra_dirs[lab].to(dev, torch.float32)
        u = u / (u.norm() + EPS)
        out[f"abscos_v1_{lab}"] = float(abs(float(v1 @ u)))
    return out


def uniformity(e_v1: np.ndarray) -> dict:
    """Three scalar uniformity indices.  All are log10 SPREADS of the per-matrix
    suppressed energy: a uniform edit suppresses every matrix equally, so the
    spread collapses; a depth-weighted or per-head edit leaves exceptions."""
    e = np.asarray(e_v1, dtype=np.float64)
    emin = max(float(e.min()), 1e-30)
    return {
        "U_ratio": float(np.log10(max(float(e.max()), 1e-30) / emin)),
        "U_iqr": float(np.log10(max(float(np.quantile(e, 0.75)), 1e-30) /
                                max(float(np.quantile(e, 0.25)), 1e-30))),
        "U_frac": float((e < 0.1).mean()),
    }


def layer_profile(e_v1: np.ndarray, layers: list[int]) -> list[dict]:
    """Per-layer min / mean over that layer's residual-write matrices."""
    e = np.asarray(e_v1, dtype=np.float64)
    prof: dict[int, list[float]] = {}
    for val, lay in zip(e, layers, strict=True):
        prof.setdefault(int(lay), []).append(float(val))
    out = []
    for lay in sorted(prof):
        v = np.array(prof[lay])
        out.append({"layer": lay, "n": int(len(v)),
                    "log10_min_e_v1": float(np.log10(max(v.min(), 1e-30))),
                    "log10_mean_e_v1": float(np.log10(max(v.mean(), 1e-30)))})
    return out


@torch.no_grad()
def wstats_fast(path: Path, *, n_random: int = 256, seed: int = 0,
                device: str = "cpu", extra_dirs=None,
                accum_dtype: torch.dtype = torch.float32) -> dict:
    """Score a local snapshot from stored tensors alone -- no transformers, no
    forward pass, no prompt."""
    mats, layers, kinds, names, cfg = load_write_matrices(path, device="cpu")
    out = stats_from_mats(mats, layers, n_random=n_random, seed=seed, device=device,
                          extra_dirs=extra_dirs, accum_dtype=accum_dtype)
    out.update({"n_layers": cfg["L"], "model_type": cfg["model_type"]})
    del mats
    return out


# --------------------------------------------------------------------------
# the sub-unit closed form
# --------------------------------------------------------------------------
def subunit_closed_form(e_r_parent, fro2_parent, d: int, w: float) -> dict:
    """Predicted log10 of the MINIMUM per-matrix energy along r after a uniform
    sub-unit edit  W <- W - w * outer(r, r@W).

    LEADING form (the one the plan stamps):
        log10 min_m e_m(w) = log10 min_m e_m(0) + 2*log10(1-w)

    That is exact in the numerator -- the energy along r really does scale as
    (1-w)^2 -- but the statistic normalises by the EDITED matrix's own Frobenius
    norm, and that norm shrinks by exactly the energy that was removed:

        F_m(w) = F_m(0) - (1 - (1-w)^2) * a_m,     a_m = ||r^T W_m||^2

    so the EXACT prediction is

        e_m(w) = (1-w)^2 * a_m * d / (F_m(0) - (1 - (1-w)^2) * a_m).

    Both are returned.  The leading form is off by ~a_m/F_m ~ 1/d, which is
    0.005 log units at d=64 and ~1e-4 at d=2048 -- small, but larger than the
    1e-6 tolerance the artifact tests everything else at, so it is worth being
    exact about.
    """
    e0 = np.asarray(e_r_parent, dtype=np.float64)
    F = np.asarray(fro2_parent, dtype=np.float64)
    a = e0 * F / d
    lead = float(np.log10(max(e0.min(), 1e-30)) + 2 * math.log10(max(1 - w, 1e-30))) \
        if w < 1 else float("-inf")
    if w >= 1:
        return {"leading": lead, "exact": float("-inf")}
    num = (1 - w) ** 2 * a * d
    den = F - (1 - (1 - w) ** 2) * a
    e_w = num / np.maximum(den, 1e-30)
    return {"leading": lead, "exact": float(np.log10(max(e_w.min(), 1e-30)))}


def solve_w_star(e_r_parent, fro2_parent, d: int, tau: float) -> dict:
    """Smallest uniform sub-unit weight w whose predicted minimum energy along r
    reaches the detection threshold tau.  Bisection on the EXACT form; the
    leading form is solved in closed form for comparison."""
    e0 = np.asarray(e_r_parent, dtype=np.float64)
    lead = 1.0 - 10 ** ((tau - float(np.log10(max(e0.min(), 1e-30)))) / 2.0)
    lo, hi = 0.0, 1.0 - 1e-12
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if subunit_closed_form(e_r_parent, fro2_parent, d, mid)["exact"] <= tau:
            hi = mid
        else:
            lo = mid
    return {"w_star_leading": float(lead), "w_star_exact": float(hi)}


# --------------------------------------------------------------------------
# E_1: the parent-REQUIRING collision-paper baseline (arXiv:2604.08844 lineage)
#      E_1 = mean_m sigma_1^2(dW) / sum_i sigma_i^2(dW),  dW = W_parent - W_child
# --------------------------------------------------------------------------
@torch.no_grad()
def top_sigma2(dW: torch.Tensor, iters: int = 200, tol: float = 1e-9,
               seed: int = 0) -> tuple[float, int]:
    """sigma_1(dW)^2 by power iteration on dW dW^T.

    A full SVD of a 2560 x 9728 delta costs seconds and there are ~56 of them
    per checkpoint; power iteration costs milliseconds and is exact to
    machine precision here because an abliteration delta is very nearly
    rank-one, which is the regime power iteration converges fastest in.
    Validated against torch.linalg.svdvals in the unit tests.
    """
    g = torch.Generator(device="cpu").manual_seed(seed)
    v = torch.randn(dW.shape[0], generator=g).to(dW.device, dW.dtype)
    v = v / v.norm()
    lam = 0.0
    for i in range(iters):
        w = dW @ (dW.T @ v)
        n = float(w.norm())
        if n <= 0:
            return 0.0, i
        v = w / n
        if abs(n - lam) <= tol * max(n, 1.0):
            return float(n), i + 1
        lam = n
    return float(lam), iters


@torch.no_grad()
def e1_baseline(child_mats, parent_mats, layers, L: int, device: str = "cpu",
                check_svd: int = 2) -> dict:
    """E_1 = mean_m sigma_1^2(dW_m) / sum_i sigma_i^2(dW_m), dW = W_child - W_parent.

    Computed ONCE per matrix and then aggregated over three depth bands, so the
    bands cost nothing extra.
    """
    per_matrix, checks = [], []
    for i, (Wc, Wp, lay) in enumerate(zip(child_mats, parent_mats, layers,
                                          strict=True)):
        dW = (Wc.to(device, torch.float32) - Wp.to(device, torch.float32))
        tot = float((dW * dW).sum())            # = sum_i sigma_i^2
        if tot <= 0 or not math.isfinite(tot):
            del dW
            continue
        s1sq, n_iter = top_sigma2(dW)
        val = s1sq / tot
        if len(checks) < check_svd:
            exact = float(torch.linalg.svdvals(dW.double())[0] ** 2) / tot
            checks.append({"layer": int(lay), "power_iteration": val,
                           "svd": exact, "abs_dev": abs(val - exact),
                           "n_iter": n_iter})
        per_matrix.append({"layer": int(lay), "E1": val, "fro2": tot})
        del dW
    bands = {"mid50": (0.25, 0.75), "full": (0.0, 1.0), "mid20": (0.4, 0.6)}
    out = {"E1_power_iteration_vs_svd_check": checks,
           "E1_per_matrix": [round(m["E1"], 6) for m in per_matrix]}
    for tag, (lo, hi) in bands.items():
        vals = [m["E1"] for m in per_matrix
                if lo <= m["layer"] / max(L - 1, 1) <= hi]
        out[f"E1_{tag}"] = float(np.mean(vals)) if vals else float("nan")
        out[f"E1_{tag}_n"] = len(vals)
    # how much of the parent-child delta is in the band at all
    out["E1_n_identical_matrices"] = sum(1 for m in per_matrix if m["fro2"] <= 0)
    return out
