import numpy as np
from scipy.spatial import Delaunay
from scipy.interpolate import LinearNDInterpolator

# Load EoS table (adjust path as needed)
eos_data = np.loadtxt("eos_tables/lattimer_swesty_220L.dat")

# Unpack columns
nB, T, P, eps, cs2 = eos_data[:, 0], eos_data[:, 1], eos_data[:, 2], eos_data[:, 3], eos_data[:, 4]

# Prepare interpolation
points = np.column_stack((nB, T))
eos_hull = Delaunay(points)
P_interp = LinearNDInterpolator(points, P)
eps_interp = LinearNDInterpolator(points, eps)
cs2_interp = LinearNDInterpolator(points, cs2)

def eos_query(nB_query, T_query, safe_mode=True):
    """
    Evaluate Equation of State (EoS) at given baryon density and temperature.

    Parameters:
        nB_query : float or array-like — baryon density in fm⁻³
        T_query  : float or array-like — temperature in MeV
        safe_mode : bool — if True, points outside valid domain return NaN (default: True)

    Returns:
        dict with:
            'P'   : pressure [MeV/fm³]
            'eps' : specific energy [MeV]
            'cs2' : sound speed squared [dimensionless, ≥ 1e-8]
    """
    nB_query = np.atleast_1d(nB_query)
    T_query  = np.atleast_1d(T_query)
    pts = np.column_stack((nB_query, T_query))

    if safe_mode:
        mask = eos_hull.find_simplex(pts) >= 0
        return {
            'P':   np.where(mask, P_interp(pts), np.nan),
            'eps': np.where(mask, eps_interp(pts), np.nan),
            'cs2': np.where(mask, np.maximum(cs2_interp(pts), 1e-8), np.nan),
        }
    else:
        return {
            'P':   P_interp(pts),
            'eps': eps_interp(pts),
            'cs2': np.maximum(cs2_interp(pts), 1e-8),
        }
