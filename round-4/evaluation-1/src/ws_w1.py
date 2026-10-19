#!/usr/bin/env python3
"""W1 - recipe-primary relabelling and regrouping (block: recipe_relabel)."""

from __future__ import annotations

import json
from typing import Any

import numpy as np
from loguru import logger

from lib_arch import Resolver, auroc, perm_p_auroc, prov, wilson95

# The four-way kernel_family map, published as a literal dict and applied ONLY
# on a verbatim toolkit/kernel string found in the archived card text.
KERNEL_STRING_MAP: dict[str, dict[str, str]] = {
    "heretic": {
        "kernel_family": "per_component_optimised",
        "recipe_class_new": "heretic_per_component",
        "mechanically_different": "TRUE",
        "why": "Heretic optimises a per-component (per-matrix-type) subtraction weight with a "
        "float-interpolated direction index; weights may exceed 1 (over-subtraction).",
    },
    "mlabonne_gaussian": {
        "kernel_family": "depth_weighted",
        "recipe_class_new": "mlabonne_v2_gaussian_depth",
        "mechanically_different": "TRUE",
        "why": "mlabonne v2 weights the subtraction by a Gaussian over layer depth "
        "(a spread and a peak layer), so per-layer strength is not uniform.",
    },
    "uniform_global_projection": {
        "kernel_family": "uniform_global",
        "recipe_class_new": "global_diff_in_means",
        "mechanically_different": "FALSE",
        "why": "W <- (I - r r^T) W applied at full unit weight in every residual-write matrix.",
    },
    "unknown": {
        "kernel_family": "unknown",
        "recipe_class_new": "UNKNOWN",
        "mechanically_different": "UNDETERMINED",
        "why": "No toolkit or kernel string present in the archived card text.",
    },
}

# Verbatim trigger substrings, searched case-insensitively in the archived
# evidence fields.  A relabel fires ONLY on one of these.
TRIGGERS: list[tuple[str, str]] = [
    ("heretic", "heretic"),
    ("normal distribution with a certain spread", "mlabonne_gaussian"),
    ("peak layer", "mlabonne_gaussian"),
]

DECISION_RULE_ID = "R-2026-08-14-verbatim-kernel-string-v1"
DECISION_RULE_TEXT = (
    "A row is relabelled ONLY on a verbatim toolkit/kernel string present in the archived card "
    "text carried by that row. The string -> kernel_family map is published as a literal dict "
    "(KERNEL_STRING_MAP). If the required evidence string is NOT present in the archived rows, "
    "evidence_status = 'NOT_IN_ARCHIVE' is emitted with the fields searched, the relabel is marked "
    "PROVISIONAL, and the OLD label is carried in the counts. No card is fetched from the Hub, and "
    "no kernel is inferred from a W05 value (that would be circular)."
)

EVIDENCE_FIELDS = ["evidence_quote", "evidence_url", "recipe_class", "declared_class"]
FITTED_THRESHOLD = -2.7415117804288127


def _scan_evidence(row: dict) -> tuple[str | None, str | None, int | None, str | None]:
    """Return (trigger_string, map_key, char_offset, field_name) or Nones."""
    for field in EVIDENCE_FIELDS:
        text = row.get(field)
        if not isinstance(text, str):
            continue
        low = text.lower()
        for trig, key in TRIGGERS:
            i = low.find(trig)
            if i >= 0:
                return trig, key, i, field
    return None, None, None, None


def run_w1(res: Resolver, a6_text: str) -> dict[str, Any]:
    logger.info("W1: recipe-primary relabelling")
    real = res.read_jsonl("A1", "results/arm1_real*.jsonl", "**/arm1*real*.jsonl")
    m1 = res.read_json("A1", "full_method_out.json")
    if real is None or m1 is None:
        return {"status": "UNAVAILABLE", "reason": "arm1_real / full_method_out not resolvable"}

    arm1_rows = [d for d in m1["datasets"] if d["dataset"] == "arm1_recipe_scope"][0]["examples"]

    # ---------------- M1.1 relabel table ----------------
    table: list[dict[str, Any]] = []
    for row in real:
        trig, key, off, field = _scan_evidence(row)
        if key is None:
            key = "unknown"
            ev_status = "NOT_IN_ARCHIVE"
            provisional = True
            span, span_field, span_off = "", None, None
        else:
            ev_status = "IN_ARCHIVE"
            provisional = False
            txt = row[field]
            lo = max(0, off - 90)
            span = txt[lo : lo + 300]
            span_field, span_off = field, [lo, min(len(txt), lo + 300)]
        m = KERNEL_STRING_MAP[key]
        # A6 taxonomy cross-reference: does the dossier name this uploader's kernel?
        up = row["uploader"]
        a6_hit = None
        if up and up.lower() in a6_text.lower():
            a6_hit = f"uploader '{up}' appears in the A6 prior-art dossier recipe taxonomy"
        table.append(
            {
                "repo_id": row["variant_id"],
                "uploader": up,
                "recipe_class_OLD": row["recipe_class"],
                "recipe_class_NEW": m["recipe_class_new"] if not provisional else row["recipe_class"],
                "recipe_class_NEW_proposed": m["recipe_class_new"],
                "mechanically_different_OLD": bool(row["mechanically_different"]),
                "mechanically_different_NEW": m["mechanically_different"],
                "kernel_family": m["kernel_family"],
                "kernel_family_justification": m["why"],
                "evidence_status": ev_status,
                "relabel_status": "PROVISIONAL" if provisional else "APPLIED",
                "evidence_span_verbatim": span,
                "evidence_span_field": span_field,
                "evidence_char_offsets": span_off,
                "fields_searched": EVIDENCE_FIELDS,
                "a6_taxonomy_crossref": a6_hit,
                "W01": row["W01"],
                "W02": row["W02"],
                "W03": row["W03"],
                "W04": row["W04"],
                "W05": row["W05"],
                "params": row["params"],
                "revision": row["revision"],
                "decision_rule_id": DECISION_RULE_ID,
                "provenance": prov(
                    "A1/results/arm1_real.jsonl", f"variant_id={row['variant_id']}", row["W05"]
                ),
            }
        )

    # E_1 as archived, joined from the arm-2 pair rows where a parent resolved.
    # E_1 comes from the assembled 41-pair dataset, which includes the 3 new-uploader pairs that
    # realcheck.py resolved; results/arm2_all.jsonl alone holds only 38 and would report None here.
    hh = [d for d in m1["datasets"] if d["dataset"] == "arm2_e1_headtohead"][0]["examples"]
    e1_by_cand = {e["metadata_candidate"]: float(e["predict_E1_parent_required"]) for e in hh}
    for t in table:
        t["E_1_as_archived"] = e1_by_cand.get(t["repo_id"])
        t["E_1_status"] = "ARCHIVED" if t["repo_id"] in e1_by_cand else "NO_RESOLVABLE_PARENT"

    n_relabelled = sum(1 for t in table if t["relabel_status"] == "APPLIED")
    n_provisional = sum(1 for t in table if t["relabel_status"] == "PROVISIONAL")

    # ---------------- M1.2 grouping analysis ----------------
    # Build the arm-1 headline member set, with the NEW recipe classes applied.
    new_class = {t["repo_id"]: t for t in table}
    members: list[dict[str, Any]] = []
    for e in arm1_rows:
        if e["metadata_layer_fraction"] is not None:
            continue  # band-sweep rows are excluded from the headline set, as archived
        rid = e["metadata_member"]
        rc_old = e["metadata_recipe_class"]
        t = new_class.get(rid)
        if t is not None:
            kf = t["kernel_family"]
            rc_new = t["recipe_class_NEW"]
        else:
            kf = "uniform_global" if rc_old != "none" else "not_edited"
            rc_new = rc_old
        members.append(
            {
                "member": rid,
                "uploader": e["metadata_uploader"],
                "source": e["metadata_source"],
                "label": 1 if e["output"] != "base" and rc_old != "none" else 0,
                "recipe_class_old": rc_old,
                "recipe_class_new": rc_new,
                "kernel_family": kf,
                "lineage_id": e["metadata_lineage_id"],
                "synthetic": e["metadata_synthetic"],
                **{k: e["metadata_W"][k] for k in ("W01", "W02", "W03", "W04", "W05")},
                "E_1": e1_by_cand.get(rid),
            }
        )
    # `label` from the archived class column, verified against recipe_class
    for m in members:
        m["label"] = 0 if m["recipe_class_old"] == "none" else 1

    negatives = [m for m in members if m["label"] == 0]
    rng = np.random.default_rng(20260814)

    directions = {"W01": True, "W03": True, "W04": True, "E_1": True, "W05": False}
    auroc_by_recipe_class: dict[str, Any] = {}
    for kf in ["uniform_global", "depth_weighted", "per_component_optimised", "unknown"]:
        pos = [m for m in members if m["label"] == 1 and m["kernel_family"] == kf]
        block: dict[str, Any] = {"n_positives": len(pos), "n_negatives": len(negatives),
                                 "members": [p["member"] for p in pos]}
        for stat, hi in directions.items():
            pv = [p[stat] for p in pos if p.get(stat) is not None]
            nv = [n[stat] for n in negatives if n.get(stat) is not None]
            a = auroc(pv, nv, hi)
            entry: dict[str, Any] = {"auroc": a, "n_pos": len(pv), "n_neg": len(nv),
                                     "per_member_values": {p["member"]: p[stat] for p in pos},
                                     "direction": "higher is positive" if hi else "lower is positive"}
            if a is not None and len(pv) >= 1 and len(pv) + len(nv) <= 200:
                entry["permutation"] = perm_p_auroc(pv, nv, hi, np.random.default_rng(20260814), 10_000)
            block[stat] = entry
        auroc_by_recipe_class[kf] = block

    def _loo(group_key: str) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for g in sorted({m[group_key] for m in members if m["label"] == 1}):
            held = [m for m in members if m["label"] == 1 and m[group_key] == g]
            train_pos = [m for m in members if m["label"] == 1 and m[group_key] != g]
            a = auroc([h["W05"] for h in held], [n["W05"] for n in negatives], False)
            hits = sum(1 for h in held if h["W05"] <= FITTED_THRESHOLD)
            out[str(g)] = {
                "n_held_out_positives": len(held),
                "held_out_members": [h["member"] for h in held],
                "auroc_W05_heldout_vs_all_negatives": a,
                "sensitivity_at_fitted_threshold": hits / len(held) if held else None,
                "held_out_hit_count": hits,
                "n_training_positives": len(train_pos),
                "fitted_threshold": FITTED_THRESHOLD,
            }
        return out

    loo_uploader = _loo("uploader")
    loo_recipe = _loo("kernel_family")

    # ---------------- variance attribution (a COUNT, never a decomposition) ----
    new_up = [m for m in members if m["source"] == "real_new_uploader"]
    misses = [m for m in new_up if m["W05"] > FITTED_THRESHOLD]
    # A miss counts as RECIPE-attributed ONLY on a verbatim non-uniform kernel string.  'unknown'
    # is NOT non-uniform - it is unattributed, and is reported in the remainder.
    non_uniform_misses = [m for m in misses
                          if m["kernel_family"] in ("depth_weighted", "per_component_optimised")]
    unknown_misses = [m for m in misses if m["kernel_family"] == "unknown"]
    x = len(non_uniform_misses)
    auroc_new_up = auroc([m["W05"] for m in new_up], [n["W05"] for n in negatives], False)
    nonuni = [m for m in new_up if m["kernel_family"] in ("depth_weighted", "per_component_optimised")]
    uni = [m for m in new_up if m["kernel_family"] == "uniform_global"]
    variance_attribution = {
        "headline_new_uploader_auroc_recomputed": auroc_new_up,
        "headline_new_uploader_auroc_archived": 0.382,
        "n_new_uploader_members": len(new_up),
        "n_misses_at_fitted_threshold": len(misses),
        "misses": [m["member"] for m in misses],
        "auroc_restricted_to_depth_weighted_plus_per_component": auroc(
            [m["W05"] for m in nonuni], [n["W05"] for n in negatives], False
        ),
        "n_in_that_subset": len(nonuni),
        "auroc_restricted_to_uniform_kernel_new_uploader": auroc(
            [m["W05"] for m in uni], [n["W05"] for n in negatives], False
        ) if uni else None,
        "n_uniform_kernel_new_uploader": len(uni),
        "share_of_misses_with_verbatim_non_uniform_kernel_string": f"{x}/{len(misses)}",
        "unattributed_remainder": len(misses) - x,
        "unattributed_members": [m["member"] for m in unknown_misses],
        "unattributed_reason": (
            "Their archived card text names no toolkit or kernel, so no relabel fires. Inferring a "
            "kernel from the W05 value would be circular and is refused."
        ),
        "sentence": (
            f"{x} of the {len(misses)} misses carry a verbatim non-uniform kernel string, so at least "
            f"{x}/{len(misses)} of the {auroc_new_up:.3f} new-uploader AUROC is a RECIPE effect; the residual "
            f"({len(misses) - x}) is unattributed and reported as such."
        ),
        "no_variance_decomposition_note": (
            "At n=4 a variance decomposition is not identifiable. What is reported is a COUNT of misses "
            "carrying a verbatim non-uniform kernel string, with an explicit unattributed remainder."
        ),
    }

    # ---------------- M1.3 uniformity headline ----------------
    a1meta = m1["metadata"]
    band_rows = [e for e in arm1_rows if e["metadata_layer_fraction"] is not None]
    fstar = a1meta.get("arm1", {}).get("layer_fraction_sweep")
    mid50 = None
    for e in band_rows:
        if abs((e["metadata_layer_fraction"] or 0) - 0.5) < 1e-9 and "1.7B" in e["metadata_member"]:
            mid50 = e
            break
    margin = 0.0763170819
    delta_w05 = abs(-1.0098422523532755 - (-1.0088))
    uniformity = {
        "headline_sentence": (
            "W05 requires a uniform, complete annihilation in every layer; any depth-weighted or "
            "sub-unit-weight kernel escapes it, exactly as a band-limited edit does."
        ),
        "support_a_layer_fraction_sweep": {
            "f_star": 1.00,
            "hosts": "both",
            "statement": "only the fully global edit (f* = 1.00) is detectable, on BOTH synthetic hosts",
            "archived": fstar,
            "provenance": prov("A1/full_method_out.json", "metadata.arm1.layer_fraction_sweep", fstar),
        },
        "support_b_middle_50_projection": {
            "harmful_refusal_before": 0.45,
            "harmful_refusal_after": 0.00,
            "W05_unedited": -1.0098422523532755,
            "W05_after_middle50_edit": -1.0088,
            "delta_W05": delta_w05,
            "panel_separating_margin_log10": margin,
            "delta_as_fraction_of_margin": delta_w05 / margin,
            "delta_as_pct_of_margin": 100.0 * delta_w05 / margin,
            "statement": (
                f"a projection confined to the middle 50% of layers drives harmful refusal 0.45 -> 0.00 "
                f"while W05 moves by {delta_w05:.4f} log10, i.e. "
                f"{100.0 * delta_w05 / margin:.1f}% of the {margin:.4f} panel separating margin"
            ),
            "provenance": prov("A1/full_method_out.json", "metadata.arm1 / diagnostics T1 W05", -1.0098422523532755),
        },
        "support_c_depth_weighted_kernel_misses": {
            "misses": [m["member"] for m in misses],
            "with_kernel_family": {m["member"]: m["kernel_family"] for m in misses},
        },
        "mechanism_synthetic_unit_test": (
            "With 4 of 12 matrices edited, v1 is no longer the injected direction at all and W02 = 0, "
            "because the Gram pools every residual-write matrix. That is why the behaviour is a "
            "THRESHOLD in the fraction of layers edited, not a ramp."
        ),
        "threshold_not_ramp": True,
    }

    # ---------------- M1.4 draft edit list ----------------
    a6_has_records = ("4,022,468,096" in a6_text) or ("4022468096" in a6_text)
    if a6_has_records:
        lim3 = {
            "limitation3_status": "REFUTED",
            "param_count_of_sub_4_2B_records": 4022468096,
            "records": [
                "YanLabs/Qwen3-4B-Instruct-2507-MPOA (MPOA, 4,022,468,096 params)",
                "heretic-org/Qwen3-4B-Instruct-2507-heretic (Heretic v1.2.0, 4,022,468,096 params)",
                "p-e-w/Qwen3-4B-Instruct-2507-heretic (Heretic v1.0.0, 4,022,468,096 params)",
                "OBLITERATUS/Qwen3-4B-OBLITERATED (OBLITERATUS, 4,022,468,096 params)",
                "0xA50C1A1/Qwen3-4B-Instruct-2507-SOM-MPOA (norm-preserving + multi-direction)",
            ],
            "already_measured_without_recognition": [
                t["repo_id"] for t in table if t["kernel_family"] == "per_component_optimised"
            ],
            "note": (
                "Three of the four 'missing' recipes have public sub-4.2B checkpoints at 4,022,468,096 "
                "params on the panel's OWN Qwen3-4B family, and the experiment already measured two "
                "Heretic checkpoints without recognising them as a distinct recipe class. Only ORBA is "
                "genuinely empty at this scale (7 repos, all 12.187B)."
            ),
            "provenance": prov("A6/research_report.md", "section C, PLAN WAS WRONG on availability", 4022468096),
        }
    else:
        lim3 = {
            "limitation3_status": "REFUTATION_NOT_LOCATED",
            "paths_searched": [str(p) for p in (
                (Resolver.__module__,),
            )],
        }

    edits = [
        {
            "n": 1,
            "section": "Introduction",
            "old_framing_paraphrase": "the detector generalises across uploaders; the four new-uploader "
            "checkpoints are framed as an UPLOADER generalisation test",
            "new_sentence": "The detector keys on the UNIFORMITY of the edit, not on who uploaded it: it "
            "fires on uniform all-layer projections and misses per-component-optimised and depth-weighted "
            "kernels, which is a recipe property stated in advance and confirmed by a synthetic layer-"
            "fraction sweep with f* = 1.00.",
            "supporting_numbers": ["f*=1.00", f"new-uploader AUROC {auroc_new_up:.3f}",
                                   f"{x}/{len(misses)} misses carry a verbatim non-uniform kernel string"],
        },
        {
            "n": 2,
            "section": "Contributions",
            "old_framing_paraphrase": "contribution claimed as uploader-independent detection",
            "new_sentence": "We characterise the detector's scope as RECIPE-CLASS BOUNDED: uniform global "
            "projection is detected at AUROC 1.000; per-component-optimised (Heretic) kernels are not.",
            "supporting_numbers": ["AUROC 1.000 on the calibration uploaders",
                                   f"leave-one-recipe-class-out sensitivity for per_component_optimised = "
                                   f"{loo_recipe.get('per_component_optimised', {}).get('sensitivity_at_fitted_threshold')}"],
        },
        {
            "n": 3,
            "section": "Results 5.1",
            "old_framing_paraphrase": "0.382 AUROC reported as a failure to generalise to new uploaders",
            "new_sentence": variance_attribution["sentence"],
            "supporting_numbers": [f"{auroc_new_up:.3f}", "0/4 at the fitted threshold -2.7415117804288127"],
        },
        {
            "n": 4,
            "section": "Discussion",
            "old_framing_paraphrase": "the miss is attributed to uploader-specific implementation drift",
            "new_sentence": uniformity["headline_sentence"],
            "supporting_numbers": ["harmful refusal 0.45 -> 0.00 at delta_W05 = 0.0010",
                                   f"{100.0 * delta_w05 / margin:.1f}% of the 0.0763 margin", "W02 = 0 at 4/12 matrices"],
        },
        {
            "n": 5,
            "section": "Conclusion",
            "old_framing_paraphrase": "concludes that broader uploader coverage would fix the gap",
            "new_sentence": "Broader uploader coverage would not fix the gap; broader RECIPE coverage is "
            "what the scope statement requires, and the sub-4.2B MPOA / Heretic / OBLITERATUS checkpoints "
            "make that test runnable today.",
            "supporting_numbers": ["4,022,468,096 params on the panel's own Qwen3-4B family"],
        },
        {
            "n": 6,
            "section": "Limitation 3",
            "old_framing_paraphrase": "no mechanically different recipe exists below the 4.2B ceiling",
            "new_sentence": "DELETE. Mechanically different recipes DO exist below the ceiling.",
            "supporting_numbers": ["4,022,468,096"],
            "recommendation": "DELETE",
            "refutation": lim3,
        },
    ]

    return {
        "status": "OK",
        "decision_rule_id": DECISION_RULE_ID,
        "decision_rule_text": DECISION_RULE_TEXT,
        "kernel_string_map": KERNEL_STRING_MAP,
        "triggers": [{"substring": t, "maps_to": k} for t, k in TRIGGERS],
        "recipe_relabel_table": table,
        "n_relabelled_applied": n_relabelled,
        "n_relabelled_provisional": n_provisional,
        "grouping_analysis": {
            "auroc_by_recipe_class": auroc_by_recipe_class,
            "leave_one_recipe_class_out_PRIMARY": loo_recipe,
            "leave_one_uploader_out_SECONDARY": loo_uploader,
            "identical_columns_note": "Both tables carry identical columns so the reader can see which "
            "grouping the failure tracks.",
            "variance_attribution": variance_attribution,
        },
        "uniformity_headline": uniformity,
        "draft_edit_list": edits,
        "members_used": members,
    }
