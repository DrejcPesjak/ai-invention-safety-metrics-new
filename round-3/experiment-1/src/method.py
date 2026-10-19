#!/usr/bin/env python3
"""How far does the weight scar reach?  --  driver.

Stages
  smoke    synthetic-tensor unit tests for w_stats / E_1 / the edit machinery
  gate     FRESH reimplementation of W01-W05 vs the archived iteration-2 values
  control  the two archived positive controls, re-run with the fresh code
  arm1     recipe scope: synthetic recipe variants + real new-toolchain checkpoints
  arm2     E_1 (parent-required incumbent) head-to-head against W05
  arm3     depth invariance of the activation metrics across the AUROC plateau
  assemble collect everything into method_out.json

Usage:  uv run method.py --stage gate --limit 3
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
from loguru import logger

WS = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(WS / "hfcache"))
sys.path.insert(0, str(WS))

(WS / "logs").mkdir(exist_ok=True)
(WS / "results").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(WS / "logs" / "run.log"), rotation="30 MB", level="DEBUG")

import hubio  # noqa: E402
import panel as P  # noqa: E402
import wstats  # noqa: E402
from e1 import e1_from_state_dicts, e1_pair  # noqa: E402
from edits import (WriteMatrixStore, measure_edited, rank_k_subspace,  # noqa: E402
                   refusal_direction)

RES = WS / "results"
SEED = 0
N_RANDOM = 256
DEV = "cuda" if torch.cuda.is_available() else "cpu"
# The archive was measured from bf16-loaded weights; the gate must match that to
# be a reproduction.  A float32 load is measured alongside on the gate members so
# the dtype contribution to any delta is quantified rather than assumed.
ARCHIVE_DTYPE = torch.bfloat16


def jdump(obj, path: Path) -> None:
    path.write_text(json.dumps(obj, indent=2, default=_default))


def _default(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, torch.Tensor):
        return o.detach().cpu().tolist()
    return str(o)


def jlines(rows: list[dict], path: Path) -> None:
    with open(path, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, default=_default) + "\n")


def load_model(path: str, dtype=ARCHIVE_DTYPE):
    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(path, torch_dtype=dtype,
                                             attn_implementation="eager",
                                             trust_remote_code=False)
    return m.eval().requires_grad_(False)


# ===========================================================================
# STAGE smoke
# ===========================================================================
def stage_smoke() -> dict:
    import e1 as e1mod
    import edits as edmod
    logger.info("smoke: w_stats synthetic-tensor unit tests")
    w = wstats.selftest()
    logger.info(f"smoke: blind spot reproduced, synthetic f*={w['synthetic_f_star']}")
    e = e1mod.selftest()
    ed = edmod.selftest()
    out = {"wstats": w, "e1": e, "edits": ed, "all_pass": True}
    jdump(out, RES / "smoke.json")
    return out


# ===========================================================================
# STAGE gate
# ===========================================================================
def _measure_repo(repo: str, revision: str | None, *, dtypes=(ARCHIVE_DTYPE,),
                  keep: bool = False) -> dict:
    rec = hubio.ensure(repo, revision)
    out = {"repo": repo, "revision": rec["revision"],
           "revision_was_pinned": rec["revision_was_pinned"],
           "resolved_sha": rec["resolved_sha"], "gb": rec["gb"],
           "weights_sha256_index": wstats.sha256_index(rec["path"]), "by_dtype": {}}
    for dt in dtypes:
        t0 = time.time()
        m = load_model(rec["path"], dtype=dt)
        r = wstats.w_stats_model(m, n_random=N_RANDOM, seed=SEED, device=DEV)
        name = str(dt).replace("torch.", "")
        out["by_dtype"][name] = {**r.as_dict(), "load_and_measure_s": round(time.time() - t0, 1)}
        out["d"], out["n_layers"], out["n_matrices"] = r.d, r.n_layers, r.n_matrices
        del m, r
        hubio.gc_cuda()
    if not keep:
        hubio.release(repo, revision)
    return out


def stage_gate(limit: int | None = None, members: list[str] | None = None) -> dict:
    arch = P.archive()
    mem = members or (P.GATE_TIER0 if limit == 3 else P.GATE_MEMBERS)
    if limit and not members:
        mem = mem[:limit] if limit != 3 else mem
    rows, dropped = [], []
    for repo in mem:
        a = arch.get(repo)
        if a is None:
            dropped.append({"repo": repo, "reason": "absent from the archive"})
            continue
        try:
            m = _measure_repo(repo, a["revision"], dtypes=(ARCHIVE_DTYPE, torch.float32))
        except Exception as exc:  # noqa: BLE001
            logger.error(f"gate {repo}: {exc}")
            dropped.append({"repo": repo, "reason": str(exc)[:300]})
            continue
        new = m["by_dtype"]["bfloat16"]
        deltas = {k: (new[k] - a["W"][k]) for k in P.WKEYS if k in a["W"]}
        d32 = {k: (m["by_dtype"]["float32"][k] - a["W"][k]) for k in P.WKEYS if k in a["W"]}
        row = {**m, "member_class": a["member_class"], "lineage_id": a["lineage_id"],
               "family": a["family"], "param_count": a["param_count"],
               "archived": a["W"], "recomputed": {k: new[k] for k in P.WKEYS},
               "recomputed_float32": {k: m["by_dtype"]["float32"][k] for k in P.WKEYS},
               "delta": deltas, "delta_float32_load": d32,
               "archived_revision": a["revision"]}
        rows.append(row)
        logger.info(f"GATE {repo}: dW05={deltas.get('W05', float('nan')):+.5f} "
                    f"dW01={deltas.get('W01', float('nan')):+.5f} "
                    f"dW03={deltas.get('W03', float('nan')):+.5f}")
        jlines(rows, RES / "gate.jsonl")

    verdict = _gate_verdict(rows)
    out = {"members_requested": mem, "n_measured": len(rows), "dropped": dropped,
           "rows": rows, **verdict}
    jdump(out, RES / "gate.json")
    logger.info(f"GATE VERDICT: {verdict['gate_pass']} -- {verdict['gate_reason']}")
    return out


def _gate_verdict(rows: list[dict]) -> dict:
    """PASS iff max|dW05|<=0.02, max|dW01|<=0.05 and the W05 ordering is unchanged."""
    if not rows:
        return {"gate_pass": "NO_DATA", "gate_reason": "no members measured",
                "max_abs_dW05": None, "max_abs_dW01": None}
    d05 = [abs(r["delta"]["W05"]) for r in rows if "W05" in r["delta"]]
    d01 = [abs(r["delta"]["W01"]) for r in rows if "W01" in r["delta"]]
    d03 = [abs(r["delta"].get("W03", 0.0)) for r in rows]
    abl = [r for r in rows if r["member_class"] == "abliterated"]
    neg = [r for r in rows if r["member_class"] != "abliterated"]
    order_ok = None
    if abl and neg:
        order_ok = (max(r["recomputed"]["W05"] for r in abl)
                    < min(r["recomputed"]["W05"] for r in neg))
    # rank correlation of the recomputed vs archived W05 over the gate members
    from scipy.stats import spearmanr
    rho = float(spearmanr([r["archived"]["W05"] for r in rows],
                          [r["recomputed"]["W05"] for r in rows]).statistic) \
        if len(rows) > 2 else float("nan")
    ok = (max(d05) <= 0.02) and (max(d01) <= 0.05) and (order_ok is not False)
    reasons = []
    if max(d05) > 0.02:
        reasons.append(f"max|dW05|={max(d05):.4f}>0.02")
    if max(d01) > 0.05:
        reasons.append(f"max|dW01|={max(d01):.4f}>0.05")
    if order_ok is False:
        reasons.append("W05 abliterated/non-abliterated ordering changed")
    return {"gate_pass": "PASS" if ok else "FAIL",
            "gate_reason": "; ".join(reasons) or "all tolerances met",
            "max_abs_dW05": max(d05), "max_abs_dW01": max(d01), "max_abs_dW03": max(d03),
            "w05_ordering_preserved": order_ok, "spearman_archived_vs_recomputed_W05": rho,
            "tolerance": {"W05": 0.02, "W01": 0.05},
            "n_abliterated": len(abl), "n_non_abliterated": len(neg)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True,
                    choices=["smoke", "gate", "control", "arm1", "arm1c", "arm2", "arm3",
                             "assemble"])
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--members", type=str, default=None)
    ap.add_argument("--tier2", action="store_true")
    args = ap.parse_args()
    mem = args.members.split(",") if args.members else None
    t0 = time.time()
    if args.stage == "smoke":
        stage_smoke()
    elif args.stage == "gate":
        stage_gate(args.limit, mem)
    else:
        import stages
        stages.dispatch(args)
    logger.info(f"stage {args.stage} done in {time.time() - t0:.1f}s "
                f"(free disk {hubio.free_gb():.1f} GB)")


if __name__ == "__main__":
    main()
