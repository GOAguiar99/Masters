"""Slide version of the Voice alert-age density figure (pt-BR labels, deck colours, side-by-side panels).
usage: plot_vo_delay_density_slides.py vo_delays.npz OUT_STEM   (writes OUT_STEM.svg and OUT_STEM.png)
"""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, NullFormatter
from scipy.stats import gaussian_kde

d = np.load(sys.argv[1]); out = sys.argv[2]
POL = [("plain", "DCF", "#7b8494", (0, (9, 4, 2, 4))),
       ("edca_only", "EDCA", "#2f6fb3", "solid"),
       ("edca_v2x_vo_stable", "stable", "#7b4fb4", (0, (2, 2))),
       ("edca_v2x_vo_guarded", "guarded", "#1f9a95", (0, (3, 3))),
       ("edca_v2x_vo_emergency", "emergency", "#d1495b", "solid")]
PANELS = [("netload_high", "(a) Carga uniforme"), ("hotspot_high", "(b) Hotspot perto do acidente")]
grid = np.linspace(np.log10(0.2), np.log10(50), 800)
plt.rcParams.update({"font.size": 15, "font.family": "DejaVu Sans", "axes.edgecolor": "#5d6675",
                     "xtick.color": "#5d6675", "ytick.color": "#5d6675", "text.color": "#17202e",
                     "axes.labelcolor": "#17202e", "svg.fonttype": "none"})
fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.9), sharey=False)
for ax, (camp, title) in zip(axes, PANELS):
    for key, label, color, dash in POL:
        v = np.concatenate([d[f"highway_heavy/{key}_{camp}-#{s}"] for s in range(3)]) * 1e3
        lv = np.log10(v)
        kde = gaussian_kde(lv, bw_method=0.04 / lv.std(ddof=1))
        ax.plot(10 ** grid, kde(grid), color=color, linestyle=dash, lw=3.0 if key == "edca_v2x_vo_emergency" else 2.0, label=label)
        print(camp, label, "mediana=%.2f" % np.median(v))
    ax.set_xscale("log"); ax.set_title(title, loc="left", fontsize=17, fontweight="bold")
    ax.set_ylim(bottom=0); ax.set_xlim(0.2, 50)
    ax.xaxis.set_major_locator(FixedLocator([0.25, 0.5, 1, 2, 5, 10, 20, 50]))
    ax.set_xticklabels(["0,25", "0,5", "1", "2", "5", "10", "20", "50"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("idade do alerta (ms, escala log)")
    ax.grid(True, which="major", color="#e7e3da", lw=0.9); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
axes[0].set_ylabel("densidade (por década)")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, ncol=5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.0), fontsize=15, handlelength=2.4)
fig.tight_layout(rect=[0, 0, 1, 0.9])
fig.savefig(out + ".svg"); fig.savefig(out + ".png", dpi=150)
