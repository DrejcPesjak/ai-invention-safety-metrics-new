#!/usr/bin/env python3
"""Abliteration construction and the five laundering treatments.

The edit primitive is iteration 2's positive control verbatim --
    W <- W - outer(r, r @ W)
over every residual-write matrix (per-layer attention-out + MLP-down) -- with the
ONLY change being that `r` is a real diff-in-means refusal direction rather than a
random one.
"""

from __future__ import annotations

import gc

import numpy as np
import torch
from loguru import logger

from lib_score import auroc

EPS = 1e-12


# ==========================================================================
# state-dict plumbing
# ==========================================================================
def write_matrix_keys(rn) -> list[dict]:
    """Full state_dict keys of the residual-write matrices, with layer + kind."""
    mod2name = {id(m): n for n, m in rn.model.named_modules()}
    out = []
    for l in range(rn.L):
        for tag, mod in rn.write_matrices(l):
            full = mod2name.get(id(mod))
            if full is None:
                raise RuntimeError(f"could not resolve full name for {tag} at layer {l}")
            out.append({"layer": l, "kind": tag.split(":")[0], "key": f"{full}.weight"})
    return out


def embed_key(rn) -> str | None:
    emb = rn.model.get_input_embeddings()
    for n, m in rn.model.named_modules():
        if m is emb:
            return f"{n}.weight"
    return None


def snapshot_sd(rn) -> dict[str, torch.Tensor]:
    """CPU copy of every parameter (bf16), for merging / restoring."""
    return {k: v.detach().to("cpu").clone() for k, v in rn.model.state_dict().items()}


@torch.no_grad()
def load_sd(rn, sd: dict[str, torch.Tensor]) -> None:
    live = rn.model.state_dict()
    n = 0
    for k, v in sd.items():
        if k in live:
            live[k].copy_(v.to(live[k].device, live[k].dtype))
            n += 1
    assert n == len(sd), f"loaded {n}/{len(sd)} tensors"
    rn._write_cache.clear()
    torch.cuda.empty_cache()


# ==========================================================================
# refusal direction (faithful diff-in-means, Arditi-style)
# ==========================================================================
@torch.no_grad()
def refusal_direction(rn, harmful: list[str], benign: list[str], seed: int = 20260813) -> dict:
    """Per-layer diff-in-means at the last prompt token, layer chosen by held-out AUROC."""
    n = min(len(harmful), len(benign))
    harmful, benign = harmful[:n], benign[:n]
    # deterministic 50/50 fit/score split by index parity of a stable hash
    import hashlib
    def half(t):
        return int(hashlib.sha256(t.encode()).hexdigest(), 16) % 2
    hA = [t for t in harmful if half(t) == 0]
    hB = [t for t in harmful if half(t) == 1]
    bA = [t for t in benign if half(t) == 0]
    bB = [t for t in benign if half(t) == 1]
    if min(len(hA), len(hB), len(bA), len(bB)) < 8:  # degenerate hash split -> index split
        hA, hB = harmful[::2], harmful[1::2]
        bA, bB = benign[::2], benign[1::2]

    HA, _ = rn.last_token_states(hA, batch=8)
    BA, _ = rn.last_token_states(bA, batch=8)
    HB, _ = rn.last_token_states(hB, batch=8)
    BB, _ = rn.last_token_states(bB, batch=8)

    L = rn.L
    dirs, aurocs, ds = [], [], []
    for l in range(L + 1):
        mu = HA[:, l].mean(0) - BA[:, l].mean(0)
        u = mu / (mu.norm() + EPS)
        dirs.append(u)
        ph = (HB[:, l] @ u).numpy()
        pb = (BB[:, l] @ u).numpy()
        aurocs.append(auroc(ph, pb))
        sp = float(np.sqrt((ph.var(ddof=1) + pb.var(ddof=1)) / 2.0))
        ds.append(float((ph.mean() - pb.mean()) / (sp + EPS)))
    aurocs, ds = np.array(aurocs), np.array(ds)
    best = float(np.nanmax(aurocs))
    cands = np.where(np.abs(aurocs - best) < 1e-9)[0]
    l_star = int(cands[int(np.argmax(ds[cands]))])          # tie-break on Cohen's d
    del HA, BA, HB, BB
    gc.collect()
    return {"r": dirs[l_star].clone(), "l_star": l_star, "rel_depth": l_star / L,
            "heldout_auroc": float(aurocs[l_star]), "heldout_dprime": float(ds[l_star]),
            "auroc_profile": [float(x) for x in aurocs],
            "dprime_profile": [float(x) for x in ds],
            "n_fit": len(hA) + len(bA), "n_hold": len(hB) + len(bB)}


# ==========================================================================
# the edit primitive
# ==========================================================================
@torch.no_grad()
def ablate_sd(sd: dict[str, torch.Tensor], keys: list[str], r: torch.Tensor,
              emb_key: str | None = None) -> dict[str, torch.Tensor]:
    """W <- W - outer(r, r@W) on every key; optionally project embedding rows too."""
    out = dict(sd)
    rf = r.to(torch.float32)
    rf = rf / rf.norm()
    for k in keys:
        W = sd[k].to(torch.float32)
        out[k] = (W - torch.outer(rf, rf @ W)).to(sd[k].dtype)
        del W
    if emb_key is not None:
        E = sd[emb_key]                             # (V, d) -- 1.2 GB in float32
        o = torch.empty_like(E)
        for a, b in _row_chunks(E):
            blk = E[a:b].to(torch.float32)
            o[a:b] = (blk - torch.outer(blk @ rf, rf)).to(E.dtype)
            del blk
        out[emb_key] = o
    return out


# ==========================================================================
# (b) linear merge with the parent
# ==========================================================================
CHUNK_ELEMS = 16 * 1024 ** 2      # ~64 MB of float32 per temporary


def _row_chunks(t: torch.Tensor):
    """Slice indices along dim 0 so each block holds <= CHUNK_ELEMS elements."""
    assert t.dim() >= 1, "0-dim tensors must be handled by the caller"
    if t.numel() <= CHUNK_ELEMS:
        yield 0, t.shape[0]
        return
    per_row = max(t.numel() // t.shape[0], 1)
    step = max(int(CHUNK_ELEMS // per_row), 1)
    for i in range(0, t.shape[0], step):
        yield i, min(i + step, t.shape[0])


@torch.no_grad()
def merge_sd(root: dict, parent: dict, w: float) -> dict:
    """(1-w)*root + w*parent, EVERY parameter tensor. Block-wise: a whole-tensor
    float32 copy of a 151669x2048 embedding is 1.2 GB and OOMs the container."""
    out = {}
    for k, v in root.items():
        p = parent.get(k)
        if p is None or p.shape != v.shape or not v.is_floating_point():
            out[k] = v.clone()
            continue
        if v.dim() == 0:
            out[k] = ((1.0 - w) * v.float() + w * p.float()).to(v.dtype)
            continue
        o = torch.empty_like(v)
        for a, b in _row_chunks(v):
            o[a:b] = ((1.0 - w) * v[a:b].to(torch.float32)
                      + w * p[a:b].to(torch.float32)).to(v.dtype)
        out[k] = o
    return out


# ==========================================================================
# (c) quantization round-trip (fake-quant: quantize then dequantize to bf16)
# ==========================================================================
@torch.no_grad()
def quant_sd(sd: dict, mode: str, min_elems: int = 1024) -> tuple[dict, dict]:
    out, skipped, touched, errs = {}, [], 0, []
    for k, v in sd.items():
        if v.dim() != 2 or v.numel() < min_elems or not v.is_floating_point():
            out[k] = v.clone()
            if v.dim() == 2 and v.numel() >= min_elems:
                skipped.append(k)
            continue
        if mode == "int4" and v.shape[1] % 128 != 0:
            skipped.append(k)
            out[k] = v.clone()
            continue
        o = torch.empty_like(v)
        num2, den2 = 0.0, 0.0
        for a, b in _row_chunks(v):
            W = v[a:b].to(torch.float32)
            if mode == "int8":
                s = W.abs().amax(dim=1, keepdim=True).clamp_min(1e-12) / 127.0
                Q = torch.round(W / s).clamp(-127, 127) * s
            elif mode == "int4":
                G = W.reshape(W.shape[0], -1, 128)
                s = G.abs().amax(dim=2, keepdim=True).clamp_min(1e-12) / 7.0
                Q = (torch.round(G / s).clamp(-7, 7) * s).reshape(W.shape)
            elif mode == "nf4":
                Q = _nf4_roundtrip(W)
            else:
                raise ValueError(mode)
            num2 += float(((Q - W) ** 2).sum())
            den2 += float((W ** 2).sum())
            o[a:b] = Q.to(v.dtype)
            del W, Q
        errs.append(float(np.sqrt(num2) / (np.sqrt(den2) + EPS)))
        out[k] = o
        touched += 1
    return out, {"mode": mode, "n_quantized": touched, "n_skipped_2d": len(skipped),
                 "skipped_examples": skipped[:8],
                 "rel_frobenius_error_mean": float(np.mean(errs)) if errs else float("nan"),
                 "rel_frobenius_error_max": float(np.max(errs)) if errs else float("nan")}


_NF4 = torch.tensor([
    -1.0, -0.6961928009986877, -0.5250730514526367, -0.39491748809814453,
    -0.28444138169288635, -0.18477343022823334, -0.09105003625154495, 0.0,
    0.07958029955625534, 0.16093020141124725, 0.24611230194568634, 0.33791524171829224,
    0.44070982933044434, 0.5626170039176941, 0.7229568362236023, 1.0], dtype=torch.float32)


@torch.no_grad()
def _nf4_roundtrip(W: torch.Tensor, gsz: int = 64) -> torch.Tensor:
    """bitsandbytes-style NF4: blockwise absmax scaling onto the 16 NF4 levels.

    The nearest-level search materialises a (blocks, gsz, 16) tensor, so it is done
    in sub-blocks: done naively on an embedding it is a 16x memory blow-up.
    """
    flat = W.reshape(-1)
    pad = (-flat.numel()) % gsz
    if pad:
        flat = torch.cat([flat, torch.zeros(pad, dtype=flat.dtype, device=flat.device)])
    G = flat.reshape(-1, gsz)
    lv = _NF4.to(W.device, W.dtype)
    out = torch.empty_like(G)
    step = max(int(CHUNK_ELEMS // (gsz * 16)), 1)
    for i in range(0, G.shape[0], step):
        blk = G[i:i + step]
        s = blk.abs().amax(dim=1, keepdim=True).clamp_min(1e-12)
        idx = (blk.div(s).unsqueeze(-1) - lv.view(1, 1, -1)).abs().argmin(dim=-1)
        out[i:i + step] = lv[idx] * s
    Q = out.reshape(-1)
    if pad:
        Q = Q[:-pad]
    return Q.reshape(W.shape)


# ==========================================================================
# (d) metric-aware rank-one add-back adversary
# ==========================================================================
@torch.no_grad()
def addback_sd(root: dict, parent: dict, keys: list[str], u: torch.Tensor,
               eps: float) -> dict:
    """W <- W + eps * outer(u, u @ W_parent) on the listed keys."""
    out = dict(root)
    uf = u.to(torch.float32)
    uf = uf / uf.norm()
    for k in keys:
        p, r0 = parent[k], root[k]
        c = torch.zeros(p.shape[1], dtype=torch.float32)
        for a, b in _row_chunks(p):
            c += uf[a:b] @ p[a:b].to(torch.float32)
        o = torch.empty_like(r0)
        for a, b in _row_chunks(r0):
            o[a:b] = (r0[a:b].to(torch.float32)
                      + eps * torch.outer(uf[a:b], c)).to(r0.dtype)
        out[k] = o
        del c
    return out


# ==========================================================================
# (a) LoRA-SFT on benign instruction data
# ==========================================================================
def lora_sft(rn, sd_start: dict, texts: list[str], step_marks: list[int], out_dir,
             seed: int = 20260813, lr: float = 1e-4, bs: int = 4, accum: int = 2,
             max_len: int = 512, rank: int = 16, alpha: int = 32) -> dict:
    """Train a LoRA adapter on the ROOT weights; write merged state_dicts per mark.

    Returns {"marks": {steps: path}, "meta": {...}}. The adapter is merged into the
    base weights before each snapshot so every stage is measured on plain weights.
    Snapshots go to disk (not RAM): four 1.7B bf16 copies would be ~14 GB.
    """
    from pathlib import Path as _P
    out_dir = _P(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    import math as _m

    from peft import LoraConfig, get_peft_model

    torch.manual_seed(seed)
    load_sd(rn, sd_start)
    model = rn.model
    cfg = LoraConfig(r=rank, lora_alpha=alpha, lora_dropout=0.0, bias="none",
                     task_type="CAUSAL_LM",
                     target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                                     "gate_proj", "up_proj", "down_proj"])
    model.requires_grad_(False)
    model.config.use_cache = False
    peft_model = get_peft_model(model, cfg)
    peft_model.train()
    peft_model.enable_input_require_grads()
    peft_model.gradient_checkpointing_enable()
    params = [p for p in peft_model.parameters() if p.requires_grad]
    n_train = sum(p.numel() for p in params)
    for p in params:
        p.data = p.data.to(torch.float32)
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.0)
    total = max(step_marks)
    warmup = 10

    def lr_at(s):
        if s < warmup:
            return (s + 1) / warmup
        prog = (s - warmup) / max(total - warmup, 1)
        return 0.5 * (1 + _m.cos(_m.pi * min(prog, 1.0)))

    rng = np.random.default_rng(seed)
    order = rng.permutation(len(texts))
    ptr = 0
    marks_out: dict[int, str] = {}
    losses: list[float] = []
    tok = rn.tok
    tok.padding_side = "right"
    n_tokens_seen = 0
    try:
        for step in range(total):
            for gset in opt.param_groups:
                gset["lr"] = lr * lr_at(step)
            opt.zero_grad(set_to_none=True)
            step_loss = 0.0
            for _ in range(accum):
                idx = [order[(ptr + i) % len(texts)] for i in range(bs)]
                ptr += bs
                batch = [texts[i] for i in idx]
                enc = tok(batch, return_tensors="pt", padding=True, truncation=True,
                          max_length=max_len, add_special_tokens=True)
                enc = {k: v.to(rn.device) for k, v in enc.items()}
                labels = enc["input_ids"].clone()
                labels[enc["attention_mask"] == 0] = -100
                out = peft_model(**enc, labels=labels, use_cache=False)
                (out.loss / accum).backward()
                step_loss += float(out.loss) / accum
                n_tokens_seen += int(enc["attention_mask"].sum())
                del out, enc, labels
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            opt.step()
            losses.append(step_loss)
            if (step + 1) in step_marks:
                peft_model.eval()
                base = _merged_cpu_sd(peft_model)
                p = out_dir / f"lora_step{step + 1}.pt"
                torch.save(base, p)
                marks_out[step + 1] = str(p)
                del base
                gc.collect()
                peft_model.train()
                logger.info(f"  lora step {step + 1}/{total} loss={step_loss:.4f}")
    finally:
        tok.padding_side = "left"
        peft_model.gradient_checkpointing_disable()
        rn.model = peft_model.unload()          # strip adapter, restore plain module
        rn.model.eval().requires_grad_(False)
        rn.model.config.use_cache = True
        from lib_model import find_block_list
        rn.blocks = find_block_list(rn.model)
        rn._write_cache.clear()
        del peft_model, opt, params
        gc.collect()
        torch.cuda.empty_cache()
    return {"marks": marks_out,
            "meta": {"rank": rank, "alpha": alpha, "lr": lr, "batch": bs, "accum": accum,
                     "max_len": max_len, "n_trainable_params": int(n_train),
                     "steps": total, "tokens_seen": int(n_tokens_seen),
                     "loss_first": losses[0] if losses else None,
                     "loss_last": losses[-1] if losses else None,
                     "loss_curve": [round(x, 4) for x in losses],
                     "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj",
                                        "gate_proj", "up_proj", "down_proj"],
                     "data": "yahma/alpaca-cleaned (CC-BY-NC-4.0, research use)"}}


@torch.no_grad()
def _merged_cpu_sd(peft_model) -> dict[str, torch.Tensor]:
    """Merge the adapter, snapshot the base weights on CPU, then unmerge."""
    peft_model.merge_adapter()
    base = peft_model.get_base_model()
    sd = {}
    for k, v in base.state_dict().items():
        kk = k.replace("base_model.model.", "")
        kk = kk.replace(".base_layer.weight", ".weight")
        if "lora_" in kk:
            continue
        sd[kk] = v.detach().to("cpu", torch.bfloat16).clone()
    peft_model.unmerge_adapter()
    return sd
