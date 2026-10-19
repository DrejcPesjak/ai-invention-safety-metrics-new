#!/usr/bin/env python3
"""Model plumbing: loading, renderers, write-matrix resolution, logit lens,
batched generation with per-step hidden-state capture, steering hooks.

Re-implemented for this artifact; the iteration-1 stack was consulted as a
reference only (renderer conventions, hook direction, steering units).
"""

from __future__ import annotations

import gc
from dataclasses import dataclass

import torch
import torch.nn as nn
from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

DTYPE = torch.bfloat16
THINK_BLOCK = "<think>\n\n</think>\n\n"


# --------------------------------------------------------------------------
# Renderers
# --------------------------------------------------------------------------
def render_chatml(tok, text: str) -> str:
    try:
        s = tok.apply_chat_template([{"role": "user", "content": text}], tokenize=False,
                                    add_generation_prompt=True, enable_thinking=False)
    except TypeError:
        s = tok.apply_chat_template([{"role": "user", "content": text}], tokenize=False,
                                    add_generation_prompt=True)
    if "<think>" in str(tok.chat_template or "") and "<think>" not in s:
        s = s + THINK_BLOCK
    return s


def render_plain(text: str) -> str:
    return f"User: {text}\nAssistant:"


# --------------------------------------------------------------------------
# Structural resolvers (architecture-agnostic)
# --------------------------------------------------------------------------
ATTN_WRITE_SUFFIX = ("o_proj", "out_proj", "attention.dense", "dense", "attn.c_proj", "wo")
MLP_WRITE_SUFFIX = ("down_proj", "dense_4h_to_h", "fc2", "c_proj", "w2")


def find_block_list(model) -> nn.ModuleList:
    n = model.config.num_hidden_layers
    for _name, mod in model.named_modules():
        if isinstance(mod, nn.ModuleList) and len(mod) == n:
            return mod
    raise RuntimeError("could not locate the decoder block list")


def find_final_norm(model, d: int):
    base = getattr(model, "model", None) or getattr(model, "transformer", None) or \
        getattr(model, "gpt_neox", None) or model
    for attr in ("norm", "final_layer_norm", "ln_f", "final_layernorm"):
        m = getattr(base, attr, None)
        if m is not None and getattr(m, "weight", None) is not None and m.weight.shape[-1] == d:
            return m
    return None


def resolve_write_matrices(block, d: int) -> list[tuple[str, nn.Linear]]:
    """Linear layers inside one decoder block whose output lands in the residual."""
    out: list[tuple[str, nn.Linear]] = []
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
    if not out:  # last-resort: any Linear writing into d, deduplicated by name
        for name, mod in block.named_modules():
            if isinstance(mod, nn.Linear) and mod.out_features == d and mod.in_features != d:
                out.append((f"other:{name}", mod))
    return out


def pos_ids(mask: torch.Tensor) -> torch.Tensor:
    """Position ids under LEFT padding. Without this, HF derives positions from
    `cache_position` (a plain arange), so padded rows are shifted -- which is
    exactly what the padded-batch logits test catches."""
    return (mask.cumsum(-1) - 1).clamp_min(0)


@dataclass
class SteerState:
    direction: torch.Tensor | None = None
    alpha: float = 0.0
    scale: float = 1.0
    enabled: bool = False
    n_applied: int = 0


def make_pre_hook(state: SteerState):
    """Forward PRE-hook: shifts the INPUT of the hooked block, so a readout
    taken at that same block's output is affected (iteration-1 finding)."""

    def hook(_module, args, kwargs):
        if not state.enabled or state.direction is None or state.alpha == 0.0:
            return None
        if args:
            hs = args[0]
            delta = (state.alpha * state.scale) * state.direction.to(hs.device, hs.dtype)
            state.n_applied += 1
            return ((hs + delta,) + tuple(args[1:]), kwargs)
        hs = kwargs["hidden_states"]
        delta = (state.alpha * state.scale) * state.direction.to(hs.device, hs.dtype)
        kwargs = dict(kwargs)
        kwargs["hidden_states"] = hs + delta
        state.n_applied += 1
        return (args, kwargs)

    return hook


class Runner:
    """One resident model plus everything the battery needs from it."""

    def __init__(self, repo: str, revision: str | None, force_plain: bool = False,
                 device: str = "cuda"):
        self.repo = repo
        self.device = device
        self.tok = AutoTokenizer.from_pretrained(repo, revision=revision,
                                                 trust_remote_code=False)
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token or self.tok.unk_token
        self.tok.padding_side = "left"
        self.model = AutoModelForCausalLM.from_pretrained(
            repo, revision=revision, torch_dtype=DTYPE, attn_implementation="eager",
            trust_remote_code=False,
        ).to(device).eval().requires_grad_(False)
        cfg = self.model.config
        self.L = int(cfg.num_hidden_layers)
        self.d = int(cfg.hidden_size)
        self.blocks = find_block_list(self.model)
        self.has_chat = bool(getattr(self.tok, "chat_template", None)) and not force_plain
        self.renderer = "chatml" if self.has_chat else "plain"
        self.final_norm = find_final_norm(self.model, self.d)
        self.state = SteerState()
        self._handle = None
        self._write_cache: dict[int, list[tuple[str, nn.Linear]]] = {}
        logger.info(f"loaded {repo}: L={self.L} d={self.d} renderer={self.renderer} "
                    f"vocab={len(self.tok)}")

    # -- rendering ---------------------------------------------------------
    def render(self, text: str) -> str:
        return render_chatml(self.tok, text) if self.renderer == "chatml" else render_plain(text)

    def encode(self, texts: list[str], max_len: int = 256):
        enc = self.tok([self.render(t) for t in texts], return_tensors="pt", padding=True,
                       truncation=True, max_length=max_len, add_special_tokens=True)
        return {k: v.to(self.device) for k, v in enc.items()}

    # -- write matrices ----------------------------------------------------
    def write_matrices(self, layer: int) -> list[tuple[str, nn.Linear]]:
        if layer not in self._write_cache:
            self._write_cache[layer] = resolve_write_matrices(self.blocks[layer], self.d)
        return self._write_cache[layer]

    # -- unembedding (logit lens, RMSNorm-folded + row-mean-centred) --------
    def folded_unembed(self) -> torch.Tensor:
        head = self.model.get_output_embeddings()
        E = head.weight.detach().float()  # (V, d)
        if self.final_norm is not None and getattr(self.final_norm, "weight", None) is not None:
            w = self.final_norm.weight.detach().float()
            if w.shape[-1] == E.shape[-1]:
                gain = w + 1.0 if "gemma" in self.model.config.model_type.lower() else w
                E = E * gain.unsqueeze(0)
        return E - E.mean(dim=0, keepdim=True)

    # -- forwards ----------------------------------------------------------
    @torch.no_grad()
    def last_token_states(self, texts: list[str], batch: int = 8):
        """(n, L+1, d) float32 residual stream at the last prompt token, plus (n, V) logits."""
        hs_all, lg_all = [], []
        for i in range(0, len(texts), batch):
            enc = self.encode(texts[i:i + batch])
            out = self.model(**enc, position_ids=pos_ids(enc["attention_mask"]),
                             output_hidden_states=True, use_cache=False)
            hs = torch.stack([h[:, -1, :].float() for h in out.hidden_states], dim=1)
            hs_all.append(hs.cpu())
            lg_all.append(out.logits[:, -1, :].float().cpu())
            del out
        return torch.cat(hs_all), torch.cat(lg_all)

    @torch.no_grad()
    def generate(self, texts: list[str], max_new_tokens: int = 32, batch: int = 8,
                 capture_layer: int | None = None, temperature: float = 0.0,
                 seed: int = 0):
        """Batched manual decode. Returns (texts, n_tokens, first_ids, r_states).

        r_states: None, or a list of (steps, d) float32 tensors -- the residual
        stream at `capture_layer` (block output) for each generated step.
        """
        gen_texts: list[str] = []
        n_tok: list[int] = []
        first_ids: list[int] = []
        caps: list[torch.Tensor] = []
        eos = self.tok.eos_token_id
        eos_set = {eos} if isinstance(eos, int) else set(eos or [])
        for i in range(0, len(texts), batch):
            chunk = texts[i:i + batch]
            enc = self.encode(chunk)
            ids, mask = enc["input_ids"], enc["attention_mask"]
            b = ids.shape[0]
            gen = torch.zeros(b, 0, dtype=torch.long, device=self.device)
            done = torch.zeros(b, dtype=torch.bool, device=self.device)
            cap = torch.zeros(b, max_new_tokens, self.d, dtype=torch.float32) \
                if capture_layer is not None else None
            past = None
            cur = ids
            cur_pos = pos_ids(mask)
            g = torch.Generator(device=self.device)
            g.manual_seed(seed + i)
            for step in range(max_new_tokens):
                out = self.model(input_ids=cur, attention_mask=mask, past_key_values=past,
                                 position_ids=cur_pos, use_cache=True,
                                 output_hidden_states=capture_layer is not None)
                past = out.past_key_values
                logits = out.logits[:, -1, :].float()
                if capture_layer is not None:
                    cap[:, step, :] = out.hidden_states[capture_layer + 1][:, -1, :].float().cpu()
                if temperature > 0:
                    p = torch.softmax(logits / temperature, dim=-1)
                    nxt = torch.multinomial(p, 1, generator=g).squeeze(-1)
                else:
                    nxt = logits.argmax(dim=-1)
                if eos_set:
                    nxt = torch.where(done, torch.full_like(nxt, list(eos_set)[0]), nxt)
                gen = torch.cat([gen, nxt.unsqueeze(1)], dim=1)
                done = done | torch.tensor([int(t) in eos_set for t in nxt.tolist()],
                                           device=self.device)
                mask = torch.cat([mask, torch.ones(b, 1, dtype=mask.dtype,
                                                   device=mask.device)], dim=1)
                cur = nxt.unsqueeze(1)
                cur_pos = cur_pos[:, -1:] + 1
                del out
                if bool(done.all()):
                    if cap is not None:
                        cap = cap[:, :step + 1, :]
                    break
            for j in range(b):
                row = gen[j].tolist()
                cut = len(row)
                for k, t in enumerate(row):
                    if t in eos_set:
                        cut = k
                        break
                gen_texts.append(self.tok.decode(row[:cut], skip_special_tokens=True))
                n_tok.append(cut)
                first_ids.append(row[0] if row else -1)
                if cap is not None:
                    caps.append(cap[j])
            del past, gen
            torch.cuda.empty_cache()
        return gen_texts, n_tok, first_ids, (caps if capture_layer is not None else None)

    # -- steering ----------------------------------------------------------
    def install_pre_hook(self, layer: int):
        self.remove_hook()
        self._handle = self.blocks[layer].register_forward_pre_hook(
            make_pre_hook(self.state), with_kwargs=True)

    def remove_hook(self):
        if self._handle is not None:
            self._handle.remove()
            self._handle = None
        self.state.enabled = False
        self.state.alpha = 0.0

    def close(self):
        self.remove_hook()
        del self.model
        gc.collect()
        torch.cuda.empty_cache()
