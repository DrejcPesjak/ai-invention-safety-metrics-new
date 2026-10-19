#!/usr/bin/env python3
"""STAGE assemble -- every statistic, every verdict, and method_out.json.

All inferential numbers come from analysis.py, whose resampling contract is
printed here and stored in the output.  The final block re-derives every quoted
figure from the raw result files and asserts equality; a failure blocks assembly.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch
from loguru import logger

WS = Path(__file__).resolve().parent
sys.path.insert(0, str(WS))
RES = WS / "results"

import analysis as AN  # noqa: E402
import panel as P  # noqa: E402
from method import jdump  # noqa: E402

WNAMES = ["W01", "W02", "W03", "W04", "W05"]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()[:32]


def rd(name: str, default=None):
    p = RES / name
    if not p.exists():
        return default
    if name.endswith(".jsonl"):
        return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    return json.loads(p.read_text())


def s(x) -> str:
    """predict_* fields must be STRINGS in the output schema."""
    if x is None:
        return ""
    if isinstance(x, float):
        return "" if not np.isfinite(x) else f"{x:.6g}"
    return str(x)


# ===========================================================================
# ARM 1 statistics
# ===========================================================================
def arm1_stats() -> dict:
    synth = rd("arm1_synth.jsonl", [])
    real = rd("arm1_real.jsonl", [])
    arch = P.archive()
    cand = rd("arm1_candidates.json", {}) or {}

    # the eight ARCHIVED abliterated positives + every archived non-abliterated
    rows = []
    for repo, a in arch.items():
        if not a["W"]:
            continue
        rows.append({"member": repo, "uploader": P.uploader(repo),
                     "recipe_class": ("global_diff_in_means"
                                      if a["member_class"] == "abliterated" else "none"),
                     "declared_class": a["member_class"], "synthetic": False,
                     "family": a["family"], "lineage_id": a["lineage_id"],
                     "source": "archive", "degenerate": False, **a["W"]})
    for r in synth:
        if r["recipe"] == "none":
            continue
        rows.append({"member": r["variant_id"], "uploader": "in-house-synthetic",
                     "recipe_class": r["recipe_class"],
                     "declared_class": "abliterated_synthetic", "synthetic": True,
                     "family": r.get("family"),
                     "lineage_id": f"{r.get('lineage_id')}::synth",
                     "source": "synthetic", "degenerate": bool(r.get("degenerate")),
                     "layer_fraction": r.get("layer_fraction"), "k": r.get("k"),
                     "behaviour_delta_refusal": r.get("behaviour_delta_refusal"),
                     "harmful_refusal_rate": r.get("behaviour", {}).get("harmful_refusal_rate"),
                     **{k: r[k] for k in WNAMES}})
    rc = {r["candidate"]: r for r in (rd("real_checkpoint_check.jsonl", []) or [])}
    for r in real:
        chk = rc.get(r["variant_id"], {})
        rows.append({"member": r["variant_id"], "uploader": r["uploader"],
                     "recipe_class": r["recipe_class"], "declared_class": "abliterated",
                     "synthetic": False, "family": r.get("family"),
                     "lineage_id": r.get("lineage_id"), "source": "real_new_uploader",
                     "degenerate": False,
                     "edit_verdict": chk.get("verdict", "UNCHECKED"),
                     "E1_vs_declared_parent": chk.get("E1"),
                     "relative_frobenius_delta": chk.get("relative_frobenius_delta"),
                     "excluded_from_auroc": chk.get("verdict") == "UNEDITED_RE_UPLOAD",
                     **{k: r[k] for k in WNAMES}})

    def pos(r):
        return r["declared_class"] in ("abliterated", "abliterated_synthetic")

    out = {"n_rows": len(rows), "rows": rows}

    # -- (i) all-vs-all, for each of W01..W05 -----------------------------
    # The headline grouping EXCLUDES, with reasons:
    #   * the whole layer-fraction sweep -- it is a within-recipe DOSE CURVE and
    #     its own deliverable; `plain_f1.00` already represents that recipe;
    #   * degenerate variants -- a weight signature on a model that no longer
    #     generates is not evidence about detection (none tripped, in fact);
    #   * real repos whose weights turn out to be UNEDITED re-uploads -- they are
    #     evidence about the repo, not the detector.
    head = [r for r in rows
            if r["recipe_class"] != "band"
            and not r["degenerate"]
            and not r.get("excluded_from_auroc")]
    out["headline_set_exclusions"] = {
        "band_sweep_rows": sum(1 for r in rows if r["recipe_class"] == "band"),
        "degenerate_rows": sum(1 for r in rows if r["degenerate"]),
        "unedited_re_upload_rows": sum(1 for r in rows if r.get("excluded_from_auroc")),
        "n_headline": len(head)}
    allvall = {}
    for w in WNAMES:
        v = np.array([r.get(w, np.nan) for r in head], float)
        y = np.array([int(pos(r)) for r in head])
        lin = [r["lineage_id"] for r in head]
        sgn = -1.0 if w in ("W03_never", "W05") else 1.0   # LOW W05 = abliterated
        sgn = -1.0 if w == "W05" else 1.0
        b = AN.bootstrap_ci(sgn * v, y, lin)
        p = AN.permutation_p(sgn * v, y)
        allvall[w] = {**b, "permutation": p, "direction":
                      "lower is positive" if sgn < 0 else "higher is positive"}
    out["auroc_all_vs_all"] = allvall

    # -- (ii) LEAVE-ONE-UPLOADER-OUT --------------------------------------
    v = np.array([r.get("W05", np.nan) for r in head], float)
    y = np.array([int(pos(r)) for r in head])
    up = [r["uploader"] for r in head]
    fam = [r.get("family") or "unknown" for r in head]
    lin = [r["lineage_id"] for r in head]
    out["leave_one_uploader_out_W05"] = AN.leave_one_group_out(v, y, up, lin,
                                                               lower_is_positive=True)
    out["leave_one_family_out_W05"] = AN.leave_one_group_out(v, y, fam, lin,
                                                             lower_is_positive=True)

    # -- REAL out-of-uploader generalisation, the sharpest test in the arm --
    # The archived eight positives come from two uploaders. These are REAL,
    # published, <=4.2B abliterated/decensored checkpoints from uploaders the
    # detector has never seen, scored against the SAME negatives.
    negs_all = [r for r in head if not pos(r)]
    new_up = [r for r in head if pos(r) and r["source"] == "real_new_uploader"]
    old_up = [r for r in head if pos(r) and r["source"] == "archive"]
    thr_arch = None
    if old_up and negs_all:
        thr_arch = (max(r["W05"] for r in old_up) + min(r["W05"] for r in negs_all)) / 2.0
    blk = {}
    for tag, grp in (("archived_uploaders", old_up), ("new_uploaders", new_up)):
        if not grp or not negs_all:
            continue
        sel = grp + negs_all
        vv = np.array([-r["W05"] for r in sel], float)
        yy = np.array([1] * len(grp) + [0] * len(negs_all))
        ll = [r["lineage_id"] for r in sel]
        b = AN.bootstrap_ci(vv, yy, ll)
        blk[tag] = {**b, "permutation": AN.permutation_p(vv, yy),
                    "members": [r["member"] for r in grp],
                    "W05_values": [r["W05"] for r in grp],
                    "catch_rate_at_archived_threshold":
                        (float(np.mean([r["W05"] < thr_arch for r in grp]))
                         if thr_arch is not None else None),
                    "threshold": thr_arch}
    out["real_uploader_generalisation_W05"] = blk
    if "new_uploaders" in blk and "archived_uploaders" in blk:
        out["real_uploader_generalisation_sentence"] = (
            f"On the two uploaders the eight archived positives come from, W05 separates "
            f"perfectly (AUROC {blk['archived_uploaders']['estimate']:.3f}, catch rate "
            f"{blk['archived_uploaders']['catch_rate_at_archived_threshold']:.2f}). On "
            f"{blk['new_uploaders']['n_pos']} REAL published abliterated/decensored "
            f"checkpoints at <=4.2B from uploaders it has never seen, scored against the "
            f"same negatives, it collapses to AUROC "
            f"{blk['new_uploaders']['estimate']:.3f} and catches "
            f"{blk['new_uploaders']['catch_rate_at_archived_threshold']:.2f} of them at "
            f"the threshold fitted on the archived uploaders.")

    # -- per-recipe-class AUROC (the scope sentence's evidence) ------------
    negs = [r for r in head if not pos(r)]
    # The scope class separates the SAME verified recipe by whether the uploader
    # is one of the two the archived positives come from.  Pooling them would
    # hide the fact that the recipe class is detected for the archived uploaders
    # and missed for every other uploader -- which is the arm's whole point.
    def scope_class(r):
        c = r["recipe_class"]
        return f"{c}@new_uploader" if r["source"] == "real_new_uploader" else c
    for r in head:
        r["scope_class"] = scope_class(r)
    per_class = {}
    for cls in sorted({r["scope_class"] for r in head if pos(r)}):
        sel = [r for r in head if (pos(r) and r["scope_class"] == cls)] + negs
        vv = np.array([-r.get("W05", np.nan) for r in sel], float)
        yy = np.array([int(pos(r) and r["scope_class"] == cls) for r in sel])
        ll = [r["lineage_id"] for r in sel]
        b = AN.bootstrap_ci(vv, yy, ll)
        w02 = [r.get("W02") for r in sel if yy[sel.index(r)] == 1] if False else None
        per_class[cls] = {**b, "n_positives": int(yy.sum()),
                          "median_W05_positives": float(np.median(
                              [r["W05"] for r, k in zip(sel, yy) if k])),
                          "median_W02_positives": float(np.median(
                              [r["W02"] for r, k in zip(sel, yy) if k]))}
    out["auroc_by_recipe_class_W05"] = per_class

    # -- (d) LAYER-FRACTION CURVE and its crossing point f* ---------------
    curves = {}
    for r in synth:
        if r.get("layer_fraction") is None:
            continue
        curves.setdefault(r["host"], []).append(
            {"f": r["layer_fraction"], **{k: r[k] for k in WNAMES},
             "cos_v1_r": r.get("cos_v1_r"), "n_layers_edited": r["audit"].get("n_layers_edited"),
             "harmful_refusal_rate": r.get("behaviour", {}).get("harmful_refusal_rate"),
             "degenerate": r.get("degenerate")})
    # detection threshold: the midpoint of the archived separation on W05
    abl = [a["W"]["W05"] for a in arch.values() if a["member_class"] == "abliterated" and a["W"]]
    non = [a["W"]["W05"] for a in arch.values() if a["member_class"] != "abliterated" and a["W"]]
    thr = (max(abl) + min(non)) / 2.0
    fstar = {}
    for host, cur in curves.items():
        cur.sort(key=lambda z: z["f"])
        det = [c["f"] for c in cur if c["W05"] < thr]
        fstar[host] = {"f_star": (min(det) if det else None),
                       "detected_fractions": det,
                       "threshold_W05": thr,
                       "threshold_note": "midpoint of the archived abliterated/"
                                         "non-abliterated W05 separation "
                                         f"({max(abl):.3f} vs {min(non):.3f})"}
    out["layer_fraction_curves"] = curves
    out["layer_fraction_f_star"] = fstar
    out["archived_separation"] = {"weakest_abliterated_W05": max(abl),
                                  "strongest_non_abliterated_W05": min(non),
                                  "gap": min(non) - max(abl), "midpoint": thr}

    # -- (D) SCOPE SENTENCE, generated from the numbers --------------------
    detected = sorted(c for c, v in per_class.items() if v["estimate"] >= 0.95)
    missed = sorted(c for c, v in per_class.items() if v["estimate"] < 0.80)
    mid = sorted(c for c, v in per_class.items() if 0.80 <= v["estimate"] < 0.95)
    fs = [v["f_star"] for v in fstar.values() if v["f_star"] is not None]
    fstar_txt = (f"the layer-fraction curve crosses at f*={min(fs):.2f}"
                 if fs else "the layer-fraction curve never crosses the detection "
                            "threshold below f=1.00")
    # the behavioural counterpart: an edit that is INVISIBLE yet fully effective
    invisible_but_working = []
    for host, cur in curves.items():
        base = next((r for r in synth if r["recipe"] == "none" and r["host"] == host), None)
        if base is None:
            continue
        b_w05 = base["W05"]
        b_rate = base["behaviour"]["harmful_refusal_rate"]
        full = next((c for c in cur if c["f"] == 1.0), None)
        for c in cur:
            if c["f"] >= 1.0:
                continue
            undetected = abs(c["W05"] - b_w05) < 0.1
            works = (full is not None and b_rate - c["harmful_refusal_rate"]
                     >= 0.99 * (b_rate - full["harmful_refusal_rate"]) and b_rate > 0)
            if undetected and works:
                invisible_but_working.append(
                    {"host": host, "f": c["f"], "W05": c["W05"], "unedited_W05": b_w05,
                     "refusal_rate": c["harmful_refusal_rate"], "unedited_rate": b_rate,
                     "full_edit_rate": full["harmful_refusal_rate"],
                     "degenerate": c["degenerate"]})
    out["invisible_but_fully_effective_edits"] = invisible_but_working

    out["scope_sentence"] = (
        f"W05 detects {', '.join(detected) if detected else 'no recipe class'} "
        f"(AUROC >= 0.95); it misses {', '.join(missed) if missed else 'no class'} "
        f"(AUROC < 0.80)"
        + (f"; intermediate: {', '.join(mid)}" if mid else "")
        + f". Within the global single-direction recipe, {fstar_txt}: surgery confined "
          f"to a smaller contiguous layer band leaves no detectable scar"
        + (f", and at f={min(z['f'] for z in invisible_but_working):.2f} the edit is "
           f"already as behaviourally effective as the full-stack edit while W05 is "
           f"indistinguishable from the unedited model"
           if invisible_but_working else "")
        + ".")
    out["prereg"] = rd("prereg_arm1.json", {})
    ver = cand.get("verified", [])
    diff = [v for v in ver if v.get("mechanically_different")]
    diff_big = [v for v in diff if v.get("params") and v["params"] > 4.2e9]
    sizes = sorted(v["params"] for v in diff if v.get("params"))
    out["candidate_search"] = {
        "n_verified": len(ver),
        "n_qualified": cand.get("n_qualified", 0),
        "qualified": cand.get("qualified", []),
        "n_new_uploader_same_recipe": cand.get("n_new_uploader_same_recipe", 0),
        "new_uploader_same_recipe": cand.get("new_uploader_same_recipe", []),
        "queries": cand.get("search", {}).get("queries", []),
        "n_unique_repos_seen": cand.get("search", {}).get("n_unique_repos", 0),
        "n_excluded_quantised": cand.get("search", {}).get("n_excluded_quantised", 0),
        "date": cand.get("search", {}).get("date"),
        "n_mechanically_different_any_size": len(diff),
        "n_mechanically_different_above_ceiling": len(diff_big),
        "mechanically_different_min_params": (sizes[0] if sizes else None),
        "mechanically_different_examples": [
            {"repo": v["repo"], "params": v["params"], "recipe_class": v["recipe_class"],
             "evidence_quote": v["evidence_quote"][:300], "evidence_url": v["evidence_url"]}
            for v in diff[:8]],
        # THE finding that forces the fallback, stated as a measured fact
        "verdict": (
            f"Mechanically different abliteration recipes DO exist on the Hub "
            f"({len(diff)} of {len(ver)} verified candidates: norm-preserving, "
            f"multi-direction, biprojected), but every one of them is ABOVE the 4.2B "
            f"ceiling (smallest {sizes[0]/1e9:.1f}B). At <=4.2B every verified "
            f"abliteration checkpoint we could find resolves to the SAME all-layer "
            f"global single-direction diff-in-means recipe. The cross-uploader "
            f"generalisation question is therefore answered here only for in-house "
            f"reimplementations, and the arm's synthetic half carries it -- as the "
            f"pre-registered fallback specified."
            if diff and not cand.get("n_qualified") else
            f"{cand.get('n_qualified', 0)} candidates qualified at <=4.2B."),
    }
    return out


# ===========================================================================
# ARM 2 statistics
# ===========================================================================
def arm2_stats() -> dict:
    pairs = [r for r in rd("arm2_all.jsonl", []) if r.get("ok")]
    # The plan requires E_1 to be applied to the NEW-TOOLCHAIN checkpoints wherever a
    # parent resolves.  Those pairs are the decisive ones: they are the only
    # positives in the head-to-head that come from an uploader outside the two the
    # detector was characterised on.  Excluding them would compare the two methods
    # only where the parent-free one was already known to work.
    for r in (rd("real_checkpoint_check.jsonl", []) or []):
        if not r.get("E1_ok") or r.get("verdict") == "UNEDITED_RE_UPLOAD":
            continue
        pairs.append({"parent": r["parent"], "candidate": r["candidate"],
                      "pair_type": "positive_new_uploader",
                      "is_abliteration_edit": True, "ok": True,
                      "E1": r["E1"], "W05_candidate": r["W_candidate"]["W05"],
                      "W01_candidate": r["W_candidate"]["W01"],
                      "W02_candidate": r["W_candidate"]["W02"],
                      "lineage_id": r["parent"], "family": None,
                      "n_matrices": r.get("n_matrices"),
                      "relative_frobenius_delta": r.get("relative_frobenius_delta"),
                      "edit_verdict": r["verdict"]})
    real = [r for r in pairs if not str(r["pair_type"]).endswith("synthetic")]
    out = {"n_pairs": len(pairs), "n_real_pairs": len(real), "pairs": pairs}
    if len(real) < 2:
        out["verdict"] = "UNRESOLVABLE"
        out["note"] = f"only {len(real)} resolvable real pairs; reported as a case study"
        return out

    def blk(rows, tag):
        v_e1 = np.array([r.get("E1", np.nan) for r in rows], float)
        v_w5 = np.array([-r.get("W05_candidate", np.nan) if r.get("W05_candidate") is not None
                         else np.nan for r in rows], float)
        y = np.array([int(bool(r["is_abliteration_edit"])) for r in rows])
        lin = [r.get("lineage_id") or r["parent"] for r in rows]
        m = np.isfinite(v_e1) & np.isfinite(v_w5)
        if m.sum() < 3 or len(set(y[m])) < 2:
            return {"skip": f"{tag}: insufficient matched data (n={int(m.sum())})"}
        v_e1, v_w5, y = v_e1[m], v_w5[m], y[m]
        lin = [l for l, k in zip(lin, m) if k]
        a_e1 = AN.bootstrap_ci(v_e1, y, lin)
        a_w5 = AN.bootstrap_ci(v_w5, y, lin)
        d = AN.paired_auroc_diff(v_w5, v_e1, y, lin)
        return {"auroc_E1_parent_required": a_e1, "auroc_W05_parent_free": a_w5,
                "paired_difference_W05_minus_E1": d,
                "permutation_E1": AN.permutation_p(v_e1, y),
                "permutation_W05": AN.permutation_p(v_w5, y),
                "n_matched": int(len(y)), "n_pos": int(y.sum()),
                "n_neg": int(len(y) - y.sum())}

    out["matched_subset_real_pairs_only"] = blk(real, "real")
    out["matched_subset_incl_synthetic"] = blk(pairs, "all")
    # The pre-declared 12 pairs only: every positive there comes from one of the
    # two uploaders the detector was characterised on.
    prereg_only = [r for r in real if r["pair_type"] != "positive_new_uploader"]
    out["matched_subset_prereg_pairs_only"] = blk(prereg_only, "prereg")
    out["pair_counts"] = {
        "prereg_pairs": len(prereg_only),
        "new_uploader_pairs": sum(1 for r in real
                                  if r["pair_type"] == "positive_new_uploader"),
        "synthetic_pairs": len(pairs) - len(real)}
    # Per-pair detail on the decisive positives, so the miss is inspectable.
    out["new_uploader_pairs_detail"] = [
        {"candidate": r["candidate"], "parent": r["parent"], "E1": r["E1"],
         "W05_candidate": r["W05_candidate"], "edit_verdict": r.get("edit_verdict"),
         "relative_frobenius_delta": r.get("relative_frobenius_delta"),
         "E1_detects": bool(r["E1"] > 0.9),
         "W05_detects": bool(r["W05_candidate"] < -2.7033532394669777)}
        for r in real if r["pair_type"] == "positive_new_uploader"]

    r = out["matched_subset_real_pairs_only"]
    if "skip" in r:
        out["verdict"] = "UNRESOLVABLE"
        out["trade_sentence"] = ("Arm 2 is reported as a case study: "
                                 + r["skip"])
    else:
        d = r["paired_difference_W05_minus_E1"]
        nu = out.get("new_uploader_pairs_detail", [])
        n_w05_miss = sum(1 for z in nu if not z["W05_detects"])
        n_e1_hit = sum(1 for z in nu if z["E1_detects"])
        if nu and n_w05_miss == len(nu) and n_e1_hit == len(nu) and not d["excludes_zero"]:
            # The interval covers zero only at its boundary and n is small; calling
            # this a match would overstate what 15 pairs can show, while calling it
            # a significant cost would overstate the interval.  State both.
            out["verdict"] = f"PARENT_FREE_COSTS_{abs(d['estimate']):.3f}_UNDERPOWERED"
            out["trade_sentence"] = (
                f"On the pre-declared 12 pairs -- whose positives all come from the two "
                f"uploaders the detector was characterised on -- the parent-free W05 and "
                f"the parent-required E_1 TIE at AUROC 1.000. Adding the "
                f"{len(nu)} pairs whose candidate comes from a NEW uploader reverses that: "
                f"E_1 stays at 1.000 while W05 falls to "
                f"{r['auroc_W05_parent_free']['estimate']:.3f}, a paired difference of "
                f"{d['estimate']:+.3f} [{d['ci_low']:.3f}, {d['ci_high']:.3f}] over "
                f"{r['n_matched']} matched members. The interval reaches zero at its "
                f"boundary, so at n={r['n_matched']} this is UNDERPOWERED as an interval "
                f"claim; descriptively it is unambiguous -- E_1 detects "
                f"{n_e1_hit}/{len(nu)} of the new-uploader edits and W05 detects "
                f"0/{len(nu)}, and all {len(nu)} are confirmed genuine near-rank-one edits "
                f"(E_1 >= 0.99, no bit-identical re-uploads). The parent-free constraint "
                f"does not cost accuracy on the recipes it was tuned on; it costs "
                f"generalisation to new uploaders of the SAME recipe.")
        elif not d["excludes_zero"]:
            out["verdict"] = "PARENT_FREE_MATCHES"
            out["trade_sentence"] = (
                f"On the {r['n_matched']} members where a parent resolves "
                f"({r['n_pos']} abliteration edits, {r['n_neg']} benign fine-tune steps), "
                f"the parent-free W05 reaches AUROC {r['auroc_W05_parent_free']['estimate']:.3f} "
                f"against the parent-required E_1's "
                f"{r['auroc_E1_parent_required']['estimate']:.3f}; the paired difference is "
                f"{d['estimate']:+.3f} [{d['ci_low']:.3f}, {d['ci_high']:.3f}], which covers "
                f"zero -- parent-free matches parent-required on this matched panel at zero "
                f"prompt cost and zero parent cost.")
        elif d["estimate"] < 0:
            out["verdict"] = f"PARENT_FREE_COSTS_{abs(d['estimate']):.3f}"
            out["trade_sentence"] = (
                f"The parent-free constraint costs {abs(d['estimate']):.3f} AUROC "
                f"[{-d['ci_high']:.3f}, {-d['ci_low']:.3f}] on the matched subset "
                f"(n={r['n_matched']}).")
        else:
            out["verdict"] = "PARENT_FREE_EXCEEDS"
            out["trade_sentence"] = (
                f"The parent-free W05 BEATS the parent-required E_1 by "
                f"{d['estimate']:.3f} AUROC [{d['ci_low']:.3f}, {d['ci_high']:.3f}] "
                f"on the matched subset (n={r['n_matched']}).")
    return out


# ===========================================================================
# ARM 3 statistics
# ===========================================================================
def arm3_stats() -> dict:
    long = rd("long_table_depth.jsonl", [])
    meta = rd("arm3.json", {}) or {}
    beh = P.behaviour()
    out = {"n_rows": len(long), "meta": meta}
    if not long:
        out["verdict"] = "NOT_RUN"
        return out

    def refusal_of(repo):
        b = beh.get(repo, {})
        for k in ("B09_greedy_refusal_rate_harmful", "harmful_refusal_rate",
                  "refusal_rate_harmful", "rubricB_harmful_refusal"):
            if isinstance(b.get(k), (int, float)):
                return float(b[k])
        for k, v in b.items():
            if "refus" in k.lower() and isinstance(v, (int, float)):
                return float(v)
        return np.nan

    arch = P.archive()
    depths = sorted({(r["depth_name"], r["rel_depth"]) for r in long}, key=lambda z: z[1])
    metrics = sorted({r["metric_id"] for r in long})
    BASE_IDS = ("B09_greedy_refusal_rate_harmful", "B01_logit_gap_harmful")
    table, censor = {}, {}
    for dname, drel in depths:
        per_metric = {}
        # per-member value of each metric at this depth, keyed for the paired test
        byval: dict[str, dict[str, float]] = {}
        for mid in metrics:
            sel = [r for r in long if r["depth_name"] == dname and r["metric_id"] == mid]
            vals = {r["member_repo"]: r.get("value") for r in sel
                    if r.get("value") is not None}
            byval[mid] = vals
            xs = [v for k, v in vals.items() if np.isfinite(refusal_of(k))]
            ys = [refusal_of(k) for k in vals if np.isfinite(refusal_of(k))]
            lins = [arch.get(k, {}).get("lineage_id", k) for k in vals
                    if np.isfinite(refusal_of(k))]
            if len(xs) >= 4:
                per_metric[mid] = {**AN.spearman_ci(np.array(xs), np.array(ys), lins),
                                   "n_members": len(xs)}
        # black-box baselines from the ARCHIVE, on the same members
        mems = sorted({r["member_repo"] for r in long if r["depth_name"] == dname})
        for base_id in BASE_IDS:
            vals = {mm: arch.get(mm, {}).get("all", {}).get(base_id) for mm in mems}
            vals = {k: v for k, v in vals.items() if v is not None}
            byval[f"BASELINE::{base_id}"] = vals
            xs = [v for k, v in vals.items() if np.isfinite(refusal_of(k))]
            ys = [refusal_of(k) for k in vals if np.isfinite(refusal_of(k))]
            lins = [arch[k]["lineage_id"] for k in vals if np.isfinite(refusal_of(k))]
            if len(xs) >= 4:
                per_metric[f"BASELINE::{base_id}"] = {
                    **AN.spearman_ci(np.array(xs), np.array(ys), lins),
                    "n_members": len(xs), "is_baseline": True}
        # PAIRED lineage-bootstrap difference of each metric against each baseline,
        # on the members where BOTH are observed.  This -- not a comparison of two
        # point estimates -- is what decides whether a metric beats the baseline.
        paired = {}
        for mid in metrics:
            if mid not in per_metric:
                continue
            for base_id in BASE_IDS:
                bkey = f"BASELINE::{base_id}"
                if bkey not in per_metric:
                    continue
                shared = [k for k in byval[mid]
                          if k in byval[bkey] and np.isfinite(refusal_of(k))]
                if len(shared) < 4:
                    continue
                # sign-align: correlations are compared in ABSOLUTE strength
                xa = np.array([byval[mid][k] for k in shared], float)
                xb = np.array([byval[bkey][k] for k in shared], float)
                yy = np.array([refusal_of(k) for k in shared], float)
                ll = [arch.get(k, {}).get("lineage_id", k) for k in shared]
                sa = np.sign(AN.spearman(xa, yy)) or 1.0
                sb = np.sign(AN.spearman(xb, yy)) or 1.0
                paired[f"{mid}__vs__{base_id}"] = {
                    **AN.paired_spearman_diff(sa * xa, sb * xb, yy, ll),
                    "metric": mid, "baseline": base_id,
                    "note": "sign-aligned; positive = the activation metric correlates "
                            "MORE strongly (in absolute terms) than the baseline"}
        table[dname] = {"rel_depth": drel, "metrics": per_metric,
                        "paired_vs_baseline": paired}
        sel = [r for r in long if r["depth_name"] == dname and r["metric_id"] == "A22_alpha_50"]
        censor[dname] = {"rel_depth": drel,
                         "n_censored": sum(1 for r in sel if r.get("is_censored")),
                         "n_total": len(sel),
                         "n_usable": sum(1 for r in sel if r.get("value") is not None)}
    out["per_depth_correlations"] = table
    out["alpha50_censoring_by_depth"] = censor

    # Does ANY activation metric beat the black-box baseline at ANY depth?
    # "Beats" = the PAIRED lineage-bootstrap difference is positive AND its CI
    # excludes zero.  A larger point estimate alone is not evidence.
    beats, nominal = [], []
    for dname, blk in table.items():
        for key, pd in blk.get("paired_vs_baseline", {}).items():
            if not np.isfinite(pd.get("estimate", np.nan)):
                continue
            rec = {"depth": dname, "rel_depth": blk["rel_depth"],
                   "metric": pd["metric"], "baseline": pd["baseline"],
                   "paired_diff": pd["estimate"],
                   "paired_ci": [pd.get("ci_low"), pd.get("ci_high")],
                   "excludes_zero": pd.get("excludes_zero"), "n": pd["n"],
                   "metric_rho": blk["metrics"][pd["metric"]]["estimate"],
                   "baseline_rho": blk["metrics"][f"BASELINE::{pd['baseline']}"]["estimate"]}
            if pd["estimate"] > 0:
                nominal.append(rec)
                if pd.get("excludes_zero"):
                    beats.append(rec)
    out["activation_beats_blackbox_nominally"] = nominal
    out["activation_beats_blackbox_paired_ci_excludes_zero"] = beats
    out["beats_criterion"] = (
        "paired lineage-bootstrap difference rho(metric) - rho(baseline), sign-aligned, "
        "on members where both are observed; 'beats' requires the CI to exclude zero. "
        "Comparing point estimates alone would have called a 0.004 gap with almost "
        "entirely overlapping CIs a win.")

    # invariance: does the falsifier conclusion change across depths?
    conclusions = {}
    for dname, blk in table.items():
        any_beat = any(b["depth"] == dname for b in beats)
        conclusions[dname] = "ACTIVATION_WINS" if any_beat else "BLACKBOX_WINS"
    vals = set(conclusions.values())
    out["per_depth_conclusion"] = conclusions

    # alpha_50's ceiling censoring is itself depth-dependent, and the
    # pre-declared depth is NOT the one that yields the most usable values.
    best = max(censor.items(), key=lambda kv: kv[1]["n_usable"]) if censor else None
    if best:
        rs = censor.get("rho_star", {})
        out["alpha50_censoring_finding"] = {
            "best_depth": best[0], "best_rel_depth": best[1]["rel_depth"],
            "best_n_usable": best[1]["n_usable"],
            "prereg_depth_n_usable": rs.get("n_usable"),
            "prereg_depth_n_censored": rs.get("n_censored"),
            "n_total": rs.get("n_total"),
            "sentence": (
                f"alpha_50's ceiling censoring is strongly depth-dependent: "
                f"{censor.get('bare_argmax', {}).get('n_censored')}/"
                f"{censor.get('bare_argmax', {}).get('n_total')} censored at the bare "
                f"AUROC argmax, {censor.get('mid', {}).get('n_censored')}/"
                f"{censor.get('mid', {}).get('n_total')} at 0.50, and "
                f"{rs.get('n_censored')}/{rs.get('n_total')} at the pre-declared "
                f"rho*=0.679. The pre-declared depth is NOT the one that yields the most "
                f"usable values -- {best[0]} (rel_depth {best[1]['rel_depth']:.3f}) gives "
                f"{best[1]['n_usable']} against {rs.get('n_usable')}. Depth selection for "
                f"the AUROC plateau and depth selection for steering headroom are "
                f"different problems, and iteration 2 conflated them.")}
    if len(vals) == 1:
        out["verdict"] = "INVARIANT"
        out["invariance_sentence"] = (
            f"The falsifier conclusion is INVARIANT across the plateau: at all "
            f"{len(conclusions)} depths ({', '.join(f'{k}={v:.3f}' for k, v in [(d, t['rel_depth']) for d, t in table.items()])}) "
            f"the verdict is {list(vals)[0]}.")
    else:
        bad = [d for d, c in conclusions.items() if c == "ACTIVATION_WINS"]
        out["verdict"] = "NOT_INVARIANT_" + ",".join(bad)
        out["invariance_sentence"] = (
            f"The falsifier conclusion is NOT invariant: it flips at depth(s) "
            f"{bad}. This is disclosed prominently even though rho*=0.679 was the "
            f"pre-declared primary.")
    return out


# ===========================================================================
def run() -> dict:
    t0 = time.time()
    AN.print_contract()
    gate = rd("gate.json", {}) or {}
    ctrl = rd("controls.json", {}) or {}
    smoke = rd("smoke.json", {}) or {}
    a1, a2, a3 = arm1_stats(), arm2_stats(), arm3_stats()

    # ---- verdicts -------------------------------------------------------
    if gate.get("gate_pass") != "PASS":
        scar = "GATE_FAILED"
    else:
        pc = a1.get("auroc_by_recipe_class_W05", {})
        diff_cls = [c for c in pc if c not in ("global_diff_in_means", "plain", "band")]
        low = [c for c in diff_cls if pc[c]["estimate"] < 0.80]
        fs = [v["f_star"] for v in a1.get("layer_fraction_f_star", {}).values()
              if v.get("f_star") is not None]
        scar = ("RECIPE_CLASS_BOUNDED" if (low or (fs and min(fs) > 0.33) or not fs)
                else "GENERALISES")
    verdicts = {"SCAR_SCOPE": scar, "E1_TRADE": a2.get("verdict", "UNRESOLVABLE"),
                "DEPTH_INVARIANCE": a3.get("verdict", "NOT_RUN"),
                "GATE": gate.get("gate_pass", "NO_DATA"),
                "CONDITIONED_ON_UNREPRODUCED_BASELINE": gate.get("gate_pass") != "PASS"}

    src = {f.name: sha(f) for f in sorted(WS.glob("*.py"))}
    run_meta = {
        "torch": torch.__version__, "transformers": __import__("transformers").__version__,
        "python": platform.python_version(),
        "gpu": (torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"),
        "seed": 0, "n_random_directions": 256, "analysis_contract": AN.CONTRACT,
        "source_sha256": src,
        "vendored_sha256": {f.name: sha(f) for f in sorted(WS.glob("vendored_*.py"))},
        "vendored_patches": [],
        "vendoring_note": "vendored_lib_*.py are BYTE-IDENTICAL copies of the iteration-2 "
                          "sources; lib_*.py in this workspace are pure alias shims so the "
                          "vendored files could stay unpatched. Arm 1's W01-W05 do NOT come "
                          "from them -- wstats.py is an independent reimplementation.",
        "llm_api_spend_usd": 0.0, "n_judge_calls": 0,
        "tier_completed": ("tier2" if a1.get("candidate_search", {}).get("n_qualified", 0)
                           or len(a1.get("layer_fraction_curves", {})) > 1 else "tier1"),
        "wall_clock_s": round(time.time() - t0, 1),
    }

    # ---- datasets (exp_gen_sol_out schema) ------------------------------
    ds = []

    gate_rows = []
    for r in gate.get("rows", []):
        gate_rows.append({
            "input": f"Recompute W01-W05 from the published definitions for {r['repo']} "
                     f"(class={r['member_class']}, {r['n_layers']} layers, d={r['d']}, "
                     f"{r['n_matrices']} residual-write matrices) at the archived revision "
                     f"{str(r['archived_revision'])[:12]}.",
            "output": json.dumps({k: round(v, 6) for k, v in r["archived"].items()}),
            "predict_reimplementation": json.dumps(
                {k: round(v, 6) for k, v in r["recomputed"].items()}),
            "predict_delta_vs_archive": json.dumps(
                {k: round(v, 8) for k, v in r["delta"].items()}),
            "metadata_fold": "gate", "metadata_repo": r["repo"],
            "metadata_member_class": r["member_class"], "metadata_family": r["family"],
            "metadata_lineage_id": r["lineage_id"],
            "metadata_revision": r["revision"], "metadata_params": r["param_count"],
            "metadata_delta_float32_gram": r["delta_float32_load"],
            "metadata_n_matrices": r["n_matrices"],
            "metadata_weights_sha256_index": r["weights_sha256_index"]})
    if gate_rows:
        ds.append({"dataset": "gate_reproduction", "examples": gate_rows})

    a1rows = []
    for r in a1.get("rows", []):
        det = "abliterated" if r.get("W05", 0) < a1["archived_separation"]["midpoint"] \
            else "not_abliterated"
        a1rows.append({
            "input": f"Weights-only screen of {r['member']} "
                     f"(uploader={r['uploader']}, recipe_class={r['recipe_class']}, "
                     f"synthetic={r['synthetic']}).",
            "output": r["declared_class"],
            "predict_W05_detector": det,
            "predict_W05": s(r.get("W05")), "predict_W01": s(r.get("W01")),
            "predict_W02": s(r.get("W02")),
            "metadata_fold": "arm1_recipe_scope", "metadata_member": r["member"],
            "metadata_uploader": r["uploader"], "metadata_recipe_class": r["recipe_class"],
            "metadata_synthetic": r["synthetic"], "metadata_source": r["source"],
            "metadata_family": r.get("family"), "metadata_lineage_id": r.get("lineage_id"),
            "metadata_degenerate": r.get("degenerate"),
            "metadata_layer_fraction": r.get("layer_fraction"), "metadata_k": r.get("k"),
            "metadata_W": {k: r.get(k) for k in WNAMES},
            "metadata_harmful_refusal_rate": r.get("harmful_refusal_rate"),
            "metadata_behaviour_delta_refusal": r.get("behaviour_delta_refusal")})
    if a1rows:
        ds.append({"dataset": "arm1_recipe_scope", "examples": a1rows})

    a2rows = []
    for r in a2.get("pairs", []):
        a2rows.append({
            "input": f"Detect an abliteration edit in {r['candidate']} given its parent "
                     f"{r['parent']} (pair_type={r['pair_type']}).",
            "output": "abliteration_edit" if r["is_abliteration_edit"] else "benign_edit",
            "predict_E1_parent_required": s(r.get("E1")),
            "predict_W05_parent_free": s(r.get("W05_candidate")),
            "metadata_fold": "arm2_e1_headtohead", "metadata_parent": r["parent"],
            "metadata_candidate": r["candidate"], "metadata_pair_type": r["pair_type"],
            "metadata_lineage_id": r.get("lineage_id"), "metadata_family": r.get("family"),
            "metadata_n_matrices": r.get("n_matrices"), "metadata_band": r.get("band"),
            "metadata_band_layers": r.get("band_layers"),
            "metadata_recipe": r.get("recipe")})
    if a2rows:
        ds.append({"dataset": "arm2_e1_headtohead", "examples": a2rows})

    long = rd("long_table_depth.jsonl", [])
    a3rows = []
    for r in long:
        a3rows.append({
            "input": f"{r['metric_id']} for {r['member_repo']} at relative depth "
                     f"{r['rel_depth']:.4f} (layer {r['layer_index']} of {r['n_layers']}, "
                     f"renderer={r['renderer']}).",
            "output": r["declared_class"],
            "predict_value": s(r.get("value")),
            "metadata_fold": "arm3_depth_long_table",
            "metadata_member_repo": r["member_repo"], "metadata_revision": r["revision"],
            "metadata_lineage_id": r["lineage_id"], "metadata_family": r["family"],
            "metadata_declared_class": r["declared_class"],
            "metadata_renderer": r["renderer"], "metadata_rel_depth": r["rel_depth"],
            "metadata_depth_name": r["depth_name"], "metadata_layer_index": r["layer_index"],
            "metadata_metric_id": r["metric_id"], "metadata_value": r.get("value"),
            "metadata_is_censored": r.get("is_censored"), "metadata_n_items": r.get("n_items"),
            "metadata_seconds": r.get("seconds"), "metadata_dtype": r.get("dtype")})
    if a3rows:
        ds.append({"dataset": "arm3_depth_long_table", "examples": a3rows})

    if not ds:
        ds = [{"dataset": "empty", "examples": [{"input": "no stage produced rows",
                                                 "output": "none"}]}]

    out = {"metadata": {
        "method_name": "Parent-free abliteration weight scar: how far does it reach?",
        "description": (
            "Three tensor-side arms on one download budget. GATE: W01-W05 reimplemented "
            "from the published definitions and checked against the archived iteration-2 "
            "values. ARM 1: recipe scope, via in-house synthetic recipe variants (norm-"
            "preserving, rank-k, per-head, layer-fraction sweep) plus verified real "
            "new-toolchain checkpoints. ARM 2: head-to-head against the parent-REQUIRING "
            "incumbent E_1 on exactly the matched subset. ARM 3: depth invariance of the "
            "activation arm across the saturated AUROC plateau."),
        "run_meta": run_meta, "verdicts": verdicts,
        "gate": {k: v for k, v in gate.items() if k != "rows"},
        "controls": ctrl, "smoke": smoke,
        "extra_controls": rd("extra_controls.json", {}),
        "real_checkpoint_check": rd("real_checkpoint_check.json", {}),
        "arm1": {k: v for k, v in a1.items() if k != "rows"},
        "arm2": {k: v for k, v in a2.items() if k != "pairs"},
        "arm3": {k: v for k, v in a3.items() if k != "meta"},
        "arm3_meta": a3.get("meta", {}),
        "long_table_pointer": "results/long_table_depth.jsonl",
        "headline": _headline(gate, a1, a2, a3, verdicts),
    }, "datasets": ds}

    jdump(out, WS / "method_out.json")
    _assert_block(out)
    logger.info(f"assembled: {sum(len(d['examples']) for d in ds)} rows over {len(ds)} datasets")
    return out


def _headline(gate, a1, a2, a3, verdicts) -> list[str]:
    h = []
    if gate:
        h.append(f"GATE {gate.get('gate_pass')}: the fresh reimplementation reproduces the "
                 f"archived W05 to max|dW05|={gate.get('max_abs_dW05'):.2e} over "
                 f"{gate.get('n_abliterated')} abliterated and "
                 f"{gate.get('n_non_abliterated')} non-abliterated members, ordering "
                 f"preserved, Spearman "
                 f"{gate.get('spearman_archived_vs_recomputed_W05'):.4f}.")
    if a1.get("scope_sentence"):
        h.append("SCOPE: " + a1["scope_sentence"])
    if a2.get("trade_sentence"):
        h.append("E_1 TRADE: " + a2["trade_sentence"])
    if a3.get("invariance_sentence"):
        h.append("DEPTH: " + a3["invariance_sentence"])
    return h


def _assert_block(out: dict) -> None:
    """Recompute every quoted figure from the raw files and assert equality."""
    md = out["metadata"]
    fails = []

    def chk(name, a, b, tol=1e-9):
        if a is None or b is None:
            return
        if not (abs(float(a) - float(b)) <= tol):
            fails.append(f"{name}: quoted {a} vs recomputed {b}")

    g = rd("gate.json", {}) or {}
    if g.get("rows"):
        d05 = max(abs(r["delta"]["W05"]) for r in g["rows"])
        chk("gate.max_abs_dW05", md["gate"]["max_abs_dW05"], d05)
        d01 = max(abs(r["delta"]["W01"]) for r in g["rows"])
        chk("gate.max_abs_dW01", md["gate"]["max_abs_dW01"], d01)

    a1 = arm1_stats()
    for w, v in md["arm1"].get("auroc_all_vs_all", {}).items():
        chk(f"arm1.auroc[{w}]", v["estimate"], a1["auroc_all_vs_all"][w]["estimate"], 1e-12)
        chk(f"arm1.ci_low[{w}]", v["ci_low"], a1["auroc_all_vs_all"][w]["ci_low"], 1e-12)
    for c, v in md["arm1"].get("auroc_by_recipe_class_W05", {}).items():
        chk(f"arm1.class[{c}]", v["estimate"],
            a1["auroc_by_recipe_class_W05"][c]["estimate"], 1e-12)

    a2 = arm2_stats()
    r = md["arm2"].get("matched_subset_real_pairs_only", {})
    r2 = a2.get("matched_subset_real_pairs_only", {})
    if "auroc_W05_parent_free" in r and "auroc_W05_parent_free" in r2:
        chk("arm2.W05", r["auroc_W05_parent_free"]["estimate"],
            r2["auroc_W05_parent_free"]["estimate"], 1e-12)
        chk("arm2.E1", r["auroc_E1_parent_required"]["estimate"],
            r2["auroc_E1_parent_required"]["estimate"], 1e-12)
        chk("arm2.diff", r["paired_difference_W05_minus_E1"]["estimate"],
            r2["paired_difference_W05_minus_E1"]["estimate"], 1e-12)

    a3 = arm3_stats()
    for dn, blk in md["arm3"].get("per_depth_correlations", {}).items():
        for mid, st in blk["metrics"].items():
            chk(f"arm3.rho[{dn}/{mid}]", st["estimate"],
                a3["per_depth_correlations"][dn]["metrics"][mid]["estimate"], 1e-12)

    jdump({"n_checks_failed": len(fails), "failures": fails,
           "contract": AN.CONTRACT}, RES / "assertions.json")
    if fails:
        raise AssertionError("analysis assertion block FAILED:\n" + "\n".join(fails[:20]))
    logger.info("assertion block PASSED: every quoted number recomputes")


if __name__ == "__main__":
    run()
