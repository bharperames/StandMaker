import os

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r') as f:
    content = f.read()

# 1. Terminology renaming
# Rename DEFAULT_STONE_B64 to DEFAULT_SPHERE_PATTERN_B64
content = content.replace('DEFAULT_STONE_B64', 'DEFAULT_SPHERE_PATTERN_B64')
content = content.replace('tex-swatch-stone', 'tex-swatch-pattern-1')
content = content.replace('Standard Stone', 'High-grade Texture')
content = content.replace('Stone Texture', 'Sphere Texture')
content = content.replace('stone_texture.png', 'sphere_texture_1.png')
content = content.replace('stone_texture_preview.png', 'texture_preview_1.png')

# 2. Arc Length Fix
# Search for the old calculation and replace it with a more robust one.
old_arc_logic = """            const angle_in = Math.asin(Math.min(1.0, R_inner / R_sphere));
            const angle_out = Math.asin(Math.min(1.0, rc_test / Math.max(0.1, diameter / 2)));
            const contactArcLength = R_sphere * (angle_out - angle_in);"""

new_arc_logic = """            const angle_in = Math.asin(Math.min(1.0, R_inner / R_sphere));
            const angle_out = Math.asin(Math.min(1.0, rc_test / R_sphere));
            // Correct arc length formula: R * theta, with safety clamp
            const contactArcLength = R_sphere * Math.max(0, angle_out - angle_in);"""

content = content.replace(old_arc_logic, new_arc_logic)

# 3. Proportional Bump Mapping & Layer Scaling
# We want the layers to look consistent.
# Current bumpScale logic: solidMaterial.bumpScale = bumpIntensity * (diameter / 20);
# Let's also adjust the texture repeat.
# If diameter is 100, we want more repeats than if diameter is 20.
old_bump_logic = "solidMaterial.bumpScale = bumpIntensity * (diameter / 20);"
new_bump_logic = """solidMaterial.bumpScale = bumpIntensity * (diameter / 20);
                if (solidMaterial.bumpMap) {
                    // Normalize layers: 1024 texture has ~170 layers at scale 6.
                    // We want ~5 layers per mm (0.2mm layers).
                    const totalHeight = z_offset; // Approximate
                    solidMaterial.bumpMap.repeat.set(diameter / 20, totalHeight / 10);
                }"""

# Wait, check if solidMaterial.bumpScale exists and matches.
content = content.replace(old_bump_logic, new_bump_logic)

# 4. Chamfer Constraints
# Add a stricter cap to chamfer to prevent it from exceeding wall thickness.
old_chamfer_check = """            if (y_at_outer < 0) {
                const safeChamfer = Math.max(0, y_at_rc);
                if (chamfer > safeChamfer) {
                    chamfer = safeChamfer;
                    syncInputs('chamfer', chamfer);
                }
            }"""

new_chamfer_check = """            // Strict Chamfer Limit: Cannot exceed wall thickness
            const chamferLimit = Math.min(thickness - 0.1, y_at_rc);
            if (chamfer > chamferLimit) {
                chamfer = Math.max(0, chamferLimit);
                syncInputs('chamfer', chamfer);
            }

            if (y_at_outer < 0) {
                const safeChamfer = Math.max(0, y_at_rc);
                if (chamfer > safeChamfer) {
                    chamfer = safeChamfer;
                    syncInputs('chamfer', chamfer);
                }
            }"""

content = content.replace(old_chamfer_check, new_chamfer_check)

with open(file_path, 'w') as f:
    f.write(content)

print("Applied terminology, arc length, bump scaling, and chamfer fixes.")
