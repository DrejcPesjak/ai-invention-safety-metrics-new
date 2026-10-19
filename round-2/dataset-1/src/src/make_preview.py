#!/usr/bin/env python3
"""Rebuild preview_data_out.json so it covers EVERY block, not just the first three.

The aii-json format script truncates the top-level array, which for this artifact
means the preview shows only external_score / panel_checkpoint / lineage and none of
the 10 measurement corpora -- exactly the half a reader most needs to see the shape
of. This regenerates the preview with the same per-example rule (3 examples per block,
every string truncated to 200 chars) applied to all 20 blocks.

Deterministic: it takes the first 3 examples of each block, no sampling.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent.parent
TRUNC = 200
PER_BLOCK = 3

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")


def shorten(v):
    if isinstance(v, str):
        return v[:TRUNC] + ("..." if len(v) > TRUNC else "")
    if isinstance(v, list):
        return [shorten(x) for x in v]
    if isinstance(v, dict):
        return {k: shorten(x) for k, x in v.items()}
    return v


def main() -> None:
    data = json.loads((HERE / "full_data_out.json").read_text())
    out = {
        "metadata": shorten(data["metadata"]),
        "datasets": [
            {"dataset": b["dataset"],
             "examples": [shorten(e) for e in b["examples"][:PER_BLOCK]]}
            for b in data["datasets"]
        ],
    }
    dest = HERE / "preview_data_out.json"
    dest.write_text(json.dumps(out, indent=1))
    n = sum(len(b["examples"]) for b in out["datasets"])
    logger.info(f"Wrote {dest.name}: {len(out['datasets'])} blocks, {n} examples, "
                f"{dest.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
