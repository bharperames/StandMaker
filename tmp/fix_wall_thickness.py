import re
file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Base Size
text = text.replace(
    '<div class="tooltip-container"><label>\n                        Base Size\n                        <span class="optimize-link" id="auto-optimize">Optimize All</span>\n                    </label>\n                    <div class="control-row">',
    '<div class="tooltip-container">\n                        <label>\n                            Base Size\n                            <span class="optimize-link" id="auto-optimize">Optimize All</span>\n                        </label>\n                        <span class="tooltip-icon" data-tooltip="The diameter of the stand\'s base plate resting on the table.">?</span>\n                    </div>\n                    <div class="control-row">'
)

# Fix Wall Thickness
text = text.replace(
    '<div class="input-group" style="margin-top: 1rem; position: relative;">\n                    <label>Wall Thickness</label><span class="tooltip-icon" data-tooltip="The vertical height / thickness of the stand wall.">?</span></div>\n                    <div class="control-row">',
    '<div class="input-group" style="margin-top: 1rem; position: relative;">\n                    <div class="tooltip-container">\n                        <label>Wall Thickness</label>\n                        <span class="tooltip-icon" data-tooltip="The vertical height / thickness of the stand wall.">?</span>\n                    </div>\n                    <div class="control-row">'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied strict replacement.")
