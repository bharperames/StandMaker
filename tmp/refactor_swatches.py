import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_js = """        // --- Dynamic Texture Swatches ---
        const TEXTURE_OPTIONS = [
            { id: 'pattern-1', name: 'High-grade Texture', b64: DEFAULT_SPHERE_PATTERN_B64 },
            { id: 'soda', name: 'Sodalite', b64: DEFAULT_SODALITE_B64 }
        ];

        const swatchContainer = document.getElementById('texture-swatch-container');
        if (swatchContainer) {
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
        // -------------------------------
"""

if '// --- Dynamic Texture Swatches ---' not in text:
    text = text.replace('// Populate Swatches with Base64 Previews', new_js + '// Populate Swatches with Base64 Previews')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Dynamic Logic Injected.")
