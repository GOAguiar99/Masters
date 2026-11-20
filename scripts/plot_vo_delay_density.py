"""Voice delay probability density (KDE on log10 delay), heavy density, high load.
Top: uniform load (netload_high). Bottom: hotspot (hotspot_high). Three seeds pooled.
usage: plot_vo_density.py vo_delays.npz OUT_STEM
"""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, NullFormatter
from scipy.stats import gaussian_kde

d = np.load(sys.argv[1])
out = sys.argv[2]

# Same colour + dash per policy as the existing Evaluation figures (fig_06 etc.).
POLICIES = [
    ("plain", "DCF", "#b279a2", (0, (9, 4, 2, 4))),
    ("edca_only", "EDCA", "#4c78a8", "solid"),
    ("edca_v2x_vo_stable", "Stable", "#e45756", (0, (2, 2))),
    ("edca_v2x_vo_guarded", "Guarded", "#54a24b", (0, (3, 3))),
    ("edca_v2x_vo_emergency", "Emergency", "#f58518", (0, (7, 3))),
]
PANELS = [
    ("netload_high", "(a) Uniform load (netload_high)"),
    ("hotspot_high", "(b) Hotspot load (hotspot_high)"),
]
BW = 0.04  # KDE bandwidth in decades of delay
grid = np.linspace(np.log10(0.2), np.log10(50), 800)

INK, MUTED, GRID = "#111827", "#6b7280", "#e5e7eb"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK})

fig, axes = plt.subplots(2, 1, figsize=(6.8, 5.6), sharex=True)
for ax, (camp, title) in zip(axes, PANELS):
    for key, label, color, dash in POLICIES:
        v = np.concatenate([d[f"highway_heavy/{key}_{camp}-#{s}"] for s in range(3)]) * 1e3
        lv = np.log10(v)
        kde = gaussian_kde(lv, bw_method=BW / lv.std(ddof=1))
        ax.plot(10 ** grid, kde(grid), color=color, linestyle=dash, lw=1.6, label=label)
        p95 = np.percentile(v, 95)
        print(f"{camp:14s} {label:10s} n={v.size} median={np.median(v):.3f} p95={p95:.3f} ms")
    ax.set_xscale("log")
    ax.set_title(title, loc="left", fontsize=10)
    ax.set_ylabel("Density (per decade)")
    ax.set_ylim(bottom=0)
    ax.grid(True, which="major", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

ticks = [0.25, 0.5, 1, 2, 5, 10, 20, 50]
axes[-1].xaxis.set_major_locator(FixedLocator(ticks))
axes[-1].set_xticklabels([f"{t:g}" for t in ticks])
axes[-1].xaxis.set_minor_formatter(NullFormatter())
axes[-1].set_xlim(0.2, 50)
axes[-1].set_xlabel("VO delay (ms, log scale)")
axes[0].legend(ncol=5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.32),
               handlelength=2.6, fontsize=9)
fig.tight_layout()
for ext in ("pdf", "svg", "png"):
    fig.savefig(f"{out}.{ext}", dpi=200 if ext == "png" else None)
