#!/usr/bin/env python3
"""Block 2 -- the three laundering corpora.

2a  sft_benign            OpenAssistant/oasst1, English single-turn pairs (Apache-2.0)
2b  fluency_wikitext      Salesforce/wikitext wikitext-2-raw-v1 test paragraphs
2c  heldout_benign_prompts databricks-dolly-15k prompts, mechanically disjoint from 2a

Every source is pinned to a resolved dataset-revision sha. A safety-topic regex
drops any pair touching harm/weapons/drugs/malware/etc, so the laundering
fine-tune is provably unrelated to safety; the drop count is reported.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from datasets import load_dataset
from loguru import logger
from transformers import AutoTokenizer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hub_common import API, ROOT, retry  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "corpora.log", rotation="30 MB", level="DEBUG")

# Deliberately broad: recall matters more than precision here, because a single
# safety-adjacent pair in the laundering set would confound the whole design.
SAFETY_RE = re.compile(
    r"(?i)\b("
    r"harm|harmful|harmless|weapon|gun|firearm|rifle|pistol|ammunition|bomb|explosiv|grenade|"
    r"drug|cocaine|heroin|meth|opioid|narcotic|overdose|"
    r"exploit|malware|virus|ransomware|hack|hacking|hacker|phishing|keylogger|botnet|ddos|"
    r"suicide|self[- ]harm|kill|murder|assassinat|torture|abuse|"
    r"hate|racist|racism|slur|nazi|terroris|extremis|"
    r"illegal|unlawful|crime|criminal|fraud|launder|smuggl|traffick|"
    r"jailbreak|uncensored|abliterat|refus|unsafe|toxic|poison|nsfw|porn|sexual|"
    r"bioweapon|anthrax|nerve agent|chemical weapon|radioactive|nuclear weapon"
    r")\b"
)

MAX_RESP_CHARS = 2000
TARGET_SFT = 5000
WIKI_MIN_CHARS = 200
WIKI_TARGET = 1000
HELDOUT_TARGET = 200


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", re.sub(r"\s+", " ", s.lower())).strip()


def five_grams(s: str) -> set[str]:
    w = norm(s).split()
    if len(w) < 5:
        return {" ".join(w)} if w else set()
    return {" ".join(w[i : i + 5]) for i in range(len(w) - 4)}


def ds_sha(repo: str) -> str:
    return retry(lambda: API.dataset_info(repo)).sha


# --------------------------------------------------------------------- 2a ----
def build_sft() -> dict:
    repo = "OpenAssistant/oasst1"
    sha = ds_sha(repo)
    logger.info(f"2a: {repo} @ {sha}")
    ds = load_dataset(repo, split="train", revision=sha)

    by_id = {r["message_id"]: r for r in ds}
    logger.info(f"2a: {len(by_id)} messages loaded")

    cand = []
    for r in by_id.values():
        if r["role"] != "assistant" or r["lang"] != "en" or r["deleted"]:
            continue
        p = by_id.get(r["parent_id"])
        if p is None or p["role"] != "prompter" or p["lang"] != "en" or p["deleted"]:
            continue
        # depth 0/1 only: the prompter turn must itself be a conversation root
        if p["parent_id"] is not None:
            continue
        rank = r.get("rank")
        cand.append(
            {
                "instruction": p["text"].strip(),
                "response": r["text"].strip()[:MAX_RESP_CHARS],
                "source_id": r["message_id"],
                "parent_id": p["message_id"],
                "rank": -1 if rank is None else int(rank),
                "review_count": r.get("review_count") or 0,
            }
        )
    logger.info(f"2a: {len(cand)} en depth-0/1 prompter->assistant pairs")

    kept, dropped_safety = [], 0
    for c in cand:
        if SAFETY_RE.search(c["instruction"]) or SAFETY_RE.search(c["response"]):
            dropped_safety += 1
            continue
        kept.append(c)
    logger.info(f"2a: dropped {dropped_safety} safety-topic pairs, {len(kept)} remain")

    # rank 0 = best-rated sibling; prefer those, then higher review counts
    kept.sort(key=lambda c: (c["rank"] if c["rank"] >= 0 else 99, -c["review_count"]))
    seen: set[str] = set()
    final, dropped_dupe = [], 0
    for c in kept:
        k = norm(c["instruction"])
        if k in seen:
            dropped_dupe += 1
            continue
        seen.add(k)
        final.append(c)
        if len(final) >= TARGET_SFT:
            break
    logger.info(f"2a: {len(final)} final pairs (dropped {dropped_dupe} duplicate instructions)")

    return {
        "rows": final,
        "meta": {
            "source_repo": repo,
            "source_revision": sha,
            "license": "apache-2.0",
            "split": "train",
            "n_messages_scanned": len(by_id),
            "n_candidate_pairs": len(cand),
            "n_dropped_safety_topic": dropped_safety,
            "n_dropped_duplicate_instruction": dropped_dupe,
            "n_final": len(final),
            "max_response_chars": MAX_RESP_CHARS,
            "selection": "lang=en, deleted=False, role=assistant, parent role=prompter at tree root (depth 0/1), safety-topic regex removed, deduped on normalised instruction, sorted by rank then review_count",
        },
    }


# --------------------------------------------------------------------- 2b ----
def build_wikitext() -> dict:
    repo = "Salesforce/wikitext"
    sha = ds_sha(repo)
    logger.info(f"2b: {repo} @ {sha}")
    ds = load_dataset(repo, "wikitext-2-raw-v1", split="test", revision=sha)

    heading = re.compile(r"^\s*=+ .* =+\s*$")
    rows = []
    for i, r in enumerate(ds):
        t = r["text"]
        if not t.strip() or heading.match(t):
            continue
        t = t.strip()
        if len(t) < WIKI_MIN_CHARS:
            continue
        rows.append({"text": t, "source_index": i})
        if len(rows) >= WIKI_TARGET:
            break
    logger.info(f"2b: {len(rows)} paragraphs >= {WIKI_MIN_CHARS} chars")

    tok = AutoTokenizer.from_pretrained("gpt2")
    tlens = [len(tok(r["text"])["input_ids"]) for r in rows]
    for r, n in zip(rows, tlens):
        r["n_tokens_gpt2"] = n
    clens = sorted(len(r["text"]) for r in rows)
    st = sorted(tlens)

    def q(xs, p):
        return xs[min(len(xs) - 1, int(p * len(xs)))]

    return {
        "rows": rows,
        "meta": {
            "source_repo": repo,
            "source_revision": sha,
            "config": "wikitext-2-raw-v1",
            "split": "test",
            "license": "cc-by-sa-3.0 / gfdl",
            "n_final": len(rows),
            "min_chars_filter": WIKI_MIN_CHARS,
            "heading_lines_stripped": True,
            "known_artifact": "WikiText raw text retains the corpus' @-@ / @,@ / @.@ substitutions for hyphens and numeric separators. This is inherent to WikiText (both -v1 and -raw-v1) and is what lm-evaluation-harness scores against; it is reported here so a perplexity screen is not surprised by it, not treated as a defect.",
            "char_stats": {
                "min": clens[0],
                "median": q(clens, 0.5),
                "p90": q(clens, 0.9),
                "max": clens[-1],
            },
            "token_stats_gpt2": {
                "tokenizer": "gpt2",
                "min": st[0],
                "median": q(st, 0.5),
                "p90": q(st, 0.9),
                "max": st[-1],
                "total": sum(st),
            },
        },
    }


# --------------------------------------------------------------------- 2c ----
def build_heldout(sft_rows: list[dict]) -> dict:
    repo = "databricks/databricks-dolly-15k"
    sha = ds_sha(repo)
    logger.info(f"2c: {repo} @ {sha}")
    ds = load_dataset(repo, split="train", revision=sha)

    keep_cat = {"open_qa", "brainstorming", "creative_writing", "general_qa"}
    cand = []
    for i, r in enumerate(ds):
        if r["category"] not in keep_cat or (r.get("context") or "").strip():
            continue
        q_ = r["instruction"].strip()
        if not (20 <= len(q_) <= 200):
            continue
        if SAFETY_RE.search(q_) or SAFETY_RE.search(r["response"]):
            continue
        cand.append({"prompt": q_, "category": r["category"], "source_index": i})
    logger.info(f"2c: {len(cand)} candidate prompts after category/length/safety filters")

    sft_norm = {norm(r["instruction"]) for r in sft_rows}
    sft_grams = [five_grams(r["instruction"]) for r in sft_rows]
    # inverted index: only 2a rows sharing at least one 5-gram can reach J >= 0.5
    index: dict[str, set[int]] = {}
    for j, sg in enumerate(sft_grams):
        for g_ in sg:
            index.setdefault(g_, set()).add(j)

    out, drop_exact, drop_jaccard = [], 0, 0
    for c in cand:
        if norm(c["prompt"]) in sft_norm:
            drop_exact += 1
            continue
        g = five_grams(c["prompt"])
        hit = False
        if g:
            neighbours: set[int] = set()
            for g_ in g:
                neighbours |= index.get(g_, set())
            for j in neighbours:
                sg = sft_grams[j]
                inter = len(g & sg)
                if inter and inter / len(g | sg) >= 0.5:
                    hit = True
                    break
        if hit:
            drop_jaccard += 1
            continue
        out.append(c)
        if len(out) >= HELDOUT_TARGET:
            break
    logger.info(f"2c: {len(out)} kept; dropped exact={drop_exact} jaccard={drop_jaccard}")

    return {
        "rows": out,
        "meta": {
            "source_repo": repo,
            "source_revision": sha,
            "license": "cc-by-sa-3.0",
            "split": "train",
            "categories_kept": sorted(keep_cat),
            "n_candidates": len(cand),
            "n_dropped_exact_match_vs_2a": drop_exact,
            "n_dropped_5gram_jaccard_ge_0.5_vs_2a": drop_jaccard,
            "n_final": len(out),
            "disjointness": "different source repo from 2a (oasst1) by construction, then exact normalised-text dedupe and 5-gram Jaccard >= 0.5 filter against every 2a instruction",
        },
    }


def main() -> None:
    sft = build_sft()
    wiki = build_wikitext()
    held = build_heldout(sft["rows"])
    out = ROOT / "results" / "corpora.json"
    out.write_text(json.dumps({"sft": sft, "wikitext": wiki, "heldout": held}))
    logger.info(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
