#!/usr/bin/env python3
# can_ingest.py – Varda AI: Ingest raw CAN logs into structured JSONL

import os
import json
import csv
from datetime import datetime

DATA_DIR = "../data/raw"
SUPPORTED_EXT = [".log", ".txt", ".csv"]

def load_can_file(filepath):
    ext = os.path.splitext(filepath)[1]
    entries = []
    with open(filepath, 'r') as f:
        if ext == ".csv":
            reader = csv.DictReader(f)
            for row in reader:
                entries.append(row)
        else:
            for line in f:
                parsed = parse_can_line(line)
                if parsed:
                    entries.append(parsed)
    return entries

def parse_can_line(line):
    parts = line.strip().split()
    if len(parts) < 3:
        return None
    try:
        return {
            "timestamp": parts[0],
            "can_id": parts[1],
            "data": parts[2:]
        }
    except Exception:
        return None

def save_jsonl(data, output_path):
    with open(output_path, 'w') as f:
        for entry in data:
            json.dump(entry, f)
            f.write('\n')

def process_file(input_path):
    print(f"[INFO] Ingesting {input_path}...")
    frames = load_can_file(input_path)
    if not frames:
        print("[WARN] No frames parsed.")
        return
    fname = os.path.basename(input_path)
    session_id = fname.replace(" ", "_").split(".")[0]
    out_path = os.path.join(DATA_DIR, f"{session_id}.jsonl")
    save_jsonl(frames, out_path)
    print(f"[DONE] {len(frames)} frames → {out_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python can_ingest.py <path_to_log>")
        sys.exit(1)
    os.makedirs(DATA_DIR, exist_ok=True)
    process_file(sys.argv[1])
