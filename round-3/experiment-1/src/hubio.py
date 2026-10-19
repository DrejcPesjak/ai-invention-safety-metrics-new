#!/usr/bin/env python3
"""Hub snapshot acquisition under a hard disk budget.

The workspace lives on a 40 GB overlay, so snapshots are acquired SEQUENTIALLY
and released as soon as every arm that needs a checkpoint has taken what it
needs.  `ensure()` / `release()` are explicit rather than a context manager
because Arm 2 (E_1) legitimately needs a parent and a candidate resident at the
same time.
"""

from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path

import torch
from huggingface_hub import HfApi, snapshot_download
from loguru import logger

WS = Path(__file__).resolve().parent
HF_HOME = WS / "hfcache"
HF_HOME.mkdir(exist_ok=True)
os.environ.setdefault("HF_HOME", str(HF_HOME))
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

ALLOW = ["*.safetensors", "*.json", "*.model", "*.txt", "*.tiktoken", "*.py"]
IGNORE = ["*.bin", "*.pth", "*.h5", "*.msgpack", "*.onnx", "*.gguf", "original/*",
          "*.pt", "consolidated*"]

_API = HfApi()
_RESIDENT: dict[str, dict] = {}


def free_gb() -> float:
    st = shutil.disk_usage(str(WS))
    return st.free / 1e9


def dir_gb(p: Path) -> float:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) / 1e9


def resolve_revision(repo: str, revision: str | None) -> tuple[str, dict]:
    """Return (sha, info).  A pinned revision is honoured; otherwise `main` is
    resolved and the sha RECORDED as a deviation."""
    info = {}
    try:
        mi = _API.model_info(repo, revision=revision or "main", files_metadata=False)
        info = {"sha": mi.sha, "downloads": getattr(mi, "downloads", None),
                "tags": list(getattr(mi, "tags", []) or [])[:40],
                "author": (repo.split("/")[0] if "/" in repo else ""),
                "gated": bool(getattr(mi, "gated", False))}
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"model_info failed for {repo}: {exc}")
        info = {"sha": None, "error": str(exc)[:200]}
    return (revision or info.get("sha") or "main"), info


def ensure(repo: str, revision: str | None = None, *, min_free_gb: float = 6.0) -> dict:
    """Download a snapshot (idempotent).  Returns {path, revision, resolved_sha}."""
    key = f"{repo}@{revision}"
    if key in _RESIDENT:
        return _RESIDENT[key]
    if free_gb() < min_free_gb:
        raise RuntimeError(f"disk below {min_free_gb} GB before fetching {repo}")
    rev, info = resolve_revision(repo, revision)
    t0 = time.time()
    last = None
    for attempt in range(3):
        try:
            path = snapshot_download(repo, revision=rev, allow_patterns=ALLOW,
                                     ignore_patterns=IGNORE, max_workers=8)
            break
        except Exception as exc:  # noqa: BLE001
            last = exc
            logger.warning(f"download {repo} attempt {attempt + 1} failed: {str(exc)[:200]}")
            time.sleep(5 * (attempt + 1))
    else:
        raise RuntimeError(f"could not fetch {repo}: {last}")
    rec = {"repo": repo, "path": path, "revision": rev,
           "revision_was_pinned": revision is not None,
           "resolved_sha": info.get("sha"), "hub_info": info,
           "gb": round(dir_gb(Path(path)), 3),
           "download_s": round(time.time() - t0, 1)}
    _RESIDENT[key] = rec
    logger.info(f"fetched {repo} ({rec['gb']:.2f} GB in {rec['download_s']}s), "
                f"free={free_gb():.1f} GB")
    return rec


def release(repo: str, revision: str | None = None) -> None:
    """Delete a snapshot's blobs so the next download fits."""
    keys = [k for k in list(_RESIDENT)
            if k == f"{repo}@{revision}" or (revision is None and k.startswith(f"{repo}@"))]
    for k in keys:
        rec = _RESIDENT.pop(k)
        # snapshot_download returns .../snapshots/<sha>; the blobs live two up
        root = Path(rec["path"]).resolve().parent.parent
        if root.exists() and "models--" in root.name:
            shutil.rmtree(root, ignore_errors=True)
            logger.info(f"released {repo} ({rec['gb']:.2f} GB), free={free_gb():.1f} GB")


def release_all() -> None:
    for k in list(_RESIDENT):
        repo, _, rev = k.rpartition("@")
        release(repo, None if rev == "None" else rev)


def gc_cuda() -> None:
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


# ---------------------------------------------------------------------------
# Tensor-level reads (no model materialisation) -- used by Arm 2
# ---------------------------------------------------------------------------
def load_config(path: str | Path) -> dict:
    return json.loads((Path(path) / "config.json").read_text())


def safetensor_key_map(path: str | Path) -> dict[str, str]:
    """key -> shard file, from the index if sharded, else the single file."""
    p = Path(path)
    idx = p / "model.safetensors.index.json"
    if idx.exists():
        return json.loads(idx.read_text())["weight_map"]
    single = p / "model.safetensors"
    if not single.exists():
        cands = sorted(p.glob("*.safetensors"))
        if not cands:
            raise FileNotFoundError(f"no safetensors under {p}")
        single = cands[0]
    from safetensors import safe_open
    with safe_open(str(single), framework="pt") as f:
        return {k: single.name for k in f.keys()}


def read_tensors(path: str | Path, keys: list[str]) -> dict[str, torch.Tensor]:
    """Read named tensors lazily, one shard at a time."""
    from safetensors import safe_open
    p = Path(path)
    kmap = safetensor_key_map(p)
    by_shard: dict[str, list[str]] = {}
    for k in keys:
        if k in kmap:
            by_shard.setdefault(kmap[k], []).append(k)
    out: dict[str, torch.Tensor] = {}
    for shard, ks in by_shard.items():
        with safe_open(str(p / shard), framework="pt") as f:
            for k in ks:
                out[k] = f.get_tensor(k)
    return out
