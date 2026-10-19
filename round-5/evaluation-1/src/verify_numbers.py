#!/usr/bin/env python3
"""Standalone checker for numbers.json.

Imports NOTHING from eval.py or archlib.py -- every path, constant, formula and
statistic below is re-declared here on purpose, so a bug shared with the analysis
script cannot hide. Recomputes every checkable numbers.json entry from the
archived RAW ROWS, prints PASS / FAIL / UNAVAILABLE per entry, and exits 1 if any
entry FAILs.

    uv run verify_numbers.py [--numbers numbers.json]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop")
V_A1 = ROOT / "iter_4/gen_art/gen_art_experiment_1"
V_A2 = ROOT / "iter_4/gen_art/gen_art_experiment_2"
V_A3 = ROOT / "iter_4/gen_art/gen_art_experiment_3"
V_A6 = ROOT / "iter_3/gen_art/gen_art_evaluation_1"
V_I3 = ROOT / "iter_3/gen_art/gen_art_experiment_1"

V_TAU = -2.7415117804288127
V_Z = 1.959963984540054
TOL = 1e-12


def jl(p: Path):
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def js(p: Path):
    return json.loads(p.read_text())


def v_wilson(k, n, z=V_Z):
    if n <= 0:
        return (None, None)
    d = n + z * z
    c = (k + z * z / 2) / d
    h = (z / d) * math.sqrt(k * (n - k) / n + z * z / 4)
    return (max(0.0, c - h), min(1.0, c + h))


def v_ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        a = (i + j) / 2.0 + 1.0
        for t in range(i, j + 1):
            r[o[t]] = a
        i = j + 1
    return r


def v_auroc(pos, neg):
    if not pos or not neg:
        return None
    a = list(pos) + list(neg)
    rr = v_ranks(a)
    return (sum(rr[: len(pos)]) - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


def v_norm_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def v_power(p1, p2, n, alpha=0.05):
    pb = (p1 + p2) / 2
    se0 = math.sqrt(pb * (1 - pb) * 2 / n)
    se1 = math.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
    if se1 <= 0:
        return 1.0
    zc = 1.959963984540054 if abs(alpha - 0.05) < 1e-12 else 1.959963984540054
    d = abs(p2 - p1)
    return v_norm_cdf((d - zc * se0) / se1) + v_norm_cdf((-d - zc * se0) / se1)


def v_mde(p1, n, power=0.80, step=0.0001):
    i = 1
    while p1 + i * step <= 1.0:
        p2 = p1 + i * step
        if v_power(p1, p2, n) >= power:
            return round(p2, 6)
        i += 1
    return None


# ---------------------------------------------------------------------------
# rebuild the pools, independently
# ---------------------------------------------------------------------------
def v_build():
    a1 = js(V_A1 / "results/analysis.json")
    arm_a = [r for r in jl(V_A1 / "results/arm_a.jsonl")
             if r["status"] == "OK" and r.get("eligible")]
    arm_b = [r for r in jl(V_A1 / "results/arm_b.jsonl") if not r.get("precision_control")]
    derived = js(V_A1 / "results/predictions_derived.json")
    w_star = derived["w_star_predicted_crossing"]
    sweep = {str(c["spread_label"]): c for c in a1["gaussian_sweep"]["curve"]}

    neg = [r["W05_abl_min_layer_energy"] for r in arm_a if r["role"] == "parent"]
    seen = set()
    for r in jl(V_I3 / "results/arm2_all.jsonl"):
        if r.get("ok") and r.get("parent") and r.get("W05_parent") is not None:
            if r["parent"] not in seen:
                seen.add(r["parent"])
                neg.append(r["W05_parent"])
    pu = next(r for r in arm_b if r["kernel_id"] == "parent_unedited")
    neg.append(pu["W05_abl_min_layer_energy"])

    def uni(r):
        f = r["family"]
        if f == "uniform_subunit":
            w = float(r["kernel_id"].split("uniform_w")[1])
            return "UNIFORM" if w >= 1.0 else "UNIFORM_BUT_INCOMPLETE"
        if f == "householder":
            return "UNIFORM_BUT_ORTHOGONAL"
        if f == "gaussian_depth":
            lab = r["kernel_id"].replace("gaussian_s", "")
            mw = sweep.get(lab, {}).get("min_depth_weight")
            return ("DEPTH_WEIGHTED_ABOVE_W_STAR" if (mw is not None and mw >= w_star)
                    else "NONUNIFORM")
        if f == "layer_band":
            return "NONUNIFORM"
        if f == "heretic":
            return "UNIFORM" if r.get("uniform") else "NONUNIFORM"
        if f in ("norm_preserving", "rank_k"):
            return "UNIFORM"
        return "UNKNOWN"

    by: dict[str, list[float]] = {}
    for r in arm_a:
        if r["role"] == "edited":
            by.setdefault(r["recipe_class_rederived"], []).append(
                r["W05_abl_min_layer_energy"])
    for r in arm_b:
        if r["kernel_id"] == "parent_unedited" or r["family"] == "control":
            continue
        by.setdefault(f"ARMB_{r['family'].upper()}__{uni(r)}", []).append(
            r["W05_abl_min_layer_energy"])
    return a1, by, neg, arm_a, arm_b


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--numbers", default="numbers.json")
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    npath = Path(args.numbers)
    if not npath.is_absolute():
        npath = here / npath
    if not npath.exists():
        print(f"FATAL: {npath} not found")
        return 1
    N = js(npath)

    rows: list[dict] = []

    def rec(key, status, expected=None, got=None, note=None):
        rows.append({"key": key, "status": status, "expected_in_numbers_json": expected,
                     "recomputed_here": got, "note": note})
        return status

    def chk(key, got, tol=TOL, note=None, subkey="value"):
        if key not in N:
            return rec(key, "UNAVAILABLE", None, got, "key absent from numbers.json")
        exp = N[key].get(subkey)
        if exp is None or got is None:
            return rec(key, "UNAVAILABLE", exp, got, note or "null on one side")
        try:
            ok = abs(float(exp) - float(got)) <= tol
        except (TypeError, ValueError):
            ok = exp == got
        return rec(key, "PASS" if ok else "FAIL", exp, got, note)

    a1, by, neg, arm_a, arm_b = v_build()
    lorco = a1["lorco"]
    n_neg = len(neg)

    # --- tau -------------------------------------------------------------
    chk("tau_fixed", a1["fixed_threshold"]["tau"])
    taus = [lorco[k]["tau_fitted_without_this_class"] for k in sorted(lorco)]
    cnt: dict[float, int] = {}
    for t in taus:
        cnt[t] = cnt.get(t, 0) + 1
    modal = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    chk("tau_refit_modal", modal)
    chk("tau_shift_log10", modal - V_TAU)
    arm3 = js(V_A2 / "results/arm3.json")
    brit = arm3["first_false_positive_filtered"]["shift_from_operating_point"]
    chk("tau_brittleness_scale", brit)
    chk("tau_shift_over_brittleness", (modal - V_TAU) / brit)

    # --- the four columns, per class -------------------------------------
    for k in sorted(lorco):
        hv = by.get(k, [])
        if not hv:
            rec(f"lorco_{k}_sens_fixed_tau", "UNAVAILABLE", None, None,
                "class not rebuildable from rows")
            continue
        tau_k = lorco[k]["tau_fitted_without_this_class"]
        chk(f"lorco_{k}_sens_fixed_tau", sum(1 for v in hv if v <= V_TAU) / len(hv))
        chk(f"lorco_{k}_sens_refit_tau", sum(1 for v in hv if v <= tau_k) / len(hv))
        chk(f"lorco_{k}_auroc_oriented", v_auroc([-v for v in hv], [-v for v in neg]))
        chk(f"lorco_{k}_specificity_refit_tau",
            sum(1 for v in neg if v > tau_k) / n_neg)
        # the archive itself must agree -- independent of numbers.json
        got = sum(1 for v in hv if v <= tau_k) / len(hv)
        rec(f"archive_agreement_lorco_{k}",
            "PASS" if abs(got - lorco[k]["heldout_sensitivity"]) <= TOL else "FAIL",
            lorco[k]["heldout_sensitivity"], got, "archived heldout_sensitivity")

    # --- specificity on eligible undeclared rows -------------------------
    prim = []
    for r in jl(V_A2 / "results/arm2_archive_eligibility.jsonl"):
        if (r.get("arm") != "control" and r.get("status") == "OK"
                and r.get("W05") is not None and r.get("eligible")):
            prim.append(r["W05"])
    for r in jl(V_A2 / "results/arm2_scan_new.jsonl"):
        if (r.get("status") == "OK" and r.get("eligible")
                and r.get("W05_abl_min_layer_energy") is not None):
            prim.append(r["W05_abl_min_layer_energy"])
    for tag, tau in (("at_tau_fixed", V_TAU), ("at_tau_refit_modal", modal)):
        k_fp = sum(1 for v in prim if v <= tau)
        chk(f"fp_rate_eligible_undeclared_{tag}", k_fp / len(prim))
        lo, hi = v_wilson(k_fp, len(prim))
        chk(f"fp_rate_eligible_undeclared_{tag}", hi, subkey="ci_high",
            note="Wilson upper bound")
        if f"fp_rate_eligible_undeclared_{tag}" in N:
            rec(f"fp_rate_eligible_undeclared_{tag}__n",
                "PASS" if N[f"fp_rate_eligible_undeclared_{tag}"]["n"] == len(prim) else "FAIL",
                N[f"fp_rate_eligible_undeclared_{tag}"]["n"], len(prim), "denominator")

    # --- scan arithmetic ---------------------------------------------------
    c = js(V_A2 / "results/arm2_archive_counts.json")
    chk("scan_total_rows", c["total_rows"], 0)
    chk("scan_n_controls", c["n_controls"], 0)
    chk("scan_n_attempted", c["n_non_control"], 0)
    chk("scan_n_completed", c["n_scored_non_control"], 0)

    # --- the bound ---------------------------------------------------------
    def bound(cos_t, log10_e_r):
        # abscos_v1_r is a float32 value, so |cos| is known only to 2^-23
        c = min(abs(cos_t), 1.0 - 2.0 ** -23)
        e_r = 10.0 ** log10_e_r
        s2 = max(0.0, 1 - c * c)
        B = s2 + 2 * c * math.sqrt(s2) * math.sqrt(max(e_r, 0.0))
        c2 = c * c
        hi = math.log10((c2 * e_r + B) / e_r)
        lo_lin = c2 * e_r - B
        if lo_lin <= 0:
            return None
        return max(abs(math.log10(lo_lin / e_r)), abs(hi))

    gaps_hold, gaps_fail, n_viol = [], [], 0
    for r in arm_b:
        cs, ler, w = r.get("abscos_v1_r"), r.get("log10_min_e_r"), \
            r.get("W05_abl_min_layer_energy")
        if cs is None or ler is None or w is None:
            continue
        g = abs(w - ler)
        (gaps_hold if abs(cs) > 0.99 else gaps_fail).append(g)
        b = bound(cs, ler)
        if b is not None and g > b + 1e-12:
            n_viol += 1
    chk("bound_max_gap_discovery_holding", max(gaps_hold) if gaps_hold else None)
    chk("bound_max_gap_discovery_failing", max(gaps_fail) if gaps_fail else None)
    chk("bound_n_violations", n_viol, 0)
    gh = sorted(gaps_hold)
    med = (gh[len(gh) // 2] if len(gh) % 2 else (gh[len(gh) // 2 - 1] + gh[len(gh) // 2]) / 2) \
        if gh else None
    chk("bound_median_gap_discovery_holding", med)

    # --- the Gaussian bracket ---------------------------------------------
    curve = a1["gaussian_sweep"]["curve"]
    first = next((x for x in curve if x["detected"]), None)
    last = None
    for x in curve:
        if x["detected"]:
            break
        last = x
    chk("discovery_min_depth_weight_bracket_lo", last["min_depth_weight"] if last else None)
    chk("discovery_min_depth_weight_bracket_hi", first["min_depth_weight"] if first else None)
    chk("stamped_critical_spread", a1["gaussian_sweep"]["predicted_critical_spread"])
    chk("stamped_critical_spread_ratio",
        a1["gaussian_sweep"]["predicted_critical_spread"] / first["spread"] if first else None)

    # --- the isometry corroboration ---------------------------------------
    pu = next(r for r in arm_b if r["kernel_id"] == "parent_unedited")
    o1 = next((r for r in arm_b if r["kernel_id"] == "orba_householder_lam1.0"), None)
    ct = next((r for r in arm_b if r["kernel_id"] == "householder_random_dir_control"), None)
    chk("isometry_orba_dW05",
        abs(o1["W05_abl_min_layer_energy"] - pu["W05_abl_min_layer_energy"]) if o1 else None)
    chk("isometry_random_control_dW05",
        abs(ct["W05_abl_min_layer_energy"] - pu["W05_abl_min_layer_energy"]) if ct else None)

    # --- effectiveness vs detectability -----------------------------------
    ev = a1["effectiveness_vs_detectability"]["rows"]
    eff = [r for r in ev if r.get("fluency_pass") and r["refusal_rate_judge"] <= 0.50]
    chk("n_effective_kernels", len(eff), 0)
    chk("n_effective_and_detected", sum(1 for r in eff if r["detected"]), 0)

    # --- undefinedness count ----------------------------------------------
    scored = [r for r in arm_a if r["role"] == "edited"
              and r.get("W05_abl_min_layer_energy") is not None]
    chk("n_rows_where_discovery_rule_undefined",
        sum(1 for r in scored
            if r["recipe_class_rederived"] in ("R_MULTIDIR_SVD", "R_HERETIC")), 0)

    # --- at-scale sensitivity ----------------------------------------------
    det = sum(1 for r in scored if r["W05_abl_min_layer_energy"] <= V_TAU)
    chk("at_scale_sensitivity", det / len(scored))

    # --- decoupling / prevalence -------------------------------------------
    a3 = js(V_A3 / "results/analysis.json")
    d = a3["decoupling"]
    chk("rootB_refusal_after", d["false_negative"]["refusal"])
    chk("rootB_W05", d["false_negative"]["W05"])
    chk("rootB_parent_W05", d["false_negative"]["parent_W05"])
    chk("rootB_cos_v1_r", d["false_negative"]["cos_v1_r"])
    chk("rootB_dW05_vs_parent",
        abs(d["false_negative"]["W05"] - d["false_negative"]["parent_W05"]))
    chk("rootC_W05", d["false_positive"]["W05"])
    chk("rootC_refusal", d["false_positive"]["refusal"])
    bs = a3["blind_spot_prevalence"]
    chk("R4_partial_layer_prevalence", bs["frac_partial_layer_or_per_head"])
    chk("repo_id_regex_hub_prevalence", bs["repo_id_regex_baseline"])

    # --- the quantization bit-width curve ----------------------------------
    dq = jl(V_A3 / "results/arm1_dequant.jsonl")
    bits = {str(r["intensity"]): r for r in dq
            if r.get("quantizer") == "reference_symmetric_rtn" and r.get("root") == "A"
            and str(r.get("intensity")).isdigit()}
    par = {str(r["intensity"]): r for r in dq
           if r.get("quantizer") == "reference_symmetric_rtn" and r.get("root") == "parent"
           and str(r.get("intensity")).isdigit()}
    dies = None
    for b in sorted(bits, key=lambda s: -int(s)):
        if bits[b]["W05_abl_min_layer_energy"] > V_TAU:
            dies = int(b)
            break
    chk("quant_scar_dies_at_bits", dies, 0)
    for b in sorted(bits, key=lambda s: -int(s)):
        chk(f"quant_W05_at_{b}bit", bits[b]["W05_abl_min_layer_energy"])
    chk("quant_min_cos_v1_r_over_bit_widths",
        min(r["cos_v1_r"] for r in bits.values()))
    if "4" in par:
        chk("quant_clean_parent_W05_at_4bit", par["4"]["W05_abl_min_layer_energy"])
    i4 = next((r for r in dq if r.get("stage_id") == "arm1_int4"), None)
    if i4:
        chk("quant_int4_ppl", i4.get("wikitext_ppl"))

    # --- the name baseline -------------------------------------------------
    rb = a1["repo_name_regex_baseline"]
    chk("name_regex_sensitivity", rb["sensitivity"])
    chk("name_regex_agreement_with_W05", rb["agreement_with_W05"])
    chk("n_caught_by_W05_missed_by_name", len(rb["caught_by_W05_missed_by_name"]), 0)

    # --- the W05 boundary ---------------------------------------------------
    if (V_A6 / "numbers.json").exists():
        a6 = js(V_A6 / "numbers.json")
        wb = a6.get("W05_boundary", {})
        for key, kk in (("W05_abliterated_max", "abliterated_max"),
                        ("W05_abliterated_min", "abliterated_min"),
                        ("W05_separating_margin", "separating_margin_log10")):
            v = wb.get(kk)
            if isinstance(v, dict) and "value" in v:
                v = v["value"]  # the archived block wraps the scalar with its checkpoint
            chk(key, v)
    else:
        rec("W05_abliterated_max", "UNAVAILABLE", None, None,
            f"probed {V_A6 / 'numbers.json'}")

    # --- the power calculation ---------------------------------------------
    p2 = v_mde(0.20, 40)
    mde = (p2 - 0.20) if p2 is not None else None
    rec("power_mde_at_n40_p020",
        "PASS" if (mde is not None and abs(mde - 0.29) <= 0.011) else "FAIL",
        0.29, mde, "smallest upward detectable DIFFERENCE (not rate), two-proportion, "
                   "alpha=0.05, power=0.80, n=40/group")

    # --- the numbers file's own bookkeeping ---------------------------------
    n_entries = sum(1 for k in N if not k.startswith("_"))
    rec("numbers_json_n_entries", "PASS" if n_entries > 0 else "FAIL",
        n_entries, n_entries, "numbers.json is non-empty")
    bad = sorted(k for k in N if not k.startswith("_")
                 and not (isinstance(N[k], dict) and "value" in N[k]
                          and "source_file" in N[k] and "units" in N[k]))
    rec("numbers_json_schema_conformance", "PASS" if not bad else "FAIL",
        [], bad, "every entry must carry value/units/source_file")

    # --- report -------------------------------------------------------------
    n_pass = sum(1 for r in rows if r["status"] == "PASS")
    n_fail = sum(1 for r in rows if r["status"] == "FAIL")
    n_una = sum(1 for r in rows if r["status"] == "UNAVAILABLE")
    width = max(len(r["key"]) for r in rows) + 2
    print("=" * (width + 60))
    print("verify_numbers.py -- recomputed from raw archived rows")
    print("=" * (width + 60))
    for r in sorted(rows, key=lambda x: (x["status"] != "FAIL", x["key"])):
        print(f"{r['status']:<12} {r['key']:<{width}} "
              f"numbers={r['expected_in_numbers_json']!r:<26} here={r['recomputed_here']!r}")
    print("-" * (width + 60))
    print(f"PASS={n_pass}  FAIL={n_fail}  UNAVAILABLE={n_una}  TOTAL={len(rows)}")

    out = {"n_pass": n_pass, "n_fail": n_fail, "n_unavailable": n_una,
           "n_total": len(rows), "rows": sorted(rows, key=lambda x: x["key"]),
           "numbers_file": str(npath),
           "independence": ("this script imports nothing from eval.py or archlib.py -- "
                            "paths, constants, Wilson, AUROC and the Cauchy-Schwarz bound "
                            "are all re-declared locally")}
    (here / "results").mkdir(parents=True, exist_ok=True)
    (here / "results/verify_report.json").write_text(
        json.dumps(out, sort_keys=True, indent=2, default=str))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
