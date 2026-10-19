#!/usr/bin/env python3
"""Abliteration kernels, laundering treatments and quantization round-trips.

The uniform edit primitive and the merge / add-back / fake-quant treatments are
adapted from the iteration-3 archive (`lib_ablate.py`) so that root A rebuilds
bit-for-bit.  NEW here:

  * `ablate_sd_kernel` -- depth-weighted (mlabonne-v2-style Gaussian) abliteration,
    the non-uniform root the experiment needs;
  * `quant_sd_bits`    -- a dependency-free reference quantizer at an ARBITRARY
    bit-width (symmetric per-output-channel round-to-nearest, optional blocking),
    which is what makes the rounding-noise sweep possible;
  * `dequantize_from_bnb` -- bitsandbytes round-trip + explicit dequantization back
    to fp16, used as a cross-check on the reference quantizer at 4 bits.

Every treatment returns a PLAIN fp/bf16 state_dict: nothing downstream ever sees a
packed quantized tensor, so the weight statistics are always computed on real
dequantized values.
"""

from __future__ import annotations

import math

import numpy as np
import torch

EPS = 1e-12
CHUNK_ELEMS = 16 * 1024 ** 2      # ~64 MB of float32 per temporary


# ==========================================================================
# state-dict plumbing
# ==========================================================================
def write_matrix_keys(rn) -> list[dict]:
    """Full state_dict keys of the residual-write matrices, with layer + kind."""
    mod2name = {id(m): n for n, m in rn.model.named_modules()}
    out = []
    for l in range(rn.L):
        for tag, mod in rn.write_matrices(l):
            full = mod2name.get(id(mod))
            if full is None:
                raise RuntimeError(f"could not resolve full name for {tag} at layer {l}")
            out.append({"layer": l, "kind": tag.split(":")[0], "key": f"{full}.weight"})
    return out


def embed_key(rn) -> str | None:
    emb = rn.model.get_input_embeddings()
    for n, m in rn.model.named_modules():
        if m is emb:
            return f"{n}.weight"
    return None


def snapshot_sd(rn) -> dict[str, torch.Tensor]:
    """CPU copy of every parameter, for merging / restoring."""
    return {k: v.detach().to("cpu").clone() for k, v in rn.model.state_dict().items()}


@torch.no_grad()
def load_sd(rn, sd: dict[str, torch.Tensor]) -> None:
    live = rn.model.state_dict()
    n = 0
    for k, v in sd.items():
        if k in live:
            live[k].copy_(v.to(live[k].device, live[k].dtype))
            n += 1
    assert n == len(sd), f"loaded {n}/{len(sd)} tensors"
    rn._write_cache.clear()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def _row_chunks(t: torch.Tensor):
    assert t.dim() >= 1, "0-dim tensors must be handled by the caller"
    if t.numel() <= CHUNK_ELEMS:
        yield 0, t.shape[0]
        return
    per_row = max(t.numel() // t.shape[0], 1)
    step = max(int(CHUNK_ELEMS // per_row), 1)
    for i in range(0, t.shape[0], step):
        yield i, min(i + step, t.shape[0])


# ==========================================================================
# the edit primitives
# ==========================================================================
@torch.no_grad()
def ablate_sd(sd: dict[str, torch.Tensor], keys: list[str], r: torch.Tensor,
              emb_key: str | None = None) -> dict[str, torch.Tensor]:
    """UNIFORM: W <- W - outer(r, r@W) on every listed key (archive-identical)."""
    out = dict(sd)
    rf = r.to(torch.float32)
    rf = rf / rf.norm()
    for k in keys:
        W = sd[k].to(torch.float32)
        out[k] = (W - torch.outer(rf, rf @ W)).to(sd[k].dtype)
        del W
    if emb_key is not None:
        E = sd[emb_key]
        o = torch.empty_like(E)
        for a, b in _row_chunks(E):
            blk = E[a:b].to(torch.float32)
            o[a:b] = (blk - torch.outer(blk @ rf, rf)).to(E.dtype)
            del blk
        out[emb_key] = o
    return out


def gaussian_kernel(n_layers: int, l_peak: float, sigma: float, scale: float = 1.0
                    ) -> np.ndarray:
    """mlabonne-v2-style depth kernel: w_l = scale * exp(-(l-l_peak)^2 / (2 sigma^2)).

    Clipped to [0, 1]: an ablation weight above 1 would OVER-project (flip the sign
    of the component) rather than merely suppress it.
    """
    l = np.arange(n_layers, dtype=np.float64)
    w = scale * np.exp(-((l - l_peak) ** 2) / (2.0 * max(sigma, 1e-9) ** 2))
    return np.clip(w, 0.0, 1.0)


@torch.no_grad()
def ablate_sd_kernel(sd: dict[str, torch.Tensor], key_rows: list[dict],
                     r: torch.Tensor, weights: np.ndarray) -> dict[str, torch.Tensor]:
    """DEPTH-WEIGHTED: W_l <- W_l - w_l * outer(r, r@W_l), w_l from `weights[layer]`."""
    out = dict(sd)
    rf = r.to(torch.float32)
    rf = rf / rf.norm()
    for row in key_rows:
        w_l = float(weights[row["layer"]])
        k = row["key"]
        if w_l <= 0.0:
            out[k] = sd[k].clone()
            continue
        W = sd[k].to(torch.float32)
        out[k] = (W - w_l * torch.outer(rf, rf @ W)).to(sd[k].dtype)
        del W
    return out


@torch.no_grad()
def merge_sd(root: dict, parent: dict, w: float) -> dict:
    """(1-w)*root + w*parent over EVERY floating parameter tensor, block-wise."""
    out = {}
    for k, v in root.items():
        p = parent.get(k)
        if p is None or p.shape != v.shape or not v.is_floating_point():
            out[k] = v.clone()
            continue
        if v.dim() == 0:
            out[k] = ((1.0 - w) * v.float() + w * p.float()).to(v.dtype)
            continue
        o = torch.empty_like(v)
        for a, b in _row_chunks(v):
            o[a:b] = ((1.0 - w) * v[a:b].to(torch.float32)
                      + w * p[a:b].to(torch.float32)).to(v.dtype)
        out[k] = o
    return out


@torch.no_grad()
def addback_sd(root: dict, parent: dict, keys: list[str], u: torch.Tensor,
               eps: float) -> dict:
    """ADD-BACK-ALL: W <- W + eps * outer(u, u @ W_parent) on every listed key."""
    out = dict(root)
    uf = u.to(torch.float32)
    uf = uf / uf.norm()
    for k in keys:
        p, r0 = parent[k], root[k]
        c = torch.zeros(p.shape[1], dtype=torch.float32)
        for a, b in _row_chunks(p):
            c += uf[a:b] @ p[a:b].to(torch.float32)
        o = torch.empty_like(r0)
        for a, b in _row_chunks(r0):
            o[a:b] = (r0[a:b].to(torch.float32)
                      + eps * torch.outer(uf[a:b], c)).to(r0.dtype)
        out[k] = o
        del c
    return out


# ==========================================================================
# quantization round-trips (quantize -> DEQUANTIZE back to the model dtype)
# ==========================================================================
_NF4 = torch.tensor([
    -1.0, -0.6961928009986877, -0.5250730514526367, -0.39491748809814453,
    -0.28444138169288635, -0.18477343022823334, -0.09105003625154495, 0.0,
    0.07958029955625534, 0.16093020141124725, 0.24611230194568634, 0.33791524171829224,
    0.44070982933044434, 0.5626170039176941, 0.7229568362236023, 1.0], dtype=torch.float32)

# fp4 (e2m1) positive levels, the other bitsandbytes 4-bit type.
_FP4 = torch.tensor([-12.0, -8.0, -6.0, -4.0, -3.0, -2.0, -1.0, 0.0,
                     1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0], dtype=torch.float32) / 12.0


@torch.no_grad()
def _levels_roundtrip(W: torch.Tensor, levels: torch.Tensor, gsz: int = 64
                      ) -> torch.Tensor:
    """Blockwise absmax scaling onto a fixed level set (bitsandbytes NF4/FP4 shape)."""
    flat = W.reshape(-1)
    pad = (-flat.numel()) % gsz
    if pad:
        flat = torch.cat([flat, torch.zeros(pad, dtype=flat.dtype, device=flat.device)])
    G = flat.reshape(-1, gsz)
    lv = levels.to(W.device, W.dtype)
    out = torch.empty_like(G)
    step = max(int(CHUNK_ELEMS // (gsz * len(lv))), 1)
    for i in range(0, G.shape[0], step):
        blk = G[i:i + step]
        s = blk.abs().amax(dim=1, keepdim=True).clamp_min(1e-12)
        idx = (blk.div(s).unsqueeze(-1) - lv.view(1, 1, -1)).abs().argmin(dim=-1)
        out[i:i + step] = lv[idx] * s
    Q = out.reshape(-1)
    if pad:
        Q = Q[:-pad]
    return Q.reshape(W.shape)


@torch.no_grad()
def quant_sd(sd: dict, mode: str, min_elems: int = 1024) -> tuple[dict, dict]:
    """Archive-identical fake-quant round-trip for the named schemes.

    IMPORTANT FRAMING (this is what ARM 1 turns on): the output is ALREADY
    dequantized -- a plain bf16 tensor holding the ROUNDED values.  'Dequantizing
    the checkpoint' therefore cannot recover anything the archive did not already
    have; see results/arm1_framing.json.
    """
    out, skipped, touched, errs = {}, [], 0, []
    for k, v in sd.items():
        if v.dim() != 2 or v.numel() < min_elems or not v.is_floating_point():
            out[k] = v.clone()
            if v.dim() == 2 and v.numel() >= min_elems:
                skipped.append(k)
            continue
        if mode == "int4" and v.shape[1] % 128 != 0:
            skipped.append(k)
            out[k] = v.clone()
            continue
        o = torch.empty_like(v)
        num2, den2 = 0.0, 0.0
        for a, b in _row_chunks(v):
            W = v[a:b].to(torch.float32)
            if mode == "int8":
                s = W.abs().amax(dim=1, keepdim=True).clamp_min(1e-12) / 127.0
                Q = torch.round(W / s).clamp(-127, 127) * s
            elif mode == "int4":
                G = W.reshape(W.shape[0], -1, 128)
                s = G.abs().amax(dim=2, keepdim=True).clamp_min(1e-12) / 7.0
                Q = (torch.round(G / s).clamp(-7, 7) * s).reshape(W.shape)
            elif mode == "nf4":
                Q = _levels_roundtrip(W, _NF4)
            elif mode == "fp4":
                Q = _levels_roundtrip(W, _FP4)
            else:
                raise ValueError(mode)
            num2 += float(((Q - W) ** 2).sum())
            den2 += float((W ** 2).sum())
            o[a:b] = Q.to(v.dtype)
            del W, Q
        errs.append(float(np.sqrt(num2) / (np.sqrt(den2) + EPS)))
        out[k] = o
        touched += 1
    return out, {"mode": mode, "n_quantized": touched, "n_skipped_2d": len(skipped),
                 "skipped_examples": skipped[:8],
                 "rel_frobenius_error_mean": float(np.mean(errs)) if errs else float("nan"),
                 "rel_frobenius_error_max": float(np.max(errs)) if errs else float("nan")}


@torch.no_grad()
def quant_sd_bits(sd: dict, bits: int, group: int = 64, min_elems: int = 1024
                  ) -> tuple[dict, dict]:
    """DEPENDENCY-FREE REFERENCE QUANTIZER at an arbitrary bit-width.

    Symmetric round-to-nearest onto 2^(bits-1)-1 levels with per-block absmax
    scaling (block size `group` along the input dimension, mimicking nf4 blocking).
    This isolates pure ROUNDING NOISE from bitsandbytes' double-quantization and
    outlier handling, which is exactly what the bit-width sweep needs.
    """
    qmax = float(2 ** (bits - 1) - 1)
    assert qmax >= 1.0, bits
    out, touched, errs = {}, 0, []
    for k, v in sd.items():
        if v.dim() != 2 or v.numel() < min_elems or not v.is_floating_point():
            out[k] = v.clone()
            continue
        o = torch.empty_like(v)
        num2, den2 = 0.0, 0.0
        for a, b in _row_chunks(v):
            W = v[a:b].to(torch.float32)
            n_in = W.shape[1]
            g = group if n_in % group == 0 else n_in     # per-output-channel fallback
            G = W.reshape(W.shape[0], -1, g)
            s = G.abs().amax(dim=2, keepdim=True).clamp_min(1e-12) / qmax
            Q = (torch.round(G / s).clamp(-qmax, qmax) * s).reshape(W.shape)
            num2 += float(((Q - W) ** 2).sum())
            den2 += float((W ** 2).sum())
            o[a:b] = Q.to(v.dtype)
            del W, G, Q
        errs.append(float(np.sqrt(num2) / (np.sqrt(den2) + EPS)))
        out[k] = o
        touched += 1
    return out, {"mode": f"ref{bits}bit", "bits": bits, "group": group,
                 "n_quantized": touched,
                 "rel_frobenius_error_mean": float(np.mean(errs)) if errs else float("nan"),
                 "rel_frobenius_error_max": float(np.max(errs)) if errs else float("nan")}


@torch.no_grad()
def bnb_roundtrip(sd: dict, quant_type: str = "nf4", min_elems: int = 1024
                  ) -> tuple[dict, dict]:
    """True bitsandbytes quantize -> dequantize cross-check (4-bit only).

    Returns (state_dict, meta).  meta['available'] is False (and the input is
    returned unchanged) when bitsandbytes is not importable or the GPU rejects it --
    the reference quantizer then carries the sweep on its own, which the fallback
    plan explicitly allows.
    """
    meta = {"mode": f"bnb_{quant_type}", "available": False, "n_quantized": 0}
    try:
        import bitsandbytes.functional as bnbF
    except Exception as e:                                    # noqa: BLE001
        meta["error"] = f"{type(e).__name__}: {e}"
        return {k: v.clone() for k, v in sd.items()}, meta
    if not torch.cuda.is_available():
        meta["error"] = "no CUDA device"
        return {k: v.clone() for k, v in sd.items()}, meta
    out, errs, touched = {}, [], 0
    try:
        for k, v in sd.items():
            if v.dim() != 2 or v.numel() < min_elems or not v.is_floating_point():
                out[k] = v.clone()
                continue
            W = v.to("cuda", torch.float16)
            q, state = bnbF.quantize_4bit(W, quant_type=quant_type, blocksize=64)
            D = bnbF.dequantize_4bit(q, state, quant_type=quant_type, blocksize=64)
            err = float((D.float() - W.float()).norm() / (W.float().norm() + EPS))
            errs.append(err)
            out[k] = D.to("cpu", v.dtype)
            touched += 1
            del W, q, state, D
        torch.cuda.empty_cache()
    except Exception as e:                                    # noqa: BLE001
        meta["error"] = f"{type(e).__name__}: {e}"
        return {k: v.clone() for k, v in sd.items()}, meta
    meta.update({"available": True, "n_quantized": touched,
                 "rel_frobenius_error_mean": float(np.mean(errs)) if errs else float("nan"),
                 "rel_frobenius_error_max": float(np.max(errs)) if errs else float("nan")})
    return out, meta


def kernel_uniformity(e_v1: list[float]) -> float:
    """max/min of the per-write-matrix v1 energy: ~1 for a uniform edit, >>1 non-uniform."""
    a = np.asarray(e_v1, dtype=np.float64)
    return float(a.max() / max(a.min(), 1e-30))


def sd_max_abs_delta(a: dict, b: dict) -> float:
    m = 0.0
    for k, v in a.items():
        w = b.get(k)
        if w is None or w.shape != v.shape or not v.is_floating_point():
            continue
        for lo, hi in _row_chunks(v):
            m = max(m, float((v[lo:hi].to(torch.float32)
                              - w[lo:hi].to(torch.float32)).abs().max()))
    return m


def n_tensors_identical(a: dict, b: dict) -> tuple[int, int]:
    """(#bit-identical, #compared) over the shared keys."""
    same, tot = 0, 0
    for k, v in a.items():
        w = b.get(k)
        if w is None or w.shape != v.shape:
            continue
        tot += 1
        if bool(torch.equal(v, w)):
            same += 1
    return same, tot


def depth_profile_summary(e_v1: list[float], layer_of: list[int]) -> dict:
    """Per-LAYER (not per-matrix) energy summary: which layers lost the suppression."""
    by_layer: dict[int, list[float]] = {}
    for e, l in zip(e_v1, layer_of):
        by_layer.setdefault(int(l), []).append(float(e))
    layers = sorted(by_layer)
    mins = [min(by_layer[l]) for l in layers]
    return {"layers": layers, "log10_min_energy_per_layer": [
        float(math.log10(max(m, 1e-30))) for m in mins]}
