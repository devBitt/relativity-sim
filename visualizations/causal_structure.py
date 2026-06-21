"""
causal_structure.py
-------------------
Visualise causal structure, light cones, and the invariant interval
classification on a Minkowski diagram.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from simulations.lorentz import spacetime_interval, classify_interval


PALETTE = {
    "bg"         : "#0d1117",
    "grid"       : "#21262d",
    "text"       : "#c9d1d9",
    "timelike"   : "#3fb950",   # green – causally connected
    "spacelike"  : "#ff7b72",   # red   – outside light cone
    "lightlike"  : "#f7c948",   # gold  – on the light cone
    "future_cone": "#58a6ff",
    "past_cone"  : "#d2a8ff",
    "event_A"    : "#ffffff",
    "event_B"    : "#ffa657",
}


def plot_causal_classification(
    events_B: list = None,
    save_path: str = None,
    show: bool = True,
):
    """
    Place event A at the origin and classify each event B in `events_B`
    by its causal relation to A.

    Parameters
    ----------
    events_B : list of (ct, x, label)
        Events to classify relative to A = (0, 0).
        Defaults to a representative demo set.
    save_path : str or None
    show : bool
    """
    if events_B is None:
        events_B = [
            ( 3.0,  1.0, "B₁\n(timelike future)"),
            (-3.5,  0.5, "B₂\n(timelike past)"),
            ( 1.0,  3.5, "B₃\n(spacelike)"),
            ( 2.0,  2.0, "B₄\n(lightlike)"),
            (-1.5, -3.0, "B₅\n(spacelike)"),
        ]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor(PALETTE["bg"])
    fig.patch.set_facecolor(PALETTE["bg"])

    LIMS = 6.0

    # --- Shade causal regions ---
    x_fill = np.linspace(-LIMS, LIMS, 600)
    # Future light-cone interior (timelike future)
    ax.fill_between(x_fill, np.abs(x_fill), LIMS,
                    color=PALETTE["future_cone"], alpha=0.07)
    # Past light-cone interior (timelike past)
    ax.fill_between(x_fill, -LIMS, -np.abs(x_fill),
                    color=PALETTE["past_cone"], alpha=0.07)

    # --- Light cone lines ---
    for sign in [1, -1]:
        ax.plot([-LIMS, LIMS], [-LIMS * sign, LIMS * sign],
                color=PALETTE["lightlike"], linewidth=1.6,
                linestyle="--", alpha=0.85)

    # --- Annotations for regions ---
    base_kwargs = dict(fontsize=9, alpha=0.6, ha="center", va="center")
    ax.text( 0,  4.5, "Absolute Future\n(timelike)", color=PALETTE["future_cone"], **base_kwargs)
    ax.text( 0, -4.5, "Absolute Past\n(timelike)",   color=PALETTE["past_cone"],   **base_kwargs)
    ax.text( 4.5, 0, "Elsewhere\n(spacelike)",       color=PALETTE["spacelike"],   **base_kwargs)
    ax.text(-4.5, 0, "Elsewhere\n(spacelike)",       color=PALETTE["spacelike"],   **base_kwargs)

    # --- Event A at origin ---
    ax.scatter([0], [0], color=PALETTE["event_A"], s=80, zorder=6)
    ax.annotate("A  (0, 0)", (0, 0), xytext=(0.2, -0.6),
                color=PALETTE["event_A"], fontsize=9)

    # --- Plot and classify each event B ---
    legend_patches = []
    seen = set()
    for (ct_b, x_b, lbl) in events_B:
        s2     = spacetime_interval(0, 0, ct_b, x_b)
        cat    = classify_interval(s2)
        colour = {"timelike": PALETTE["timelike"],
                  "spacelike": PALETTE["spacelike"],
                  "lightlike": PALETTE["lightlike"]}[cat]

        ax.scatter([x_b], [ct_b], color=colour, s=70, zorder=5)
        ax.annotate(f"{lbl}\ns² = {s2:.1f} ({cat})",
                    (x_b, ct_b), xytext=(x_b + 0.25, ct_b + 0.25),
                    color=colour, fontsize=8)
        # Draw dashed line from A to B
        ax.plot([0, x_b], [0, ct_b], color=colour,
                linewidth=1, linestyle=":", alpha=0.6)

        if cat not in seen:
            legend_patches.append(
                mpatches.Patch(color=colour, label=cat.capitalize()))
            seen.add(cat)

    ax.legend(handles=legend_patches,
              facecolor="#161b22", edgecolor=PALETTE["grid"],
              labelcolor=PALETTE["text"], fontsize=9, loc="upper right")

    # Axes styling
    ax.spines[:].set_color(PALETTE["grid"])
    ax.tick_params(colors=PALETTE["text"])
    ax.grid(True, color=PALETTE["grid"], linewidth=0.5, linestyle="--", alpha=0.6)
    ax.set_xlim(-LIMS, LIMS)
    ax.set_ylim(-LIMS, LIMS)
    ax.set_aspect("equal")
    ax.axhline(0, color=PALETTE["text"], linewidth=0.6, alpha=0.3)
    ax.axvline(0, color=PALETTE["text"], linewidth=0.6, alpha=0.3)
    ax.set_xlabel("x / c", color=PALETTE["text"], fontsize=11)
    ax.set_ylabel("ct", color=PALETTE["text"], fontsize=11)
    ax.set_title("Causal Structure of Minkowski Spacetime",
                 color=PALETTE["text"], fontsize=13, pad=12)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=PALETTE["bg"])
        print(f"Saved → {save_path}")
    if show:
        plt.show()
    return fig


def print_interval_table(event_pairs: list):
    """
    Print a formatted table of spacetime intervals.

    Parameters
    ----------
    event_pairs : list of ((ct1,x1), (ct2,x2), label)
    """
    print(f"\n{'Label':<25} {'s²':>8}  {'Type':<12}")
    print("-" * 50)
    for (p1, p2, lbl) in event_pairs:
        s2  = spacetime_interval(*p1, *p2)
        cat = classify_interval(s2)
        print(f"{lbl:<25} {s2:>8.3f}  {cat}")
    print()
