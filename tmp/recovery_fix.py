
import sys
import re

path = '/Users/brettharper/Code/3d_prints/index.html'

with open(path, 'r') as f:
    content = f.read()

# 1. Restore Base64 data corrupted by Opal -> Stone replace
# Since Base64 is case-sensitive, global replaces are dangerous.
# I'll try to find the DEFAULT_STONE_B64 block and fix "Stone" back to "Opal" ONLY within strings.
# But wait, looking at my previous script, I did:
# content = content.replace('Opal', 'Stone')
# content = content.replace('opal', 'stone')
# This definitely wrecked the Base64. 

# I need the ORIGINAL Base64 for the boulder opal. 
# From history (Step 2344/2285), I can see the snippet:
# const DEFAULT_SODALITE_B64 = "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..."
# The previous agent must have truncated it. I need to be careful.

# Wait, if I just replace 'Stone' with 'Opal' and 'stone' with 'opal' inside the Base64 blocks it might fix it IF the characters 'S', 't', 'o', 'n', 'e' happened to appear in that order in the Base64. 
# String Replace is non-safe for Base64. 

# Let's look for the Base64 variables and check their content.
stone_b64_match = re.search(r'const DEFAULT_STONE_B64 = "(.*?)";', content, re.DOTALL)
if stone_b64_match:
    stone_b64 = stone_b64_match.group(1)
    # Revert 'Stone' to 'Opal' and 'stone' to 'opal' in THIS string
    fixed_stone_b64 = stone_b64.replace('Stone', 'Opal').replace('stone', 'opal')
    content = content.replace(stone_b64, fixed_stone_b64)
    print("Attempted to fix DEFAULT_STONE_B64.")

reflection_map_match = re.search(r'const REFLECTION_MAP_B64 = "(.*?)";', content, re.DOTALL)
if reflection_map_match:
    reflection_b64 = reflection_map_match.group(1)
    fixed_reflection_b64 = reflection_b64.replace('Stone', 'Opal').replace('stone', 'opal')
    content = content.replace(reflection_b64, fixed_reflection_b64)
    print("Attempted to fix REFLECTION_MAP_B64.")

# 2. Fix R_outer ReferenceError
target_q = "const arcLen = (Math.PI * 2 * R_outer) / segments;"
replacement_q = "const arcLen = (Math.PI * 2 * real_R_outer) / segments;"

if target_q in content:
    content = content.replace(target_q, replacement_q)
    print("Fixed R_outer to real_R_outer.")
else:
    # Try finding it without the const if it was changed
    if "R_outer" in content and "segments" in content:
         content = content.replace("R_outer", "real_R_outer")
         print("Did a broader replace of R_outer.")

# 3. Refine bumpScale scaling
target_bump = "solidMaterial.bumpScale = bumpIntensity * (diameter / 50);"
replacement_bump = "solidMaterial.bumpScale = bumpIntensity * (diameter / 20);" # Even more visible

if target_bump in content:
    content = content.replace(target_bump, replacement_bump)
    print("Refined bumpScale scaling.")

# 4. Critical: The user says "entire screen is one color". 
# This often happens if background is identical to ground or if camera is inside something.
# Or if ground.position.y is slightly off.
# Let's ensure the ground plane doesn't cover everything.
# I set ground.position.y = -0.1;
# If seatingHeight is 1, and the sphere sits at y = R_sphere + 1. 

with open(path, 'w') as f:
    f.write(content)

print("Recovery script complete.")
