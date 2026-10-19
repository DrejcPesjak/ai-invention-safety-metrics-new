#!/usr/bin/env python3
"""Single entry point: build full_data_out.json from local files only.

    uv run data.py

Reads nothing from the network. The ten evaluated HuggingFace dataset
candidates live in temp/datasets/ (downloaded by download_candidates.py) and the
Hub METADATA harvest lives in results/ (harvest_enumerate.py ->
resolve_parents.py -> fetch_repo_details.py). This script turns those into the
five delivered datasets, one example per data ROW, grouped by dataset.

Selection: ten dataset candidates were downloaded and inspected; five datasets
are shipped. See CANDIDATE_EVALUATION below -- the verdict for every one of the
ten is recorded in the output, kept and dropped alike.

Scope guard: DATA ONLY. No weights, no forward passes, no training, no AUROC.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from loguru import logger
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import recipes  # noqa: E402
from build_dataset import (  # noqa: E402
    HAND_CHECK,
    build_manifest,
    build_pool,
)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "data.log", rotation="30 MB", level="DEBUG")

DATASETS_DIR = ROOT / "temp" / "datasets"
COLLECTED_AT = date.today().isoformat()

# Resolved at collection time via HfApi().dataset_info(...).sha and pinned here,
# so this script reproduces the exact same rows with no network access.
PINNED = {
    "OpenAssistant/oasst1": "fdf72ae0827c1cda404aff25b6603abec9e3399b",
    "Salesforce/wikitext": "b08601e04326c79dfdd32d625aee71d232d685c3",
    "databricks/databricks-dolly-15k": "bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a",
}

# Every candidate that was downloaded and inspected, with its verdict. Ten in,
# five out; the five dropped are recorded rather than quietly omitted.
CANDIDATE_EVALUATION = [
    {
        "repo": "OpenAssistant/oasst1",
        "verdict": "SHIPPED as sft_benign (2a)",
        "license": "apache-2.0",
        "why": "Apache-2.0 (the only permissive licence among the human-written instruction corpora), NeurIPS 2023 D&B paper arXiv:2304.07327, and per-message `rank` labels that let the best sibling reply be chosen without a model in the loop.",
    },
    {
        "repo": "Salesforce/wikitext",
        "verdict": "SHIPPED as fluency_wikitext (2b)",
        "license": "cc-by-sa-3.0 / gfdl",
        "why": "1.49M downloads; Merity et al. ICLR 2017 (arXiv:1609.07843); the reference perplexity corpus that lm-evaluation-harness scores against, so a fluency screen built on it is comparable to published numbers.",
    },
    {
        "repo": "databricks/databricks-dolly-15k",
        "verdict": "SHIPPED as heldout_benign_prompts (2c)",
        "license": "cc-by-sa-3.0",
        "why": "A DIFFERENT source repo from 2a, which is what makes the held-out set disjoint by construction rather than by filtering alone; human-written by 5,000+ Databricks employees; category labels isolate context-free prompts.",
    },
    {
        "repo": "allenai/tulu-3-sft-personas-instruction-following",
        "verdict": "dropped",
        "license": "odc-by",
        "why": "Permissive and well documented, but synthetic persona-generated prompts carrying explicit IFEval-style format constraints. A laundering fine-tune should be ordinary benign text, not constraint-following drills.",
    },
    {
        "repo": "allenai/tulu-3-sft-mixture",
        "verdict": "dropped",
        "license": "odc-by (mixed)",
        "why": "Its own card states some portions are non-commercial. Mixed provenance defeats the point of a cleanly-licensed laundering corpus.",
    },
    {
        "repo": "OpenAssistant/oasst2",
        "verdict": "dropped",
        "license": "apache-2.0",
        "why": "A superset of oasst1 with the same structure and licence. Shipping both would add rows without adding independence, and oasst1 is the version with the citable paper.",
    },
    {
        "repo": "OpenAssistant/oasst_top1_2023-08-25",
        "verdict": "dropped",
        "license": "apache-2.0",
        "why": "A pre-flattened top-1 export of the same oasst trees. Pre-joined ChatML strings give less control than reconstructing depth-0/1 pairs ourselves, and it is not independent of 2a.",
    },
    {
        "repo": "timdettmers/openassistant-guanaco",
        "verdict": "dropped",
        "license": "apache-2.0",
        "why": "Also an oasst subset, and multilingual: sampled rows include Spanish. 2a requires English-only, and it is not independent of 2a.",
    },
    {
        "repo": "argilla/databricks-dolly-15k-curated-en",
        "verdict": "dropped",
        "license": "cc-by-sa-3.0",
        "why": "A curation pass over the same dolly rows. Not independent of 2c, and its original-/new- column pairs add ambiguity about which text is canonical.",
    },
    {
        "repo": "HuggingFaceTB/everyday-conversations-llama3.1-2k",
        "verdict": "dropped",
        "license": "apache-2.0",
        "why": "Only 2,260 rows, below the >=3000 floor for 2a, and Llama-3.1-generated rather than human-written.",
    },
]

# Deliberately broad: one safety-adjacent pair in the laundering set would
# confound the whole design, so recall matters more than precision here.
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


def load_dump(slug: str) -> list[dict]:
    p = DATASETS_DIR / f"full_{slug}.json"
    if not p.exists():
        raise FileNotFoundError(
            f"{p} missing -- run `uv run download_candidates.py` first (it writes temp/datasets/)"
        )
    return json.loads(p.read_text())


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", re.sub(r"\s+", " ", s.lower())).strip()


def five_grams(s: str) -> set[str]:
    w = norm(s).split()
    if len(w) < 5:
        return {" ".join(w)} if w else set()
    return {" ".join(w[i : i + 5]) for i in range(len(w) - 4)}


# --------------------------------------------------------------------- 2a ----
def build_sft() -> dict:
    repo = "OpenAssistant/oasst1"
    msgs = load_dump("OpenAssistant_oasst1_default_train")
    by_id = {r["message_id"]: r for r in msgs}
    logger.info(f"2a: {len(by_id)} oasst1 messages from local dump")

    def truthy(v) -> bool:
        # the local dump was written with default=str, so booleans may be "True"
        return v is True or (isinstance(v, str) and v.lower() == "true")

    cand = []
    for r in by_id.values():
        if r["role"] != "assistant" or r["lang"] != "en" or truthy(r["deleted"]):
            continue
        p = by_id.get(r["parent_id"])
        if p is None or p["role"] != "prompter" or p["lang"] != "en" or truthy(p["deleted"]):
            continue
        if p["parent_id"] not in (None, "None", ""):
            continue  # depth 0/1 only: the prompter turn must be a tree root
        rank = r.get("rank")
        try:
            rank_i = int(float(rank))
        except (TypeError, ValueError):
            rank_i = -1
        try:
            rc = int(float(r.get("review_count") or 0))
        except (TypeError, ValueError):
            rc = 0
        cand.append(
            {
                "instruction": p["text"].strip(),
                "response": r["text"].strip()[:MAX_RESP_CHARS],
                "source_id": r["message_id"],
                "parent_id": p["message_id"],
                "rank": rank_i,
                "review_count": rc,
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

    kept.sort(key=lambda c: (c["rank"] if c["rank"] >= 0 else 99, -c["review_count"]))
    seen, final, dropped_dupe = set(), [], 0
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
    if len(final) < 3000:
        raise RuntimeError(f"2a floor breached: {len(final)} < 3000 pairs")

    return {
        "rows": final,
        "meta": {
            "source_repo": repo,
            "source_revision": PINNED[repo],
            "source_local_dump": "temp/datasets/full_OpenAssistant_oasst1_default_train.json",
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
    rows_in = load_dump("Salesforce_wikitext_wikitext-2-raw-v1_test")
    heading = re.compile(r"^\s*=+ .* =+\s*$")
    rows = []
    for i, r in enumerate(rows_in):
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
            "source_revision": PINNED[repo],
            "source_local_dump": "temp/datasets/full_Salesforce_wikitext_wikitext-2-raw-v1_test.json",
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
    rows_in = load_dump("databricks_databricks-dolly-15k_default_train")
    keep_cat = {"open_qa", "brainstorming", "creative_writing", "general_qa"}

    cand = []
    for i, r in enumerate(rows_in):
        if r["category"] not in keep_cat or (r.get("context") or "").strip():
            continue
        q_ = r["instruction"].strip()
        if not (20 <= len(q_) <= 200):
            continue
        if SAFETY_RE.search(q_) or SAFETY_RE.search(r["response"]):
            continue
        cand.append({"prompt": q_, "category": r["category"], "source_index": i})
    logger.info(f"2c: {len(cand)} candidates after category/length/safety filters")

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
            "source_revision": PINNED[repo],
            "source_local_dump": "temp/datasets/full_databricks_databricks-dolly-15k_default_train.json",
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


# --------------------------------------------------------------------------- #
def main() -> None:
    enum = {
        m["repo_id"]: m
        for m in json.loads((ROOT / "results" / "enumerated.json").read_text())["models"]
    }
    det = {d["repo_id"]: d for d in json.loads((ROOT / "results" / "details.json").read_text())}
    logger.info(f"hub metadata: {len(enum)} enumerated repos, {len(det)} with details")

    manifest, m_meta = build_manifest(enum, det)
    logger.info(f"block 1: {len(manifest)} rows; {m_meta['coverage']['diversity_floors']}")
    pool, p_cov = build_pool(enum, det, {r["repo_id"] for r in manifest})
    logger.info(f"block 3: {len(pool)} rows; strata {p_cov['strata_achieved']}")

    sft = build_sft()
    wiki = build_wikitext()
    held = build_heldout(sft["rows"])

    ev_docs = {}
    for name, meta in recipes.EVIDENCE_DOCS.items():
        f = ROOT / "evidence" / f"{name}.md"
        if f.exists():
            ev_docs[name] = {
                **meta,
                "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                "bytes": f.stat().st_size,
                "local_path": f"evidence/{name}.md",
            }

    datasets = [
        {
            "dataset": "edit_manifest",
            "examples": [
                {
                    "input": r["repo_id"],
                    "output": r["recipe_class"] if r["recipe_class"] else "PARENT",
                    "metadata_fold": "edit_manifest",
                    "metadata_block": "1",
                    "metadata_row_id": r["row_id"],
                    "metadata_task_type": "classification",
                    "metadata_features": r,
                }
                for r in manifest
            ],
        },
        {
            "dataset": "sft_benign",
            "examples": [
                {
                    "input": r["instruction"],
                    "output": r["response"],
                    "metadata_fold": "sft_benign",
                    "metadata_block": "2a",
                    "metadata_row_id": f"sft_{i:05d}",
                    "metadata_task_type": "generation",
                    "metadata_row_index": i,
                    "metadata_features": r,
                }
                for i, r in enumerate(sft["rows"])
            ],
        },
        {
            "dataset": "fluency_wikitext",
            "examples": [
                {
                    "input": r["text"],
                    "output": "",
                    "metadata_fold": "fluency_wikitext",
                    "metadata_block": "2b",
                    "metadata_row_id": f"wiki_{i:05d}",
                    "metadata_task_type": "language_modeling",
                    "metadata_row_index": i,
                    "metadata_features": r,
                }
                for i, r in enumerate(wiki["rows"])
            ],
        },
        {
            "dataset": "heldout_benign_prompts",
            "examples": [
                {
                    "input": r["prompt"],
                    "output": "",
                    "metadata_fold": "heldout_benign_prompts",
                    "metadata_block": "2c",
                    "metadata_row_id": f"held_{i:05d}",
                    "metadata_task_type": "generation_prompt",
                    "metadata_row_index": i,
                    "metadata_features": r,
                }
                for i, r in enumerate(held["rows"])
            ],
        },
        {
            "dataset": "hub_scan_pool",
            "examples": [
                {
                    "input": r["repo_id"],
                    "output": "declared" if r["declares_abliteration"] else "not_declared",
                    "metadata_fold": "hub_scan_pool",
                    "metadata_block": "3",
                    "metadata_row_id": r["row_id"],
                    "metadata_task_type": "classification",
                    "metadata_features": r,
                }
                for r in pool
            ],
        },
    ]

    m_meta["coverage"]["hand_check"] = HAND_CHECK
    out = {
        "metadata": {
            "title": "Labelled Edit-Recipe Model Manifest + laundering corpora + Hub scan pool",
            "collected_at": COLLECTED_AT,
            "built_by": "data.py (uv run data.py) -- local files only, no network access",
            "empty_output_note": "fluency_wikitext and heldout_benign_prompts are unlabelled by design -- a perplexity paragraph and a generation prompt have no target. The plan specifies output=null; the schema requires a string, so they carry \"\". An empty output in those two folds is intentional, not a missing value.",
            "scope_guard": "DATA ONLY. No model weights were downloaded, no forward pass was run, nothing was trained, no detector statistic (W01-W05) was computed and no AUROC is reported. Parameter counts come from the Hub's safetensors index; file sizes from the Hub file index.",
            "dataset_selection": {
                "n_candidates_downloaded": len(CANDIDATE_EVALUATION),
                "n_shipped": sum(
                    1 for c in CANDIDATE_EVALUATION if c["verdict"].startswith("SHIPPED")
                ),
                "note": "Ten HuggingFace dataset candidates were downloaded to temp/datasets/ and inspected; three of them are shipped as Blocks 2a/2b/2c. The other two delivered datasets (edit_manifest, hub_scan_pool) are built from the HuggingFace MODEL Hub metadata harvest rather than from a dataset repo, which is why the five shipped datasets are not simply five of the ten. Five dataset candidates were dropped and each reason is recorded below.",
                "candidates": CANDIDATE_EVALUATION,
            },
            "dataset_meta": {
                "blocks": {
                    "1_edit_manifest": {
                        "source": "Hugging Face Hub model listings + model cards",
                        "ceiling_params": 4.2e9,
                        "recipe_class_vocabulary": recipes.CLASSES,
                        "labelling_precedence": [r[1] for r in recipes.RULES],
                        "evidence_documents": ev_docs,
                        **m_meta,
                    },
                    "2a_sft_benign": sft["meta"],
                    "2b_fluency_wikitext": wiki["meta"],
                    "2c_heldout_benign_prompts": held["meta"],
                    "3_hub_scan_pool": {
                        "source": "Hugging Face Hub model listings",
                        "ceiling_params": 4.0e9,
                        **p_cov,
                    },
                },
                "coverage": {
                    "block_1": m_meta["coverage"],
                    "block_2": {
                        "sft_benign": sft["meta"],
                        "fluency_wikitext": wiki["meta"],
                        "heldout_benign_prompts": held["meta"],
                    },
                    "block_3": p_cov,
                },
            },
        },
        "datasets": datasets,
    }

    p = ROOT / "full_data_out.json"
    p.write_text(json.dumps(out))
    logger.info(f"wrote {p} ({p.stat().st_size / 1e6:.1f} MB)")
    total = 0
    for d in datasets:
        total += len(d["examples"])
        logger.info(f"  {d['dataset']}: {len(d['examples'])} examples")
    logger.info(f"  TOTAL: {total} examples across {len(datasets)} datasets")


if __name__ == "__main__":
    main()
