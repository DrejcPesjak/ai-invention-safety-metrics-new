#!/usr/bin/env python3
"""Pass 2 of the HF census.

The `?search=&full=true` list endpoint does NOT carry `safetensors`, so pass 1
reported 0 param counts for every hit. Here we take pass 1's repo-id lists,
keep only ids whose NAME suggests a small model (documented, reported filter --
never used as evidence of size), and resolve each one's true param count from
`safetensors.total` on the per-model endpoint.
"""

import json
import re
import time
from pathlib import Path

import requests

WS = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/gen_art/gen_art_research_1")
CEILING = 4.2e9
HDRS = {"User-Agent": "aii-research/1.0"}

# Documented name-based prefilter. Reported in the dossier as a coverage limit:
# a sub-4.2B checkpoint whose repo name carries NO size token is not resolved.
SMALL = re.compile(
    r"(?<![0-9.])(0\.5|0\.6|0\.27|0\.35|1|1\.5|1\.7|1\.8|2|2\.7|3|3\.8|4)\s*b\b"
    r"|(?:^|[-_/])(e2b|e4b|270m|350m|360m|500m|600m|small|mini|tiny)",
    re.I,
)


def get(url, params=None, tries=3):
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=HDRS, timeout=45)
            if r.status_code == 200:
                return r.json(), 200
            if r.status_code in (401, 403, 404):
                return None, r.status_code
            time.sleep(1.5 * (i + 1))
        except Exception:  # noqa: BLE001
            time.sleep(1.5 * (i + 1))
    return None, -1


def main():
    pass1 = json.loads((WS / "hf_census.json").read_text())

    # repo_id -> set of terms it was found under
    cand: dict[str, set] = {}
    total_hits = {}
    for term, block in pass1["search_census"].items():
        ids = block["all_repo_ids"]
        total_hits[term] = len(ids)
        for rid in ids:
            if SMALL.search(rid):
                cand.setdefault(rid, set()).add(term)

    print(f"{len(cand)} name-prefiltered candidates from {sum(total_hits.values())} hits")

    resolved = []
    for n, (rid, terms) in enumerate(sorted(cand.items()), 1):
        data, code = get(f"https://huggingface.co/api/models/{rid}")
        if data is None:
            resolved.append({"repo_id": rid, "terms": sorted(terms), "http": code,
                             "params": None, "status": "UNREACHABLE"})
            print(f"  [{n}/{len(cand)}] {rid}: HTTP {code}")
            time.sleep(0.4)
            continue
        st = data.get("safetensors") or {}
        tot = st.get("total")
        resolved.append({
            "repo_id": rid,
            "terms": sorted(terms),
            "http": 200,
            "params": tot,
            "createdAt": data.get("createdAt"),
            "sha": data.get("sha"),
            "gated": data.get("gated"),
            "downloads": data.get("downloads"),
            "likes": data.get("likes"),
            "arch": (data.get("config") or {}).get("architectures"),
            "base_model_tags": [t for t in (data.get("tags") or []) if t.startswith("base_model")][:4],
        })
        if n % 25 == 0:
            print(f"  [{n}/{len(cand)}] ...")
        time.sleep(0.35)

    sub = [r for r in resolved if r.get("params") and r["params"] <= CEILING]
    by_term: dict[str, list] = {}
    for r in sub:
        for t in r["terms"]:
            by_term.setdefault(t, []).append(r["repo_id"])

    out = {
        "prefilter_regex": SMALL.pattern,
        "n_hits_per_term": total_hits,
        "n_candidates_after_name_prefilter": len(cand),
        "n_resolved_with_param_count": sum(1 for r in resolved if r.get("params")),
        "n_sub_4p2B": len(sub),
        "sub_4p2B_by_term": by_term,
        "sub_4p2B_rows": sorted(sub, key=lambda r: -(r.get("downloads") or 0)),
        "unreachable": [r for r in resolved if r.get("status") == "UNREACHABLE"],
        "all_resolved": resolved,
    }
    (WS / "hf_census_pass2.json").write_text(json.dumps(out, indent=1))
    print(f"WROTE hf_census_pass2.json -- {len(sub)} sub-4.2B of {len(cand)} candidates")
    for t in sorted(by_term):
        print(f"  {t}: {len(by_term[t])}")


if __name__ == "__main__":
    main()
