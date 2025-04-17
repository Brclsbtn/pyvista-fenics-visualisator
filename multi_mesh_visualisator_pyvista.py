import os
import sys
import h5py
import numpy as np
import pyvista as pv
import xml.etree.ElementTree as ET

from dolfin import Mesh, XDMFFile

# ========================
# USER CONFIGURATION
# ========================
main_folder = "EXT_TEMP"  # Change another other base directory (EXT: extension, COMP: compression - TEMP: temperature gradient variation, CF: friction coefficient variation)
variable = "strain_rate"  # Name of your variable file (without .h5 extension)

# ========================
# Get all parameter directories
parameters = [d for d in os.listdir(main_folder)
              if os.path.isdir(os.path.join(main_folder, d))]
parameters.sort()  # Ensure consistent order

# Get time steps from first parameter file
first_h5 = os.path.join(main_folder, parameters[0], f"{variable}.h5")
with h5py.File(first_h5, "r") as h5_file:
    time_steps = sorted(int(k) for k in h5_file["Mesh"].keys())

def load_mesh_data(h5_filename, time_step):
    """Load mesh data for a specific timestep"""
    with h5py.File(h5_filename, "r") as h5_file:
        return (
            np.array(h5_file[f"/Mesh/{time_step}/mesh/geometry"]),
            np.array(h5_file[f"/Mesh/{time_step}/mesh/topology"]),
            np.array(h5_file[f"/VisualisationVector/{time_step}"]).flatten()
        )

def load_paraview_colormap(xml_file):
    """Load ParaView colormap as a matplotlib colormap"""
    import matplotlib.colors as mcolors
    tree = ET.parse(xml_file)
    
    # Extract color points from XML
    color_points = []
    for p in tree.findall("ColorMap/Point"):
        x = float(p.get("x"))  # Position in the colormap (0 to 1)
        r = float(p.get("r"))
        g = float(p.get("g"))
        b = float(p.get("b"))
        color_points.append((x, (r, g, b)))
    
    # Create a matplotlib colormap
    return mcolors.LinearSegmentedColormap.from_list("custom_cmap", color_points)

def create_pyvista_mesh(nodes, elements, data):
    """Create a PyVista mesh from nodes, elements, and data"""
    # Convert 2D points to 3D by adding z=0 coordinate
    if nodes.shape[1] == 2:
        nodes_3d = np.zeros((nodes.shape[0], 3))
        nodes_3d[:, 0:2] = nodes
        nodes = nodes_3d
    
    # Create cells array for PyVista
    n_cells = elements.shape[0]
    
    # Create the cells array in the correct format
    cell_array = np.column_stack((
        np.full(n_cells, 3, dtype=np.int64),  # 3 points per cell
        elements
    )).flatten()
    
    # Create cell types array - all triangles (type 5)
    cell_types = np.full(n_cells, 5)  # 5 = VTK_TRIANGLE
    
    # Create the UnstructuredGrid with the correct constructor
    mesh = pv.UnstructuredGrid(cell_array, cell_types, nodes)
    
    # Check data length to determine if it's point data or cell data
    if len(data) == mesh.n_points:
        # It's point data
        mesh.point_data[variable] = data
    elif len(data) == mesh.n_cells:
        # It's cell data
        mesh.cell_data[variable] = data
    else:
        # Interpolate data if needed
        print(f"Warning: Data length ({len(data)}) doesn't match points ({mesh.n_points}) or cells ({mesh.n_cells})")
        # For visualization, we'll resize the data to match points
        resized_data = np.zeros(mesh.n_points)
        valid_indices = min(len(data), mesh.n_points)
        resized_data[:valid_indices] = data[:valid_indices]
        mesh.point_data[variable] = resized_data
    
    return mesh

# Calculate grid dimensions based on number of parameters
if len(parameters) <= 4:
    n_cols = 2
    n_rows = 2
elif len(parameters) <= 6:
    n_cols = 3
    n_rows = 2
else:
    n_cols = 3
    n_rows = (len(parameters) + 2) // 3

# Set global theme for minimal spacing
pv.global_theme.multi_rendering_splitting_position = 0.95

# Create plotter with optimized settings
plotter = pv.Plotter(
    shape=(n_rows, n_cols),
    border=False,
    window_size=[1600, 1200],
    row_weights=[1] * n_rows,
    col_weights=[1] * n_cols
)

# After creating all subplots, adjust the layout
plotter.subplot(0, 0)  # Reset to first subplot

def calculate_precise_scalar_bar_positions(n_rows, n_cols, window_size):
    """Calculate precise scalar bar positions based on window size."""
    width, height = window_size
    subplot_width = width / n_cols
    subplot_height = height / n_rows
    
    scalar_bar_args_list = []
    
    for idx in range(n_rows * n_cols):
        try:
            row = idx // n_cols
            col = idx % n_cols
            
            # Calculate upper left corner of this subplot in pixels
            x = col * subplot_width
            y = height - (row + 1) * subplot_height  # Invert y-axis for upper left corner
            
            # Normalize to [0, 1] range for PyVista (coordinated begin from center)
            if idx ==0:
                position_x = (x + subplot_width * 0.7) / width # Position at 70% of subplot width
                position_y = (y + subplot_height * -0.9) / height  # Position at -90% of subplot height
            elif idx ==1:
                position_x = (x - subplot_width * 0.3) / width # Position at 70% of subplot width
                position_y = (y + subplot_height * -0.9) / height  # Position at -90% of subplot height
            elif idx ==2:
                position_x = (x + subplot_width * 0.7) / width # Position at 70% of subplot width
                position_y = (y + subplot_height * 0.1) / height  # Position at -90% of subplot height
            elif idx ==3:
                position_x = (x - subplot_width * 0.3) / width # Position at 70% of subplot width
                position_y = (y + subplot_height * 0.1) / height  # Position at -90% of subplot height
            
            scalar_bar_args = {
                "title": f"{variable.capitalize().replace('_', ' ')} - {parameters[idx]}",  # Add unique identifier
                "position_x": position_x,
                "position_y": position_y,
                "width": 0.3,
                "height": 0.1,
                "n_labels": 3,
                "title_font_size": 16,
                "label_font_size": 12,
                "font_family": "arial",
                "fmt": "%.2f",
                "color": "black"
            }
            
            scalar_bar_args_list.append(scalar_bar_args)
        except:
            continue
    
    return scalar_bar_args_list

# Calculate precise scalar bar positions
scalar_bar_args_list = calculate_precise_scalar_bar_positions(n_rows, n_cols, [1600, 1200])

# Store meshes and metadata for each parameter
meshes = []
current_step = time_steps[0]
text_actors = [None] * (n_rows * n_cols)  # Track text actors for each subplot

# Load colormap
cmap = load_paraview_colormap("w_ymiddle1.xml")

# In the initial visualization loop:
for idx, param in enumerate(parameters):
    if idx >= n_rows * n_cols:
        print(f"Warning: Not enough subplot space for parameter {param}. Skipping.")
        continue
        
    # Calculate row and column for the subplot
    row = idx // n_cols
    col = idx % n_cols
    
    plotter.subplot(row, col)
    
    h5_path = os.path.join(main_folder, param, f"{variable}.h5")
    
    # Load initial data
    nodes, elements, data = load_mesh_data(h5_path, current_step)
    
    # Create mesh
    mesh = create_pyvista_mesh(nodes, elements, data)
    
    # Store mesh info
    meshes.append({
        "mesh": mesh,
        "h5_path": h5_path,
        "actor": None
    })
    
    # Use subplot-specific scalar bar arguments
    meshes[idx]["actor"] = plotter.add_mesh(
        mesh,
        scalars=variable,
        cmap=cmap,
        show_edges=True,
        line_width=1,
        scalar_bar_args=scalar_bar_args_list[idx],  # Use specific scalar bar args
        preference='cell'
    )
    
    # Optimize camera view
    plotter.camera_position = 'xy'
    plotter.reset_camera()
    plotter.camera.zoom(1.5*(2/n_cols))
    
    # Add mesh to plotter with text
    text_actors[idx] = plotter.add_text(f"{param} - Step {current_step}", position=(310, 420), font_size=10)

    # Add this after your text_actors definition
    bounds_actors = [None] * (n_rows * n_cols)  # Track bounds actors for each subplot

    # Get the bounds of the mesh
    mesh_bounds = mesh.bounds
    
    # Create custom axes ranges, ensuring y starts at a small positive value
    axes_ranges = [
        mesh_bounds[0], mesh_bounds[1],  # x min, x max
        0.001, mesh_bounds[3],           # y min, y max (force y min to be positive)
        mesh_bounds[4], mesh_bounds[5]   # z min, z max
    ]

    # In the initial visualization loop, store the bounds actor reference:
    bounds_actors[idx] = plotter.show_bounds(
        mesh,
        grid='front',
        location='outer',
        ticks='outside',
        n_xlabels=0,
        n_ylabels=6,
        n_zlabels=0,
        ytitle='Altitude (m)',
        show_zaxis=False,
        show_xaxis=False,
        font_size=10,
        color='black',
        fmt='%.0f',
        axes_ranges=axes_ranges
    )

def update_step(step):
    for idx, mesh_data in enumerate(meshes):
        if idx >= n_rows * n_cols:
            continue
            
        # Calculate row and column for the subplot
        row = idx // n_cols
        col = idx % n_cols
        
        plotter.subplot(row, col)
        
        # Load new data
        nodes, elements, data = load_mesh_data(mesh_data["h5_path"], step)
        
        # Create new mesh
        new_mesh = create_pyvista_mesh(nodes, elements, data)
        
        # Remove all bounds axes at the beginning
        plotter.remove_bounds_axes()
        # Remove old mesh
        plotter.remove_actor(mesh_data["actor"])
        
        # Remove old bounds actor
        if bounds_actors[idx] is not None:
            plotter.remove_actor(bounds_actors[idx])
            bounds_actors[idx] = None
        
        # Add new mesh
        mesh_data["mesh"] = new_mesh
        mesh_data["actor"] = plotter.add_mesh(
            new_mesh,
            scalars=variable,
            cmap=cmap,
            show_edges=True,
            line_width=1,
            scalar_bar_args=scalar_bar_args_list[idx],  # Use specific scalar bar args
            preference='cell'
        )

        # Get the bounds of the mesh
        new_mesh_bounds = new_mesh.bounds

        # Create custom axes ranges, ensuring y starts at a small positive value
        new_axes_ranges = [
            new_mesh_bounds[0], new_mesh_bounds[1],  # x min, x max
            0.001, new_mesh_bounds[3],           # y min, y max (force y min to be positive)
            new_mesh_bounds[4], new_mesh_bounds[5]   # z min, z max
        ]
        
        # Add new bounds actor and store reference
        bounds_actors[idx] = plotter.show_bounds(
            new_mesh,
            grid='front',
            location='outer',
            ticks='outside',
            n_xlabels=0,
            n_ylabels=6,
            n_zlabels=0,
            ytitle='Altitude',
            show_zaxis=False,
            show_xaxis=False,
            font_size=10,
            color='black',
            fmt='%.0f',
            axes_ranges=new_axes_ranges
        )
        
        # Optimize camera view
        plotter.camera_position = 'xy'
        plotter.reset_camera()
        plotter.camera.zoom(1.5)
        
        # Remove old text and add new one
        if text_actors[idx] is not None:
            plotter.remove_actor(text_actors[idx])
        
        param_name = os.path.basename(os.path.dirname(mesh_data["h5_path"]))
        text_actors[idx] = plotter.add_text(f"{param_name} - Step {step}", position=(310, 420), font_size=10)
    
    # Force garbage collection after updates
    import gc
    gc.collect()
    
    plotter.render()

def next_step_callback():
    global current_step
    step_idx = time_steps.index(current_step)
    if step_idx < len(time_steps) - 1:
        current_step = time_steps[step_idx + 1]
        update_step(current_step)

def prev_step_callback():
    global current_step
    step_idx = time_steps.index(current_step)
    if step_idx > 0:
        current_step = time_steps[step_idx - 1]
        update_step(current_step)

plotter.add_key_event("Right", next_step_callback)
plotter.add_key_event("Left", prev_step_callback)

# Add instructions
plotter.add_text(
    "Use Left/Right arrow keys to navigate time steps",
    position="lower_left",
    font_size=12,
    color="black"
)

# Show the plotter
plotter.show()
