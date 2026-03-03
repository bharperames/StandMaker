import os
import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix default sphere style
content = content.replace("let sphereStyle = 'hide';", "let sphereStyle = 'design';")

# Implement proportional bump scaling
bump_logic = """
            if (vizMode === 'solid' || vizMode === 'both') {
                solidMaterial.bumpMap = (baseStyle === 'plaster') ? printBumpMap : null;
                // Proportional scaling: Intensity relative to diameter
                solidMaterial.bumpScale = bumpIntensity * (diameter / 50.0);
                if (solidMaterial.bumpMap) {
                    // Normalize layers: 1024 texture has ~170 layers at scale 6.
                    // Keep layer height visually consistent regardless of stand size.
                    const layerDensity = 5; // ~5 layers per mm
                    const repeatY = z_offset * layerDensity / 170.0 * 6.0;
                    const repeatX = diameter * Math.PI * layerDensity / 1024.0 * textureScale;
                    
                    solidMaterial.bumpMap.repeat.set(repeatX, repeatY);
                }
                solidMaterial.needsUpdate = true;
"""

old_bump_logic = """
            if (vizMode === 'solid' || vizMode === 'both') {
                solidMaterial.bumpMap = (baseStyle === 'plaster') ? printBumpMap : null;
                solidMaterial.bumpScale = bumpIntensity * (diameter / 20);
                if (solidMaterial.bumpMap) {
                    // Normalize layers: 1024 texture has ~170 layers at scale 6.
                    // We want ~5 layers per mm (0.2mm layers).
                    const totalHeight = z_offset; // Approximate
                    solidMaterial.bumpMap.repeat.set(diameter / 20, totalHeight / 10);
                }
                solidMaterial.needsUpdate = true;
"""

content = content.replace(old_bump_logic, bump_logic)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Sphere style and bump logic updated successfully.")
