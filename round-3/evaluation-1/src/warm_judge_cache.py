#!/usr/bin/env python3
"""Warm the adjudicator cache on its own, so `analysis.py` can be iterated for free.

Builds exactly the same item list and cache keys as analysis.py's reliability arm --
the six hand-labelled calibration items plus 44 checkpoints x (40 harmful + 25 XSTest)
archived (request, response) pairs -- and fills cache/judge_cache.jsonl. Running
analysis.py afterwards makes zero API calls.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "inputs"))

import lib_contract as C  # noqa: E402
import lib_data  # noqa: E402
from lib_judge import Judge, key_of  # noqa: E402

E1 = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_2/"
          "gen_art/gen_art_experiment_1")

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(HERE / "logs/warm_cache.log", rotation="10 MB", level="DEBUG")


@logger.catch(reraise=True)
def main() -> None:
    inp = lib_data.load_inputs()
    core40 = [r["input"] for r in inp.core40]
    xs25 = [r["input"] for r in inp.xs25]
    jc = json.loads((E1 / "results/judge_calibration.json").read_text())
    rubric_b = jc["rubric_B"]

    items = [{"request": r["request"], "response": r["response"],
              "key": key_of(C.JUDGE_MODEL, rubric_b, r["request"], r["response"])}
             for r in jc["hand_labelled_calibration_set"]]
    for line in (E1 / "generations.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        g = json.loads(line)
        for qs, fold in ((core40, "core40"), (xs25, "xs25")):
            for q, a in zip(qs, g[fold]):
                items.append({"request": q, "response": a,
                              "key": key_of(C.JUDGE_MODEL, rubric_b, q, a)})
    logger.info(f"{len(items)} items ({len({i['key'] for i in items})} distinct keys)")

    judge = Judge(model=C.JUDGE_MODEL, rubric=rubric_b, temperature=C.JUDGE_TEMPERATURE,
                  cache_path=HERE / "cache/judge_cache.jsonl",
                  ledger_path=HERE / "cost_ledger.jsonl",
                  hard_stop_usd=C.JUDGE_HARD_STOP_USD, concurrency=24)
    labels = judge.judge_all(items)
    got = sum(1 for i in items if i["key"] in labels)
    logger.info(f"cached {got}/{len(items)} | new calls {judge.n_new_calls} | "
                f"failed {judge.n_failed} | spend ${judge.spent:.4f} | "
                f"hard-stopped={judge.stopped_on_budget}")


if __name__ == "__main__":
    main()
