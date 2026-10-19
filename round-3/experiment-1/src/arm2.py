#!/usr/bin/env python3
"""ARM 2 -- E_1 (parent-REQUIRING incumbent) head-to-head against W05.

E_1 is the published weight signal for detecting an abliteration edit, but it
needs the PARENT checkpoint.  W05 needs nothing but the candidate.  The question
is what that parent-free constraint costs, measured on EXACTLY the subset of
members where a parent resolves -- comparing the two on different panels would
be meaningless.

Pairs are grouped by parent so each snapshot is fetched once.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import torch
from loguru import logger

WS = Path(__file__).resolve().parent
sys.path.insert(0, str(WS))
RES = WS / "results"

import hubio  # noqa: E402
import panel as P  # noqa: E402
import wstats  # noqa: E402
from e1 import e1_pair  # noqa: E402
from method import DEV, N_RANDOM, SEED, jdump, jlines, load_model  # noqa: E402

_W05_CACHE: dict[str, dict] = {}


def w_of(repo: str, path: str) -> dict:
    if repo in _W05_CACHE:
        return _W05_CACHE[repo]
    m = load_model(path)
    r = wstats.w_stats_model(m, n_random=N_RANDOM, seed=SEED, device=DEV)
    del m
    hubio.gc_cuda()
    _W05_CACHE[repo] = {k: getattr(r, k) for k in P.WKEYS}
    return _W05_CACHE[repo]


def run(limit: int | None = None) -> dict:
    t0 = time.time()
    arch = P.archive()
    pairs = P.E1_PAIRS[:limit] if limit else P.E1_PAIRS
    by_parent: dict[str, list[tuple]] = {}
    for par, cand, kind in pairs:
        by_parent.setdefault(par, []).append((cand, kind))

    rows, skipped = [], []
    for par, kids in by_parent.items():
        prev = arch.get(par, {}).get("revision")
        try:
            prec = hubio.ensure(par, prev)
        except Exception as exc:  # noqa: BLE001
            for cand, kind in kids:
                skipped.append({"parent": par, "candidate": cand, "pair_type": kind,
                                "skip_reason": f"parent fetch failed: {str(exc)[:200]}"})
            continue
        try:
            wpar = w_of(par, prec["path"])
        except Exception as exc:  # noqa: BLE001
            logger.error(f"W stats for parent {par}: {exc}")
            wpar = {}
        for cand, kind in kids:
            crev = arch.get(cand, {}).get("revision")
            try:
                crec = hubio.ensure(cand, crev)
            except Exception as exc:  # noqa: BLE001
                skipped.append({"parent": par, "candidate": cand, "pair_type": kind,
                                "skip_reason": f"candidate fetch failed: {str(exc)[:200]}"})
                continue
            res = e1_pair(prec["path"], crec["path"], device=DEV)
            try:
                wc = w_of(cand, crec["path"])
            except Exception as exc:  # noqa: BLE001
                logger.error(f"W stats for {cand}: {exc}")
                wc = {}
            row = {"parent": par, "candidate": cand, "pair_type": kind,
                   "is_abliteration_edit": kind == "positive",
                   "parent_revision": prec["revision"], "candidate_revision": crec["revision"],
                   "lineage_id": arch.get(cand, {}).get("lineage_id", par),
                   "family": arch.get(cand, {}).get("family"),
                   "candidate_class": arch.get(cand, {}).get("member_class"),
                   "params": arch.get(cand, {}).get("param_count"),
                   "W05_candidate": wc.get("W05"), "W01_candidate": wc.get("W01"),
                   "W02_candidate": wc.get("W02"), "W05_parent": wpar.get("W05"),
                   **res}
            rows.append(row)
            logger.info(f"E1 {par} -> {cand} [{kind}]: E1={res.get('E1')} "
                        f"W05={wc.get('W05')} ok={res.get('ok')}")
            jlines(rows, RES / "arm2_pairs.jsonl")
            hubio.release(cand, crev)
        hubio.release(par, prev)

    # synthetic edits vs their own parent -- always resolvable, from arm1
    synth = []
    sp = RES / "arm1_synth.jsonl"
    if sp.exists():
        for line in sp.read_text().splitlines():
            r = __import__("json").loads(line)
            if r.get("E1_vs_parent") is not None:
                synth.append({"parent": r["host"], "candidate": r["variant_id"],
                              "pair_type": "positive_synthetic",
                              "is_abliteration_edit": True, "recipe": r["recipe"],
                              "lineage_id": r.get("lineage_id"), "family": r.get("family"),
                              "E1": r["E1_vs_parent"], "W05_candidate": r["W05"],
                              "W01_candidate": r["W01"], "W02_candidate": r["W02"],
                              "degenerate": r.get("degenerate"),
                              "ok": True, **{k: v for k, v in r.get("E1_detail", {}).items()
                                             if k in ("n_matrices", "band", "band_layers")}})
    out = {"n_pairs_attempted": len(pairs), "n_pairs_ok": sum(1 for r in rows if r.get("ok")),
           "n_pairs_skipped": len(skipped), "skipped": skipped,
           "n_synthetic_pairs": len(synth), "seconds": round(time.time() - t0, 1),
           "band": [0.25, 0.75],
           "band_note": "our reading of 'mid-stack'; recorded because the source is "
                        "not numerically specific"}
    jlines(rows + synth, RES / "arm2_all.jsonl")
    jdump(out, RES / "arm2.json")
    logger.info(f"ARM2: {out['n_pairs_ok']}/{len(pairs)} real pairs + "
                f"{len(synth)} synthetic pairs")
    return out


if __name__ == "__main__":
    run()
