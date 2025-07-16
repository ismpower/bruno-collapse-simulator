import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import subprocess
import os

def convert_eps_to_png(eps_path, output_png="converted_plot.png", dpi=300):
    # Requires ghostscript installed: `sudo apt install ghostscript`
    subprocess.run([
        "gs", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=pngalpha",
        f"-r{dpi}", f"-sOutputFile={output_png}", eps_path
    ], check=True)
    return output_png

def extract_curve_from_region(png_path, region_box, x_range, y_range):
    """
    Extracts curve pixels from a given bounding box (left, upper, right, lower)
    Maps them to (x_range, y_range) axis units.
    """
    img = Image.open(png_path).convert("L")
    cropped = img.crop(region_box)
    arr = np.array(cropped)
    curve_coords = np.column_stack(np.where(arr < 128))  # threshold for dark pixels

    if len(curve_coords) == 0:
        print("⚠️ No curve found in selected region.")
        return None, None

    # Invert Y since pixel 0 is top
    ys = cropped.height - curve_coords[:, 0]
    xs = curve_coords[:, 1]

    # Normalize to axis scale
    x_vals = np.interp(xs, [0, cropped.width], x_range)
    y_vals = np.interp(ys, [0, cropped.height], y_range)
    return x_vals, y_vals

def plot_extracted_signal(x, y, label):
    plt.figure(figsize=(10, 4))
    plt.plot(x, y, label=label)
    plt.title(f"Extracted Signal: {label}")
    plt.xlabel("Time (s)")
    plt.ylabel("Signal Value")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# === MAIN USAGE ===
if __name__ == "__main__":
    eps_file = "shot_comparisons_formatted.eps"
    png_file = convert_eps_to_png(eps_file)

    # Define manually the region (x1, y1, x2, y2) for each subplot
    # These must be tuned per your figure. Below are dummy boxes:
    subplot_boxes = {
        "ANB_SS_SUM_POWER": (100, 150, 700, 280),
        "ANU_NEUTRONS":     (100, 300, 700, 430),
        "AYC_TE_CORE":      (100, 450, 700, 580),
        "AYC_NE_CORE":      (100, 600, 700, 730)
    }

    # Time range shared across all shots (check axis labels!)
    time_range = (0, 0.25)  # in seconds

    # Value ranges per subplot (tune this visually from axes):
    value_ranges = {
        "ANB_SS_SUM_POWER": (0, 4e6),     # e.g., Power in Watts
        "ANU_NEUTRONS":     (0, 1e16),    # neutron rate
        "AYC_TE_CORE":      (0, 2000),    # eV (→ multiply by 11600 for Kelvin)
        "AYC_NE_CORE":      (0, 8e19)     # m⁻³
    }

    extracted = {}

    for name, box in subplot_boxes.items():
        x, y = extract_curve_from_region(png_file, box, time_range, value_ranges[name])
        if x is not None:
            extracted[name] = (x, y)
            plot_extracted_signal(x, y, label=name)
