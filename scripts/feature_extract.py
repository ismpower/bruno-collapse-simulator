import os
import pandas as pd
from datetime import datetime

INPUT_DIR = "data/raw"
OUTPUT_DIR = "data/parsed"

def parse_filename_metadata(filename):
    """Extract date, customer, and unit from filename."""
    base = os.path.basename(filename)
    name = os.path.splitext(base)[0]
    parts = name.split("_")
    if len(parts) != 3:
        raise ValueError(f"Filename format invalid: {filename}")
    date_str, customer, unit_id = parts
    return date_str, customer, unit_id

def process_file(path):
    try:
        df = pd.read_csv(path)
        if 'time_ms' not in df.columns or 'can_id' not in df.columns:
            raise ValueError("Required columns missing")

        date_str, customer, unit_id = parse_filename_metadata(path)
        df['log_date'] = date_str
        df['customer'] = customer
        df['unit_id'] = unit_id

        # Optional: add timestamp column
        df['timestamp'] = pd.to_datetime(df['time_ms'], unit='ms')

        output_path = os.path.join(OUTPUT_DIR, os.path.basename(path))
        df.to_csv(output_path, index=False)
        print(f"[OK] Parsed and saved: {output_path}")
    except Exception as e:
        print(f"[ERROR] {path}: {e}")

def process_all_logs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fname in os.listdir(INPUT_DIR):
        if fname.endswith(".csv"):
            fpath = os.path.join(INPUT_DIR, fname)
            process_file(fpath)

if __name__ == "__main__":
    print(f"[RUN] Feature Extract started at {datetime.now()}")
    process_all_logs()
    print(f"[DONE] Finished at {datetime.now()}")
