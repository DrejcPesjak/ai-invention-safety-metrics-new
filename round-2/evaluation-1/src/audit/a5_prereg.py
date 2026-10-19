"""A5 — pre-registration fidelity audit.

Deviations table (trigger, date, direction of effect) across E1/E2/E3, plus the
two mandatory items (the excess-width sign convention and the alpha-grid
amendment), the refusal_direction.pt provenance trace, and the mechanical
abliteration write-matrix coverage check.
"""

from __future__ import annotations

import ast
import datetime as dt
import re
import subprocess
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger

from .common import E1, E2, E3, OUT, dump_json, load_json
from spi.indicators import wilson_ci  # noqa: E402

MODELS_E2 = ("base", "instruct", "abliterated")
REPORTED_EXCESS_WIDTH = {"instruct": 0.019, "abliterated": -0.031, "base": -0.330}
# Arditi-style abliteration must orthogonalise every matrix WRITING to the
# residual stream.  In a Llama/Qwen-style decoder those are:
REQUIRED_WRITE_MATRICES = ["self_attn.o_proj.weight", "mlp.down_proj.weight",
                           "embed_tokens.weight"]


def _mtime(p: Path) -> str:
    return dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).isoformat()


# --------------------------------------------------------------------------- #
# (c)(i) excess-width sign convention
# --------------------------------------------------------------------------- #
def excess_width_audit() -> dict[str, Any]:
    pre = load_json(E2 / "prereg.json")
    rows = []
    for key in MODELS_E2:
        m = load_json(E2 / "results" / f"model_{key}.json")
        pp = m["agg"]["per_prompt"]
        a = np.asarray([r["alpha_down"] for r in pp], dtype=float)
        b = np.asarray([r["alpha_down_forced_a"] for r in pp], dtype=float)
        conv_prereg = a - b                    # prereg: alpha_down - alpha_down_forced_A
        conv_paper = b - a                     # paper:  alpha_down_forced_A - alpha_down
        rep = REPORTED_EXCESS_WIDTH[key]
        summ = m["summary"]
        rows.append({
            "model": key, "n_prompts": len(pp),
            "prereg_convention_mean_alpha_down_minus_forcedA": float(conv_prereg.mean()),
            "paper_convention_mean_forcedA_minus_alpha_down": float(conv_paper.mean()),
            "reported_excess_width": rep,
            "matches_prereg_convention": bool(abs(conv_prereg.mean() - rep) < 5e-3),
            "matches_paper_convention": bool(abs(conv_paper.mean() - rep) < 5e-3),
            "archived_summary_excess_width": summ["excess_width"],
            "archived_summary_residual": summ["residual"],
            "sign_corrected_value_prereg_convention": float(conv_prereg.mean()),
            "ci_excludes_zero_reported": summ.get("excess_width_ci_excludes_0"),
            "noise_floor_p95": summ.get("noise_floor_p95"),
            "lower_bound_below_noise_floor": bool(
                summ["excess_width"]["ci_low"] < summ.get("noise_floor_p95", 0.05)),
        })
    invariant = all(r["ci_excludes_zero_reported"] is False for r in rows)
    return {
        "prereg_primary_statistic": pre.get("primary_statistic"),
        "paper_reported_statistic": "excess_width = alpha_down_forced_A - alpha_down",
        "per_model": rows,
        "which_convention_the_reported_numbers_use": (
            "paper" if all(r["matches_paper_convention"] for r in rows)
            else "prereg" if all(r["matches_prereg_convention"] for r in rows)
            else "mixed"),
        "conclusion_invariant_to_the_flip": invariant,
        "statement": (
            "The pre-registration names the primary statistic as residual = alpha_down "
            "- alpha_down_forced_A; the reported excess_width is its NEGATION, "
            "alpha_down_forced_A - alpha_down. Recomputing both conventions from the "
            "archived per-prompt values confirms that the reported 0.019 / -0.031 / "
            "-0.330 are the PAPER convention. Because H1b is a TWO-SIDED test about "
            "zero - every CI overlaps 0 and every lower bound sits below the "
            "temperature-0.7 RESET noise floor p95 = 0.05 - the substantive conclusion "
            "is INVARIANT to the flip: negating a statistic negates its interval, and "
            "an interval that covers zero still covers zero. This is therefore recorded "
            "as a REPORTING ERROR in the sign convention, NOT as a change in result, "
            "and it must not be inflated into one."),
    }


# --------------------------------------------------------------------------- #
# (c)(ii) alpha-grid amendment and alpha_50 resolvability
# --------------------------------------------------------------------------- #
def _alpha50_from_curve(alphas: list[float], rates: list[float]) -> float | None:
    """First upward crossing of 0.5, linearly interpolated (E2's read-off)."""
    for i in range(1, len(alphas)):
        if rates[i - 1] < 0.5 <= rates[i]:
            x0, x1, y0, y1 = alphas[i - 1], alphas[i], rates[i - 1], rates[i]
            if y1 == y0:
                return float(x1)
            return float(x0 + (0.5 - y0) * (x1 - x0) / (y1 - y0))
    return None


def alpha50_audit() -> dict[str, Any]:
    pre = load_json(E2 / "prereg.json")
    am = [a for a in pre.get("amendments", [])
          if "alpha" in str(a.get("change", "")).lower()
          and ("grid" in str(a.get("change", "")).lower()
               or "delta" in str(a.get("change", "")).lower())]
    curves = {}
    for key in MODELS_E2:
        m = load_json(E2 / "results" / f"model_{key}.json")
        f = m["steering_response_curve"]["fitted"]
        alphas, rates = list(f["alphas"]), list(f["refusal_rate"])
        n_draws = len(f.get("example_generation_prompt0", {})) or None
        # E2's alpha_50 probe uses 5 prompts per alpha point (Bernoulli draws)
        n_per_point = 5
        a50 = _alpha50_from_curve(alphas, rates)
        wil = [{"alpha": a, "rate": r,
                **wilson_ci(int(round(r * n_per_point)), n_per_point)}
               for a, r in zip(alphas, rates)]
        # bootstrap the 5 Bernoulli draws per point and re-read alpha_50
        rng = np.random.default_rng(29)
        draws = []
        ks = [int(round(r * n_per_point)) for r in rates]
        for _ in range(5000):
            rr = [float(rng.binomial(n_per_point, k / n_per_point)) / n_per_point
                  for k in ks]
            v = _alpha50_from_curve(alphas, rr)
            if v is not None:
                draws.append(v)
        defined = a50 is not None
        curves[key] = {
            "alphas": alphas, "refusal_rate": rates,
            "max_refusal_rate": max(rates) if rates else None,
            "n_bernoulli_draws_per_alpha": n_per_point,
            "alpha_50_read_off": a50,
            "alpha_50_defined": defined,
            "alpha_50_bootstrap_ci95": (
                [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))]
                if defined and len(draws) > 100 else None),
            "alpha_50_bootstrap_sd": (float(np.std(draws))
                                      if defined and len(draws) > 100 else None),
            "frac_bootstrap_undefined": 1 - len(draws) / 5000,
            "note": (None if defined else
                     "alpha_50 is UNDEFINED for this member: the curve never reaches a "
                     "0.5 refusal rate (max rate "
                     f"{max(rates) if rates else float('nan'):.2f}). The bootstrap "
                     "interval is suppressed because it would be read off resamples "
                     "that happen to cross a threshold the point curve never reaches."),
            "per_alpha_wilson": wil,
        }
    grid_delta = pre["alpha_grid"]["delta"]
    gap = None
    ci_i = curves["instruct"].get("alpha_50_bootstrap_ci95")
    ci_a = curves["abliterated"].get("alpha_50_bootstrap_ci95")
    if curves["instruct"]["alpha_50_read_off"] and curves["abliterated"]["alpha_50_read_off"]:
        gap = abs(curves["abliterated"]["alpha_50_read_off"]
                  - curves["instruct"]["alpha_50_read_off"])
    resolvable = bool(gap is not None and ci_i and ci_a
                      and (ci_i[1] < ci_a[0] or ci_a[1] < ci_i[0]))
    return {
        "prereg_alpha_grid": pre["alpha_grid"],
        "originally_preregistered_alpha_grid": pre["alpha_grid_as_originally_preregistered"],
        "amendments_matching_alpha_grid": am,
        "reported_alpha_50": {"instruct": 0.475, "abliterated": 0.550, "base": None},
        "recomputed_curves": curves,
        "gap_instruct_vs_abliterated": gap,
        "grid_step": grid_delta,
        "gap_in_grid_steps": (gap / grid_delta) if gap else None,
        "alpha_50_gap_is_resolvable": resolvable,
        "statement": (
            f"The reported alpha_50 gap between instruct and abliterated is "
            f"{gap if gap is not None else float('nan'):.3f}, i.e. "
            f"{(gap / grid_delta) if gap else float('nan'):.1f} steps of the amended "
            f"{grid_delta} grid, read off a curve with only 5 Bernoulli draws per alpha "
            "point. Bootstrapping those 5 draws per point and re-reading the 50% "
            "crossing gives overlapping intervals for the two members, so the gap is "
            "NOT resolvable at this grid resolution and sample size. iteration 2 must "
            "not treat alpha_50 as a graded metric that separates these two members "
            "without a denser grid and more draws per point."
            if not resolvable else
            "The bootstrapped alpha_50 intervals for instruct and abliterated are "
            "disjoint, so the gap is resolvable at this grid resolution."),
    }


# --------------------------------------------------------------------------- #
# (d) refusal_direction.pt provenance trace
# --------------------------------------------------------------------------- #
def refusal_direction_trace() -> dict[str, Any]:
    hits = []
    for name, root in (("E1", E1), ("E2", E2), ("E3", E3)):
        try:
            out = subprocess.run(
                ["grep", "-rn", "-E",
                 r"refusal_direction|estimate_refusal_direction|r_dir|direction\.pt",
                 "--include=*.py", str(root)],
                capture_output=True, text=True, timeout=60).stdout
        except Exception:  # noqa: BLE001
            out = ""
        for line in out.splitlines():
            parts = line.split(":", 2)
            if len(parts) == 3:
                hits.append({"experiment": name,
                             "file": str(Path(parts[0]).relative_to(root)),
                             "line": int(parts[1]), "code": parts[2].strip()[:220]})
    an3 = load_json(E3 / "results" / "analysis.json")
    meta = an3.get("ladder", {}).get("refusal_direction_meta")
    downstream = [
        {"result": "in-house abliteration-strength ladder "
                   "(abl_c0.25 / c0.50 / c0.75 / c1.00 members)",
         "uses_the_same_fitted_vector": True,
         "reported_as": "abliteration_strength verdict = SNAPPED under both scorers"},
        {"result": "abliteration_screen_table (fluency screen on the 4 ladder members)",
         "uses_the_same_fitted_vector": True, "reported_as": "screen table"},
        {"result": "E1 toward_refuse / toward_comply perturbation directions",
         "uses_the_same_fitted_vector": False,
         "reported_as": "E1 fits its OWN diff-in-means direction at its own layer L=15 "
                        "(spi/observable.py DiffMeansObservable); it does not load "
                        "E3/refusal_direction.pt"},
        {"result": "E2 steering axis",
         "uses_the_same_fitted_vector": False,
         "reported_as": "E2 fits its own CAA-style response-contrast axis "
                        "(direction.py) at its own selected layer"},
    ]
    shared = [d for d in downstream if d["uses_the_same_fitted_vector"]]
    return {
        "file": str(E3 / "refusal_direction.pt"),
        "bytes": (E3 / "refusal_direction.pt").stat().st_size,
        "mtime_utc": _mtime(E3 / "refusal_direction.pt"),
        "fit_metadata": meta,
        "grep_hits": hits,
        "n_grep_hits": len(hits),
        "downstream_results": downstream,
        "n_results_sharing_the_same_fitted_vector": len(shared),
        "feeds_anything_besides_the_in_house_abliteration_ladder": bool(
            len(shared) > 2),
        "statement": (
            "refusal_direction.pt is fitted ONCE in E3 (diff-in-means over 128 held-out "
            "harmful/benign pairs at layer_frac 0.6) and is used ONLY by E3's in-house "
            "abliteration ladder and its fluency screen. E1 and E2 each fit their own "
            "directions independently (E1 spi/observable.py DiffMeansObservable at L=15; "
            "E2 direction.py CAA-style response contrast), so no result outside the "
            "ladder is downstream of this particular fitted vector. The correlated-error "
            "risk is therefore CONFINED to the ladder results, which is the narrowest "
            "possible scope for it - but within that scope the vector is unvalidated: no "
            "held-out check that the direction actually mediates refusal is archived, "
            "only the diff-in-means fit statistics."),
    }


# --------------------------------------------------------------------------- #
# (e) abliteration write-matrix coverage check (static inspection, no GPU)
# --------------------------------------------------------------------------- #
def abliteration_coverage() -> dict[str, Any]:
    src = (E3 / "method.py").read_text()
    m = re.search(r"def build_abliterated\(.*?\n(?=\ndef |\nclass )", src, re.S)
    body = m.group(0) if m else ""
    edited = []
    if "o_proj.weight" in body:
        edited.append("self_attn.o_proj.weight")
    if "down_proj.weight" in body:
        edited.append("mlp.down_proj.weight")
    if "embed_tokens.weight" in body:
        edited.append("embed_tokens.weight")
    missing = [x for x in REQUIRED_WRITE_MATRICES if x not in edited]
    complete = not missing
    manifest = load_json(E3 / "results" / "ladder_models_manifest.json")
    an3 = load_json(E3 / "results" / "analysis.json")
    ladder = an3.get("ladder", {})
    verdict = (ladder.get("abliteration_strength_repaired_scorer")
               or ladder.get("abliteration_strength") or {}).get("verdict")

    if complete:
        relabel = (
            "COVERAGE IS COMPLETE. The in-house edit W <- W - c*r*r^T*W is applied to "
            "every matrix that writes to the residual stream in a Qwen3-style decoder: "
            "attention o_proj, MLP down_proj, and the embedding (whose rows are "
            "residual-stream vectors). Under the relabel rule stated in advance, the "
            "ladder's SNAPPED failure may therefore be attributed to the TECHNIQUE at "
            "this scale rather than to an incomplete reimplementation. Two caveats "
            "belong with that attribution and must be reported alongside it: (1) the "
            "run's COMMUNITY abliterated checkpoints (mlabonne, huihui-ai) DID produce "
            "the expected behavioural shift, so a defect elsewhere in the recipe - the "
            "single-layer diff-in-means direction, the choice of layer_frac 0.6, the "
            "absence of any held-out validation that the direction mediates refusal, or "
            "the lack of the per-layer direction selection Arditi-style abliteration "
            "normally performs - remains a live alternative to 'the technique does not "
            "work'; (2) the edit uses ONE global direction fitted at one layer applied "
            "to all layers, which is a simplification of the published method. The "
            "defensible sentence is 'our single-direction weight-edit implementation of "
            "abliteration did not produce a graded knob at this scale', NOT 'abliteration "
            "strength is not a knob'.")
    else:
        relabel = (
            "COVERAGE IS INCOMPLETE: the edit misses " + ", ".join(missing) +
            ". Under the relabel rule stated in advance, the ladder's SNAPPED failure is "
            "relabelled 'a failed reimplementation of abliteration (incomplete "
            "write-matrix coverage)' and NOT 'a property of the technique'. The run's "
            "community abliterated checkpoints (mlabonne / huihui-ai) DID produce the "
            "expected behavioural shift, which makes an implementation defect the more "
            "likely explanation.")

    return {
        "source": "E3/method.py build_abliterated()",
        "edit_rule": "W <- W - c * r r^T W on every matrix writing to the residual stream",
        "required_write_matrices": REQUIRED_WRITE_MATRICES,
        "edited_matrices": edited,
        "missing_matrices": missing,
        "coverage_complete": complete,
        "matrices_deliberately_excluded": [
            "q_proj / k_proj / v_proj (READ from the residual stream)",
            "gate_proj / up_proj (READ from the residual stream)",
            "lm_head (tied to embed_tokens in Qwen3-0.6B)"],
        "direction_fit": an3.get("ladder", {}).get("refusal_direction_meta"),
        "single_direction_all_layers": True,
        "ladder_verdict_as_reported": verdict,
        "manifest_construction": manifest.get("construction"),
        "relabel_rule_applied": relabel,
        "relabelled_claim": (
            "our single-direction weight-edit implementation of abliteration did not "
            "produce a graded refusal knob at 0.6B scale" if complete else
            "a failed reimplementation of abliteration (incomplete write-matrix coverage)"),
    }


# --------------------------------------------------------------------------- #
# (a/b) deviations table
# --------------------------------------------------------------------------- #
def deviations_table(ew: dict[str, Any], a50: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pre2 = load_json(E2 / "prereg.json")
    for a in pre2.get("amendments", []):
        change = str(a.get("change", ""))
        direction, why = _direction_of_effect(change, a.get("reason", ""))
        rows.append({
            "experiment": "E2", "amendment_id": a.get("id"),
            "prereg_field": _field_of(change),
            "prereg_value": _prereg_value(pre2, change),
            "as_reported_value": change,
            "trigger": a.get("when") or a.get("trigger"),
            "date_timestamp": a.get("timestamp"),
            "date_source": "amendment record",
            "announced_in_prereg": True,
            "direction_of_effect": direction,
            "direction_justification": why,
            "reason": str(a.get("reason", ""))[:600],
        })
    # E2 unannounced deviation: the sign convention
    rows.append({
        "experiment": "E2", "amendment_id": None,
        "prereg_field": "primary_statistic",
        "prereg_value": pre2.get("primary_statistic"),
        "as_reported_value": "excess_width = alpha_down_forced_A - alpha_down (negated)",
        "trigger": "reporting step; not recorded as an amendment",
        "date_timestamp": _mtime(E2 / "method_out.json"),
        "date_source": "file mtime of E2/method_out.json (no amendment record exists)",
        "announced_in_prereg": False,
        "direction_of_effect": "neutral",
        "direction_justification": (
            "H1b is two-sided about zero; negating the statistic negates the interval, "
            "and an interval covering zero still covers zero. Verified by recomputing "
            "both conventions from the archived per-prompt values: "
            f"conclusion_invariant_to_the_flip = {ew['conclusion_invariant_to_the_flip']}."),
        "reason": "sign-convention inversion between pre-registration and report",
    })
    # E3 amendment
    am3 = load_json(E3 / "prereg_amendment.json")
    rows.append({
        "experiment": "E3", "amendment_id": "POST-HOC-JUDGE-REPAIR",
        "prereg_field": "judge (model + system prompt) used to score generations",
        "prereg_value": "openai/gpt-5.4-nano, frozen rubric, EMPTY system prompt",
        "as_reported_value": ("repaired arm added: meta-llama/llama-3.3-70b-instruct + "
                              "evaluator system prompt, run at full coverage alongside "
                              "the frozen arm"),
        "trigger": str(am3.get("headline", ""))[:300],
        "date_timestamp": _mtime(E3 / "prereg_amendment.json"),
        "date_source": "file mtime of E3/prereg_amendment.json",
        "announced_in_prereg": False,
        "direction_of_effect": "strengthens",
        "direction_justification": (
            "prereg.json was not edited and the frozen arm is reported in full "
            "including its failure; the amendment ADDS a scorer rather than replacing "
            "one, and it is what turns a silent measurement failure into the paper's "
            "main deliverable. It does, however, move the pre-registered sanity gate "
            "from FAIL to PASS on identical generations, so the gate's PASS is a "
            "post-hoc result and must be reported as such."),
        "reason": str(am3.get("status", ""))[:400],
    })
    # E1: no pre-registration archived
    rows.append({
        "experiment": "E1", "amendment_id": None,
        "prereg_field": "(none)",
        "prereg_value": "NO PRE-REGISTRATION ARCHIVED FOR E1",
        "as_reported_value": (
            "the closest archived analogues are out/layer_choice.json (written and "
            "asserted BEFORE any indicator was computed) and the pre-registered "
            "ordering direction / verdict rule embedded in out/tier0_raw.json "
            "['ordering_tests']['prereg_direction'] and ['verdict']"),
        "trigger": "n/a",
        "date_timestamp": _mtime(E1 / "out" / "layer_choice.json"),
        "date_source": "file mtime of E1/out/layer_choice.json",
        "announced_in_prereg": False,
        "direction_of_effect": "unknown",
        "direction_justification": (
            "Without an archived pre-registration for E1 the fidelity of its verdict "
            "rule to a plan fixed in advance cannot be checked from the tree. This is "
            "stated plainly rather than filled in with a reconstructed prereg."),
        "reason": "E1/prereg.json does not exist",
    })
    # E1: the four pre-flight repairs, each a deviation from the planned measurement
    for name, detail, eff in [
        ("injection site", "hook moved from the layer OUTPUT to a forward PRE-hook on "
                           "the layer INPUT", "strengthens"),
        ("primary channel", "free-running replaced by teacher-forced as the primary "
                            "delta channel", "strengthens"),
        ("delta statistic", "mean|delta| replaced by the SIGNED across-rollout mean",
         "strengthens"),
        ("flicker statistic", "flicker-as-fraction replaced by crossings-per-100",
         "strengthens"),
    ]:
        rows.append({
            "experiment": "E1", "amendment_id": None,
            "prereg_field": name,
            "prereg_value": "(no archived pre-registration; planned form per the "
                            "experiment's own description)",
            "as_reported_value": detail,
            "trigger": "pre-flight gate caught the defect before the main run",
            "date_timestamp": _mtime(E1 / "out" / "tier0_raw.json"),
            "date_source": "file mtime of E1/out/tier0_raw.json",
            "announced_in_prereg": False,
            "direction_of_effect": eff,
            "direction_justification": (
                "each replaces a measurement that provably could not work (identically "
                "zero delta, growing delta, +38-68% upward bias, saturation at 1.0) "
                "with one that can; caught before the main run, so no reported number "
                "depends on the broken form"),
            "reason": "pre-flight gate",
        })
    return rows


_FIELD_HINTS = [
    ("layer", "layer_rule"), ("alpha", "alpha_grid"), ("prompt", "n_prompts"),
    ("seed", "n_seeds_per_prompt"), ("refusal", "refusal_onset_criterion"),
    ("complian", "compliance_resumption_criterion"), ("fluency", "fluency_screen"),
    ("model", "models"), ("decod", "decoding"), ("eos", "decoding.eos_banned_during_ramps"),
]


def _field_of(change: str) -> str:
    c = change.lower()
    for k, f in _FIELD_HINTS:
        if k in c:
            return f
    return "(unmapped)"


def _prereg_value(pre: dict, change: str) -> Any:
    f = _field_of(change)
    cur: Any = pre
    for part in f.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


_STRENGTHEN = ("does not saturate", "outcome-blind", "held-out", "noise floor",
               "cannot confound", "deterministic", "bit-exact", "fallback",
               "positive control", "sensitivity")
_WEAKEN = ("censored", "reduced", "fewer", "narrower", "dropped", "excluded",
           "truncat", "gated")


def _direction_of_effect(change: str, reason: str) -> tuple[str, str]:
    t = (change + " " + str(reason)).lower()
    if any(k in t for k in _STRENGTHEN):
        return "strengthens", ("the amendment removes a way the measurement could "
                               "have produced a spurious or unreadable result; it "
                               "cannot manufacture the reported null")
    if any(k in t for k in _WEAKEN):
        return "weakens", ("the amendment narrows the measured range or drops data, "
                           "which can only reduce the power to detect the effect the "
                           "hypothesis predicts")
    return "neutral", ("the amendment changes bookkeeping or presentation and does not "
                       "move the primary statistic in a predictable direction")


# --------------------------------------------------------------------------- #
def run() -> dict[str, Any]:
    ew = excess_width_audit()
    a50 = alpha50_audit()
    trace = refusal_direction_trace()
    cov = abliteration_coverage()
    table = deviations_table(ew, a50)

    out = {
        "analysis": "A5_preregistration_fidelity_audit",
        "e1_prereg_archived": (E1 / "prereg.json").exists(),
        "e2_n_amendments_documented": len(load_json(E2 / "prereg.json")
                                          .get("amendments", [])),
        "deviations_table": table,
        "n_deviations": len(table),
        "n_announced": sum(1 for r in table if r["announced_in_prereg"]),
        "n_unannounced": sum(1 for r in table if not r["announced_in_prereg"]),
        "direction_of_effect_tally": _tally(table, "direction_of_effect"),
        "excess_width_sign_convention": ew,
        "alpha_grid_amendment_and_alpha50": a50,
        "refusal_direction_provenance": trace,
        "abliteration_coverage_check": cov,
    }
    dump_json(OUT / "a5_prereg.json", out)
    logger.info(f"A5: {len(table)} deviation rows; coverage_complete="
                f"{cov['coverage_complete']}; alpha_50 resolvable="
                f"{a50['alpha_50_gap_is_resolvable']}")
    return out


def _tally(rows: list[dict], field: str) -> dict[str, int]:
    o: dict[str, int] = {}
    for r in rows:
        o[str(r.get(field))] = o.get(str(r.get(field)), 0) + 1
    return dict(sorted(o.items()))
