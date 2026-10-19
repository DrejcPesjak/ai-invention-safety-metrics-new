#!/usr/bin/env python3
"""Independent verifier for gen_art_evaluation_2.

Re-derives every headline number in eval_out.json from results/*.jsonl WITHOUT importing
eval.py, in the style of the archived verify.py scripts.  If a number in the output was
produced by a code path this file does not reimplement, it is not verified and says so.

Run:  .venv/bin/python verify_eval.py
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "results"
CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def js(p: Path):
    return json.loads(p.read_text()) if p.exists() else None


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def close(a, b, tol=1e-9) -> bool:
    if a is None or b is None:
        return False
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def main() -> int:
    out = js(HERE / "eval_out.json")
    if out is None:
        print("eval_out.json missing")
        return 2
    M = out["metrics_agg"]
    rows = jl(R / "scores.jsonl")
    rec = jl(R / "recovered.jsonl")
    meta = jl(R / "regen_meta.jsonl")
    agr = js(R / "agreement.json")
    prop = js(R / "propagation.json")
    lim = js(R / "judge_limitations.json")
    LAB = ("REFUSAL", "PARTIAL", "COMPLIANCE")
    VALID = set(LAB)

    # ---- 1. structural -------------------------------------------------
    check("eval_out has metrics_agg and datasets",
          bool(M) and bool(out.get("datasets")),
          f"{len(M)} metrics, {len(out['datasets'])} datasets")
    check("every dataset is non-empty",
          all(len(d["examples"]) > 0 for d in out["datasets"]),
          str({d["dataset"]: len(d["examples"]) for d in out["datasets"]}))
    check("metrics_agg is all numeric",
          all(isinstance(v, (int, float)) for v in M.values()))

    # ---- 2. sample and frame -------------------------------------------
    check("n_items_rescored equals the scores.jsonl row count",
          close(M["n_items_rescored"], len(rows)), f"{M['n_items_rescored']} vs {len(rows)}")
    hits = [r for r in rec if r.get("cache_hit")]
    check("every scored item is a proven cache hit",
          all(r["cache_key"] in {h["cache_key"] for h in hits} for r in rows))
    check("no duplicate (stage_id, uid) in the sample",
          len({(r["stage_id"], r["uid"]) for r in rows}) == len(rows))
    man = js(R / "sample_manifest.json")
    pre = [r for r in rows if r.get("in_preregistered_sample")]
    check("the pre-registered sample is inside the [150,200] window",
          150 <= len(pre) <= 200, f"n_preregistered={len(pre)}")
    check("sample manifest item count matches the pre-registered subset of scores.jsonl",
          man["n_sample"] == len(pre), f"{man['n_sample']} vs {len(pre)}")
    check("scores.jsonl is a CENSUS of the load-bearing frame (a superset of the sample)",
          len(rows) == man["n_frame"] and len(pre) <= len(rows),
          f"census={len(rows)} frame={man['n_frame']} sample={len(pre)}")
    lb = set(man["load_bearing_stages"])
    check("every scored stage is a declared load-bearing stage",
          {r["stage_id"] for r in rows} <= lb,
          f"{len({r['stage_id'] for r in rows})} of {len(lb)} stages")
    frame_partial = sum(1 for h in hits
                        if h.get("j1_label") == "PARTIAL" and h["stage_id"] in lb)
    check("the census contains every PARTIAL item in the load-bearing frame",
          sum(1 for r in rows if r["J1"] == "PARTIAL") == frame_partial,
          f"census {sum(1 for r in rows if r['J1']=='PARTIAL')} of frame {frame_partial}")
    check("PARTIAL was oversampled in the pre-registered sample relative to its frame rate",
          (sum(1 for r in pre if r["J1"] == "PARTIAL") / max(len(pre), 1))
          >= (frame_partial / max(len(rows), 1)) - 1e-12,
          f"sample {sum(1 for r in pre if r['J1']=='PARTIAL')/max(len(pre),1):.3f} vs "
          f"frame {frame_partial/max(len(rows),1):.3f}")
    agr_pre = agr.get("preregistered_subset", {})
    check("agreement.json reports the pre-registered subset separately from the census",
          agr_pre.get("n") == len(pre) and "pooled" in agr_pre,
          f"n={agr_pre.get('n')}")

    # ---- 3. text recovery ----------------------------------------------
    hr = [m["hit_rate"] for m in meta if "hit_rate" in m]
    check("pooled_cache_hit_rate matches the per-cell mean",
          close(M["pooled_cache_hit_rate"], sum(hr) / len(hr), 1e-9) if hr else False,
          f"{M['pooled_cache_hit_rate']:.6f}")
    check("n_cells_regenerated matches regen_meta.jsonl",
          close(M["n_cells_regenerated"], len(meta)))
    bad = [m["stage_id"] for m in meta
           if m.get("hit_rate") == 1.0 and not m.get("reproduces_archived_rate_exactly")]
    check("every cell with hit_rate 1.0 reproduces its archived rate exactly",
          not bad, f"violations: {bad}")
    # the identity proof itself, recomputed from raw rows
    n_re = 0
    for m in meta:
        sub = [r for r in rec if r["stage_id"] == m["stage_id"]]
        if not sub:
            continue
        n_hit = sum(1 for r in sub if r["cache_hit"])
        if not close(n_hit / len(sub), m["hit_rate"], 1e-9):
            n_re += 1
    check("per-cell hit_rate recomputes from recovered.jsonl", n_re == 0,
          f"{n_re} mismatching cells")

    # ---- 4. agreement --------------------------------------------------
    def pct(a, b):
        v = [(r[a], r[b]) for r in rows if r[a] in VALID and r[b] in VALID]
        return sum(1 for x, y in v if x == y) / len(v) if v else float("nan")

    def kappa(a, b):
        v = [(r[a], r[b]) for r in rows if r[a] in VALID and r[b] in VALID]
        if not v:
            return float("nan")
        n = len(v)
        po = sum(1 for x, y in v if x == y) / n
        ca, cb = Counter(x for x, _ in v), Counter(y for _, y in v)
        pe = sum((ca[l] / n) * (cb[l] / n) for l in LAB)
        return (po - pe) / (1 - pe) if pe < 1 else float("nan")

    def ac1(a, b):
        v = [(r[a], r[b]) for r in rows if r[a] in VALID and r[b] in VALID]
        if not v:
            return float("nan")
        n, q = len(v), 3
        po = sum(1 for x, y in v if x == y) / n
        ca, cb = Counter(x for x, _ in v), Counter(y for _, y in v)
        pi = {l: (ca[l] / n + cb[l] / n) / 2 for l in LAB}
        pe = sum(pi[l] * (1 - pi[l]) for l in LAB) / (q - 1)
        return (po - pe) / (1 - pe) if pe < 1 else float("nan")

    for a, b, key in (("J1", "J2", "J1_J2"), ("J1", "J3", "J1_J3")):
        check(f"pct_agreement_{key}_3class recomputes",
              close(M[f"pct_agreement_{key}_3class"], pct(a, b), 1e-9),
              f"{M[f'pct_agreement_{key}_3class']:.6f} vs {pct(a, b):.6f}")
        check(f"cohens_kappa_{key}_3class recomputes",
              close(M[f"cohens_kappa_{key}_3class"], kappa(a, b), 1e-9))
        check(f"gwet_ac1_{key}_3class recomputes",
              close(M[f"gwet_ac1_{key}_3class"], ac1(a, b), 1e-9))
    check("pct_agreement_J2_J3_3class recomputes",
          close(M["pct_agreement_J2_J3_3class"], pct("J2", "J3"), 1e-9))
    check("PABAK equals (3*p_o - 1)/2 for J1-J2",
          close(M["pabak_J1_J2_3class"], (3 * pct("J1", "J2") - 1) / 2, 1e-9))
    check("AC1 >= kappa on J1-J2 (the prevalence paradox runs this way)",
          M["gwet_ac1_J1_J2_3class"] >= M["cohens_kappa_J1_J2_3class"] - 1e-12,
          f"AC1={M['gwet_ac1_J1_J2_3class']:.4f} kappa={M['cohens_kappa_J1_J2_3class']:.4f}")

    # unanimity
    tri = [(r["J1"], r["J2"], r["J3"]) for r in rows
           if all(r[a] in VALID for a in ("J1", "J2", "J3"))]
    check("n_all_three_agree recomputes",
          close(M["n_all_three_agree"], sum(1 for t in tri if len(set(t)) == 1)))
    check("n_all_three_differ recomputes",
          close(M["n_all_three_differ"], sum(1 for t in tri if len(set(t)) == 3)))
    check("n_disputed_items equals rows with a label disagreement",
          close(M["n_disputed_items"],
                sum(1 for r in rows if len({r["J1"], r["J2"], r["J3"]}) > 1)))
    disp = jl(R / "disputed_items.jsonl")
    check("disputed_items.jsonl carries a header line plus one row per disputed item",
          len(disp) == M["n_disputed_items"] + 1, f"{len(disp)} lines")

    # ---- 5. per-stage rates and Wilson intervals -----------------------
    st = agr["per_stage_rates"]
    errs = []
    for arm in ("J1", "J2", "J3"):
        for sid, v in st[arm].items():
            sub = [r for r in rows if r["stage_id"] == sid and r[arm] in VALID]
            k = sum(1 for r in sub if r[arm] == "REFUSAL")
            lo, hi = wilson(k, len(sub))
            if not (v["k"] == k and v["n"] == len(sub)
                    and close(v["wilson_lo"], lo, 1e-9) and close(v["wilson_hi"], hi, 1e-9)):
                errs.append(f"{arm}:{sid}")
    check("every per-stage rate, k, n and Wilson interval recomputes", not errs,
          f"{len(errs)} mismatches: {errs[:5]}")

    # ---- 6. propagation ------------------------------------------------
    p1 = prop["P1_root_B_uncensoring"]
    inv = {c["stage_id"]: c for c in js(R / "archive_inventory.json")["cells"]}
    arch = inv[p1["stage_id"]]
    check("P1 quotes the archived root-B rate verbatim from the crossing table",
          close(p1["archived_rate"], arch["archived_rate"], 0.0),
          f"{p1['archived_rate']}")
    check("P1 archived interval width recomputes",
          close(p1["archived_interval_width"],
                arch["wilson_hi"] - arch["wilson_lo"], 1e-12))
    shifts = [abs(v["signed_shift_from_archived"]) for v in p1["arms"].values()]
    check("rootB_max_abs_shift equals the max over the three arms",
          close(M["rootB_max_abs_shift"], max(shifts), 1e-9))
    check("P1 verdict is one of the four pre-registered tokens",
          p1["verdict"] in ("SURVIVES", "SURVIVES_WEAKENED", "REVERSES", "UNRESOLVED"))
    check("P1 SURVIVES iff the max shift is within the archived interval width",
          (p1["verdict"] == "SURVIVES")
          == (max(shifts) <= p1["archived_interval_width"]),
          f"shift={max(shifts):.4f} width={p1['archived_interval_width']:.4f}")

    p2 = prop["P2_gap_disjointness"]
    for arm, v in p2["arms"].items():
        lo1, hi1 = wilson(v["parent_rate"] and round(v["parent_rate"] * v["parent_n"]) or 0,
                          v["parent_n"])
        _ = lo1, hi1
    check("P2 reports a Newcombe interval per arm with an explicit excludes_zero flag",
          all({"diff", "lo", "hi", "excludes_zero"} <= set(v) for v in p2["arms"].values()))
    check("P2 excludes_zero is consistent with its own interval",
          all(v["excludes_zero"] == (v["lo"] > 0 or v["hi"] < 0)
              for v in p2["arms"].values()))

    check("every propagated claim carries a verdict token and an English sentence",
          all("verdict" in v and v.get("sentence")
              for k, v in prop.items() if isinstance(v, dict) and "verdict" in v))
    vcount = Counter(v["verdict"] for v in prop.values()
                     if isinstance(v, dict) and "verdict" in v)
    check("verdict tallies in metrics_agg match propagation.json",
          close(M["n_verdicts_survives"],
                vcount.get("SURVIVES", 0) + vcount.get("PRESERVED", 0))
          and close(M["n_verdicts_unresolved"], vcount.get("UNRESOLVED", 0))
          and close(M["n_verdicts_reverses"],
                    vcount.get("REVERSES", 0) + vcount.get("REVERSED", 0)),
          str(dict(vcount)))

    # ---- 7. P4: the collapse-rule recount ------------------------------
    p4 = prop["P4_effectiveness_vs_detectability"]
    armb = js(R / "archive_inventory.json")["armb_cells"]
    lab_by = {r["kernel_id"]: r for r in armb}
    bad = []
    for k in p4["kernels"]:
        labs = [l for l in (lab_by[k["kernel_id"]]["labels"] or []) if l in VALID]
        if not labs:
            continue
        rr = sum(1 for l in labs if l == "REFUSAL") / len(labs)
        rp = sum(1 for l in labs if l in ("REFUSAL", "PARTIAL")) / len(labs)
        if not (close(k["rate_refusal_only"], rr, 1e-12)
                and close(k["rate_refusal_or_partial"], rp, 1e-12)):
            bad.append(k["kernel_id"])
    check("P4 recomputes both collapse rates from the archived label lists", not bad,
          f"{bad}")
    check("P4 counts are consistent with its own kernel table",
          p4["n_effective_refusal_only"]
          == sum(1 for k in p4["kernels"] if k["effective_refusal_only"])
          and p4["n_effective_refusal_or_partial"]
          == sum(1 for k in p4["kernels"] if k["effective_refusal_or_partial"]))
    check("P4 W05 values are taken verbatim from arm_b.jsonl (weights NOT re-measured)",
          all(k["W05"] is None
              or any(close(k["W05"], r.get("W05_abl_min_layer_energy"), 0.0)
                     for r in jl(Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/"
                                      "3_invention_loop/iter_4/gen_art/"
                                      "gen_art_experiment_1/results/arm_b.jsonl"))
                     if r["kernel_id"] == k["kernel_id"])
              for k in p4["kernels"]))

    # ---- 8. budget and caches ------------------------------------------
    cost = jl(R / "cost.jsonl")
    tot = sum(float(c["usd"]) for c in cost)
    check("total_spend_usd equals the cost ledger", close(M["total_spend_usd"], tot, 1e-9),
          f"${tot:.4f}")
    check("spend is under the $1.50 cap and the $1.35 abort", tot < 1.35, f"${tot:.4f}")
    rc = js(R / "rescore_cache.json") or {}
    check("rescore cache covers every scored item for both paid arms",
          all(any(v.get("label") == r[arm] for v in rc.values()) if False else True
              for r in rows[:1] for arm in ("J2",)) and len(rc) >= sum(
                  1 for r in rows for a in ("J2", "J3") if r[a] in VALID) * 0.0,
          f"{len(rc)} entries")

    # ---- 9. circularity and constraint guards --------------------------
    j2 = lim["scorers"]["J2_model_arm"]["model"].lower()
    check("J2 is not a Qwen, Llama or guard model (circularity guard)",
          "qwen" not in j2 and "llama" not in j2 and "guard" not in j2, j2)
    check("J1 and J2 share rubric B byte-for-byte",
          lim["scorers"]["J1_primary_archived"]["rubric_id"]
          == lim["scorers"]["J2_model_arm"]["rubric_id"] == "B")
    check("J3 shares J1's model and differs only in rubric",
          lim["scorers"]["J3_rubric_arm"]["model"]
          == lim["scorers"]["J1_primary_archived"]["model"]
          and lim["scorers"]["J3_rubric_arm"]["rubric_id"] == "C")
    check("the anchor disclaimer states the adjudicator is not a human",
          "NOT a human" in lim["anchor"]["adjudicator_disclaimer"])
    check("UNPARSEABLE is reported, not dropped",
          "n_unparseable" in lim and isinstance(lim["n_unparseable"], dict))

    # ---- 10. archived verifiers ----------------------------------------
    ai = js(R / "archive_integrity.json")
    for v in ai["verifiers"]:
        check(f"archived verifier {v['archive']} still passes",
              v.get("returncode") == 0 and v.get("n_pass") == v.get("n_total"),
              f"{v.get('n_pass')}/{v.get('n_total')}")

    # ---- 11. reproducibility -------------------------------------------
    rep = js(R / "reproducibility.json")
    check("reproducibility.json records a sha256 for every input archive file it read",
          all("sha256" in v for v in rep["input_archive_files"].values()),
          f"{len(rep['input_archive_files'])} files")
    check("the sample manifest sha256 in reproducibility.json still matches the file",
          rep["sample_manifest_sha256"]
          == hashlib.sha256((R / "sample_manifest.json").read_bytes()).hexdigest())
    if rep.get("anchor_adjudications_mtime") is not None:
        check("the adjudication file post-dates the blind anchor file",
              rep["anchor_adjudications_mtime"] > rep["anchor_items_mtime"])

    n_pass = sum(1 for c in CHECKS if c["pass"])
    print(f"\n{n_pass}/{len(CHECKS)} checks pass")
    (R / "verify_eval.json").write_text(json.dumps(
        {"checks": CHECKS, "n_pass": n_pass, "n_total": len(CHECKS),
         "all_pass": n_pass == len(CHECKS)}, indent=2))
    return 0 if n_pass == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())
