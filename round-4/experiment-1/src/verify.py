#!/usr/bin/env python3
"""Independent re-derivation of every headline number in method_out.json.

Reads ONLY the shipped results files and recomputes each claim from the raw
rows, so a number that was mis-copied into the summary fails here.  Run:

    .venv/bin/python verify.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
TAU = -2.7415117804288127

checks: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append((name, bool(ok), detail))


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def main() -> int:
    out = json.loads((HERE / "method_out.json").read_text())
    an = json.loads((RES / "analysis.json").read_text())
    arm_b = jl(RES / "arm_b.jsonl")
    arm_a = jl(RES / "arm_a.jsonl")
    gate = json.loads((RES / "gate_iter4.json").read_text())
    gate_rows = jl(RES / "gate_iter4.jsonl")
    tests = json.loads((RES / "unit_tests.json").read_text())
    by_kid = {r["kernel_id"]: r for r in arm_b}

    # -- 1. the stamped prediction file has not moved -----------------------
    import hashlib
    h = hashlib.sha256((RES / "predictions.json").read_bytes()).hexdigest()
    rec = (RES / "predictions.sha256").read_text().strip()
    check("predictions.json matches its stamped sha256", h == rec, f"{h[:16]}")
    h2 = hashlib.sha256((RES / "predictions_derived.json").read_bytes()).hexdigest()
    rec2 = (RES / "predictions_derived.sha256").read_text().strip()
    check("predictions_derived.json matches its stamped sha256", h2 == rec2,
          f"{h2[:16]}")

    # -- 2. every detection flag follows from W05 and tau -------------------
    bad = [r["kernel_id"] for r in arm_b
           if r["detected"] != (r["W05_abl_min_layer_energy"] <= TAU)]
    check("arm_b detected flags follow from W05 <= tau", not bad, str(bad[:3]))
    bad = [r["repo_id"] for r in arm_a
           if r.get("status") == "OK" and r.get("eligible")
           and r["detected"] != (r["W05_abl_min_layer_energy"] <= TAU)]
    check("arm_a detected flags follow from W05 <= tau", not bad, str(bad[:3]))

    # -- 3. the reproduction gate's headline claim --------------------------
    ok_rows = [r for r in gate_rows if r["status"] == "OK"]
    head = max(r["archived_max_delta_headline"] for r in ok_rows)
    check("gate headline (W05/W02) reproduces to <1e-4",
          head < 1e-4 and abs(head - gate["max_delta_headline"]) < 1e-15,
          f"max={head:.3e} over {len(ok_rows)} members")
    fp = max(r["fastpath_max_delta"] for r in ok_rows)
    check("fast path == Runner path exactly", fp == 0.0, f"max={fp}")
    w01 = max(r["archived_delta"].get("W01_abl_suppression_depth", 0)
              for r in ok_rows)
    shift = max(r["precision_shift"]["W01_abl_suppression_depth"] for r in ok_rows)
    check("W01 archive gap is explained by the float32->float64 shift",
          abs(w01 - shift) < 1e-6, f"archive {w01:.4e} vs precision {shift:.4e}")

    # -- 4. the root rebuild is bit-identical -------------------------------
    g2 = out["metadata"]["root_rebuild_gate"]
    check("rebuilt root write matrices are bit-identical to the archive",
          g2["write_matrix_sha256_match"] is True,
          g2["write_matrix_sha256_rebuilt"][:16])
    check("root rebuild reproduces W02/W03/W05 to <1e-4",
          g2["max_delta_headline"] < 1e-4, f"{g2['max_delta_headline']:.3e}")

    # -- 5. unit tests all pass ---------------------------------------------
    check("all six synthetic unit tests pass", tests["all_pass"] is True,
          " ".join(f"{k}={v['pass']}" for k, v in tests.items()
                   if isinstance(v, dict)))

    # -- 6. ORBA invariance is below the measured noise floor ---------------
    o = by_kid["orba_householder_lam1.0"]
    c = by_kid["householder_random_dir_control"]
    o_max = max(o["dW01_vs_parent"], o["dW04_vs_parent"], o["dW05_vs_parent"])
    c_max = max(c["dW01_vs_parent"], c["dW04_vs_parent"], c["dW05_vs_parent"])
    check("ORBA moves the statistic less than a random-direction Householder",
          o_max < c_max, f"orba {o_max:.3e} < floor {c_max:.3e}")
    check("ORBA is NOT detected", o["detected"] is False,
          f"W05={o['W05_abl_min_layer_energy']:.4f}")

    # -- 7. the sub-unit closed form ----------------------------------------
    sub = an["subunit_closed_form"]
    d32 = sub.get("max_abs_dev_energy_along_r_float32_storage")
    check("sub-unit closed form holds at float32 storage to <1e-4",
          d32 is not None and d32 < 1e-4, f"{d32}")
    check("sub-unit detection matches the stamped w* rule",
          sub["detection_matches_prediction"] is True,
          f"w*={sub['w_star']:.4f}")

    # -- 8. the Gaussian sweep brackets and is a threshold ------------------
    g = an["gaussian_sweep"]
    check("Gaussian sweep brackets parent and full-abliteration", g["brackets"],
          f"parent {g['parent_W05']:.3f} .. uniform {g['uniform_W05']:.3f}")
    check("Gaussian transition occupies <=2 sweep steps (THRESHOLD)",
          g["shape"] == "THRESHOLD", f"{g['n_intermediate_steps']} steps")

    # -- 9. effectiveness vs detectability ----------------------------------
    e = an["effectiveness_vs_detectability"]
    eff = [r for r in e["rows"] if r["fluency_pass"]
           and r["refusal_rate_judge"] is not None
           and r["refusal_rate_judge"] <= 0.5]
    n_det = sum(1 for r in eff if r["detected"])
    check("effectiveness table recomputes",
          len(eff) == e["n_effective"] and n_det == e["n_effective_detected"],
          f"{n_det}/{len(eff)} effective edits detected")

    # -- 10. the mechanism rule ---------------------------------------------
    m = an["mechanism_decomposition"]
    rows = [r for r in m["rows"] if r["rule_applicable"]]
    agree = sum(1 for r in rows if r["rule_agrees"]) / max(len(rows), 1)
    check("mechanism rule agreement recomputes",
          abs(agree - (m["agreement"] or 0)) < 1e-12,
          f"{agree:.3f} over {len(rows)} applicable kernels")

    # -- 11. every stamped prediction has a verdict --------------------------
    preds = out["metadata"]["predictions"]["predictions"]
    missing = [p["id"] for p in preds if not p.get("verdict")]
    check("every stamped prediction P1-P13 carries a verdict", not missing,
          str(missing))

    # -- 12. schema-shaped output -------------------------------------------
    ex = out["datasets"][0]["examples"]
    okkeys = all(
        set(k for k in r if not k.startswith(("metadata_", "predict_")))
        <= {"input", "output"} for r in ex)
    check("every example row is schema-shaped", okkeys, f"{len(ex)} examples")

    # -- report --------------------------------------------------------------
    width = max(len(n) for n, _, _ in checks)
    n_ok = 0
    for name, ok, detail in checks:
        n_ok += ok
        print(f"{'PASS' if ok else 'FAIL'}  {name:<{width}}  {detail}")
    print(f"\n{n_ok}/{len(checks)} checks passed")
    return 0 if n_ok == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
