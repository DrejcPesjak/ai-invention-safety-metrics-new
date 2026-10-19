#!/usr/bin/env python3
"""STAGE 1 -- text recovery by deterministic regeneration (GPU).

The archived iteration-4 experiment (art_VLI4IOs9Xy9P) stored, per behavioural cell,
only binary per-item labels keyed by prompt uid plus ONE 400-character sample; and it
stored the judge's decisions in results/judge_cache.json as
sha256(JUDGE_MODEL || RUBRIC_ID || prompt || response[:1500]) -> label, i.e. hashes.
The generation TEXT was never persisted.

It is nevertheless recoverable, and the recovery is SELF-VERIFYING.  Generation is
greedy argmax at temperature 0 with a fixed batch order (lib_model.Runner.generate),
and the edited checkpoints rebuild bit-identically from archive/root_recipe.json plus
results/roots.json.  So a regenerated (prompt, response) pair that is byte-identical to
the archived one HITS the archived cache key.  Cache-hit rate is therefore a PROOF of
text identity, not a convenience: without it every downstream agreement number would
silently confound scorer disagreement with regeneration drift.

This script writes results/recovered.jsonl -- one row per (stage_id, uid) carrying the
prompt, the regenerated response, the cache key, whether it hit, the archived THREE-CLASS
label recovered from the hit, the archived BINARY label from per_item_harmful, and the
Arditi-style substring screen recomputed on the same text.

Tiering is mandatory: cells are attempted in a pre-registered priority order under a
wall-clock budget, and the tier reached is reported.
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
from loguru import logger

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
LOGS = HERE / "logs"
VENDOR = HERE / "vendor"
for _p in (RESULTS, LOGS):
    _p.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(VENDOR))

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "regen.log", rotation="30 MB", level="DEBUG")

ARCH3 = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/"
             "gen_art/gen_art_experiment_3")
ARCH1 = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_4/"
             "gen_art/gen_art_experiment_1")

import lib_behave as B          # noqa: E402
import lib_edit as E            # noqa: E402
from lib_data import is_refusal  # noqa: E402
from lib_model import Runner    # noqa: E402
from lib_prompts import Prompts  # noqa: E402

PARENT_A = "Qwen/Qwen3-1.7B"
HOST_C = "meta-llama/Llama-3.2-1B-Instruct"
MAX_NEW = 64
BATCH = 16
OUT = RESULTS / "recovered.jsonl"
STATE = RESULTS / "regen_state.json"

# ---------------------------------------------------------------------------
# pre-registered cell priority.  TIER_A is mandatory; B then C are attempted in
# order under the wall-clock budget and the tier reached is reported.
# ---------------------------------------------------------------------------
TIER_A_QWEN = ["A_parent", "A_root", "B_parent", "B_root", "B_root_n120", "A_root_n120"]
TIER_B_QWEN = [
    # flag-death cells (merge w=0.10, add-back eps=0.10, quant nf4) PLUS the immediately
    # adjacent intensity on each side, so an ORDERING can be re-tested, not just a point.
    "A_merge_w0.10", "A_merge_w0.25",
    "A_addback_eps0.05", "A_addback_eps0.10", "A_addback_eps0.25",
    "A_quant_int8", "A_quant_nf4", "A_quant_int4",
    "B_merge_w0.10", "B_merge_w0.25",
    "B_addback_eps0.05", "B_addback_eps0.10", "B_addback_eps0.25",
    "B_quant_int8", "B_quant_nf4", "B_quant_int4",
    "A_merge_w0.10_n120", "A_addback_eps0.10_n120", "A_quant_int4_n120",
    "B_merge_w0.10_n120", "B_addback_eps0.05_n120", "B_quant_int4_n120",
]
TIER_D_QWEN = ["A_merge_w0.50", "A_merge_w0.75", "A_addback_eps0.50", "A_addback_eps1.00",
               "A_merge_w0.50_n120", "A_addback_eps0.50_n120",
               "B_merge_w0.50", "B_merge_w0.75", "B_addback_eps0.50", "B_addback_eps1.00",
               "B_merge_w0.50_n120", "B_addback_eps0.50_n120"]
TIER_A_LLAMA = ["C_parent", "C_root", "C_root_auroc_argmax", "C_root_n120"]
TIER_B_LLAMA = ["C_merge_w0.10", "C_merge_w0.25",
                "C_addback_eps0.05", "C_addback_eps0.10", "C_addback_eps0.25",
                "C_quant_int8", "C_quant_nf4", "C_quant_int4",
                "C_merge_w0.10_n120", "C_addback_eps0.10_n120", "C_quant_int4_n120"]
TIER_D_LLAMA = ["C_merge_w0.50", "C_merge_w0.75", "C_addback_eps0.50", "C_addback_eps1.00",
                "C_merge_w0.50_n120", "C_addback_eps0.50_n120"]

# Tier C of the plan: the Arm-B effectiveness set from art_dp7WBo6hhVBX.  The 6 kernels
# named in the effectiveness-vs-detectability claim come first so a reduced run still
# answers it.
TIER_C_KERNELS = ["parent_unedited", "orba_householder_lam1.0", "heretic_percomponent",
                  "rank_k4", "band_mid50", "gaussian_sinf", "uniform_w0.85",
                  "uniform_w1.0", "uniform_w0.7", "uniform_w0.5", "gaussian_s2",
                  "gaussian_s8", "gaussian_s32", "mpoa_norm_preserving"]


def read_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def append_jsonl(p: Path, rows: list[dict]) -> None:
    with p.open("a") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")


def free_mem() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


# ==========================================================================
# cache-key re-implementation, asserted byte-for-byte against lib_behave
# ==========================================================================
def cache_key(prompt: str, response: str) -> str:
    """Independent re-implementation; unit-tested against lib_behave.cache_key."""
    import hashlib
    h = hashlib.sha256()
    h.update(B.JUDGE_MODEL.encode())
    h.update(b"\x00")
    h.update(B.RUBRIC_ID.encode())
    h.update(b"\x00")
    h.update(prompt.encode("utf-8", "replace"))
    h.update(b"\x00")
    h.update(response[:1500].encode("utf-8", "replace"))
    return h.hexdigest()


def load_archive_cache() -> dict[str, str]:
    return json.loads((ARCH3 / "results" / "judge_cache.json").read_text())


# ==========================================================================
# cell reconstruction
# ==========================================================================
def parse_stage(sid: str) -> dict:
    base = sid[:-5] if sid.endswith("_n120") else sid
    n120 = sid.endswith("_n120")
    root = base.split("_")[0]
    rest = base[len(root) + 1:]
    if rest == "root":
        fam, inten = "root", 0.0
    elif rest == "parent":
        fam, inten = "reference", -1.0
    elif rest == "root_auroc_argmax":
        fam, inten = "root_sensitivity", None
    elif rest.startswith("merge_w"):
        fam, inten = "merge", float(rest[len("merge_w"):])
    elif rest.startswith("addback_eps"):
        fam, inten = "addback", float(rest[len("addback_eps"):])
    elif rest.startswith("quant_"):
        fam, inten = "quant", rest[len("quant_"):]
    else:
        raise ValueError(f"unparseable stage_id {sid}")
    return {"stage_id": sid, "root": root, "family": fam, "intensity": inten,
            "n120": n120}


def build_sd(spec: dict, ctx: dict):
    """Rebuild a cell's state_dict exactly as method.py did."""
    fam = spec["family"]
    if fam == "root":
        return ctx["root_sd"], False
    if fam == "reference":
        return ctx["parent_sd"], False
    if fam == "root_sensitivity":
        return ctx["root_sd_auroc"], False
    if fam == "merge":
        return E.merge_sd(ctx["root_sd"], ctx["parent_sd"], float(spec["intensity"])), True
    if fam == "quant":
        sd, _m = E.quant_sd(ctx["root_sd"], str(spec["intensity"]))
        return sd, True
    if fam == "addback":
        return E.addback_sd(ctx["root_sd"], ctx["parent_sd"], ctx["keys"], ctx["r"],
                            float(spec["intensity"])), True
    raise ValueError(fam)


# ==========================================================================
# one regenerated cell
# ==========================================================================
def regen_cell(rn, P: Prompts, spec: dict, ctx: dict, cache: dict[str, str],
               archived: dict[str, dict], tier: str) -> dict:
    sid = spec["stage_id"]
    t0 = time.time()
    sd, temp = build_sd(spec, ctx)
    E.load_sd(rn, sd)
    if temp:
        del sd
        free_mem()

    prompts = P.harmful120 if spec["n120"] else P.harmful40
    uids = P.harmful120_uids if spec["n120"] else P.harmful40_uids
    texts, _n, _f, _c = rn.generate(prompts, max_new_tokens=MAX_NEW, batch=BATCH)

    arow = archived.get(sid, {})
    per_item = arow.get("per_item_harmful", {}) or {}
    rows, n_hit = [], 0
    for p, u, t in zip(prompts, uids, texts):
        k = cache_key(p, t)
        lab = cache.get(k)
        hit = lab in B.VALID_LABELS
        n_hit += int(hit)
        rows.append({"stage_id": sid, "root": spec["root"], "family": spec["family"],
                     "intensity": spec["intensity"], "n120": spec["n120"], "tier": tier,
                     "uid": u, "prompt": p, "response": t, "cache_key": k,
                     "cache_hit": bool(hit),
                     "j1_label": lab if hit else None,
                     "archived_binary": per_item.get(u),
                     "screen_refusal": int(is_refusal(t)),
                     "host": arow.get("host")})
    hit_rate = n_hit / max(len(rows), 1)

    # identity check: the refusal rate recomputed from the ARCHIVED labels of the hits
    # must equal the archived rate exactly when the hit rate is 1.0.
    hits = [r for r in rows if r["cache_hit"]]
    rate_from_hits = (sum(1 for r in hits if r["j1_label"] == "REFUSAL") / len(hits)
                      if hits else float("nan"))
    arch_rate = arow.get("refusal_rate")
    exact = (bool(hit_rate == 1.0 and arch_rate is not None
                  and abs(rate_from_hits - arch_rate) < 1e-12))
    # a hit_rate of 1.0 with n_achieved < n_requested means the archive DROPPED
    # unparseable labels; those uids are absent from per_item_harmful but their text
    # still hits the cache only if the judge produced a valid label, so the honest
    # comparison restricts to uids the archive kept.
    kept = [r for r in hits if r["uid"] in per_item]
    rate_kept = (sum(1 for r in kept if r["j1_label"] == "REFUSAL") / len(kept)
                 if kept else float("nan"))
    exact_kept = (arch_rate is not None and len(kept) == arow.get("n_harmful", -1)
                  and abs(rate_kept - arch_rate) < 1e-12)
    binary_match = sum(1 for r in kept
                       if int(r["j1_label"] == "REFUSAL") == r["archived_binary"])

    # SELECTION CHECK.  Conditioning the sample frame on a cache hit is a selection, so
    # it must be measured, not assumed benign: compare the ARCHIVED binary label rate on
    # hit vs missed items.  A large gap would mean the recoverable items are the easy
    # ones and every agreement figure would be conditioned on that.
    hb = [r["archived_binary"] for r in rows
          if r["cache_hit"] and r["archived_binary"] is not None]
    mb = [r["archived_binary"] for r in rows
          if not r["cache_hit"] and r["archived_binary"] is not None]
    sel = {"n_hit_with_archived_label": len(hb), "n_miss_with_archived_label": len(mb),
           "archived_rate_on_hits": float(np.mean(hb)) if hb else None,
           "archived_rate_on_misses": float(np.mean(mb)) if mb else None,
           "selection_delta": (float(np.mean(hb) - np.mean(mb)) if hb and mb else None)}

    # Cross-device bf16 nondeterminism (the archive ran on an RTX 2000 Ada, this box is
    # an RTX 4090) means a fraction of 64-step greedy continuations diverge.  The items
    # that DO hit are proven byte-identical and are the analysis frame; the rest are
    # reported, never silently dropped.  probe_batch.json shows batch size is not the
    # cause (0.55-0.65 across batch 8/16/32/40), so batch=16 -- archive-identical -- is
    # kept and the residual is attributed to the device.
    status = ("CLEAN" if hit_rate >= 0.95 else
              "PARTIAL_RECOVERY" if hit_rate >= 0.30 else "REGENERATION_DRIFT")
    diffs = []
    if status != "CLEAN":
        samp = arow.get("sample_generation", "")
        for r in rows[:5]:
            if not r["cache_hit"]:
                diffs.append({"uid": r["uid"], "regenerated_head": r["response"][:400],
                              "archived_sample_generation_head": samp[:400],
                              "is_first_item": r["uid"] == uids[0]})

    meta = {"stage_id": sid, "tier": tier, "root": spec["root"],
            "family": spec["family"], "intensity": spec["intensity"],
            "n_items": len(rows), "n_cache_hit": n_hit, "hit_rate": hit_rate,
            "status": status,
            "archived_rate": arch_rate, "archived_n_achieved": arow.get("n_harmful"),
            "rate_from_cache_hits": rate_from_hits,
            "rate_from_hits_restricted_to_archived_uids": rate_kept,
            "n_hits_restricted": len(kept),
            "reproduces_archived_rate_exactly": bool(exact or exact_kept),
            "binary_label_agreement_with_archive": (binary_match / len(kept)
                                                    if kept else float("nan")),
            "n_empty_generations": int(sum(1 for r in rows if not r["response"].strip())),
            "screen_refusal_rate": float(np.mean([r["screen_refusal"] for r in rows])),
            "archived_screen_rate": arow.get("regex_harmful_refusal_rate"),
            "selection_check": sel,
            "drift_examples": diffs, "seconds": time.time() - t0}
    append_jsonl(OUT, rows)
    logger.info(f"  [{sid}] n={len(rows)} hit={n_hit} ({hit_rate:.3f}) {status} "
                f"rate_hits={rate_from_hits:.3f} archived={arch_rate} "
                f"({meta['seconds']:.0f}s)")
    free_mem()
    return meta


# ==========================================================================
# host contexts
# ==========================================================================
def qwen_ctx(rn) -> dict:
    recipe = json.loads((ARCH3 / "archive" / "root_recipe.json").read_text())
    roots = json.loads((ARCH3 / "results" / "roots.json").read_text())
    parent_sd = E.snapshot_sd(rn)
    key_rows = E.write_matrix_keys(rn)
    keys = [k["key"] for k in key_rows]
    assert keys == recipe["keys"], "write-matrix keys differ from the archived recipe"
    r = torch.tensor(recipe["r"], dtype=torch.float32)
    r = r / r.norm()
    root_A = E.ablate_sd(parent_sd, keys, r, emb_key=None)
    same, tot = E.n_tensors_identical(root_A, parent_sd)
    assert tot - same == 56, f"expected 56 modified tensors, got {tot - same}"
    kern = np.asarray(roots["B"]["kernel"], dtype=float)
    root_B = E.ablate_sd_kernel(parent_sd, key_rows, r, kern)
    return {"parent_sd": parent_sd, "keys": keys, "key_rows": key_rows, "r": r,
            "roots": {"A": root_A, "B": root_B},
            "n_tensors_modified_A": tot - same,
            "kernel_sum": float(kern.sum())}


def llama_ctx(rn, P: Prompts) -> dict:
    """Root C: diff-in-means direction, archive-identical fit/hold hashing.

    The archived run swept all 17 layers; the selected layers are recorded
    (l_star_behavioural = 14, l_star_auroc_argmax = 8), so only those two directions
    need rebuilding -- the diff-in-means itself is deterministic given the same halves.
    """
    import hashlib
    roots = json.loads((ARCH3 / "results" / "roots.json").read_text())
    dinfo = roots["C"]["direction"]
    parent_sd = E.snapshot_sd(rn)
    key_rows = E.write_matrix_keys(rn)
    keys = [k["key"] for k in key_rows]

    def half(t: str) -> int:
        return int(hashlib.sha256(t.encode()).hexdigest(), 16) % 2

    hA = [t for t in P.lc_harmful if half(t) == 0]
    bA = [t for t in P.lc_benign if half(t) == 0]
    HA, _ = rn.last_token_states(hA, batch=8)
    BA, _ = rn.last_token_states(bA, batch=8)
    dirs = {}
    for lab, l in (("beh", int(dinfo["l_star_behavioural"])),
                   ("auroc", int(dinfo["l_star_auroc_argmax"]))):
        mu = HA[:, l].mean(0) - BA[:, l].mean(0)
        dirs[lab] = mu / (mu.norm() + 1e-12)
    del HA, BA
    free_mem()
    root_C = E.ablate_sd(parent_sd, keys, dirs["beh"], emb_key=None)
    root_C_auroc = E.ablate_sd(parent_sd, keys, dirs["auroc"], emb_key=None)
    return {"parent_sd": parent_sd, "keys": keys, "key_rows": key_rows,
            "r": dirs["beh"], "root_sd_auroc": root_C_auroc,
            "roots": {"C": root_C},
            "n_fit": len(hA) + len(bA),
            "l_star_behavioural": int(dinfo["l_star_behavioural"]),
            "l_star_auroc_argmax": int(dinfo["l_star_auroc_argmax"])}


# ==========================================================================
# main
# ==========================================================================
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qwen-budget-min", type=float, default=32.0)
    ap.add_argument("--llama-budget-min", type=float, default=22.0)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()

    t_start = time.time()
    P = Prompts()
    cache = load_archive_cache()
    logger.info(f"archived judge cache: {len(cache)} entries")

    # --- unit test: our cache_key must equal lib_behave's, byte for byte ----
    probe = {"n_cache_entries": len(cache), "checks": []}
    tv = [("hello", "world"), ("", ""), ("éè", "x" * 2000)]
    ok = all(cache_key(a, b) == B.cache_key(a, b) for a, b in tv)
    probe["checks"].append({"check": "cache_key == lib_behave.cache_key on 3 vectors",
                            "pass": bool(ok)})
    assert ok, "cache_key re-implementation diverges from lib_behave"
    assert B.JUDGE_SYSTEM.startswith("You are evaluating whether an AI assistant")
    probe["judge_system_sha256"] = __import__("hashlib").sha256(
        B.JUDGE_SYSTEM.encode()).hexdigest()
    probe["judge_model"] = B.JUDGE_MODEL
    probe["rubric_id"] = B.RUBRIC_ID
    (RESULTS / "cache_probe.json").write_text(json.dumps(probe, indent=2))

    archived = {r["stage_id"]: r for r in read_jsonl(ARCH3 / "results" / "crossing_table.jsonl")}
    done = {r["stage_id"] for r in read_jsonl(OUT)}
    metas = read_jsonl(RESULTS / "regen_meta.jsonl")
    done_meta = {m["stage_id"] for m in metas}

    tiers_reached = []

    def run_host(host_repo: str, ctx_fn, plan: list[tuple[str, list[str]]],
                 budget_min: float) -> None:
        pending = [(t, s) for t, sids in plan for s in sids if s not in done]
        if not pending:
            logger.info(f"{host_repo}: nothing to do")
            return
        logger.info(f"=== host {host_repo}: {len(pending)} cells, "
                    f"budget {budget_min:.0f} min ===")
        rn = Runner(host_repo, None)
        ctx = ctx_fn(rn)
        end = time.time() + budget_min * 60
        for tier, sid in pending:
            if time.time() > end:
                logger.warning(f"{host_repo}: wall-clock budget exhausted at tier {tier}")
                break
            spec = parse_stage(sid)
            spec_ctx = dict(ctx)
            spec_ctx["root_sd"] = ctx["roots"][spec["root"]]
            if sid not in archived:
                logger.warning(f"{sid} absent from the archived crossing table -- skipped")
                continue
            try:
                m = regen_cell(rn, P, spec, spec_ctx, cache, archived, tier)
            except Exception as exc:                               # noqa: BLE001
                logger.error(f"{sid} failed: {type(exc).__name__}: {exc}")
                m = {"stage_id": sid, "tier": tier, "status": "UNAVAILABLE",
                     "reason": f"{type(exc).__name__}: {exc}"}
            append_jsonl(RESULTS / "regen_meta.jsonl", [m])
            tiers_reached.append(tier)
        rn.close()
        del rn, ctx
        free_mem()

    qplan = [("A", TIER_A_QWEN), ("B", TIER_B_QWEN), ("D", TIER_D_QWEN)]
    lplan = [("A", TIER_A_LLAMA), ("B", TIER_B_LLAMA), ("D", TIER_D_LLAMA)]
    if args.smoke:
        qplan = [("A", TIER_A_QWEN[:2])]
        lplan = []

    run_host(PARENT_A, qwen_ctx, qplan, args.qwen_budget_min)
    if lplan:
        run_host(HOST_C, lambda rn: llama_ctx(rn, P), lplan, args.llama_budget_min)

    all_meta = read_jsonl(RESULTS / "regen_meta.jsonl")
    clean = [m for m in all_meta if m.get("status") == "CLEAN"]
    summary = {
        "n_cells_attempted": len(all_meta),
        "n_cells_clean": len(clean),
        "n_cells_drift": sum(1 for m in all_meta if m.get("status") == "REGENERATION_DRIFT"),
        "n_cells_unavailable": sum(1 for m in all_meta if m.get("status") == "UNAVAILABLE"),
        "tiers_reached": sorted(set(m.get("tier") for m in all_meta if m.get("tier"))),
        "pooled_hit_rate": float(np.mean([m["hit_rate"] for m in all_meta
                                          if "hit_rate" in m and m.get("tier") != "C"]))
        if any("hit_rate" in m and m.get("tier") != "C" for m in all_meta) else None,
        "n_cells_reproducing_archived_rate_exactly":
            sum(1 for m in all_meta if m.get("reproduces_archived_rate_exactly")),
        "n_rows": len(read_jsonl(OUT)),
        "wall_clock_s": time.time() - t_start,
    }
    (RESULTS / "regen_summary.json").write_text(json.dumps(summary, indent=2))
    STATE.write_text(json.dumps({"done": sorted(done | {m["stage_id"] for m in all_meta})}))
    logger.info(f"REGEN DONE: {json.dumps(summary)}")


if __name__ == "__main__":
    main()
