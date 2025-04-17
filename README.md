<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Finite Element Simulation Visualization Tools

This repository contains two Python scripts for advanced visualization and analysis of finite element simulation results stored in HDF5 files. The tools are designed for side-by-side comparison and detailed plotting of simulation data, supporting both 2D and 3D mesh data.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Directory Structure](#directory-structure)
- [Usage](#usage)
    - [1. Multi-Mesh Visualisator (PyVista)](#1-multi-mesh-visualisator-pyvista)
    - [2. Diagram Subplot Maker (Matplotlib)](#2-diagram-subplot-maker-matplotlib)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

This project provides two main scripts:


| Script | Purpose |
| :-- | :-- |
| `multi_mesh_visualisator_pyvista.py` | Interactive 2D/3D mesh visualization and comparison across multiple parameter sets and time steps using PyVista. |
| `diagram_subplot_maker.py` | Automated generation of comparative subplots (using Matplotlib) for binned and averaged simulation data. |

Both scripts are designed for scientific visualization of simulation results, making it easy to compare the effects of different parameters or time steps.

---

## Features

- **Batch visualization** of multiple parameter sets and time steps.
- **Interactive navigation** (keyboard controls) for time-stepping in mesh visualizations.
- **Support for custom colormaps** (imported from ParaView XML).
- **Automated subplot grid creation** for comparative diagrams.
- **Flexible and easily configurable parameters** at the top of each script.
- **Support for both point and cell data** in mesh files.
- **Export of figures** for publication-quality graphics.

---

## Requirements

- Python 3.x
- [PyVista](https://docs.pyvista.org/) (`multi_mesh_visualisator_pyvista.py`)
- [h5py](https://www.h5py.org/)
- [numpy](https://numpy.org/)
- [matplotlib](https://matplotlib.org/) (`diagram_subplot_maker.py`)
- [scipy](https://scipy.org/) (`diagram_subplot_maker.py`)
- [dolfin](https://fenicsproject.org/) (optional, for mesh handling in PyVista script)
- HDF5 simulation output files organized by parameter set

Install dependencies with:

```bash
pip install pyvista h5py numpy matplotlib scipy
```

---

## Directory Structure

```
project_root/
│
├── EXT_TEMP/
│   ├── param_set_1/
│   │   └── strain_rate.h5
│   ├── param_set_2/
│   │   └── strain_rate.h5
│   └── ...
├── COMP_CF/
│   └── ...
├── COMP_TEMP/
│   └── ...
├── EXT_CF/
│   └── ...
├── EXT_TEMP/
│   └── ...
├── w_ymiddle1.xml          # ParaView colormap XML (for PyVista script)
├── multi_mesh_visualisator_pyvista.py
├── diagram_subplot_maker.py
└── Figures/                # Output directory for figures (created by scripts)
```

---

## Usage

### 1. Multi-Mesh Visualisator (PyVista)

**Purpose:**
Compare and interactively explore multiple simulation results (meshes and fields) across parameter sets and time steps.

**Configuration:**
At the top of `multi_mesh_visualisator_pyvista.py`, set:

```python
main_folder = "EXT_TEMP"     # Directory containing parameter folders
variable = "strain_rate"     # Name of variable to visualize (without .h5 extension)
```

**Run the script:**

```bash
python multi_mesh_visualisator_pyvista.py
```

**Controls:**

- Use **Left/Right arrow keys** to navigate through available time steps.
- Each subplot displays a different parameter set, colored by the selected variable.
- Scalar bars, axis labels, and parameter/time annotations are included.

**Colormap:**
Place your ParaView XML colormap (e.g., `w_ymiddle1.xml`) in the project root.

---

### 2. Diagram Subplot Maker (Matplotlib)

**Purpose:**
Generate comparative subplots of binned and averaged simulation variables (e.g., viscosity, velocity) as a function of altitude or other mesh properties.

**Configuration:**
At the top of `diagram_subplot_maker.py`, set the `parameters` list and `BASE_PATH`:

```python
BASE_PATH = "./"

parameters = [
    ("COMP_CF", "CF", ["mechanisms.h5", "velocity.h5"]),
    ("COMP_TEMP", "TEMP", ["mechanisms.h5", "viscosity.h5"]),
    ("EXT_CF", "CF", ["mechanisms.h5", "viscosity.h5"]),
    ("EXT_TEMP", "TEMP", ["mechanisms.h5", "plastic_strain.h5"])
]
```

**Run the script:**

```bash
python diagram_subplot_maker.py
```

**Output:**
Saves a figure (`subplots.pgf`) in the `Figures/` directory, showing comparative plots for each parameter and variable.

---

## Customization

- **Parameters:**
Edit the `parameters` list at the top of each script to specify which parameter sets, data types, and HDF5 files to process.
- **Main Folder/Variable:**
Adjust `main_folder` and `variable` in the PyVista script as needed.
- **Colormap:**
Replace or modify the XML colormap file for different color schemes in PyVista visualizations.
- **Plot Appearance:**
Adjust Matplotlib or PyVista settings within the scripts for custom figure sizes, labels, or styles.

---

## Troubleshooting

- **Missing Files:**
Ensure all specified HDF5 files and the colormap XML are present in the correct locations.
- **Data Shape Mismatch:**
The scripts attempt to handle mismatches between mesh and data shapes, but check your data if warnings appear.
- **Dependencies:**
Install all required Python packages as listed above.

---

## License

This project is provided as-is for research and educational purposes.

---

**Author:**
Quentin BETTON - Nantes Université (FRANCE)
**Date:** April 2025

---

## Acknowledgments

- Developed with [PyVista](https://docs.pyvista.org/), [Matplotlib](https://matplotlib.org/), and [h5py](https://www.h5py.org/).
- Colormap support via ParaView XML.

---

*For issues, suggestions, or contributions, please open an issue or submit a pull request.*

<div style="text-align: center">⁂</div>

[^1]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/50658283/73852cbd-a69c-40d5-8194-4daf86d18806/diagram_subplot_maker.py

[^2]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/50658283/4232b6ef-ea0b-4e67-a102-63454f08e60d/multi_mesh_visualisator_pyvista.py

[^3]: https://codingnomads.com/python-101-documentation-readme

[^4]: https://hackernoon.com/how-to-create-an-engaging-readme-for-your-data-science-project-on-github

[^5]: https://packaging.python.org/guides/making-a-pypi-friendly-readme/

[^6]: https://ubc-library-rc.github.io/rdm/content/03_create_readme.html

[^7]: https://www.makeareadme.com

[^8]: https://realpython.com/readme-python-project/

[^9]: https://github.com/kwaldenphd/interactive-visualization-python/blob/main/README.md

[^10]: https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/

[^11]: https://github.com/Atefeh97hmt/PythonPlottingExamples/blob/main/README.md

[^12]: https://geo-python.github.io/site/notebooks/L4/writing-scripts.html

[^13]: https://github.com/jmv74211/matplotlib/blob/master/README.md

[^14]: https://dev.to/documatic/how-to-write-an-awesome-readme-cfl

[^15]: https://matplotlib.org/stable/gallery/index.html

[^16]: https://github.com/PacktPublishing/Data-visualization-projects-in-python/blob/master/README.md

[^17]: https://pbpython.com/best-practices.html

[^18]: https://dev.to/scottydocs/how-to-write-a-kickass-readme-5af9

[^19]: https://github.com/sfbrigade/data-science-wg/blob/master/dswg_project_resources/Project-README-template.md

[^20]: https://cosmologist.info/cosmomc/readme_python.html

[^21]: https://prosem.genisys-gmbh.com/scripts-plot-basics.html

[^22]: https://www.youtube.com/watch?v=4ATucrptdYA
