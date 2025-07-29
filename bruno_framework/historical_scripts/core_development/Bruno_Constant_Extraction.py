# === Bruno Constant Extraction Script (with PNG output) ===
# === Figure Tag: fig_bruno_1_5.png - fig_bruno_vs_temperature_1_5.png ===
# Description: Bruno Constant emergence during entropy collapse (Test 1.5)
# Related Data Export: Entropy_Collapse_Export_1.5.csv
# Outputs Final Figure: /Figures/fig_bruno_1_5.png - fig_bruno_vs_temperature_1_5.png

# fig_bruno_vs_temperature_1_5.png | Bruno Constant as a function of entropy-derived temperature | Entropy Collapse Test 1.5.py | Entropy_Collapse_Export_1.5.csv | Confirms Bruno ∝ T under radiation scaling |

import re
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Extract valid numerical lines from the test file
def extract_numeric_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            if re.match(r'^\s*[\d.+eE-]+\s*,\s*[\d.+eE-]+\s*,\s*[\d.+eE-]+\s*,\s*[\d.+eE-]+', line):
                try:
                    time, entropy, volume, area = map(float, line.strip().split(','))
                    data.append((time, entropy, volume, area))
                except:
                    continue
    return pd.DataFrame(data, columns=["Time", "Entropy", "Volume", "Area"])

# 2. Calculate entropy densities and Bruno estimate
def compute_bruno_estimates(df):
    df["s_3D"] = df["Entropy"] / df["Volume"]
    df["s_2D"] = df["Entropy"] / df["Area"]
    df["BrunoEstimate"] = df["s_3D"] / df["s_2D"]
    return df

# 3. Plot + Save PNG
def plot_bruno_threshold(df, label='Collapse Test', output_dir="."):
    plt.figure(figsize=(10,6))
    plt.plot(df["Time"], df["BrunoEstimate"], label=f'Bruno Const ~ A/V: {label}')
    plt.axhline(1, color='gray', linestyle='--', label='Threshold (1:1)')
    plt.xlabel("Time")
    plt.ylabel("Bruno Constant Estimate")
    plt.title("Bruno Constant Emergence During Collapse")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Save figure to PNG
    safe_label = label.replace(" ", "_").replace(".", "")
    filename = f"fig_bruno_{safe_label.lower()}.png"
    full_path = os.path.join(output_dir, filename)
    plt.savefig(full_path)
    print(f"📁 Figure saved: {full_path}")
    plt.show()

# === RUN HERE ===
file_path = "D:\Entropy-Collapse-Research\Data\Entropy_Collapse_Export_1.5.csv"
df_test = extract_numeric_data(file_path)
df_test = compute_bruno_estimates(df_test)
plot_bruno_threshold(df_test, label='1.5', output_dir="D:\Entropy-Collapse-Research\Figures\Final")

# Show last few Bruno values for inspection
print("\n🧠 Last few Bruno Constant values:")
print(df_test[["Time", "BrunoEstimate"]].tail(10).to_string(index=False))

def plot_bruno_vs_temperature(df, label='Collapse Test', output_dir="."):
    # Optional: estimate temperature from time if T_range is log scale
    # This assumes time index matches 10^time = T
    df["Temperature"] = [10**i for i in range(len(df))]
    

    plt.figure(figsize=(10,6))
    plt.plot(df["Temperature"], df["BrunoEstimate"], marker='o', linestyle='-', color='darkred', label="Bruno Constant")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Entropy-Derived Temperature (K)")
    plt.ylabel("Bruno Constant Estimate")
    plt.title("Bruno Constant vs. Entropy-Derived Temperature")
    plt.grid(True, which='both', linestyle='--')
    plt.legend()
    plt.tight_layout()

    # Save figure
    safe_label = label.replace(" ", "_").replace(".", "")
    filename = f"fig_bruno_vs_temperature_{safe_label.lower()}.png"
    full_path = os.path.join(output_dir, filename)
    plt.savefig(full_path)
    print(f"📁 Figure saved: {full_path}")
    plt.show()

plot_bruno_vs_temperature(df_test, label="1.5", output_dir="D:\Entropy-Collapse-Research\Figures\Final")

def detect_bruno_threshold(df):
    # Ensure temperature is defined
    if "Temperature" not in df.columns:
        df["Temperature"] = [10**i for i in range(len(df))]

    # Find first point where BrunoEstimate ≥ 1
    threshold_index = df[df["BrunoEstimate"] >= 1].index.min()

    if pd.isna(threshold_index):
        print("⚠️ Bruno Constant never crosses 1.")
        return None, None
    else:
        threshold_time = df.loc[threshold_index, "Time"]
        threshold_temp = df.loc[threshold_index, "Temperature"]
        print(f"🧨 Collapse threshold detected at:")
        print(f"   Time       = {threshold_time}")
        print(f"   Temperature = {threshold_temp:.2e} K")
        return threshold_time, threshold_temp

def plot_bruno_with_collapse_marker(df, label='Collapse Test', output_dir="."):
    df["Temperature"] = [10**i for i in range(len(df))]
    collapse_time, collapse_temp = detect_bruno_threshold(df)

    plt.figure(figsize=(10,6))
    plt.plot(df["Temperature"], df["BrunoEstimate"], color='darkred', label="Bruno Constant")
    plt.xscale('log')
    plt.yscale('log')

    if collapse_temp:
        plt.axvline(collapse_temp, color='red', linestyle='--', alpha=0.7, label="Collapse Threshold (Bruno = 1)")
        plt.scatter([collapse_temp], [1], color='red', s=80, zorder=5)

    plt.xlabel("Entropy-Derived Temperature (K)")
    plt.ylabel("Bruno Constant Estimate")
    plt.title("Bruno Constant vs. Entropy-Derived Temperature (with Collapse Marker)")
    plt.grid(True, which='both', linestyle='--')
    plt.legend()
    plt.tight_layout()

    filename = f"fig_bruno_vs_temperature_marked_{label}.png"
    full_path = os.path.join(output_dir, filename)
    plt.savefig(full_path)
    print(f"📁 Figure saved: {full_path}")
    plt.show()

plot_bruno_with_collapse_marker(df_test, label="1_5", output_dir="D:\Entropy-Collapse-Research\Figures\Final")

df_test = extract_numeric_data(file_path)
df_test = compute_bruno_estimates(df_test)
plot_bruno_with_collapse_marker(df_test, label="1_5_extended", output_dir="D:\Entropy-Collapse-Research\Figures\Final")
