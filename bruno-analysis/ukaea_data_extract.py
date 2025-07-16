import json
import requests
import os

# === CONFIG ===
json_path = "collection_20224.json"  # Change to any other collection_*.json
output_dir = "ukaea_downloads"       # Where files will be saved

# === SETUP ===
os.makedirs(output_dir, exist_ok=True)

# === LOAD JSON ===
with open(json_path, "r") as f:
    data = json.load(f)

# === EXTRACT AND DOWNLOAD ===
for fig in data.get("figures", []):
    urls = [fig.get("figure")] + fig.get("data", [])
    for url in urls:
        if not url:
            continue
        fname = url.split("/")[-1]
        out_path = os.path.join(output_dir, fname)

        try:
            r = requests.get(url)
            r.raise_for_status()
            with open(out_path, "wb") as f:
                f.write(r.content)
            print(f"✅ Downloaded: {fname}")
        except Exception as e:
            print(f"❌ Failed: {fname} ({e})")
