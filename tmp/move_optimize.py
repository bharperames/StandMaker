import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the old auto-optimize span
old_span = '<span class="optimize-link" id="auto-optimize">Optimize All</span>'
if old_span in text:
    text = text.replace(old_span, '')
else:
    print("Warning: could not find exact old_span string")
    # try regex just in case
    text = re.sub(r'<span[^>]*id="auto-optimize"[^>]*>Optimize All</span>', '', text)

# 2. Insert the new big Optimize Button just before Materials & Finish
target = '<div class="section-title">Materials & Finish</div>'

new_button_html = """                <div class="input-group" style="margin-top: 2rem; margin-bottom: 2.5rem;">
                    <button id="auto-optimize" class="primary" style="width: 100%; padding: 0.75rem; font-weight: 500; font-size: 0.95rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                        Auto-Optimize Geometry
                    </button>
                    <div style="text-align: center; margin-top: 0.5rem; font-size: 0.75rem; color: var(--text-dim); line-height: 1.4;">
                        Instantly calculates optimal Sphere Height, Base Size, Wall Thickness, and Top Edge Chamfer based on your Sphere Diameter.
                    </div>
                </div>

                """

if target in text:
    text = text.replace(target, new_button_html + target)
else:
    print("Warning: could not find Materials & Finish target")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Moved and styled the Optimize All button.")
