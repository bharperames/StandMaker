
import re

path = '/Users/brettharper/Code/3d_prints/index.html'

with open(path, 'r') as f:
    content = f.read()

# 1. Ensure textureScale is initialized before generatePrintTexture is called
# The code has: let currentUnit = 'mm'; 
# followed by some other lets.
# Let's add textureScale there if it's missing or move it.
if 'let textureScale = 6;' not in content:
    content = content.replace("let diameter = 50;", "let textureScale = 6; let diameter = 50;")

# 2. Fix the line 843 crash: const printBumpMap = generatePrintTexture(1024, textureScale);
# It might be using an uninitialized textureScale or crashing inside generatePrintTexture.
# I'll make sure generatePrintTexture has a default value for layerThickness.

# 3. Fix the Arc: 0.00mm issue
# The user mentioned angle_out calculation: 
# const angle_out = Math.asin(Math.min(1.0, rc_test / R_sphere));
# If R_sphere is 0 or very small or rc_test is 0, we get 0.
# Also check if R_sphere is initialized correctly.
# In updateGeometry: const R_sphere = diameter / 2;

content = content.replace("const angle_out = Math.asin(Math.min(1.0, rc_test / R_sphere));", 
                         "const R_sphere = diameter / 2; const angle_out = Math.asin(Math.min(1.0, rc_test / Math.max(0.1, R_sphere)));")

# 4. Check for any other ReferenceErrors in the initialization block
# The subagent mentioned a "solid light-blue/purple gradient" - this often means the canvas exists but the scene never renders.
# Usually caused by a single JS error stopping the requestAnimationFrame loop.

with open(path, 'w') as f:
    f.write(content)

print("Applied textureScale and Arc calculation fixes.")
