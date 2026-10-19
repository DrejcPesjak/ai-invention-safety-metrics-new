#!/usr/bin/env python3
"""ARM 2: score arbitrary Hub checkpoints from STORED TENSORS ONLY.

No transformers instantiation, no forward pass, no prompt. Streams the
.safetensors shards, accumulates the shared Gram matrix over the residual-write
matrices, and returns exactly the same W01-W05 (+W05q10) the Runner path returns.
Gate T4 asserts the two paths agree to 1e-3.
"""

from __future__ import annotations

import json
import re
import shutil
import time
from pathlib import Path

import numpy as np
import torch
from loguru import logger
from safetensors import safe_open

from lib_model import ATTN_WRITE_SUFFIX, MLP_WRITE_SUFFIX
from lib_score import _stats_from

DECLARED_RE = re.compile(
    r"abliterat|gabliterat|orthogonaliz|uncensor|unalign|jailbr|nsfw|dolphin|dan-|amoral",
    re.IGNORECASE)

LAYER_RE = re.compile(r"(?:^|\.)(?:layers|h|blocks|block)\.(\d+)\.")

PANEL_FAMILIES = {"qwen2", "qwen3", "llama", "gemma2", "olmo", "gpt_neox", "smollm-llama"}


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


def download(repo: str, cache_dir: Path, revision: str | None = None,
             max_bytes: int = 12 * 1024 ** 3) -> tuple[Path, int]:
    from huggingface_hub import HfApi, snapshot_download
    api = HfApi()
    info = api.model_info(repo, revision=revision, files_metadata=True)
    st = [f for f in info.siblings if f.rfilename.endswith(".safetensors")]
    if not st:
        raise RuntimeError("no .safetensors files")
    tot = sum(f.size or 0 for f in st)
    if tot > max_bytes:
        raise RuntimeError(f"repo tensors {tot / 1e9:.1f} GB exceed cap")
    p = snapshot_download(repo, revision=revision, cache_dir=str(cache_dir),
                          allow_patterns=["*.safetensors", "config.json", "*.index.json"])
    return Path(p), tot


@torch.no_grad()
def weights_from_safetensors(path: Path, n_random: int = 256, seed: int = 0,
                             device: str = "cpu") -> dict:
    """W01-W05 + W05q10 from stored tensors alone."""
    t0 = time.time()
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
    if d == 0 or L == 0:                       # nested config not at a known key
        for v in cfg.values():
            if isinstance(v, dict):
                d = d or _get(v, dk)
                L = L or _get(v, lk)
    mt = str(tcfg.get("model_type") or cfg.get("model_type", "unknown"))
    if d <= 0 or L <= 0:
        raise RuntimeError(f"unresolved config (d={d}, L={L})")
    if mt in ("gpt2", "gptj", "gpt_bigcode"):
        raise RuntimeError(f"transposed Conv1D-style weights not supported ({mt})")

    shards = sorted(path.glob("*.safetensors"))
    if not shards:
        raise RuntimeError("no shards")

    # -- pass 1: locate the write matrices ---------------------------------
    catalog: list[tuple[Path, str, int, str]] = []      # (shard, name, layer, kind)
    for sh in shards:
        with safe_open(str(sh), framework="pt", device="cpu") as f:
            for name in f.keys():
                kind = classify_tensor(name)
                if kind is None:
                    continue
                m = LAYER_RE.search(name)
                if m is None:
                    continue
                sl = f.get_slice(name)
                shape = sl.get_shape()
                if len(shape) != 2 or shape[0] != d:
                    continue
                catalog.append((sh, name, int(m.group(1)), kind))
    n_expected = 2 * L
    if len(catalog) < 0.8 * n_expected:
        raise RuntimeError(f"UNRESOLVED architecture: {len(catalog)} write matrices, "
                           f"expected ~{n_expected} (d={d}, L={L}, {mt})")

    # float32 summation is not associative, and lam[0] on an abliterated model sits
    # ~5 orders below the trace, so accumulation ORDER is load-bearing: the Runner
    # path walks (layer, attn-before-mlp), and the scan must walk it identically or
    # W01/W04 drift by ~8e-3. Verified by gate T4.
    catalog.sort(key=lambda c: (c[2], 0 if c[3] == "attn" else 1, c[1]))
    handles = {sh: safe_open(str(sh), framework="pt", device="cpu")
               for sh in {c[0] for c in catalog}}

    dev = torch.device(device)
    A = torch.zeros(d, d, dtype=torch.float32, device=dev)
    for sh, name, _layer, _kind in catalog:
        W = handles[sh].get_tensor(name).to(dev, torch.float32)
        fro2 = float((W * W).sum())
        if fro2 <= 0 or not np.isfinite(fro2):
            del W
            continue
        A += (W @ W.T) / fro2
        del W

    evals, evecs = torch.linalg.eigh(A.double().cpu())
    lam = np.clip(evals.numpy(), 1e-30, None)
    v1 = evecs[:, 0].to(dev, torch.float32)
    del A, evals, evecs

    g = torch.Generator(device="cpu").manual_seed(seed)
    R = torch.randn(n_random, d, generator=g).to(dev, torch.float32)
    R = R / R.norm(dim=1, keepdim=True)
    U = torch.cat([v1.unsqueeze(0), R], dim=0)
    e_v1, e_rand, layers_of = [], [], []
    for sh, name, layer, _kind in catalog:
        W = handles[sh].get_tensor(name).to(dev, torch.float32)
        fro2 = float((W * W).sum())
        if fro2 <= 0 or not np.isfinite(fro2):
            del W
            continue
        proj = U @ W
        e = (proj * proj).sum(dim=1) / (fro2 / d)
        e_v1.append(float(e[0]))
        e_rand.append(e[1:].cpu().numpy())
        layers_of.append(layer)
        del W, proj, e
    del R, U, handles
    out = _stats_from(lam, np.array(e_v1), np.concatenate(e_rand), v1.cpu().numpy())
    out.pop("v1", None)
    out.update({"hidden_size": d, "n_layers": L, "model_type": mt,
                "n_write_matrices": len(catalog), "layer_of_matrix": layers_of,
                "wall_clock_s": time.time() - t0})
    return out


def purge(repo_path: Path, cache_dir: Path) -> int:
    """Delete the snapshot's blobs; return freed bytes."""
    # snapshot_download returns .../models--org--name/snapshots/<sha>
    root = repo_path
    for _ in range(3):
        if root.name.startswith("models--"):
            break
        root = root.parent
    if not root.name.startswith("models--") or not str(root).startswith(str(cache_dir)):
        return 0
    freed = sum(f.stat().st_size for f in root.rglob("*") if f.is_file())
    shutil.rmtree(root, ignore_errors=True)
    return freed


# ==========================================================================
# enumeration + adjudication
# ==========================================================================
def enumerate_candidates(exclude_repos: set[str], limit: int = 1500,
                         max_params: float = 4.2e9) -> tuple[list[dict], dict]:
    from huggingface_hub import HfApi
    api = HfApi()
    models = list(api.list_models(
        pipeline_tag="text-generation", sort="downloads", limit=limit,
        expand=["safetensors", "cardData", "tags", "downloads", "gated", "private"]))
    counts = {"listed": len(models), "dropped_gated": 0, "dropped_declared": 0,
              "dropped_in_panel": 0, "dropped_size": 0, "dropped_no_safetensors": 0,
              "no_param_count": 0}
    keep: list[dict] = []
    for m in models:
        mid = m.id
        if getattr(m, "gated", False) or getattr(m, "private", False):
            counts["dropped_gated"] += 1
            continue
        card_txt = json.dumps(getattr(m, "card_data", None) or {},
                              default=str)[:4000]
        if DECLARED_RE.search(mid) or DECLARED_RE.search(card_txt):
            counts["dropped_declared"] += 1
            continue
        if mid in exclude_repos:
            counts["dropped_in_panel"] += 1
            continue
        st = getattr(m, "safetensors", None)
        n_params = getattr(st, "total", None) if st is not None else None
        if n_params is None:
            counts["no_param_count"] += 1
            counts["dropped_no_safetensors"] += 1
            continue
        if n_params > max_params:
            counts["dropped_size"] += 1
            continue
        keep.append({"repo": mid, "params": int(n_params),
                     "downloads": int(getattr(m, "downloads", 0) or 0),
                     "tags": list(getattr(m, "tags", []) or [])[:20]})
    # smallest-first within download-rank decile
    n = max(len(keep), 1)
    for i, r in enumerate(keep):
        r["decile"] = int(10 * i / n)
    keep.sort(key=lambda r: (r["decile"], r["params"]))
    counts["kept"] = len(keep)
    return keep, counts


def adjudicate(repo: str) -> dict:
    """Classify a hit against its card and lineage. Every verdict is quoted."""
    from huggingface_hub import HfApi, ModelCard
    api = HfApi()
    text, base_models, tags, err = "", [], [], None
    try:
        info = api.model_info(repo, cardData=True)
        cd = getattr(info, "card_data", None)
        tags = list(getattr(info, "tags", []) or [])
        if cd is not None:
            bm = getattr(cd, "base_model", None)
            base_models = ([bm] if isinstance(bm, str) else list(bm or []))
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}"
    try:
        text = (ModelCard.load(repo).text or "")[:20000]
    except Exception as e:  # noqa: BLE001
        err = err or f"card: {type(e).__name__}: {e}"

    hay = " ".join([text, " ".join(base_models), " ".join(tags)])
    m = DECLARED_RE.search(hay)
    if m and any(DECLARED_RE.search(b) for b in base_models):
        i = max(0, hay.find(m.group(0)) - 120)
        return {"verdict": "MERGE_OF_ABLITERATED_ANCESTOR", "evidence": hay[i:i + 300],
                "base_models": base_models, "card_len": len(text), "error": err}
    if m:
        i = max(0, hay.find(m.group(0)) - 120)
        return {"verdict": "GENUINE_UNDECLARED_EDIT", "evidence": hay[i:i + 300],
                "base_models": base_models, "card_len": len(text), "error": err}
    edit_re = re.compile(r"refusal direction|ablation|ortho|steer|direction removal|"
                         r"safety removal|remove refusal|projection out", re.IGNORECASE)
    m2 = edit_re.search(hay)
    if m2:
        i = max(0, hay.find(m2.group(0)) - 120)
        return {"verdict": "GENUINE_UNDECLARED_EDIT", "evidence": hay[i:i + 300],
                "base_models": base_models, "card_len": len(text), "error": err}
    if len(text.strip()) < 80 and not base_models:
        return {"verdict": "UNDETERMINED", "evidence": (text or "<empty card>")[:300],
                "base_models": base_models, "card_len": len(text), "error": err}
    return {"verdict": "FALSE_POSITIVE", "evidence": text[:300] or "<no card text>",
            "base_models": base_models, "card_len": len(text), "error": err}


def scan_one(repo: str, cache_dir: Path, revision: str | None = None,
             device: str = "cpu") -> dict:
    row = {"repo": repo, "revision": revision, "status": "OK", "error": None}
    t0 = time.time()
    p = None
    try:
        p, tot_bytes = download(repo, cache_dir, revision=revision)
        row["tensor_bytes"] = int(tot_bytes)
        row.update(weights_from_safetensors(p, device=device))
    except Exception as e:  # noqa: BLE001
        msg = f"{type(e).__name__}: {e}"
        row["status"] = ("UNRESOLVED" if "UNRESOLVED" in msg or "unresolved" in msg
                         or "not supported" in msg
                         else "SKIPPED" if ("401" in msg or "403" in msg or "cap" in msg
                                            or "no .safetensors" in msg)
                         else "ERROR")
        row["error"] = msg[:400]
        logger.warning(f"{repo}: {row['status']} {msg[:160]}")
    finally:
        if p is not None:
            row["freed_bytes"] = purge(p, cache_dir)
    row["total_s"] = time.time() - t0
    row.pop("v1", None)
    return row
