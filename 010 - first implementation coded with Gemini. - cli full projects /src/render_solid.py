import trimesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
import json
import os
import glob
import sys

# Custom Voxel Clustering Simplification (Fast & Pure Python)
def simplify_mesh_voxel(mesh, voxel_size):
    # 1. Quantize vertices to grid
    # (vertices / voxel_size).round() * voxel_size
    quantized = np.round(mesh.vertices / voxel_size) * voxel_size
    
    # 2. Find unique vertices and inverse mapping
    unique_verts, inverse = np.unique(quantized, axis=0, return_inverse=True)
    
    # 3. Re-map faces
    new_faces = inverse[mesh.faces]
    
    # 4. Remove degenerate faces (where 2 or more vertices are the same)
    # Check if v0==v1 or v1==v2 or v0==v2
    non_degenerate = (new_faces[:,0] != new_faces[:,1]) & \
                     (new_faces[:,1] != new_faces[:,2]) & \
                     (new_faces[:,0] != new_faces[:,2])
    
    clean_faces = new_faces[non_degenerate]
    
    # Create new mesh
    new_mesh = trimesh.Trimesh(vertices=unique_verts, faces=clean_faces)
    return new_mesh

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

def render_solid(stl_path, strategy_path, output_path):
    print(f"Rendering solid preview for {strategy_path}...")
    
    with open(strategy_path, 'r') as f:
        strategy = json.load(f)
    
    # Extract palette
    try:
        colors = [
            strategy['palette']['Color 1']['hex'],
            strategy['palette']['Color 2']['hex'],
            strategy['palette']['Color 3']['hex'],
            strategy['palette']['Color 4']['hex']
        ]
    except:
        # Fallback for "concept" style json if different
        colors = strategy.get('colors', ["#CCCCCC"]*4)
        
    rgb_colors = [hex_to_rgb(c) for c in colors]

    # Load mesh
    mesh = trimesh.load(stl_path)
    
    # Simplify Loop to get target face count (~2000-3000 for matplotlib trisurf)
    target_faces = 2500
    voxel_size = mesh.extents.max() / 50.0 # Start guess
    
    for attempt in range(5):
        simple = simplify_mesh_voxel(mesh, voxel_size)
        if len(simple.faces) > target_faces * 1.5:
            voxel_size *= 1.5 # Increase voxel size to reduce faces
        elif len(simple.faces) < target_faces * 0.5:
            voxel_size *= 0.75 # Decrease voxel size
        else:
            break
            
    print(f"Original faces: {len(mesh.faces)}, Simplified faces: {len(simple.faces)}")
    mesh = simple
    
    # Segmentation (Height based)
    z_centroids = mesh.triangles_center[:, 2]
    z_min, z_max = z_centroids.min(), z_centroids.max()
    height = z_max - z_min
    section_height = height / 4.0
    
    face_colors = np.zeros((len(mesh.faces), 3))
    
    for i in range(4):
        z_lower = z_min + (i * section_height)
        z_upper = z_min + ((i + 1) * section_height)
        if i == 3: mask = (z_centroids >= z_lower)
        else: mask = (z_centroids >= z_lower) & (z_centroids < z_upper)
        face_colors[mask] = rgb_colors[i % 4]

    # Matplotlib Render
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Use Poly3DCollection for flat shading (looks better/cleaner than trisurf often)
    poly3d = art3d.Poly3DCollection(mesh.vertices[mesh.faces], linewidths=0.0)
    poly3d.set_facecolor(face_colors)
    poly3d.set_edgecolor(face_colors) # Same color edges to hide wireframe look
    poly3d.set_alpha(1.0)
    
    ax.add_collection3d(poly3d)
    
    # Scaling
    scale = mesh.vertices.flatten()
    ax.auto_scale_xyz(scale, scale, scale)
    
    # Light source illusion (not real lighting in mpl, but we can fake it or just accept flat)
    # Matplotlib 3D doesn't do real lights easily on Collections.
    # We will stick to flat shaded colors which shows the scheme well.
    
    ax.view_init(elev=30, azim=-45)
    ax.set_axis_off()
    
    plt.title(f"Concept: {strategy['name']}", fontsize=15)
    
    # Add Legend
    legend_text = ""
    try:
        for k, v in strategy['palette'].items():
            legend_text += f"{v['role']}: {v['color']}\n"
    except:
        pass
        
    plt.figtext(0.02, 0.02, legend_text, fontsize=9, bbox={"facecolor":"white", "alpha":0.9, "pad":5})

    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Saved {output_path}")

def main():
    stl_path = "capri/capri_fixed.stl"
    concepts_dir = "Capri_concepts2"
    
    json_files = glob.glob(os.path.join(concepts_dir, "strategy_*.json"))
    
    for json_file in json_files:
        basename = os.path.basename(json_file).replace(".json", "_solid.png")
        output_path = os.path.join(concepts_dir, basename)
        try:
            render_solid(stl_path, json_file, output_path)
        except Exception as e:
            print(f"Failed {json_file}: {e}")

if __name__ == "__main__":
    main()
