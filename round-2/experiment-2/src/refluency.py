#!/usr/bin/env python3
"""Recompute the fluency screen for already-completed members from the recorded
generations, and patch it into results/member_*.json.

Needed because the screen was initially computed with a POOLED distinct_3, which flags
successful steering (all 100 responses becoming near-identical refusals) as degeneration.
lib_common.fluency_stats now measures distinct_3 WITHIN each response; this script applies
the corrected screen to members that were already run, without re-running the GPU work.
Members run after the fix are unaffected (the recomputation is idempotent).
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib_common as C


def main():
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

    texts: dict[tuple, list[str]] = defaultdict(list)
    with open(C.RESULTS / "generations.jsonl") as f:
        for line in f:
            g = json.loads(line)
            texts[(g["member"], g["axis"], g["alpha"])].append(g["text"])
    logger.info(f"loaded {sum(len(v) for v in texts.values())} generations over "
                f"{len(texts)} cells")

    for p in sorted(C.RESULTS.glob("member_*.json")):
        rec = json.loads(p.read_text())
        changed = 0
        for pt in rec["dose_response"]:
            key = (rec["slug"], pt["axis"], pt["alpha"])
            if key not in texts:
                logger.warning(f"no recorded texts for {key}")
                continue
            old = pt["degenerate"]
            fl = C.fluency_stats(texts[key])
            pt.update(fl)
            changed += int(old != fl["degenerate"])
        rec["fluency_screen_recomputed"] = True
        p.write_text(json.dumps(rec, indent=1))
        logger.info(f"{rec['slug']}: {changed}/{len(rec['dose_response'])} points changed "
                    f"degeneracy verdict")


if __name__ == "__main__":
    main()
