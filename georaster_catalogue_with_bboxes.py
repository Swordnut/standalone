import os
import csv
import uuid
from queue import Queue
from threading import Thread
from osgeo import gdal
import geopandas as gpd
from shapely.geometry import Polygon
from pyproj import CRS
import tkinter as tk
from tkinter import filedialog, ttk
from concurrent.futures import ThreadPoolExecutor

# Enable GDAL exceptions to handle errors properly
gdal.UseExceptions()

def log_message(log_queue, message):
    """Add a message to the log queue."""
    log_queue.put(message)

def log_updater(log_box, log_queue):
    """Update log messages from the queue."""
    while not log_queue.empty():
        message = log_queue.get()
        log_box.config(state=tk.NORMAL)
        log_box.insert(tk.END, message + "\n")
        log_box.config(state=tk.DISABLED)
        log_box.see(tk.END)
    root.after(100, log_updater, log_box, log_queue)

def should_skip_folder(folder_name):
    """Check if a folder should be skipped based on its name."""
    skip_keywords = ["admin", "archiving"] # alter this list with your own keywords to ignore
    if folder_name.lower() in skip_keywords or folder_name.lower().startswith("00000"):
        return True
    return False

def process_rasters_parallel(input_folder, output_gpkg_base, output_crs, default_crs, search_subfolders, log_queue):
    """Catalog and process raster files in parallel."""
    raster_files = []
    extensions = [".tif", ".png"]

    def discover_files():
        """Discover files recursively or in a single folder."""
        for root_dir, dirs, files in os.walk(input_folder):
            # Skip specified folders
            dirs[:] = [d for d in dirs if not should_skip_folder(d)]
            if should_skip_folder(os.path.basename(root_dir)):
                log_message(log_queue, f"Skipping folder and subfolders: {root_dir}")
                continue

            # Filter raster files
            relevant_files = [os.path.join(root_dir, f) for f in files if os.path.splitext(f)[1].lower() in extensions]
            if relevant_files:
                raster_files.extend(relevant_files)
                log_message(log_queue, f"Discovered folder with files: {root_dir}")
            else:
                log_message(log_queue, f"No relevant files found in folder: {root_dir}")

    def process_file(file):
        """Process a single raster file."""
        try:
            dataset = gdal.Open(file)
            if dataset is None:
                raise ValueError(f"Unsupported file format for {file}")

            corners = get_corner_coords(dataset)

            # Check for georeferenced rasters
            if corners[0][0] == 0 or corners[2][1] == 0:
                raise ValueError(f"Non-georeferenced raster: {file}")

            prj_file = file.replace(os.path.splitext(file)[1], ".prj")
            crs = get_crs_from_prj(prj_file) if os.path.isfile(prj_file) else "N/A"

            return {
                "filepath": os.path.normpath(file),
                "filename": os.path.basename(file),
                "crs": crs,
                "minx": corners[0][0],
                "miny": corners[0][1],
                "maxx": corners[2][0],
                "maxy": corners[2][1],
                "geometry": Polygon(corners),
            }
        except Exception as e:
            log_message(log_queue, f"Error processing {file}: {e}")
            return None

    def save_results(data, unique_id):
        """Save processed data to GeoPackage."""
        if not data:
            return
        gdf = gpd.GeoDataFrame(data, geometry="geometry", crs=output_crs or default_crs)
        output_gpkg = f"{output_gpkg_base}_{unique_id}.gpkg"
        gdf.to_file(output_gpkg, driver="GPKG")
        log_message(log_queue, f"Saved results to {output_gpkg}")

    # Discover files and process them in parallel
    log_message(log_queue, "Starting discovery...")
    discover_files()
    log_message(log_queue, f"Discovered {len(raster_files)} files.")

    batch_size = 50  # Process files in batches for efficiency
    processed_data = []
    errors = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, file) for file in raster_files]
        for i, future in enumerate(futures):
            result = future.result()
            if result:
                processed_data.append(result)
            if (i + 1) % batch_size == 0 or i == len(futures) - 1:
                # Save batch results
                save_results(processed_data, str(uuid.uuid4())[:8])
                processed_data.clear()

    log_message(log_queue, "Processing complete!")

def get_corner_coords(dataset):
    """Retrieve bounding box corner coordinates from a GDAL dataset."""
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    gt = dataset.GetGeoTransform()

    if gt is None:
        raise ValueError("No geotransformation available.")

    minx = gt[0]
    miny = gt[3] + width * gt[4] + height * gt[5]
    maxx = gt[0] + width * gt[1] + height * gt[2]
    maxy = gt[3]
    return [(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)]

def get_crs_from_prj(prj_file):
    """Extract CRS from a .prj file using pyproj."""
    with open(prj_file, "r") as file:
        prj_content = file.read()
    try:
        crs = CRS.from_string(prj_content)
        return crs.to_string()
    except Exception as e:
        return f"ERROR parsing CRS: {e}"

def start_processing(input_folder, output_gpkg_base, output_crs, default_crs, search_subfolders, log_box):
    """Start processing workflow."""
    log_queue = Queue()
    log_updater(log_box, log_queue)

    def processing():
        process_rasters_parallel(
            input_folder, output_gpkg_base, output_crs, default_crs, search_subfolders, log_queue
        )

    Thread(target=processing).start()

# Main UI Window
root = tk.Tk()
root.title("Raster Processing Tool")
root.geometry("600x600")

# Input Folder Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10, padx=10, fill="x")
tk.Label(input_frame, text="Input Folder:").grid(row=0, column=0, sticky="w")
input_folder_var = tk.StringVar()
tk.Entry(input_frame, textvariable=input_folder_var, width=50).grid(row=0, column=1, padx=5)
tk.Button(input_frame, text="Browse", command=lambda: input_folder_var.set(filedialog.askdirectory())).grid(row=0, column=2)

# Output File Frame
output_frame = tk.Frame(root)
output_frame.pack(pady=10, padx=10, fill="x")
tk.Label(output_frame, text="Output file:").grid(row=0, column=0, sticky="w")
output_gpkg_var = tk.StringVar()
tk.Entry(output_frame, textvariable=output_gpkg_var, width=50).grid(row=0, column=1, padx=5)
tk.Button(output_frame, text="Browse", command=lambda: output_gpkg_var.set(filedialog.asksaveasfilename(defaultextension=".gpkg", filetypes=[("GeoPackage files", "*.gpkg")]))).grid(row=0, column=2)

# CRS Selection Frame
crs_frame = tk.Frame(root)
crs_frame.pack(pady=10, padx=10, fill="x")
tk.Label(crs_frame, text="Select CRS:").grid(row=0, column=0, sticky="w")
selected_crs = tk.StringVar(value="EPSG:27700")
crs_options = ["EPSG:27700 - OSGB 1936", "EPSG:3857 - WGS 84 / Pseudo-Mercator", "EPSG:4326 - WGS 84"]
tk.OptionMenu(crs_frame, selected_crs, *crs_options).grid(row=0, column=1, padx=5)

custom_crs_entry = tk.Entry(crs_frame, width=15)
custom_crs_entry.insert(0, "Custom EPSG Code")
custom_crs_entry.grid(row=0, column=2, padx=5)

# Subfolder Checkbox
search_subfolders_var = tk.BooleanVar()
tk.Checkbutton(root, text="Include Subfolders", variable=search_subfolders_var).pack()

# Buttons Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
tk.Button(button_frame, text="Start Processing", command=lambda: start_processing(
    input_folder_var.get(),
    output_gpkg_var.get(),
    selected_crs.get().split(" ")[0],
    "EPSG:27700",
    search_subfolders_var.get(),
    log_box,
)).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Close", command=root.destroy).grid(row=0, column=1, padx=5)

# Log Frame
log_frame = tk.Frame(root)
log_frame.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(log_frame, text="Log:").pack(anchor="w")
log_box = tk.Text(log_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
log_box.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar = tk.Scrollbar(log_frame, command=log_box.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
log_box.config(yscrollcommand=scrollbar.set)

root.mainloop()
