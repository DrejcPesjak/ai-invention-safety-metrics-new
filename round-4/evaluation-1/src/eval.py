#!/usr/bin/env python3
"""Recheck every number in the draft.

PURE RE-ANALYSIS over the archived iteration-2 and iteration-3 trees.
No model weights, no forward passes, no generations, no LLM calls ($0.00), no Hub fetches.

Outputs
-------
eval_out.json                     blocks: recipe_relabel, ladder_intervals, e1_bands,
                                  cost_table, fidelity, assertions, provenance, manifest
results/arm1_real_corrected.jsonl corrected arm-1 rows, OLD and NEW labels side by side
results/disagreements.json        every MISMATCH / UNAVAILABLE assertion row
results/draft_edit_list.json      the numbered draft edit list
README.md                         spend, seed, determinism result, MATCH/MISMATCH/UNAVAILABLE counts
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from loguru import logger

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(str(HERE / "logs/run.log"), rotation="30 MB", level="DEBUG")

from lib_arch import ARCHIVES, BOOT_B, SEED, Resolver, build_manifest  # noqa: E402
from ws_assert import build_assertions, cross_check_gates  # noqa: E402
from ws_w1 import run_w1  # noqa: E402
from ws_w2 import run_w2  # noqa: E402
from ws_w3 import run_w3  # noqa: E402
from ws_w4 import run_w4  # noqa: E402
from ws_w5 import run_w5  # noqa: E402


def _headers(res: Resolver) -> dict[str, Any]:
    """Print (and record) the top-level key set of every *_out.json and header keys of .jsonl."""
    out: dict[str, Any] = {}
    from lib_arch import walk_archive

    for tag, root in ARCHIVES.items():
        entry: dict[str, Any] = {}
        files = walk_archive(root)
        for p in [f for f in files if f.name.endswith("_out.json") and f.parent == root]:
            try:
                d = json.loads(p.read_text())
            except (json.JSONDecodeError, OSError):
                continue
            entry[p.name] = sorted(d.keys()) if isinstance(d, dict) else f"list[{len(d)}]"
            if isinstance(d, dict) and "datasets" in d:
                entry[p.name + "::datasets"] = {
                    ds["dataset"]: len(ds["examples"]) for ds in d["datasets"]
                }
            break  # one representative assembled artifact per tree is enough
        for p in [f for f in files if f.suffix == ".jsonl"]:
            try:
                first = next((ln for ln in p.read_text().splitlines() if ln.strip()), None)
            except OSError:
                continue
            if first is None:
                continue
            try:
                entry[str(p.relative_to(root))] = sorted(json.loads(first).keys())
            except json.JSONDecodeError:
                continue
        out[tag] = entry
        for k, v in entry.items():
            logger.info(f"[{tag}] {k}: {v if not isinstance(v, list) else v[:12]}")
    return out


def _flatten_metrics(blocks: dict[str, Any], assertions: list[dict], gates: dict) -> dict[str, float]:
    va = blocks["recipe_relabel"].get("grouping_analysis", {}).get("variance_attribution", {})
    r2, r3, r5 = blocks["ladder_intervals"], blocks["e1_bands"], blocks["fidelity"]
    prim15 = next((b for b in r3.get("e1_by_band", [])
                   if b["pairset"] == "extended_15" and b["band"] == [0.25, 0.75]), {})
    el = r5.get("eligibility_denominator", {})
    c5 = r5.get("counts_from_rows", {})
    verd = {v: sum(1 for a in assertions if a["verdict"] == v)
            for v in ("MATCH", "MISMATCH", "UNAVAILABLE")}
    m: dict[str, float] = {
        "n_assertions": float(len(assertions)),
        "n_assertions_match": float(verd["MATCH"]),
        "n_assertions_mismatch": float(verd["MISMATCH"]),
        "n_assertions_unavailable": float(verd["UNAVAILABLE"]),
        "assertion_match_rate": verd["MATCH"] / len(assertions) if assertions else 0.0,
        "n_recipe_rows_relabelled": float(blocks["recipe_relabel"].get("n_relabelled_applied", 0)),
        "n_recipe_rows_provisional": float(blocks["recipe_relabel"].get("n_relabelled_provisional", 0)),
        "new_uploader_auroc_recomputed": float(va.get("headline_new_uploader_auroc_recomputed") or 0.0),
        "n_misses_with_verbatim_non_uniform_kernel": float(
            len(va.get("share_of_misses_with_verbatim_non_uniform_kernel_string", "0/0").split("/")[0])
            and int(va.get("share_of_misses_with_verbatim_non_uniform_kernel_string", "0/0").split("/")[0])
        ),
        "n_ladder_interval_rows": float(r2.get("n_interval_rows", 0)),
        "n_wilson_vs_bootstrap_disagreements": float(r2.get("n_wilson_vs_bootstrap_disagreements", 0)),
        "n_unresolvable_evasion_costs": float(
            sum(1 for e in r2.get("evasion_cost_intervals", []) if not e.get("resolvable"))
        ),
        "ladder_mdd_upward_at_p020_n40": float(
            (r2.get("ladder_power", {}).get("grid", {}).get("40", {}).get("0.20") or {})
            .get("mdd_upward") or 0.0),
        "e1_bands_recomputable": float(sum(
            1 for b in r3.get("e1_by_band", []) if b.get("band_status") == "RECOMPUTED_FROM_ARCHIVE")),
        "e1_bands_not_recomputable": float(sum(
            1 for b in r3.get("e1_by_band", []) if b.get("band_status") == "NOT_RECOMPUTABLE_FROM_ARCHIVE")),
        "paired_diff_W05_minus_E1_15pairs": float(prim15.get("paired_diff_W05_minus_E1") or 0.0),
        "n_cost_table_rows": float(len(blocks["cost_table"].get("behavioural_cost_table", []))),
        "n_carry_forward_values": float(len(blocks["cost_table"].get("carry_forward", []))),
        "n_subset_corrected_values": float(len(
            blocks["cost_table"].get("subset_correction", {}).get("rows", []))),
        "scan_total_rows": float(c5.get("total_rows", 0)),
        "scan_completed": float(c5.get("completed_scanned_non_control", 0)),
        "scan_unresolved_recomputed": float(
            c5.get("unresolved_discrepancy", {}).get("recomputed_unresolved_non_control", 0)),
        "eligibility_n_raw": float(el.get("n_raw", 0)),
        "eligibility_n_eligible": float(el.get("n_eligible", 0)),
        "eligibility_n_excluded": float(el.get("n_excluded_rows", 0)),
        "fp_rate_eligible": float(el.get("fp_rate_eligible_PRIMARY") or 0.0),
        "fp_rate_raw": float(el.get("fp_rate_raw_SECONDARY") or 0.0),
        "wilson95_upper_eligible": float((el.get("wilson95_eligible_PRIMARY") or [0, 0])[1] or 0.0),
        "smallest_shift_to_first_false_positive": float(
            r5.get("threshold_brittleness", {}).get("smallest_shift_to_first_false_positive") or 0.0),
        "n_prereg_claims": float(r5.get("claim_map", {}).get("total", 0)),
        "verify_py_checks_passed": float(gates.get("verify_py", {}).get("n_pass") or 0),
        "verify_py_checks_total": float(gates.get("verify_py", {}).get("n_total") or 0),
        "wstats_max_abs_delta_W05": float(gates.get("wstats_gate", {}).get("max_abs_delta_W05_vs_archive") or 0.0),
        "openrouter_spend_usd": 0.0,
        "n_forward_passes": 0.0,
        "n_generations": 0.0,
        "n_hub_fetches": 0.0,
    }
    return {k: float(v) for k, v in m.items()}


def _datasets(blocks: dict[str, Any], assertions: list[dict]) -> list[dict[str, Any]]:
    """Tabular views for the schema's datasets[] array."""
    ds: list[dict[str, Any]] = []

    ds.append({
        "dataset": "assertions",
        "examples": [
            {
                "input": a["claim_id"],
                "output": a["verdict"],
                "predict_recomputed_value": json.dumps(a["recomputed_value"]),
                "predict_draft_quoted_value": json.dumps(a["draft_quoted_value"]),
                "eval_abs_diff": float(a["abs_diff"]) if a["abs_diff"] is not None else -1.0,
                "eval_tolerance": float(a["tolerance"]),
                "eval_is_match": 1.0 if a["verdict"] == "MATCH" else 0.0,
                "metadata_provenance": a["provenance"],
                "metadata_tolerance_class": a["tolerance_class"],
            }
            for a in assertions
        ],
    })

    r1 = blocks["recipe_relabel"]
    ds.append({
        "dataset": "recipe_relabel",
        "examples": [
            {
                "input": t["repo_id"],
                "output": t["recipe_class_NEW"],
                "predict_kernel_family": t["kernel_family"],
                "predict_recipe_class_old": t["recipe_class_OLD"],
                "eval_W05": float(t["W05"]),
                "eval_W01": float(t["W01"]),
                "eval_caught_at_fitted_threshold": 1.0 if t["W05"] <= -2.7415117804288127 else 0.0,
                "metadata_evidence_status": t["evidence_status"],
                "metadata_relabel_status": t["relabel_status"],
                "metadata_evidence_span_verbatim": t["evidence_span_verbatim"],
                "metadata_evidence_char_offsets": t["evidence_char_offsets"],
                "metadata_mechanically_different_old": t["mechanically_different_OLD"],
                "metadata_mechanically_different_new": t["mechanically_different_NEW"],
                "metadata_decision_rule_id": t["decision_rule_id"],
                "metadata_uploader": t["uploader"],
            }
            for t in r1.get("recipe_relabel_table", [])
        ],
    })

    r2 = blocks["ladder_intervals"]
    ds.append({
        "dataset": "ladder_intervals",
        "examples": [
            {
                "input": f"{r['stage_id']}::{r['rate_field']}",
                "output": f"{r['rate']:.4f}" if r["rate"] is not None else "NA",
                "predict_wilson95": f"[{r['wilson95_lo']:.4f}, {r['wilson95_hi']:.4f}]",
                "predict_bootstrap95": f"[{r['bootstrap95_lo']:.4f}, {r['bootstrap95_hi']:.4f}]",
                "eval_rate": float(r["rate"]) if r["rate"] is not None else -1.0,
                "eval_k_refused": float(r["k_refused"]),
                "eval_n_achieved": float(r["n_achieved"]),
                "eval_n_nominal": float(r["n_nominal"]),
                "eval_se_binomial": float(r["se_binomial"]),
                "eval_reconstruction_residual": float(r["reconstruction_residual"]),
                "metadata_axis": r["axis"],
                "metadata_intensity": r["intensity"],
                "metadata_denominator_source": r["denominator_source"],
            }
            for r in r2.get("rows", [])
        ],
    })

    r3 = blocks["e1_bands"]
    ds.append({
        "dataset": "e1_bands",
        "examples": [
            {
                "input": f"band={b['band']}::pairset={b['pairset']}",
                "output": b["band_status"],
                "predict_paired_diff_W05_minus_E1": (
                    f"{b['paired_diff_W05_minus_E1']:.4f}"
                    if b.get("paired_diff_W05_minus_E1") is not None else "NOT_RECOMPUTABLE"
                ),
                "eval_auroc_E1": float(b["auroc_E1"]) if b.get("auroc_E1") is not None else -1.0,
                "eval_auroc_W05": float(b["auroc_W05"]) if b.get("auroc_W05") is not None else -1.0,
                "eval_n_pairs": float(b["n_pairs"]),
                "metadata_band_label": b["band_label"],
                "metadata_ci": [b.get("ci_lo"), b.get("ci_hi")],
                "metadata_reason": b.get("reason"),
            }
            for b in r3.get("e1_by_band", [])
        ],
    })

    r4 = blocks["cost_table"]
    ds.append({
        "dataset": "cost_table",
        "examples": [
            {
                "input": r["metric_id"],
                "output": r["family"],
                "predict_rho_member": (f"{r['rho_member']:.4f}" if r.get("rho_member") is not None
                                       else "NA"),
                "eval_harmful_prompts_required": float(r.get("harmful_prompts_required") or 0.0),
                "eval_prompts_required": float(r.get("prompts_required") or 0.0),
                "eval_forward_passes_required": float(r.get("forward_passes_required") or 0.0),
                "eval_wall_clock_median_s": float(r.get("measured_wall_clock_median_s") or 0.0),
                "eval_rho_lineage": float(r["rho_lineage"]) if r.get("rho_lineage") is not None else 0.0,
                "metadata_ci_member": r.get("ci_member"),
                "metadata_ci_lineage": r.get("ci_lineage"),
                "metadata_paired_diff_vs_best_blackbox": r.get("paired_diff_vs_best_blackbox"),
                "metadata_paired_diff_ci": r.get("paired_diff_ci"),
                "metadata_parent_model_required": r.get("parent_model_required"),
                "metadata_carried_forward": r.get("carried_forward"),
            }
            for r in r4.get("behavioural_cost_table", [])
        ],
    })

    r5 = blocks["fidelity"]
    ds.append({
        "dataset": "claim_map",
        "examples": [
            {
                "input": c["claim_text_in_draft"],
                "output": c["status"],
                "predict_corrected_wording": c["corrected_wording"] or "(no change required)",
                "eval_is_supported": 1.0 if c["status"] == "SUPPORTED" else 0.0,
                "metadata_artifact_file": c["artifact_file"],
                "metadata_line_or_key": c["line_or_key"],
            }
            for c in r5.get("claim_map", {}).get("rows", [])
        ],
    })

    ds.append({
        "dataset": "threshold_brittleness",
        "examples": [
            {
                "input": f"threshold={s['threshold']}",
                "output": str(s["hits_raw_160"]),
                "predict_hits_eligible": str(s["hits_eligible"]),
                "eval_threshold": float(s["threshold"]),
                "eval_hits_raw_160": float(s["hits_raw_160"]),
                "eval_hits_eligible": float(s["hits_eligible"]),
            }
            for s in r5.get("threshold_brittleness", {}).get("coarse_sweep_step_0.1", [])
        ],
    })

    weights_rows = r5.get("weights_table_minmax", {}).get("rows", [])
    ds.append({
        "dataset": "weights_table_minmax",
        "examples": [
            {
                "input": f"{w['statistic']}::{w['class']}",
                "output": f"median={w['median']:.4f} [min={w['min']:.4f}, max={w['max']:.4f}]",
                "predict_range_as_the_paper_must_report_it": (
                    f"n={w['n']}, median {w['median']:.3f}, range [{w['min']:.3f}, {w['max']:.3f}]"
                ),
                "eval_n": float(w["n"]),
                "eval_median": float(w["median"]),
                "eval_min": float(w["min"]),
                "eval_max": float(w["max"]),
                "metadata_provenance": w["provenance"],
            }
            for w in weights_rows
        ],
    })
    return ds


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="eval_out.json")
    ap.add_argument("--skip-verify", action="store_true", help="skip re-running A2/verify.py")
    args = ap.parse_args()

    t0 = time.time()
    logger.info("=" * 78)
    logger.info("RECHECK EVERY NUMBER IN THE DRAFT - pure re-analysis, $0.00 LLM spend")
    logger.info("=" * 78)

    # ---- STEP 0 ----
    manifest = build_manifest()
    headers = _headers(Resolver())
    res = Resolver()

    a6_report = ARCHIVES["A6"] / "research_report.md"
    a6_out = ARCHIVES["A6"] / "research_out.json"
    a6_text = ""
    for p in (a6_report, a6_out):
        if p.is_file():
            a6_text += p.read_text()

    blocks: dict[str, Any] = {}
    blocks["recipe_relabel"] = run_w1(res, a6_text)
    blocks["ladder_intervals"] = run_w2(res)
    blocks["e1_bands"] = run_w3(res)
    blocks["cost_table"] = run_w4(res)
    blocks["fidelity"] = run_w5(res)

    gates = cross_check_gates(res)
    if args.skip_verify:
        gates["verify_py"] = {"ran": False, "error": "skipped by --skip-verify flag"}

    numbers = res.read_json("A5", "numbers.json")
    assertions = build_assertions(blocks, numbers or {}, gates)
    verdicts = {v: sum(1 for a in assertions if a["verdict"] == v)
                for v in ("MATCH", "MISMATCH", "UNAVAILABLE")}
    logger.info(f"assertions: {len(assertions)} rows -> {verdicts}")

    # Each disagreement is annotated so the paper can tell a genuine reporting error from a
    # difference that is expected by design.  Anything unannotated is reported as UNCLASSIFIED.
    INTERPRETATION = {
        "W2.n_real_intensity_axes_quoted_as_6": (
            "DRAFT_ERROR_DENOMINATOR",
            "crossing.jsonl carries 7 real intensity axes (4 EVADABLE + 3 NEITHER_DIES) plus one "
            "'combined' row that is NOT an intensity axis. The per-verdict counts are right; the "
            "denominator quoted as 6 is stale and must read 7.",
        ),
        "W4.B09_abs_rho_member_0.766_against_28_member_contract_subset": (
            "SUBSET_DEFECT_CONFIRMED",
            "EXPECTED. 0.766 is B09's correlation on the 26-member renderer=='chatml' subset "
            "(reproduced to 1e-4 there, see the companion assertion), not on the 28-member non-base "
            "contract subset the draft states, where it is 0.670. The number is not wrong; the "
            "SUBSET LABEL is. The draft must state which rule it used.",
        ),
        "W4.n_subset_corrected_values_quoted_as_4": (
            "DRAFT_ERROR_COUNT",
            "The forensics block carries FIVE quoted values that fail to reproduce under the stated "
            "convention (A01, A02, A22, B09, W01), not four. Exactly one of the five (B09) reproduces "
            "under the renderer subset; the other four reproduce under NO convention searched.",
        ),
        "W5.unresolved_quoted_as_65": (
            "DRAFT_ERROR_COUNT_ADJUDICATED",
            "Recomputed mechanically from scan.jsonl: 81 non-control rows carry status UNRESOLVED. "
            "The '65' transcribed in the iteration-3 experiment-2 summary is stale. 81 is the value "
            "generated from the rows and is the one the paper must use.",
        ),
        "W5.skipped_7": (
            "DRAFT_ERROR_COUNT",
            "8 non-control rows carry status SKIPPED, not 7.",
        ),
    }
    disagreements = []
    for a in assertions:
        if a["verdict"] not in ("MISMATCH", "UNAVAILABLE"):
            continue
        cls, why = INTERPRETATION.get(a["claim_id"], ("UNCLASSIFIED", None))
        disagreements.append({**a, "finding_class": cls, "interpretation": why})

    metrics = _flatten_metrics(blocks, assertions, gates)
    out = {
        "metadata": {
            "evaluation_name": "Recheck every number in the draft",
            "description": "Pure re-analysis over the archived iteration-2 and iteration-3 trees. "
                           "One numbers file plus a corrected-rows file, with a hard assertion block "
                           "that recomputes each draft-quoted value and emits a disagreement table.",
            "scope_constraints": {
                "model_weights_loaded": False,
                "forward_passes": 0,
                "generations": 0,
                "llm_calls": 0,
                "openrouter_spend_usd": 0.0,
                "hub_fetches": 0,
                "hand_reconstructed_numbers": 0,
            },
            "seed": SEED,
            "bootstrap_B": BOOT_B,
            "archives": {k: str(v) for k, v in ARCHIVES.items()},
            "resolved_paths": res.resolved,
            "unresolved_globs": res.missing,
            "assertion_tolerances": {
                "verbatim_copy": 1e-6,
                "float_rederivation": 1e-4,
                "rate_from_reconstructed_counts": 0.005,
                "repo_ids_and_evidence_spans": "exact string match",
            },
            "assertion_verdict_counts": verdicts,
            "cross_check_gates": gates,
            "wall_clock_s": None,
        },
        "metrics_agg": metrics,
        "datasets": _datasets(blocks, assertions),
    }
    out["metadata"]["blocks"] = {
        "recipe_relabel": blocks["recipe_relabel"],
        "ladder_intervals": blocks["ladder_intervals"],
        "e1_bands": blocks["e1_bands"],
        "cost_table": blocks["cost_table"],
        "fidelity": blocks["fidelity"],
        "assertions": assertions,
        "provenance": {
            "rule": "Every emitted number carries provenance = {file, line_or_key, raw_value}. "
                    "Blocks carry it inline on the value they describe; this index records how each "
                    "archive file was RESOLVED, which is the other half of the trail.",
            "archives": {k: str(v) for k, v in ARCHIVES.items()},
            "archive_roles": {
                "A1": "iter-3 experiment 1 - scope of the weight scar (arms 1-3, wstats gate)",
                "A2": "iter-3 experiment 2 - laundering ladder + wild Hub scan",
                "A3": "iter-2 experiment 1 - frozen 53-metric battery (sha 544ff994)",
                "A4": "iter-2 dataset 1 - panel manifest, frozen split, corpora, external scores",
                "A5": "iter-3 evaluation 1 - numbers.json (carry-forward source), READ FROM DISK "
                      "because an evaluation may only declare experiment/dataset dependencies",
                "A6": "iter-3 research 1 - prior-art dossier, READ FROM DISK for the same reason",
            },
            "resolved_by_glob": res.resolved,
            "unresolved_globs": res.missing,
            "n_files_in_manifest": len(manifest),
            "carry_forward_policy": "values marked recomputed=false are copied verbatim from an "
                                    "archive and are never re-derived by hand",
            "unavailable_policy": "if an archived field needed for a recomputation is absent, an "
                                  "UNAVAILABLE / NOT_IN_ARCHIVE / NOT_RECOMPUTABLE_FROM_ARCHIVE row "
                                  "is emitted with the paths and fields searched; no number is "
                                  "reconstructed by hand",
        },
        "manifest": manifest,
        "archive_headers": headers,
    }
    out["metadata"]["wall_clock_s"] = round(time.time() - t0, 2)

    # ---- outputs ----
    (HERE / "results").mkdir(exist_ok=True)
    Path(HERE / args.out).write_text(json.dumps(out, indent=1, sort_keys=True, default=str))
    Path(HERE / "results/disagreements.json").write_text(
        json.dumps({"n": len(disagreements), "rows": disagreements}, indent=1, sort_keys=True,
                   default=str)
    )
    Path(HERE / "results/draft_edit_list.json").write_text(
        json.dumps(blocks["recipe_relabel"].get("draft_edit_list", []), indent=1, sort_keys=True,
                   default=str)
    )
    with (HERE / "results/arm1_real_corrected.jsonl").open("w") as fh:
        for t in blocks["recipe_relabel"].get("recipe_relabel_table", []):
            fh.write(json.dumps(t, sort_keys=True, default=str) + "\n")

    logger.info(f"wrote {args.out} ({(HERE / args.out).stat().st_size / 1e6:.2f} MB) in "
                f"{out['metadata']['wall_clock_s']}s")

    # ---- README ----
    fc = {}
    for d in disagreements:
        fc[d["finding_class"]] = fc.get(d["finding_class"], 0) + 1
    det = json.loads((HERE / "results/determinism.json").read_text()) \
        if (HERE / "results/determinism.json").is_file() else {"status": "NOT_YET_RUN"}
    readme = f"""# Recheck every number in the draft

Pure re-analysis over the archived iteration-2 and iteration-3 trees.

| | |
|---|---|
| OpenRouter / LLM spend | **$0.00** (no LLM client is imported anywhere in this artifact) |
| Model weights loaded | 0 |
| Forward passes | 0 |
| Generations | 0 |
| HuggingFace Hub fetches | 0 |
| Seed | `{SEED}` |
| Bootstrap resamples | {BOOT_B} |
| Wall clock | {out['metadata']['wall_clock_s']} s |
| Determinism check | {det.get('status', 'NOT_YET_RUN')} |

## Assertion table

{len(assertions)} claim_ids covered across W1-W5 plus the cross-check gates.

| verdict | n |
|---|---|
| MATCH | {verdicts['MATCH']} |
| MISMATCH | {verdicts['MISMATCH']} |
| UNAVAILABLE | {verdicts['UNAVAILABLE']} |

A MISMATCH does not abort the run - it is the product. Every disagreement is in
`results/disagreements.json`, annotated with a `finding_class`:

{chr(10).join(f'- `{k}` x{v}' for k, v in sorted(fc.items())) or '- (none)'}

## Cross-check gates

- `A2/verify.py` re-run against the archived `results/*.jsonl`:
  **{gates.get('verify_py', {}).get('summary_line', 'not run')}**
- `A1` wstats reimplementation vs the archive: max |dW05| =
  `{gates.get('wstats_gate', {}).get('max_abs_delta_W05_vs_archive')}`
  (gate.json full precision `{gates.get('wstats_gate', {}).get('gate_json_reported_max_abs_dW05')}`),
  W05 ordering preserved =
  `{gates.get('wstats_gate', {}).get('gate_json_w05_ordering_preserved')}`.

## Outputs

- `eval_out.json` - blocks `recipe_relabel`, `ladder_intervals`, `e1_bands`, `cost_table`,
  `fidelity`, `assertions`, `provenance`, `manifest` (under `metadata.blocks`)
- `results/arm1_real_corrected.jsonl` - one row per arm-1 new-uploader member, OLD and NEW labels
  side by side with the verbatim evidence span
- `results/disagreements.json` - every MISMATCH / UNAVAILABLE
- `results/draft_edit_list.json` - the numbered draft edit list
- `results/determinism.json` - the two-run byte-identity check

## Reproduce

```bash
uv run eval.py            # writes eval_out.json and results/*
uv run determinism.py     # runs the pipeline twice and diffs the bytes
```
"""
    (HERE / "README.md").write_text(readme)
    if not assertions:
        raise SystemExit("FAIL: assertion table is empty")
    for req in ("eval_out.json", "results/disagreements.json", "results/draft_edit_list.json",
                "results/arm1_real_corrected.jsonl"):
        if not (HERE / req).is_file():
            raise SystemExit(f"FAIL: missing output {req}")
    logger.info("DONE")


if __name__ == "__main__":
    main()
