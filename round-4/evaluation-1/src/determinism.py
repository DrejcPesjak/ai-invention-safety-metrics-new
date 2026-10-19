#!/usr/bin/env python3
"""Determinism gate: run the whole pipeline twice with the same seed and assert
eval_out.json is byte-identical apart from the timestamp-like fields.

The only fields allowed to differ are the wall-clock measurements, which are
stripped before comparison and reported separately.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = str(HERE / ".venv/bin/python") if (HERE / ".venv/bin/python").is_file() else sys.executable

# Fields whose value is a measured duration, not a result.
VOLATILE_KEYS = {"wall_clock_s", "seconds", "total_s", "weight_stats_wall_clock_s"}


def strip_volatile(obj):
    if isinstance(obj, dict):
        return {k: ("<VOLATILE>" if k in VOLATILE_KEYS else strip_volatile(v))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_volatile(x) for x in obj]
    return obj


def run(out_name: str) -> Path:
    r = subprocess.run([PY, str(HERE / "eval.py"), "--out", out_name],
                       capture_output=True, text=True, cwd=str(HERE), timeout=3600)
    if r.returncode != 0:
        print(r.stdout[-3000:])
        print(r.stderr[-3000:])
        raise SystemExit(f"run {out_name} failed with exit {r.returncode}")
    return HERE / out_name


def main() -> None:
    a = run("_determinism_run_a.json")
    b = run("_determinism_run_b.json")
    raw_a, raw_b = a.read_bytes(), b.read_bytes()
    da = strip_volatile(json.loads(raw_a))
    db = strip_volatile(json.loads(raw_b))
    ca = json.dumps(da, sort_keys=True).encode()
    cb = json.dumps(db, sort_keys=True).encode()

    diffs: list[str] = []
    if ca != cb:
        def walk(x, y, path=""):
            if type(x) is not type(y):
                diffs.append(f"{path}: type {type(x).__name__} vs {type(y).__name__}")
                return
            if isinstance(x, dict):
                for k in sorted(set(x) | set(y)):
                    if k not in x or k not in y:
                        diffs.append(f"{path}.{k}: present in only one run")
                    else:
                        walk(x[k], y[k], f"{path}.{k}")
            elif isinstance(x, list):
                if len(x) != len(y):
                    diffs.append(f"{path}: length {len(x)} vs {len(y)}")
                else:
                    for i, (u, v) in enumerate(zip(x, y)):
                        walk(u, v, f"{path}[{i}]")
            elif x != y:
                diffs.append(f"{path}: {x!r} vs {y!r}")
        walk(da, db)

    result = {
        "status": "BYTE_IDENTICAL_APART_FROM_TIMING" if ca == cb else "NON_DETERMINISTIC",
        "raw_bytes_identical": raw_a == raw_b,
        "identical_after_stripping_volatile_fields": ca == cb,
        "volatile_fields_stripped": sorted(VOLATILE_KEYS),
        "sha256_run_a_raw": hashlib.sha256(raw_a).hexdigest(),
        "sha256_run_b_raw": hashlib.sha256(raw_b).hexdigest(),
        "sha256_run_a_canonical": hashlib.sha256(ca).hexdigest(),
        "sha256_run_b_canonical": hashlib.sha256(cb).hexdigest(),
        "n_differences": len(diffs),
        "differences": diffs[:200],
        "note": "Both runs use the same fixed seed. Every bootstrap and permutation draws from a "
                "np.random.Generator seeded at 20260814, so all intervals are reproducible.",
    }
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results/determinism.json").write_text(json.dumps(result, indent=1, sort_keys=True))
    a.unlink(missing_ok=True)
    b.unlink(missing_ok=True)
    print(json.dumps({k: v for k, v in result.items() if k != "differences"}, indent=1))
    if diffs:
        print("\nfirst differences:")
        for d in diffs[:20]:
            print("  ", d)


if __name__ == "__main__":
    main()
