import pandas as pd
import matplotlib.pyplot as plt

# === CONFIG ===
filename = 'your_file.csv'  # Replace with your downloaded data filename
kappa = 0.001005  # Bruno Constant scalar

# === LOAD DATA ===
df = pd.read_csv(filename)

# Display column headers to verify contents
print("Available columns:", df.columns)

# === CONVERT AND COMPUTE (customize based on column names) ===
# Example: if temperature is in 'Te_keV', convert to Kelvin
if 'Te_keV' in df.columns:
    df['Te_K'] = df['Te_keV'] * 1.160e7
    df['beta_B'] = kappa * df['Te_K']

# === PLOT (adjust columns based on what's available) ===
plt.figure(figsize=(12, 5))
if 'time' in df.columns and 'beta_B' in df.columns:
    plt.plot(df['time'], df['beta_B'], label='β_B = κ·T', color='purple')
    plt.axhline(1.0, linestyle='--', color='red', label='Collapse Threshold')
    plt.xlabel("Time (s)")
    plt.ylabel("β_B")
    plt.title("Bruno Constant Collapse Tracking")
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("🛑 Required columns not found. Please inspect df.columns and adjust the script.")
