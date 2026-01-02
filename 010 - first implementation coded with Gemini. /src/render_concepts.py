import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
import json
import os
import glob
import sys

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

def render_concept(stl_path, strategy_path, output_path):
    print(f"Processing {strategy_path}...")
    
    # Load strategy
    with open(strategy_path, 'r') as f:
        strategy = json.load(f)
    
    colors = [
        strategy['palette']['Color 1']['hex'],
        strategy['palette']['Color 2']['hex'],
        strategy['palette']['Color 3']['hex'],
        strategy['palette']['Color 4']['hex']
    ]
    rgb_colors = [hex_to_rgb(c) for c in colors]

    # Load mesh
    mesh = trimesh.load(stl_path)
    
    # Simplify mesh for matplotlib performance (target ~5000 faces)
    simplified_mesh = None
    try:
        if len(mesh.faces) > 5000:
            print(f"Simplifying mesh from {len(mesh.faces)} faces...")
            # correct method name: simplify_quadric_decimation
            simplified_mesh = mesh.simplify_quadric_decimation(5000)
    except Exception as e:
        print(f"Simplification failed ({e}). Falling back to point cloud.")
        simplified_mesh = None

    if simplified_mesh:
        mesh = simplified_mesh
        # Re-calculate centroids for the new mesh
        z_centroids = mesh.triangles_center[:, 2]
        face_colors = np.zeros((len(mesh.faces), 3))
        # ... segmentation logic for faces ...
        z_min, z_max = z_centroids.min(), z_centroids.max()
        height = z_max - z_min
        section_height = height / 4.0
        
        for i in range(4):
            z_lower = z_min + (i * section_height)
            z_upper = z_min + ((i + 1) * section_height)
            if i == 3: mask = (z_centroids >= z_lower)
            else: mask = (z_centroids >= z_lower) & (z_centroids < z_upper)
            face_colors[mask] = rgb_colors[i % 4]
            
        render_mode = 'mesh'
    else:
        render_mode = 'points'
        # Sample points
        points, _ = trimesh.sample.sample_surface(mesh, 10000)
        z_points = points[:, 2]
        point_colors = np.zeros((len(points), 3))
        
        z_min, z_max = z_points.min(), z_points.max()
        height = z_max - z_min
        section_height = height / 4.0

        for i in range(4):
            z_lower = z_min + (i * section_height)
            z_upper = z_min + ((i + 1) * section_height)
            if i == 3: mask = (z_points >= z_lower)
            else: mask = (z_points >= z_lower) & (z_points < z_upper)
            point_colors[mask] = rgb_colors[i % 4]

    # Render with Matplotlib
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    if render_mode == 'mesh':
        # Create Poly3DCollection
        poly3d = art3d.Poly3DCollection(mesh.vectors, linewidths=0.05, alpha=1.0)
        poly3d.set_facecolor(face_colors)
        poly3d.set_edgecolor('black') # Slight edge for definition
        ax.add_collection3d(poly3d)
        scale = mesh.points.flatten()
    else:
        # Scatter plot
        ax.scatter(points[:,0], points[:,1], points[:,2], c=point_colors, s=1, alpha=0.5)
        scale = points.flatten()
    
    # Auto-scale
    ax.auto_scale_xyz(scale, scale, scale)
    ax.auto_scale_xyz(scale, scale, scale)
    
    # Set view
    ax.view_init(elev=30, azim=45)
    
    # Remove axis clutter
    ax.set_axis_off()
    
    # Add title
    plt.title(f"Concept: {strategy['name']}\n{strategy['description']}", fontsize=14)
    
    # Add Legend-like text
    legend_text = ""
    for k, v in strategy['palette'].items():
        legend_text += f"{v['role']}: {v['color']} ({v['usage']})\n"
    
    plt.figtext(0.05, 0.05, legend_text, fontsize=10, bbox={"facecolor":"white", "alpha":0.8, "pad":5})

    print(f"Saving render to {output_path}...")
    plt.savefig(output_path, dpi=100)
    plt.close()

def main():
    stl_path = "capri/capri_fixed.stl"
    concepts_dir = "Capri_concepts2"
    
    if not os.path.exists(stl_path):
        print(f"Error: STL not found at {stl_path}")
        return

    json_files = glob.glob(os.path.join(concepts_dir, "strategy_*.json"))
    
    for json_file in json_files:
        basename = os.path.basename(json_file).replace(".json", ".png")
        output_path = os.path.join(concepts_dir, basename)
        try:
            render_concept(stl_path, json_file, output_path)
        except Exception as e:
            print(f"Failed to render {json_file}: {e}")

if __name__ == "__main__":
    main()
