import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS for tooltips
old_css_pattern = re.compile(r'\.tooltip-icon\s*{[^}]*}\s*\.tooltip-icon:hover\s*{[^}]*}', re.MULTILINE)

new_tooltip_css = """        .tooltip-container {
            display: flex;
            align-items: center;
        }
        .tooltip-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            border: 1px solid rgba(0, 0, 0, 0.3);
            color: rgba(0, 0, 0, 0.5);
            font-size: 10px;
            font-weight: bold;
            margin-left: 6px;
            cursor: help;
            transition: all 0.2s;
            position: relative;
        }
        .tooltip-icon:hover {
            color: #fff;
            border-color: #3b82f6;
            background: #3b82f6;
        }
        .tooltip-icon:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 150%;
            left: 50%;
            transform: translateX(-50%);
            background: #222;
            color: #fff;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 11px;
            white-space: normal;
            width: max-content;
            max-width: 220px;
            text-align: center;
            z-index: 1000;
            pointer-events: none;
            line-height: 1.4;
            font-weight: 400;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .tooltip-icon:hover::before {
            content: '';
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 5px solid transparent;
            border-top-color: #222;
            z-index: 1000;
        }"""

if '.tooltip-container' not in text:
    if old_css_pattern.search(text):
        text = old_css_pattern.sub(new_tooltip_css, text)
    else:
        text = text.replace('        .setting-label {', new_tooltip_css + '\n        .setting-label {')

# 2. Fix the HTML wrappers and switch title to data-tooltip
# We'll match <label>XYZ</label><span class="tooltip-icon" title="ABC">?</span>
pattern_label = re.compile(
    r'(<(?:label|span class="setting-label"[^>]*)>)(.*?)(</(?:label|span)>)\s*(<span class="tooltip-icon"\s+title="([^"]+)">\?</span>)'
)

def wrapper_repl(match):
    start_tag = match.group(1)
    content = match.group(2)
    end_tag = match.group(3)
    span_tag = match.group(4)
    tooltip_text = match.group(5)
    
    # replace title with data-tooltip
    span_tag_new = span_tag.replace('title=', 'data-tooltip=')
    
    return f'<div class="tooltip-container">{start_tag}{content}{end_tag}{span_tag_new}</div>'

text = pattern_label.sub(wrapper_repl, text)

# Just in case some were missed if they span lines? (They shouldn't).
# Wait, let's fix the Base Size which is a special case inside the UI string
# "Base Size <a ...>Optimize All</a>" might break the regex if the label doesn't contain the a...
# But Base Size doesn't have a label anymore, wait, is it just <label>Base Size\n<a href...>?
# Let's fix Base Size specifically if it didn't get caught

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied tooltip wrappers and custom CSS hover.")
