from gwosc.datasets import event_gps, find_datasets
from gwpy.timeseries import TimeSeries
import os

# Create data directory if not exists
os.makedirs("../data/gw_fresh_run", exist_ok=True)

# 1. Get list of available datasets and sort by most recent
datasets = find_datasets(type="event")
datasets = sorted(datasets, reverse=True)

# 2. Get the latest event and GPS time
latest_event = datasets[0]
gps_time = event_gps(latest_event)

print(f"📡 Latest LIGO event: {latest_event} (GPS: {gps_time})")

# 3. Fetch strain data (Hanford, 4s window)
strain = TimeSeries.fetch_open_data("H1", gps_time - 2, gps_time + 2, cache=True)

# 4. Save as ASCII
output_path = f"../data/gw_fresh_run/{latest_event.replace('/', '_')}_H1_strain.txt"
strain.write(output_path, format="txt")

print(f"✅ Strain data saved to: {output_path}")
if not datasets:
    print("❌ No GW events found. Try again later or check your connection.")
    exit()

