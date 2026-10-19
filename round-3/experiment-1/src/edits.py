#!/usr/bin/env python3
"""In-house synthetic abliteration recipes (Arm 1, synthetic half).

Every recipe edits ONLY residual-write matrices (attention output projection and
MLP down projection), the same set the W01-W05 statistics read, so a miss is a
property of the statistic and not of where the surgery landed.

Recipes
  plain      : W <- (I - r r^T) W                 -- the huihui/global reference class
  normpres   : plain, then W *= ||W||_F / ||W'||_F   -- norm-preserving projection
  rank_k     : W <- (I - R_k R_k^T) W, R_k = top-k right singular subspace of the
               (harmful - benign) activation difference matrix
  per_head   : project r out of the top-25% attention heads by write energy along
               r, in o_proj only; down_proj untouched
  band(f)    : plain projection restricted to a contiguous mid-stack band covering
               a fraction f of the layers  -- the layer-fraction sweep

The store keeps a CPU float32 copy of every original write matrix so a variant
can be applied, measured, and exactly reverted without reloading the model.
"""

from __future__ import annotations

import numpy as np
import torch
from loguru import logger

from wstats import collect_write_tensors, find_block_list, resolve_write_matrices, w_stats_from_matrices


class WriteMatrixStore:
    """Original residual-write matrices, with apply/revert."""

    def __init__(self, model):
        self.model = model
        self.d = int(model.config.hidden_size)
        self.blocks = find_block_list(model)
        self.L = len(self.blocks)
        self.entries: list[dict] = []
        for li, blk in enumerate(self.blocks):
            for nm, mod in resolve_write_matrices(blk, self.d):
                self.entries.append({"layer": li, "name": nm, "mod": mod,
                                     "kind": nm.split(":")[0],
                                     "orig": mod.weight.detach().to("cpu", torch.float32).clone()})
        if not self.entries:
            raise RuntimeError("no residual-write matrices to edit")
        logger.info(f"edit store: {len(self.entries)} matrices over {self.L} layers")

    def revert(self) -> None:
        for e in self.entries:
            with torch.no_grad():
                e["mod"].weight.copy_(e["orig"].to(e["mod"].weight.device,
                                                   e["mod"].weight.dtype))

    def band(self, f: float) -> tuple[int, int]:
        """Contiguous mid-stack band covering fraction f of the layers."""
        n = int(round(f * self.L))
        n = max(0, min(self.L, n))
        lo = (self.L - n) // 2
        return lo, lo + n

    # -- recipes ----------------------------------------------------------
    @torch.no_grad()
    def apply(self, recipe: str, *, r: torch.Tensor | None = None,
              Rk: torch.Tensor | None = None, f: float = 1.0,
              head_frac: float = 0.25, n_heads: int | None = None,
              device: str = "cuda") -> dict:
        """Apply a recipe in place.  Returns an audit dict."""
        self.revert()
        d = self.d
        dev = torch.device(device if (device == "cuda" and torch.cuda.is_available()) else "cpu")
        lo, hi = self.band(f)
        touched, layers_touched, heads_touched = 0, set(), 0
        fro_before, fro_after = 0.0, 0.0

        if recipe in ("plain", "normpres", "band", "per_head"):
            assert r is not None
            r = r.to(torch.float32).cpu()
            r = r / r.norm()
            P = (torch.eye(d, dtype=torch.float32) - torch.outer(r, r)).to(dev)
        elif recipe == "rank_k":
            assert Rk is not None
            Rk = Rk.to(torch.float32).cpu()
            P = (torch.eye(d, dtype=torch.float32) - Rk @ Rk.T).to(dev)
        else:
            raise ValueError(recipe)
        r_dev = r.to(dev) if r is not None else None

        for e in self.entries:
            if not (lo <= e["layer"] < hi):
                continue
            W0 = e["orig"].to(dev)
            if recipe == "per_head":
                if e["kind"] != "attn":
                    continue  # down_proj deliberately untouched
                nh = n_heads or 1
                dh = W0.shape[1] // nh
                if dh * nh != W0.shape[1]:
                    continue
                energies = np.array([float((r_dev @ W0[:, h * dh:(h + 1) * dh]).pow(2).sum())
                                     for h in range(nh)])
                k = max(1, int(round(head_frac * nh)))
                top = np.argsort(-energies)[:k]
                Wn = W0.clone()
                for h in top:
                    Wn[:, h * dh:(h + 1) * dh] = P @ W0[:, h * dh:(h + 1) * dh]
                heads_touched += k
            else:
                Wn = P @ W0
                if recipe == "normpres":
                    n0, n1 = W0.norm(), Wn.norm()
                    if float(n1) > 0:
                        Wn = Wn * (n0 / n1)
            fro_before += float(W0.pow(2).sum())
            fro_after += float(Wn.pow(2).sum())
            e["mod"].weight.copy_(Wn.to(e["mod"].weight.device, e["mod"].weight.dtype))
            touched += 1
            layers_touched.add(e["layer"])
            del Wn, W0

        return {"recipe": recipe, "f": f, "band_layers": [lo, hi],
                "n_matrices_edited": touched, "n_layers_edited": len(layers_touched),
                "n_heads_edited": heads_touched,
                "frobenius_ratio": (fro_after / fro_before) if fro_before else float("nan"),
                "rank_removed": (1 if recipe != "rank_k" else int(Rk.shape[1]))}


# ---------------------------------------------------------------------------
# Refusal direction / subspace from the FROZEN layer_contrast fold
# ---------------------------------------------------------------------------
def refusal_direction(hs_fit: torch.Tensor, n_harmful: int, layer_index: int
                      ) -> tuple[torch.Tensor, torch.Tensor]:
    """(r, D) at a given layer.  `hs_fit` is (n, L+1, d); hidden_states[l+1] is
    the output of block l, so layer l is index l+1."""
    li = layer_index + 1
    H = hs_fit[:n_harmful, li].float()
    B = hs_fit[n_harmful:, li].float()
    mu = H.mean(0) - B.mean(0)
    r = mu / mu.norm().clamp_min(1e-12)
    n = min(H.shape[0], B.shape[0])
    D = H[:n] - B[:n]            # paired harmful-minus-benign difference matrix
    return r, D


def rank_k_subspace(D: torch.Tensor, k: int) -> torch.Tensor:
    """Top-k RIGHT singular subspace of the difference matrix D (n, d) -> (d, k)."""
    Dc = D.float()
    _U, _S, Vh = torch.linalg.svd(Dc, full_matrices=False)
    Rk = Vh[:k].T.contiguous()               # (d, k), orthonormal columns
    q, _ = torch.linalg.qr(Rk)               # re-orthonormalise against round-off
    return q[:, :k]


def measure_edited(store: WriteMatrixStore, *, n_random: int = 256, seed: int = 0,
                   device: str = "cpu"):
    """W01-W05 on the CURRENTLY applied edit."""
    names, mats, info = collect_write_tensors(store.model, store.d)
    return w_stats_from_matrices(names, mats, store.d, info["n_layers"],
                                 n_random=n_random, seed=seed, device=device)


def selftest() -> dict:
    """Recipe machinery on random tensors: the plain global projection at f=1.0
    must produce the scar; band f<1 must not."""
    d, din, L = 64, 96, 8

    class _Fake(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.layers = torch.nn.ModuleList()
            for _ in range(L):
                blk = torch.nn.Module()
                blk.self_attn = torch.nn.Module()
                blk.self_attn.o_proj = torch.nn.Linear(din, d, bias=False)
                blk.mlp = torch.nn.Module()
                blk.mlp.down_proj = torch.nn.Linear(din, d, bias=False)
                self.layers.append(blk)

    class _Cfg:
        hidden_size, num_hidden_layers = d, L

    m = _Fake()
    m.config = _Cfg()
    st = WriteMatrixStore(m)
    r = torch.randn(d)
    r = r / r.norm()
    base = measure_edited(st)
    st.apply("plain", r=r, f=1.0)
    full = measure_edited(st)
    st.apply("plain", r=r, f=0.5)
    half = measure_edited(st)
    st.apply("normpres", r=r, f=1.0)
    npv = measure_edited(st)
    st.revert()
    back = measure_edited(st)
    assert full.W02 == 1.0 and full.W05 < base.W05 - 5, (full.W02, full.W05, base.W05)
    assert half.W02 < 1.0, half.W02
    assert npv.W02 == 1.0, npv.W02
    assert abs(back.W05 - base.W05) < 1e-6, "revert failed"
    return {"base_W05": base.W05, "plain_f1_W05": full.W05, "plain_f1_W02": full.W02,
            "plain_f05_W02": half.W02, "normpres_W02": npv.W02, "revert_exact": True}


if __name__ == "__main__":
    import json
    print(json.dumps(selftest(), indent=2))
