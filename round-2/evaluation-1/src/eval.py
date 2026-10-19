#!/usr/bin/env python3
"""Auditing last round's negative results — single entry point.

Subcommands: inventory | a1 | a2 | a3 | a4 | a5 | finalize | all
--stage smoke runs everything at reduced N for pipeline validation.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from loguru import logger  # noqa: E402

from audit.common import OUT, dump_json, flush_substitutions, setup_logging  # noqa: E402

STAGES = ("inventory", "a1", "a2", "a3", "a4", "a5", "finalize")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=list(STAGES) + ["all"])
    ap.add_argument("--stage", choices=["full", "smoke"], default="full")
    ap.add_argument("--n", type=int, default=None,
                    help="override A3 probe size (default 150 full / 12 smoke)")
    args = ap.parse_args()
    setup_logging(f"{args.command}_{args.stage}")
    smoke = args.stage == "smoke"
    timings = {}
    cmds = list(STAGES) if args.command == "all" else [args.command]
    for c in cmds:
        t0 = time.time()
        logger.info(f"=== stage {c} ({args.stage}) ===")
        if c == "inventory":
            from audit import inventory
            inventory.run()
        elif c == "a1":
            from audit import a1_lambda
            a1_lambda.run()
        elif c == "a2":
            from audit import a2_gate
            a2_gate.run()
        elif c == "a3":
            from audit import a3_probe
            n = args.n if args.n else (12 if smoke else a3_probe.TARGET_N)
            a3_probe.run(target_n=n)
        elif c == "a4":
            from audit import a4_permutation
            a4_permutation.run()
        elif c == "a5":
            from audit import a5_prereg
            a5_prereg.run()
        elif c == "finalize":
            from audit import finalize
            finalize.run(smoke=smoke)
        timings[c] = round(time.time() - t0, 2)
        logger.info(f"stage {c} took {timings[c]}s")
    flush_substitutions()
    p = OUT / "stage_timings.json"
    old = {}
    if p.exists():
        import json
        old = json.loads(p.read_text())
    old.update(timings)
    dump_json(p, old)


if __name__ == "__main__":
    main()
