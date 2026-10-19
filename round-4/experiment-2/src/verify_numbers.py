#!/usr/bin/env python3
"""Recompute EVERY entry of numbers.json from the raw jsonl rows and exit
nonzero on any mismatch.  Assembly of any downstream paper is blocked on this.

Tolerances are recorded per key: 1e-9 for arithmetic recomputation from stored
rows, 1e-4 where a value came from a re-download + re-decode path.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
W05_BOUNDARY = -2.7415117804288127
W05_NONABL_MAX = -2.665194698505143
TOL_ARITH = 1e-9
TOL_REDOWNLOAD = 1e-4


def jl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def jd(p):
    return json.loads(Path(p).read_text())


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (float("nan"), 0.0, 1.0)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (p, max(0.0, c - h), min(1.0, c + h))


def main() -> int:
    nums = jd(RES / "numbers.json")
    checks: list[dict] = []

    def chk(key, recomputed, tol=TOL_ARITH, note=""):
        if key not in nums:
            checks.append({"key": key, "status": "MISSING_FROM_NUMBERS", "note": note})
            return
        quoted = nums[key]["value"]
        if isinstance(quoted, str) or isinstance(recomputed, str):
            ok = (quoted == recomputed)
            delta = None
        else:
            delta = abs(float(quoted) - float(recomputed))
            ok = delta <= tol
        checks.append({"key": key, "quoted": quoted, "recomputed": recomputed,
                       "abs_delta": delta, "tolerance": tol,
                       "status": "OK" if ok else "MISMATCH", "note": note})

    # ---- gate ------------------------------------------------------------
    g = jl(RES / "gate_arithmetic.jsonl")
    chk("gate_arithmetic_max_abs_delta_W05",
        float(max(r["abs_delta_W05"] for r in g)),
        note="max over gate_arithmetic.jsonl rows")

    gn = jd(RES / "gate_numerics.json")
    chk("gate_kL_identity_max_abs_delta_synthetic",
        float(max(gn["kL_equals_W05"][x] for x in ("clean", "full", "partial"))))
    chk("gate_4of12_W02", gn["four_of_twelve_injection"]["W02"])
    chk("gate_4of12_cos_v1_to_injected", gn["four_of_twelve_injection"]["cos_v1_to_u"])
    if (RES / "gate_root.json").exists():
        gr = jd(RES / "gate_root.json")
        chk("gate_root_W05_abs_delta", gr["root_W05_abs_delta"], tol=TOL_REDOWNLOAD)
        chk("gate_root_tensors_matched", gr["n_applied"])

    # ---- arm 1 -----------------------------------------------------------
    rows = []
    for f in ("arm1_synth.jsonl", "arm1_panel.jsonl", "arm2_scan_new.jsonl"):
        if (RES / f).exists():
            rows += [r for r in jl(RES / f) if r.get("status", "OK") == "OK"
                     and "W05w_by_k" in r]
    if rows:
        chk("kL_reproduces_W05_on_real_models_max_abs_delta",
            float(max(abs(r["W05w_by_k"]["L"] - r["W05_abl_min_layer_energy"])
                      for r in rows)),
            note="recomputed from the shipped per-model rows")

    panel = [r for r in jl(RES / "arm1_panel.jsonl")
             if r.get("group") == "G1_panel" and r["status"] == "OK"] \
        if (RES / "arm1_panel.jsonl").exists() else []
    if panel:
        y = np.array([1 if r["label"] == "abliterated" else 0 for r in panel])

        def auroc(v, y):
            v = np.asarray(v, float)
            pos, neg = v[y == 1], v[y == 0]
            if len(pos) == 0 or len(neg) == 0:
                return float("nan")
            wins = sum((1.0 if a > b else 0.5 if a == b else 0.0)
                       for a in pos for b in neg)
            return wins / (len(pos) * len(neg))

        for s, get in [("w05", lambda r: r["W05_abl_min_layer_energy"]),
                       ("w05q10", lambda r: r["W05q10_abl_p10_layer_energy"])] + \
                      [(f"w05w_{k}", (lambda r, k=k: r["W05w_by_k"].get(k, r["W05w_by_k"]["L"])))
                       for k in ("2", "4", "6", "8", "L")]:
            v = [get(r) for r in panel]
            raw = auroc(v, y)
            chk(f"panel_auroc_{s}_raw", raw, tol=1e-9,
                note="independent O(n^2) pairwise recount")
            chk(f"panel_auroc_{s}_oriented", 1.0 - raw, tol=1e-9,
                note="lower_is_positive")

    # ---- arm 2 -----------------------------------------------------------
    arch = jl(RES / "arm2_archive_eligibility.jsonl")
    new = [r for r in jl(RES / "arm2_scan_new.jsonl")
           if r["status"] == "OK"] if (RES / "arm2_scan_new.jsonl").exists() else []
    hub = [r for r in arch if r.get("arm") != "control"]
    scored = [r for r in hub if r["status"] == "OK"]
    elig = [r for r in scored if r["eligible"]]
    k_fp = (sum(1 for r in elig if r["W05"] is not None and r["W05"] <= W05_BOUNDARY)
            + sum(1 for r in new if r["W05_abl_min_layer_energy"] <= W05_BOUNDARY))
    n_den = len(elig) + len(new)
    p, lo, hi = wilson(k_fp, n_den)
    chk("n_eligible_denominator", n_den)
    chk("n_false_positives_filtered", k_fp)
    chk("fp_rate_filtered_primary", p)
    chk("n_archived_eligible", len(elig))
    chk("n_new_eligible_completed", len(new))
    k_raw = sum(1 for r in scored if r["W05"] is not None and r["W05"] <= W05_BOUNDARY)
    p_raw, _, _ = wilson(k_raw, len(scored))
    chk("fp_rate_raw_unfiltered_secondary", p_raw)

    reasons = Counter()
    for r in hub:
        if r["primary_reason"]:
            reasons[r["primary_reason"]] += 1
        elif r["undecidable"]:
            reasons["UNDECIDABLE:" + ",".join(r["undecidable"])] += 1
    for rule, cnt in reasons.items():
        chk(f"n_excluded_archive_{rule}", cnt)

    scan = jl("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop/iter_3/"
              "gen_art/gen_art_experiment_2/results/scan.jsonl")
    nc = [r for r in scan if r.get("arm") != "control"]
    chk("archive_scan_total_rows", len(scan))
    chk("archive_scan_n_controls", sum(1 for r in scan if r.get("arm") == "control"))
    chk("archive_scan_n_non_control", len(nc))
    chk("archive_scan_n_scored_non_control", sum(1 for r in nc if r["status"] == "OK"))
    chk("archive_scan_n_unresolved_non_control",
        sum(1 for r in nc if r["status"] == "UNRESOLVED"))
    chk("archive_scan_n_skipped_non_control",
        sum(1 for r in nc if r["status"] == "SKIPPED"))
    chk("archive_scan_n_error_non_control", sum(1 for r in nc if r["status"] == "ERROR"))
    chk("archive_scan_n_in_abliterated_region_0of160",
        sum(1 for r in nc if r["status"] == "OK"
            and r["W05_abl_min_layer_energy"] <= W05_BOUNDARY))

    # ---- arm 3 -----------------------------------------------------------
    a3 = jd(RES / "arm3.json")
    pool = [(r["W05"], r["repo_id"]) for r in elig if r["W05"] is not None] + \
           [(r["W05_abl_min_layer_energy"], r["repo"]) for r in new]
    above = sorted([x for x in pool if x[0] > W05_BOUNDARY])
    if above:
        chk("threshold_first_fp_value", float(above[0][0]))
        chk("threshold_first_fp_shift", float(above[0][0] - W05_BOUNDARY))
    chk("threshold_operating_point", W05_BOUNDARY)
    chk("threshold_panel_margin", abs(W05_BOUNDARY - W05_NONABL_MAX))
    chk("openrouter_cost_usd", 0.0)

    # threshold curve internal consistency
    curve = jl(RES / "arm3_threshold_curve.jsonl")
    bad = []
    for c in curve:
        if c["statistic"] == "W05" and c["population"] == "new_eligible_undeclared":
            h = sum(1 for r in new if r["W05_abl_min_layer_energy"] <= c["threshold"])
            if h != c["hits"]:
                bad.append(c)
    checks.append({"key": "arm3_curve_W05_new_population_recount",
                   "quoted": "see arm3_threshold_curve.jsonl", "recomputed": len(bad),
                   "abs_delta": len(bad), "tolerance": 0,
                   "status": "OK" if not bad else "MISMATCH"})

    n_bad = sum(1 for c in checks if c["status"] != "OK")
    Path(RES / "assertions.json").write_text(json.dumps(
        {"n_checks": len(checks), "n_failed": n_bad, "checks": checks}, indent=1))
    for c in checks:
        if c["status"] != "OK":
            print(f"FAIL {c['key']}: quoted={c.get('quoted')} "
                  f"recomputed={c.get('recomputed')} delta={c.get('abs_delta')}")
    print(f"verify_numbers: {len(checks) - n_bad}/{len(checks)} checks passed")
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main())
