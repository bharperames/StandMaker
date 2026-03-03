import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the appended dynamic logic
start_marker = "// --- Dynamic Texture Swatches ---"
end_marker = "// -------------------------------"

if start_marker in text and end_marker in text:
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker) + len(end_marker)
    text = text[:start_idx] + text[end_idx:]

# 2. Add the dynamic logic INSIDE the main module script, e.g., right before updateGeometry is initially called
# Or near where the help modal logic is
insertion_point = "updateGeometry(); // Initial draw"

new_js = """        // --- Dynamic Texture Swatches (Module Scope) ---
        const TEXTURE_OPTIONS = [
            { id: 'pattern-1', name: 'High-grade Texture', b64: DEFAULT_SPHERE_PATTERN_B64 },
            { id: 'soda', name: 'Sodalite', b64: DEFAULT_SODALITE_B64 }
        ];

        const swatchContainer = document.getElementById('texture-swatch-container');
        if (swatchContainer) {
            swatchContainer.innerHTML = ''; // clear any existing
            TEXTURE_OPTIONS.forEach((tex, index) => {
                const swatch = document.createElement('div');
                swatch.className = 'tex-swatch' + (index === 0 ? ' active' : '');
                swatch.id = 'tex-swatch-' + tex.id;
                swatch.title = tex.name;
                
                // Set background exactly like CSS
                swatch.style.backgroundImage = 'url(data:image/png;base64,' + tex.b64 + ')';
                swatch.style.backgroundSize = 'cover';
                swatch.style.backgroundPosition = 'center';
                
                if (index === 0) swatch.style.border = '1px solid #3b82f6';
                
                swatch.addEventListener('click', (e) => {
                    // Update active styling
                    document.querySelectorAll('.tex-swatch').forEach(s => {
                        s.classList.remove('active');
                        s.style.border = ''; // Reset border
                    });
                    swatch.classList.add('active');
                    swatch.style.border = '1px solid #3b82f6';
                    
                    // Load texture
                    loadSphereTexture('data:image/png;base64,' + tex.b64);
                });
                
                swatchContainer.appendChild(swatch);
            });
        }
        // ---------------------------------------------
"""

if '// --- Dynamic Texture Swatches (Module Scope) ---' not in text:
    text = text.replace(insertion_point, new_js + '\n        ' + insertion_point)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Scope fixed.")
