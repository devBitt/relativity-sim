# Relativity Simulation & Spacetime Visualisation

A Python project for simulating and visualising Special Relativity — Lorentz transformations, spacetime diagrams, causal structure, time dilation, length contraction, twin paradox, and uniformly accelerated (Rindler) worldlines.

Built as part of an independent study in General Relativity and Computational Physics.

---

## Features

| Module | What it does |
|---|---|
| `simulations/lorentz.py` | Core Lorentz boosts, γ, time dilation, length contraction, velocity addition, spacetime interval |
| `visualizations/spacetime_diagram.py` | Minkowski diagrams with light cones, boosted axes, simultaneity lines, multiple observers |
| `visualizations/relativistic_effects.py` | γ vs β plots, twin paradox, relativistic velocity addition |
| `visualizations/causal_structure.py` | Causal classification (timelike / lightlike / spacelike) of event pairs |
| `notebooks/exploration.ipynb` | Interactive Jupyter notebook covering all topics |

---

## Visualisations

### Minkowski Spacetime Diagram
- Lab frame and boosted observer worldlines
- Future and past light cones from the origin
- Boosted ct′ and x′ axes
- Lines of simultaneity in the moving frame
- Optional Rindler (uniformly accelerated) worldline

### Relativistic Effects
- Lorentz factor γ as a function of β
- Time dilation ratio t/τ vs β
- Length contraction ratio L/L₀ vs β

### Twin Paradox
- Full spacetime diagram of the travelling and stay-at-home twins
- Annotated departure, turnaround, and reunion events
- Correct proper-time computation for each twin

### Causal Structure
- Shaded timelike, lightlike, and spacelike regions
- Classification of arbitrary event pairs by their invariant interval s²

### Velocity Addition
- Relativistic vs Galilean velocity addition
- Demonstrates the speed-of-light speed limit

---

## Physics Background

**Lorentz transformation** (boost along x-axis):

```
ct′ =  γ(ct − βx)
 x′ =  γ(x  − βct)
```

where `β = v/c` and `γ = 1/√(1 − β²)`.

**Spacetime interval** (Lorentz invariant):

```
s² = −(Δct)² + (Δx)²
```

- `s² < 0` → timelike  (causally connected)
- `s² = 0` → lightlike (on the light cone)
- `s² > 0` → spacelike (no causal connection)

**Uniformly accelerated worldline** (Rindler, natural units c = 1):

```
ct(τ) = (1/α) sinh(ατ)
 x(τ) = (1/α) cosh(ατ)
```

---

## Project Structure

```
relativity-sim/
├── simulations/
│   ├── __init__.py
│   └── lorentz.py            # Core physics
├── visualizations/
│   ├── __init__.py
│   ├── spacetime_diagram.py  # Minkowski diagrams
│   ├── relativistic_effects.py
│   └── causal_structure.py
├── notebooks/
│   └── exploration.ipynb     # Interactive notebook
├── output/                   # Generated figures (git-ignored)
├── main.py                   # CLI entry point
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/relativity-sim.git
cd relativity-sim
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the full demo suite

```bash
python main.py
```

Figures are saved to `output/`.

### 4. Run a specific demo

```bash
python main.py --demo spacetime     # Minkowski diagram
python main.py --demo observers     # Multiple observers
python main.py --demo effects       # γ, dilation, contraction
python main.py --demo twins         # Twin paradox
python main.py --demo velocity      # Velocity addition
python main.py --demo causal        # Causal structure
python main.py --demo acceleration  # Rindler worldline
python main.py --demo intervals     # Interval table (text)
```

### 5. Interactive Jupyter notebook

```bash
jupyter notebook notebooks/exploration.ipynb
```

---

## Example Usage (Python API)

```python
from simulations.lorentz import gamma, boost_event, time_dilation, spacetime_interval

# Lorentz factor
g = gamma(0.8)
print(f"γ = {g:.4f}")   # γ = 1.6667

# Boost a spacetime event
ct_p, x_p = boost_event(ct=5.0, x=3.0, beta=0.6)

# Time dilation: proper time τ=10 s in a ship at β=0.8
t = time_dilation(tau=10, beta=0.8)
print(f"Coordinate time: {t:.2f} s")

# Classify two events
s2 = spacetime_interval(0, 0, 3, 1)   # s² = −8  → timelike
```

---

## Dependencies

- Python ≥ 3.9
- NumPy ≥ 1.24
- Matplotlib ≥ 3.7
- SciPy ≥ 1.11
- Jupyter (for notebook)

---

## References

- Susskind, L. & Friedman, A. — *Special Relativity and Classical Field Theory* (Theoretical Minimum series)
- Carroll, S. — *Spacetime and Geometry: An Introduction to General Relativity*
- Tong, D. — [Lectures on General Relativity](http://www.damtp.cam.ac.uk/user/tong/gr.html)
- Misner, Thorne & Wheeler — *Gravitation*

---

## Author

**Adithyan S**  
Integrated M.Sc. Physics, Amrita Vishwa Vidyapeetham, Amritapuri  
Research interests: General Relativity · Quantum Field Theory · Quantum Gravity · Computational Physics
