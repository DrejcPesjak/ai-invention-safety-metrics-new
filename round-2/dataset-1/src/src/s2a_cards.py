#!/usr/bin/env python3
"""Stage 2a: fetch every panel checkpoint's model card and scan it for safety numbers.

Fetches https://huggingface.co/<repo>/raw/<revision>/README.md for all <=4.2B panel
checkpoints (plus the hypothesis-named augmentation repos), caches each card verbatim
under cache/cards/, and regex-scans for numerics that sit near a safety keyword.

This stage produces CANDIDATES, not rows. Every candidate carries the exact matched
line so a human/agent pass can confirm the benchmark, metric, scale and polarity
before it becomes an external_score row. Nothing is promoted automatically: a regex
cannot tell HIGHER_IS_SAFER from LOWER_IS_SAFER, and getting that backwards silently
flips a Spearman sign downstream.
"""

from __future__ import annotations

import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import requests
from loguru import logger

HERE = Path(__file__).resolve().parent.parent
CACHE, RESULTS, LOGS = HERE / "cache", HERE / "results", HERE / "logs"
CARDS = CACHE / "cards"
for d in (CACHE, RESULTS, LOGS, CARDS):
    d.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(LOGS / "s2a_cards.log"), rotation="30 MB", level="DEBUG")

RETRIEVAL_DATE = date.today().isoformat()
HDRS = {"User-Agent": "aii-iter2-dataset/1.0"}
_TOK = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
if _TOK:
    HDRS["Authorization"] = f"Bearer {_TOK}"

# Repos named by the hypothesis / needed for the circularity rule that are ABSENT
# from the iteration-1 frozen manifest. They are fetched and reported, and their
# panel membership is decided explicitly (see results/panel_augmentation.json).
AUGMENT = [
    "Qwen/Qwen3-4B-SafeRL",
    "Qwen/Qwen3Guard-Gen-4B",
    "Qwen/Qwen3-4B-Instruct-2507",
]

SAFETY_KEYWORDS = re.compile(
    r"(safety|safe[ -]?rate|refus|harmful|harmless|toxic|jailbreak|\bASR\b|"
    r"attack success|over[- ]?refus|WildGuard|Llama[- ]?Guard|Qwen3Guard|guard model|"
    r"XSTest|OR-Bench|SALAD|SorryBench|SORRY-Bench|HarmBench|AdvBench|BeaverTails|"
    r"ToxiGen|RealToxicity|DecodingTrust|TrustLLM|AIR-Bench|HELM Safety|"
    r"red[- ]?team|abliterat|uncensor|censorship|content filter|moderation)",
    re.IGNORECASE,
)
# Any bare number that could be a score: 0-100 with optional decimals, or a 0-1 rate.
# Deliberately permissive - this stage only produces CANDIDATES for curation, so a
# false positive costs a glance while a false negative loses a real published score.
NUMERIC = re.compile(r"(?<![\w.\-])(\d{1,3}(?:\.\d{1,4})?)(?![\w.])")


def fetch_card(repo: str, revision: str) -> tuple[str, str, int]:
    """Return (text, resolved_url, http_status). Falls back main -> pinned revision."""
    for rev in (revision or "main", "main"):
        url = f"https://huggingface.co/{repo}/raw/{rev}/README.md"
        try:
            r = requests.get(url, headers=HDRS, timeout=45)
        except Exception as exc:  # noqa: BLE001
            logger.debug(f"{repo}: {exc}")
            continue
        if r.status_code == 200:
            return r.text, url, 200
        last = r.status_code
    return "", f"https://huggingface.co/{repo}", locals().get("last", 0)


def scan(repo: str, text: str) -> list[dict]:
    """Return candidate (line, numbers) hits where a numeric sits near a safety word."""
    out = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not SAFETY_KEYWORDS.search(line):
            continue
        nums = NUMERIC.findall(line)
        # Markdown tables: the keyword may head the row while numbers follow in
        # the same row, or the keyword may head a COLUMN. Capture both by also
        # looking one line ahead when the keyword line itself has no numeric.
        ctx = line
        if not nums and i + 1 < len(lines):
            nxt = lines[i + 1]
            nums = NUMERIC.findall(nxt)
            if nums:
                ctx = line + " || " + nxt
        if not nums:
            continue
        out.append({
            "checkpoint_id": repo,
            "line_no": i + 1,
            "matched_keyword": SAFETY_KEYWORDS.search(line).group(0),
            "numbers_on_line": nums[:12],
            "verbatim_snippet": ctx.strip()[:300],
        })
    return out


def main() -> None:
    panel = json.loads((RESULTS / "panel_resolved.json").read_text())
    targets = [
        (x["hf_repo_id"], x.get("revision", ""), True)
        for x in panel if x["in_panel_le_4p2b"]
    ] + [(r, "", False) for r in AUGMENT]
    logger.info(f"Fetching {len(targets)} model cards "
                f"({sum(1 for t in targets if t[2])} panel + {len(AUGMENT)} augmentation)")

    def work(t):
        repo, rev, in_panel = t
        text, url, status = fetch_card(repo, rev)
        if text:
            (CARDS / (repo.replace("/", "__") + ".md")).write_text(text)
        return {
            "checkpoint_id": repo,
            "in_frozen_panel": in_panel,
            "card_url": url,
            "http_status": status,
            "card_chars": len(text),
            "hits": scan(repo, text) if text else [],
        }

    with ThreadPoolExecutor(max_workers=8) as ex:
        recs = list(ex.map(work, targets))

    ok = [r for r in recs if r["card_chars"] > 0]
    withhits = [r for r in recs if r["hits"]]
    logger.info(f"Cards fetched: {len(ok)}/{len(recs)}; "
                f"{len(withhits)} have >=1 safety-keyword-near-numeric hit")
    for r in sorted(withhits, key=lambda z: -len(z["hits"])):
        logger.info(f"  {r['checkpoint_id']}: {len(r['hits'])} hits")

    (RESULTS / "card_scan.json").write_text(json.dumps(recs, indent=1))
    logger.info(f"Wrote {RESULTS / 'card_scan.json'}; raw cards cached in {CARDS}")


if __name__ == "__main__":
    main()
