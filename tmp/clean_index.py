import os

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r') as f:
    lines = f.readlines()

# We want to:
# 1. Add 'let isAnimatingSphere = false;' to the first block (after sphereTextureRotation)
# 2. Delete the duplicate lines we found.

new_lines = []
for i, line in enumerate(lines):
    ln = i + 1
    # Add missing variable to the first block
    if ln == 712: # After let sphereTextureRotation = 0;
        new_lines.append(line)
        new_lines.append("        let isAnimatingSphere = false;\n")
        continue
    
    # Delete first duplicate block (717-724)
    if 717 <= ln <= 724:
        continue
        
    # Delete second duplicate block (727-735) and the redeclaration of isAnimatingSphere (736)
    if 727 <= ln <= 736:
        continue
        
    new_lines.append(line)

with open(file_path, 'w') as f:
    f.writelines(new_lines)

print("Cleanup complete.")
