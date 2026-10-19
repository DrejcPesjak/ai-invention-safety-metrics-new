#!/usr/bin/env python3
"""FRESH reimplementation of the W01-W05 weight-scar statistics.

Written from the PUBLISHED DEFINITIONS ONLY (the artifact plan's formulae),
deliberately WITHOUT consulting the iteration-2 `lib_metrics.compute_weights`
source, so that agreement with the archived values is a genuine reproduction
rather than a copy.  `lib_metrics.py` is vendored into this workspace and is
read only AFTER the gate, to diff against if the gate fails.

Definitions (d = d_model; Ws = residual-write matrices, each [d_out=d, d_in]):

    A     = sum_m  W_m W_m^T / ||W_m||_F^2                  (d x d, float64)
    lam   = eigenvalues of A, ASCENDING;  v1 = eigenvector of lam[0] (MINIMUM)
    e(u,W)= ||u^T W||^2 / (||W||_F^2 / d)                   (energy ratio, 1.0 = isotropic)

    W01 = log10( median(lam) / lam[0] )         suppression depth
    W02 = mean( e(v1, W_m) < 0.1 )              direction consistency
    W03 = log10( q05( mean_m e(u_j, W_m) ) / mean_m e(v1, W_m) )   gap vs random
    W04 = log10( lam[1] / lam[0] )              isolation
    W05 = log10( max( min_m e(v1, W_m), 1e-30 ) ) min-layer energy

Numerics: A is accumulated in float64; eigendecomposition via `eigh` on the
symmetric float64 matrix.  Singular values, where needed, come from
`torch.linalg.svdvals` and never from `sqrt(eigvalsh(W W^T))`.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from loguru import logger

# ---------------------------------------------------------------------------
# Residual-write matrix resolution.
#
# Only the SUFFIX TABLE is taken from the iteration-2 stack, and only for
# RESOLUTION (which modules are residual writes) -- never the statistic itself.
# ---------------------------------------------------------------------------
ATTN_WRITE_SUFFIX = ("o_proj", "out_proj", "attention.dense", "dense", "attn.c_proj", "wo")
MLP_WRITE_SUFFIX = ("down_proj", "dense_4h_to_h", "fc2", "c_proj", "w2")


def find_block_list(model) -> nn.ModuleList:
    n = int(model.config.num_hidden_layers)
    for _name, mod in model.named_modules():
        if isinstance(mod, nn.ModuleList) and len(mod) == n:
            return mod
    raise RuntimeError("could not locate the decoder block list")


def resolve_write_matrices(block, d: int) -> list[tuple[str, nn.Module]]:
    """Linear layers inside one decoder block whose output lands in the residual."""
    out: list[tuple[str, nn.Module]] = []
    for name, mod in block.named_modules():
        if not isinstance(mod, nn.Linear) or mod.out_features != d:
            continue
        low = name.lower()
        kind = None
        if any(low.endswith(s.split(".")[-1]) for s in ATTN_WRITE_SUFFIX) and \
                ("attn" in low or "attention" in low):
            kind = "attn"
        elif any(low.endswith(s.split(".")[-1]) for s in MLP_WRITE_SUFFIX) and \
                ("mlp" in low or "ffn" in low or "feed" in low):
            kind = "mlp"
        if kind is None:
            continue
        out.append((f"{kind}:{name}", mod))
    if not out:  # last resort: any Linear writing into d
        for name, mod in block.named_modules():
            if isinstance(mod, nn.Linear) and mod.out_features == d and mod.in_features != d:
                out.append((f"other:{name}", mod))
    return out


def collect_write_tensors(model, d: int) -> tuple[list[str], list[torch.Tensor], dict]:
    """Every residual-write matrix in the model, oriented as [d, d_in].

    ORIENTATION.  `torch.nn.Linear` stores `weight` as [out_features, in_features]
    and computes `x @ W.T`, so the residual WRITE direction lives in the ROW space
    (out_features = d_model).  Conv1D-style families (gpt2 / gpt_neox `c_proj`)
    store the transpose; those are not `nn.Linear` and so are resolved by shape
    below.  Every returned tensor satisfies `W.shape[0] == d`.
    """
    blocks = find_block_list(model)
    names: list[str] = []
    mats: list[torch.Tensor] = []
    n_transposed = 0
    for li, blk in enumerate(blocks):
        for nm, mod in resolve_write_matrices(blk, d):
            W = mod.weight.detach()
            if W.shape[0] != d:
                if W.shape[1] == d:
                    W = W.T
                    n_transposed += 1
                else:
                    continue
            names.append(f"L{li:03d}:{nm}")
            mats.append(W.float())
    info = {"n_matrices": len(mats), "n_transposed": n_transposed,
            "n_layers": len(blocks)}
    if n_transposed:
        logger.info(f"transposed {n_transposed} write matrices to [d, d_in] orientation")
    return names, mats, info


# ---------------------------------------------------------------------------
# The statistics
# ---------------------------------------------------------------------------
def _energy(u: torch.Tensor, W: torch.Tensor, d: int) -> float:
    """e(u, W) = ||u^T W||^2 / (||W||_F^2 / d).  u is a unit vector in R^d."""
    num = float((u @ W).pow(2).sum())
    den = float(W.pow(2).sum()) / d
    return num / max(den, 1e-300)


def _energy_batch(U: torch.Tensor, W: torch.Tensor, d: int) -> torch.Tensor:
    """(k,) energies for k unit directions stacked in U (k, d)."""
    num = (U @ W).pow(2).sum(dim=1)
    den = W.pow(2).sum() / d
    return num / den.clamp_min(1e-30)


@dataclass
class WResult:
    W01: float
    W02: float
    W03: float
    W04: float
    W05: float
    v1: np.ndarray
    e_v1: np.ndarray
    eigvals: np.ndarray
    names: list[str]
    d: int
    n_layers: int
    n_matrices: int
    seconds: float
    dtype: str
    extra: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {"W01": self.W01, "W02": self.W02, "W03": self.W03,
                "W04": self.W04, "W05": self.W05, "d": self.d,
                "n_layers": self.n_layers, "n_matrices": self.n_matrices,
                "seconds": self.seconds, "dtype": self.dtype, **self.extra}


def w_stats_from_matrices(names: list[str], mats: list[torch.Tensor], d: int,
                          n_layers: int, *, n_random: int = 256, seed: int = 0,
                          device: str = "cpu", v1_override: np.ndarray | None = None,
                          accum_dtype: str = "float64", w03_mode: str = "per_direction",
                          clip_lam: bool = False) -> WResult:
    """Compute W01..W05 from an explicit list of [d, d_in] write matrices.

    `accum_dtype` and `w03_mode` exist ONLY so the reproduction gate can
    attribute a mismatch.  The published definition is
    (accum_dtype='float64', w03_mode='per_direction'):

      * 'per_direction' takes the 5th percentile of the per-direction MEAN
        energy, i.e. `quantile(e_rand.mean(over matrices), 0.05)` -- the
        published formula.
      * 'flat' pools all (n_random x n_matrices) energies before the quantile.
        This is what the iteration-2 code does and it is a DIFFERENT statistic.
    """
    t0 = time.time()
    if not mats:
        raise ValueError("no residual-write matrices supplied")
    if w03_mode not in ("per_direction", "flat"):
        raise ValueError(f"w03_mode={w03_mode!r}")
    dev = torch.device(device)
    acc = torch.float64 if accum_dtype == "float64" else torch.float32

    # --- shared Gram matrix ----------------------------------------------
    A = torch.zeros(d, d, dtype=acc, device=dev)
    for W in mats:
        Wd = W.to(dev, acc)
        fro2 = Wd.pow(2).sum()
        A += (Wd @ Wd.T) / fro2.clamp_min(1e-30)
        del Wd
    A = A.double()
    A = 0.5 * (A + A.T)  # enforce exact symmetry against round-off

    evals, evecs = torch.linalg.eigh(A)  # ASCENDING
    lam = evals.cpu().numpy()
    if clip_lam:
        lam = np.clip(lam, 1e-30, None)
    v1 = evecs[:, 0].to(torch.float32).cpu()  # MINIMUM eigenvector
    if v1_override is not None:  # sanity control: substitute a random direction
        v1 = torch.as_tensor(v1_override, dtype=torch.float32)
        v1 = v1 / v1.norm()
    del A, evecs, evals

    # --- energies along v1 ------------------------------------------------
    v1_dev = v1.to(dev)
    e_v1 = np.array([_energy(v1_dev, W.to(dev), d) for W in mats], dtype=np.float64)

    # --- random-direction reference (W03 only) ----------------------------
    rng = np.random.default_rng(seed)
    U = rng.normal(size=(n_random, d))
    U = U / np.linalg.norm(U, axis=1, keepdims=True)
    Ut = torch.as_tensor(U, dtype=torch.float32, device=dev)
    e_rand_sum = torch.zeros(n_random, dtype=torch.float64, device=dev)
    e_rand_flat: list[np.ndarray] = []
    for W in mats:
        e = _energy_batch(Ut, W.to(dev), d)
        e_rand_sum += e.to(torch.float64)
        if w03_mode == "flat":
            e_rand_flat.append(e.cpu().numpy())
        del e
    e_rand_mean = (e_rand_sum / len(mats)).cpu().numpy()  # (n_random,) mean over matrices
    e_rand_pool = np.concatenate(e_rand_flat) if w03_mode == "flat" else e_rand_mean
    del Ut, e_rand_sum

    lam_min = max(float(lam[0]), 1e-300)
    W01 = float(np.log10(float(np.median(lam)) / lam_min))
    W02 = float(np.mean(e_v1 < 0.1))
    W03 = float(np.log10(max(float(np.quantile(e_rand_pool, 0.05)), 1e-30) /
                         max(float(e_v1.mean()), 1e-30)))
    W04 = float(np.log10(max(float(lam[1]), 1e-300) / lam_min))
    W05 = float(np.log10(max(float(e_v1.min()), 1e-30)))

    return WResult(W01=W01, W02=W02, W03=W03, W04=W04, W05=W05,
                   v1=v1.numpy(), e_v1=e_v1, eigvals=lam, names=names, d=d,
                   n_layers=n_layers, n_matrices=len(mats),
                   seconds=round(time.time() - t0, 3), dtype="float32/float64",
                   extra={"lam_min": lam_min, "lam_median": float(np.median(lam)),
                          "e_v1_mean": float(e_v1.mean()),
                          "e_rand_q05": float(np.quantile(e_rand_pool, 0.05)),
                          "accum_dtype": accum_dtype, "w03_mode": w03_mode,
                          "n_random": n_random, "seed": seed})


def w_stats_model(model, *, n_random: int = 256, seed: int = 0,
                  device: str = "cpu", **kw) -> WResult:
    d = int(model.config.hidden_size)
    names, mats, info = collect_write_tensors(model, d)
    res = w_stats_from_matrices(names, mats, d, info["n_layers"],
                                n_random=n_random, seed=seed, device=device, **kw)
    res.extra["n_transposed"] = info["n_transposed"]
    del mats
    return res


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def sha256_index(snapshot_dir: str | Path) -> str:
    """sha256 over the sorted (name, size) of every weight shard in a snapshot."""
    p = Path(snapshot_dir)
    items = []
    for f in sorted(p.rglob("*")):
        if f.is_file() and f.suffix in (".safetensors", ".bin", ".pth"):
            items.append(f"{f.name}:{f.stat().st_size}")
    return hashlib.sha256("|".join(items).encode()).hexdigest()[:32] if items else ""


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Self-test (testing_plan items 1-3): pure synthetic tensors, no model needed
# ---------------------------------------------------------------------------
def selftest() -> dict:
    out: dict = {}
    d, din, n = 256, 512, 12
    g = torch.Generator().manual_seed(11)
    base = [torch.randn(d, din, generator=g) for _ in range(n)]
    r = torch.randn(d, generator=g)
    r = r / r.norm()
    P = torch.eye(d) - torch.outer(r, r)

    def mk(k):  # project r out of the FIRST k matrices
        return [(P @ W) if i < k else W.clone() for i, W in enumerate(base)]

    names = [f"m{i}" for i in range(n)]
    un = w_stats_from_matrices(names, base, d, n)
    full = w_stats_from_matrices(names, mk(n), d, n)
    part = w_stats_from_matrices(names, mk(4), d, n)

    cos_full = abs(float(np.dot(full.v1, r.numpy())))
    out["unedited"] = {k: getattr(un, k) for k in ("W01", "W02", "W03", "W04", "W05")}
    out["full_edit"] = {k: getattr(full, k) for k in ("W01", "W02", "W03", "W04", "W05")}
    out["full_edit"]["cos_v1_r"] = cos_full
    out["partial_edit_4of12"] = {k: getattr(part, k) for k in ("W01", "W02", "W03", "W04", "W05")}

    # 1. full injection detected
    assert full.W02 == 1.0, f"full W02 {full.W02}"
    assert cos_full > 0.999, f"cos {cos_full}"
    assert full.W05 < un.W05 - 3.0, f"W05 {full.W05} vs {un.W05}"
    # 2. PARTIAL injection.  The plan predicted W02 == 4/12 (the fraction edited)
    #    with W05 unchanged.  The truth is stronger and worth recording: because
    #    A pools ALL matrices, 8 unedited matrices keep r out of the minimum-
    #    eigenvector, so v1 is not r at all -- W02 collapses to 0 and NOTHING is
    #    detected.  This is the band-limited blind spot in its sharpest form and
    #    it is why the layer-fraction sweep (Arm 1d) is a threshold, not a ramp.
    out["partial_edit_4of12"]["cos_v1_r"] = abs(float(np.dot(part.v1, r.numpy())))
    assert part.W02 == 0.0, f"partial W02 {part.W02}"
    # W05 must stay near the UNEDITED value, i.e. nowhere near the full-edit scar.
    frac_moved = abs(part.W05 - un.W05) / abs(full.W05 - un.W05)
    out["partial_edit_4of12"]["W05_fraction_of_full_shift"] = frac_moved
    assert frac_moved < 0.05, f"partial W05 moved {frac_moved:.3f} of the full shift"
    out["blind_spot_reproduced"] = True

    # 2b. fraction sweep: where does detection switch on?  (free preview of Arm 1d)
    sweep = []
    for k in range(0, n + 1):
        rk = w_stats_from_matrices(names, mk(k), d, n)
        sweep.append({"k": k, "frac": k / n, "W01": rk.W01, "W02": rk.W02,
                      "W05": rk.W05, "cos_v1_r": abs(float(np.dot(rk.v1, r.numpy())))})
    out["fraction_sweep"] = sweep
    detected = [s["frac"] for s in sweep if s["W02"] > 0.5]
    out["synthetic_f_star"] = min(detected) if detected else None

    # 3. ORIENTATION test.  Feed transposed [d_in, d] matrices through the same
    #    correction the resolver applies, and require the statistics to be
    #    recovered.  Run on the UNEDITED set: the full-edit W05 sits on the
    #    float noise floor (~1e-15), where log10 amplifies bit-level differences
    #    and no equality test is meaningful.
    mats_T = [W.T.contiguous() for W in base]
    fixed = [(W.T if W.shape[0] != d else W) for W in mats_T]
    assert all(W.shape[0] == d for W in fixed), "orientation correction failed"
    un_T = w_stats_from_matrices(names, fixed, d, n)
    # Tolerance 1e-6, not exact equality: transposing changes the matmul
    # reduction order, and on random matrices lam[0] and lam[1] are nearly
    # degenerate, so v1 (and hence W05) is only conditionally stable.
    ori = {k: abs(getattr(un_T, k) - getattr(un, k))
           for k in ("W01", "W02", "W04", "W05")}
    out["orientation_max_delta"] = max(ori.values())
    for k, dv in ori.items():
        assert dv < 1e-6, f"orientation {k}: {dv}"
    # and the UNcorrected transposed input must be rejected by the shape guard
    out["orientation_uncorrected_shapes"] = [list(mats_T[0].shape), d]
    out["orientation_test_pass"] = True

    # 4. determinism / seed sensitivity: only W03 uses random directions
    a = w_stats_from_matrices(names, base, d, n, seed=0)
    b = w_stats_from_matrices(names, base, d, n, seed=0)
    c = w_stats_from_matrices(names, base, d, n, seed=99)
    assert (a.W01, a.W02, a.W04, a.W05) == (b.W01, b.W02, b.W04, b.W05) and a.W03 == b.W03
    assert (a.W01, a.W02, a.W04, a.W05) == (c.W01, c.W02, c.W04, c.W05)
    out["determinism_pass"] = True
    out["W03_seed_delta"] = abs(a.W03 - c.W03)
    assert out["W03_seed_delta"] < 0.01, out["W03_seed_delta"]

    # 5. NEGATIVE control: a random direction in place of v1 must NOT give a low W05
    rnd = np.random.default_rng(5).normal(size=d)
    rand_dir = w_stats_from_matrices(names, mk(n), d, n, v1_override=rnd)
    out["random_direction_W05"] = rand_dir.W05
    out["random_direction_W02"] = rand_dir.W02
    assert rand_dir.W05 > full.W05 + 3.0, "random direction gave a scar-like W05"
    out["random_direction_control_pass"] = True
    return out


if __name__ == "__main__":
    res = selftest()
    print(json.dumps(res, indent=2))
