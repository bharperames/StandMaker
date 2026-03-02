import numpy as np
import struct
import os

def create_sphere_stand(sphere_diameter, M, filename="sphere_stand.stl", num_segments=72):
    """
    Creates an STL file for a sphere stand.
    
    The stand is a hollow cylinder with:
    - Inner radius: R_base - M/2
    - Outer radius: R_base + M/2
    - Top edge 'cupped' to match a sphere of radius R_sphere.
    """
    R_sphere = sphere_diameter / 2.0
    
    # Stability: Let's assume the base ring radius is 60% of the sphere radius
    # unless M is so large that it changes the geometry significantly.
    R_base = R_sphere * 0.6
    
    R_inner = R_base - (M / 2.0)
    R_outer = R_base + (M / 2.0)
    
    # Height of the cylinder (vertical part)
    # We want the top to be cupped. The lower the R_base, the deeper the cup.
    # Let's set a minimum wall height of M.
    # The sphere's equation: x^2 + y^2 + (z - Z_center)^2 = R_sphere^2
    # We want the cup to be at the top. Let's place the sphere so its lowest point
    # is at some height H_base.
    H_base = M 
    
    # Z_center of sphere so its bottom is at H_base + some 'cup depth'
    # Actually, let's just use the sphere equation to determine Z at R_inner and R_outer.
    # z = Z_center - sqrt(R_sphere^2 - (x^2 + y^2))
    # Let's say the top-outer edge is at height H_total = M + (R_sphere - sqrt(R_sphere^2 - R_outer^2))
    # This ensures the sphere sits flush on the outer edge.
    
    z_offset = R_sphere + H_base # Position sphere center so its bottom is at H_base
    
    def get_sphere_z(r):
        # z = z_offset - sqrt(R_sphere^2 - r^2)
        return z_offset - np.sqrt(R_sphere**2 - r**2)

    angles = np.linspace(0, 2 * np.pi, num_segments, endpoint=False)
    
    vertices = []
    facets = []

    # Create vertices
    # Bottom Inner: 0 to num_segments-1
    # Bottom Outer: num_segments to 2*num_segments-1
    # Top Inner: 2*num_segments to 3*num_segments-1
    # Top Outer: 3*num_segments to 4*num_segments-1
    
    for a in angles:
        x_i, y_i = R_inner * np.cos(a), R_inner * np.sin(a)
        x_o, y_o = R_outer * np.cos(a), R_outer * np.sin(a)
        
        # Bottom
        vertices.append([x_i, y_i, 0])
        vertices.append([x_o, y_o, 0])
        
        # Top (Cupped)
        vertices.append([x_i, y_i, get_sphere_z(R_inner)])
        vertices.append([x_o, y_o, get_sphere_z(R_outer)])

    # Re-organize vertices for easier indexing
    # V[4*i + 0] = Bottom Inner
    # V[4*i + 1] = Bottom Outer
    # V[4*i + 2] = Top Inner
    # V[4*i + 3] = Top Outer
    
    def add_quad(v1, v2, v3, v4):
        # v1, v2, v3, v4 are indices in CCW order
        facets.append([v1, v2, v3])
        facets.append([v1, v3, v4])

    for i in range(num_segments):
        next_i = (i + 1) % num_segments
        
        # indices for current segment
        bi, bo, ti, to = 4*i, 4*i+1, 4*i+2, 4*i+3
        # indices for next segment
        nbi, nbo, nti, nto = 4*next_i, 4*next_i+1, 4*next_i+2, 4*next_i+3
        
        # Bottom face (Looking from below: bo -> bi -> nbi -> nbo)
        add_quad(bo, bi, nbi, nbo)
        
        # Outer face (bo -> nbo -> nto -> to)
        add_quad(bo, nbo, nto, to)
        
        # Top face (to -> nto -> nti -> ti)
        add_quad(to, nto, nti, ti)
        
        # Inner face (bi -> ti -> nti -> nbi)
        add_quad(bi, ti, nti, nbi)

    # Write Binary STL
    with open(filename, 'wb') as f:
        f.write(b'\x00' * 80) # Header
        f.write(struct.pack('<I', len(facets))) # Number of facets
        
        for facet in facets:
            v1, v2, v3 = vertices[facet[0]], vertices[facet[1]], vertices[facet[2]]
            
            # Normal (can be zero, most slicers calculate it)
            f.write(struct.pack('<fff', 0, 0, 0))
            
            # Vertices
            for v in [v1, v2, v3]:
                f.write(struct.pack('<fff', v[0], v[1], v[2]))
                
            f.write(struct.pack('<H', 0)) # Attribute byte count

    print(f"STL saved to {filename}")
    print(f"Sphere Diameter: {sphere_diameter}mm")
    print(f"M: {M}mm")
    print(f"Base Radius: {R_base:.2f}mm")

if __name__ == "__main__":
    create_sphere_stand(sphere_diameter=50.0, M=5.0)
