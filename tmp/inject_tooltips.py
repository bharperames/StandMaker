import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# First, remove the title tooltips we added to the inputs and buttons just to keep DOM clean
tooltips_to_remove = [
    "Render the base as a smooth, solid object.",
    "Render the base solid with a visible wireframe overlay for visualizing structure.",
    "Render the base purely as a wireframe mesh.",
    "The outer diameter of the sphere you intend to display (e.g., 50mm).",
    "Extra breathing room between the sphere and the stand interface so it doesn\\'t get stuck.",
    "The diameter of the stand\\'s base plate resting on the table.",
    "The vertical height / thickness of the stand wall.",
    "A bevel applied to the top inner edge to prevent a sharp, fragile lip.",
    "Show abstract mathematical wireframe to visualize fit.",
    "Render the sphere as a solid object to visualize final aesthetics.",
    "Hide the reference sphere completely.",
    "Tint the sphere\\'s 3D render (Photo mode).",
    "Scale the repeating texture pattern applied to the solid base.",
    "Intensity of the 3D bump mapping (layer lines/texture depth) on the base.",
    "The rotational resolution of the CAD model (higher = smoother, slower to slice).",
    "The material color of the primary stand geometry."
]

for tooltip in tooltips_to_remove:
    # Remove tooltip added with single or double quotes
    text = text.replace(f' title="{tooltip}" ', '')
    text = text.replace(f" title='{tooltip}' ", "")

# Define mapping for Labels
label_tooltips = {
    'Units': "Toggles all measurement values displayed in the UI.",
    'Render Mode': "Changes how the stand geometry is rendered (Solid, Wireframe, or Both).",
    'Base Color': "Changes the material color of the primary stand geometry.",
    'Sphere Diameter': "The outer diameter of the sphere you intend to display (e.g., 50mm).",
    'Sphere Clearance': "Extra breathing room between the sphere and the stand interface so it doesnt get stuck.",
    'Base Size': "The diameter of the stand's base plate resting on the table.",
    'Wall Thickness': "The vertical height / thickness of the stand wall.",
    'Top Edge Chamfer': "A bevel applied to the top inner edge to prevent a sharp, fragile lip.",
    'Sphere Style': "Toggles the 3D sphere visual (Wireframe, Solid, Hidden).",
    'Tessellation': "The rotational resolution of the CAD model (higher = smoother, slower to slice).",
    'Base Style': "Toggles custom textures for the Solid base material.",
    'Color / Tint': "Tints the sphere's 3D render (Photo mode only).",
    'Texture Style': "Applies a predefined pattern/texture to the base."
}

# Generate some CSS for the tooltip
css_to_add = """
        .tooltip-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            border: 1px solid rgba(255, 255, 255, 0.4);
            color: rgba(255, 255, 255, 0.7);
            font-size: 9px;
            font-weight: 500;
            margin-left: 6px;
            cursor: help;
            transition: all 0.2s;
        }
        .tooltip-icon:hover {
            color: #fff;
            border-color: #fff;
            background: rgba(255, 255, 255, 0.1);
        }
"""
if '.tooltip-icon {' not in text:
    text = text.replace('        .setting-label {', css_to_add + '        .setting-label {')

for label, tooltip in label_tooltips.items():
    # Only replace if we haven't already
    icon_html = f'<span class="tooltip-icon" title="{tooltip}">?</span>'
    
    # We look for something like <span class="setting-label">Units</span>
    # Or <span class="setting-label" style="...">Color / Tint</span>
    
    pattern = re.compile(rf'(<span class="setting-label"[^>]*>{re.escape(label)}</span>)(?!\s*<span class="tooltip-icon")', re.IGNORECASE)
    def replace_with_icon(match):
        return match.group(1) + icon_html
    
    text = pattern.sub(replace_with_icon, text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Tooltips changed to question marks next to labels.")
