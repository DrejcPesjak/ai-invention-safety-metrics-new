#!/usr/bin/env python3
"""Specificity-matched thresholds from the negatives, then the verdict on the positive.
Threshold rule copied verbatim from round-5/experiment-1/src/analysis.py::spec_matched_threshold
(0 FP allowed): the most permissive cutoff that excludes every negative, i.e. nextafter(min(neg), -inf)."""
import argparse, json, math
from pathlib import Path
import numpy as np

R = Path(__file__).resolve().parent / "results"
TAU_ARCHIVED = -2.7415  # pre-registered pooled threshold from the paper (sub-4.2B panel)

def spec_matched_threshold(neg_vals, n_allowed_fp=0):
    v = sorted(x for x in neg_vals if x is not None and math.isfinite(x))
    if not v: return float("-inf")
    if n_allowed_fp >= len(v): return float("inf")
    return float(np.nextafter(v[n_allowed_fp], -np.inf))

def stats(r):
    out = {"W05": r["W05"]}
    for k, w in r["windowed"].items():
        out[f"W05w_k{k}"] = w["W05w"]; out[f"c_k{k}"] = w["consistency_c"]
    return out

ap = argparse.ArgumentParser(); ap.add_argument("--negatives", nargs="+", required=True)
ap.add_argument("--positive"); ap.add_argument("--out", required=True); a = ap.parse_args()
negs = {n: json.load(open(R / f"{n}.json")) for n in a.negatives}
out = {"negatives": {n: stats(r) for n, r in negs.items()}, "thresholds": {}}
for key in ["W05", "W05w_k2", "W05w_k4"]:
    vals = [out["negatives"][n].get(key) for n in negs]
    out["thresholds"][key] = {"tau_0fp": spec_matched_threshold(vals), "neg_values": vals}
out["thresholds"]["W05_archived_tau"] = TAU_ARCHIVED
if a.positive:
    p = json.load(open(R / f"{a.positive}.json")); ps = stats(p)
    out["positive"] = {"name": a.positive, **ps, "verdict": {}}
    for key in ["W05", "W05w_k2", "W05w_k4"]:
        tau = out["thresholds"][key]["tau_0fp"]
        out["positive"]["verdict"][key] = {"value": ps[key], "threshold": tau, "fires": bool(ps[key] < tau),
                                           "margin_log10": ps[key] - tau}
    out["positive"]["verdict"]["W05_vs_archived_tau"] = bool(ps["W05"] < TAU_ARCHIVED)
    # per-window profile for k=2, compact
    out["positive"]["k2_profile"] = [(w["win_start"], round(w["log10_e_min"], 3),
                                      None if w["cos_to_prev_v1"] is None else round(w["cos_to_prev_v1"], 3),
                                      w["argmin_matrix"]) for w in p["windowed"]["2"]["windows"]]
json.dump(out, open(a.out, "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "negatives"}, indent=1)[:3000])
