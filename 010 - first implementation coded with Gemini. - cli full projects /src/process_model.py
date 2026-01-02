import trimesh
import numpy as np
import sys
import os

def process_model(input_path, output_path):
    print(f"Loading model from {input_path}...")
    try:
        mesh = trimesh.load(input_path)
    except Exception as e:
        print(f"Error loading mesh: {e}")
        sys.exit(1)

    # Ensure it's a single Trimesh object or a Scene
    if isinstance(mesh, trimesh.Scene):
        # If it's a scene, dump all geometries into a single list
        geometries = list(mesh.geometry.values())
    else:
        geometries = [mesh]

    print(f"Initial geometry count: {len(geometries)}")

    final_parts = []

    for geom in geometries:
        # Attempt to split into connected components
        parts = geom.split(only_watertight=False)
        if len(parts) > 1:
            print(f"Geometry split into {len(parts)} connected components.")
            final_parts.extend(parts)
        else:
            print("Geometry is a single component. Applying fallback segmentation (Height-based).")
            # Fallback: Slice the mesh into 4 vertical sections
            # bounds: [[min_x, min_y, min_z], [max_x, max_y, max_z]]
            z_min, z_max = geom.bounds[0][2], geom.bounds[1][2]
            height = z_max - z_min
            section_height = height / 4.0
            
            # We can't easily "cut" the mesh perfectly without boolean ops which are slow/complex.
            # Instead, we will identify faces in each region and separate them into sub-meshes.
            # This is a bit hacky but fast for visualization.
            
            # centroids of faces
            centroids = geom.triangles_center
            z_centroids = centroids[:, 2]
            
            for i in range(4):
                z_lower = z_min + (i * section_height)
                z_upper = z_min + ((i + 1) * section_height)
                
                # Mask for faces in this band
                if i == 3:
                     mask = (z_centroids >= z_lower)
                else:
                    mask = (z_centroids >= z_lower) & (z_centroids < z_upper)
                
                if np.sum(mask) > 0:
                    sub_mesh = geom.submesh([mask], append=True)
                    final_parts.append(sub_mesh)

    print(f"Total parts for export: {len(final_parts)}")

    # Create a scene with these parts
    scene = trimesh.Scene()
    
    # Assign names/colors to parts
    # Bambu Studio interprets separate objects in a 3MF as printable parts.
    colors = [
        [255, 0, 0, 255],   # Red
        [0, 255, 0, 255],   # Green
        [0, 0, 255, 255],   # Blue
        [255, 255, 0, 255]  # Yellow
    ]

    for i, part in enumerate(final_parts):
        color = colors[i % 4]
        part.visual.face_colors = color
        name = f"part_{i}_color_{i%4}"
        # trimesh scene add_geometry
        scene.add_geometry(part, node_name=name, geom_name=name)

    print(f"Exporting to {output_path}...")
    scene.export(output_path)
    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python process_model.py <input_stl> <output_3mf>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        sys.exit(1)
        
    process_model(input_file, output_file)
