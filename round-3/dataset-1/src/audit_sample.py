#!/usr/bin/env python3
"""Step 1d self-audit -- print 10 random labelled rows against their raw card.

The executor reads these by hand and records how many survive. The survival
count goes into the coverage report whatever it turns out to be; the point of
the check is to bound the labeller's error rate, not to defend it.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def main() -> None:
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20260813
    data = json.loads((ROOT / "data_out.json").read_text())
    manifest = next(d for d in data["datasets"] if d["dataset"] == "edit_manifest")
    rows = [
        e["metadata_features"]
        for e in manifest["examples"]
        if not e["metadata_features"]["is_parent"]
    ]
    det = {d["repo_id"]: d for d in json.loads((ROOT / "results" / "details.json").read_text())}

    rng = random.Random(seed)
    sample = rng.sample(rows, min(10, len(rows)))
    for i, r in enumerate(sample, 1):
        card = (det.get(r["repo_id"]) or {}).get("readme") or ""
        print("=" * 100)
        print(f"[{i}] {r['repo_id']}")
        print(f"    class={r['recipe_class']}  rule={r['label_rule']}  params={r['param_count_hub']}")
        print(f"    evidence: {r['recipe_evidence']}")
        print(f"    --- card (first 1200 chars of {len(card)}) ---")
        print(card[:1200].replace("\n\n", "\n"))
    print("=" * 100)
    print(f"seed={seed}  n={len(sample)}")


if __name__ == "__main__":
    main()
