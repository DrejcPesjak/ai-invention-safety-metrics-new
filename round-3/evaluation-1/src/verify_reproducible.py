#!/usr/bin/env python3
"""Determinism check: run analysis.py a second time with the cache warm and
assert numbers.json is BYTE-IDENTICAL.

The only fields allowed to differ are the wall-clock timings, which are stripped
before comparison (and the stripped keys are named in the report, so the check
cannot be widened silently).
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
VOLATILE = [("runtime", "wall_clock_s")]

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs/verify.log", rotation="10 MB", level="DEBUG")


def canonical(p: Path) -> tuple[str, str]:
    raw = p.read_bytes()
    d = json.loads(raw)
    for path in VOLATILE:
        cur = d
        for k in path[:-1]:
            cur = cur.get(k, {})
        cur.pop(path[-1], None)
    return (hashlib.sha256(raw).hexdigest(),
            hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest())


def main() -> None:
    src = HERE / "numbers.json"
    if not src.exists():
        raise SystemExit("numbers.json missing -- run analysis.py first")
    raw1, canon1 = canonical(src)
    first = json.loads(src.read_text())
    logger.info(f"run 1: raw sha256 {raw1[:16]} | canonical (timings stripped) {canon1[:16]}")

    logger.info("second invocation with the cache warm ...")
    r = subprocess.run([str(HERE / ".venv/bin/python"), str(HERE / "analysis.py")],
                       cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        logger.error(r.stdout[-4000:])
        logger.error(r.stderr[-4000:])
        raise SystemExit(f"second run failed with exit code {r.returncode}")
    raw2, canon2 = canonical(src)
    second = json.loads(src.read_text())
    logger.info(f"run 2: raw sha256 {raw2[:16]} | canonical (timings stripped) {canon2[:16]}")

    ok = canon1 == canon2
    report = {
        "byte_identical_ignoring_wall_clock": ok,
        "volatile_keys_stripped_before_comparison": [".".join(p) for p in VOLATILE],
        "raw_sha256_run1": raw1, "raw_sha256_run2": raw2,
        "canonical_sha256_run1": canon1, "canonical_sha256_run2": canon2,
        "llm_spend_run2_usd": second["runtime"]["llm_spend_usd"],
        "n_new_llm_calls_run2": second["runtime"]["n_new_llm_calls"],
        "second_run_cost_zero": second["runtime"]["n_new_llm_calls"] == 0,
        "wall_clock_run1_s": first["runtime"]["wall_clock_s"],
        "wall_clock_run2_s": second["runtime"]["wall_clock_s"],
    }
    if not ok:
        diffs = []

        def walk(a, b, p=""):
            if isinstance(a, dict) and isinstance(b, dict):
                for k in sorted(set(a) | set(b)):
                    walk(a.get(k), b.get(k), f"{p}/{k}")
            elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
                for i, (x, y) in enumerate(zip(a, b)):
                    walk(x, y, f"{p}[{i}]")
            elif a != b and not p.endswith("wall_clock_s"):
                diffs.append({"path": p, "run1": a, "run2": b})

        walk(first, second)
        report["n_differing_fields"] = len(diffs)
        report["differing_fields"] = diffs[:50]
        logger.error(f"NOT reproducible: {len(diffs)} differing fields")
    else:
        logger.info("REPRODUCIBLE: numbers.json is identical across two runs")
    (HERE / "results/reproducibility.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
