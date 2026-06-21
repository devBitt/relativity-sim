"""
spacetime_diagram.py
--------------------
Generate Minkowski spacetime diagrams with worldlines, light cones,
simultaneity lines, and Lorentz-boosted axes.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from simulations.lorentz import (
    gamma, boost_events, inertial_worldline, uniformly_accelerated_worldline
)


# ---------------------------------------------------------------------------
# Colour palette (dark physics-lab aesthetic)
# ---------------------------------------------------------------------------
PALETTE = {
    "bg"          : "#0d1117",
    "axes"        : "#ffffff",
    "grid"        : "#21262d",
    "lightcone"   : "#f7c948",
    "worldline_S" : "#58a6ff",
    "worldline_Sp": "#ff7b72",
    "boosted_axis": "#3fb950",
    "simultaneity": "#d2a8ff",
    "event"       : "#f78166",
    "text"        : "#c9d1d9",
}


def _setup_dark_axes(ax, xlim=(-6, 6), ylim=(-6, 6), xlabel="x / c", ylabel="ct"):
    """Apply dark-theme styling to a matplotlib Axes object."""
    ax.set_facecolor(PALETTE["bg"])
    ax.figure.patch.set_facecolor(PALETTE["bg"])
    ax.spines[:].set_color(PALETTE["grid"])
    ax.tick_params(colors=PALETTE["text"], labelsize=9)
    ax.set_xlabel(xlabel, color=PALETTE["text"], fontsize=11)
    ax.set_ylabel(ylabel, color=PALETTE["text"], fontsize=11)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")
    ax.grid(True, color=PALETTE["grid"], linewidth=0.6, linestyle="--", alpha=0.7)
    # Draw lab-frame axes
    ax.axhline(0, color=PALETTE["axes"], linewidth=0.8, alpha=0.5)
    ax.axvline(0, color=PALETTE["axes"], linewidth=0.8, alpha=0.5)


def _draw_light_cone(ax, ct0=0, x0=0, extent=6):
    """Draw forward and backward light cones from a given event."""
    t_vals = np.array([-extent, extent])
    # Future light cone
    ax.plot([x0, x0 + extent], [ct0, ct0 + extent],
            color=PALETTE["lightcone"], linewidth=1.5, linestyle="--", alpha=0.85)
    ax.plot([x0, x0 - extent], [ct0, ct0 + extent],
            color=PALETTE["lightcone"], linewidth=1.5, linestyle="--", alpha=0.85)
    # Past light cone
    ax.plot([x0, x0 + extent], [ct0, ct0 - extent],
            color=PALETTE["lightcone"], linewidth=1.5, linestyle="--", alpha=0.85)
    ax.plot([x0, x0 - extent], [ct0, ct0 - extent],
            color=PALETTE["lightcone"], linewidth=1.5, linestyle="--", alpha=0.85)
    # Shade future / past light-cone regions (very faint)
    x_fill = np.linspace(-extent, extent, 400)
    ax.fill_between(x_fill + x0, np.abs(x_fill) + ct0, extent + ct0,
                    color=PALETTE["lightcone"], alpha=0.04)
    ax.fill_between(x_fill + x0, -extent + ct0, -np.abs(x_fill) + ct0,
                    color=PALETTE["lightcone"], alpha=0.04)


def _draw_boosted_axes(ax, beta, extent=6):
    """Draw the ct' and x' axes of a boosted frame S'."""
    g = gamma(beta)
    # ct' axis: x = 0 in S' → ct = x / β in S
    if abs(beta) > 1e-9:
        ct_range = np.linspace(-extent, extent, 400)
        x_ctprime = beta * ct_range
        ax.plot(x_ctprime, ct_range, color=PALETTE["boosted_axis"],
                linewidth=1.4, linestyle="-.", alpha=0.8, label="ct′ axis")
    # x' axis: ct = 0 in S' → ct = β·x in S
    x_range = np.linspace(-extent, extent, 400)
    ct_xprime = beta * x_range
    ax.plot(x_range, ct_xprime, color=PALETTE["boosted_axis"],
            linewidth=1.4, linestyle=":", alpha=0.8, label="x′ axis")


def plot_spacetime_diagram(
    beta: float = 0.6,
    show_acceleration: bool = False,
    alpha_accel: float = 1.0,
    events: list = None,
    save_path: str = None,
    show: bool = True,
):
    """
    Plot a complete Minkowski spacetime diagram.

    Parameters
    ----------
    beta : float
        Velocity of the moving frame S'.
    show_acceleration : bool
        If True, also plot a uniformly accelerating worldline.
    alpha_accel : float
        Proper acceleration for the Rindler worldline.
    events : list of (ct, x, label) tuples
        Extra events to mark on the diagram.
    save_path : str or None
        If given, save the figure to this path.
    show : bool
        Call plt.show() at the end.

    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    _setup_dark_axes(ax)

    # Light cone from origin
    _draw_light_cone(ax)

    # Lab-frame observer (at rest)
    ax.axvline(0, ymin=0.1, ymax=0.9, color=PALETTE["worldline_S"],
               linewidth=2.2, label=f"S  (β = 0)")

    # Moving inertial worldline
    ct_wl, x_wl = inertial_worldline(beta, tau_range=(-5.5, 5.5))
    ax.plot(x_wl, ct_wl, color=PALETTE["worldline_Sp"],
            linewidth=2.2, label=f"S′ (β = {beta})")

    # Boosted axes
    _draw_boosted_axes(ax, beta)

    # Simultaneity line in S' (t' = 2 for demonstration)
    # In S': ct' = const → ct = γ(ct' + β·x') ; for x' ranging
    ct_sim = 2.0  # choose ct' = 2 in S'
    x_s_arr = np.linspace(-5, 5, 300)
    # x' = γ(x - β·ct), ct' = γ(ct - β·x)
    # For ct' = ct_sim: ct = γ·ct_sim + β·x  →  ct = β·x + γ·ct_sim
    g = gamma(beta)
    ct_sim_line = beta * x_s_arr + g * ct_sim
    mask = (ct_sim_line > -6) & (ct_sim_line < 6)
    ax.plot(x_s_arr[mask], ct_sim_line[mask],
            color=PALETTE["simultaneity"], linewidth=1.2,
            linestyle="--", alpha=0.7, label=f"ct′ = {ct_sim} (simult.)")

    # Accelerating worldline
    if show_acceleration:
        ct_a, x_a = uniformly_accelerated_worldline(alpha_accel, tau_range=(-2.5, 2.5))
        mask = (ct_a > -5.8) & (ct_a < 5.8) & (x_a > -5.8) & (x_a < 5.8)
        ax.plot(x_a[mask], ct_a[mask], color="#ffa657", linewidth=2,
                linestyle="-", label=f"Rindler (α = {alpha_accel})")

    # Extra events
    if events:
        for (ct_e, x_e, lbl) in events:
            ax.scatter([x_e], [ct_e], color=PALETTE["event"], s=60, zorder=5)
            ax.annotate(lbl, (x_e, ct_e), textcoords="offset points",
                        xytext=(6, 4), color=PALETTE["event"], fontsize=9)

    # Legend & title
    ax.legend(facecolor="#161b22", edgecolor=PALETTE["grid"],
              labelcolor=PALETTE["text"], fontsize=9, loc="upper left")
    ax.set_title(
        f"Minkowski Spacetime Diagram  |  β = {beta},  γ = {g:.3f}",
        color=PALETTE["text"], fontsize=13, pad=12
    )

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=PALETTE["bg"])
        print(f"Saved → {save_path}")
    if show:
        plt.show()
    return fig, ax


def plot_multiple_observers(betas: list, save_path: str = None, show: bool = True):
    """
    Plot worldlines for multiple inertial observers on one diagram.

    Parameters
    ----------
    betas : list of float
        Velocities for each observer.
    """
    colours = ["#58a6ff", "#ff7b72", "#3fb950", "#d2a8ff",
               "#ffa657", "#79c0ff", "#ffb3ba"]

    fig, ax = plt.subplots(figsize=(8, 8))
    _setup_dark_axes(ax)
    _draw_light_cone(ax)

    for i, beta in enumerate(betas):
        col = colours[i % len(colours)]
        ct_wl, x_wl = inertial_worldline(beta, tau_range=(-5.5, 5.5))
        ax.plot(x_wl, ct_wl, color=col, linewidth=2,
                label=f"β = {beta:+.2f},  γ = {gamma(beta):.2f}")

    ax.legend(facecolor="#161b22", edgecolor=PALETTE["grid"],
              labelcolor=PALETTE["text"], fontsize=9)
    ax.set_title("Multiple Inertial Observers", color=PALETTE["text"], fontsize=13)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=PALETTE["bg"])
    if show:
        plt.show()
    return fig, ax
