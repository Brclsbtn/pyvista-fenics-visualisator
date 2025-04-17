import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

BASE_PATH = "./"

def get_hdf5_data(h5_filename, time_step):
    """Loads mesh data for a specific time step."""
    with h5py.File(h5_filename, "r") as h5_file:
        node_coords = np.array(h5_file[f"/Mesh/{time_step}/mesh/geometry"])
        element_connectivity = np.array(h5_file[f"/Mesh/{time_step}/mesh/topology"])  
        h5datafile_data = np.array(h5_file[f"/VisualisationVector/{time_step}"]).flatten()
    return node_coords, element_connectivity, h5datafile_data

def bin_and_average(y_values, data_values, bin_size=200):
    """Bins y-values and computes the average intensity per bin."""
    min_y, max_y = np.min(y_values), np.max(y_values)
    bins = np.arange(min_y, max_y + bin_size, bin_size)
    avg_y, avg_data = [], []

    for i in range(len(bins) - 1):
        mask = (y_values >= bins[i]) & (y_values < bins[i + 1])
        indices = np.where(mask)[0]
        if len(indices) > 0:
            avg_y.append(np.mean(y_values[indices]))
            avg_data.append(np.mean(data_values[indices]))
    
    return np.array(avg_y), np.array(avg_data)

def plot_on_axis(files, data_type, ax, file_label, subplot_index):
    """Plots results on a specified axis."""
    styles = ['-', '--', '-.', ':', (0, (3, 5, 1, 5))]
    colors = ['tab:blue', 'tab:orange', 'g', 'r', 'tab:purple']
    
    for idx, file in enumerate(files):
        with h5py.File(file, "r") as h5_file:
            time_steps = sorted(int(k) for k in h5_file["Mesh"].keys())

        for j, step in enumerate(time_steps):
            # Select appropriate time step
            if data_type == "CF" and j != 8:
                continue
            if data_type == "TEMP" and j != 10:
                continue

            nodes, elements, h5datafile = get_hdf5_data(file, step)
            y_values = np.mean(nodes[elements, 1], axis=1)
            avg_y, avg_values = bin_and_average(y_values, abs(h5datafile))

            if len(avg_y) < 2:
                continue

            try:
                spline = make_interp_spline(avg_y, avg_values)
                X_ = np.linspace(avg_y.min(), avg_y.max(), 500)
                Y_ = spline(X_)
            except:
                X_, Y_ = avg_y, avg_values

            ax.plot(Y_, X_, 
                    label=os.path.basename(os.path.dirname(file)),
                    linestyle=styles[idx % len(styles)],
                    color=colors[idx % len(colors)])

    file_label_to_unit = {
    "Viscosity": "(Pa.s)",
    "Velocity": "(m/s)"
    }

    unit = file_label_to_unit.get(file_label, "")


    ax.set_xlabel(f"Averaged {file_label}\n{unit}")
    ax.set_ylabel("Altitude (m)")
    ax.legend(loc='best')
    ax.grid(True)
    # ax.set_title(f"{file.split("/")[-3]} - {file.split("/")[-2]}")
    # Add letter index in the top-left corner of the plot
    ax.text(-0.1, 1.05, f"{chr(97 + subplot_index)}.", transform=ax.transAxes,
            fontsize=14, fontweight='bold', va='center', ha='center')

def main():
    # Define parameters and their components
    parameters = [
        ("COMP_CF", "CF", ["mechanisms.h5", "velocity.h5"]),
        ("COMP_TEMP", "TEMP", ["mechanisms.h5", "viscosity.h5"]),
        ("EXT_CF", "CF", ["mechanisms.h5", "viscosity.h5"]),
        ("EXT_TEMP", "TEMP", ["mechanisms.h5", "plastic_strain.h5"])
    ]

    fig, axs = plt.subplots(2, 4, figsize=(11, 8))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    subplot_index = 0  # Counter for subplot letter indices

    for i, (param, data_type, files) in enumerate(parameters):
        row = i // 2
        start_col = (i % 2) * 2
        
        for j, h5_file in enumerate(files):
            col = start_col + j
            ax = axs[row, col]
            param_path = os.path.join(BASE_PATH, param)
            
            # Collect all available folders
            folders = [f for f in os.listdir(param_path) 
                      if os.path.isdir(os.path.join(param_path, f))]
            
            # Build full file paths
            file_paths = [os.path.join(param_path, folder, h5_file) 
                         for folder in folders 
                         if os.path.exists(os.path.join(param_path, folder, h5_file))]
            
            if file_paths:
                plot_on_axis(file_paths, data_type, ax, h5_file[:-3].capitalize().replace('_', ' '), subplot_index)
                subplot_index += 1
            else:
                ax.axis('off')
                print(f"Missing data for {param}/{h5_file}")

    plt.tight_layout()
    plt.savefig("Figures/subplots.pgf")

if __name__ == "__main__":
    main()
