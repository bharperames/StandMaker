
import sys
import re

path = '/Users/brettharper/Code/3d_prints/index.html'

with open(path, 'r') as f:
    content = f.read()

# 1. Fix groundMat ReferenceError (Removing premature updateGrid call)
content = content.replace("let currentUnit = 'mm'; updateGrid();", "let currentUnit = 'mm';")

# 2. Fix R_outer ReferenceError
content = content.replace("const arcLen = (Math.PI * 2 * R_outer) / segments;", "const arcLen = (Math.PI * 2 * real_R_outer) / segments;")

# 3. Restore Base64 strings
def restore_b64(match):
    prefix = match.group(1)
    b64_data = match.group(2)
    if len(b64_data) > 100:
        fixed = b64_data.replace('Stone', 'Opal').replace('stone', 'opal')
        return f'{prefix}"{fixed}";'
    return match.group(0)

# Defined 2 groups here
content = re.sub(r'(const \w+_B64 = )"(.*?)";', restore_b64, content, flags=re.DOTALL)

# 4. Refine bumpScale scaling
content = content.replace("solidMaterial.bumpScale = bumpIntensity * (diameter / 50);", "solidMaterial.bumpScale = bumpIntensity * (diameter / 20);")

with open(path, 'w') as f:
    f.write(content)

print("Final recovery script complete.")
