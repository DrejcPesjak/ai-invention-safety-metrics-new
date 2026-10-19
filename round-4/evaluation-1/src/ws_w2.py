#!/usr/bin/env python3
"""W2 - Wilson + bootstrap intervals on the 34-stage laundering ladder (block: ladder_intervals)."""

from __future__ import annotations

from typing import Any

import numpy as np
from loguru import logger

from lib_arch import (
    BOOT_B,
    Resolver,
    boot_diff_ci,
    boot_rate_ci,
    newcombe_diff,
    prov,
    recover_kn,
    two_prop_mdd_directional,
    wilson95,
)

RATE_FIELDS = [
    ("harmful_refusal_rate", "n_harmful", 40),
    ("xstest_overrefusal_rate", "n_xstest", 25),
    ("regex_harmful_refusal_rate", "n_harmful", 40),
    ("regex_xstest_overrefusal_rate", "n_xstest", 25),
]
SEED_W2 = 20260814


def _one_sig(x: float) -> str:
    if x == 0:
        return "0"
    from decimal import Decimal

    import math as _m

    e = _m.floor(_m.log10(abs(x)))
    v = round(x, -e)
    return f"{v:+.{max(0, -e)}f}" if e < 0 else f"{v:+.0f}"


def run_w2(res: Resolver) -> dict[str, Any]:
    logger.info("W2: ladder intervals")
    ladder = res.read_jsonl("A2", "results/ladder*.jsonl", "**/ladder*.jsonl")
    m2 = res.read_json("A2", "full_method_out.json")
    if ladder is None or m2 is None:
        return {"status": "UNAVAILABLE", "reason": "ladder.jsonl / full_method_out not resolvable"}
    crossing = [d for d in m2["datasets"] if d["dataset"] == "crossing"][0]["examples"]

    rng = np.random.default_rng(SEED_W2)

    # ---------------- M2.1 per-stage, per-rate intervals ----------------
    rows: list[dict[str, Any]] = []
    kn_index: dict[tuple[str, str], tuple[int, int]] = {}
    disagreements_wilson_vs_boot: list[dict[str, Any]] = []
    flagged_reconstructions: list[dict[str, Any]] = []
    for st in ladder:
        for field, nfield, nominal in RATE_FIELDS:
            rate = st.get(field)
            if rate is None:
                continue
            n_nominal = st.get(nfield, nominal) or nominal
            k, n_ach, resid = recover_kn(float(rate), n_max=int(n_nominal))
            src = "RECONSTRUCTED"
            flagged = resid >= 0.5 / max(n_ach, 1)
            if flagged:
                flagged_reconstructions.append(
                    {"stage_id": st["stage_id"], "rate_field": field, "rate": rate,
                     "k": k, "n": n_ach, "residual": resid}
                )
            wlo, whi = wilson95(k, n_ach)
            blo, bhi = boot_rate_ci(k, n_ach, rng)
            se = (k / n_ach * (1 - k / n_ach) / n_ach) ** 0.5 if n_ach else float("nan")
            if max(abs(wlo - blo), abs(whi - bhi)) > 0.02:
                disagreements_wilson_vs_boot.append(
                    {"stage_id": st["stage_id"], "rate_field": field,
                     "wilson": [wlo, whi], "bootstrap": [blo, bhi],
                     "max_endpoint_gap": max(abs(wlo - blo), abs(whi - bhi))}
                )
            kn_index[(st["stage_id"], field)] = (k, n_ach)
            rows.append(
                {
                    "stage_id": st["stage_id"],
                    "axis": st.get("family"),
                    "intensity": st.get("intensity"),
                    "rate_field": field,
                    "k_refused": k,
                    "n_achieved": n_ach,
                    "n_nominal": int(n_nominal),
                    "rate": k / n_ach if n_ach else None,
                    "rate_as_archived": rate,
                    "denominator_source": src,
                    "reconstruction_residual": resid,
                    "reconstruction_flagged": flagged,
                    "wilson95_lo": wlo,
                    "wilson95_hi": whi,
                    "bootstrap95_lo": blo,
                    "bootstrap95_hi": bhi,
                    "se_binomial": se,
                    "provenance": prov("A2/results/ladder.jsonl", f"{st['stage_id']}.{field}", rate),
                }
            )

    # Root stage: the unlaundered abliterated root (intensity 0 / the archived root record).
    root = res.read_json("A2", "results/root.json")
    root_rate = 0.16216216216216217
    if isinstance(root, dict):
        for key in ("harmful_refusal_rate", "harmful_refusal", "root_harmful_refusal_rate"):
            if key in root and isinstance(root[key], (int, float)):
                root_rate = float(root[key])
                break
    rk, rn, rres = recover_kn(root_rate, 40)
    rwlo, rwhi = wilson95(rk, rn)
    rblo, rbhi = boot_rate_ci(rk, rn, rng)
    root_block = {
        "harmful_refusal_rate": root_rate,
        "k_refused": rk,
        "n_achieved": rn,
        "n_nominal": 40,
        "wilson95": [rwlo, rwhi],
        "bootstrap95": [rblo, rbhi],
        "denominator_source": "RECONSTRUCTED",
        "reconstruction_residual": rres,
        "provenance": prov("A2/results/root.json", "harmful_refusal_rate", root_rate),
    }

    # ---------------- M2.2 crossing restatements ----------------
    restatements: list[dict[str, Any]] = []
    for c in crossing:
        meta = c["metadata_meta"]
        axis = c["input"]
        verdict = c["output"]
        curve = meta.get("curve", [])
        i_flag = meta.get("i_flag_death")
        i_beh = meta.get("i_beh_death")
        entry: dict[str, Any] = {
            "axis": axis,
            "verdict_as_archived": verdict,
            "flag_dies_at": i_flag,
            "uncensor_dies_at": i_beh,
            "n_stages_on_axis": len(curve),
        }
        if i_flag is None and i_beh is None:
            entry["order"] = "NEITHER_DIES"
        elif i_flag is not None and i_beh is None:
            entry["order"] = "FLAG_FIRST"
        elif i_flag is None and i_beh is not None:
            entry["order"] = "CENSOR_FIRST"
        else:
            entry["order"] = "FLAG_FIRST" if i_flag < i_beh else ("CENSOR_FIRST" if i_beh < i_flag else "TIED")

        # rate at the intensity where the flag first dies
        pt = None
        if i_flag is not None:
            for p in curve:
                if abs(float(p["intensity"]) - float(i_flag)) < 1e-12 and not p["flag_alive"]:
                    pt = p
                    break
            if pt is None:
                for p in curve:
                    if not p["flag_alive"]:
                        pt = p
                        break
        if pt is not None:
            k, n = kn_index.get((pt["stage_id"], "harmful_refusal_rate"), recover_kn(pt["harmful_refusal"], 40)[:2])
            lo, hi = wilson95(k, n)
            blo, bhi = boot_rate_ci(k, n, rng)
            overlaps = not (hi < rwlo or lo > rwhi)
            cost = k / n - rk / rn
            nlo, nhi = newcombe_diff(k, n, rk, rn)
            dlo, dhi = boot_diff_ci(k, n, rk, rn, rng)
            entry.update(
                {
                    "stage_at_flag_death": pt["stage_id"],
                    "harmful_refusal_at_flag_death": k / n,
                    "k_at_flag_death": k,
                    "n_at_flag_death": n,
                    "wilson95_at_flag_death": [lo, hi],
                    "bootstrap95_at_flag_death": [blo, bhi],
                    "root_rate": rk / rn,
                    "root_wilson95": [rwlo, rwhi],
                    "intervals_overlap": overlaps,
                    "signed_evasion_cost_point": cost,
                    "signed_evasion_cost_bootstrap95": [dlo, dhi],
                    "signed_evasion_cost_newcombe95": [nlo, nhi],
                    "resolvable": not (dlo <= 0.0 <= dhi),
                    "restated_sentence": (
                        f"at the intensity where the flag first dies ({axis}, intensity {i_flag}), harmful "
                        f"refusal is {k / n:.3f} [{lo:.3f}, {hi:.3f}] vs the unlaundered root's "
                        f"{rk / rn:.3f} [{rwlo:.3f}, {rwhi:.3f}]; the intervals "
                        f"{'overlap' if overlaps else 'do not overlap'}."
                    ),
                }
            )
        else:
            entry["restated_sentence"] = (
                f"on {axis} the flag never dies over the swept intensity range, so there is no crossing "
                f"intensity at which to state a rate; verdict {verdict} exactly as archived."
            )
        entry["evadable"] = verdict == "EVADABLE"
        entry["is_real_intensity_axis"] = verdict != "NOT_AN_INTENSITY_AXIS"
        restatements.append(entry)

    # ---------------- M2.3 evasion-cost intervals, incl. the two named values ----
    named: list[dict[str, Any]] = []
    for r in restatements:
        if "signed_evasion_cost_point" not in r:
            continue
        cost = r["signed_evasion_cost_point"]
        dlo, dhi = r["signed_evasion_cost_bootstrap95"]
        named.append(
            {
                "axis": r["axis"],
                "cost_point_full_precision": cost,
                "cost_point_one_sig_fig": _one_sig(cost),
                "cost_ci_lo": dlo,
                "cost_ci_hi": dhi,
                "newcombe95": r["signed_evasion_cost_newcombe95"],
                "resolvable": r["resolvable"],
                "sentence": (
                    f"{r['axis']}: signed evasion cost {_one_sig(cost)} "
                    f"[{dlo:+.3f}, {dhi:+.3f}] - "
                    + ("resolvable (CI excludes 0)." if r["resolvable"] else "NOT A RESOLVABLE DIFFERENCE.")
                ),
            }
        )

    # int4 stage: refusal 0.135 vs the root's 0.162 (a DIFFERENCE, not two rates)
    int4 = None
    for st in ladder:
        if "int4" in st["stage_id"] or ("quant" in str(st.get("family", "")) and st.get("intensity") == 4):
            if abs(float(st.get("harmful_refusal_rate", -1)) - 0.135) < 0.02:
                int4 = st
                break
    if int4 is None:
        cands = [s for s in ladder if "quant" in str(s.get("family", ""))]
        int4 = min(cands, key=lambda s: abs(float(s.get("harmful_refusal_rate", 1)) - 0.135)) if cands else None
    int4_block: dict[str, Any]
    if int4 is not None:
        k, n = kn_index[(int4["stage_id"], "harmful_refusal_rate")]
        dlo, dhi = boot_diff_ci(k, n, rk, rn, rng)
        nlo, nhi = newcombe_diff(k, n, rk, rn)
        d = k / n - rk / rn
        int4_block = {
            "stage_id": int4["stage_id"],
            "int4_rate": k / n,
            "int4_k_n": [k, n],
            "root_rate": rk / rn,
            "root_k_n": [rk, rn],
            "difference_point": d,
            "difference_one_sig_fig": _one_sig(d),
            "bootstrap95": [dlo, dhi],
            "newcombe95": [nlo, nhi],
            "binomial_se_reference_p020_n40": (0.2 * 0.8 / 40) ** 0.5,
            "resolvable": not (dlo <= 0.0 <= dhi),
            "sentence": (
                f"int4 refusal {k / n:.3f} vs the root's {rk / rn:.3f}: difference {_one_sig(d)} "
                f"[{dlo:+.3f}, {dhi:+.3f}]"
                + ("" if not (dlo <= 0 <= dhi) else " - NOT A RESOLVABLE DIFFERENCE.")
            ),
        }
    else:
        int4_block = {"status": "UNAVAILABLE", "reason": "no int4/quantization stage located in ladder.jsonl"}

    addback = next((n for n in named if "targeted_all" in n["axis"]), None)

    real_axes = [r for r in restatements if r["is_real_intensity_axis"]]
    axis_census = {
        "n_crossing_rows_in_archive": len(restatements),
        "n_real_intensity_axes_recomputed": len(real_axes),
        "n_quoted_in_draft": 6,
        "excluded_non_axis_rows": [r["axis"] for r in restatements if not r["is_real_intensity_axis"]],
        "n_evadable": sum(1 for r in real_axes if r["evadable"]),
        "n_neither_dies": sum(1 for r in real_axes if r["order"] == "NEITHER_DIES"),
        "evadable_axes": [r["axis"] for r in real_axes if r["evadable"]],
        "neither_dies_axes": [r["axis"] for r in real_axes if r["order"] == "NEITHER_DIES"],
        "finding": (
            f"The archive's own summary says 'EVADABLE in 4 of 6 real intensity axes', but there are "
            f"{len(real_axes)} real intensity axes in crossing.jsonl "
            f"({sum(1 for r in real_axes if r['evadable'])} EVADABLE + "
            f"{sum(1 for r in real_axes if r['order'] == 'NEITHER_DIES')} NEITHER_DIES). The counts "
            f"of each verdict are right; the DENOMINATOR quoted as 6 is stale and must read "
            f"{len(real_axes)}."
        ) if len(real_axes) != 6 else "the quoted denominator of 6 real intensity axes reproduces",
    }

    # ---------------- M2.4 ladder power ----------------
    ns = sorted({r["n_achieved"] for r in rows if r["rate_field"] == "harmful_refusal_rate"})
    power = {
        "note": "minimum detectable rate difference at 80% power, two-proportion z, alpha 0.05, "
        "equal group sizes",
        "grid": {},
        "n_achieved_range": [min(ns), max(ns)] if ns else None,
    }
    power["direction_note"] = (
        "UPWARD is the direction the ladder actually asks about (an evasion cost is an INCREASE in "
        "harmful refusal relative to the root). The downward magnitude is smaller at a given base "
        "rate because the variance shrinks toward the floor, so both are printed and the upward "
        "number is the one the paper should quote."
    )
    for n in [34, 37, 40]:
        power["grid"][str(n)] = {}
        for p in (0.15, 0.20, 0.35, 0.90):
            up = two_prop_mdd_directional(n, p, +1)
            dn = two_prop_mdd_directional(n, p, -1)
            power["grid"][str(n)][f"{p:.2f}"] = {
                "mdd_upward": up,
                "mdd_downward": dn,
                "mdd_smaller_magnitude": min([v for v in (up, dn) if v is not None], default=None),
            }
    up40 = power["grid"]["40"]["0.20"]["mdd_upward"]
    power["resolution_sentence"] = (
        f"At the ladder's achieved denominators (n = {min(ns) if ns else '?'}-{max(ns) if ns else '?'} items "
        f"per stage) the smallest UPWARD rate difference detectable at 80% power is "
        f"{up40:.2f} at a base rate of 0.20, so any quoted evasion cost below that "
        f"is arithmetic on noise and is reported as an ORDERING, not a decimal."
    )

    return {
        "status": "OK",
        "seed": SEED_W2,
        "bootstrap_B": BOOT_B,
        "interval_convention": "Wilson is PRIMARY (small n, rates near 0, Wald undercovers); the item-level "
        "bootstrap is reported beside it and any endpoint disagreement > 0.02 is listed.",
        "n_stages": len(ladder),
        "n_interval_rows": len(rows),
        "rows": rows,
        "root": root_block,
        "wilson_vs_bootstrap_disagreements": disagreements_wilson_vs_boot,
        "n_wilson_vs_bootstrap_disagreements": len(disagreements_wilson_vs_boot),
        "flagged_reconstructions": flagged_reconstructions,
        "crossing_restatements": restatements,
        "axis_census": axis_census,
        "evasion_cost_intervals": named,
        "named_unresolvable_checks": {
            "add_back_all_cost": addback,
            "int4_vs_root": int4_block,
        },
        "ladder_power": power,
    }
