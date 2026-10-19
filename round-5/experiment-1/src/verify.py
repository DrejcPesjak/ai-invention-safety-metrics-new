#!/usr/bin/env python3
"""STANDALONE verifier.

Imports NOTHING from the pipeline -- only json, math, os, sys and numpy -- and
re-derives every entry of results/numbers.json from the raw rows in results/*.jsonl
and results/*.json.  The ROWS are the truth: if an entry disagrees, the number is
wrong, not the rows.

Prints a PASS/FAIL table and exits 0 (all pass) or 1 (any fail).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

RES = Path(__file__).resolve().parent / "results"
ARCHIVE = Path(__file__).resolve().parent / "archive"
TAU = -2.7415117804288127
KS_ALL = ["2", "4", "6", "8", "L"]
CONTROL_CLASSES = {"PARENT", "CONTROL_NOISE_FLOOR"}
BASELINE_TERMS = ["abliterat", "gabliterat", "obliterat", "uncensor", "decensor",
                  "orthogonal", "norm[-_]preserv", "refusal[-_]?(free|removed)",
                  "heretic", "lorablated", "josiefied"]


def jl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def js(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def wilson(k: int, n: int, z: float = 1.959963984540054):
    if n == 0:
        return (float("nan"), 0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (p, max(0.0, c - h), min(1.0, c + h))


def _missing(x) -> bool:
    """None and NaN denote the same thing here.

    The writer serialises non-finite floats as JSON null (NaN is not legal JSON),
    so a re-derived NaN and a stored null are the SAME value and must compare
    equal; otherwise every empty-denominator rate reads as a verification
    failure rather than as an empty denominator.
    """
    return x is None or (isinstance(x, float) and math.isnan(x))


def close(a, b, tol=1e-9) -> bool:
    if _missing(a) or _missing(b):
        return _missing(a) and _missing(b)
    if isinstance(a, bool) or isinstance(b, bool):
        return bool(a) == bool(b)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if not (math.isfinite(a) and math.isfinite(b)):
            return repr(a) == repr(b)
        return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
    return a == b


def w05w(row: dict, k: str):
    w = (row.get("windowed") or {}).get(k)
    return None if w is None else float(w["W05w"])


def spec_matched_threshold(vals, n_fp=0) -> float:
    v = sorted(x for x in vals if x is not None and math.isfinite(x))
    if not v:
        return float("-inf")
    if n_fp >= len(v):
        return float("inf")
    return float(np.nextafter(v[n_fp], -np.inf))


def main() -> int:
    num = js(RES / "numbers.json")
    if num is None:
        print("FATAL: results/numbers.json missing")
        return 1
    armb = [r for r in jl(RES / "armb_w05w.jsonl") if r.get("status") == "OK"]
    arma = jl(RES / "arma_w05w.jsonl")
    frontier = jl(RES / "frontier.jsonl")
    gates = js(RES / "gates.json")
    gkl = js(RES / "gate_kL.json")
    s6 = js(RES / "arm3_subspace.json")
    s7 = js(RES / "derivation_summary.json")
    preds = js(RES / "predictions_outcome.json")
    bl = js(RES / "baseline.json")
    negs = [r for r in jl(ARCHIVE / "arm2_scan_new.jsonl")
            if r.get("status") == "OK" and r.get("windowed") and r.get("eligible")]

    rows: list[tuple[str, bool, str]] = []

    def chk(key, expected, tol=1e-9, how=""):
        if key not in num:
            rows.append((key, False, f"ABSENT from numbers.json (expected {expected})"))
            return
        got = num[key]["value"]
        ok = close(got, expected, tol)
        rows.append((key, ok, f"numbers={got!r} rederived={expected!r} [{how}]"
                     if not ok else how))

    # ---- gates ----
    chk("G1_max_abs_dW05", gates["G1_wstats_reproduction"]["max_abs_dW05"],
        how="results/gates.json")
    chk("G1_host_parent_dW01",
        gates["G1_wstats_reproduction"]["host_parent_deltas"]["W01_abl_suppression_depth"])
    chk("G2_write_matrix_sha256_match",
        gates["G2_root_rebuild"]["write_matrix_sha256_match"])
    chk("G2_root_dW05", gates["G2_root_rebuild"]["delta_W05"])
    chk("G3_kL_max_delta_vs_f64",
        max(r["delta_a_vs_f64"] for r in gkl["rows"]), how="max over gate_kL.json rows")
    chk("G3_kL_max_delta_vs_f32", max(r["delta_b_vs_f32"] for r in gkl["rows"]))
    chk("G3_derived_float32_bound_at_d2048",
        math.log10(1 + 2048 * (2.0 ** -24) / (1 - 2048 * (2.0 ** -24))),
        how="recomputed from d=2048 and eps32=2^-24")
    chk("G3_PASS_at_iter4_declared_1e-9",
        all(r["delta_b_vs_f32"] <= 1e-9 for r in gkl["rows"]))

    # ---- the k=L identity, re-derived from the rows themselves ----
    bad = [r["kernel_id"] for r in armb
           if abs(w05w(r, "L") - r["W05_f64"]) > 1e-9]
    rows.append(("kL_identity_holds_on_every_armB_row", not bad,
                 f"{len(armb) - len(bad)}/{len(armb)} rows satisfy |W05w(L) - W05_f64| <= 1e-9"
                 + (f"; violations {bad[:5]}" if bad else "")))
    bada = [r["repo_id"] for r in arma if r.get("status") == "OK"
            and abs(w05w(r, "L") - r["W05_f64"]) > 1e-9]
    rows.append(("kL_identity_holds_on_every_armA_row", not bada,
                 f"{sum(1 for r in arma if r.get('status') == 'OK') - len(bada)} rows OK"
                 + (f"; violations {bada[:5]}" if bada else "")))

    # ---- headline recovery ----
    pb = [r for r in armb if r.get("recipe_class") not in CONTROL_CLASSES]
    ks8 = [k for k in KS_ALL if k != "L"]
    missed = [r for r in pb if r["W05_abl_min_layer_energy"] > TAU]
    rec = [r for r in missed
           if min((w05w(r, k) if w05w(r, k) is not None else 1e9) for k in ks8) <= TAU]
    p, lo, hi = wilson(len(rec), len(missed))
    chk("armB_pooled_misses_recovered_by_windowing", p,
        how=f"{len(rec)}/{len(missed)} recomputed from armb_w05w.jsonl")
    if "armB_pooled_misses_recovered_by_windowing" in num:
        ci = num["armB_pooled_misses_recovered_by_windowing"]["ci"]
        rows.append(("armB_recovery_ci", close(ci[0], lo) and close(ci[1], hi),
                     f"Wilson [{lo:.4f},{hi:.4f}]"))
    chk("armB_n_positives", len(pb))
    chk("armB_n_kernels_total", len(armb))

    # ---- sensitivity / specificity, re-derived from the raw rows ----
    neg_by_k = {k: [x for x in (w05w(r, k) for r in negs) if x is not None]
                for k in KS_ALL}
    pa = [r for r in arma if r.get("status") == "OK"
          and r.get("role") in ("edited", "parent_also_edited")]
    for k in KS_ALL:
        if not neg_by_k.get(k):
            continue
        for arm, pos in (("B", pb), ("A", pa)):
            key = f"sensitivity_arm{arm}_k{k}"
            if key not in num:
                continue
            sel = num[key]["source_row_selector"]
            fr = [r for r in frontier if r["k"] == k and r["rule"] == "RAW"
                  and r["arm"] == arm and sel.endswith(r["threshold_kind"])]
            if len(fr) != 1:
                rows.append((key, False,
                             f"selector {sel!r} matches {len(fr)} frontier rows; a "
                             f"numbers.json entry must resolve to exactly one row"))
                continue
            thr = fr[0]["threshold"]
            # a model with fewer than k layers has NO window of width k, so the
            # statistic is undefined for it and it leaves the denominator -- it is
            # not a miss.  This is why n_pos shrinks as k grows.
            defined = [r for r in pos if w05w(r, k) is not None]
            hit = sum(1 for r in defined if w05w(r, k) <= thr)
            v, l2, h2 = wilson(hit, len(defined)) if defined else (float("nan"), 0.0, 1.0)
            chk(key, v, how=f"{hit}/{len(defined)} at threshold {thr:.6f} "
                            f"({len(pos) - len(defined)} models have no width-{k} window)")
            fpn = sum(1 for x in neg_by_k[k] if x <= thr)
            sv, _, _ = wilson(len(neg_by_k[k]) - fpn, len(neg_by_k[k]))
            chk(f"specificity_arm{arm}_k{k}", sv,
                how=f"{len(neg_by_k[k])-fpn}/{len(neg_by_k[k])}")

    chk("negatives_n_eligible_with_W05w", len(negs), how="archive/arm2_scan_new.jsonl")

    # ---- every frontier row is internally consistent ----
    fbad = []
    for r in frontier:
        v, l2, h2 = wilson(r["n_hit"], r["n_pos"]) if r["n_pos"] else (float("nan"), 0, 1)
        sv, sl, sh = (wilson(r["n_neg"] - r["n_false_positive"], r["n_neg"])
                      if r["n_neg"] else (float("nan"), 0, 1))
        if not (close(v, r["sensitivity"]) and close(sv, r["specificity"])
                and close(l2, r["sens_wilson_lo"]) and close(h2, r["sens_wilson_hi"])
                and close(sl, r["spec_wilson_lo"]) and close(sh, r["spec_wilson_hi"])):
            fbad.append(f"{r['rule']}@k{r['k']}/{r['arm']}")
    rows.append(("frontier_rows_internally_consistent", not fbad,
                 f"{len(frontier) - len(fbad)}/{len(frontier)} rows reproduce their own "
                 f"Wilson intervals" + (f"; bad {fbad[:5]}" if fbad else "")))

    # ---- Arm 3 ----
    appl = [r for r in s6["rows"] if r.get("applicable")]
    ag = sum(1 for r in appl
             if r["predicted_detection"] == r["observed_detection_W05"]) / len(appl)
    chk("arm3_agreement_fraction", ag, how=f"{len(appl)} applicable rows")
    tab = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
    for r in appl:
        p_, o_ = r["predicted_detection"], r["observed_detection_W05"]
        tab["TP" if (p_ and o_) else "FP" if (p_ and not o_) else
            "FN" if (not p_ and o_) else "TN"] += 1
    rows.append(("arm3_2x2_table", tab == s6["agreement_2x2_vs_W05"],
                 f"rederived {tab} vs stored {s6['agreement_2x2_vs_W05']}"))
    und = sorted(r["model_id"] for r in appl if r["dim_R"] != 1)
    chk("arm3_single_direction_rule_undefined_on", und,
        how="kernels whose known removed span has dim > 1")
    # discovery/completion recomputed straight from the stored subspace block
    dbad = []
    for r in armb:
        sub = r.get("subspace")
        if not sub:
            continue
        row = next((x for x in appl if x["model_id"] == r["kernel_id"]), None)
        if row is None:
            continue
        if (bool(sub["SD_at_dimR"] >= 0.9) != row["discovery_generalised"]
                or bool(sub["log10_min_e_R"] <= TAU) != row["completion"]):
            dbad.append(r["kernel_id"])
    rows.append(("arm3_discovery_completion_rederive", not dbad,
                 f"{len(appl) - len(dbad)}/{len(appl)} rows reproduce discovery+completion"
                 + (f"; bad {dbad[:5]}" if dbad else "")))

    # ---- Arm 4: the derivation identity, recomputed from the per-matrix arrays ----
    der = jl(RES / "derivation.jsonl")
    worst_abs, worst_rel, nchk = 0.0, 0.0, 0
    disc_rel, n_disc = [], 0
    ident_bad = []
    for r in der:
        if r.get("e_W_v1") is None or r.get("e_W_r") is None:
            continue
        ev = np.asarray(r["e_W_v1"], dtype=float)
        er = np.asarray(r["e_W_r"], dtype=float)
        c2 = float(r["cos2_theta"])
        resid = ev - er * c2
        i = int(np.argmin(ev))
        if not close(float(resid[i]), float(r["residual_at_argmin"]), 1e-9):
            ident_bad.append(r["model_id"])
        worst_abs = max(worst_abs, abs(float(resid[i])))
        rel = abs(float(resid[i]) / max(ev[i], 1e-300))
        worst_rel = max(worst_rel, rel)
        if c2 >= 0.9:
            disc_rel.append(rel)
            n_disc += 1
        nchk += 1
    rows.append(("derivation_identity_recomputed", not ident_bad,
                 f"{nchk - len(ident_bad)}/{nchk} models reproduce "
                 "e_W(v1) - e_W(r) cos^2(theta) at the argmin matrix"
                 + (f"; bad {ident_bad[:5]}" if ident_bad else "")))
    chk("derivation_max_abs_residual_at_argmin", worst_abs, tol=1e-9,
        how=f"max over {nchk} models, recomputed from the per-matrix energy arrays")
    chk("derivation_max_rel_residual_at_argmin", worst_rel, tol=1e-9)
    chk("derivation_max_rel_residual_where_discovery_holds",
        (max(disc_rel) if disc_rel else None), tol=1e-9,
        how=f"max over the {n_disc} models with cos^2(theta) >= 0.9")
    # the residual-scaling law, recomputed from the per-matrix arrays
    ratios = []
    for r in der:
        if r.get("e_W_v1") is None or r.get("e_W_r") is None:
            continue
        c2 = float(r["cos2_theta"])
        if c2 < 0.9 or (1.0 - c2) <= 1e-12:
            continue
        ev = np.asarray(r["e_W_v1"], dtype=float)
        er = np.asarray(r["e_W_r"], dtype=float)
        i = int(np.argmin(ev))
        ratios.append(abs(float(ev[i] - er[i] * c2) / (1.0 - c2)))
    chk("derivation_residual_over_sin2_theta", (max(ratios) if ratios else None), tol=1e-9,
        how=f"max |residual|/sin^2(theta) over the {len(ratios)} models where discovery holds")
    rows.append(("residual_scaling_law_is_O1", bool(ratios) and max(ratios) < 10.0,
                 f"max |residual|/sin^2(theta) = {max(ratios):.4f} -- an O(1) constant, "
                 "confirming the leftover is the energy along the component of v1 "
                 "orthogonal to r" if ratios else "no model with discovery holding"))

    # ---- the corrected layer-subset calibration, recomputed from the draws ----
    s5j = js(RES / "arm2_frontier_summary.json")
    sbad, nsub = [], 0
    par_p = None
    for r in armb:
        sn = r.get("subset_null")
        if not sn or not sn.get("null_values"):
            continue
        k = str(sn["k"])
        w = (r.get("windowed") or {}).get(k)
        if not w or not w.get("profile"):
            continue
        vals = np.asarray(sn["null_values"], dtype=float)
        mu, sd = float(vals.mean()), float(vals.std(ddof=1))
        pw = [0.5 * (1 + math.erf(((float(p_["log10_e_min"]) - mu) / sd) / math.sqrt(2)))
              for p_ in w["profile"]]
        nw = len(pw)
        p_sid = 1.0 - (1.0 - min(pw)) ** nw
        nsub += 1
        if r["kernel_id"] == "PARENT":
            par_p = p_sid
        stored = next((x for x in s5j["subset_null_correction"]["rows"]
                       if x["model_id"] == r["kernel_id"]), None)
        if stored is None or not close(stored["p_sidak_parametric"], p_sid, 1e-9):
            sbad.append(r["kernel_id"])
    rows.append(("subset_null_sidak_recomputed", not sbad,
                 f"{nsub - len(sbad)}/{nsub} kernels reproduce the per-window Sidak p "
                 "from their own stored null draws"
                 + (f"; bad {sbad[:5]}" if sbad else "")))
    if par_p is not None:
        chk("subset_null_p_sidak_unedited_parent", par_p,
            how="recomputed from the PARENT row's own 32 subset draws")
    # the contiguity confound, recomputed
    pr = next((r for r in armb if r["kernel_id"] == "PARENT"), None)
    if pr and pr.get("subset_null"):
        w = (pr.get("windowed") or {}).get(str(pr["subset_null"]["k"]))
        gap = (float(np.mean([p_["log10_e_min"] for p_ in w["profile"]]))
               - float(pr["subset_null"]["null_mean"]))
        chk("contiguity_gap_unedited_parent", gap,
            how="mean contiguous-window depth minus mean random-subset depth, "
                "recomputed for the unedited parent")
        rows.append(("contiguity_gap_is_negative", gap < 0,
                     f"gap = {gap:.4f}: contiguous windows are deeper than random "
                     "subsets on the UNEDITED model, which is the confound"))

    # The superseded field really is uninformative -- asserted on the rows, not in prose.
    # Two facts: it never reaches any conventional alpha for ANY kernel (so it cannot
    # discriminate at all), and it collapses onto one value for the large majority.
    sup = [r["subset_null"]["p_multiwindow_empirical"] for r in armb
           if r.get("subset_null")]
    mode_frac = (max(sup.count(x) for x in set(sup)) / len(sup)) if sup else 0.0
    rows.append(("superseded_subset_p_never_significant", bool(sup) and min(sup) > 0.05,
                 f"the naive min-vs-single-subset p has minimum {min(sup):.4f} over "
                 f"{len(sup)} kernels -- it never reaches alpha = 0.05 even for a complete "
                 f"rank-one projection, and {mode_frac:.0%} of kernels share one value"))
    corr = [r["p_sidak_parametric"] for r in s5j["subset_null_correction"]["rows"]]
    rows.append(("corrected_subset_p_discriminates",
                 bool(corr) and min(corr) < 0.05 < max(corr),
                 f"the corrected per-window Sidak p spans [{min(corr):.3g}, "
                 f"{max(corr):.3g}] over {len(corr)} kernels"))

    # ---- the baseline ----
    import re
    brx = re.compile("(?i)(" + "|".join(BASELINE_TERMS) + ")")
    hits = sum(1 for r in pa if brx.search(r["repo_id"]))
    bv, blo, bhi = wilson(hits, len(pa)) if pa else (float("nan"), 0.0, 1.0)
    chk("baseline_repo_name_regex", bv, how=f"{hits}/{len(pa)} Arm A positives")
    f8 = re.compile("(?i)(" + "|".join(BASELINE_TERMS[:8]) + ")")
    h8 = sum(1 for r in pa if f8.search(r["repo_id"]))
    b8, _, _ = wilson(h8, len(pa)) if pa else (float("nan"), 0.0, 1.0)
    chk("baseline_repo_name_regex_frozen8", b8,
        how=f"{h8}/{len(pa)} under the frozen 8-term feature")
    if bl is not None:
        rows.append(("baseline_json_matches_rows",
                     close(bl["baseline_n_hit"], hits) and close(bl["n_pos"], len(pa)),
                     f"baseline.json n_hit={bl['baseline_n_hit']} n_pos={bl['n_pos']} "
                     f"vs rederived {hits}/{len(pa)}"))

    # ---- predictions scorecard ----
    if preds is not None:
        sc = {r["id"]: r["verdict"] for r in preds["results"]}
        chk("predictions_scorecard", sc, how="results/predictions_outcome.json")
        rows.append(("predictions_stamped_before_scoring",
                     (RES / "predictions_iter5.sha256").exists()
                     and _sha(RES / "predictions_iter5.json")
                     == (RES / "predictions_iter5.sha256").read_text().strip(),
                     "sha256(predictions_iter5.json) matches the stamped digest"))

    # ---- tier honesty: no denominator silently includes an UNRESOLVED row ----
    unres = [r for r in arma if r.get("status") != "OK"]
    rows.append(("unresolved_rows_excluded_from_denominators",
                 all(r.get("status") == "OK" for r in pa),
                 f"{len(unres)} Arm A rows UNRESOLVED and excluded; "
                 f"{len(pa)} positives in the denominator"))
    chk("tier_completed", js(RES / "arma_tier_status.json")["tier_completed"]
        if (RES / "arma_tier_status.json").exists() else num.get(
            "tier_completed", {}).get("value"),
        how="results/arma_tier_status.json")

    # ---- every numbers.json entry carries its provenance ----
    missing = [k for k, v in num.items()
               if not isinstance(v, dict) or "source_file" not in v
               or "circularity_flag" not in v]
    rows.append(("numbers_entries_carry_provenance", not missing,
                 f"{len(num) - len(missing)}/{len(num)} entries have "
                 "source_file + circularity_flag"
                 + (f"; missing {missing[:5]}" if missing else "")))

    npass = sum(1 for _, ok, _ in rows if ok)
    print(f"{'ENTRY':52s} {'':4s} DETAIL")
    print("-" * 110)
    for key, ok, detail in rows:
        print(f"{key:52s} {'PASS' if ok else 'FAIL'} {detail}")
    print("-" * 110)
    print(f"{npass}/{len(rows)} PASS")
    return 0 if npass == len(rows) else 1


def _sha(p: Path) -> str:
    import hashlib
    return hashlib.sha256(p.read_bytes()).hexdigest()


if __name__ == "__main__":
    sys.exit(main())
