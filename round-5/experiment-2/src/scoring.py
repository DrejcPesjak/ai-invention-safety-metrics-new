#!/usr/bin/env python3
"""Download -> eligibility -> W05 -> delete.  One repo at a time, always purged."""

from __future__ import annotations

import gc
import json
import time
from pathlib import Path

import torch
from loguru import logger

import vendored_hubio as hubio
import vendored_wstats as wstats
from common import CACHE, TAU_PANEL, TAU_REFIT

N_RANDOM = 256
SEED = 0
# per-row keys copied into the shipped output.  e_v1 / fro2 / v1 stay on disk.
SUMMARY_KEYS = (
    "W01_abl_suppression_depth", "W02_abl_direction_consistency",
    "W03_abl_gap_vs_random", "W04_abl_isolation", "W05_abl_min_layer_energy",
    "W05q10_abl_p10_layer_energy", "lam_min", "lam_median", "lam_second",
    "n_write_matrices", "hidden_size", "n_layers", "model_type",
    "U_ratio", "U_iqr", "U_frac", "accum_dtype", "wall_clock_s",
)


def device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def score_repo(repo: str, revision: str | None, *, max_bytes: float = 12e9,
               keep_vectors: bool = True) -> dict:
    """Full pipeline for one repo.  Never raises: failures come back as a row."""
    t0 = time.time()
    row: dict = {"repo_id": repo, "revision": revision, "status": "OK",
                 "error": None, "tensor_bytes": None}
    local = None
    try:
        local, tot = hubio.download(repo, CACHE, revision=revision, max_bytes=max_bytes)
        row["tensor_bytes"] = int(tot)
        cfg = wstats.read_config(local)
        names = [p.name for p in Path(local).glob("*")]
        ok, why = wstats.eligibility(cfg, names)
        row["wstats_eligible"] = bool(ok)
        row["wstats_eligibility_reason"] = why
        if not ok:
            row["status"] = "INELIGIBLE"
            row["error"] = why
            return row
        s = wstats.wstats_fast(local, n_random=N_RANDOM, seed=SEED, device=device())
        for k in SUMMARY_KEYS:
            if k in s:
                v = s[k]
                row[k] = str(v) if isinstance(v, torch.dtype) else v
        row["layer_profile"] = s["layer_profile"]
        if keep_vectors:
            row["e_v1"] = s["e_v1"]
            row["layer_of_matrix"] = s["layer_of_matrix"]
        w05 = float(s["W05_abl_min_layer_energy"])
        row["detect_panel"] = bool(w05 <= TAU_PANEL)
        row["detect_refit"] = bool(w05 <= TAU_REFIT)
        row["margin_panel"] = float(w05 - TAU_PANEL)
        row["margin_refit"] = float(w05 - TAU_REFIT)
    except Exception as exc:                                     # noqa: BLE001
        row["status"] = "UNRESOLVED"
        row["error"] = f"{type(exc).__name__}: {exc}"[:300]
        logger.warning(f"{repo}: {row['error']}")
    finally:
        if local is not None:
            try:
                row["freed_bytes"] = hubio.purge(Path(local), CACHE)
            except OSError as exc:
                logger.warning(f"purge failed {repo}: {exc}")
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        row["seconds"] = round(time.time() - t0, 2)
    return row


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(row) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not Path(path).exists():
        return []
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
