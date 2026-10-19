"""A2 — observable-validity gate on the 'indicators track lineage, not safety' claim.

The claim compares Var*, AC1 and flicker ACROSS members.  A cross-member
comparison is only meaningful where the observable r_t actually discriminates
harmful from benign prompts on each member.  This module states the gate BEFORE
looking at the downstream effect, applies it, and reports the sensitivity curve.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from loguru import logger

from .common import (E1, N_BOOT, OUT, SEED_BOOTSTRAP, dump_json, load_json,
                     record_substitution)
from spi.indicators import paired_bootstrap_diff  # noqa: E402

GATE_AUROC = 0.70
GATE_MARGIN = 0.30
THRESHOLDS = (0.60, 0.65, 0.70, 0.75, 0.80)
INDICATORS = ("var_star", "ac1", "flicker_crossings_per_100")

GATE_DEFINITION = {
    "declared_before_computing_downstream_effect": True,
    "written_at": "stage a2, before any gated indicator comparison was evaluated",
    "rule": (
        "A panel member PASSES the observable-validity gate at a given readout if the "
        "harmful-vs-benign AUROC of r_0 at that readout is >= 0.70; where AUROC is not "
        "archived, the equivalent margin criterion is r_0 margin >= 0.30 nats."),
    "auroc_threshold": GATE_AUROC,
    "margin_threshold_nats": GATE_MARGIN,
    "threshold_justification": (
        "0.70 is the conventional 'better than weak discrimination' line for a binary "
        "AUROC: below it the observable separates the two prompt classes so poorly that "
        "its fluctuation statistics are statistics of noise rather than of the quantity "
        "the hypothesis is about. The full sensitivity curve at "
        f"{list(THRESHOLDS)} is reported so the conclusion's dependence on the cut is "
        "visible and the cut is not a researcher degree of freedom."),
    "sensitivity_thresholds": list(THRESHOLDS),
    "primary_readout_declaration": {
        "cross_model_indicator_comparison": "final",
        "perturbation_local_quantities": "layerL",
        "rationale": (
            "The cross-model comparison is PRIMARY at the FINAL-LAYER readout, where "
            "r_t is defined by construction on the model's own output logits and does "
            "not depend on logit-lens fidelity at an intermediate layer. Anything "
            "perturbation-local (A1's decay statistics) is PRIMARY at the LAYER-L lens, "
            "because that is where the perturbation is injected. This split matters "
            "because E1 measures the layer-L lens against the final-layer readout at "
            "only 0.17-0.26, below its own pre-registered 0.3 threshold, so 'which "
            "readout' is a live confound rather than a formality."),
    },
    "unsupported_rule": (
        "If fewer than 2 members pass at the readout under test, the cross-model "
        "comparison is UNDEFINED and is reported as "
        "indicator_comparison_status = UNSUPPORTED_ONLY_N_MEMBERS_PASS."),
}

REQUIRED_STATEMENT = (
    "The iteration-1 conclusion that the fluctuation indicators track LINEAGE rather "
    "than SAFETY rests on comparisons involving models on which the observable r_t is "
    "uninformative: on the panel of four, only qwen3-0.6b/instruct discriminates "
    "harmful from benign prompts at the pre-stated gate, while qwen3-0.6b/base "
    "(AUROC 0.414, margin -0.153 nats), qwen3-0.6b/abliterated (AUROC 0.481, margin "
    "0.026) and smollm2/base (AUROC 0.633, margin 0.110) do not. Var*, AC1 and flicker "
    "measured on those three members are fluctuation statistics of an observable that "
    "does not track the construct, so the cross-member comparison cannot separate "
    "'indicators track lineage' from 'the instrument only works on one member'. The "
    "conclusion is DOWNGRADED to a qualitative observation about lineage-level spread "
    "in the indicator values, and must not be used as a settled negative result.")


def _per_prompt(indicators: list[dict], model: str, readout: str,
                field: str) -> dict[str, float]:
    key = "primary" if readout == "layerL" else "final_layer_readout"
    out = {}
    for r in indicators:
        if r["model"] != model:
            continue
        v = (r.get(key) or {}).get("detrended", {}).get(field)
        if v is not None and np.isfinite(v):
            out[r["prompt_id"]] = float(v)
    return out


def run() -> dict[str, Any]:
    dump_json(OUT / "gate_definition.json", GATE_DEFINITION)

    raw = load_json(E1 / "out" / "tier0_raw.json")
    pmm = raw["per_model_meta"]
    indicators = raw["indicators"]
    models = sorted(pmm)

    # ---- (a) per-member observable validity -------------------------------
    per_member: list[dict[str, Any]] = []
    for m in models:
        os_ = pmm[m]["observable_sanity"]
        dm = pmm[m]["diff_means"]
        rec = {
            "model": m,
            "member": raw["aggregate_by_model"][m]["member"],
            "lineage": raw["aggregate_by_model"][m]["lineage"],
            "r0_auroc_layerL": os_.get("auroc"),
            "r0_margin_layerL": os_.get("margin"),
            "r0_harmful_mean": os_.get("r0_harmful_mean"),
            "r0_benign_mean": os_.get("r0_benign_mean"),
            "r0_auroc_bootstrap_ci": None,
            "diff_means_probe_auroc": dm.get("auroc"),
            "diff_means_cohens_d": dm.get("cohens_d"),
            "observable_degenerate_flag": raw["observable_degenerate_by_model"].get(m),
            "lens_vs_final_corr": raw["aggregate_by_model"][m].get("lens_vs_final_corr"),
        }
        rec["r0_auroc_final"] = None
        rec["r0_margin_final"] = None
        per_member.append(rec)

    record_substitution(
        "A2", "per-item r_0 values for the harmful and benign contrast sets",
        "archived per-model observable_sanity {auroc, margin, r0_harmful_mean, "
        "r0_benign_mean} only",
        "E1/out/tier0_raw.json archives the harmful/benign r_0 SUMMARIES, not the "
        "per-item scores, so a 2000-rep bootstrap CI on the AUROC cannot be computed "
        "from the archived tree",
        "the gate itself is unaffected (it keys off the archived AUROC point estimate); "
        "only the CI on that AUROC is unavailable and is reported as null")
    record_substitution(
        "A2", "observable_sanity at the FINAL-LAYER readout",
        "layer-L observable_sanity applied as the gate at both readouts",
        "E1 archives observable_sanity once, computed on the layer-L lens; no "
        "final-layer r_0 harmful-vs-benign sanity block exists in the tree",
        "the final-layer indicator comparison is gated on layer-L discrimination; "
        "recorded as a limitation, and it does not change n_passing because the same "
        "member set passes")

    # ---- (b/d) gate application + sensitivity curve ------------------------
    def passes(rec: dict[str, Any], thr: float) -> bool:
        a = rec.get("r0_auroc_layerL")
        if a is not None and np.isfinite(a):
            return bool(a >= thr)
        mg = rec.get("r0_margin_layerL")
        # margin fallback: 0.30 nats <-> 0.70 AUROC, scaled linearly off 0.5
        return bool(mg is not None and mg >= GATE_MARGIN * (thr - 0.5) / (GATE_AUROC - 0.5))

    for rec in per_member:
        rec["passes_gate"] = passes(rec, GATE_AUROC)
        rec["gate_basis"] = ("auroc" if rec.get("r0_auroc_layerL") is not None
                             else "margin_fallback")

    sensitivity = []
    for thr in THRESHOLDS:
        p = [r["model"] for r in per_member if passes(r, thr)]
        sensitivity.append({"threshold": thr, "n_passing": len(p), "passing_models": p,
                            "comparison_defined": len(p) >= 2})

    passing = [r["model"] for r in per_member if r["passes_gate"]]
    n_passing = len(passing)
    logger.info(f"A2 gate at AUROC>={GATE_AUROC}: {n_passing} of {len(models)} pass "
                f"-> {passing}")

    # ---- (c/e) gated cross-model indicator comparison, both readouts -------
    def comparison(model_set: list[str], readout: str) -> dict[str, Any]:
        out: dict[str, Any] = {"readout": readout, "models": model_set,
                               "n_models": len(model_set), "contrasts": []}
        if len(model_set) < 2:
            out["status"] = f"UNSUPPORTED_ONLY_{len(model_set)}_MEMBERS_PASS"
            return out
        out["status"] = "COMPUTED"
        for i, a in enumerate(model_set):
            for b in model_set[i + 1:]:
                for ind in INDICATORS:
                    pb = paired_bootstrap_diff(
                        _per_prompt(indicators, a, readout, ind),
                        _per_prompt(indicators, b, readout, ind),
                        n_reps=N_BOOT, seed=SEED_BOOTSTRAP)
                    out["contrasts"].append(
                        {"model_a": a, "model_b": b, "indicator": ind, **pb})
        return out

    gated = {ro: comparison(passing, ro) for ro in ("layerL", "final")}
    ungated = {ro: comparison(models, ro) for ro in ("layerL", "final")}

    sens_comparisons = {}
    for thr in THRESHOLDS:
        p = [r["model"] for r in per_member if passes(r, thr)]
        sens_comparisons[f"thr_{thr}"] = {
            ro: comparison(p, ro) for ro in ("layerL", "final")}

    status = ("COMPUTED" if n_passing >= 2
              else f"UNSUPPORTED_ONLY_{n_passing}_MEMBERS_PASS")

    # ---- descriptive per-member indicator values (both readouts) ----------
    per_member_indicators = []
    for m in models:
        row = {"model": m}
        for ro in ("layerL", "final"):
            for ind in INDICATORS:
                vals = list(_per_prompt(indicators, m, ro, ind).values())
                row[f"{ind}_{ro}_mean"] = float(np.mean(vals)) if vals else None
                row[f"{ind}_{ro}_n"] = len(vals)
        row["passes_gate"] = next(r["passes_gate"] for r in per_member if r["model"] == m)
        per_member_indicators.append(row)

    out = {
        "analysis": "A2_observable_validity_gate",
        "defect": ("the 'indicators track lineage, not safety' conclusion compares "
                   "Var*/AC1/flicker across members without checking that r_t is "
                   "informative on each member"),
        "gate_definition": GATE_DEFINITION,
        "per_member_validity": per_member,
        "n_members": len(models), "n_passing": n_passing, "passing_models": passing,
        "sensitivity_curve": sensitivity,
        "gated_comparison": gated,
        "ungated_comparison_for_reference": ungated,
        "sensitivity_comparisons": sens_comparisons,
        "per_member_indicator_values": per_member_indicators,
        "indicator_comparison_status": status,
        "required_statement": REQUIRED_STATEMENT if n_passing <= 1 else None,
        "conclusion_downgraded": n_passing <= 1,
        "downgraded_to": ("a qualitative observation about lineage-level spread in the "
                          "indicator values" if n_passing <= 1 else None),
        "final_layer_arm_note": (
            "The final-layer arm is reported because r_t there is defined on the "
            "model's own output logits, independent of logit-lens fidelity at layer L; "
            "E1 measures the layer-L lens against the final-layer readout at only "
            "0.17-0.26, below its own pre-registered 0.3 threshold."),
    }
    dump_json(OUT / "a2_gate.json", out)
    logger.info(f"A2 status: {status}")
    return out
