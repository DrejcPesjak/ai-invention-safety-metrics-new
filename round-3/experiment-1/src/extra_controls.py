#!/usr/bin/env python3
"""The two sanity controls that need a REAL checkpoint rather than random tensors.

(1) REVISION STABILITY.  A model measured at two revisions of the same repo must
    agree.  If it does not, revision pinning -- not the recipe -- is the
    confound, and every cross-checkpoint comparison inherits that noise.

(2) RANDOM-DIRECTION CONTROL ON A REAL MODEL.  W05 is a MINIMUM over many
    matrices, so a low value could in principle be an artefact of minimising over
    a large set rather than evidence of a shared suppressed direction.  Feeding a
    random unit direction in place of v1 must NOT produce a scar-like W05 on any
    member -- including the abliterated ones, where the true v1 does.
"""

from __future__ import annotations

import sys
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
from method import DEV, N_RANDOM, SEED, jdump, load_model  # noqa: E402

REVISION_PAIRS = ["Qwen/Qwen3-0.6B", "huihui-ai/Qwen2.5-0.5B-Instruct-abliterated"]
RANDOM_DIR_MEMBERS = ["huihui-ai/Qwen2.5-0.5B-Instruct-abliterated",  # a true positive
                      "Qwen/Qwen2.5-0.5B-Instruct",                   # a true negative
                      "allenai/OLMo-1B-hf"]                           # the hardest negative


def _measure(path: str, *, v1_override=None):
    m = load_model(path)
    d = int(m.config.hidden_size)
    names, mats, info = wstats.collect_write_tensors(m, d)
    r = wstats.w_stats_from_matrices(names, mats, d, info["n_layers"],
                                     n_random=N_RANDOM, seed=SEED, device=DEV,
                                     v1_override=v1_override)
    del m, mats
    hubio.gc_cuda()
    return r


def run() -> dict:
    arch = P.archive()
    out: dict = {}

    # ---- (1) revision stability ----------------------------------------
    rev_rows = []
    for repo in REVISION_PAIRS:
        pinned = arch.get(repo, {}).get("revision")
        try:
            a = hubio.ensure(repo, pinned)
            wa = _measure(a["path"])
            hubio.release(repo, pinned)
            b = hubio.ensure(repo, None)          # resolves main
            wb = _measure(b["path"])
            hubio.release(repo, None)
        except Exception as exc:  # noqa: BLE001
            rev_rows.append({"repo": repo, "error": str(exc)[:250]})
            continue
        same = (a["revision"] == b["revision"])
        rev_rows.append({
            "repo": repo, "revision_archived": a["revision"], "revision_main": b["revision"],
            "same_commit": same,
            "W_archived_rev": {k: getattr(wa, k) for k in P.WKEYS},
            "W_main_rev": {k: getattr(wb, k) for k in P.WKEYS},
            "delta": {k: getattr(wb, k) - getattr(wa, k) for k in P.WKEYS},
            "max_abs_delta": max(abs(getattr(wb, k) - getattr(wa, k)) for k in P.WKEYS)})
        logger.info(f"REVISION {repo}: same_commit={same} "
                    f"max|delta|={rev_rows[-1]['max_abs_delta']:.2e}")
    out["revision_stability"] = {
        "rows": rev_rows,
        "max_abs_delta_overall": max((r.get("max_abs_delta", 0.0) for r in rev_rows),
                                     default=None),
        "verdict": ("STABLE" if all(r.get("max_abs_delta", 1e9) < 1e-6 for r in rev_rows)
                    else "REVISION_DRIFT_DETECTED"),
        "note": "if two revisions of the same repo disagree, revision pinning rather "
                "than the recipe is the confound"}

    # ---- (2) random direction in place of v1, on real models ------------
    rnd_rows = []
    rng = np.random.default_rng(4242)
    for repo in RANDOM_DIR_MEMBERS:
        rev = arch.get(repo, {}).get("revision")
        try:
            rec = hubio.ensure(repo, rev)
            true_w = _measure(rec["path"])
            d = true_w.d
            reps = []
            for i in range(5):
                rw = _measure(rec["path"], v1_override=rng.normal(size=d))
                reps.append({"W02": rw.W02, "W05": rw.W05})
            hubio.release(repo, rev)
        except Exception as exc:  # noqa: BLE001
            rnd_rows.append({"repo": repo, "error": str(exc)[:250]})
            continue
        w05s = [r["W05"] for r in reps]
        rnd_rows.append({
            "repo": repo, "member_class": arch.get(repo, {}).get("member_class"),
            "true_v1_W05": true_w.W05, "true_v1_W02": true_w.W02,
            "random_dir_W05_mean": float(np.mean(w05s)),
            "random_dir_W05_min": float(np.min(w05s)),
            "random_dir_W02_max": float(max(r["W02"] for r in reps)),
            "n_random_draws": len(reps),
            "gap_true_minus_random": true_w.W05 - float(np.mean(w05s))})
        logger.info(f"RANDOMDIR {repo}: true W05={true_w.W05:.3f} vs "
                    f"random {np.mean(w05s):.3f} (min {np.min(w05s):.3f})")
    thr = -2.7033532394669777  # the archived separation midpoint
    out["random_direction_control"] = {
        "rows": rnd_rows,
        "detection_threshold_W05": thr,
        "n_random_below_threshold": sum(1 for r in rnd_rows
                                        if r.get("random_dir_W05_min", 0) < thr),
        "verdict": ("PASS" if all(r.get("random_dir_W05_min", 0) > thr for r in rnd_rows)
                    else "FAIL_random_direction_looks_like_a_scar"),
        "note": "W05 is a MINIMUM over matrices; this rules out the statistic being an "
                "artefact of minimising over a large set. A random unit direction must "
                "never look like a scar, including on the abliterated member where the "
                "true minimum eigenvector does."}
    jdump(out, RES / "extra_controls.json")
    return out


if __name__ == "__main__":
    run()
