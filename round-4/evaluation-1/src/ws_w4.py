#!/usr/bin/env python3
"""W4 - cost annotation and the practitioner sentence (block: cost_table)."""

from __future__ import annotations

from typing import Any

from loguru import logger

from lib_arch import Resolver, prov

PROMPTS_BY_REQUIREMENT = {
    "none": {"prompts": 0, "harmful_prompts": 0},
    "few_harmful": {"prompts": 65, "harmful_prompts": 40},
    "few_benign": {"prompts": 25, "harmful_prompts": 0},
    "contrast_pairs": {"prompts": 65, "harmful_prompts": 40},
    "generation": {"prompts": 65, "harmful_prompts": 40},
}
FAMILY_MAP = {"weights": "weights_only", "activation": "activations", "blackbox": "blackbox"}


def run_w4(res: Resolver) -> dict[str, Any]:
    logger.info("W4: cost annotation")
    m3 = res.read_json("A3", "full_method_out.json")
    numbers = res.read_json("A5", "numbers.json")
    if m3 is None or numbers is None:
        return {"status": "UNAVAILABLE", "reason": "A3 method_out / A5 numbers.json not resolvable"}

    spec = [d for d in m3["datasets"] if d["dataset"] == "metric_spec"][0]["examples"]
    spec_sha = m3["metadata"]["metric_spec_sha256"]
    long_table = [d for d in m3["datasets"] if d["dataset"] == "long_table"][0]["examples"]
    panel = [d for d in m3["datasets"] if d["dataset"] == "panel"][0]["examples"]

    # measured wall-clock medians by size bucket, straight from the long table
    size_bucket: dict[str, str] = {}
    for p in panel:
        pc = p.get("metadata_param_count") or 0
        size_bucket[p["metadata_repo"]] = (
            "0.6B" if pc < 1.0e9 else ("1.7B" if pc < 2.5e9 else "4B")
        )
    wc: dict[str, dict[str, list[float]]] = {}
    for r in long_table:
        mid = r["metadata_metric_id"]
        b = size_bucket.get(r["metadata_checkpoint"])
        w = r.get("metadata_wall_clock_s")
        if b is None or w is None:
            continue
        wc.setdefault(mid, {}).setdefault(b, []).append(float(w))

    def med(xs: list[float]) -> float:
        s = sorted(xs)
        n = len(s)
        return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

    corr = numbers["correlations"]
    pdiff = numbers["paired_differences"]

    # A5's paired_differences carries only the pre-declared comparison set (7 metrics).  The
    # depth-arm paired differences for every OTHER activation metric live in A1's arm 3, at the
    # pre-declared depth rho* = 0.679.  Both are carried forward verbatim; neither is recomputed.
    m1 = res.read_json("A1", "full_method_out.json")
    nominal_by_metric: dict[str, dict[str, Any]] = {}
    a1_arm3_nominal: list[dict[str, Any]] = []
    if m1 is not None:
        a1_arm3_nominal = m1["metadata"]["arm3"].get("activation_beats_blackbox_nominally", [])
        for e in a1_arm3_nominal:
            if e.get("baseline") == "B09_greedy_refusal_rate_harmful" and e.get("depth") == "rho_star":
                nominal_by_metric[e["metric"]] = {
                    "point": e["paired_diff"],
                    "ci95": e["paired_ci"],
                    "excludes_zero": e["excludes_zero"],
                    "source": "A1 arm3 activation_beats_blackbox_nominally at rho*=0.679, n=26 members",
                }

    rows: list[dict[str, Any]] = []
    for s in spec:
        mid = s["metadata_id"]
        fam = FAMILY_MAP.get(s["metadata_family"], s["metadata_family"])
        req = s.get("metadata_prompt_requirement") or "none"
        pr = PROMPTS_BY_REQUIREMENT.get(req, {"prompts": None, "harmful_prompts": None})
        cm = corr["member"].get(mid, {}).get("harmful_refusal_rate")
        cl = corr["lineage"].get(mid, {}).get("harmful_refusal_rate")
        pdb = pdiff["member"]["harmful_refusal_rate"].get(mid, {}).get("vs_B09_posthoc")
        if pdb is None and mid in nominal_by_metric:
            pdb = nominal_by_metric[mid]
        buckets = wc.get(mid, {})
        rows.append(
            {
                "metric_id": mid,
                "family": fam,
                "prompt_requirement": req,
                "prompts_required": pr["prompts"],
                "harmful_prompts_required": pr["harmful_prompts"],
                "forward_passes_required": s.get("metadata_measured_forward_passes_median"),
                "forward_passes_declared": s.get("metadata_declared_forward_passes"),
                "generations_required": s.get("metadata_measured_forward_passes_median")
                if s.get("metadata_stage") == "generation" else 0,
                "measured_wall_clock_median_s": s.get("metadata_measured_wallclock_s_median"),
                "measured_wall_clock_median_s_0p6B": med(buckets["0.6B"]) if buckets.get("0.6B") else None,
                "measured_wall_clock_median_s_1p7B": med(buckets["1.7B"]) if buckets.get("1.7B") else None,
                "measured_wall_clock_median_s_4B": med(buckets["4B"]) if buckets.get("4B") else None,
                "parent_model_required": False,
                "rho_member": cm["rho"] if cm else None,
                "ci_member": cm["ci95"] if cm else None,
                "n_member": cm["n"] if cm else None,
                "rho_lineage": cl["rho"] if cl else None,
                "ci_lineage": cl["ci95"] if cl else None,
                "n_lineages": cl["n_lineages"] if cl else None,
                "paired_diff_vs_best_blackbox": pdb["point"] if pdb else None,
                "paired_diff_ci": pdb["ci95"] if pdb else None,
                "paired_diff_excludes_zero": pdb["excludes_zero"] if pdb else None,
                "carried_forward": True,
                "recomputed": False,
                "provenance": prov("A5/numbers.json", f"correlations.member.{mid}.harmful_refusal_rate",
                                   cm["rho"] if cm else None),
                "cost_provenance": prov("A3/full_method_out.json",
                                        f"datasets.metric_spec[{mid}].metadata_measured_wallclock_s_median",
                                        s.get("metadata_measured_wallclock_s_median")),
            }
        )
    # sort by cost ascending: harmful prompts, then forward passes, then wall clock
    rows.sort(key=lambda r: (
        r["harmful_prompts_required"] if r["harmful_prompts_required"] is not None else 1e9,
        r["forward_passes_required"] if r["forward_passes_required"] is not None else 1e9,
        r["measured_wall_clock_median_s"] if r["measured_wall_clock_median_s"] is not None else 1e9,
    ))

    # E_1 is the one parent-REQUIRING entry; it is not in metric_spec, so add it explicitly.
    rows.append({
        "metric_id": "E_1_parent_required_incumbent",
        "family": "weights_only",
        "prompt_requirement": "none",
        "prompts_required": 0,
        "harmful_prompts_required": 0,
        "forward_passes_required": 0,
        "forward_passes_declared": 0,
        "generations_required": 0,
        "measured_wall_clock_median_s": None,
        "parent_model_required": True,
        "note": "requires BOTH the candidate and its parent checkpoint; not part of the 53-metric "
                "frozen battery, so it carries no correlation row.",
        "carried_forward": True,
        "recomputed": False,
    })

    # ---------------- M4.2 carry-forward, verbatim ----------------
    power = numbers["power"]
    rel = numbers["reliability"]
    depth = numbers["depth"]
    sel = numbers["selection_corrected_comparator"]
    a19_m = corr["member"]["A19_refusal_axis_unembed_cosine"]["harmful_refusal_rate"]
    a19_l = corr["lineage"]["A19_refusal_axis_unembed_cosine"]["harmful_refusal_rate"]
    b09_m = corr["member"]["B09_greedy_refusal_rate_harmful"]["harmful_refusal_rate"]
    b08_l = corr["lineage"]["B08_first_token_entropy_asymmetry"]["harmful_refusal_rate"]
    b01_m = corr["member"]["B01_logit_gap_harmful"]["harmful_refusal_rate"]
    a19_vs_b09 = nominal_by_metric.get(
        "A19_refusal_axis_unembed_cosine",
        {"point": None, "ci95": [None, None], "excludes_zero": None, "source": "NOT_IN_ARCHIVE"},
    )
    b09_argmax_member = sel["member"]["harmful_refusal_rate"]["B09_wins_fraction_of_resamples"]
    b09_argmax_lineage = sel["lineage"]["harmful_refusal_rate"]["B09_wins_fraction_of_resamples"]
    optimism_lineage = (
        sel["lineage"]["harmful_refusal_rate"]["mean_abs_rho_reselected_winner"]
        - sel["lineage"]["harmful_refusal_rate"]["mean_abs_rho_fixed_B09"]
    )

    def cf(key: str, value: Any, file: str, path: str) -> dict[str, Any]:
        return {"key": key, "value": value, "recomputed": False,
                "provenance": prov(file, path, value)}

    carry = [
        cf("minimum_detectable_abs_drho_at_80pct_at_19_lineages",
           power["minimum_detectable_abs_drho_at_80pct"], "A5/numbers.json",
           "power.minimum_detectable_abs_drho_at_80pct"),
        cf("power_at_delta_0.20", power["power_curve"]["0.2"]["power"], "A5/numbers.json",
           "power.power_curve['0.2'].power"),
        cf("power_at_delta_0.30", power["power_curve"]["0.3"]["power"], "A5/numbers.json",
           "power.power_curve['0.3'].power"),
        cf("n_lineages_required_for_80pct_at_0.30",
           power["n_lineages_required_for_80pct_power"]["0.3"], "A5/numbers.json",
           "power.n_lineages_required_for_80pct_power['0.3']"),
        cf("n_lineages_required_for_80pct_at_0.20",
           power["n_lineages_required_for_80pct_power"]["0.2"], "A5/numbers.json",
           "power.n_lineages_required_for_80pct_power['0.2']"),
        cf("n_lineages_required_for_80pct_at_0.10",
           power["n_lineages_required_for_80pct_power"]["0.1"], "A5/numbers.json",
           "power.n_lineages_required_for_80pct_power['0.1'] (null = unreachable up to 300)"),
        cf("falsifier_could_have_failed", power["falsifier_could_have_failed"], "A5/numbers.json",
           "power.falsifier_could_have_failed"),
        cf("B08_first_token_entropy_asymmetry_abs_rho_lineage", abs(b08_l["rho"]), "A5/numbers.json",
           "correlations.lineage.B08_first_token_entropy_asymmetry.harmful_refusal_rate.rho"),
        cf("B01_logit_gap_harmful_abs_rho_member", abs(b01_m["rho"]), "A5/numbers.json",
           "correlations.member.B01_logit_gap_harmful.harmful_refusal_rate.rho"),
        cf("B09_abs_rho_member", abs(b09_m["rho"]), "A5/numbers.json",
           "correlations.member.B09_greedy_refusal_rate_harmful.harmful_refusal_rate.rho"),
        cf("B09_in_resample_argmax_share_member", b09_argmax_member, "A5/numbers.json",
           "selection_corrected_comparator.member.harmful_refusal_rate.B09_wins_fraction_of_resamples"),
        cf("B09_in_resample_argmax_share_lineage", b09_argmax_lineage, "A5/numbers.json",
           "selection_corrected_comparator.lineage.harmful_refusal_rate.B09_wins_fraction_of_resamples"),
        cf("selection_optimism_lineage", optimism_lineage, "A5/numbers.json",
           "selection_corrected_comparator.lineage.harmful_refusal_rate."
           "mean_abs_rho_reselected_winner - mean_abs_rho_fixed_B09"),
        cf("observed_best_blackbox_lineage",
           sel["lineage"]["harmful_refusal_rate"]["observed_best_blackbox"], "A5/numbers.json",
           "selection_corrected_comparator.lineage.harmful_refusal_rate.observed_best_blackbox"),
        cf("observed_best_blackbox_abs_rho_lineage",
           sel["lineage"]["harmful_refusal_rate"]["observed_best_abs_rho"], "A5/numbers.json",
           "selection_corrected_comparator.lineage.harmful_refusal_rate.observed_best_abs_rho"),
        cf("A19_near_win_rho_at_rho_star",
           next((e["metric_rho"] for e in a1_arm3_nominal
                 if e["metric"] == "A19_refusal_axis_unembed_cosine"
                 and e["baseline"] == "B09_greedy_refusal_rate_harmful"), None),
           "A1/full_method_out.json", "metadata.arm3.activation_beats_blackbox_nominally"),
        cf("B09_rho_at_rho_star",
           next((e["baseline_rho"] for e in a1_arm3_nominal
                 if e["metric"] == "A19_refusal_axis_unembed_cosine"
                 and e["baseline"] == "B09_greedy_refusal_rate_harmful"), None),
           "A1/full_method_out.json", "metadata.arm3.activation_beats_blackbox_nominally"),
        cf("n_activation_metrics_with_paired_ci_excluding_zero",
           len(m1["metadata"]["arm3"].get("activation_beats_blackbox_paired_ci_excludes_zero", []))
           if m1 else None,
           "A1/full_method_out.json", "metadata.arm3.activation_beats_blackbox_paired_ci_excludes_zero"),
        cf("arm3_depth_long_table_rows", m1["metadata"]["arm3"].get("n_rows") if m1 else None,
           "A1/full_method_out.json", "metadata.arm3.n_rows"),
        cf("split_half_r_xx", rel["split_half_odd_even_core40"]["spearman_brown_r_xx_from_spearman"],
           "A5/numbers.json", "reliability.split_half_odd_even_core40.spearman_brown_r_xx_from_spearman"),
        cf("attenuation_correction_factor", numbers["attenuation"]["correction_factor"],
           "A5/numbers.json", "attenuation.correction_factor"),
        cf("attenuation_ordering_moved", numbers["attenuation"]["ordering_moved"],
           "A5/numbers.json", "attenuation.ordering_moved"),
        cf("BLACKBOX_WINS_invariant_across_depth", depth.get("falsifier_invariant_across_depth"),
           "A5/numbers.json", "depth.falsifier_invariant_across_depth"),
        cf("A19_rho_member", a19_m["rho"], "A5/numbers.json",
           "correlations.member.A19_refusal_axis_unembed_cosine.harmful_refusal_rate.rho"),
        cf("A19_ci_member", a19_m["ci95"], "A5/numbers.json",
           "correlations.member.A19_refusal_axis_unembed_cosine.harmful_refusal_rate.ci95"),
        cf("A19_rho_lineage", a19_l["rho"], "A5/numbers.json",
           "correlations.lineage.A19_refusal_axis_unembed_cosine.harmful_refusal_rate.rho"),
        cf("A19_minus_B09_paired_difference_member", a19_vs_b09["point"],
           "A1/full_method_out.json",
           "metadata.arm3.activation_beats_blackbox_nominally[A19 vs B09 @ rho*].paired_diff"),
        cf("A19_minus_B09_paired_difference_ci", a19_vs_b09["ci95"],
           "A1/full_method_out.json",
           "metadata.arm3.activation_beats_blackbox_nominally[A19 vs B09 @ rho*].paired_ci"),
    ]

    # ---------------- M4.3 subset correction ----------------
    qvf = numbers["quoted_value_forensics"]
    close = qvf["closest_match_per_quoted_value"]
    subset_rows: list[dict[str, Any]] = []
    for mid, rec in close.items():
        conv = rec["closest_convention"]
        is_renderer = conv.startswith("member_chatml_renderer")
        true_rho = corr["member"].get(mid, {}).get("harmful_refusal_rate", {}).get("rho")
        subset_rows.append(
            {
                "metric_id": mid,
                "draft_quoted_value": rec["quoted"],
                "what_it_actually_is": (
                    "a correlation computed on the 26-member renderer=='chatml' subset, NOT the "
                    "28-member non-base subset the draft states"
                    if is_renderer else
                    f"not reproduced under ANY of the {rec['n_conventions_tried']} conventions searched; "
                    f"closest is '{conv}' at n={rec['n']}"
                ),
                "value_under_the_closest_convention": rec["rho_under_that_convention"],
                "correct_value_as_a_correlation_contract_subset": true_rho,
                "subset_n_of_closest_convention": rec["n"],
                "subset_n_quoted_implicitly": rec["n"] if rec["reproduced_within_0.005"] else None,
                "subset_n_stated_in_draft": 28,
                "abs_gap": rec["abs_gap"],
                "reproduced_within_0.005": rec["reproduced_within_0.005"],
                "sign_error_flag": (
                    true_rho is not None and rec["quoted"] is not None
                    and (true_rho < 0) != (rec["quoted"] < 0)
                ),
                "corrected_draft_sentence": (
                    (
                        f"{mid}: rho = {true_rho:+.3f} on the 28-member contract subset. The "
                        f"previously quoted {rec['quoted']:+.3f} is the value on the {rec['n']}-member "
                        f"renderer=='chatml' subset, which reproduces to "
                        f"{rec['abs_gap']:.4f} - the number was right, the SUBSET LABEL was not."
                    ) if rec["reproduced_within_0.005"] else (
                        f"{mid}: rho = {true_rho:+.3f} on the 28-member contract subset. The "
                        f"previously quoted {rec['quoted']:+.3f} does NOT reproduce under any of the "
                        f"{rec['n_conventions_tried']} (subset, target, unit) conventions searched "
                        f"(closest: '{conv}' at n={rec['n']}, gap {rec['abs_gap']:.4f}), so it cannot "
                        f"be recovered from the archived artifacts and must be regenerated from "
                        f"numbers.json rather than transcribed."
                    )
                ) if true_rho is not None else (
                    f"{mid}: the quoted {rec['quoted']:+.3f} has no counterpart in the correlation "
                    f"tables and must be regenerated from numbers.json."
                ),
                "closest_convention_searched": conv,
                "n_conventions_searched": rec["n_conventions_tried"],
                "carried_forward_with_recheck": True,
            }
        )
    falsifier_both = {
        "verdict_on_28_member_contract_subset": "BLACKBOX_WINS",
        "verdict_on_26_member_renderer_subset": "BLACKBOX_WINS",
        "basis": (
            "No candidate BEATS B09: every paired candidate-minus-B09 CI that excludes zero does so "
            "on the NEGATIVE side (W02 at -0.457 [-0.736, -0.023], i.e. significantly WORSE), and no "
            "activation metric's paired difference excludes zero in the positive direction under "
            "either subset rule. The depth arm at rho* = 0.679 adds zero positive exclusions over 26 "
            "members."
        ),
        "n_paired_differences_excluding_zero_on_the_POSITIVE_side": sum(
            1 for v in pdiff["member"]["harmful_refusal_rate"].values()
            if isinstance(v, dict) and v.get("vs_B09_posthoc", {}).get("excludes_zero")
            and (v["vs_B09_posthoc"].get("point") or 0) > 0
        ),
        "n_paired_differences_excluding_zero_member": sum(
            1 for v in pdiff["member"]["harmful_refusal_rate"].values()
            if isinstance(v, dict) and v.get("vs_B09_posthoc", {}).get("excludes_zero")
        ),
        "n_paired_differences_tested_member": len(pdiff["member"]["harmful_refusal_rate"]),
        "n_depth_arm_paired_differences_excluding_zero": len(
            m1["metadata"]["arm3"].get("activation_beats_blackbox_paired_ci_excludes_zero", [])
        ) if m1 else None,
    }

    # ---------------- M4.4 practitioner sentence ----------------
    sentence = (
        f"Interior observables ARE predictive of harmful-refusal rate (A19: rho {a19_m['rho']:+.3f} "
        f"[{a19_m['ci95'][0]:+.3f}, {a19_m['ci95'][1]:+.3f}] member, {a19_l['rho']:+.3f} lineage, "
        f"comparable to B01 and better than B09) - they simply do not beat a 40-prompt greedy refusal "
        f"rate, which is already the cheapest thing anyone would run. The falsifier is about marginal "
        f"value over a cheaper instrument, not about whether interior observables carry signal."
    )
    sentence_bindings = {
        "A19 rho member": prov("A5/numbers.json",
                               "correlations.member.A19_refusal_axis_unembed_cosine.harmful_refusal_rate.rho",
                               a19_m["rho"]),
        "A19 ci member": prov("A5/numbers.json",
                              "correlations.member.A19_refusal_axis_unembed_cosine.harmful_refusal_rate.ci95",
                              a19_m["ci95"]),
        "A19 rho lineage": prov("A5/numbers.json",
                                "correlations.lineage.A19_refusal_axis_unembed_cosine.harmful_refusal_rate.rho",
                                a19_l["rho"]),
        "B01 rho member": prov("A5/numbers.json",
                               "correlations.member.B01_logit_gap_harmful.harmful_refusal_rate.rho",
                               b01_m["rho"]),
        "B09 rho member": prov("A5/numbers.json",
                               "correlations.member.B09_greedy_refusal_rate_harmful.harmful_refusal_rate.rho",
                               b09_m["rho"]),
        "40-prompt core": prov("A3/full_method_out.json", "metadata.prompt_subsets", "CORE40"),
    }

    cheapest_blackbox = next((r for r in rows if r["family"] == "blackbox"), None)
    return {
        "status": "OK",
        "metric_spec_sha256": spec_sha,
        "metric_spec_sha256_prefix": spec_sha[:8],
        "n_metrics_declared": len(spec),
        "sorted_by": "cost ascending (harmful prompts, then forward passes, then measured wall clock)",
        "behavioural_cost_table": rows,
        "cheapest_row": rows[0]["metric_id"] if rows else None,
        "cheapest_blackbox_row": cheapest_blackbox["metric_id"] if cheapest_blackbox else None,
        "carry_forward": carry,
        "subset_correction": {
            "rows": subset_rows,
            "n_rows": len(subset_rows),
            "falsifier_verdict_on_both_subsets": falsifier_both,
            "note": "This is carry-forward with a re-check, not a re-derivation.",
        },
        "practitioner_sentence": sentence,
        "practitioner_sentence_bindings": sentence_bindings,
    }
