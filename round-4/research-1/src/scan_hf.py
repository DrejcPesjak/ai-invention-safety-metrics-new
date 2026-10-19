#!/usr/bin/env python3
"""Census HuggingFace for sub-4.2B abliteration checkpoints by recipe term.

Uses the public HF API. Records safetensors.total (NEVER trusts the repo name),
createdAt, sha, gated status. Writes hf_census.json into the workspace.
"""

import json
import time
from pathlib import Path

import requests

WS = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_research_1")
CEILING = 4.2e9
HDRS = {"User-Agent": "aii-research/1.0"}

SEARCH_TERMS = [
    "orthogonal-reflection-bounded",
    "ORBA",
    "MPOA",
    "gabliterated",
    "gabliteration",
    "OBLITERATED",
    "heretic",
    "apostate",
    "abliterix",
    "AEON",
    "HauhauCS",
    "reaper",
    "abliterated",
]

DIRECT_REPOS = [
    "YanLabs/Qwen3-4B-Instruct-2507-MPOA",
    "heretic-org/Qwen3-4B-Instruct-2507-heretic",
    "p-e-w/Qwen3-4B-Instruct-2507-heretic",
    "p-e-w/Qwen3-4B-Instruct-2507-heretic-v4",
    "0xA50C1A1/Qwen3-4B-Instruct-2507-SOM-MPOA",
    "OBLITERATUS/Qwen3-4B-OBLITERATED",
    "MagicalAlchemist/Qwen3-1.7B-Magic_decensored",
    "prithivMLmods/VibeThinker-3B-heretic_decensored",
    "mlabonne/Qwen3-0.6B-abliterated",
    "DreamFast/Qwen3-4B-2507-Instruct-Uncensored-HauhauCS-Aggressive-Safetensor-Benchmark",
    "DreamFast/Qwen3-VL-4b-Heretic",
    "DreamFast/Gemma4-e2b-abliterlitics",
    "huihui-ai/Huihui-Qwen3-4B-Instruct-2507-abliterated",
    "HauhauCS/Qwen3-4B-2507-Instruct-Uncensored-HauhauCS-Aggressive",
    "coder3101/Qwen3.5-4B-heretic",
    "grimjim/gemma-3-12b-it-orthogonal-reflection-bounded-ablation-v4-12B",
]


def get(url, params=None, tries=3):
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=HDRS, timeout=45)
            if r.status_code == 200:
                return r.json(), 200
            if r.status_code in (401, 403, 404):
                return None, r.status_code
            time.sleep(2 * (i + 1))
        except Exception as exc:  # noqa: BLE001
            last = str(exc)
            time.sleep(2 * (i + 1))
    return None, -1


def params_of(info):
    st = info.get("safetensors") or {}
    tot = st.get("total")
    if tot is None:
        params = st.get("parameters") or {}
        if isinstance(params, dict):
            tot = sum(v for v in params.values() if isinstance(v, (int, float)))
    return tot


def row(info, source):
    return {
        "repo_id": info.get("id") or info.get("modelId"),
        "uploader": (info.get("id") or "/").split("/")[0],
        "sha": info.get("sha"),
        "params": params_of(info),
        "createdAt": info.get("createdAt"),
        "lastModified": info.get("lastModified"),
        "gated": info.get("gated"),
        "private": info.get("private"),
        "downloads": info.get("downloads"),
        "likes": info.get("likes"),
        "tags": [t for t in (info.get("tags") or []) if not t.startswith("region")][:14],
        "source": source,
    }


def main():
    out = {"search_census": {}, "direct": [], "errors": []}

    for term in SEARCH_TERMS:
        data, code = get(
            "https://huggingface.co/api/models",
            params={"search": term, "limit": 100, "full": "true"},
        )
        if data is None:
            out["errors"].append({"term": term, "http": code})
            print(f"[search] {term}: HTTP {code}")
            continue
        rows = [row(m, f"search:{term}") for m in data]
        sub = [r for r in rows if r["params"] and r["params"] <= CEILING]
        out["search_census"][term] = {
            "n_hits": len(rows),
            "n_with_param_count": sum(1 for r in rows if r["params"]),
            "n_sub_4p2B": len(sub),
            "sub_4p2B": sorted(sub, key=lambda r: -(r["downloads"] or 0)),
            "all_repo_ids": [r["repo_id"] for r in rows],
        }
        print(f"[search] {term}: {len(rows)} hits, {len(sub)} sub-4.2B")
        time.sleep(1.0)

    for rid in DIRECT_REPOS:
        data, code = get(f"https://huggingface.co/api/models/{rid}")
        if data is None:
            out["direct"].append({"repo_id": rid, "http": code, "status": "UNREACHABLE"})
            print(f"[direct] {rid}: HTTP {code}")
            continue
        r = row(data, "direct")
        r["http"] = 200
        r["config_arch"] = (data.get("config") or {}).get("architectures")
        r["base_model_tags"] = [t for t in (data.get("tags") or []) if t.startswith("base_model")]
        out["direct"].append(r)
        print(f"[direct] {rid}: params={r['params']} created={r['createdAt']} gated={r['gated']}")
        time.sleep(0.8)

    (WS / "hf_census.json").write_text(json.dumps(out, indent=1))
    print("WROTE hf_census.json")


if __name__ == "__main__":
    main()
