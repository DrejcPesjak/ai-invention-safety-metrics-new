#!/usr/bin/env python3
"""Step 2 -- per-repo detail fetch: file list with sizes + README + configs.

Weights are never touched. `files_metadata=True` returns sizes from the Hub's
own file index, and only README.md / config.json / tokenizer_config.json are
downloaded (kilobytes). Every response is cached under cache/ so a rerun after
a crash costs nothing.

Selection: (a) every sub-4.2B repo whose id matches the abliteration regex
(Block-1 candidates), (b) the most-downloaded sub-4.0B repos (Block-3 scan
pool), (c) declared parents of (a) that are themselves in the enumeration.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from huggingface_hub import hf_hub_download
from huggingface_hub.utils import (
    EntryNotFoundError,
    GatedRepoError,
    RepositoryNotFoundError,
)
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hub_common import ABLIT_RE, API, ROOT, cache_path, retry  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "details.log", rotation="30 MB", level="DEBUG")

ABLIT = re.compile(ABLIT_RE)  # feature-definition regex (frozen)
SCAN_POOL_TARGET = 2000  # over-fetch: many rows are filtered out downstream

# tokenizer_config.json is deliberately NOT fetched: list_models(expand=['config'])
# already returns config.tokenizer_config including chat_template, and the real
# files run to tens of MB on Llama-family repos.
SMALL_FILES = ("README.md", "config.json")

# Harvest net, deliberately WIDER than ABLIT_RE. ABLIT_RE is the plan's frozen
# definition of the repo_id_contains_abliteration_string FEATURE and must not
# drift; these extra tool names only decide who gets looked at.
# (ABLIT_RE already carries the inline (?i); a second one mid-pattern is a syntax error)
HARVEST = re.compile(ABLIT_RE + r"|(heretic|lorablated|josiefied|amoral|unfiltered|unalign)")


def fetch_one(repo_id: str, sha: str | None) -> dict:
    """One repo -> {status, files, readme, config, tokenizer_config}."""
    p = cache_path("details", f"{repo_id}@{sha}")
    if p.exists():
        try:
            return json.loads(p.read_text())["v"]
        except (json.JSONDecodeError, KeyError):
            logger.warning(f"corrupt cache for {repo_id}")

    out: dict = {
        "repo_id": repo_id,
        "sha": sha,
        "status": "ok",
        "files": None,
        "readme": None,
        "config": None,
        "tokenizer_config": None,
    }
    rev = sha or "main"
    try:
        info = retry(lambda: API.model_info(repo_id, revision=rev, files_metadata=True))
        out["sha"] = info.sha or sha
        out["files"] = [
            {"rfilename": s.rfilename, "size_bytes": s.size} for s in (info.siblings or [])
        ]
    except GatedRepoError:
        out["status"] = "gated"
        p.write_text(json.dumps({"k": repo_id, "v": out}))
        return out
    except RepositoryNotFoundError:
        out["status"] = "not_found"
        p.write_text(json.dumps({"k": repo_id, "v": out}))
        return out
    except Exception as e:
        out["status"] = "error"
        out["error"] = f"{type(e).__name__}: {e}"[:300]
        p.write_text(json.dumps({"k": repo_id, "v": out}))
        return out

    present = {f["rfilename"] for f in (out["files"] or [])}
    for fn in SMALL_FILES:
        if fn not in present:
            continue
        try:
            path = retry(
                lambda fn=fn: hf_hub_download(
                    repo_id, fn, revision=out["sha"], cache_dir=str(ROOT / "cache" / "hf")
                )
            )
            raw = Path(path).read_bytes()
        except (EntryNotFoundError, GatedRepoError, RepositoryNotFoundError):
            continue
        except Exception as e:
            logger.debug(f"{repo_id}:{fn} {type(e).__name__}: {e}")
            continue
        if fn == "README.md":
            text = raw.decode("utf-8", errors="replace")
            out["readme"] = text
            out["readme_sha256"] = hashlib.sha256(raw).hexdigest()
            out["readme_bytes"] = len(raw)
        else:
            try:
                out[fn.replace(".json", "")] = json.loads(raw.decode("utf-8", errors="replace"))
            except json.JSONDecodeError:
                pass

    p.write_text(json.dumps({"k": repo_id, "v": out}))
    return out


def select_targets(models: list[dict]) -> list[dict]:
    sub42 = [m for m in models if (m["st_total"] or 0) and m["st_total"] <= 4.2e9]
    by_id = {m["repo_id"]: m for m in models}

    targets: dict[str, dict] = {}
    for m in sub42:
        if HARVEST.search(m["repo_id"]):
            targets[m["repo_id"]] = m
    logger.info(f"block-1 id-matched candidates: {len(targets)}")

    # declared parents that we already enumerated (needed for the H3 pairs)
    for m in list(targets.values()):
        bm = m.get("card_base_model")
        for parent in [bm] if isinstance(bm, str) else (bm or []):
            if isinstance(parent, str) and parent in by_id and parent not in targets:
                targets[parent] = by_id[parent]
    logger.info(f"after adding enumerated parents: {len(targets)}")

    # block-3 scan pool: most-downloaded sub-4.0B, excluding quant/GGUF re-uploads
    pool = [
        m
        for m in sub42
        if m["st_total"] <= 4.0e9
        and not re.search(r"(?i)(gguf|awq|gptq|-mlx|mlx-|4bit|8bit|bnb|exl2|onnx)", m["repo_id"])
    ]
    pool.sort(key=lambda m: -(m["downloads"] or 0))
    for m in pool[:SCAN_POOL_TARGET]:
        targets.setdefault(m["repo_id"], m)
    logger.info(f"total detail targets: {len(targets)}")
    return list(targets.values())


def main() -> None:
    models = json.loads((ROOT / "results" / "enumerated.json").read_text())["models"]
    targets = select_targets(models)

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=10) as pool:
        futs = {pool.submit(fetch_one, m["repo_id"], m["sha"]): m["repo_id"] for m in targets}
        for i, f in enumerate(as_completed(futs), 1):
            try:
                results.append(f.result())
            except Exception as e:
                logger.error(f"{futs[f]}: {e}")
            if i % 200 == 0:
                logger.info(f"{i}/{len(targets)} fetched")

    out = ROOT / "results" / "details.json"
    out.write_text(json.dumps(results))
    st = {}
    for r in results:
        st[r["status"]] = st.get(r["status"], 0) + 1
    logger.info(f"{len(results)} details -> {out} ({out.stat().st_size / 1e6:.1f} MB); status {st}")
    logger.info(f"with README: {sum(1 for r in results if r.get('readme'))}")


if __name__ == "__main__":
    main()
