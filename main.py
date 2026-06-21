"""
main.py
-------
Entry point for the Relativity Simulation & Spacetime Visualisation project.

Run individual demonstrations or the full suite:

    python main.py                  # full demo suite (saves all figures)
    python main.py --demo spacetime # single demo
    python main.py --list           # list available demos

Figures are saved to  output/
"""

import argparse
import os
import sys

# Make sure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Individual demo functions
# ---------------------------------------------------------------------------

def demo_spacetime_diagram():
    """Minkowski diagram with one boosted observer."""
    from visualizations.spacetime_diagram import plot_spacetime_diagram
    fig, _ = plot_spacetime_diagram(
        beta=0.6,
        events=[(3, 1, "E₁"), (-2, 0.5, "E₂")],
        save_path=os.path.join(OUTPUT_DIR, "spacetime_diagram.png"),
        show=False,
    )
    print("[1/6] Spacetime diagram saved.")
    return fig


def demo_multiple_observers():
    """Worldlines for several inertial observers."""
    from visualizations.spacetime_diagram import plot_multiple_observers
    fig, _ = plot_multiple_observers(
        betas=[-0.8, -0.5, 0.0, 0.5, 0.8],
        save_path=os.path.join(OUTPUT_DIR, "multiple_observers.png"),
        show=False,
    )
    print("[2/6] Multiple observers saved.")
    return fig


def demo_relativistic_effects():
    """γ, time dilation, and length contraction vs β."""
    from visualizations.relativistic_effects import plot_relativistic_effects
    fig = plot_relativistic_effects(
        save_path=os.path.join(OUTPUT_DIR, "relativistic_effects.png"),
        show=False,
    )
    print("[3/6] Relativistic effects saved.")
    return fig


def demo_twin_paradox():
    """Twin-paradox spacetime diagram."""
    from visualizations.relativistic_effects import plot_twin_paradox
    fig = plot_twin_paradox(
        beta=0.8, L=4.0,
        save_path=os.path.join(OUTPUT_DIR, "twin_paradox.png"),
        show=False,
    )
    print("[4/6] Twin paradox saved.")
    return fig


def demo_velocity_addition():
    """Relativistic vs Galilean velocity addition."""
    from visualizations.relativistic_effects import plot_velocity_addition
    fig = plot_velocity_addition(
        save_path=os.path.join(OUTPUT_DIR, "velocity_addition.png"),
        show=False,
    )
    print("[5/6] Velocity addition saved.")
    return fig


def demo_causal_structure():
    """Causal classification of events relative to the origin."""
    from visualizations.causal_structure import plot_causal_classification
    fig = plot_causal_classification(
        save_path=os.path.join(OUTPUT_DIR, "causal_structure.png"),
        show=False,
    )
    print("[6/6] Causal structure saved.")
    return fig


def demo_acceleration():
    """Minkowski diagram with a Rindler (accelerating) worldline."""
    from visualizations.spacetime_diagram import plot_spacetime_diagram
    fig, _ = plot_spacetime_diagram(
        beta=0.5,
        show_acceleration=True,
        alpha_accel=0.8,
        save_path=os.path.join(OUTPUT_DIR, "rindler_worldline.png"),
        show=False,
    )
    print("[bonus] Rindler worldline saved.")
    return fig


# ---------------------------------------------------------------------------
# Interval-table demo (text output only)
# ---------------------------------------------------------------------------

def demo_interval_table():
    from visualizations.causal_structure import print_interval_table
    pairs = [
        ((0, 0), (3, 1),  "A → E₁  (timelike future)"),
        ((0, 0), (-3, 1), "A → E₂  (timelike past)"),
        ((0, 0), (1, 4),  "A → E₃  (spacelike)"),
        ((0, 0), (2, 2),  "A → E₄  (lightlike)"),
        ((1, 2), (3, 4),  "E₅ → E₆  (timelike)"),
    ]
    print("\n=== Spacetime Interval Table ===")
    print_interval_table(pairs)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

DEMOS = {
    "spacetime"   : demo_spacetime_diagram,
    "observers"   : demo_multiple_observers,
    "effects"     : demo_relativistic_effects,
    "twins"       : demo_twin_paradox,
    "velocity"    : demo_velocity_addition,
    "causal"      : demo_causal_structure,
    "acceleration": demo_acceleration,
    "intervals"   : demo_interval_table,
}


def main():
    parser = argparse.ArgumentParser(
        description="Relativity Simulation & Spacetime Visualisation"
    )
    parser.add_argument(
        "--demo", choices=list(DEMOS.keys()),
        help="Run a specific demo instead of the full suite."
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List available demos and exit."
    )
    args = parser.parse_args()

    if args.list:
        print("Available demos:")
        for name in DEMOS:
            print(f"  {name}")
        return

    if args.demo:
        DEMOS[args.demo]()
        return

    # Full suite
    print("\n=== Relativity Simulation: Full Demo Suite ===")
    print(f"Output directory: {OUTPUT_DIR}\n")
    for fn in DEMOS.values():
        try:
            fn()
        except Exception as exc:
            print(f"  [!] {fn.__name__} failed: {exc}")

    print(f"\nAll figures saved to → {OUTPUT_DIR}/")
    print("Done.")


if __name__ == "__main__":
    main()
