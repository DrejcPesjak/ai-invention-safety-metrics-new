#!/usr/bin/env python3
"""Download the evaluated dataset candidates to temp/datasets/ (full/mini/preview).

The skill's downloader ran into Hub 429s while the model-metadata sweep was
saturating the same rate limit, so this does the same job at low concurrency
with backoff, and reuses the datasets cache the corpora build already warmed.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from datasets import load_dataset
from loguru import logger

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(ROOT / "cache" / "hfds"))
OUT = ROOT / "temp" / "datasets"
OUT.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "download.log", rotation="30 MB", level="DEBUG")

MAX_ROWS = 40_000  # keeps every dump comfortably under the 300MB bar

CANDIDATES = [
    ("OpenAssistant/oasst1", None, "train"),
    ("Salesforce/wikitext", "wikitext-2-raw-v1", "test"),
    ("databricks/databricks-dolly-15k", None, "train"),
    ("allenai/tulu-3-sft-personas-instruction-following", None, "train"),
    ("HuggingFaceTB/everyday-conversations-llama3.1-2k", None, "train_sft"),
    ("timdettmers/openassistant-guanaco", None, "train"),
    ("OpenAssistant/oasst_top1_2023-08-25", None, "train"),
    ("argilla/databricks-dolly-15k-curated-en", None, "train"),
    ("OpenAssistant/oasst2", None, "train"),
    ("allenai/tulu-3-sft-mixture", None, "train"),
]


def truncate(o, n=200):
    if isinstance(o, str):
        return o[:n] + ("..." if len(o) > n else "")
    if isinstance(o, dict):
        return {k: truncate(v, n) for k, v in o.items()}
    if isinstance(o, list):
        return [truncate(v, n) for v in o]
    return o


def one(repo: str, config: str | None, split: str) -> dict:
    slug = repo.replace("/", "_") + f"_{config or 'default'}_{split}"
    full = OUT / f"full_{slug}.json"
    if full.exists() and full.stat().st_size > 10_000:
        logger.info(f"{repo}: already present ({full.stat().st_size / 1e6:.1f} MB)")
        return {"repo": repo, "status": "cached", "path": str(full)}

    last = None
    for attempt in range(4):
        try:
            ds = load_dataset(repo, config, split=split)
            break
        except Exception as e:
            last = e
            logger.warning(f"{repo} attempt {attempt + 1}: {type(e).__name__}: {str(e)[:160]}")
            time.sleep(5 * 2**attempt)
    else:
        logger.error(f"{repo}: giving up -- {last}")
        return {"repo": repo, "status": "failed", "error": f"{type(last).__name__}: {last}"[:300]}

    n = min(len(ds), MAX_ROWS)
    rows = ds.select(range(n)).to_list()
    full.write_text(json.dumps(rows, default=str))
    (OUT / f"mini_{slug}.json").write_text(json.dumps(rows[:3], indent=2, default=str))
    (OUT / f"preview_{slug}.json").write_text(
        json.dumps(truncate(rows[:3]), indent=2, default=str)
    )
    mb = full.stat().st_size / 1e6
    logger.info(f"{repo}: {n}/{len(ds)} rows, {mb:.1f} MB -> {full.name}")
    return {
        "repo": repo,
        "config": config,
        "split": split,
        "status": "ok",
        "n_rows_written": n,
        "n_rows_total": len(ds),
        "megabytes": round(mb, 2),
        "columns": list(ds.features.keys()),
        "path": str(full.relative_to(ROOT)),
    }


def main() -> None:
    report = [one(*c) for c in CANDIDATES]  # sequential on purpose: the Hub 429s
    (ROOT / "results" / "download_report.json").write_text(json.dumps(report, indent=2))
    ok = sum(1 for r in report if r["status"] in ("ok", "cached"))
    logger.info(f"{ok}/{len(report)} candidates downloaded")


if __name__ == "__main__":
    main()
