#!/usr/bin/env python3
"""Step 1f -- resolve declared parents the sweeps did not happen to enumerate.

The Block-1 sweeps are keyword/author/architecture driven, so a parent that is
neither popular nor abliteration-named (an obscure base model, or an
intermediate merge) never shows up. Those are exactly the rows the H3
parent-vs-child head-to-head needs, so they are fetched by name here and merged
into results/enumerated.json.

Metadata only: model_info(expand=[...]) reads the Hub's index, not the weights.
"""

from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from huggingface_hub.utils import GatedRepoError, RepositoryNotFoundError
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hub_common import ABLIT_RE, API, ROOT, cached_json, retry  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "parents.log", rotation="30 MB", level="DEBUG")

HARVEST = re.compile(ABLIT_RE + r"|(heretic|lorablated|josiefied|amoral|unfiltered|unalign)")
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


def resolve(repo_id: str) -> dict | None:
    def _go():
        try:
            m = retry(lambda: API.model_info(repo_id, expand=EXPAND))
        except (RepositoryNotFoundError, GatedRepoError) as e:
            return {"repo_id": repo_id, "_unresolved": type(e).__name__}
        except Exception as e:
            logger.debug(f"{repo_id}: {type(e).__name__}: {e}")
            return {"repo_id": repo_id, "_unresolved": type(e).__name__}
        st = getattr(m, "safetensors", None)
        cfg = getattr(m, "config", None) or {}
        card = getattr(m, "cardData", None) or {}
        lm = getattr(m, "last_modified", None)
        return {
            "repo_id": m.id,
            "sha": m.sha,
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
            "found_by": ["parent_resolution"],
        }

    return cached_json("parents", repo_id, _go)


def main() -> None:
    path = ROOT / "results" / "enumerated.json"
    blob = json.loads(path.read_text())
    enum = {m["repo_id"]: m for m in blob["models"]}

    wanted: set[str] = set()
    for m in blob["models"]:
        n = m.get("st_total") or 0
        if not (n and n <= 4.2e9 and HARVEST.search(m["repo_id"])):
            continue
        bm = m.get("card_base_model")
        for p in [bm] if isinstance(bm, str) else (bm or []):
            if isinstance(p, str) and "/" in p and p not in enum:
                wanted.add(p)
    logger.info(f"{len(wanted)} declared parents to resolve by name")

    added, unresolved = 0, 0
    with ThreadPoolExecutor(max_workers=12) as pool:
        futs = {pool.submit(resolve, p): p for p in sorted(wanted)}
        for f in as_completed(futs):
            r = f.result()
            if not r:
                continue
            if r.get("_unresolved"):
                unresolved += 1
                continue
            enum[r["repo_id"]] = r
            added += 1
    logger.info(f"resolved {added}, unresolved {unresolved}")

    blob["models"] = list(enum.values())
    path.write_text(json.dumps(blob))
    logger.info(f"enumeration now {len(enum)} repos -> {path}")


if __name__ == "__main__":
    main()
