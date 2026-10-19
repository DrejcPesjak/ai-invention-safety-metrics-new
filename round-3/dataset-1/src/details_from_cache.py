#!/usr/bin/env python3
"""Assemble results/details.json from whatever is already in cache/details/.

Safety net: the per-repo fetch is monotone (every success is cached), so if a
run is interrupted the finished work is still usable. Running this turns the
cache into the same file the fetch would have written, minus the repos that
never completed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")


def main() -> None:
    rows, bad = [], 0
    for p in (ROOT / "cache" / "details").glob("*.json"):
        try:
            rows.append(json.loads(p.read_text())["v"])
        except (json.JSONDecodeError, KeyError):
            bad += 1
    out = ROOT / "results" / "details.json"
    out.write_text(json.dumps(rows))
    st: dict[str, int] = {}
    for r in rows:
        st[r.get("status", "?")] = st.get(r.get("status", "?"), 0) + 1
    logger.info(f"{len(rows)} rows ({bad} unreadable) -> {out} ({out.stat().st_size / 1e6:.1f} MB)")
    logger.info(f"status {st}; with README {sum(1 for r in rows if r.get('readme'))}")


if __name__ == "__main__":
    main()
