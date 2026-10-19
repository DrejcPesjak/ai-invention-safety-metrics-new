#!/usr/bin/env python3
"""Memory-lean W05 / W05w(k) scorer for 12B-class checkpoints.

Same estimator as round-5/experiment-1/src/wstats.py (whose window definition,
tensor selector and layer regex are IMPORTED, not re-implemented), but the
weights are never all held in RAM.  Instead every residual-write matrix W is
reduced on the fly to its normalised Gram

    G_W = W W^T / ||W||_F^2            (d x d, float64, cached on disk)

which is sufficient for everything the statistic needs:

    A_window   = sum_{W in window} G_W
    v1         = min eigenvector of A_window
    e(u, W)    = ||u^T W||^2 / (||W||_F^2 / d)  =  d * u^T G_W u

Deviation from the archive, declared: Grams are accumulated in float64 (the
archive accumulated float32).  W05 is insensitive to this (paper: reproduces to
1.3e-5); W01/W04 are the ones that drift and are not load-bearing here.

Stages
  grams  <src> <cache>   src = local model dir OR hf repo id (shards are
                         downloaded ONE AT A TIME and deleted after reduction)
  score  <cache> <out.json> [--ks 2,4]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import torch
from safetensors import safe_open
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "round-5" / "experiment-1" / "src"))
from wstats import LAYER_RE, classify_tensor, windows_for  # noqa: E402  (vendored estimator)

torch.set_num_threads(max(1, os.cpu_count() or 1))


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# --------------------------------------------------------------------------- grams
def _read_config(cfg: dict) -> tuple[int, int, str]:
    c = cfg.get("text_config", cfg)
    return int(c["hidden_size"]), int(c["num_hidden_layers"]), str(cfg.get("model_type", "?"))


def _reduce_shard(shard: Path, d: int, cache: Path, meta: list[dict]) -> int:
    n = 0
    with safe_open(str(shard), framework="pt", device="cpu") as f:
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
            t0 = time.time()
            W = f.get_tensor(name).to(torch.float64)
            fro2 = float((W * W).sum())
            if fro2 <= 0 or not np.isfinite(fro2):
                del W
                continue
            G = (W @ W.T) / fro2
            del W
            fn = name.replace("/", "_") + ".npy"
            np.save(cache / fn, G.numpy())
            del G
            meta.append({"name": name, "layer": int(m.group(1)), "kind": kind,
                         "shape": [int(s) for s in shape], "fro2": fro2, "file": fn})
            n += 1
            log(f"  {name} {list(shape)} -> gram in {time.time() - t0:.1f}s")
    return n


def stage_grams(src: str, cache: Path, max_shards: int | None = None) -> None:
    cache.mkdir(parents=True, exist_ok=True)
    meta_path = cache / "meta.json"
    done = json.load(open(meta_path)) if meta_path.exists() else {"matrices": [], "shards_done": []}
    local = Path(src).is_dir()
    if local:
        cfg = json.load(open(Path(src) / "config.json"))
        shards = sorted(p.name for p in Path(src).glob("*.safetensors"))
        fetch = lambda fn: Path(src) / fn  # noqa: E731
    else:
        from huggingface_hub import hf_hub_download
        mdir = HERE / "models" / src.replace("/", "__")
        mdir.mkdir(parents=True, exist_ok=True)
        cfg = json.load(open(hf_hub_download(src, "config.json", local_dir=str(mdir))))
        try:
            idx = json.load(open(hf_hub_download(src, "model.safetensors.index.json", local_dir=str(mdir))))
            shards = sorted(set(idx["weight_map"].values()))
        except Exception:
            shards = ["model.safetensors"]

        def fetch(fn: str) -> Path:
            log(f"downloading {src}/{fn}")
            return Path(hf_hub_download(src, fn, local_dir=str(mdir)))
    d, L, mt = _read_config(cfg)
    done.update({"src": src, "hidden_size": d, "n_layers": L, "model_type": mt,
                 "architectures": cfg.get("architectures")})
    todo = [s for s in shards if s not in done["shards_done"]]
    if max_shards is not None:
        todo = todo[:max_shards]
    log(f"{src}: d={d} L={L} type={mt}; {len(todo)} shard(s) to process")
    for s in todo:
        p = fetch(s)
        n = _reduce_shard(p, d, cache, done["matrices"])
        done["shards_done"].append(s)
        json.dump(done, open(meta_path, "w"), indent=1)
        if not local:
            os.remove(p)  # free disk before the next shard
            log(f"deleted {p.name} ({n} write matrices reduced)")
    log(f"grams complete: {len(done['matrices'])} write matrices in {cache}")


# --------------------------------------------------------------------------- score
def _min_evec(A: np.ndarray, full: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Smallest eigenvector; eigenvalues = full spectrum (pooled, for W01/W04) or the two smallest."""
    if full:
        w = eigh(A, eigvals_only=True, driver="evd")
        _, v = eigh(A, subset_by_index=[0, 0], driver="evr")
    else:
        w, v = eigh(A, subset_by_index=[0, 1], driver="evr")
    return np.clip(w, 1e-30, None), v[:, 0]


def stage_score(cache: Path, out: Path, ks: tuple[int, ...]) -> dict:
    meta = json.load(open(cache / "meta.json"))
    d, L = meta["hidden_size"], meta["n_layers"]
    mats = sorted(meta["matrices"], key=lambda c: (c["layer"], 0 if c["kind"] == "attn" else 1, c["name"]))
    layers = [m["layer"] for m in mats]
    present = sorted(set(layers))
    log(f"scoring {meta['src']}: {len(mats)} matrices over {len(present)}/{L} layers, d={d}")

    def gram(m):
        return np.load(cache / m["file"], mmap_mode="r")

    def layer_gram(l):
        A = np.zeros((d, d), dtype=np.float64)
        for m in mats:
            if m["layer"] == l:
                A += gram(m)
        return A

    def energies(u, idx):
        return np.array([d * float(u @ gram(mats[i]) @ u) for i in idx])

    t0 = time.time()
    # pooled (k = L)
    A = np.zeros((d, d), dtype=np.float64)
    lay_cache: dict[int, np.ndarray] = {}
    for l in present:
        lay_cache[l] = layer_gram(l)
        A += lay_cache[l]
    lam, v1 = _min_evec(A, full=True)
    del A
    e_v1 = energies(v1, range(len(mats)))
    res = {
        "src": meta["src"], "model_type": meta["model_type"], "hidden_size": d,
        "n_layers": L, "layers_present": present, "n_write_matrices": len(mats),
        "W05": float(np.log10(max(e_v1.min(), 1e-300))),
        "W01": float(np.log10(np.median(lam) / lam[0])),
        "W04": float(np.log10(lam[1] / lam[0])),
        "W02": float((e_v1 < 0.1).mean()),
        "lam_min": float(lam[0]), "lam_second": float(lam[1]), "lam_median": float(np.median(lam)),
        "e_v1_per_matrix": [{"name": m["name"], "layer": m["layer"], "log10_e": float(np.log10(max(e, 1e-300)))}
                            for m, e in zip(mats, e_v1)],
        "windowed": {},
    }
    log(f"pooled W05={res['W05']:.4f}  W04={res['W04']:.3f}  ({time.time() - t0:.0f}s)")

    Lp = max(present) + 1
    for k in ks:
        if k >= L:
            continue
        rows, prev = [], None
        for (s, e) in windows_for(Lp, k):
            idx = [i for i in range(len(mats)) if s <= layers[i] < e]
            if not idx:
                continue  # window entirely inside a missing-layer gap
            Aw = np.zeros((d, d), dtype=np.float64)
            for l in present:
                if s <= l < e:
                    Aw += lay_cache[l]
            lw, vw = _min_evec(Aw)
            del Aw
            ews = energies(vw, idx)
            cosv = None if prev is None else float(abs(np.dot(vw, prev)))
            prev = vw
            rows.append({"win_start": s, "win_end": e, "n_matrices": len(idx),
                         "log10_e_min": float(np.log10(max(ews.min(), 1e-300))),
                         "log10_e_mean": float(np.log10(max(ews.mean(), 1e-300))),
                         "argmin_matrix": mats[idx[int(ews.argmin())]]["name"],
                         "lam_min": float(lw[0]), "lam_second": float(lw[1]),
                         "cos_to_prev_v1": cosv})
            log(f"  k={k} win [{s},{e}) log10_e_min={rows[-1]['log10_e_min']:.3f} cos_prev={cosv}")
        coss = [r["cos_to_prev_v1"] for r in rows if r["cos_to_prev_v1"] is not None]
        res["windowed"][str(k)] = {
            "W05w": float(min(r["log10_e_min"] for r in rows)),
            "argmin_window": min(rows, key=lambda r: r["log10_e_min"])["win_start"],
            "consistency_c": float(min(coss)) if coss else None,
            "n_windows": len(rows), "windows": rows,
        }
        log(f"W05w(k={k}) = {res['windowed'][str(k)]['W05w']:.4f}  c={res['windowed'][str(k)]['consistency_c']}")
    res["seconds"] = time.time() - t0
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(out, "w"), indent=1)
    log(f"wrote {out}")
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grams"); g.add_argument("src"); g.add_argument("cache"); g.add_argument("--max-shards", type=int)
    s = sub.add_parser("score"); s.add_argument("cache"); s.add_argument("out"); s.add_argument("--ks", default="2,4")
    a = ap.parse_args()
    if a.cmd == "grams":
        stage_grams(a.src, Path(a.cache), a.max_shards)
    else:
        stage_score(Path(a.cache), Path(a.out), tuple(int(x) for x in a.ks.split(",")))


if __name__ == "__main__":
    main()
