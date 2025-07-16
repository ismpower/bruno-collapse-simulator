import os
import json
import scipy.io
import pandas as pd

folder = "CF-20-230"
full_path = os.path.join(os.getcwd(), folder)

for filename in os.listdir(full_path):
    file_path = os.path.join(full_path, filename)
    print(f"\n🔍 Processing: {filename}")

    if filename.endswith(".json"):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
                print(f"✅ JSON keys: {list(data.keys())}")
            except Exception as e:
                print(f"❌ Error loading JSON: {e}")

    elif filename.endswith(".csv"):
        try:
            df = pd.read_csv(file_path)
            print(f"✅ CSV shape: {df.shape}")
            print(df.head())
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")

    elif filename.endswith(".mat"):
        try:
            mat = scipy.io.loadmat(file_path)
            keys = [k for k in mat.keys() if not k.startswith("__")]
            print(f"✅ MAT keys: {keys}")
        except Exception as e:
            print(f"❌ Error reading MAT file: {e}")

    elif filename.endswith(".txt"):
        with open(file_path, "r") as f:
            lines = f.readlines()
            print(f"📄 TXT lines: {len(lines)}")
            print("Preview:", lines[:5])

    else:
        print("⚠️ Unknown format or skipped.")
