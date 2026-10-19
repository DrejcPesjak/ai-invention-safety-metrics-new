#!/usr/bin/env python3
"""Archive access layer: path resolution, manifest, provenance, and shared statistics.

PURE RE-ANALYSIS.  This module never loads model weights, never runs a forward
pass, never calls an LLM and never touches the HuggingFace Hub.  It only reads
archived JSON/JSONL from the six iteration-2 / iteration-3 trees.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path, PurePath
from typing import Any, Iterable

import numpy as np
from loguru import logger

# --------------------------------------------------------------------------
# Archive roots.  A1-A4 are declared dependencies; A5/A6 are read directly from
# disk because an evaluation artifact may only declare experiment/dataset deps.
# --------------------------------------------------------------------------
LOOP = Path("/ai-inventor/aii_data/runs/run_UtpduT_D2IS2/3_invention_loop")
ARCHIVES: dict[str, Path] = {
    "A1": LOOP / "iter_3/gen_art/gen_art_experiment_1",
    "A2": LOOP / "iter_3/gen_art/gen_art_experiment_2",
    "A3": LOOP / "iter_2/gen_art/gen_art_experiment_1",
    "A4": LOOP / "iter_2/gen_art/gen_art_dataset_1",
    "A5": LOOP / "iter_3/gen_art/gen_art_evaluation_1",
    "A6": LOOP / "iter_3/gen_art/gen_art_research_1",
}

SEED = 20260814
BOOT_B = 10_000

# Directories/files that are environment noise, not archive content.
_MANIFEST_SKIP_DIRS = {".venv", "__pycache__", ".git", "hf_home", "cache", "temp", "figs"}
_MANIFEST_SKIP_SUFFIX = {".ptylog", ".pyc", ".pdf", ".png", ".pt", ".safetensors"}


def sha256_file(p: Path, cap: int = 64 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        read = 0
        while read < cap:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
            read += len(chunk)
    return h.hexdigest()


def _role_guess(rel: str) -> str:
    r = rel.lower()
    table = [
        ("arm1_real", "arm-1 real new-uploader checkpoint rows (W01-W05 + card evidence)"),
        ("arm1_synth", "arm-1 in-house synthetic recipe variants"),
        ("arm1_candidates", "Hub candidate search + card-evidence verification records"),
        ("arm2_pairs", "arm-2 pre-declared parent/candidate E_1 pairs"),
        ("arm2_all", "arm-2 all pairs including synthetics"),
        ("long_table_depth", "arm-3 (member, metric, depth) long table"),
        ("ladder_e_v1", "per-layer e_v1 profiles for ladder stages"),
        ("ladder", "34-stage laundering ladder rows"),
        ("scan_enumeration", "Hub enumeration counters for the wild scan"),
        ("scan", "wild-scan per-repo weight statistics"),
        ("numbers.json", "iteration-3 evaluation numbers (carry-forward source)"),
        ("metric_spec", "frozen 53-metric declaration (sha 544ff994...)"),
        ("battery.jsonl", "iteration-2 53-metric battery rows"),
        ("behaviour", "iteration-2 behavioural readout"),
        ("research_out", "iteration-3 prior-art dossier"),
        ("full_method_out", "assembled experiment artifact"),
        ("full_data_out", "assembled dataset artifact"),
        ("full_eval_out", "assembled evaluation artifact"),
        ("verify.py", "archived cross-check script (17 recomputations)"),
        ("wstats.py", "independent W01-W05 reimplementation"),
        ("diagnostics", "gate / diagnostic records"),
        ("root.json", "in-house abliterated root model record"),
        ("crossing", "flag-death vs uncensoring-death crossing curves"),
        ("robustness", "statistic survival across the ladder"),
    ]
    for key, role in table:
        if key in r:
            return role
    if r.endswith(".py"):
        return "source"
    if r.endswith(".md"):
        return "documentation"
    if r.endswith(".log") or "/logs/" in r:
        return "run log"
    return "other archive file"


def walk_archive(root: Path) -> list[Path]:
    """Walk an archive tree, PRUNING environment directories instead of descending them."""
    import os

    hits: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in _MANIFEST_SKIP_DIRS)
        for fn in sorted(filenames):
            hits.append(Path(dirpath) / fn)
    return hits


def build_manifest() -> list[dict[str, Any]]:
    """STEP 0: walk all six trees; record size + sha256 + a one-line role guess."""
    out: list[dict[str, Any]] = []
    for tag, root in ARCHIVES.items():
        if not root.is_dir():
            out.append({"archive": tag, "path": str(root), "status": "ARCHIVE_ROOT_MISSING"})
            continue
        for p in walk_archive(root):
            if not p.is_file():
                continue
            rel = p.relative_to(root)
            if p.suffix in _MANIFEST_SKIP_SUFFIX:
                continue
            st = p.stat()
            if st.st_size > 96 * 1024 * 1024:
                digest = "SKIPPED_TOO_LARGE"
            else:
                digest = sha256_file(p)
            out.append(
                {
                    "archive": tag,
                    "rel_path": str(rel),
                    "size_bytes": st.st_size,
                    "sha256": digest,
                    "role_guess": _role_guess(str(rel)),
                }
            )
    logger.info(f"manifest: {len(out)} files across {len(ARCHIVES)} archives")
    return out


# --------------------------------------------------------------------------
# Resolution + provenance
# --------------------------------------------------------------------------
class Resolver:
    """Resolve archive files by GLOB, never by assumed filename."""

    def __init__(self) -> None:
        self.resolved: dict[str, str] = {}
        self.missing: list[dict[str, Any]] = []

    _cache: dict[str, list[Path]] = {}

    def _files(self, archive: str) -> list[Path]:
        if archive not in Resolver._cache:
            Resolver._cache[archive] = walk_archive(ARCHIVES[archive])
        return Resolver._cache[archive]

    def glob_one(self, archive: str, *patterns: str) -> Path | None:
        root = ARCHIVES[archive]
        files = self._files(archive)
        for pat in patterns:
            hits = [h for h in files if h.match(pat) or PurePath(str(h.relative_to(root))).match(pat)]
            if hits:
                key = f"{archive}:{patterns[0]}"
                self.resolved[key] = str(hits[0].relative_to(root))
                return hits[0]
        self.missing.append({"archive": archive, "patterns": list(patterns)})
        logger.warning(f"UNRESOLVED glob {archive} {patterns}")
        return None

    def read_json(self, archive: str, *patterns: str) -> Any:
        p = self.glob_one(archive, *patterns)
        return None if p is None else json.loads(p.read_text())

    def read_jsonl(self, archive: str, *patterns: str) -> list[dict] | None:
        p = self.glob_one(archive, *patterns)
        if p is None:
            return None
        return [json.loads(ln) for ln in p.read_text().splitlines() if ln.strip()]


def prov(file: str, line_or_key: str, raw_value: Any) -> dict[str, Any]:
    """Every emitted number carries provenance = {file, line_or_key, raw_value}."""
    if isinstance(raw_value, float) and (math.isnan(raw_value) or math.isinf(raw_value)):
        raw_value = str(raw_value)
    return {"file": file, "line_or_key": line_or_key, "raw_value": raw_value}


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------
def auroc(pos: Iterable[float], neg: Iterable[float], higher_is_positive: bool = True) -> float | None:
    """Mann-Whitney AUROC with mid-ranks for ties.  None if either side is empty."""
    pos = [float(x) for x in pos]
    neg = [float(x) for x in neg]
    if not pos or not neg:
        return None
    if not higher_is_positive:
        pos = [-x for x in pos]
        neg = [-x for x in neg]
    wins = 0.0
    for a in pos:
        for b in neg:
            wins += 1.0 if a > b else (0.5 if a == b else 0.0)
    return wins / (len(pos) * len(neg))


def wilson95(k: int, n: int) -> tuple[float, float]:
    """Wilson score interval (primary for small n and rates near 0)."""
    if n <= 0:
        return (float("nan"), float("nan"))
    z = 1.959963984540054
    p = k / n
    d = 1.0 + z * z / n
    c = p + z * z / (2 * n)
    hw = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - hw) / d, (c + hw) / d)


def boot_rate_ci(k: int, n: int, rng: np.random.Generator, b: int = BOOT_B) -> tuple[float, float]:
    """Item-level nonparametric bootstrap of a binomial rate."""
    if n <= 0:
        return (float("nan"), float("nan"))
    items = np.zeros(n)
    items[:k] = 1.0
    draws = rng.integers(0, n, size=(b, n))
    reps = items[draws].mean(axis=1)
    return (float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5)))


def newcombe_diff(k1: int, n1: int, k2: int, n2: int) -> tuple[float, float]:
    """Newcombe hybrid-score interval for p1 - p2 (closed-form cross-check)."""
    l1, u1 = wilson95(k1, n1)
    l2, u2 = wilson95(k2, n2)
    p1, p2 = k1 / n1, k2 / n2
    lo = (p1 - p2) - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = (p1 - p2) + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return (lo, hi)


def boot_diff_ci(
    k1: int, n1: int, k2: int, n2: int, rng: np.random.Generator, b: int = BOOT_B
) -> tuple[float, float]:
    """Independent-proportions item bootstrap of p1 - p2."""
    if n1 <= 0 or n2 <= 0:
        return (float("nan"), float("nan"))
    a = np.zeros(n1)
    a[:k1] = 1.0
    c = np.zeros(n2)
    c[:k2] = 1.0
    ra = a[rng.integers(0, n1, size=(b, n1))].mean(axis=1)
    rc = c[rng.integers(0, n2, size=(b, n2))].mean(axis=1)
    d = ra - rc
    return (float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)))


def two_prop_mdd_directional(
    n: int, p_base: float, sign: int, power: float = 0.80, alpha: float = 0.05
) -> float | None:
    """Minimum detectable rate difference in ONE direction (+1 = increase, -1 = decrease).

    Two independent proportions of size `n`, two-sided z test at `alpha`.  Returns None if the
    swept range runs out of the unit interval before reaching the requested power.
    """
    from scipy.stats import norm

    za = norm.ppf(1 - alpha / 2)
    zb = norm.ppf(power)
    for step in range(1, 10001):
        d = step / 10000.0
        p2 = p_base + sign * d
        if not (0.0 < p2 < 1.0):
            return None
        pbar = (p_base + p2) / 2
        se0 = math.sqrt(2 * pbar * (1 - pbar) / n)
        se1 = math.sqrt(p_base * (1 - p_base) / n + p2 * (1 - p2) / n)
        if se1 <= 0:
            continue
        if (d - za * se0) / se1 >= zb:
            return d
    return None


def two_prop_mdd(n: int, p_base: float, power: float = 0.80, alpha: float = 0.05) -> float | None:
    """Minimum detectable |rate difference|: the smaller of the two directional magnitudes."""
    vals = [v for v in (two_prop_mdd_directional(n, p_base, s, power, alpha) for s in (+1, -1))
            if v is not None]
    return min(vals) if vals else None


def lineage_boot_auroc_diff(
    rows: list[dict],
    score_a: str,
    score_b: str,
    label_key: str,
    lineage_key: str,
    a_higher_pos: bool,
    b_higher_pos: bool,
    rng: np.random.Generator,
    b: int = BOOT_B,
) -> dict[str, Any]:
    """Paired AUROC difference (A - B) with the resampling unit = LINEAGE."""
    lineages = sorted({r[lineage_key] for r in rows})
    by_lin: dict[str, list[dict]] = {L: [] for L in lineages}
    for r in rows:
        by_lin[r[lineage_key]].append(r)

    def _pair(sub: list[dict]) -> tuple[float | None, float | None]:
        pa = [r[score_a] for r in sub if r[label_key] == 1]
        na = [r[score_a] for r in sub if r[label_key] == 0]
        pb = [r[score_b] for r in sub if r[label_key] == 1]
        nb = [r[score_b] for r in sub if r[label_key] == 0]
        return auroc(pa, na, a_higher_pos), auroc(pb, nb, b_higher_pos)

    a0, b0 = _pair(rows)
    if a0 is None or b0 is None:
        return {"status": "DEGENERATE", "n_lineages": len(lineages)}
    reps, degen = [], 0
    idx = rng.integers(0, len(lineages), size=(b, len(lineages)))
    for row in idx:
        sub: list[dict] = []
        for j in row:
            sub.extend(by_lin[lineages[j]])
        aa, bb = _pair(sub)
        if aa is None or bb is None:
            degen += 1
            continue
        reps.append(aa - bb)
    if not reps:
        return {"status": "ALL_REPLICATES_DEGENERATE", "n_lineages": len(lineages)}
    arr = np.asarray(reps)
    return {
        "status": "OK",
        "auroc_a": a0,
        "auroc_b": b0,
        "paired_diff": a0 - b0,
        "ci_lo": float(np.percentile(arr, 2.5)),
        "ci_hi": float(np.percentile(arr, 97.5)),
        "n_lineages": len(lineages),
        "n_items": len(rows),
        "B": b,
        "n_degenerate_replicates": degen,
        "resampling_unit": "lineage",
    }


def perm_p_auroc(
    pos: list[float], neg: list[float], higher_is_positive: bool, rng: np.random.Generator, n_perm: int = 10_000
) -> dict[str, Any]:
    """Permutation p with the EXACT floor 1/C(n,k) reported beside it (iter-3 convention)."""
    obs = auroc(pos, neg, higher_is_positive)
    if obs is None:
        return {"p_permutation": None, "exact_floor": None, "observed": None}
    allv = np.array(pos + neg, dtype=float)
    k = len(pos)
    ge = 0
    for _ in range(n_perm):
        rng.shuffle(allv)
        v = auroc(list(allv[:k]), list(allv[k:]), higher_is_positive)
        if v is not None and v >= obs:
            ge += 1
    return {
        "observed": obs,
        "p_permutation": (1 + ge) / (1 + n_perm),
        "n_permutations": n_perm,
        "exact_floor": 1.0 / float(math.comb(len(allv), k)),
        "exact_floor_expr": f"1/C({len(allv)},{k})",
    }


def recover_kn(rate: float, n_max: int = 40) -> tuple[int, int, float]:
    """Back out the ACHIEVED denominator from a stored rate.

    Returns (k, n, residual).  The achieved denominator is at most the nominal one, and a stage
    that scored every item has n = n_max.  So the reconstruction takes the LARGEST n <= n_max whose
    rational k/n reproduces the stored rate exactly -- taking the smallest instead would report
    0.200 as 1/5 rather than 8/40 and understate every interval.  If no denominator reproduces the
    rate exactly, the closest one is returned and residual = |rate - k/n| is non-zero, which the
    caller flags when it exceeds 0.5/n.
    """
    if rate is None:
        return (0, 0, float("nan"))
    best = None
    for n in range(n_max, 0, -1):
        k = round(rate * n)
        if k < 0 or k > n:
            continue
        res = abs(rate - k / n)
        if res < 1e-12:
            return (k, n, res)
        if best is None or res < best[2]:
            best = (k, n, res)
    if best is None:
        fr = Fraction(rate).limit_denominator(n_max)
        return (fr.numerator, fr.denominator, abs(rate - float(fr)))
    return best
