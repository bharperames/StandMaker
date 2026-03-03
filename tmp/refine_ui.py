import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix Tooltip Clipping
text = text.replace(
    'left: 50%;\n            transform: translateX(-50%);',
    'left: -10px;\n            transform: none;'
)

# 2. Refactor Base Color UI
old_color_ui = """                    <div class="setting-row">
                        <div class="tooltip-container"><span class="setting-label">Base Color</span><span
                                class="tooltip-icon"
                                data-tooltip="Changes the material color of the primary stand geometry.">?</span></div>
                        <input type="color" id="color-base" class="color-picker" value="#555555">
                    </div>
                    <div style="display: flex; gap: 0.4rem; margin-top: 0.5rem; flex-wrap: wrap;">
                        <div class="color-preset" style="background: #111111;" title="Jet Black" data-color="#111111">
                        </div>
                        <div class="color-preset" style="background: #8E918F;" title="Cool Grey" data-color="#8E918F">
                        </div>
                        <div class="color-preset" style="background: #f0f0f0;" title="Signal White"
                            data-color="#f0f0f0"></div>
                        <div class="color-preset" style="background: #FF0000;" title="Fire Red" data-color="#FF0000">
                        </div>
                        <div class="color-preset" style="background: #0000FF;" title="Deep Blue" data-color="#0000FF">
                        </div>
                        <div class="color-preset" style="background: #facc15;" title="Bumblebee Yellow"
                            data-color="#facc15"></div>
                    </div>"""

new_color_ui = """                    <div class="setting-row">
                        <div class="tooltip-container"><span class="setting-label">Base Color</span><span
                                class="tooltip-icon"
                                data-tooltip="Changes the material color of the primary stand geometry.">?</span></div>
                        <div style="display: flex; gap: 0.4rem; align-items: center; justify-content: flex-end; flex-wrap: wrap;">
                            <div class="color-preset" style="background: #111111;" title="Jet Black" data-color="#111111"></div>
                            <div class="color-preset" style="background: #8E918F;" title="Cool Grey" data-color="#8E918F"></div>
                            <div class="color-preset" style="background: #f0f0f0;" title="Signal White" data-color="#f0f0f0"></div>
                            <div class="color-preset" style="background: #FF0000;" title="Fire Red" data-color="#FF0000"></div>
                            <div class="color-preset" style="background: #0000FF;" title="Deep Blue" data-color="#0000FF"></div>
                            <div class="color-preset" style="background: #facc15;" title="Bumblebee Yellow" data-color="#facc15"></div>
                            <input type="color" id="color-base" class="color-picker" value="#555555" style="margin-left: 0.2rem;">
                        </div>
                    </div>"""

if old_color_ui in text:
    text = text.replace(old_color_ui, new_color_ui)
else:
    print("Warning: Old color UI block not found. Trying regex.")
    text = re.sub(
        r'<div class="setting-row">.*?<input type="color" id="color-base" class="color-picker" value="#555555">\s*</div>\s*<div[^>]*>.*?data-color="#facc15"></div>\s*</div>',
        new_color_ui,
        text,
        flags=re.DOTALL
    )

# 3. Move Stability Label
old_stability = """                        <div style="display: flex; justify-content: flex-end; margin-top: 4px; margin-right: 4px;">
                            <span id="stability-label" class="status-tag">STABLE</span>
                        </div>"""

if old_stability in text:
    text = text.replace(old_stability, "")
else:
    print("Warning: old_stability block not found perfectly.")
    # let's try a regex
    text = re.sub(
        r'<div style="display: flex; justify-content: flex-end; margin-top: 4px; margin-right: 4px;">\s*<span id="stability-label" class="status-tag">STABLE</span>\s*</div>',
        '',
        text
    )

old_actions = """                <div class="actions" style="display: flex; flex-direction: column; gap: 0.5rem;">"""
new_actions = """                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 0.75rem; color: var(--text-dim); font-weight: 500;">Build Assessment:</span>
                    <span id="stability-label" class="status-tag">STABLE</span>
                </div>
                <div class="actions" style="display: flex; flex-direction: column; gap: 0.5rem;">"""

text = text.replace(old_actions, new_actions)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied UI refinements.")
