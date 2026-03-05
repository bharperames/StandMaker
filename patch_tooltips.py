import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS
css_old = """        .help-btn {
            position: absolute;
            top: 2rem;
            right: 2rem;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            border: 1px solid var(--text-dim);
            color: var(--text-dim);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            z-index: 20;
        }

        .help-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
            background: rgba(59, 130, 246, 0.05);
        }

        .tooltip {
            position: absolute;
            top: 4.5rem;
            right: 2rem;
            width: 300px;
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            font-size: 0.8rem;
            line-height: 1.5;
            display: none;
            z-index: 100;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }"""

css_new = """        .help-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            border: 1px solid var(--text-dim);
            color: var(--text-dim);
            font-size: 0.65rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            z-index: 20;
            margin-left: 0.5rem;
            flex-shrink: 0;
            position: relative;
        }

        #main-help-btn {
            position: absolute;
            top: 2rem;
            right: 2rem;
            width: 24px;
            height: 24px;
            font-size: 0.75rem;
            margin-left: 0;
        }

        .help-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
            background: rgba(59, 130, 246, 0.05);
        }

        .tooltip {
            position: absolute;
            top: calc(100% + 0.5rem);
            left: 0;
            width: 280px;
            background: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            font-size: 0.75rem;
            line-height: 1.5;
            display: none;
            z-index: 100;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }

        #main-tooltip {
            top: 4.5rem;
            right: 2rem;
            left: auto;
            width: 300px;
            padding: 1.5rem;
            font-size: 0.8rem;
        }"""

text = text.replace(css_old, css_new)

# 2. Update the main help button
text = text.replace('<div class="help-btn">?</div>', '<div id="main-help-btn" class="help-btn">?</div>')
text = text.replace('<div class="tooltip">\\n                    <h3>Printing Guide</h3>', '<div id="main-tooltip" class="tooltip">\\n                    <h3>Printing Guide</h3>')

# Also fix the line in case there's slight whitespace diffs
text = re.sub(r'<div class="tooltip">\s*<h3>Printing Guide</h3>', '<div id="main-tooltip" class="tooltip">\\n                    <h3>Printing Guide</h3>', text)

# 3. Remove .tooltip-icon CSS
text = re.sub(r'        \.tooltip-icon \{.*?\n        \}\n', '', text, flags=re.DOTALL)

# 4. Replace <span class="tooltip-icon" data-tooltip="...">?</span> with <div class="help-btn">?</div><div class="tooltip"><p>...</p></div>
# We need to ensure that the parent container is relative so the tooltip anchors correctly. 
# Some of them are in <div class="tooltip-container"> already (which we'll make relative in css)
# Some parents might not be. Let's add position: relative to .tooltip-container in CSS or inline.
text = text.replace('.tooltip-container {', '.tooltip-container {\\n            position: relative;')

def replace_tooltip(match):
    tooltip_text = match.group(1)
    # Return the new HTML structure
    return f'<div class="help-btn">?</div>\\n<div class="tooltip"><p>{tooltip_text}</p></div>'

text = re.sub(r'<span[^>]*class="tooltip-icon"[^>]*data-tooltip="([^"]+)"[^>]*>\?</span>', replace_tooltip, text)


# Wait, some tooltip-icons were rendered across multiple lines!
text = re.sub(r'(?s)<span\s+(?:[^>]*?\s+)?class="tooltip-icon"(?:\s+[^>]*?)?\s+data-tooltip="([^"]+)"(?:\s+[^>]*?)?>\?</span>', replace_tooltip, text)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Patching complete.")
