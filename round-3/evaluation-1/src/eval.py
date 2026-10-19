#!/usr/bin/env python3
"""Canonical entry point for this evaluation.

    uv run eval.py            # warm the adjudicator cache, then recompute everything
    uv run eval.py --no-judge # skip the adjudicator entirely (arms 1, 2, 4, 5, 6 only)

The work itself lives in `analysis.py`, which is the artifact's centrepiece and is
meant to be read: it prints the full analysis contract (seed, B, cluster-resampling
scheme, singleton rule, tie handling, exclusion rule, NaN policy) before it prints a
single number. This file only sequences the two steps so that a fresh checkout has one
obvious thing to run.

Outputs, all in this directory:
    numbers.json   the machine-readable numerals the paper generates from
    eval_out.json  schema-valid (exp_eval_sol_out) evaluation output
    results/tables.txt
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
PY = HERE / ".venv/bin/python"
if not PY.exists():
    PY = Path(sys.executable)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(HERE / "logs").mkdir(exist_ok=True)
logger.add(HERE / "logs/eval.log", rotation="10 MB", level="DEBUG")


def run(script: str) -> None:
    logger.info(f"running {script}")
    r = subprocess.run([str(PY), str(HERE / script)], cwd=HERE)
    if r.returncode != 0:
        raise SystemExit(f"{script} exited {r.returncode}")


def main() -> None:
    skip_judge = "--no-judge" in sys.argv
    if skip_judge:
        # analysis.py still runs the reliability arm, but reads only what is cached
        # and marks the arm PARTIAL with the achieved n. Nothing is imputed.
        os.environ["AII_SKIP_JUDGE"] = "1"
        logger.info("--no-judge: the adjudicator will not be called; the reliability arm "
                    "reports whatever the cache already holds and is marked PARTIAL")
    else:
        if not os.environ.get("OPENROUTER_API_KEY"):
            logger.error("OPENROUTER_API_KEY is not set. Re-run with --no-judge, or export it. "
                         "With cache/judge_cache.jsonl present the key is not needed and the "
                         "run costs $0.")
            raise SystemExit(2)
        run("warm_judge_cache.py")
    run("analysis.py")
    logger.info("done: numbers.json, eval_out.json, results/tables.txt")
    logger.info("to check determinism: .venv/bin/python verify_reproducible.py")


if __name__ == "__main__":
    main()
