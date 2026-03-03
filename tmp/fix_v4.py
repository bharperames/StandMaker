
import re

path = '/Users/brettharper/Code/3d_prints/index.html'

with open(path, 'r') as f:
    content = f.read()

# 1. Fix SyntaxError: Identifier 'R_sphere' has already been declared
# Remove my previous sloppy replacement that added a second declaration.
content = content.replace("const R_sphere = diameter / 2; const angle_out = Math.asin(Math.min(1.0, rc_test / Math.max(0.1, R_sphere)));", 
                         "const angle_out = Math.asin(Math.min(1.0, rc_test / Math.max(0.1, diameter / 2)));")

# 2. Fix ReferenceError: Cannot access 'groundMat' before initialization
# Move the updateGrid() call near the Three.js setup to after groundMat is fully defined.
# I previously moved it once, but let's ensure it's in a safe place.
# Actually, the subagent recommended moving it to the bottom.
content = content.replace("scene.add(ground);\n        updateGrid();", "scene.add(ground);")

# 3. Add updateGrid() to the very end of the initialization flow (after updateGeometry)
if "updateGeometry();" in content:
    content = content.replace("updateGeometry();", "updateGeometry();\n        updateGrid();")

# 4. Ensure textureScale is initialized early
if "let textureScale = 6;" not in content:
    content = content.replace("let diameter = 50;", "let textureScale = 6; let diameter = 50;")

with open(path, 'w') as f:
    f.write(content)

print("Fixed SyntaxError and initialization sequence.")
