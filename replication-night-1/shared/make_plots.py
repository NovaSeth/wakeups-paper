#!/usr/bin/env python3
"""make_plots.py — generate replication figures from results.json."""

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLOTS_DIR = ROOT / "plots"
PLOTS_DIR.mkdir(exist_ok=True)

results = json.loads((ROOT / "results.json").read_text())
cycles = sorted(int(c) for c in results["by_cycle"].keys())

# Color palette — restrained, academic
COLOR_DONE = "#4c72b0"
COLOR_NOOP = "#dd8452"
COLOR_OTHER = "#bbbbbb"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
})


# === Plot 1: Decision distribution per cycle, per condition ===
fig, (ax_w, ax_c) = plt.subplots(2, 1, figsize=(6.5, 5), sharex=True)

for ax, cond, title in [(ax_w, "wakeup_decisions", "Wakeup-loop variant (n=5)"),
                        (ax_c, "control_decisions", "Control variant (n=5)")]:
    done_counts = [results["by_cycle"][str(c)][cond].get("DONE", 0) for c in cycles]
    noop_counts = [results["by_cycle"][str(c)][cond].get("NO_OP", 0) for c in cycles]
    other = [5 - d - n for d, n in zip(done_counts, noop_counts)]

    x = np.array(cycles)
    ax.bar(x, done_counts, label="DONE", color=COLOR_DONE)
    ax.bar(x, noop_counts, bottom=done_counts, label="NO_OP", color=COLOR_NOOP)
    ax.bar(x, other, bottom=[d + n for d, n in zip(done_counts, noop_counts)],
           label="other", color=COLOR_OTHER)
    ax.set_ylim(0, 5.5)
    ax.set_yticks([0, 1, 2, 3, 4, 5])
    ax.set_ylabel("# agents")
    ax.set_title(title)
    ax.legend(loc="upper right", frameon=False, fontsize=8)

ax_c.set_xlabel("Cycle")
ax_c.set_xticks(cycles)
fig.suptitle("Decision distribution per cycle, by condition", fontsize=12, y=0.98)
fig.tight_layout()
fig.savefig(PLOTS_DIR / "fig1_decisions_per_cycle.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved {PLOTS_DIR / 'fig1_decisions_per_cycle.png'}")


# === Plot 2: NO_OP rate per condition (with cycle-by-cycle breakdown) ===
fig, ax = plt.subplots(figsize=(6, 4))

wk_rates = [results["by_cycle"][str(c)]["wakeup_no_op_rate"] for c in cycles]
ctrl_rates = [results["by_cycle"][str(c)]["control_no_op_rate"] for c in cycles]

x = np.array(cycles)
ax.plot(x, wk_rates, "-o", label="Wakeup (legal NO_OP)",
        color=COLOR_NOOP, linewidth=2, markersize=8)
ax.plot(x, ctrl_rates, "-s", label="Control (no NO_OP affordance)",
        color=COLOR_DONE, linewidth=2, markersize=8)
ax.axhline(0, color="black", linewidth=0.5)
ax.set_xticks(cycles)
ax.set_xlabel("Cycle")
ax.set_ylabel("NO_OP rate")
ax.set_ylim(-0.05, 1.05)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.set_title("NO_OP exercise rate per cycle")
ax.legend(loc="center right", frameon=False)

# Annotate the gap at cycle 3
ax.annotate("", xy=(3, 1.0), xytext=(3, 0.0),
            arrowprops=dict(arrowstyle="<->", color="gray", lw=1))
ax.text(3.15, 0.5, "100 pp", fontsize=9, color="gray", verticalalignment="center")

fig.tight_layout()
fig.savefig(PLOTS_DIR / "fig2_noop_rate.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved {PLOTS_DIR / 'fig2_noop_rate.png'}")


# === Plot 3: Output volume per cycle per condition ===
fig, ax = plt.subplots(figsize=(6.5, 4))

# Average output bytes per agent per cycle within condition
def avg_size(condition_agents, cycle_n):
    sizes = [results["agents"][a]["output_bytes_by_cycle"].get(str(cycle_n), 0)
             for a in condition_agents]
    sizes = [s for s in sizes if s > 0]
    return sum(sizes) / len(sizes) if sizes else 0

WK = ["w1", "w2", "w3", "w4", "w5"]
CT = ["c1", "c2", "c3", "c4", "c5"]
wk_sizes = [avg_size(WK, c) / 1024 for c in cycles]
ct_sizes = [avg_size(CT, c) / 1024 for c in cycles]

x_pos = np.arange(len(cycles))
width = 0.4
ax.bar(x_pos - width/2, wk_sizes, width, label="Wakeup", color=COLOR_NOOP)
ax.bar(x_pos + width/2, ct_sizes, width, label="Control", color=COLOR_DONE)
ax.set_xticks(x_pos)
ax.set_xticklabels([str(c) for c in cycles])
ax.set_xlabel("Cycle")
ax.set_ylabel("Mean output size (KB)")
ax.set_title("Mean output volume per agent per cycle, by condition")
ax.legend(loc="upper right", frameon=False)

fig.tight_layout()
fig.savefig(PLOTS_DIR / "fig3_output_volume.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved {PLOTS_DIR / 'fig3_output_volume.png'}")

print("\nAll plots saved to:", PLOTS_DIR)
