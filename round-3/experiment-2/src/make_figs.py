#!/usr/bin/env python3
"""Build the figure specs from method_out.json and render them.

Every number plotted is read back out of the shipped artifact, so a figure
cannot disagree with the table it illustrates.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from loguru import logger

HERE = Path(__file__).resolve().parent
FIGS = HERE / "figs"
FIGS.mkdir(exist_ok=True)
GEN = "/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py"
PY = str(HERE / ".venv" / "bin" / "python")

BOUNDARY = -2.742

FAMILY_LABEL = {
    "merge_parent": "Merge with parent",
    "quantization": "Quantization",
    "addback_random": "Add-back, random dir",
    "addback_targeted_argmin": "Add-back, argmin matrix",
    "addback_targeted_all": "Add-back, all matrices",
    "addback_targeted_topk": "Add-back, k smallest",
    "lora_sft_benign": "LoRA-SFT (benign)",
    "gaussian_noise": "Gaussian weight noise",
    "combined": "Combined",
}


def render(spec: dict, name: str) -> None:
    p = FIGS / f"{name}_spec.json"
    p.write_text(json.dumps(spec, indent=1))
    r = subprocess.run([PY, GEN, "--spec", str(p), "--out", str(FIGS / name)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        logger.error(f"{name}: {r.stdout[-2000:]}\n{r.stderr[-2000:]}")
        raise SystemExit(f"figure {name} refused")
    logger.info(f"wrote {FIGS / name}.pdf/.png")


def main() -> None:
    out = json.loads((HERE / "method_out.json").read_text())
    ds = {d["dataset"]: d["examples"] for d in out["datasets"]}
    rows = [e["metadata_meta"] for e in ds["ladder"]]
    prof = {e["metadata_meta"]["stage_id"]: e["metadata_meta"]["e_v1"]
            for e in ds["ladder_e_v1_profiles"]}
    diag = {e["input"]: e["metadata_meta"]["value"] for e in ds["diagnostics"]}
    parent = diag["parent_row"]
    root = diag["root_row"]
    scan = [e["metadata_meta"] for e in ds["scan"]]
    rob = {e["input"]: e["metadata_meta"] for e in ds["robustness"]}

    fams: dict[str, list[dict]] = {}
    for r in rows:
        fams.setdefault(r["family"], []).append(r)
    for v in fams.values():
        v.sort(key=lambda r: r["intensity"])

    # ---- panel (a): flag strength; (b): harmful compliance -----------------
    def norm_x(rs):
        xs = [r["intensity"] for r in rs]
        lo, hi = min(xs), max(xs)
        return [(x - lo) / (hi - lo) if hi > lo else 0.0 for x in xs]

    fam_order = [f for f in ["addback_targeted_all", "addback_targeted_topk",
                             "addback_targeted_argmin", "addback_random",
                             "merge_parent", "quantization", "lora_sft_benign",
                             "gaussian_noise", "combined"] if f in fams]
    a_series, b_series = [], []
    for f in fam_order:
        rs = fams[f]
        if len(rs) < 2:
            continue
        x = norm_x(rs)
        a_series.append({"label": FAMILY_LABEL[f], "x": x,
                         "values": [r["W05_abl_min_layer_energy"] for r in rs]})
        b_series.append({"label": FAMILY_LABEL[f], "x": x,
                         "values": [1.0 - r["harmful_refusal_rate"] for r in rs]})
    a_series.append({"label": "Panel boundary", "x": [0.0, 1.0],
                     "values": [BOUNDARY, BOUNDARY]})
    b_series.append({"label": "Abliterated root", "x": [0.0, 1.0],
                     "values": [1.0 - root["harmful_refusal_rate"]] * 2})
    b_series.append({"label": "Instruct parent", "x": [0.0, 1.0],
                     "values": [1.0 - parent["harmful_refusal_rate"]] * 2})

    # ---- panel (c): the crossing, every stage at once ----------------------
    c_series = []
    for f in [x for x in fam_order if x != "combined"]:   # 8-colour palette cap
        rs = fams[f]
        c_series.append({"label": FAMILY_LABEL[f],
                         "x": [r["harmful_refusal_rate"] for r in rs],
                         "values": [r["W05_abl_min_layer_energy"] for r in rs]})
    c_series.append({"label": "Root / parent",
                     "x": [root["harmful_refusal_rate"], parent["harmful_refusal_rate"]],
                     "values": [root["W05_abl_min_layer_energy"],
                                parent["W05_abl_min_layer_energy"]]})

    # ---- panel (d): the per-matrix v1 energy profile -----------------------
    import math
    want = [("parent", "Instruct parent"), ("root_V_A", "Abliterated root")]
    for cand, lab in (("d2topk_k4", "Add-back, 4 smallest"),
                      ("d2min_eps1.00", "Add-back, argmin only"),
                      ("d2all_eps0.10", "Add-back, all @ eps=0.10")):
        if cand in prof:
            want.append((cand, lab))
    d_series = []
    for sid, lab in want:
        ev = prof.get(sid)
        if not ev:
            continue
        y = sorted(math.log10(max(v, 1e-30)) for v in ev)
        d_series.append({"label": lab, "x": list(range(1, len(y) + 1)), "values": y})
    d_series.append({"label": "Panel boundary",
                     "x": [1, len(prof["root_V_A"])], "values": [BOUNDARY, BOUNDARY]})

    render({"type": "line", "width_in": 7.0, "aspect": "4:3",
            "title": "Flag strength collapses under every treatment but one",
            "xlabel": "Treatment intensity (normalised within family)",
            "ylabel": "W05 (log10 min energy on v1)", "series": a_series},
           "fig1a_flag_strength")
    render({"type": "line", "width_in": 7.0, "aspect": "4:3",
            "title": "Harmful compliance is what the launderer is trying to keep",
            "xlabel": "Treatment intensity (normalised within family)",
            "ylabel": "Harmful compliance (1 - refusal rate)", "series": b_series},
           "fig1b_compliance")
    render({"type": "scatter", "width_in": 7.0, "aspect": "4:3",
            "title": "The crossing: every ladder stage (panel boundary at W05 = -2.742)",
            "xlabel": "Harmful refusal rate (rubric-B judge, 40-item core)",
            "ylabel": "W05 (log10 min energy on v1)", "series": c_series},
           "fig2a_crossing")
    render({"type": "line", "width_in": 7.0, "aspect": "4:3",
            "title": "W05 is a minimum, so it always has a runner-up",
            "xlabel": "Residual-write matrix, sorted by v1 energy",
            "ylabel": "log10 v1 energy", "series": d_series},
           "fig2b_profiles")

    # ---- figure 2: ARM 2 + statistic robustness ----------------------------
    ok_hub = [r for r in scan if r.get("arm") == "hub" and r["status"] == "OK"]
    ctrl_a = [r for r in scan if r.get("control_class") == "abliterated"
              and r["status"] == "OK"]
    ctrl_c = [r for r in scan if r.get("control_class") == "panel_clean"
              and r["status"] == "OK"]
    e_series = [
        {"label": f"Undeclared Hub checkpoints (n={len(ok_hub)})",
         "values": [r["W05_abl_min_layer_energy"] for r in ok_hub]},
        {"label": f"Panel non-abliterated (n={len(ctrl_c)})",
         "values": [r["W05_abl_min_layer_energy"] for r in ctrl_c]},
        {"label": f"Panel abliterated (n={len(ctrl_a)})",
         "values": [r["W05_abl_min_layer_energy"] for r in ctrl_a]},
    ]
    stats = ["W01", "W02", "W03", "W04", "W05", "W05q10"]
    render({"type": "ecdf", "width_in": 7.0, "aspect": "4:3",
            "title": "No undeclared Hub checkpoint enters the abliterated region",
            "xlabel": "W05 (log10 min energy on v1)",
            "ylabel": "Fraction of checkpoints", "series": e_series},
           "fig3a_scan_distribution")
    render({"type": "bar", "width_in": 7.0, "aspect": "4:3",
            "title": "Fraction of non-broken ladder stages still flagged",
            "xlabel": "Weight statistic", "ylabel": "Survival fraction",
            "categories": stats,
            "series": [{"values": [rob[s]["survival_fraction"] for s in stats]}]},
           "fig3b_robustness")


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    main()
