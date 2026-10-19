#!/usr/bin/env python3
"""Disambiguation for the REAL new-uploader checkpoints.

A real abliterated repo whose W01-W05 equal its parent's admits TWO readings:

  (1) the detector MISSES a genuine edit made by a different toolchain, or
  (2) the repo is effectively an UNEDITED re-upload, in which case it is
      evidence about the repo, not about the detector.

Only a parent-referenced measurement separates them.  For each real candidate we
compute E_1 (which needs the parent and is near 1.0 for a rank-one edit and ~0
for no edit at all) AND the raw weight-delta norm, and we report which reading
the data supports.  Without this check the Arm 1 headline would be unsound.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from loguru import logger

WS = Path(__file__).resolve().parent
sys.path.insert(0, str(WS))
RES = WS / "results"

import hubio  # noqa: E402
import panel as P  # noqa: E402
import wstats  # noqa: E402
from e1 import BAND_HI, BAND_LO, band_keys, e1_pair  # noqa: E402
from hubio import load_config, read_tensors  # noqa: E402
from method import DEV, N_RANDOM, SEED, jdump, jlines, load_model  # noqa: E402

# candidate -> declared parent (from the card / the obvious sibling)
PARENT_OF = {
    "mlabonne/Qwen3-0.6B-abliterated": "Qwen/Qwen3-0.6B",
    "huihui-ai/Qwen3-0.6B-abliterated": "Qwen/Qwen3-0.6B",
    "MagicalAlchemist/Qwen3-1.7B-Magic_decensored": "Qwen/Qwen3-1.7B",
    "BennyDaBall/Qwen3-4b-Z-Image-Turbo-AbliteratedV1": "Qwen/Qwen3-4B",
    # prithivMLmods/VibeThinker-3B-heretic_decensored: the card names no parent we
    # can resolve to a Hub repo, so it is left unpaired and reported as such
    # rather than guessed.
}


def weight_delta(parent_path: str, cand_path: str) -> dict:
    """Relative Frobenius change over the mid-stack residual-write matrices, and
    the fraction of those matrices that are BIT-IDENTICAL to the parent's."""
    L = int(load_config(parent_path)["num_hidden_layers"])
    keys = sorted(set(band_keys(parent_path, L)) & set(band_keys(cand_path, L)))
    num, den, identical = 0.0, 0.0, 0
    for k in keys:
        tp = read_tensors(parent_path, [k]).get(k)
        tc = read_tensors(cand_path, [k]).get(k)
        if tp is None or tc is None or tp.shape != tc.shape:
            continue
        a, b = tp.to(torch.float32), tc.to(torch.float32)
        d = float((a - b).pow(2).sum())
        num += d
        den += float(a.pow(2).sum())
        identical += int(d == 0.0)
        del tp, tc, a, b
    return {"relative_frobenius_delta": (num / den) ** 0.5 if den else float("nan"),
            "n_matrices": len(keys), "n_bit_identical": identical,
            "frac_bit_identical": identical / max(len(keys), 1)}


def run() -> dict:
    real = []
    p = RES / "arm1_real.jsonl"
    if p.exists():
        real = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    cands = [r["variant_id"] for r in real]
    for extra in PARENT_OF:
        if extra not in cands:
            cands.append(extra)

    arch = P.archive()
    rows = []
    for cand in cands:
        par = PARENT_OF.get(cand)
        if par is None:
            rows.append({"candidate": cand, "verdict": "NO_PARENT_DECLARED"})
            continue
        try:
            prec = hubio.ensure(par, arch.get(par, {}).get("revision"))
            crec = hubio.ensure(cand, None)
        except Exception as exc:  # noqa: BLE001
            rows.append({"candidate": cand, "parent": par,
                         "verdict": "FETCH_FAILED", "error": str(exc)[:200]})
            continue
        e1 = e1_pair(prec["path"], crec["path"], device=DEV)
        wd = weight_delta(prec["path"], crec["path"])
        m = load_model(crec["path"])
        w = wstats.w_stats_model(m, n_random=N_RANDOM, seed=SEED, device=DEV)
        del m
        hubio.gc_cuda()
        wp = arch.get(par, {}).get("W", {})

        rel = wd["relative_frobenius_delta"]
        if wd["frac_bit_identical"] > 0.99 or (np.isfinite(rel) and rel < 1e-6):
            verdict = "UNEDITED_RE_UPLOAD"
            reading = ("the candidate's mid-stack write matrices are (bit-)identical to "
                       "the parent's, so this repo carries NO edit; it is evidence about "
                       "the repo, NOT about the detector, and is excluded from the "
                       "recipe-scope AUROC.")
        elif e1.get("ok") and e1["E1"] > 0.9:
            verdict = "GENUINE_RANK_ONE_EDIT_DETECTED_BY_E1"
            reading = ("the parent-referenced E_1 sees a near-rank-one edit; if W05 does "
                       "not, that is a genuine parent-free MISS.")
        elif e1.get("ok"):
            verdict = "GENUINE_EDIT_NOT_RANK_ONE"
            reading = "the edit exists but is not near-rank-one in the mid-stack band."
        else:
            verdict = "UNRESOLVED"
            reading = e1.get("skip_reason", "")

        row = {"candidate": cand, "parent": par,
               "candidate_revision": crec["revision"], "parent_revision": prec["revision"],
               "E1": e1.get("E1"), "E1_ok": e1.get("ok"),
               "E1_skip_reason": e1.get("skip_reason"),
               **wd,
               "W_candidate": {k: getattr(w, k) for k in P.WKEYS},
               "W_parent_archived": wp,
               "W05_delta_vs_parent": (w.W05 - wp["W05"]) if wp else None,
               "verdict": verdict, "reading": reading}
        rows.append(row)
        logger.info(f"REALCHECK {cand}: E1={e1.get('E1')} relF={rel:.3g} "
                    f"bitident={wd['frac_bit_identical']:.2f} -> {verdict}")
        hubio.release(cand, None)
        hubio.release(par, arch.get(par, {}).get("revision"))

    out = {"rows": rows,
           "n_unedited_re_upload": sum(1 for r in rows if r.get("verdict") ==
                                       "UNEDITED_RE_UPLOAD"),
           "n_genuine_miss": sum(1 for r in rows if r.get("verdict") ==
                                 "GENUINE_RANK_ONE_EDIT_DETECTED_BY_E1"
                                 and abs(r.get("W05_delta_vs_parent") or 0) < 0.1),
           "note": "This check exists because a real 'abliterated' repo whose W01-W05 "
                   "equal its parent's is ambiguous between a detector miss and an "
                   "unedited upload. Only the parent-referenced measurement separates "
                   "them, and the recipe-scope AUROC uses the result."}
    jdump(out, RES / "real_checkpoint_check.json")
    jlines(rows, RES / "real_checkpoint_check.jsonl")
    return out


if __name__ == "__main__":
    run()
