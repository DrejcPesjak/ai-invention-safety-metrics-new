#!/usr/bin/env python3
"""Stage 2d: curated external_score rows from official model cards.

The card scan (s2a) found that exactly TWO panel-relevant cards publish quantitative
safety numbers. Those tables are transcribed here with an explicit, hand-checked
column mapping, because a regex cannot decide which column belongs to which model
nor which direction is safer.

Anti-fabrication guard: every transcribed value must appear as a literal substring
in the cached card, and the row's verbatim_snippet must be a literal substring of
the cached card too. Both are asserted at build time -- a typo or an invented
number aborts the stage instead of shipping.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent.parent
CACHE, RESULTS, LOGS = HERE / "cache", HERE / "results", HERE / "logs"
CARDS = CACHE / "cards"
LOGS.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "s2d_curated.log"), rotation="30 MB", level="DEBUG")

RETRIEVAL_DATE = date.today().isoformat()

# --------------------------------------------------------------------------
# SOURCE 1 - Qwen/Qwen3-4B-SafeRL model card, "Performance" table.
# The table reports Qwen3-4B and Qwen3-4B-SafeRL side by side in Non-Think and
# Think modes. Qwen3-4B IS a panel checkpoint; Qwen3-4B-SafeRL is 4.41e9 params,
# i.e. ABOVE the 4.2e9 ceiling, and is carried as an augmentation row.
#
# Circularity: the SafeRL model was RL-trained against a Qwen3Guard-Gen-4B safety
# reward. The judges used in THIS table are Qwen3-235B and WildGuard, so the
# WildGuard columns are the non-circular ones. The Qwen3-235B columns share the
# Qwen3 family with both the model and its training reward, so they are flagged
# QWEN3_SAME_FAMILY_JUDGE rather than left unmarked, and the outright
# QWEN3GUARD_REWARD_CIRCULAR flag is reserved for any row whose grader IS a
# Qwen3Guard variant (rule QWEN3GUARD_CIRCULARITY).
# --------------------------------------------------------------------------
QWEN_CARD = "Qwen__Qwen3-4B-SafeRL.md"
QWEN_URL = "https://huggingface.co/Qwen/Qwen3-4B-SafeRL/blob/main/README.md"
QWEN_ROW_SNIPPETS = {
    ("Qwen/Qwen3-4B", "Non-Think"):
        "| **Non-Think** | Qwen3-4B                | 47.5                     | 64.7                     | 12.9                | 9.5                               | **19.1**            | 26.4            | **41.7**          |",
    ("Qwen/Qwen3-4B-SafeRL", "Non-Think"):
        "|             | Qwen3-4B-SafeRL       | **86.5**                     | **98.1**                     | **5.3**             | **10.7**                          | 18.2            | **27.7**        | 40.8          |",
    ("Qwen/Qwen3-4B", "Think"):
        "| **Think**     | Qwen3-4B                | 43.8                     | 59.0                     | 6.5                 | 13.7                              | **65.6**            | **48.4**        | **55.9**      |",
    ("Qwen/Qwen3-4B-SafeRL", "Think"):
        "|             | Qwen3-4B-SafeRL       | **83.4**                     | **97.4**                     | **6.2**             | **16.6**                          | 63.5            | 47.5            | 51.2          |",
}
# (benchmark, metric_name, axis, polarity, scale, judge, circularity, polarity_evidence)
QWEN_COLS = [
    ("Qwen3Guard-suite safety evaluation", "safety_rate", "SAFETY_HARM", "HIGHER_IS_SAFER",
     "0-100 percent", "Qwen3-235B LLM judge", "QWEN3_SAME_FAMILY_JUDGE",
     "Column header reads 'Safety Rate (Qwen3-235B)'; the card presents the SafeRL model's higher value (86.5 vs 47.5) as the improvement, so higher = safer."),
    ("Qwen3Guard-suite safety evaluation", "safety_rate", "SAFETY_HARM", "HIGHER_IS_SAFER",
     "0-100 percent", "WildGuard classifier", "",
     "Column header reads 'Safety Rate (WildGuard)'; the card bolds the SafeRL model's higher value (98.1 vs 64.7) as the improvement, so higher = safer."),
    ("Qwen3Guard-suite refusal evaluation", "refusal_rate", "SAFETY_OVERREFUSAL", "LOWER_IS_SAFER",
     "0-100 percent", "WildGuard classifier", "",
     "Column header reads 'Refusal (WildGuard)'. The card states the hybrid reward applies 'a moderate penalty for unnecessary refusals' and bolds the LOWER SafeRL value (5.3 vs 12.9), so lower = better (less over-refusal)."),
    ("ArenaHard-v2", "winrate_vs_gpt41", "CAPABILITY", "HIGHER_IS_MORE_CAPABLE",
     "0-100 percent winrate", "GPT-4.1 pairwise judge", "", "Winrate; higher is more capable."),
    ("AIME25", "pass_at_1", "CAPABILITY", "HIGHER_IS_MORE_CAPABLE",
     "0-100 percent", "exact answer match", "", "Pass@1 accuracy; higher is more capable."),
    ("LiveCodeBench v6", "pass_at_1", "CAPABILITY", "HIGHER_IS_MORE_CAPABLE",
     "0-100 percent", "unit-test execution", "", "Pass@1; higher is more capable."),
    ("GPQA", "pass_at_1", "CAPABILITY", "HIGHER_IS_MORE_CAPABLE",
     "0-100 percent", "exact answer match", "", "Pass@1 accuracy; higher is more capable."),
]
QWEN_VALUES = {
    ("Qwen/Qwen3-4B", "Non-Think"): [47.5, 64.7, 12.9, 9.5, 19.1, 26.4, 41.7],
    ("Qwen/Qwen3-4B-SafeRL", "Non-Think"): [86.5, 98.1, 5.3, 10.7, 18.2, 27.7, 40.8],
    ("Qwen/Qwen3-4B", "Think"): [43.8, 59.0, 6.5, 13.7, 65.6, 48.4, 55.9],
    ("Qwen/Qwen3-4B-SafeRL", "Think"): [83.4, 97.4, 6.2, 16.6, 63.5, 47.5, 51.2],
}

# --------------------------------------------------------------------------
# SOURCE 2 - Gemma 2 "Ethics and Safety" table.
# The table header is "Gemma 2 IT 2B | Gemma 2 IT 9B | Gemma 2 IT 27B", so column 1
# is the INSTRUCTION-TUNED 2B model. google/gemma-2-2b (the BASE repo) reproduces
# the identical IT table on its own card; those numbers are therefore NOT base-model
# numbers and no base row is emitted for them. The duplication is recorded instead.
# The card states no polarity, so each row's polarity comes from the benchmark's own
# definition and polarity_evidence says so explicitly.
# --------------------------------------------------------------------------
GEMMA_CARD = "google__gemma-2-2b-it.md"
GEMMA_URL = "https://huggingface.co/google/gemma-2-2b-it/blob/main/README.md"
GEMMA_ROWS = [
    # (line_snippet, benchmark, metric, value, axis, polarity, scale, polarity_evidence)
    ("| [RealToxicity][realtox]  | average       |  8.16         |  8.25         |  8.84          |",
     "RealToxicityPrompts", "average_toxicity", 8.16, "SAFETY_HARM", "LOWER_IS_SAFER",
     "0-100 (card states 'average'; scale not stated on the card)",
     "Polarity from the RealToxicityPrompts definition (toxicity score): a higher toxicity score is worse. The Gemma card states no direction."),
    ("| [CrowS-Pairs][crows]     | top-1         | 37.67         | 37.47         | 36.67          |",
     "CrowS-Pairs", "top_1", 37.67, "SAFETY_OTHER", "LOWER_IS_SAFER",
     "0-100 percent",
     "Polarity from the CrowS-Pairs definition (stereotype preference rate, 50 = no bias, higher = more stereotyped). The Gemma card states no direction; treat as bias, not harm-refusal."),
    ("| [BBQ Ambig][bbq]         | 1-shot, top-1 | 83.20         | 88.58         | 85.99          |",
     "BBQ Ambiguous", "one_shot_top_1_accuracy", 83.20, "SAFETY_OTHER", "HIGHER_IS_SAFER",
     "0-100 percent accuracy",
     "Polarity from the BBQ definition (accuracy on ambiguous contexts, where the correct answer is UNKNOWN): higher accuracy = less bias. The Gemma card states no direction."),
    ("| [BBQ Disambig][bbq]      | top-1         | 69.31         | 82.67         | 86.94          |",
     "BBQ Disambiguated", "top_1_accuracy", 69.31, "SAFETY_OTHER", "HIGHER_IS_SAFER",
     "0-100 percent accuracy",
     "Polarity from the BBQ definition (accuracy on disambiguated contexts): higher accuracy = less bias. The Gemma card states no direction."),
    ("| [Winogender][winogender] | top-1         | 52.91         | 79.17         | 77.22          |",
     "Winogender", "top_1_accuracy", 52.91, "SAFETY_OTHER", "HIGHER_IS_SAFER",
     "0-100 percent accuracy",
     "Polarity from the Winogender definition (coreference accuracy across gendered pronouns): higher = less gender bias. The Gemma card states no direction."),
    ("| [TruthfulQA][truthfulqa] |               | 43.72         | 50.27         | 51.60          |",
     "TruthfulQA", "score_metric_unstated", 43.72, "SAFETY_OTHER", "HIGHER_IS_SAFER",
     "UNSTATED (the card gives no metric variant, e.g. MC1/MC2/gen)",
     "Polarity from the TruthfulQA definition (truthfulness score): higher = more truthful. The exact metric variant is UNSTATED on the card."),
    ("| [Winobias 1_2][winobias] |               | 59.28         | 78.09         | 81.94          |",
     "WinoBias 1_2", "score_metric_unstated", 59.28, "SAFETY_OTHER", "HIGHER_IS_SAFER",
     "UNSTATED (the card gives no metric name)",
     "Polarity from the WinoBias definition (accuracy on the pro/anti-stereotype coreference split): higher = less occupational gender bias. The card states no direction and no metric name."),
    ("| [Winobias 2_2][winobias] |               | 88.57         | 95.32         | 97.22          |",
     "WinoBias 2_2", "score_metric_unstated", 88.57, "SAFETY_OTHER", "HIGHER_IS_SAFER",
     "UNSTATED (the card gives no metric name)",
     "Polarity from the WinoBias definition: higher = less occupational gender bias. The card states no direction and no metric name."),
    ("| [Toxigen][toxigen]       |               | 48.32         | 39.30         | 38.42          |",
     "ToxiGen", "score_metric_unstated", 48.32, "SAFETY_HARM", "LOWER_IS_SAFER",
     "UNSTATED (the card gives no metric name)",
     "Polarity from the ToxiGen definition (toxic-generation rate): higher = more toxic. NOTE the 2B value (48.32) is the WORST of the three sizes, consistent with a toxicity rate rather than an accuracy. The card states no direction."),
]
# Repos the Gemma IT table applies to: the evaluated model, plus verified mirrors.
GEMMA_TARGETS = [
    ("google/gemma-2-2b-it", "EXACT_MODEL_EVALUATED"),
    ("unsloth/gemma-2-2b-it", "MIRROR_OF_EVALUATED_MODEL"),
]

# --------------------------------------------------------------------------
# SOURCE 3 - huihui-ai abliteration cards. These publish the ONLY per-checkpoint
# numbers that exist anywhere for abliterated panel members, and they report the
# parent instruct model alongside, so both sides of each pair are covered. They are
# CAPABILITY only -- the cards report no safety metric -- and the grader is a repo
# script (eval.sh) with no stated harness version, so judge_or_grader records that
# verbatim and source_type is THIRD_PARTY_REPO.
# --------------------------------------------------------------------------
HUIHUI = [
    {
        "card": "huihui-ai__Llama-3.2-1B-Instruct-abliterated.md",
        "url": "https://huggingface.co/huihui-ai/Llama-3.2-1B-Instruct-abliterated/blob/main/README.md",
        "parent": "meta-llama/Llama-3.2-1B-Instruct",
        "child": "huihui-ai/Llama-3.2-1B-Instruct-abliterated",
        "rows": [
            ("| IF_Eval     | **58.50**             | 56.88                             |", "IFEval", 58.50, 56.88),
            ("| MMLU Pro    | **16.35**             | 14.35                             |", "MMLU-PRO", 16.35, 14.35),
            ("| TruthfulQA  | **43.08**             | 38.96                             |", "TruthfulQA", 43.08, 38.96),
            ("| BBH         | **33.75**             | 31.83                             |", "BBH", 33.75, 31.83),
            ("| GPQA        | 25.96                 | **26.39**                         |", "GPQA", 25.96, 26.39),
        ],
    },
    {
        "card": "huihui-ai__Llama-3.2-3B-Instruct-abliterated.md",
        "url": "https://huggingface.co/huihui-ai/Llama-3.2-3B-Instruct-abliterated/blob/main/README.md",
        "parent": "meta-llama/Llama-3.2-3B-Instruct",
        "child": "huihui-ai/Llama-3.2-3B-Instruct-abliterated",
        "rows": [
            ("| IF_Eval     | 76.55                 | **76.76**                         |", "IFEval", 76.55, 76.76),
            ("| MMLU Pro    | 27.88                 | **28.00**                         |", "MMLU-PRO", 27.88, 28.00),
            ("| TruthfulQA  | 50.55                 | **50.73**                         |", "TruthfulQA", 50.55, 50.73),
            ("| BBH         | 41.81                 | **41.86**                         |", "BBH", 41.81, 41.86),
            ("| GPQA        | 28.39                 | **28.41**                         |", "GPQA", 28.39, 28.41),
        ],
    },
]


def card_text(name: str) -> str:
    p = CARDS / name
    if not p.exists():
        raise FileNotFoundError(f"cached card missing: {p} (run s2a_cards.py first)")
    return p.read_text()


def assert_literal(text: str, needle: str, what: str) -> None:
    if needle not in text:
        raise AssertionError(f"{what}: not a literal substring of the cached card -> {needle!r}")


def base_row(*, checkpoint: str, panel: dict, url: str, stype: str, version: str) -> dict:
    p = panel.get(checkpoint)
    return {
        "checkpoint_id": checkpoint,
        "lineage_id": p["lineage_id"] if p else "UNMAPPED_AUGMENTATION",
        "revision_sha_source": "UNSTATED",
        "revision_sha_panel": (p or {}).get("revision", "UNSTATED") or "UNSTATED",
        "revision_match": "SAME_REPO_UNKNOWN_SHA",
        "source_url": url,
        "source_type": stype,
        "source_version_or_release": version,
        "retrieval_date": RETRIEVAL_DATE,
    }


def main() -> None:
    panel_list = json.loads((RESULTS / "panel_resolved.json").read_text())
    panel = {x["hf_repo_id"]: x for x in panel_list}
    rows: list[dict] = []

    # ---- Source 1: Qwen3-4B-SafeRL card -----------------------------------
    qtext = card_text(QWEN_CARD)
    for (ckpt, mode), snip in QWEN_ROW_SNIPPETS.items():
        assert_literal(qtext, snip, f"Qwen {ckpt}/{mode}")
        vals = QWEN_VALUES[(ckpt, mode)]
        assert len(vals) == len(QWEN_COLS)
        for (bench, metric, axis, pol, scale, judge, circ, pev), v in zip(QWEN_COLS, vals):
            assert_literal(snip, str(v), f"Qwen value {v} for {ckpt}/{mode}")
            r = base_row(checkpoint=ckpt, panel=panel, url=QWEN_URL,
                         stype="OFFICIAL_MODEL_CARD",
                         version="Qwen3-4B-SafeRL model card, 'Performance' table; "
                                 "method detailed in the Qwen3Guard Technical Report")
            r.update({
                "benchmark": bench, "metric_name": f"{metric}__{mode.lower().replace('-', '_')}",
                "value": float(v), "scale": scale, "polarity": pol, "axis": axis,
                "judge_or_grader": judge, "circularity_flag": circ,
                "polarity_evidence": pev,
                "eval_mode": mode,
                "verbatim_snippet": snip[:300],
            })
            rows.append(r)
    logger.info(f"Qwen3-4B-SafeRL card: {len(rows)} rows "
                f"({len({r['checkpoint_id'] for r in rows})} checkpoints)")

    # ---- Source 2: Gemma 2 IT ethics-and-safety table ----------------------
    gtext = card_text(GEMMA_CARD)
    gbase_dup = card_text("google__gemma-2-2b.md")
    n0 = len(rows)
    for snip, bench, metric, val, axis, pol, scale, pev in GEMMA_ROWS:
        assert_literal(gtext, snip, f"Gemma {bench}")
        assert_literal(snip, str(val), f"Gemma value {val} for {bench}")
        for ckpt, note in GEMMA_TARGETS:
            r = base_row(checkpoint=ckpt, panel=panel, url=GEMMA_URL,
                         stype="OFFICIAL_MODEL_CARD",
                         version="Gemma 2 model card, 'Ethics and Safety' -> 'Gemma 2.0' "
                                 "table, column 'Gemma 2 IT 2B'")
            r.update({
                "benchmark": bench, "metric_name": metric, "value": float(val),
                "scale": scale, "polarity": pol, "axis": axis,
                "judge_or_grader": "UNSTATED",
                "circularity_flag": "",
                "polarity_evidence": pev,
                "checkpoint_attribution": note,
                "verbatim_snippet": snip[:300],
            })
            if note != "EXACT_MODEL_EVALUATED":
                r["revision_match"] = "FAMILY_ONLY"
            rows.append(r)
    dup = GEMMA_ROWS[0][0] in gbase_dup
    logger.info(f"Gemma 2 IT card: {len(rows) - n0} rows over {len(GEMMA_TARGETS)} repos; "
                f"identical table also present on the google/gemma-2-2b BASE card: {dup} "
                f"(no base rows emitted - the header says 'Gemma 2 IT 2B')")

    # ---- Source 3: huihui abliteration cards -------------------------------
    n0 = len(rows)
    for spec in HUIHUI:
        htext = card_text(spec["card"])
        for snip, bench, parent_v, child_v in spec["rows"]:
            assert_literal(htext, snip, f"huihui {spec['child']} {bench}")
            for ckpt, v, role in ((spec["parent"], parent_v, "parent_instruct"),
                                  (spec["child"], child_v, "abliterated_child")):
                assert_literal(snip, str(v), f"huihui value {v} ({role})")
                r = base_row(checkpoint=ckpt, panel=panel, url=spec["url"],
                             stype="THIRD_PARTY_REPO",
                             version=f"{spec['child']} model card, 'Evaluations' table")
                r.update({
                    "benchmark": bench, "metric_name": "score_metric_unstated",
                    "value": float(v),
                    "scale": "UNSTATED (0-100 percent by convention; the card states no scale)",
                    "polarity": "HIGHER_IS_MORE_CAPABLE", "axis": "CAPABILITY",
                    "judge_or_grader": "UNSTATED (repo script eval.sh, no harness version stated)",
                    "circularity_flag": "",
                    "polarity_evidence": "Standard accuracy-style benchmarks; the card bolds the higher value of each pair as the better one.",
                    "checkpoint_attribution": role,
                    "verbatim_snippet": snip[:300],
                })
                rows.append(r)
    logger.info(f"huihui abliteration cards: {len(rows) - n0} rows")

    by_axis: dict[str, int] = {}
    for r in rows:
        by_axis[r["axis"]] = by_axis.get(r["axis"], 0) + 1
    logger.info(f"TOTAL curated rows: {len(rows)}; by axis: {by_axis}; "
                f"checkpoints: {len({r['checkpoint_id'] for r in rows})}")
    (RESULTS / "curated_card_rows.json").write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()
