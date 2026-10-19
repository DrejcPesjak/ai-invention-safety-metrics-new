#!/usr/bin/env python3
"""Shared, dependency-free helpers for the iteration-5 numbers file.

Pure re-analysis: NO model weights, NO forward passes, NO LLM calls, NO Hub fetches.
Every function here is deterministic -- no RNG without an explicit seed, no timestamps,
no dict-iteration-order dependence (every key list is sorted before use).
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

# ---------------------------------------------------------------------------
# Archive map -- the exact paths probed. A missing path becomes UNAVAILABLE,
# never an estimate.
# ---------------------------------------------------------------------------
ROOT = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop")
A1 = ROOT / "iter_4/gen_art/gen_art_experiment_1"
A2 = ROOT / "iter_4/gen_art/gen_art_experiment_2"
A3 = ROOT / "iter_4/gen_art/gen_art_experiment_3"
A4 = ROOT / "iter_2/gen_art/gen_art_experiment_1"
A5 = ROOT / "iter_2/gen_art/gen_art_dataset_1"
A6 = ROOT / "iter_3/gen_art/gen_art_evaluation_1"
A7a = ROOT / "iter_3/gen_art/gen_art_research_1"
A7b = ROOT / "iter_4/gen_art/gen_art_research_1"
DRAFT4 = ROOT / "iter_4/gen_paper_text/gen_paper_text/.terminal_claude_agent_struct_out.json"

# The panel operating point, carried verbatim from A1/results/analysis.json.
TAU_FIXED = -2.7415117804288127

Z95 = 1.959963984540054  # two-sided normal quantile used by every Wilson interval here


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------
def sha256_of(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict]:
    out = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def dump_json(obj: Any, path: Path) -> str:
    """Deterministic dump: sorted keys, fixed separators, full float precision."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, sort_keys=True, indent=2, allow_nan=False, default=_jsonable)
    path.write_text(text)
    return sha256_of_text(text)


def _jsonable(o: Any) -> Any:
    # numpy scalars / arrays -> python
    if hasattr(o, "item") and not isinstance(o, (str, bytes)):
        try:
            return o.item()
        except Exception:  # pragma: no cover - defensive
            pass
    if hasattr(o, "tolist"):
        return o.tolist()
    raise TypeError(f"not JSON serialisable: {type(o)!r}")


def clean_float(x: Any) -> Any:
    """JSON has no NaN/Inf. Map them to explicit sentinel strings so nothing is
    silently dropped and nothing invents a value."""
    if isinstance(x, float):
        if math.isnan(x):
            return "NaN"
        if math.isinf(x):
            return "Infinity" if x > 0 else "-Infinity"
    return x


def deep_clean(o: Any) -> Any:
    if isinstance(o, dict):
        return {k: deep_clean(v) for k, v in sorted(o.items(), key=lambda kv: str(kv[0]))}
    if isinstance(o, (list, tuple)):
        return [deep_clean(v) for v in o]
    if isinstance(o, float):
        return clean_float(o)
    if hasattr(o, "item") and not isinstance(o, (str, bytes, int, float, bool)):
        try:
            return deep_clean(o.item())
        except Exception:
            return o
    return o


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
def wilson(k: int, n: int, z: float = Z95, continuity: bool = False) -> tuple[float | None, float | None]:
    """Wilson score interval.

        centre = (k + z^2/2) / (n + z^2)
        half   = z/(n + z^2) * sqrt( k(n-k)/n + z^2/4 )

    continuity=False everywhere in this artifact (flag carried explicitly in the
    numbers file so a reader never has to guess which variant produced a bound).
    """
    if n <= 0:
        return (None, None)
    if continuity:  # Newcombe's continuity-corrected form
        p = k / n
        denom = 2 * (n + z * z)
        a = 2 * n * p + z * z
        rad_lo = z * math.sqrt(max(z * z - 1 / n + 4 * n * p * (1 - p) + (4 * p - 2), 0.0))
        rad_hi = z * math.sqrt(max(z * z - 1 / n + 4 * n * p * (1 - p) - (4 * p - 2), 0.0))
        lo = max(0.0, (a - 1 - rad_lo) / denom)
        hi = min(1.0, (a + 1 + rad_hi) / denom)
        return (lo, hi)
    denom = n + z * z
    centre = (k + z * z / 2.0) / denom
    half = (z / denom) * math.sqrt(k * (n - k) / n + z * z / 4.0)
    return (max(0.0, centre - half), min(1.0, centre + half))


WILSON_FORMULA = (
    "centre=(k+z^2/2)/(n+z^2); half=(z/(n+z^2))*sqrt(k*(n-k)/n+z^2/4); "
    "interval=[centre-half, centre+half] clipped to [0,1]; z=1.959963984540054; "
    "continuity_correction=False"
)


def _ranks_with_ties(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def auroc(pos: list[float], neg: list[float]) -> float | None:
    """Mann-Whitney AUROC of `pos` scored HIGHER than `neg`. Ties count 0.5."""
    if not pos or not neg:
        return None
    allv = list(pos) + list(neg)
    r = _ranks_with_ties(allv)
    rp = sum(r[: len(pos)])
    n1, n2 = len(pos), len(neg)
    return (rp - n1 * (n1 + 1) / 2.0) / (n1 * n2)


def spearman(x: list[float], y: list[float]) -> float | None:
    if len(x) < 3 or len(x) != len(y):
        return None
    rx, ry = _ranks_with_ties(list(x)), _ranks_with_ties(list(y))
    return pearson(rx, ry)


def pearson(x: list[float], y: list[float]) -> float | None:
    n = len(x)
    if n < 2 or n != len(y):
        return None
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def bootstrap_ci(
    x: list[float],
    y: list[float],
    stat,
    n_boot: int,
    seed: int,
    method: str = "percentile",
) -> dict:
    """Paired bootstrap over the resampling unit (rows of x/y, which the caller names)."""
    import numpy as np

    if len(x) < 3:
        return {"point": None, "lo": None, "hi": None, "n_boot": n_boot, "seed": seed,
                "ci_method": method, "n_valid_resamples": 0}
    rng = np.random.default_rng(seed)
    point = stat(x, y)
    n = len(x)
    draws: list[float] = []
    idx = rng.integers(0, n, size=(n_boot, n))
    for row in idx:
        xs = [x[i] for i in row]
        ys = [y[i] for i in row]
        v = stat(xs, ys)
        if v is not None and not math.isnan(v):
            draws.append(v)
    if not draws:
        return {"point": point, "lo": None, "hi": None, "n_boot": n_boot, "seed": seed,
                "ci_method": method, "n_valid_resamples": 0}
    draws.sort()
    lo = draws[max(0, int(math.floor(0.025 * len(draws))))]
    hi = draws[min(len(draws) - 1, int(math.ceil(0.975 * len(draws))) - 1)]
    return {"point": point, "lo": lo, "hi": hi, "n_boot": n_boot, "seed": seed,
            "ci_method": f"{method} bootstrap", "n_valid_resamples": len(draws)}


def norm_ppf(p: float) -> float:
    """Acklam's inverse normal CDF -- deterministic, no scipy dependence."""
    a = [-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
         1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00]
    b = [-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
         6.680131188771972e01, -1.328068155288572e01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
         -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00,
         3.754408661907416e00]
    pl, ph = 0.02425, 1 - 0.02425
    if p < pl:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > ph:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def two_proportion_power(p1: float, p2: float, n1: int, n2: int, alpha: float = 0.05) -> float:
    """Power of a two-sided two-proportion z-test (pooled-variance null, unpooled
    alternative), normal approximation."""
    if p1 == p2:
        return alpha
    pbar = (p1 * n1 + p2 * n2) / (n1 + n2)
    se0 = math.sqrt(pbar * (1 - pbar) * (1 / n1 + 1 / n2))
    se1 = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    if se1 <= 0:
        return 1.0
    zc = norm_ppf(1 - alpha / 2)
    d = abs(p2 - p1)
    z_up = (d - zc * se0) / se1
    z_lo = (-d - zc * se0) / se1
    return _norm_cdf(z_up) + _norm_cdf(z_lo)


def _norm_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def smallest_detectable_upward(p1: float, n: int, power: float = 0.80,
                               alpha: float = 0.05, step: float = 0.0001) -> float | None:
    """Smallest p2 > p1 whose two-proportion power reaches `power` at n per group.
    Grid search on a fixed 1e-4 grid -- deterministic, no optimiser state."""
    steps = int(round((1.0 - p1) / step))
    for i in range(1, steps + 1):
        p2 = p1 + i * step
        if p2 > 1.0:
            break
        if two_proportion_power(p1, p2, n, n, alpha) >= power:
            return round(p2, 6)
    return None


# ---------------------------------------------------------------------------
# numbers.json entry factory -- schema EXTENDED from A2/results/numbers.json so
# the two files are mergeable (same nine keys, plus five new ones).
# ---------------------------------------------------------------------------
def num(
    value: Any,
    units: str | None,
    *,
    n: Any = None,
    ci_low: Any = None,
    ci_high: Any = None,
    ci_method: str | None = None,
    source_file: str | None = None,
    key_path: str | None = None,
    raw_value: Any = None,
    recomputed_from_rows: bool = False,
    orientation_convention: str | None = None,
    status: str = "OK",
    computed_by: str = "eval.py",
    note: str | None = None,
) -> dict:
    return {
        "value": clean_float(value),
        "units": units,
        "n": n,
        "ci_low": clean_float(ci_low),
        "ci_high": clean_float(ci_high),
        "ci_method": ci_method,
        "source_file": source_file,
        "source_rows": None,
        "computed_by": computed_by,
        # --- extensions ---
        "key_path": key_path,
        "raw_value": clean_float(raw_value) if not isinstance(raw_value, (list, dict)) else raw_value,
        "recomputed_from_rows": recomputed_from_rows,
        "orientation_convention": orientation_convention,
        "status": status,
        "note": note,
    }


def rel(p: Path | str) -> str:
    """Archive path rendered relative to ROOT so provenance is greppable."""
    return str(Path(p)).replace(str(ROOT) + "/", "")


def approx(a: Any, b: Any, tol: float = 1e-12) -> bool:
    if a is None or b is None:
        return a is b
    try:
        if isinstance(a, str) or isinstance(b, str):
            return a == b
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return a == b


def sorted_unique(xs: Iterable) -> list:
    return sorted(set(xs), key=lambda v: (v is None, str(v)))
