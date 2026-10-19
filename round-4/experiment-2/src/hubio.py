#!/usr/bin/env python3
"""Hub I/O: metadata-only fetches, snapshot download, and immediate purge.

Disk is the binding constraint on this host (40 GB), so every repo is
downloaded, scored, and deleted before the next one starts, and free space is
asserted before each new download.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import requests
from loguru import logger

HF = "https://huggingface.co"
TIMEOUT = 30


def fetch_config(repo: str, revision: str = "main", timeout: int = TIMEOUT) -> dict | None:
    """config.json only -- a few kB, never weights."""
    url = f"{HF}/{repo}/resolve/{revision}/config.json"
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            return None
        return r.json()
    except (requests.RequestException, json.JSONDecodeError) as exc:
        logger.debug(f"config fetch failed {repo}: {type(exc).__name__}")
        return None


def config_facts(cfg: dict | None) -> dict:
    """(n_layers, hidden_size, model_type, quantization_config) from a raw config."""
    if not cfg:
        return {}
    t = (cfg.get("text_config") or cfg.get("llm_config")
         or cfg.get("language_config") or cfg)

    def g(c, keys):
        for k in keys:
            v = c.get(k)
            if isinstance(v, int) and v > 0:
                return v
        return None

    d = g(t, ("hidden_size", "n_embd", "n_embed", "d_model", "hidden_dim", "model_dim"))
    L = g(t, ("num_hidden_layers", "n_layer", "n_layers", "num_layers",
              "num_transformer_layers"))
    if d is None or L is None:
        for v in cfg.values():
            if isinstance(v, dict):
                d = d or g(v, ("hidden_size", "n_embd", "d_model"))
                L = L or g(v, ("num_hidden_layers", "n_layer", "num_layers"))
    return {
        "n_layers": L, "hidden_size": d,
        "model_type": str(t.get("model_type") or cfg.get("model_type") or "unknown"),
        "quantization_config": cfg.get("quantization_config"),
    }


def repo_size_and_dtypes(repo: str, revision: str | None = None) -> tuple[int, dict, str | None]:
    """(total safetensors bytes, param dtype histogram, resolved sha) via the Hub API."""
    from huggingface_hub import HfApi
    api = HfApi()
    info = api.model_info(repo, revision=revision, files_metadata=True)
    st = [f for f in info.siblings if f.rfilename.endswith(".safetensors")]
    total = sum(f.size or 0 for f in st)
    dtypes: dict = {}
    sfi = getattr(info, "safetensors", None)
    if sfi is not None:
        params = getattr(sfi, "parameters", None)
        if isinstance(params, dict):
            dtypes = dict(params)
    return int(total), dtypes, getattr(info, "sha", None)


def download(repo: str, cache_dir: Path, revision: str | None = None,
             max_bytes: int = 12 * 1024 ** 3) -> tuple[Path, int]:
    """VENDORED from the archive's lib_scan.download (same allow_patterns, same cap)."""
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


def purge(repo_path: Path, cache_dir: Path) -> int:
    """VENDORED from the archive's lib_scan.purge: delete the snapshot's blobs."""
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


def free_gb(path: Path) -> float:
    st = shutil.disk_usage(str(path))
    return st.free / 1e9
