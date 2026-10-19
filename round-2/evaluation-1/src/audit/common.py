"""Shared paths, logging and helpers for the iteration-1 negative-results audit.

Everything here is READ-ONLY with respect to the three archived experiment trees.
The estimators are IMPORTED from the archived E1 library so the audit uses the
exact machinery the original artifact used; nothing is reimplemented.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
WORKSPACE = Path(__file__).resolve().parent.parent
OUT = WORKSPACE / "out"
FIGS = WORKSPACE / "figs"
LOGS = WORKSPACE / "logs"
for _d in (OUT, FIGS, LOGS):
    _d.mkdir(parents=True, exist_ok=True)

_ITER1 = Path("/ai-inventor/aii_data/runs/run_CbJDs3opF7E_/3_invention_loop/iter_1/gen_art")
E1 = _ITER1 / "gen_art_experiment_1"
E2 = _ITER1 / "gen_art_experiment_2"
E3 = _ITER1 / "gen_art_experiment_3"

# Make the archived E1 `spi` package importable so paired_bootstrap_diff,
# cluster_bootstrap_ci, half_life_auc and wilson_ci are the ORIGINAL ones.
if str(E1) not in sys.path:
    sys.path.insert(0, str(E1))

SEED_BOOTSTRAP = 11          # matches spi.indicators.paired_bootstrap_diff default
SEED_CLUSTER = 7             # matches spi.indicators.cluster_bootstrap_ci default
SEED_SAMPLING = 20260813     # judge-probe sampling seed, recorded in the output
N_BOOT = 5000

REF_MODEL = "qwen3-0.6b/instruct"
DIRECTIONS = ("toward_refuse", "toward_comply", "random_direction")
READOUTS = ("layerL", "final")


# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
def setup_logging(tag: str) -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO",
               format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{tag}.log", rotation="30 MB", level="DEBUG")


# --------------------------------------------------------------------------- #
# IO helpers
# --------------------------------------------------------------------------- #
def load_json(p: Path) -> Any:
    return json.loads(p.read_text())


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def dump_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, default=_default))
    logger.info(f"wrote {p} ({p.stat().st_size / 1024:.1f} KB)")


def _default(o: Any) -> Any:
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(f"not JSON serialisable: {type(o)}")


def clean(o: Any) -> Any:
    """Recursively replace non-finite floats with None (schema hygiene)."""
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        f = float(o)
        return f if np.isfinite(f) else None
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


# --------------------------------------------------------------------------- #
# Substitution log — every time a planned field is absent we record what we used
# --------------------------------------------------------------------------- #
_SUBS: list[dict[str, Any]] = []


def record_substitution(analysis: str, planned_field: str, used_instead: str,
                        reason: str, impact: str) -> None:
    _SUBS.append({"analysis": analysis, "planned_field": planned_field,
                  "used_instead": used_instead, "reason": reason,
                  "impact_on_conclusion": impact})
    logger.warning(f"SUBSTITUTION [{analysis}] {planned_field} -> {used_instead}: {reason}")


def flush_substitutions() -> None:
    """Merge into out/field_substitutions.json (stages run separately)."""
    p = OUT / "field_substitutions.json"
    existing = load_json(p) if p.exists() else []
    keys = {(e["analysis"], e["planned_field"]) for e in existing}
    for s in _SUBS:
        if (s["analysis"], s["planned_field"]) not in keys:
            existing.append(s)
    dump_json(p, existing)


# --------------------------------------------------------------------------- #
# Statistics that are NOT in the archived library
# --------------------------------------------------------------------------- #
def spearman_rho(x: list[float], y: list[float]) -> float:
    """Spearman rho with average ranks (identical to scipy for our n=4 cases)."""
    from scipy.stats import rankdata
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    den = float(np.sqrt((rx ** 2).sum() * (ry ** 2).sum()))
    return float((rx * ry).sum() / den) if den > 0 else float("nan")


def auroc_from_scores(pos: list[float], neg: list[float]) -> float:
    """Mann-Whitney U / (n_pos * n_neg), ties counted at 0.5."""
    from scipy.stats import rankdata
    if not pos or not neg:
        return float("nan")
    allv = np.concatenate([np.asarray(pos, float), np.asarray(neg, float)])
    r = rankdata(allv)
    n1, n2 = len(pos), len(neg)
    u = r[:n1].sum() - n1 * (n1 + 1) / 2.0
    return float(u / (n1 * n2))


def bootstrap_stat_ci(fn, arrays: list[np.ndarray], n_reps: int = 2000,
                      seed: int = 13) -> dict[str, Any]:
    """Non-parametric bootstrap of an arbitrary statistic over resampled arrays."""
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(n_reps):
        rs = [a[rng.integers(0, len(a), len(a))] for a in arrays]
        try:
            v = fn(*rs)
        except Exception:  # noqa: BLE001 - degenerate resample
            continue
        if np.isfinite(v):
            draws.append(float(v))
    if len(draws) < 20:
        return {"point": None, "ci_lo": None, "ci_hi": None, "n_reps": len(draws)}
    return {"point": float(fn(*arrays)),
            "ci_lo": float(np.percentile(draws, 2.5)),
            "ci_hi": float(np.percentile(draws, 97.5)),
            "n_reps": len(draws)}


def cohens_kappa(a: list[str], b: list[str], labels: list[str]) -> float:
    """Cohen's kappa for two raters over a fixed label set."""
    n = len(a)
    if n == 0:
        return float("nan")
    idx = {l: i for i, l in enumerate(labels)}
    m = np.zeros((len(labels), len(labels)), dtype=float)
    for x, y in zip(a, b):
        if x in idx and y in idx:
            m[idx[x], idx[y]] += 1
    tot = m.sum()
    if tot == 0:
        return float("nan")
    po = np.trace(m) / tot
    pe = float((m.sum(axis=1) / tot * (m.sum(axis=0) / tot)).sum())
    if abs(1 - pe) < 1e-12:
        return float("nan")
    return float((po - pe) / (1 - pe))


def confusion(a: list[str], b: list[str], labels: list[str]) -> list[list[int]]:
    idx = {l: i for i, l in enumerate(labels)}
    m = [[0] * len(labels) for _ in labels]
    for x, y in zip(a, b):
        if x in idx and y in idx:
            m[idx[x]][idx[y]] += 1
    return m
