import h5py
import os

file_path = "20ja074_fig01b_data.h5"  # ✅ local path only

if os.path.exists(file_path):
    with h5py.File(file_path, "r") as h5_file:
        def print_structure(name, obj):
            print(name, "->", type(obj))
        print("\n📁 HDF5 File Structure:\n")
        h5_file.visititems(print_structure)
else:
    print("❌ File not found:", file_path)
