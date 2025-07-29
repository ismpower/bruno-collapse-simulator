import numpy as np
import matplotlib.pyplot as plt

# --- Constants ---
kappa = 1366  # Bruno constant (from GW150914)
collapse_threshold = lambda T: kappa * T

# --- Sample Time Series (replace or load from CSV) ---
# Simulated radius (m) and temperature (K) values over 40 time steps
time_steps = np.arange(40)
radius_series = np.logspace(10, 3, len(time_steps))  # collapsing from 10^10 to 10^3 m
temperature_series = np.logspace(3, 11, len(time_steps))  # heating from 10^3 to 10^11 K

# --- Bruno Computation ---
beta_B_series = 3 / radius_series
threshold_series = collapse_threshold(temperature_series)
collapse_triggered = beta_B_series >= threshold_series

# --- Find collapse point (first True)
collapse_index = np.argmax(collapse_triggered)
collapse_detected = collapse_triggered[collapse_index]
collapse_time = time_steps[collapse_index] if collapse_detected else None

# --- Output summary ---
print("🧠 Bruno Collapse Tracker Report")
if collapse_detected:
    print(f"🧨 Collapse triggered at time step {collapse_time}")
    print(f"    Radius       : {radius_series[collapse_index]:.3e} m")
    print(f"    Temperature  : {temperature_series[collapse_index]:.3e} K")
    print(f"    β_B          : {beta_B_series[collapse_index]:.3e}")
    print(f"    κ·T          : {threshold_series[collapse_index]:.3e}")
else:
    print("✅ No Bruno collapse occurred in this time series.")

# --- Plotting ---
plt.figure(figsize=(10, 6))
plt.plot(time_steps, beta_B_series, label='β_B = 3/R', color='red')
plt.plot(time_steps, threshold_series, label='κ · T', color='blue', linestyle='--')
if collapse_detected:
    plt.axvline(collapse_time, color='purple', linestyle=':', label='Collapse Triggered')
plt.xlabel("Time Step")
plt.ylabel("Bruno Collapse Metrics")
plt.title("Bruno Collapse Tracker")
plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.tight_layout()
plt.show()
