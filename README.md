# Multi-Mesh Visualisator with PyVista

This script provides an interactive visualization tool for comparing multiple finite element simulation results (such as strain rate fields) across different parameter sets and time steps. It leverages PyVista for rendering, h5py for reading simulation data, and supports custom colormaps imported from ParaView XML files.

## Features

- Visualize multiple simulation results in a grid layout for side-by-side comparison.
- Interactive navigation through time steps using keyboard arrows.
- Automatic detection of parameter sets and time steps from directory structure and HDF5 files.
- Customizable colormaps via ParaView XML.
- Annotated subplots with parameter names and time step indicators.
- Scalar bars with precise positioning and custom formatting.
- Supports both point and cell data for mesh coloring.


## Requirements

- Python 3.x
- [PyVista](https://docs.pyvista.org/)
- [h5py](https://www.h5py.org/)
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/) (for colormap handling)
- [dolfin](https://fenicsproject.org/) (for mesh handling, optional)
- HDF5 simulation output files organized by parameter set


## Directory Structure

```
EXT_TEMP/
  param_set_1/
    strain_rate.h5
  param_set_2/
    strain_rate.h5
  ...
w_ymiddle1.xml  # ParaView colormap XML
```

- `EXT_TEMP/` is the main folder containing subdirectories for each parameter set.
- Each parameter directory contains an HDF5 file (e.g., `strain_rate.h5`) with simulation results.
- The XML file defines the colormap used for visualization.


## Usage

1. **Configure the script:**
    - Set the `main_folder` variable to your main results directory (default: `"EXT_TEMP"`).
    - Set the `variable` to the base name of your HDF5 result files (e.g., `"strain_rate"`).
    - Ensure the colormap XML file (e.g., `w_ymiddle1.xml`) is present.
2. **Run the script:**

```bash
python multi_mesh_visualisator_pyvista.py
```

3. **Interact with the visualization:**
    - Use the **Left** and **Right** arrow keys to navigate through available time steps.
    - Each subplot displays the mesh for a different parameter set, colored by the selected variable.
    - Scalar bars and labels help interpret the results.

## Script Overview

- **Parameter and Time Step Detection:**
The script scans the main results folder for parameter subdirectories and extracts available time steps from the first HDF5 file.
- **Data Loading:**
Mesh geometry, topology, and variable data are loaded for each parameter set and time step.
- **Mesh Construction:**
Meshes are built using PyVista's `UnstructuredGrid`, supporting both 2D and 3D data.
- **Colormap Loading:**
Custom colormaps are imported from ParaView XML files and converted for use with matplotlib and PyVista.
- **Grid Layout:**
The number of rows and columns is determined automatically based on the number of parameter sets.
- **Interactive Navigation:**
Keyboard events allow users to step forward and backward in time, updating all subplots simultaneously.
- **Annotations:**
Each subplot is labeled with the parameter set and current time step. Scalar bars are positioned precisely for clarity.


## Customization

- **Change the Main Folder or Variable:**
Edit the `main_folder` and `variable` variables at the top of the script.
- **Colormap:**
Replace `"w_ymiddle1.xml"` with your own ParaView colormap XML file as needed.
- **Grid Layout:**
The script automatically adjusts the grid, but you can modify the logic for custom layouts.


## Troubleshooting

- **Data Shape Mismatch:**
If the variable data does not match the number of mesh points or cells, the script attempts to interpolate or resize the data for visualization.
- **Missing Files:**
Ensure all required HDF5 files and the colormap XML are present in the correct locations.
- **Dependencies:**
Install missing Python packages using pip:

```bash
pip install pyvista h5py numpy matplotlib
```


## License

This script is provided as-is for research and educational purposes.

---

**Author:**
Quentin BETTON - Nantes Université (FRANCE)
**Date:** April 2025

---

*For questions or contributions, please open an issue or submit a pull request.*

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/50658283/1965e02f-f695-44d1-a85b-c69940c1c0a0/2.multi_mesh_visualisator_pyvista.py

