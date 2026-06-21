"""
lorentz.py
----------
Core module for Lorentz transformations in Special Relativity.

All velocities are expressed as fractions of the speed of light (β = v/c).
Natural units: c = 1 unless stated otherwise.
"""

import numpy as np


# ---------------------------------------------------------------------------
# Fundamental helpers
# ---------------------------------------------------------------------------

def gamma(beta: float) -> float:
    """
    Compute the Lorentz factor γ = 1 / sqrt(1 - β²).

    Parameters
    ----------
    beta : float
        Velocity as a fraction of c.  Must satisfy |β| < 1.

    Returns
    -------
    float
        Lorentz factor γ ≥ 1.
    """
    if abs(beta) >= 1.0:
        raise ValueError(f"Speed |β| must be < 1 (got β = {beta})")
    return 1.0 / np.sqrt(1.0 - beta ** 2)


def lorentz_matrix(beta: float) -> np.ndarray:
    """
    Return the 2×2 Lorentz boost matrix for a boost along the x-axis.

    The matrix maps (ct, x) in frame S to (ct', x') in frame S':

        | ct' |   |  γ   -γβ | | ct |
        |  x' | = | -γβ   γ  | |  x |

    Parameters
    ----------
    beta : float
        Velocity of S' relative to S as a fraction of c.

    Returns
    -------
    np.ndarray, shape (2, 2)
    """
    g = gamma(beta)
    return np.array([
        [ g,      -g * beta],
        [-g * beta,  g     ]
    ])


def boost_event(ct: float, x: float, beta: float):
    """
    Transform a single spacetime event (ct, x) under a Lorentz boost.

    Parameters
    ----------
    ct, x : float
        Spacetime coordinates in frame S.
    beta : float
        Boost velocity (fraction of c).

    Returns
    -------
    tuple (ct_prime, x_prime)
    """
    vec = np.array([ct, x])
    ct_p, x_p = lorentz_matrix(beta) @ vec
    return float(ct_p), float(x_p)


def boost_events(ct_arr: np.ndarray, x_arr: np.ndarray, beta: float):
    """
    Vectorised Lorentz boost for arrays of events.

    Parameters
    ----------
    ct_arr, x_arr : array-like, shape (N,)
    beta : float

    Returns
    -------
    ct_prime, x_prime : np.ndarray, shape (N,)
    """
    ct_arr = np.asarray(ct_arr, dtype=float)
    x_arr  = np.asarray(x_arr,  dtype=float)
    g = gamma(beta)
    ct_p = g * ct_arr - g * beta * x_arr
    x_p  = -g * beta * ct_arr + g * x_arr
    return ct_p, x_p


# ---------------------------------------------------------------------------
# Derived physical quantities
# ---------------------------------------------------------------------------

def time_dilation(tau: float, beta: float) -> float:
    """
    Compute the coordinate time elapsed in S when proper time τ passes in S'.

    t = γ τ

    Parameters
    ----------
    tau : float
        Proper time (time measured in the moving frame S').
    beta : float
        Velocity of S' relative to S.

    Returns
    -------
    float  – coordinate time in S.
    """
    return gamma(beta) * tau


def length_contraction(L0: float, beta: float) -> float:
    """
    Compute the contracted length measured in S for a rod at rest in S'.

    L = L₀ / γ

    Parameters
    ----------
    L0 : float
        Proper length (length in the rest frame S').
    beta : float
        Velocity of S' relative to S.

    Returns
    -------
    float – contracted length measured in S.
    """
    return L0 / gamma(beta)


def velocity_addition(u: float, v: float) -> float:
    """
    Relativistic velocity-addition formula.

    w = (u + v) / (1 + uv/c²)

    Parameters
    ----------
    u : float
        Velocity of object in frame S' (fraction of c).
    v : float
        Velocity of S' relative to S (fraction of c).

    Returns
    -------
    float – velocity of object as measured in S (fraction of c).
    """
    return (u + v) / (1.0 + u * v)


def spacetime_interval(ct1: float, x1: float, ct2: float, x2: float) -> float:
    """
    Compute the Lorentz-invariant spacetime interval s² between two events.

    s² = -(Δct)² + (Δx)²

    Negative → timelike, zero → lightlike, positive → spacelike.

    Parameters
    ----------
    ct1, x1 : float  – first event.
    ct2, x2 : float  – second event.

    Returns
    -------
    float – s²  (can be negative).
    """
    dct = ct2 - ct1
    dx  = x2  - x1
    return -(dct ** 2) + (dx ** 2)


def classify_interval(s2: float) -> str:
    """Return 'timelike', 'lightlike', or 'spacelike' for a given s²."""
    if np.isclose(s2, 0.0):
        return "lightlike"
    return "timelike" if s2 < 0 else "spacelike"


# ---------------------------------------------------------------------------
# Worldline generation
# ---------------------------------------------------------------------------

def inertial_worldline(beta: float, tau_range: tuple = (-5, 5), n: int = 400):
    """
    Generate the worldline of an inertial observer moving at velocity β.

    The observer passes through the origin at τ = 0.

    Parameters
    ----------
    beta : float
        Velocity (fraction of c).
    tau_range : (float, float)
        Range of proper time.
    n : int
        Number of sample points.

    Returns
    -------
    ct, x : np.ndarray  – coordinate arrays in the lab frame S.
    """
    g   = gamma(beta)
    tau = np.linspace(*tau_range, n)
    ct  = g * tau
    x   = g * beta * tau
    return ct, x


def uniformly_accelerated_worldline(alpha: float, tau_range: tuple = (-3, 3), n: int = 600):
    """
    Generate the Rindler worldline of a uniformly accelerating observer.

    The parametric equations in natural units (c = 1) are:
        ct(τ) = (1/α) sinh(α τ)
         x(τ) = (1/α) cosh(α τ)

    Parameters
    ----------
    alpha : float
        Proper acceleration (in units of c²/length).
    tau_range : (float, float)
        Proper-time range.
    n : int
        Number of sample points.

    Returns
    -------
    ct, x : np.ndarray
    """
    tau = np.linspace(*tau_range, n)
    ct  = (1.0 / alpha) * np.sinh(alpha * tau)
    x   = (1.0 / alpha) * np.cosh(alpha * tau)
    return ct, x
