#!/usr/bin/env python3
"""Stage 2c: panel-overlap census over the published safety benchmarks.

For each safety source that does NOT expose a machine-readable per-model table
(HELM/AIR-Bench do, and are handled in s2b), fetch the primary document, cache it
verbatim, and search it for every panel checkpoint's model name.

The output is a coverage measurement, not a score harvest: for each source we
record how many panel checkpoints are named anywhere in the document at all. A
zero here is the finding -- it means the source evaluates nothing in our size
class, and the checkpoint must be measured in-house in iteration 3.

Matching is deliberately LOOSE (family+size tokens, case-insensitive) so the count
errs towards over-reporting overlap. An over-reported overlap is visible and gets
checked; an under-reported one silently hides a usable published number.
"""

from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import requests
from loguru import logger

HERE = Path(__file__).resolve().parent.parent
CACHE, RESULTS, LOGS = HERE / "cache", HERE / "results", HERE / "logs"
DOCS = CACHE / "safety_sources"
for d in (CACHE, RESULTS, LOGS, DOCS):
    d.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "s2c_census.log"), rotation="30 MB", level="DEBUG")

RETRIEVAL_DATE = date.today().isoformat()

SOURCES = [
    {"key": "sorry_bench", "label": "SORRY-Bench (ICLR 2025)", "arxiv": "2406.14598",
     "url": "https://arxiv.org/abs/2406.14598",
     "doc": "https://arxiv.org/html/2406.14598v2",
     "metric": "fulfillment rate on unsafe instructions (LOWER_IS_SAFER)"},
    {"key": "or_bench", "label": "OR-Bench (ICML 2025)", "arxiv": "2405.20947",
     "url": "https://arxiv.org/abs/2405.20947",
     "doc": "https://arxiv.org/pdf/2405.20947",
     "metric": "over-refusal rejection rate on safe prompts (LOWER_IS_SAFER) + toxic-prompt rejection rate (HIGHER_IS_SAFER)"},
    {"key": "xstest", "label": "XSTest (NAACL 2024)", "arxiv": "2308.01263",
     "url": "https://arxiv.org/abs/2308.01263",
     "doc": "https://arxiv.org/pdf/2308.01263",
     "metric": "full / partial refusal rate on 250 SAFE prompts (LOWER_IS_SAFER)"},
    {"key": "trustllm", "label": "TrustLLM (ICML 2024)", "arxiv": "2401.05561",
     "url": "https://arxiv.org/abs/2401.05561",
     "doc": "https://arxiv.org/pdf/2401.05561",
     "metric": "per-dimension trustworthiness scores (mixed polarity, stated per dimension)"},
    {"key": "salad_bench", "label": "SALAD-Bench (ACL Findings 2024)", "arxiv": "2402.05044",
     "url": "https://arxiv.org/abs/2402.05044",
     "doc": "https://arxiv.org/pdf/2402.05044",
     "metric": "attack success rate / safety rate per domain (ASR is LOWER_IS_SAFER)"},
    {"key": "decodingtrust", "label": "DecodingTrust (NeurIPS 2023)", "arxiv": "2306.11698",
     "url": "https://arxiv.org/abs/2306.11698",
     "doc": "https://arxiv.org/pdf/2306.11698",
     "metric": "per-perspective trustworthiness scores (mixed polarity)"},
    {"key": "jailbreakbench", "label": "JailbreakBench (NeurIPS D&B 2024)", "arxiv": "2404.01318",
     "url": "https://arxiv.org/abs/2404.01318",
     "doc": "https://arxiv.org/pdf/2404.01318",
     "metric": "attack success rate per attack/defence (LOWER_IS_SAFER)"},
    {"key": "harmbench", "label": "HarmBench (ICML 2024)", "arxiv": "2402.04249",
     "url": "https://arxiv.org/abs/2402.04249",
     "doc": "https://arxiv.org/pdf/2402.04249",
     "metric": "attack success rate (LOWER_IS_SAFER)"},
    {"key": "air_bench_paper", "label": "AIR-Bench 2024 (paper)", "arxiv": "2407.17436",
     "url": "https://arxiv.org/abs/2407.17436",
     "doc": "https://arxiv.org/pdf/2407.17436",
     "metric": "AIR-Bench safety score per risk category (HIGHER_IS_SAFER)"},
    {"key": "refusal_compliance_audit",
     "label": "The Refusal-Compliance Tradeoff: a large-scale safety behaviour audit",
     "arxiv": "2605.05427", "url": "https://arxiv.org/abs/2605.05427",
     "doc": "https://arxiv.org/html/2605.05427",
     "metric": "over-refusal rate ORR (LOWER_IS_SAFER) and harmful compliance rate HCR (LOWER_IS_SAFER)"},
]


FAMILY_SIZE = re.compile(
    r"(?:Llama|Qwen|Gemma|Mistral|Mixtral|Vicuna|Falcon|Phi|OLMo|SmolLM|TinyLlama|"
    r"Granite|Pythia)[-_ ]?[\d.]*[-_ ]?\d*\.?\d*\s?[Bb]?\b"
)


def model_patterns(repo: str) -> list[re.Pattern]:
    """Loose name patterns for a checkpoint: the bare model name with '-'/'_'/'.'/' '
    treated as interchangeable separators."""
    name = repo.split("/")[-1]
    sep = r"[-_. ]?"
    body = sep.join(re.escape(tok) for tok in re.split(r"[-_. ]+", name) if tok)
    return [re.compile(body, re.IGNORECASE)]


PAGE = 50000  # the fetch ability caps a single call at ~50k chars regardless of
# --max-chars, so the whole document is paged in with --char-offset. Scanning only
# the first page would silently miss every appendix results table.


def fetch(url: str, key: str) -> str:
    dest = DOCS / f"{key}.txt"
    if dest.exists():
        return dest.read_text()
    skill = Path("/ai-inventor/.claude/skills/aii-web-tools")
    py = (skill / ".." / ".ability_client_venv" / "bin" / "python").resolve()
    import subprocess

    parts: list[str] = []
    offset = 0
    for _ in range(24):  # hard stop at ~1.2M chars
        proc = subprocess.run(
            [str(py), str(skill / "scripts" / "aii_fast_web_fetch.py"),
             "fetch", "--url", url, "--max-chars", str(PAGE),
             "--char-offset", str(offset)],
            capture_output=True, text=True, timeout=600,
        )
        chunk = proc.stdout or ""
        body = chunk.split("--- Content ---", 1)[-1]
        if len(body.strip()) < 200:
            break
        parts.append(body)
        if len(body) < PAGE * 0.8:
            break
        offset += PAGE
    text = "".join(parts)
    if len(text) < 500:
        logger.warning(f"{key}: fetch returned only {len(text)} chars from {url}")
    logger.info(f"{key}: paged {len(parts)} chunk(s), {len(text)} chars from {url}")
    dest.write_text(text)
    return text


def main() -> None:
    panel = json.loads((RESULTS / "panel_resolved.json").read_text())
    ckpts = [x for x in panel if x["in_panel_le_4p2b"]]
    pats = {c["hf_repo_id"]: model_patterns(c["hf_repo_id"]) for c in ckpts}
    logger.info(f"Census over {len(SOURCES)} safety sources x {len(ckpts)} panel checkpoints")

    def work(src: dict) -> dict:
        text = fetch(src["doc"], src["key"])
        named = []
        for repo, ps in pats.items():
            for p in ps:
                m = p.search(text)
                if m:
                    lo = max(0, m.start() - 140)
                    named.append({
                        "checkpoint_id": repo,
                        "verbatim_snippet": text[lo:m.end() + 140].replace("\n", " ")[:300],
                    })
                    break
        # Evidence the census matcher is live and that the source evaluates a
        # different size class: the model-name tokens the document contains. Only
        # the token list is reported -- a regex-parsed "smallest size in B" was
        # tried and discarded because it picks up noise like "Llama-2 0B".
        tokens = sorted({
            m.group(0).strip()
            for m in FAMILY_SIZE.finditer(text)
        })
        return {
            "source": src["label"],
            "source_key": src["key"],
            "arxiv_id": src["arxiv"],
            "source_url": src["url"],
            "document_fetched": src["doc"],
            "document_chars": len(text),
            "primary_metric_and_polarity": src["metric"],
            "n_panel_checkpoints_named_in_document": len(named),
            "n_panel_checkpoints_total": len(ckpts),
            "panel_checkpoints_named": named,
            "model_name_tokens_found_in_document": tokens[:60],

            "retrieval_date": RETRIEVAL_DATE,
        }

    with ThreadPoolExecutor(max_workers=5) as ex:
        out = list(ex.map(work, SOURCES))

    for r in out:
        logger.info(
            f"{r['source_key']:28s} doc={r['document_chars']:>7d} chars  "
            f"panel checkpoints named: {r['n_panel_checkpoints_named_in_document']}/"
            f"{r['n_panel_checkpoints_total']}  "
            f"{[n['checkpoint_id'] for n in r['panel_checkpoints_named']]}"
        )
    (RESULTS / "safety_source_census.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
