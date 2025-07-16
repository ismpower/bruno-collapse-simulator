#!/usr/bin/env python3
import argparse, os

# Constants (SI Units)
hbar = 1.0545718e-34  # Planck constant over 2π [J·s]
G    = 6.67430e-11    # Gravitational constant [m³/kg/s²]
c    = 299792458      # Speed of light [m/s]
kB   = 1.380649e-23   # Boltzmann constant [J/K]

# Derived Planck length
l_P = (hbar * G / c**3)**0.5

def parse_args():
    p = argparse.ArgumentParser(
        description="Compute and plot the Bruno entropy collapse threshold."
    )
    p.add_argument(
        "--min-radius", "-r0", type=float, default=0.1,
        help="Minimum radius (in multiples of l_P)"
    )
    p.add_argument(
        "--max-radius", "-r1", type=float, default=1000,
        help="Maximum radius (in multiples of l_P)"
    )
    p.add_argument(
        "--num-points", "-n", type=int, default=10000,
        help="Number of radius samples"
    )
    p.add_argument(
        "--output-dir", "-o", default="results/sim1",
        help="Directory to save CSV and plot"
    )
    return p.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # Attempt to use CuPy on GPU, else NumPy on CPU
    try:
        import cupy as xp
        on_gpu = True
        print("🔧 Using CuPy on GPU")
    except ImportError:
        import numpy as xp
        on_gpu = False
        print("⚙️  CuPy not found—falling back to NumPy on CPU")

    import matplotlib.pyplot as plt

    # Radius range in Planck lengths
    r_values = xp.linspace(args.min_radius, args.max_radius, args.num_points)
    radii_m  = r_values * l_P

    # Entropy models (scaled, α=β=1)
    S_volume  = kB * (r_values)**3
    S_surface = kB * (r_values)**2
    K_bruno   = S_volume / S_surface

    # Move back to NumPy for saving & plotting
    if on_gpu:
        r_values  = xp.asnumpy(r_values)
        radii_m   = xp.asnumpy(radii_m)
        S_volume  = xp.asnumpy(S_volume)
        S_surface = xp.asnumpy(S_surface)
        K_bruno   = xp.asnumpy(K_bruno)

    # Find collapse threshold (closest to K=1)
    idx        = np.argmin(np.abs(K_bruno - 1))
    r_coll     = r_values[idx]
    r_coll_m   = radii_m[idx]

    # Save CSV
    out_csv = os.path.join(args.output_dir, "entropy_vs_radius.csv")
    header  = "r_planck,r_m,K_bruno,S_volume,S_surface"
    np.savetxt(
        out_csv,
        np.vstack([r_values, radii_m, K_bruno, S_volume, S_surface]).T,
        delimiter=",",
        header=header,
        comments=""
    )

    # Plot
    out_png = os.path.join(args.output_dir, "bruno_constant_threshold_plot.png")
    plt.figure(figsize=(10, 6))
    plt.plot(r_values, K_bruno, label='K_bruno = S_vol / S_surf')
    plt.axhline(1, color='gray', linestyle='--', label='Threshold (K=1)')
    plt.axvline(r_coll, color='red', linestyle='--',
                label=f'r_collapse ≈ {r_coll:.2f} l_P ({r_coll_m:.2e} m)')
    plt.xlabel('Radius (in Planck lengths)')
    plt.ylabel('K_bruno')
    plt.title('Entropy Collapse Threshold via Bruno Constant')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.show()

    print(f"✔ Results saved in {args.output_dir}")
    print(f"  • Collapse at K=1 when r ≈ {r_coll:.2f} l_P ({r_coll_m:.2e} m)")

if __name__ == "__main__":
    import numpy as np  # for argmin and savetxt
    main()
