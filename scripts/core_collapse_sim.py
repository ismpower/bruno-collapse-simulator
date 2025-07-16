# core_collapse.py

import numpy as np
import pandas as pd
import argparse

def eos_query(nB, T):
    # Replace with physical EoS interpolation when available
    P = 1e-2 * nB * T
    eps = 1.0 + 0.1 * nB + 0.05 * T
    cs2 = 0.1
    return P, eps, cs2

def simulate_collapse(t_final=1e-3, dt=1e-6):
    steps = int(t_final / dt)
    
    data = {
        't': [], 'P': [], 'eps': [], 'beta_B': [], 'cs2': [],
        's': [], 'S': [], 'L': [], 'Phi_nu': [], 'Qdot_nu': []
    }

    for step in range(steps):
        t = step * dt
        T = 0.5 + 0.5 * t / t_final
        nB = 0.26 * (1 + 10 * t / t_final)

        P, eps, cs2 = eos_query(nB, T)
        beta_B = P / eps if eps > 0 else np.nan
        
        s = 2.1 - 0.1 * t / t_final  # placeholder
        S = s * 1e-18
        L = (t / t_final) ** 2 * 1e42
        Phi_nu = (t / t_final) ** 2 * 1e34
        Qdot_nu = (1 - t / t_final) * 1e20

        data['t'].append(t)
        data['P'].append(P)
        data['eps'].append(eps)
        data['beta_B'].append(beta_B)
        data['cs2'].append(cs2)
        data['s'].append(s)
        data['S'].append(S)
        data['L'].append(L)
        data['Phi_nu'].append(Phi_nu)
        data['Qdot_nu'].append(Qdot_nu)

    return pd.DataFrame(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--t_final', type=float, default=1e-3, help='Simulation time in seconds')
    parser.add_argument('--dt', type=float, default=1e-6, help='Timestep in seconds')
    parser.add_argument('--output', type=str, default='collapse_output.csv', help='CSV output path')
    args = parser.parse_args()

    df = simulate_collapse(args.t_final, args.dt)
    df.to_csv(args.output, index=False)
    print(f"✅ Simulation complete. Output written to {args.output}")

if __name__ == '__main__':
    main()
