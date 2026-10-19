#!/usr/bin/env python3
"""E_1 -- the PARENT-REQUIRING incumbent weight signal (the baseline).

    dW   = W_parent - W_candidate,  over o_proj and down_proj in the MID-STACK band
    E_1  = mean_m  sigma_1^2(dW_m) / sum_i sigma_i^2(dW_m)

BAND.  The source's "mid-stack" is not numerically specified, so we read it as
the relative layer range [0.25 L, 0.75 L) and record that this is OUR reading.
The band is reported with every value.

Singular values come from `torch.linalg.svdvals` in float32 -- never from
`sqrt(eigvalsh(W W^T))`, which squares the condition number.

E_1 needs no forward passes but DOES need the parent, which is the whole point
of the head-to-head against the parent-free W05.
"""

from __future__ import annotations

import time

import numpy as np
import torch
from loguru import logger

from hubio import load_config, read_tensors, safetensor_key_map

BAND_LO, BAND_HI = 0.25, 0.75
SUFFIXES = (".o_proj.weight", ".down_proj.weight", ".self_attn.dense.weight",
            ".attention.dense.weight", ".mlp.dense_4h_to_h.weight",
            ".attn.c_proj.weight", ".mlp.c_proj.weight", ".wo.weight", ".w2.weight",
            ".out_proj.weight", ".fc2.weight")


def _layer_of(key: str) -> int | None:
    parts = key.split(".")
    for i, p in enumerate(parts):
        if p.isdigit() and i > 0 and parts[i - 1] in ("layers", "h", "blocks", "block",
                                                      "decoder", "transformer"):
            return int(p)
    # generic fallback: first bare integer segment
    for p in parts:
        if p.isdigit():
            return int(p)
    return None


def band_keys(path: str, n_layers: int) -> list[str]:
    lo, hi = int(BAND_LO * n_layers), int(BAND_HI * n_layers)
    keys = []
    for k in safetensor_key_map(path):
        if not k.endswith(SUFFIXES):
            continue
        li = _layer_of(k)
        if li is None or not (lo <= li < hi):
            continue
        keys.append(k)
    return sorted(keys)


def e1_pair(parent_path: str, cand_path: str, *, device: str = "cuda",
            max_matrices: int | None = None) -> dict:
    """E_1 for one (parent, candidate) pair.  Returns a fully self-describing row."""
    t0 = time.time()
    pc, cc = load_config(parent_path), load_config(cand_path)
    Lp, Lc = int(pc["num_hidden_layers"]), int(cc["num_hidden_layers"])
    guard = {"parent_layers": Lp, "cand_layers": Lc,
             "parent_hidden": int(pc["hidden_size"]), "cand_hidden": int(cc["hidden_size"]),
             "parent_vocab": int(pc.get("vocab_size", -1)),
             "cand_vocab": int(cc.get("vocab_size", -1))}
    if Lp != Lc or pc["hidden_size"] != cc["hidden_size"]:
        return {"ok": False, "skip_reason": "shape_mismatch", **guard}
    if guard["parent_vocab"] != guard["cand_vocab"]:
        return {"ok": False, "skip_reason": "vocab_mismatch", **guard}

    kp, kc = set(band_keys(parent_path, Lp)), set(band_keys(cand_path, Lc))
    keys = sorted(kp & kc)
    n_dropped = len(kp | kc) - len(keys)
    if max_matrices:
        keys = keys[:max_matrices]
    if not keys:
        return {"ok": False, "skip_reason": "no_shared_band_matrices", **guard}

    dev = torch.device(device if torch.cuda.is_available() and device == "cuda" else "cpu")
    ratios, identical = [], 0
    # read shard-by-shard on BOTH sides, one key at a time to bound memory
    for k in keys:
        tp = read_tensors(parent_path, [k]).get(k)
        tc = read_tensors(cand_path, [k]).get(k)
        if tp is None or tc is None or tp.shape != tc.shape:
            continue
        dW = (tp.to(dev, torch.float32) - tc.to(dev, torch.float32))
        del tp, tc
        nrm = float(dW.pow(2).sum())
        if nrm <= 0 or not np.isfinite(nrm):
            identical += 1
            del dW
            continue
        s = torch.linalg.svdvals(dW)
        s2 = s.pow(2)
        ratios.append(float(s2[0] / s2.sum().clamp_min(1e-30)))
        del dW, s, s2
    if not ratios:
        return {"ok": False, "skip_reason": "all_matrices_identical",
                "n_identical": identical, **guard}
    r = np.array(ratios)
    return {"ok": True, "E1": float(r.mean()), "E1_median": float(np.median(r)),
            "E1_max": float(r.max()), "E1_min": float(r.min()),
            "n_matrices": len(ratios), "n_identical_matrices": identical,
            "n_keys_dropped_unshared": n_dropped,
            "band": [BAND_LO, BAND_HI], "band_layers": [int(BAND_LO * Lp), int(BAND_HI * Lp)],
            "band_note": "our reading of 'mid-stack'; the source is not numerically specific",
            "seconds": round(time.time() - t0, 2), **guard}


def e1_from_state_dicts(parent_sd: dict[str, torch.Tensor],
                        cand_sd: dict[str, torch.Tensor], n_layers: int,
                        *, device: str = "cuda") -> dict:
    """E_1 for an in-memory pair (used for the synthetic edits, whose parent is
    the unedited model already resident)."""
    t0 = time.time()
    lo, hi = int(BAND_LO * n_layers), int(BAND_HI * n_layers)
    keys = sorted(k for k in (set(parent_sd) & set(cand_sd))
                  if k.endswith(SUFFIXES) and (_layer_of(k) is not None)
                  and lo <= _layer_of(k) < hi)
    dev = torch.device(device if torch.cuda.is_available() and device == "cuda" else "cpu")
    ratios, identical = [], 0
    for k in keys:
        dW = parent_sd[k].to(dev, torch.float32) - cand_sd[k].to(dev, torch.float32)
        if float(dW.pow(2).sum()) <= 0:
            identical += 1
            del dW
            continue
        s2 = torch.linalg.svdvals(dW).pow(2)
        ratios.append(float(s2[0] / s2.sum().clamp_min(1e-30)))
        del dW, s2
    if not ratios:
        return {"ok": False, "skip_reason": "all_matrices_identical", "n_identical": identical}
    r = np.array(ratios)
    return {"ok": True, "E1": float(r.mean()), "E1_median": float(np.median(r)),
            "E1_max": float(r.max()), "E1_min": float(r.min()),
            "n_matrices": len(ratios), "n_identical_matrices": identical,
            "band": [BAND_LO, BAND_HI], "band_layers": [lo, hi],
            "seconds": round(time.time() - t0, 2)}


def selftest() -> dict:
    """Internal check D: E_1 on a synthetic GLOBAL RANK-ONE edit must be ~1.0 by
    construction (the delta IS rank one); a dense benign perturbation must not."""
    d, din, L = 128, 256, 8
    g = torch.Generator().manual_seed(3)
    r = torch.randn(d, generator=g)
    r = r / r.norm()
    P = torch.eye(d) - torch.outer(r, r)
    parent, rank1, dense = {}, {}, {}
    for li in range(L):
        for suf in ("self_attn.o_proj.weight", "mlp.down_proj.weight"):
            k = f"model.layers.{li}.{suf}"
            W = torch.randn(d, din, generator=g)
            parent[k] = W
            rank1[k] = P @ W
            dense[k] = W + 0.01 * torch.randn(d, din, generator=g)
    a = e1_from_state_dicts(parent, rank1, L, device="cpu")
    b = e1_from_state_dicts(parent, dense, L, device="cpu")
    assert a["E1"] > 0.999, a
    assert b["E1"] < 0.10, b
    assert a["n_matrices"] == 8, a  # 4 mid-stack layers x 2 matrices
    logger.info(f"E1 selftest: rank-one {a['E1']:.4f} vs dense {b['E1']:.4f}")
    return {"rank_one_edit_E1": a["E1"], "dense_benign_E1": b["E1"],
            "n_matrices": a["n_matrices"], "pass": True}


if __name__ == "__main__":
    import json
    print(json.dumps(selftest(), indent=2))
