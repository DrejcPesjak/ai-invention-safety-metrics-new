#!/usr/bin/env python3
"""Stage 1: capability-axis harvest from the Open LLM Leaderboard datasets.

Pulls open-llm-leaderboard/contents (v2) and open-llm-leaderboard-old/contents (v1)
as parquet, joins them to the resolved <=4.2B panel on normalised repo id, and emits
one external_score row per (checkpoint, benchmark, metric).

v1 and v2 scores are NOT comparable, so every row carries
source_version_or_release = 'open-llm-leaderboard v1|v2 snapshot <date>' and the
leaderboard version is never mixed silently.

Flagged rows are dropped from the score set but retained in a separate list.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pandas as pd
from loguru import logger

HERE = Path(__file__).resolve().parent.parent
CACHE, RESULTS, LOGS = HERE / "cache", HERE / "results", HERE / "logs"
for d in (CACHE, RESULTS, LOGS):
    d.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "s1_capability.log"), rotation="30 MB", level="DEBUG")

RETRIEVAL_DATE = date.today().isoformat()

# (leaderboard column, benchmark, metric_name, scale, polarity)
V2_METRICS = [
    ("IFEval", "IFEval", "normalised_accuracy", "0-100 percent (normalised)", "HIGHER_IS_MORE_CAPABLE"),
    ("IFEval Raw", "IFEval", "raw_accuracy", "0-1 rate (raw)", "HIGHER_IS_MORE_CAPABLE"),
    ("BBH", "BBH", "normalised_accuracy", "0-100 percent (normalised)", "HIGHER_IS_MORE_CAPABLE"),
    ("BBH Raw", "BBH", "raw_accuracy", "0-1 rate (raw)", "HIGHER_IS_MORE_CAPABLE"),
    ("MATH Lvl 5", "MATH Lvl 5", "normalised_accuracy", "0-100 percent (normalised)", "HIGHER_IS_MORE_CAPABLE"),
    ("MATH Lvl 5 Raw", "MATH Lvl 5", "raw_accuracy", "0-1 rate (raw)", "HIGHER_IS_MORE_CAPABLE"),
    ("GPQA", "GPQA", "normalised_accuracy", "0-100 percent (normalised)", "HIGHER_IS_MORE_CAPABLE"),
    ("GPQA Raw", "GPQA", "raw_accuracy", "0-1 rate (raw)", "HIGHER_IS_MORE_CAPABLE"),
    ("MUSR", "MUSR", "normalised_accuracy", "0-100 percent (normalised)", "HIGHER_IS_MORE_CAPABLE"),
    ("MUSR Raw", "MUSR", "raw_accuracy", "0-1 rate (raw)", "HIGHER_IS_MORE_CAPABLE"),
    ("MMLU-PRO", "MMLU-PRO", "normalised_accuracy", "0-100 percent (normalised)", "HIGHER_IS_MORE_CAPABLE"),
    ("MMLU-PRO Raw", "MMLU-PRO", "raw_accuracy", "0-1 rate (raw)", "HIGHER_IS_MORE_CAPABLE"),
    ("Average ⬆️", "OpenLLMLeaderboard v2 Average", "average_of_six_normalised", "0-100 percent", "HIGHER_IS_MORE_CAPABLE"),
]
V1_METRICS = [
    ("ARC", "ARC-Challenge", "normalised_accuracy_25shot", "0-100 percent", "HIGHER_IS_MORE_CAPABLE"),
    ("HellaSwag", "HellaSwag", "normalised_accuracy_10shot", "0-100 percent", "HIGHER_IS_MORE_CAPABLE"),
    ("MMLU", "MMLU", "accuracy_5shot", "0-100 percent", "HIGHER_IS_MORE_CAPABLE"),
    ("TruthfulQA", "TruthfulQA-MC2", "mc2_0shot", "0-100 percent", "HIGHER_IS_MORE_CAPABLE"),
    ("Winogrande", "Winogrande", "accuracy_5shot", "0-100 percent", "HIGHER_IS_MORE_CAPABLE"),
    ("GSM8K", "GSM8K", "accuracy_5shot", "0-100 percent", "HIGHER_IS_MORE_CAPABLE"),
    ("Average ⬆️", "OpenLLMLeaderboard v1 Average", "average_of_six", "0-100 percent", "HIGHER_IS_MORE_CAPABLE"),
]

SOURCES = [
    {
        "repo": "open-llm-leaderboard/contents",
        "version": "v2",
        "metrics": V2_METRICS,
        "url": "https://huggingface.co/datasets/open-llm-leaderboard/contents",
        "date_col": "Submission Date",
    },
    {
        "repo": "open-llm-leaderboard-old/contents",
        "version": "v1",
        "metrics": V1_METRICS,
        "url": "https://huggingface.co/datasets/open-llm-leaderboard-old/contents",
        "date_col": "date",
    },
]


def norm(s: str) -> str:
    return str(s).strip().lower()


def main() -> None:
    panel = json.loads((RESULTS / "panel_resolved.json").read_text())
    pk = {norm(x["hf_repo_id"]): x for x in panel if x["in_panel_le_4p2b"]}
    logger.info(f"Panel <=4.2B: {len(pk)} checkpoints")

    rows: list[dict] = []
    flagged: list[dict] = []
    per_source: list[dict] = []

    for src in SOURCES:
        path = CACHE / (src["repo"].replace("/", "__") + ".parquet")
        if not path.exists():
            from datasets import load_dataset  # local import: heavy

            load_dataset(src["repo"], split="train").to_pandas().to_parquet(path)
        df = pd.read_parquet(path)
        df["_k"] = df["fullname"].map(norm)
        # The archived v1 dataset sets Flagged=True on ALL 7260 rows, so there it
        # is an archive-wide artefact and carries no per-model information. Only
        # honour the column where it actually discriminates.
        flag_informative = df["Flagged"].nunique() > 1
        if not flag_informative:
            logger.warning(
                f"{src['repo']}: 'Flagged' is constant ({df['Flagged'].iloc[0]}) across "
                f"all {len(df)} rows -> treated as uninformative, not used to drop rows"
            )
        hit = df[df["_k"].isin(pk)].copy()
        logger.info(
            f"{src['repo']} ({src['version']}): {len(df)} leaderboard rows, "
            f"{len(hit)} match the panel over {hit['_k'].nunique()} checkpoints"
        )
        per_source.append({
            "source": src["repo"],
            "leaderboard_version": src["version"],
            "n_models_source_evaluates": int(df["_k"].nunique()),
            "n_panel_checkpoints_present": int(hit["_k"].nunique()),
            "n_panel_checkpoints_total": len(pk),
        })

        for _, r in hit.iterrows():
            p = pk[r["_k"]]
            is_flagged = bool(r.get("Flagged", False)) and flag_informative
            sha_src = str(r.get("Model sha") or "").strip()
            sha_panel = str(p.get("revision") or "").strip()
            if sha_src and sha_panel and sha_src == sha_panel:
                match = "EXACT"
            elif sha_src:
                match = "SIBLING"  # same repo, source pinned a DIFFERENT commit
            else:
                match = "SAME_REPO_UNKNOWN_SHA"
            snap = str(r.get(src["date_col"]) or "UNSTATED")
            base = {
                "checkpoint_id": p["hf_repo_id"],
                "lineage_id": p["lineage_id"],
                "revision_sha_source": sha_src or "UNSTATED",
                "revision_sha_panel": sha_panel or "UNSTATED",
                "revision_match": match,
                "axis": "CAPABILITY",
                "source_url": src["url"],
                "source_type": "LEADERBOARD_SNAPSHOT",
                "source_version_or_release": (
                    f"Open LLM Leaderboard {src['version']}; dataset snapshot pulled "
                    f"{RETRIEVAL_DATE}; leaderboard row submitted/dated {snap}"
                ),
                "retrieval_date": RETRIEVAL_DATE,
                "judge_or_grader": "lm-evaluation-harness automatic scoring (string/loglikelihood match)",
                "circularity_flag": "",
                "leaderboard_flagged_raw": bool(r.get("Flagged", False)),
                "leaderboard_flag_informative": bool(flag_informative),
                "leaderboard_precision": str(r.get("Precision") or "UNSTATED"),
                "leaderboard_chat_template": bool(r.get("Chat Template", False)),
                "leaderboard_params_b": float(r["#Params (B)"]) if pd.notna(r.get("#Params (B)")) else None,
            }
            for col, bench, metric, scale, pol in src["metrics"]:
                if col not in hit.columns:
                    continue
                v = r[col]
                if pd.isna(v):
                    continue
                rec = dict(base)
                rec.update({
                    "benchmark": bench,
                    "metric_name": metric,
                    "value": float(v),
                    "scale": scale,
                    "polarity": pol,
                    "verbatim_snippet": (
                        f"Open LLM Leaderboard {src['version']} contents dataset, row "
                        f"eval_name={r['eval_name']!r}, column {col!r} = {float(v)!r}; "
                        f"Model sha={sha_src or 'UNSTATED'}; Precision={base['leaderboard_precision']}"
                    )[:300],
                })
                (flagged if is_flagged else rows).append(rec)

    logger.info(f"Emitted {len(rows)} capability rows; {len(flagged)} withheld as Flagged")
    (RESULTS / "capability_rows.json").write_text(json.dumps(rows, indent=1))
    (RESULTS / "capability_flagged_rows.json").write_text(json.dumps(flagged, indent=1))
    (RESULTS / "capability_source_overlap.json").write_text(json.dumps(per_source, indent=1))


if __name__ == "__main__":
    main()
