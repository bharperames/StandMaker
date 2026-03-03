import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add help button to header
help_button = """
            <button id="help-btn" style="position: absolute; right: 1rem; top: 1rem; background: none; border: none; font-size: 1.2rem; cursor: pointer; opacity: 0.7; z-index: 1000;" title="Help">❓</button>
"""
if '<button id="help-btn"' not in content:
    content = content.replace('<div class="sidebar">', '<div class="sidebar">\n' + help_button)

# Add modal HTML
modal_html = """
    <div id="help-modal" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.8); z-index: 2000; justify-content: center; align-items: center;">
        <div style="background: #1e1e1e; padding: 2rem; border-radius: 12px; max-width: 500px; color: #fff; position: relative; border: 1px solid rgba(255,255,255,0.1);">
            <button id="close-help" style="position: absolute; right: 1rem; top: 1rem; background: none; border: none; color: #fff; font-size: 1.5rem; cursor: pointer;">×</button>
            <h2 style="margin-top: 0; color: #60a5fa; font-weight: 600;">How to use the Generator</h2>
            <ul style="line-height: 1.6; opacity: 0.9; padding-left: 1.2rem; font-size: 0.9rem;">
                <li><strong>Arc Length:</strong> Represents the physical contact length between the sphere and the stand's cupped edge. Optimize for at least 1-2mm to distribute weight safely and prevent denting the sphere.</li>
                <li><strong>Chamfer vs Thickness:</strong> The chamfer (outer angled edge) cannot mathematically exceed the wall thickness. The app auto-limits this to ensure structural integrity.</li>
                <li><strong>3D Print Texture:</strong> Simulates FDM layers. The bump scale automatically adjusts based on the sphere diameter, but you can tweak the 'Bump Intensity' under Advanced Visuals.</li>
                <li><strong>Exporting:</strong> We export standard OBJ and modern 3MF. 3MF is recommended as it preserves the exact 3D models and units (mm vs inches) for modern slicers like Bambu Studio.</li>
            </ul>
        </div>
    </div>
"""
if 'id="help-modal"' not in content:
    content = content.replace('</body>', modal_html + '\n</body>')

# Add modal JS event listeners
modal_js = """
        // Help Modal Logic
        const helpBtn = document.getElementById('help-btn');
        const helpModal = document.getElementById('help-modal');
        const closeHelp = document.getElementById('close-help');

        if (helpBtn) helpBtn.addEventListener('click', () => helpModal.style.display = 'flex');
        if (closeHelp) closeHelp.addEventListener('click', () => helpModal.style.display = 'none');
        if (helpModal) helpModal.addEventListener('click', (e) => {
            if (e.target === helpModal) helpModal.style.display = 'none';
        });
"""
if '// Help Modal Logic' not in content:
    content = content.replace('// --- Event Listeners & UI Logic ---', '// --- Event Listeners & UI Logic ---\n' + modal_js)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Help UI added successfully.")
