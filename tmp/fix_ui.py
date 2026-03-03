import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the CSS for tooltips to be visible on light background
old_css = """        .tooltip-icon {
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
        }"""
new_css = """        .tooltip-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            border: 1px solid rgba(0, 0, 0, 0.2);
            color: rgba(0, 0, 0, 0.4);
            font-size: 9px;
            font-weight: 500;
            margin-left: 6px;
            cursor: help;
            transition: all 0.2s;
        }
        .tooltip-icon:hover {
            color: #000;
            border-color: #000;
            background: rgba(0, 0, 0, 0.05);
        }"""

text = text.replace(old_css, new_css)

# 2. Rename Sphere Clearance label and input logic
text = text.replace('<label>Sphere Clearance</label>', '<label>Sphere Height</label>')
text = text.replace('id="clearance" min="0.1" max="100" value="1.0" step="0.1"', 'id="clearance" min="2.0" max="100" value="2.0" step="0.1"')
text = text.replace('id="num-clearance" class="num-input" value="1.0" step="0.1"', 'id="num-clearance" class="num-input" value="2.0" step="0.1"')
text = text.replace('let seatingHeight = 1.0;', 'let seatingHeight = 2.0;')
text = text.replace('clearance: [0.1, 100, 0.1]', 'clearance: [2.0, 100, 0.1]')
text = text.replace('clearance: [0.01, 4, 0.01]', 'clearance: [0.08, 4, 0.01]')

# 3. Add the missing tooltips to the <label> tags
missing_tooltips = {
    'Sphere Diameter': "The outer diameter of the sphere you intend to display (e.g., 50mm).",
    'Sphere Height': "How high the sphere is from the base of the stand (i.e. how high in the air it will be when supported).",
    'Base Size': "The diameter of the stand's base plate resting on the table.",
    'Wall Thickness': "The vertical height / thickness of the stand wall.",
    'Top Edge Chamfer': "A bevel applied to the top inner edge to prevent a sharp, fragile lip.",
    'Tessellation': "The rotational resolution of the CAD model (higher = smoother, slower to slice)."
}

for label, tooltip in missing_tooltips.items():
    icon_html = f'<span class="tooltip-icon" title="{tooltip}">?</span>'
    # Only replace if not already present
    pattern = re.compile(rf'(<label>{re.escape(label)}</label>)(?!\s*<span class="tooltip-icon")', re.IGNORECASE)
    def replace_with_icon(match):
        return match.group(0).replace(f'<label>{label}</label>', f'<label>{label}</label>{icon_html}')
    text = pattern.sub(replace_with_icon, text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied fix UI safely.")
