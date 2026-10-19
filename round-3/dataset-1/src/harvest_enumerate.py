#!/usr/bin/env python3
"""Step 1 -- enumerate Hub candidate checkpoints (metadata only, no weights).

Runs the Block-1 (edit-manifest candidate) and Block-3 (scan pool) sweeps in one
pass, because both are `list_models` calls over the same Hub and the union is
cheaper to page once than twice. Writes raw per-query listings to cache/ and a
deduplicated candidate table to results/enumerated.json.

Nothing here downloads weights: `list_models(expand=[...])` returns the resolved
commit sha and the safetensors parameter counts from the Hub's own index.
"""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hub_common import API, ROOT, retry  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "enumerate.log", rotation="30 MB", level="DEBUG")

EXPAND = [
    "safetensors",
    "downloads",
    "likes",
    "config",
    "cardData",
    "tags",
    "lastModified",
    "sha",
    "pipeline_tag",
    "library_name",
]

# --- Block 1: edit-recipe candidate sweeps -------------------------------------
SEARCH_TERMS = [
    "abliterated",
    "gabliterated",
    "obliterated",
    "uncensored",
    "decensored",
    "orthogonalized",
    "norm-preserved",
    "biprojected",
    "refusal",
    "Josiefied",
    "lorablated",
    "heretic",
    "unaligned",
    "refusal-removed",
    "projected abliteration",
    "amoral",
    "toxic-dpo",
    "unfiltered",
    "no-refusal",
    "safetensors abliterated",
]

AUTHORS = [
    "huihui-ai",
    "Goekdeniz-Guelmez",
    "mlabonne",
    "grimjim",
    "failspy",
    "byroneverson",
    "NousResearch",
    "lunahr",
    "prithivMLmods",
    "DavidAU",
    "cognitivecomputations",
    "TheDrummer",
    "nicoboss",
    "bunnycore",
    "Undi95",
    "Delta-Vector",
    "ClaudioItaly",
    "nbeerbower",
    "p-e-w",
    "SicariusSicariiStuff",
]

# --- Block 3: scan-pool per-architecture sweeps --------------------------------
ARCHES = [
    "qwen2",
    "qwen3",
    "llama",
    "gemma2",
    "gemma3",
    "phi3",
    "mistral",
    "olmo",
    "olmo2",
    "gpt_neox",
    "stablelm",
    "granite",
    "falcon",
    "minicpm",
    "smollm",
    "smollm3",
    "exaone",
    "internlm2",
    "cohere",
    "bloom",
]


def _slim(m) -> dict:
    """Keep only what the manifest needs; ModelInfo itself is not JSON-safe."""
    st = getattr(m, "safetensors", None)
    cfg = getattr(m, "config", None) or {}
    card = getattr(m, "cardData", None) or {}
    lm = getattr(m, "last_modified", None)
    return {
        "repo_id": m.id,
        "sha": getattr(m, "sha", None),
        "downloads": getattr(m, "downloads", None),
        "likes": getattr(m, "likes", None),
        "tags": list(getattr(m, "tags", None) or []),
        "pipeline_tag": getattr(m, "pipeline_tag", None),
        "library_name": getattr(m, "library_name", None),
        "last_modified": lm.isoformat() if lm is not None else None,
        "st_total": getattr(st, "total", None) if st is not None else None,
        "st_parameters": dict(getattr(st, "parameters", None) or {}) if st is not None else None,
        "architectures": cfg.get("architectures"),
        "model_type": cfg.get("model_type"),
        "tokenizer_config": cfg.get("tokenizer_config"),
        "card_base_model": card.get("base_model"),
        "card_license": card.get("license"),
        "card_tags": card.get("tags"),
    }


def sweep(kind: str, value: str, limit: int) -> list[dict]:
    """One list_models query. `kind` selects search= / author= / arch-filter."""
    kwargs: dict = {
        "sort": "downloads",
        "limit": limit,
        "expand": EXPAND,  # already yields cardData; passing cardData= too is an error
    }
    if kind == "search":
        kwargs["search"] = value
        kwargs["filter"] = "text-generation"
    elif kind == "author":
        kwargs["author"] = value
    elif kind == "arch":
        kwargs["filter"] = ["text-generation", value]
    elif kind == "top":
        kwargs["filter"] = "text-generation"
    else:
        raise ValueError(kind)

    def _go():
        return [_slim(m) for m in API.list_models(**kwargs)]

    try:
        rows = retry(_go)
    except Exception as e:  # a dead query must not kill the sweep
        logger.error(f"sweep {kind}={value} failed: {e}")
        return []
    logger.info(f"sweep {kind}={value!r}: {len(rows)} rows")
    (ROOT / "cache" / "sweeps").mkdir(parents=True, exist_ok=True)
    (ROOT / "cache" / "sweeps" / f"{kind}__{value.replace('/', '_')}.json").write_text(
        json.dumps(rows)
    )
    return rows


def main() -> None:
    jobs: list[tuple[str, str, int]] = []
    jobs += [("search", t, 1000) for t in SEARCH_TERMS]
    jobs += [("author", a, 1000) for a in AUTHORS]
    jobs += [("arch", a, 700) for a in ARCHES]
    jobs += [("top", "all", 3000)]
    logger.info(f"{len(jobs)} sweeps queued")

    all_rows: dict[str, dict] = {}
    query_hits: dict[str, list[str]] = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(sweep, k, v, n): (k, v) for k, v, n in jobs}
        for f in as_completed(futs):
            k, v = futs[f]
            rows = f.result()
            query_hits[f"{k}:{v}"] = [r["repo_id"] for r in rows]
            for r in rows:
                prev = all_rows.get(r["repo_id"])
                # a later sweep may carry fields an earlier one lacked
                if prev is None:
                    r["found_by"] = [f"{k}:{v}"]
                    all_rows[r["repo_id"]] = r
                else:
                    prev["found_by"].append(f"{k}:{v}")
                    for key, val in r.items():
                        if prev.get(key) is None and val is not None:
                            prev[key] = val

    out = ROOT / "results" / "enumerated.json"
    out.parent.mkdir(exist_ok=True, parents=True)
    out.write_text(json.dumps({"queries": query_hits, "models": list(all_rows.values())}))
    logger.info(f"{len(all_rows)} distinct repos -> {out} ({out.stat().st_size / 1e6:.1f} MB)")

    n_st = sum(1 for r in all_rows.values() if r["st_total"])
    n_sub = sum(1 for r in all_rows.values() if (r["st_total"] or 0) and r["st_total"] <= 4.2e9)
    logger.info(f"with safetensors param count: {n_st}; sub-4.2B: {n_sub}")


if __name__ == "__main__":
    main()
