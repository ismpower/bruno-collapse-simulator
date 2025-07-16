#!/usr/bin/env python

from gwosc.datasets import event_gps, find_datasets
from gwpy.timeseries import TimeSeries
import numpy as np
import os

# Create output folder
data_dir = "../data/gw_fresh_run"
os.makedirs(data_dir, exist_ok=True)

# Fetch the latest GW event
events = find_datasets(type="event")
events = sorted(events, reverse=True)
latest_event = events[0]
gps_time = event_gps(latest_event)

print(f"📡 Downloading: {latest_event} (GPS: {gps_time})")

# Fetch 4 seconds of strain data from both detectors
try:
    h1 = TimeSeries.fetch_open_data("H1", gps_time - 2, gps_time + 2, cache=True)
    l1 = TimeSeries.fetch_open_data("L1", gps_time - 2, gps_time + 2, cache=True)
except Exception as e:
    print(f"❌ Failed to fetch data: {e}")
    exit(1)

# Align time series (resample if needed)
common_times = h1.times.value  # assume same sampling rate

# If L1 is misaligned, resample to match H1
if not np.allclose(l1.times.value, common_times):
    print("⚠️ Resampling L1 to match H1 timebase")
    l1 = l1.interpolate(h1.times)

# Export to CSV
csv_file = f"{data_dir}/{latest_event.replace('/', '_')}_H1_L1.csv"
with open(csv_file, "w") as f:
    f.write("time,strain_H1,strain_L1\n")
    for t, s1, s2 in zip(common_times, h1.value, l1.value):
        f.write(f"{t},{s1},{s2}\n")

print(f"✅ Dual-detector CSV saved to: {csv_file}")
