import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Define tooltips mapped to element IDs
tooltips = {
    'viz-solid': "Render the base as a smooth, solid object.",
    'viz-both': "Render the base solid with a visible wireframe overlay for visualizing structure.",
    'viz-tess': "Render the base purely as a wireframe mesh.",
    'diameter': "The outer diameter of the sphere you intend to display (e.g., 50mm).",
    'clearance': "Extra breathing room between the sphere and the stand interface so it doesn\\'t get stuck.",
    'ratio': "The diameter of the stand\\'s base plate resting on the table.",
    'thickness': "The vertical height / thickness of the stand wall.",
    'chamfer': "A bevel applied to the top inner edge to prevent a sharp, fragile lip.",
    'sphere-design': "Show abstract mathematical wireframe to visualize fit.",
    'sphere-photo': "Render the sphere as a solid object to visualize final aesthetics.",
    'sphere-hide': "Hide the reference sphere completely.",
    'color-sphere': "Tint the sphere\\'s 3D render (Photo mode).",
    'tex-scale': "Scale the repeating texture pattern applied to the solid base.",
    'tex-bump': "Intensity of the 3D bump mapping (layer lines/texture depth) on the base.",
    'segments': "The rotational resolution of the CAD model (higher = smoother, slower to slice).",
    'color-base': "The material color of the primary stand geometry."
}

# Add tooltips to inputs/buttons
for element_id, tooltip in tooltips.items():
    # regex to find the tag with this id, making sure we don't duplicate title attribute
    pattern1 = re.compile(rf'(<(?:input|button)\s+[^>]*?id=[\'"]{element_id}[\'"][^>]*?)(/?>)', re.IGNORECASE)
    
    def replace_with_title(match):
        tag_content = match.group(1)
        closing = match.group(2)
        if 'title=' not in tag_content:
            return tag_content + f' title="{tooltip}" ' + closing
        return match.group(0)
    
    text = pattern1.sub(replace_with_title, text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Tooltips added.")
