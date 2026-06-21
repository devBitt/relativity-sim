"""
relativistic_effects.py
-----------------------
Visualise time dilation, length contraction, and the Lorentz factor
as functions of velocity.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from simulations.lorentz import gamma, time_dilation, length_contraction


PALETTE = {
    "bg"   : "#0d1117",
    "grid" : "#21262d",
    "text" : "#c9d1d9",
    "blue" : "#58a6ff",
    "red"  : "#ff7b72",
    "green": "#3fb950",
    "gold" : "#f7c948",
}

# ---------------------------------------------------------------------------
# 1.  γ, time dilation, length contraction vs β
# ---------------------------------------------------------------------------

def plot_relativistic_effects(save_path: str = None, show: bool = True):
    """
    Three-panel plot showing γ, time-dilation ratio, and length-contraction
    ratio as β → 1.
    """
    beta_vals = np.linspace(0.0, 0.9999, 2000)
    gamma_vals = 1.0 / np.sqrt(1.0 - beta_vals ** 2)

    fig = plt.figure(figsize=(14, 5), facecolor=PALETTE["bg"])
    gs  = gridspec.GridSpec(1, 3, wspace=0.38)

    # --- Panel 1: Lorentz factor ---
    ax1 = fig.add_subplot(gs[0])
    ax1.set_facecolor(PALETTE["bg"])
    ax1.plot(beta_vals, gamma_vals, color=PALETTE["blue"], linewidth=2)
    ax1.axhline(1, color=PALETTE["grid"], linewidth=0.8, linestyle="--")
    ax1.set_xlabel("β = v/c", color=PALETTE["text"])
    ax1.set_ylabel("γ (Lorentz factor)", color=PALETTE["text"])
    ax1.set_title("Lorentz Factor γ", color=PALETTE["text"], fontsize=12)
    ax1.set_ylim(0, 12)

    # Annotation at β = 0.9
    g_09 = gamma(0.9)
    ax1.annotate(f"β=0.9 → γ={g_09:.2f}",
                 xy=(0.9, g_09), xytext=(0.55, 7),
                 color=PALETTE["gold"], fontsize=9,
                 arrowprops=dict(arrowstyle="->", color=PALETTE["gold"], lw=0.9))

    # --- Panel 2: Time dilation ---
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor(PALETTE["bg"])
    # If τ_proper = 1 s, coordinate time = γ
    ax2.plot(beta_vals, gamma_vals, color=PALETTE["red"], linewidth=2)
    ax2.axhline(1, color=PALETTE["grid"], linewidth=0.8, linestyle="--")
    ax2.set_xlabel("β = v/c", color=PALETTE["text"])
    ax2.set_ylabel("t / τ  (dilation ratio)", color=PALETTE["text"])
    ax2.set_title("Time Dilation  t = γτ", color=PALETTE["text"], fontsize=12)
    ax2.set_ylim(0, 12)
    ax2.fill_between(beta_vals, 1, gamma_vals,
                     color=PALETTE["red"], alpha=0.08)

    # --- Panel 3: Length contraction ---
    ax3 = fig.add_subplot(gs[2])
    ax3.set_facecolor(PALETTE["bg"])
    contraction = 1.0 / gamma_vals          # L / L₀
    ax3.plot(beta_vals, contraction, color=PALETTE["green"], linewidth=2)
    ax3.axhline(1, color=PALETTE["grid"], linewidth=0.8, linestyle="--")
    ax3.set_xlabel("β = v/c", color=PALETTE["text"])
    ax3.set_ylabel("L / L₀  (contraction ratio)", color=PALETTE["text"])
    ax3.set_title("Length Contraction  L = L₀/γ", color=PALETTE["text"], fontsize=12)
    ax3.set_ylim(0, 1.1)
    ax3.fill_between(beta_vals, contraction, 1,
                     color=PALETTE["green"], alpha=0.08)

    # Common styling
    for ax in [ax1, ax2, ax3]:
        ax.spines[:].set_color(PALETTE["grid"])
        ax.tick_params(colors=PALETTE["text"])
        ax.grid(True, color=PALETTE["grid"], linewidth=0.5, linestyle="--")

    fig.suptitle("Relativistic Effects as a Function of Velocity",
                 color=PALETTE["text"], fontsize=14, y=1.02)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=PALETTE["bg"])
        print(f"Saved → {save_path}")
    if show:
        plt.show()
    return fig


# ---------------------------------------------------------------------------
# 2.  Twin paradox illustration
# ---------------------------------------------------------------------------

def plot_twin_paradox(beta: float = 0.8, L: float = 4.0,
                      save_path: str = None, show: bool = True):
    """
    Illustrate the twin paradox on a spacetime diagram.

    The travelling twin leaves at t=0, travels to distance L at speed β,
    then turns around and returns.

    Parameters
    ----------
    beta : float  Outbound (and inbound) speed.
    L    : float  Proper distance to the turnaround point (light-years).
    """
    g = gamma(beta)
    # Coordinate-time events (lab frame)
    t_turn  = L / beta          # turnaround
    t_return = 2 * L / beta     # arrival back

    # Proper time of travelling twin
    tau_half   = t_turn / g
    tau_travel = 2 * tau_half

    fig, ax = plt.subplots(figsize=(6, 9))
    ax.set_facecolor(PALETTE["bg"])
    fig.patch.set_facecolor(PALETTE["bg"])

    # Stay-at-home twin
    ax.plot([0, 0], [0, t_return],
            color=PALETTE["blue"], linewidth=2.5, label=f"Stay-at-home  (age: {t_return:.1f} yr)")

    # Travelling twin: out
    ax.plot([0, L], [0, t_turn],
            color=PALETTE["red"], linewidth=2.5, label=f"Traveller  (age: {tau_travel:.1f} yr)")
    # Travelling twin: return
    ax.plot([L, 0], [t_turn, t_return],
            color=PALETTE["red"], linewidth=2.5)

    # Events
    for (x_e, ct_e, lbl) in [
        (0, 0, "Departure"),
        (L, t_turn, f"Turnaround\n(x={L} ly, t={t_turn:.1f} yr)"),
        (0, t_return, "Reunion"),
    ]:
        ax.scatter([x_e], [ct_e], color=PALETTE["gold"], s=70, zorder=5)
        ax.annotate(lbl, (x_e, ct_e), xytext=(0.15, ct_e + 0.2),
                    color=PALETTE["gold"], fontsize=8.5)

    ax.set_xlabel("x  (light-years)", color=PALETTE["text"])
    ax.set_ylabel("t  (years)", color=PALETTE["text"])
    ax.set_title(f"Twin Paradox  |  β = {beta},  γ = {g:.3f}",
                 color=PALETTE["text"], fontsize=13)
    ax.legend(facecolor="#161b22", edgecolor=PALETTE["grid"],
              labelcolor=PALETTE["text"], fontsize=9)
    ax.spines[:].set_color(PALETTE["grid"])
    ax.tick_params(colors=PALETTE["text"])
    ax.grid(True, color=PALETTE["grid"], linewidth=0.5, linestyle="--")
    ax.set_xlim(-1, L + 1.5)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=PALETTE["bg"])
        print(f"Saved → {save_path}")
    if show:
        plt.show()
    return fig


# ---------------------------------------------------------------------------
# 3.  Velocity addition visualisation
# ---------------------------------------------------------------------------

def plot_velocity_addition(save_path: str = None, show: bool = True):
    """
    Show relativistic velocity addition vs Galilean addition for several
    values of v (frame velocity) and u (object velocity in that frame).
    """
    from simulations.lorentz import velocity_addition

    u_vals = np.linspace(-0.99, 0.99, 400)
    v_choices = [0.3, 0.6, 0.8, 0.95]
    colours   = [PALETTE["blue"], PALETTE["green"], PALETTE["red"], PALETTE["gold"]]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor=PALETTE["bg"])

    for ax, (v, col) in zip(axes, [(v_choices[1], colours[1]),
                                    (v_choices[3], colours[3])]):
        ax.set_facecolor(PALETTE["bg"])
        w_rel  = [velocity_addition(u, v) for u in u_vals]
        w_gal  = np.clip(u_vals + v, -1, 1)

        ax.plot(u_vals, w_rel, color=col, linewidth=2, label="Relativistic")
        ax.plot(u_vals, w_gal, color=PALETTE["text"], linewidth=1.5,
                linestyle="--", alpha=0.5, label="Galilean  (u + v)")
        ax.axhline( 1, color=PALETTE["gold"], linewidth=0.8, linestyle=":")
        ax.axhline(-1, color=PALETTE["gold"], linewidth=0.8, linestyle=":")
        ax.set_xlabel("u  (object speed in S′, fraction of c)", color=PALETTE["text"])
        ax.set_ylabel("w  (object speed in S, fraction of c)", color=PALETTE["text"])
        ax.set_title(f"Velocity Addition  |  frame v = {v}c",
                     color=PALETTE["text"], fontsize=12)
        ax.legend(facecolor="#161b22", edgecolor=PALETTE["grid"],
                  labelcolor=PALETTE["text"], fontsize=9)
        ax.spines[:].set_color(PALETTE["grid"])
        ax.tick_params(colors=PALETTE["text"])
        ax.grid(True, color=PALETTE["grid"], linewidth=0.5, linestyle="--")
        ax.set_ylim(-1.05, 1.05)

    fig.suptitle("Relativistic Velocity Addition", color=PALETTE["text"], fontsize=14)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=PALETTE["bg"])
        print(f"Saved → {save_path}")
    if show:
        plt.show()
    return fig
