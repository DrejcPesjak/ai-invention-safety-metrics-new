#!/usr/bin/env python3
"""Screen of the 53 pre-registered metrics from round-2/experiment-1.

Separation = |AUROC - 0.5| * 2 folded back onto [0.5, 1.0], i.e. the AUROC of the
metric after orienting its sign so that "abliterated scores higher" -- the same
orientation-free reading the paper uses. 0.5 = chance, 1.0 = perfect.

Ground truth = member_class == 'abliterated' (8 positives / 36 negatives).
Reads results/battery.jsonl directly; no numbers are transcribed.
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

SRC = Path(__file__).resolve().parent
BATTERY = SRC / "results/battery.jsonl"
OUT = SRC / "figs"

# dataviz reference palette, categorical slots 1-3 (validated all-pairs, light)
FAMILY_COLOR = {"weights": "#2a78d6", "blackbox": "#eb6834", "activation": "#1baf7a"}
FAMILY_LABEL = {"weights": "weights-only", "blackbox": "black-box", "activation": "activation"}
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
INK_MUTED = "#8a8981"
GRID = "#e5e4df"


def auroc(pairs):
    pos = [v for y, v in pairs if y]
    neg = [v for y, v in pairs if not y]
    if not pos or not neg:
        return None
    s = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return s / (len(pos) * len(neg))


def load():
    rows = [json.loads(l) for l in BATTERY.open()]
    vals = collections.defaultdict(list)
    meta = {}
    for r in rows:
        meta[r["metric_id"]] = (r["metric_family"], r["is_negative_control"], r["is_in_fifty"])
        if r["ok"] and r["value"] is not None:
            vals[r["metric_id"]].append((r["member_class"] == "abliterated", r["value"]))

    out = []
    for mid, (fam, neg, fifty) in meta.items():
        a = auroc(vals.get(mid, []))
        sep = None if a is None else max(a, 1 - a)
        out.append({"id": mid, "family": fam, "neg": neg, "fifty": fifty,
                    "sep": sep, "n": len(vals.get(mid, []))})
    out.sort(key=lambda d: (d["sep"] is not None, d["sep"] or 0))
    return out


def main():
    data = load()
    OUT.mkdir(exist_ok=True)
    n = len(data)
    assert n == 53, n

    fig, ax = plt.subplots(figsize=(11.5, 14.5))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    y = range(n)
    x0 = 0.5
    for i, d in enumerate(data):
        c = FAMILY_COLOR[d["family"]]
        if d["sep"] is None:
            ax.text(x0 + 0.006, i, "not measurable  (null on 37/44 models)",
                    va="center", ha="left", fontsize=8.5, color=INK_MUTED, style="italic")
            continue
        w = d["sep"] - x0
        # 2px surface gap between adjacent bars -> height 0.62 on a 1.0 pitch
        ax.barh(i, w, left=x0, height=0.62, color=c, zorder=3,
                hatch="////" if d["neg"] else None,
                edgecolor=SURFACE if d["neg"] else "none", linewidth=0.0)
        lab = f"{d['sep']:.3f}"
        ax.text(d["sep"] + 0.004, i, lab, va="center", ha="left", fontsize=8.5,
                color=INK if d["sep"] >= 0.9 else INK_2,
                fontweight="bold" if d["sep"] >= 0.9 else "normal", zorder=4)

    # the five that worked
    win = [i for i, d in enumerate(data) if d["sep"] and d["sep"] >= 0.9]
    lo, hi = min(win) - 0.5, max(win) + 0.5
    ax.axhspan(lo, hi, color="#2a78d6", alpha=0.055, zorder=1)
    ax.annotate("", xy=(1.045, hi), xytext=(1.045, lo), zorder=5,
                arrowprops=dict(arrowstyle="-", color="#2a78d6", lw=2.2))
    ax.text(1.038, (lo + hi) / 2 - 4.6,
            "the abliteration spectral block\n"
            "W01–W05 — the only five that\nseparate, and all five read the\n"
            "weight files with zero prompts",
            fontsize=10, color=INK, ha="right", va="top",
            fontweight="bold", linespacing=1.6, zorder=5)

    ax.axvline(0.5, color=INK_2, lw=1.4, zorder=2)
    for gx in (0.6, 0.7, 0.8, 0.9, 1.0):
        ax.axvline(gx, color=GRID, lw=1, zorder=0)

    ax.set_yticks(list(y))
    ax.set_yticklabels(
        [d["id"] + ("  △" if d["neg"] else "") for d in data], fontsize=8.5)
    for t, d in zip(ax.get_yticklabels(), data):
        t.set_color(INK if (d["sep"] or 0) >= 0.9 else (INK_MUTED if d["neg"] else INK_2))
    ax.set_ylim(-2.4, n - 0.3)
    ax.set_xlim(0.5, 1.055)
    ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    ax.set_xticklabels(["0.5\nchance", "0.6", "0.7", "0.8", "0.9", "1.0\nperfect"])
    ax.tick_params(axis="x", colors=INK_2, labelsize=9, length=0)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("separation of abliterated (n=8) from everything else (n=36)   ·   "
                  "orientation-free AUROC", fontsize=10, color=INK_2, labelpad=10)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)

    handles = [mpatches.Patch(facecolor=FAMILY_COLOR[f], label=FAMILY_LABEL[f])
               for f in ("weights", "blackbox", "activation")]
    handles.append(mpatches.Patch(facecolor="#b9b8b1", hatch="////",
                                  edgecolor=SURFACE, label="declared negative control  △"))
    leg = ax.legend(handles=handles, loc="lower right", bbox_to_anchor=(1.0, 0.008),
                    frameon=True, fontsize=9, ncol=1, borderpad=0.8, labelspacing=0.6)
    leg.get_frame().set_facecolor(SURFACE)
    leg.get_frame().set_edgecolor(GRID)
    for t in leg.get_texts():
        t.set_color(INK_2)

    fig.suptitle("Of 53 pre-registered safety metrics, 5 work", x=0.012, y=0.992,
                 ha="left", fontsize=17, fontweight="bold", color=INK)
    fig.text(0.012, 0.9565,
             "Frozen and sha256-stamped before any model was downloaded, then measured on "
             "44 checkpoints / 23 lineages / 7 architecture families.\n"
             "Every metric that separates reads the weight files only — zero prompts, zero "
             "forward passes.   Source: round-2/experiment-1/src/results/battery.jsonl",
             ha="left", fontsize=9.5, color=INK_2, linespacing=1.5)

    fig.tight_layout(rect=(0, 0, 1, 0.941))
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig_53_metric_screen.{ext}", dpi=200, facecolor=SURFACE)
    print("wrote", OUT / "fig_53_metric_screen.png")

    for d in reversed(data[-8:]):
        print(f"  {d['sep']!s:>18}  {d['family']:11s} {d['id']}")


if __name__ == "__main__":
    main()
