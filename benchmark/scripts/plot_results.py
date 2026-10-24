#!/usr/bin/env python3
"""Plot completion vs. board size from results/results.csv -> images/completion_vs_complexity.png"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402,F401

HERE = Path(__file__).resolve().parent.parent
rows = [r for r in csv.DictReader(open(HERE / "results/results.csv"))
        if r["config"] == "fr25-default" and r["completion_pct"]]

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
GROUPS = [  # (label, test, colour, marker) - categorical slots 1-3, shapes as secondary encoding
    ("2 copper layers", lambda n: n == 2, "#2a78d6", "o"),
    ("4 copper layers", lambda n: n == 4, "#eb6834", "s"),
    ("6–12 copper layers", lambda n: n >= 6, "#1baf7a", "D"),
]
LABEL = {
    "kicad-pic-programmer": "PIC programmer", "kicad-stickhub": "StickHub",
    "kicad-coldfire": "ColdFire", "kicad-video": "video demo", "pocketbeagle": "PocketBeagle",
    "ulx3s": "ULX3S", "lpddr4-testbed": "LPDDR4 testbed", "butterstick": "ButterStick",
    "imx8mp-som": "iMX8MP SOM", "jetson-orin-baseboard": "Jetson Orin baseboard",
    "rdimm-ddr4-tester": "RDIMM DDR4\ntester (12L)", "strf": "STRF",
}

OFFSETS = {  # (dx, dy, ha) in points, hand-placed to avoid collisions
    "kicad-pic-programmer": (-8, 4, "right"),
    "jetson-orin-baseboard": (-8, 10, "right"),
    "rdimm-ddr4-tester": (4, 12, "left"),
}
fig, ax = plt.subplots(figsize=(9, 5.4), dpi=150)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
for name, test, colour, marker in GROUPS:
    pts = [r for r in rows if test(int(r["layers"]))]
    ax.scatter([int(r["connections_to_route"]) for r in pts], [float(r["completion_pct"]) for r in pts],
               s=70, c=colour, marker=marker, edgecolors=SURFACE, linewidths=2, label=name, zorder=3)
    for r in pts:
        if r["board"] in LABEL:
            x, y = int(r["connections_to_route"]), float(r["completion_pct"])
            dx, dy, ha = OFFSETS.get(r["board"], (6, 7, "left"))
            ax.annotate(LABEL[r["board"]], (x, y), xytext=(dx, dy), textcoords="offset points",
                        fontsize=8, color=INK2, va="center", ha=ha)

ax.set_xscale("log")
ax.set_ylim(-4, 106)
ax.set_xlim(35, 4000)
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.set_xlabel("Connections to route after stripping (log scale)", color=INK2, fontsize=10)
ax.set_ylabel("Completion after 12–15 min (%)", color=INK2, fontsize=10)
ax.set_title("Freerouting 2.5 completion falls off sharply with board size and layer count",
             color=INK, fontsize=12, loc="left", pad=12)
ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRID)
ax.tick_params(colors=INK2, labelsize=9)
leg = ax.legend(loc="lower left", frameon=False, fontsize=9)
for t in leg.get_texts():
    t.set_color(INK)
fig.tight_layout()
out = HERE / "images/completion_vs_complexity.png"
fig.savefig(out, facecolor=SURFACE)
print(out)
