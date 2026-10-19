#!/usr/bin/env python3
"""W01-W05 (VENDORED, unchanged) + W05w (NEW: sliding-layer-window generalisation).

The W01-W05 half of this file is vendored from the iteration-3 archive
(`gen_art_experiment_2/lib_scan.py` + `lib_score._stats_from`) so that the
baseline statistic in this artifact is byte-for-byte the same estimator that
produced the archived numbers.  Do not edit those functions.  W05w is added
BELOW them and re-uses the *identical* residual-write-matrix selector, so the
pooled statistic and the windowed statistic differ ONLY in the pooling scope.

Definitions
-----------
    A      = sum_m  W_m W_m^T / ||W_m||_F^2                (d x d)
    lam    = eigenvalues of A ascending; v1 = eigenvector of lam[0]
    e(u,W) = ||u^T W||^2 / (||W||_F^2 / d)

    W01 = log10(median(lam)/lam[0])     W02 = mean(e(v1,W_m) < 0.1)
    W03 = log10(q05(e_rand)/mean(e_v1)) W04 = log10(lam[1]/lam[0])
    W05 = log10(min_m e(v1, W_m))                        <-- POOLED, the baseline

    W05w(k) = min over windows of  log10( min_{m in window} e(v1_win, W_m) )
    where a window is k CONSECUTIVE LAYERS, stride = max(1, k//2), ragged tails
    dropped, and v1_win is the minimum eigenvector of the Gram accumulated over
    that window's matrices only.  By construction W05w(L) == W05 exactly.

    c(k)      = min over ADJACENT window pairs of |cos(v1_win_i, v1_win_{i+1})|
    W05wc(k,tau) = W05w(k) if c(k) >= tau else +inf ("not a global edit")
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import numpy as np
import torch
from safetensors import safe_open

# ---------------------------------------------------------------------------
# VENDORED, unchanged: residual-write matrix resolution (lib_model/lib_scan)
# ---------------------------------------------------------------------------
ATTN_WRITE_SUFFIX = ("o_proj", "out_proj", "attention.dense", "dense", "attn.c_proj", "wo")
MLP_WRITE_SUFFIX = ("down_proj", "dense_4h_to_h", "fc2", "c_proj", "w2")

LAYER_RE = re.compile(r"(?:^|\.)(?:layers|h|blocks|block)\.(\d+)\.")

DECLARED_RE = re.compile(
    r"abliterat|gabliterat|orthogonaliz|uncensor|unalign|jailbr|nsfw|dolphin|dan-|amoral",
    re.IGNORECASE)


def classify_tensor(name: str) -> str | None:
    """'attn' | 'mlp' | None, matching lib_model.resolve_write_matrices semantics."""
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


def read_config(path: Path) -> tuple[int, int, str, dict]:
    """(d, L, model_type, raw_cfg) using the archive's key-resolution order."""
    cfgp = path / "config.json"
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
    if d <= 0 or L <= 0:
        raise RuntimeError(f"unresolved config (d={d}, L={L})")
    if mt in ("gpt2", "gptj", "gpt_bigcode"):
        raise RuntimeError(f"transposed Conv1D-style weights not supported ({mt})")
    return d, L, mt, cfg


def load_write_matrices(path: Path, d: int, L: int, mt: str
                        ) -> tuple[list[torch.Tensor], list[int], list[str]]:
    """All residual-write matrices as float32 [d, d_in], in the ARCHIVE's order.

    The archive's comment is load-bearing and is preserved here: float32
    summation is not associative and lam[0] on an abliterated model sits ~5
    orders below the trace, so the accumulation ORDER (layer, attn-before-mlp,
    then name) must be identical or W01/W04 drift by ~8e-3.
    """
    shards = sorted(path.glob("*.safetensors"))
    if not shards:
        raise RuntimeError("no shards")
    catalog: list[tuple[Path, str, int, str]] = []
    for sh in shards:
        with safe_open(str(sh), framework="pt", device="cpu") as f:
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
                           f"expected ~{n_expected} (d={d}, L={L}, {mt})")
    catalog.sort(key=lambda c: (c[2], 0 if c[3] == "attn" else 1, c[1]))
    handles = {sh: safe_open(str(sh), framework="pt", device="cpu")
               for sh in {c[0] for c in catalog}}
    mats, layers, names = [], [], []
    for sh, name, layer, _kind in catalog:
        W = handles[sh].get_tensor(name).to(torch.float32)
        fro2 = float((W * W).sum())
        if fro2 <= 0 or not np.isfinite(fro2):
            del W
            continue
        mats.append(W)
        layers.append(layer)
        names.append(name)
    del handles
    return mats, layers, names


# ---------------------------------------------------------------------------
# VENDORED, unchanged: the pooled statistics  (lib_score._stats_from)
# ---------------------------------------------------------------------------
def _stats_from(lam: np.ndarray, e_v1: np.ndarray, e_rand: np.ndarray,
                v1: np.ndarray) -> dict:
    return {
        "W01_abl_suppression_depth": float(np.log10(np.median(lam) / lam[0])),
        "W02_abl_direction_consistency": float((e_v1 < 0.1).mean()),
        "W03_abl_gap_vs_random": float(np.log10(
            max(np.quantile(e_rand, 0.05), 1e-30) / max(e_v1.mean(), 1e-30))),
        "W04_abl_isolation": float(np.log10(lam[1] / lam[0])),
        "W05_abl_min_layer_energy": float(np.log10(max(e_v1.min(), 1e-30))),
        "W05q10_abl_p10_layer_energy": float(np.log10(
            max(float(np.quantile(e_v1, 0.10)), 1e-30))),
        "e_v1": [float(x) for x in e_v1],
        "lam_min": float(lam[0]), "lam_median": float(np.median(lam)),
        "v1": v1,
    }


# ---------------------------------------------------------------------------
# NEW: window machinery
# ---------------------------------------------------------------------------
def windows_for(L: int, k: int) -> list[tuple[int, int]]:
    """[start, end) layer windows of width k, stride max(1, k//2), ragged tail dropped."""
    k = min(k, L)
    stride = max(1, k // 2)
    out = []
    for s in range(0, L, stride):
        e = min(s + k, L)
        if e - s >= k:
            out.append((s, e))
    if not out:
        out = [(0, L)]
    return out


@torch.no_grad()
def _gram(W: torch.Tensor) -> torch.Tensor:
    fro2 = float((W * W).sum())
    return (W @ W.T) / fro2


@torch.no_grad()
def _energies64(mats: list[torch.Tensor], u64: torch.Tensor, d: int) -> np.ndarray:
    """e(u, W) in float64 for every matrix.  u64 must be a float64 unit vector."""
    out = np.empty(len(mats), dtype=np.float64)
    for i, W in enumerate(mats):
        Wd = W.double()
        fro2 = float((Wd * Wd).sum())
        pr = u64 @ Wd
        out[i] = float((pr * pr).sum()) / (fro2 / d)
        del Wd, pr
    return out


@torch.no_grad()
def analyse(mats: list[torch.Tensor], layers: list[int], d: int, L: int, *,
            ks: tuple[int, ...] = (2, 4, 6, 8), n_random: int = 256, seed: int = 0,
            keep_profiles: bool = True) -> dict:
    """Pooled W01-W05 (baseline) + windowed W05w for every k, from one weight load."""
    t0 = time.time()
    if not mats:
        raise RuntimeError("no residual-write matrices")

    # ---- per-layer Grams (float32, archive dtype), summed in catalog order ----
    layer_gram: dict[int, torch.Tensor] = {}
    for W, l in zip(mats, layers):
        g = _gram(W)
        if l in layer_gram:
            layer_gram[l] += g
        else:
            layer_gram[l] = g
        del g
    present = sorted(layer_gram)

    # ---- pooled (BASELINE) ----
    A = torch.zeros(d, d, dtype=torch.float32)
    for l in present:
        A += layer_gram[l]
    evals, evecs = torch.linalg.eigh(A.double())
    lam = np.clip(evals.numpy(), 1e-30, None)
    v1_64 = evecs[:, 0].clone()
    v1 = v1_64.to(torch.float32)
    del A, evals, evecs

    g = torch.Generator(device="cpu").manual_seed(seed)
    R = torch.randn(n_random, d, generator=g).to(torch.float32)
    R = R / R.norm(dim=1, keepdim=True)
    U = torch.cat([v1.unsqueeze(0), R], dim=0)
    e_v1, e_rand = [], []
    for W in mats:
        fro2 = float((W * W).sum())
        proj = U @ W
        e = (proj * proj).sum(dim=1) / (fro2 / d)
        e_v1.append(float(e[0]))
        e_rand.append(e[1:].numpy())
        del proj, e
    del R, U
    e_v1 = np.array(e_v1)
    out = _stats_from(lam, e_v1, np.concatenate(e_rand), v1.numpy())
    out.pop("v1", None)

    # float64 energies along the SAME eigenvector.  The vendored path above keeps
    # the archive's float32 arithmetic so W01-W05 reproduce the archived numbers
    # exactly; the float64 copy exists because a perfectly annihilated direction
    # (e ~ 1e-13 on an exact synthetic rank-1 removal) is pure cancellation noise
    # in float32, and the windowed statistic must be compared against something
    # stable.  On real checkpoints e_v1 ~ 1e-5 and the two agree to ~1e-9.
    e64 = _energies64(mats, v1_64, d)
    out["e_v1_f64_min"] = float(e64.min())
    out["W05_f64"] = float(np.log10(max(e64.min(), 1e-300)))
    out["W05_f32_minus_f64"] = out["W05_abl_min_layer_energy"] - out["W05_f64"]
    out["hidden_size"] = d
    out["n_layers"] = L
    out["n_write_matrices"] = len(mats)
    out["layer_of_matrix"] = [int(x) for x in layers]
    out["lam_second"] = float(lam[1])
    out["lam_max"] = float(lam[-1])

    # ---- windowed (OUR METHOD) ----
    lay_arr = np.asarray(layers)
    Lp = max(present) + 1
    w_by_k: dict[str, dict] = {}
    profiles: list[dict] = []
    for k in tuple(ks) + (L,):
        key = "L" if k >= L else str(k)
        if key in w_by_k:
            continue
        wins = windows_for(Lp, min(k, Lp))
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
            vw = evec[:, 0].clone()                     # float64
            del Aw, ev, evec
            idx = [i for i in range(len(mats)) if s <= layers[i] < e]
            ews = _energies64([mats[i] for i in idx], vw, d)
            cosv = None if prev_v1 is None else float(abs(torch.dot(vw, prev_v1)))
            prev_v1 = vw
            # numerical rank of the window Gram (relative to the largest eigenvalue)
            rank = int((lw > lw[-1] * (d * np.finfo(np.float64).eps)).sum())
            rows.append({
                "win_start": int(s), "win_end": int(e), "k": int(min(k, Lp)),
                "n_matrices": int(n_mat_win),
                "log10_e_min": float(np.log10(max(ews.min(), 1e-300))),
                "log10_e_mean": float(np.log10(max(ews.mean(), 1e-300))),
                "cos_to_prev_v1": cosv,
                "lam_min": float(lw[0]), "lam_second": float(lw[1]),
                "lam_max": float(lw[-1]),
                "rank_numerical": rank, "d": int(d),
                "full_rank": bool(rank == d),
                "eig_gap_log10": float(np.log10(max(lw[1], 1e-300) / max(lw[0], 1e-300))),
            })
        logs = np.array([r["log10_e_min"] for r in rows])
        coss = [r["cos_to_prev_v1"] for r in rows if r["cos_to_prev_v1"] is not None]
        w_by_k[key] = {
            "k": int(min(k, Lp)),
            "n_windows": len(rows),
            "W05w": float(logs.min()),
            "argmin_window": [rows[int(logs.argmin())]["win_start"],
                              rows[int(logs.argmin())]["win_end"]],
            "consistency_c": float(min(coss)) if coss else 1.0,
            "mean_cos": float(np.mean(coss)) if coss else 1.0,
            "min_rank": int(min(r["rank_numerical"] for r in rows)),
            "all_full_rank": bool(all(r["full_rank"] for r in rows)),
            "profile": rows if keep_profiles else [],
        }
    out["windowed"] = w_by_k
    out["wall_clock_s"] = time.time() - t0
    del layer_gram
    return out


def w05wc(win: dict, k: str, tau: float) -> float:
    """Consistency-gated windowed statistic: +inf when the windows disagree."""
    e = win[k]
    return e["W05w"] if e["consistency_c"] >= tau else float("inf")


@torch.no_grad()
def score_dir(path: Path, *, ks: tuple[int, ...] = (2, 4, 6, 8),
              n_random: int = 256, seed: int = 0, keep_profiles: bool = True) -> dict:
    d, L, mt, _cfg = read_config(path)
    mats, layers, _names = load_write_matrices(path, d, L, mt)
    out = analyse(mats, layers, d, L, ks=ks, n_random=n_random, seed=seed,
                  keep_profiles=keep_profiles)
    out["model_type"] = mt
    del mats
    return out
