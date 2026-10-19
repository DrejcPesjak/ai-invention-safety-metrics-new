#!/usr/bin/env python3
"""Shared Hugging Face Hub helpers: cached, retrying, unauthenticated-safe."""

from __future__ import annotations

import hashlib
import json
import os
import random
import time
from pathlib import Path
from typing import Any, Callable

import requests
from huggingface_hub import HfApi
from huggingface_hub.utils import (
    EntryNotFoundError,
    GatedRepoError,
    HfHubHTTPError,
    RepositoryNotFoundError,
)
from loguru import logger

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
CACHE.mkdir(exist_ok=True, parents=True)

TOKEN = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN") or None
API = HfApi(token=TOKEN)

ABLIT_RE = r"(?i)(abliterat|gabliterat|obliterat|uncensor|decensor|orthogonal|norm[-_]preserv|refusal[-_]?(free|removed))"


def cache_path(namespace: str, key: str) -> Path:
    d = CACHE / namespace
    d.mkdir(exist_ok=True, parents=True)
    h = hashlib.sha256(key.encode()).hexdigest()[:24]
    return d / f"{h}.json"


def cached_json(namespace: str, key: str, fn: Callable[[], Any]) -> Any:
    """Run fn() once, memoise its JSON-serialisable result on disk."""
    p = cache_path(namespace, key)
    if p.exists():
        try:
            return json.loads(p.read_text())["v"]
        except (json.JSONDecodeError, KeyError):
            logger.warning(f"corrupt cache {p}, refetching")
    v = fn()
    p.write_text(json.dumps({"k": key, "v": v}))
    return v


def retry(fn: Callable[[], Any], tries: int = 5, base: float = 1.0) -> Any:
    """Exponential backoff on 429/5xx. Terminal Hub errors are re-raised at once."""
    last: Exception | None = None
    for i in range(tries):
        try:
            return fn()
        except (GatedRepoError, RepositoryNotFoundError, EntryNotFoundError):
            raise
        except (HfHubHTTPError, requests.RequestException) as e:
            status = getattr(getattr(e, "response", None), "status_code", None)
            if status is not None and status not in (429, 500, 502, 503, 504):
                raise
            last = e
            sleep = base * (2**i) + random.uniform(0, 0.4)
            logger.debug(f"retry {i + 1}/{tries} after {sleep:.1f}s ({status}): {e}")
            time.sleep(sleep)
    assert last is not None
    raise last
