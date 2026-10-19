"""Mandatory first stage: discover the ACTUAL field names in the archived trees.

Every later analysis keys off what this stage records, never off names assumed
from the experiment summaries.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from loguru import logger

from .common import E1, E2, E3, OUT, dump_json, load_json, load_jsonl


def _structure(o: Any, depth: int = 0, max_depth: int = 3) -> Any:
    if depth > max_depth:
        return "..."
    if isinstance(o, dict):
        return {k: _structure(v, depth + 1, max_depth) for k, v in list(o.items())[:40]}
    if isinstance(o, list):
        return {"__list__": len(o),
                "__item0__": _structure(o[0], depth + 1, max_depth) if o else None}
    return type(o).__name__


def run() -> dict[str, Any]:
    inv: dict[str, Any] = {"experiments": {}}

    # ---------------- E1 ----------------
    e1: dict[str, Any] = {"workspace": str(E1), "files": {}}
    raw = load_json(E1 / "out" / "tier0_raw.json")
    e1["files"]["out/tier0_raw.json"] = {
        "top_level_keys": sorted(raw.keys()),
        "n_lambda_rows": len(raw["lambda"]),
        "n_indicator_rows": len(raw["indicators"]),
        "lambda_row_keys": sorted(raw["lambda"][0].keys()),
        "lambda_readout_keys": sorted(raw["lambda"][0]["layerL"].keys()),
        "lambda_estimate_keys": sorted(raw["lambda"][0]["layerL"]["estimates"].keys()),
        "indicator_row_keys": sorted(raw["indicators"][0].keys()),
        "models": sorted(raw["aggregate_by_model"].keys()),
        "directions": sorted({r["direction"] for r in raw["lambda"]}),
        "grid_actually_run": raw["grid_actually_run"],
        "per_model_meta_keys": sorted(raw["per_model_meta"][list(raw["per_model_meta"])[0]].keys()),
        "observable_sanity_keys": sorted(
            raw["per_model_meta"][list(raw["per_model_meta"])[0]]["observable_sanity"].keys()),
        "n_lambda_identifiable_true": sum(1 for r in raw["lambda"] if r.get("identifiable")),
        "verdict": raw["verdict"]["code"],
        "structure": _structure(raw, max_depth=1),
    }
    cert = load_json(E1 / "out" / "refit_certified.json")
    e1["files"]["out/refit_certified.json"] = {
        "top_level_keys": sorted(cert.keys()),
        "geometry": {k: cert[k] for k in
                     ("fit_len", "n_roll", "T", "p", "eps_c", "teacher_forced")},
        "all_rows_identifiable": cert["all_rows_identifiable"],
        "rule_at_refit_noise": cert["rule_at_refit_noise"],
        "n_rows": len(cert["rows"]),
        "row_keys": sorted(cert["rows"][0].keys()),
        "readout_keys": sorted(cert["rows"][0]["layerL"].keys()),
        "mean_delta_curve_len": len(cert["rows"][0]["layerL"]["mean_delta_curve"]),
        "prereg_ordering_tests_lambda_refuse": cert["prereg_ordering_tests_lambda_refuse"],
    }
    e1["files"]["out/layer_choice.json"] = {
        "keys": sorted(load_json(E1 / "out" / "layer_choice.json").keys())}
    mo1 = load_json(E1 / "method_out.json")
    e1["files"]["method_out.json"] = {
        "keys": sorted(mo1.keys()),
        "datasets": [d["dataset"] for d in mo1.get("datasets", [])],
        "metadata_keys": sorted(mo1.get("metadata", {}).keys()),
    }
    e1["prereg_archived"] = (E1 / "prereg.json").exists()
    inv["experiments"]["E1"] = e1

    # ---------------- E2 ----------------
    e2: dict[str, Any] = {"workspace": str(E2), "files": {}}
    pre2 = load_json(E2 / "prereg.json")
    e2["files"]["prereg.json"] = {
        "keys": sorted(pre2.keys()),
        "n_amendments": len(pre2.get("amendments", [])),
        "amendment_ids": [a.get("id") for a in pre2.get("amendments", [])],
        "amendment_keys": sorted(pre2["amendments"][0].keys()) if pre2.get("amendments") else [],
        "primary_statistic": pre2.get("primary_statistic"),
        "alpha_grid": pre2.get("alpha_grid"),
        "alpha_grid_as_originally_preregistered": pre2.get(
            "alpha_grid_as_originally_preregistered"),
    }
    for key in ("base", "instruct", "abliterated"):
        m = load_json(E2 / "results" / f"model_{key}.json")
        e2["files"][f"results/model_{key}.json"] = {
            "keys": sorted(m.keys()),
            "n_rows": len(m["rows"]),
            "row_keys": sorted(m["rows"][0].keys()),
            "n_per_prompt": len(m["agg"]["per_prompt"]),
            "per_prompt_keys": sorted(m["agg"]["per_prompt"][0].keys()),
            "summary_keys": sorted(m["summary"].keys()),
            "steering_response_curve_keys": sorted(m["steering_response_curve"].keys()),
            "layer": m.get("layer"), "norm_L": m.get("norm_L"),
        }
    nf = E2 / "results" / "narrow_floor"
    e2["narrow_floor_dir_exists"] = nf.exists()
    e2["narrow_floor_substitute"] = sorted(
        p.name for p in (E2 / "results").glob("*narrowfloor*"))
    inv["experiments"]["E2"] = e2

    # ---------------- E3 ----------------
    e3: dict[str, Any] = {"workspace": str(E3), "files": {}}
    gens = load_jsonl(E3 / "generations.jsonl")
    scored = load_jsonl(E3 / "scored.jsonl")
    e3["files"]["generations.jsonl"] = {"n": len(gens), "keys": sorted(gens[0].keys())}
    e3["files"]["scored.jsonl"] = {
        "n": len(scored), "keys": sorted(scored[0].keys()),
        "members": sorted({r["member"] for r in scored}),
        "blocks": sorted({r["block"] for r in scored}),
        "n_with_gold": sum(1 for r in scored if r.get("judge_gold_label")),
        "frozen_label_counts": _counts(scored, "judge_label"),
        "repaired_label_counts": _counts(scored, "judge_repaired_label"),
        "gold_label_counts": _counts(scored, "judge_gold_label"),
    }
    probe = load_json(E3 / "results" / "judge_probe_items.json")
    e3["files"]["results/judge_probe_items.json"] = {
        "n": len(probe), "keys": sorted(probe[0].keys()),
        "truth_counts": _counts(probe, "truth"),
    }
    pr = load_json(E3 / "results" / "judge_probe_results.json")
    e3["files"]["results/judge_probe_results.json"] = {
        "keys": sorted(pr.keys()),
        "n_results": len(pr.get("results", [])),
        "result_keys": sorted(pr["results"][0].keys()) if pr.get("results") else [],
    }
    an = load_json(E3 / "results" / "analysis.json")
    e3["files"]["results/analysis.json"] = {"keys": sorted(an.keys())}
    e3["files"]["prereg.json"] = {"keys": sorted(load_json(E3 / "prereg.json").keys())}
    e3["files"]["prereg_amendment.json"] = {
        "keys": sorted(load_json(E3 / "prereg_amendment.json").keys())}
    e3["files"]["adjudication_labels.json"] = {
        "n": len(load_json(E3 / "adjudication_labels.json"))}
    for c in sorted(E3.glob("judge*_cache.jsonl")):
        rows = load_jsonl(c)
        e3["files"][c.name] = {"n": len(rows),
                               "keys": sorted(rows[0].keys()) if rows else []}
    e3["files"]["results/ladder_models_manifest.json"] = {
        "keys": sorted(load_json(E3 / "results" / "ladder_models_manifest.json").keys())}
    e3["refusal_direction_pt_bytes"] = (E3 / "refusal_direction.pt").stat().st_size
    inv["experiments"]["E3"] = e3

    dump_json(OUT / "input_inventory.json", inv)
    logger.info("inventory complete")
    return inv


def _counts(rows: list[dict], field: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in rows:
        v = r.get(field)
        k = str(v) if v is not None else "__null__"
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))
