import re
import sys

file_path = '/Users/brettharper/Code/3d_prints/index.html'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Clean up any previous partial insertions
    text = re.sub(r'// --- Dynamic Texture Swatches.*?// ---------------------------------------------', '', text, flags=re.DOTALL)
    text = re.sub(r'// --- Dynamic Texture Swatches.*?// -------------------------------', '', text, flags=re.DOTALL)

    # 2. Add the dynamic logic INSIDE the main module script, at the end of the module but inside it.
    # The module seems to end with: loadSphereTexture(DEFAULT_SPHERE_PATTERN_B64); and then </script>
    
    new_js = """
        // --- Dynamic Texture Swatches (Module Scope) ---
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
    
    # Let's insert it right before the closing tag of the module script
    # Need to be careful. Let's find: `updateGeometry(); // Initial draw`
    # or `    </script>` the first one after `DEFAULT_SPHERE_PATTERN_B64`
    
    if "updateGeometry(); // Initial draw" in text:
        text = text.replace("updateGeometry(); // Initial draw", new_js + "\n        updateGeometry(); // Initial draw")
        print("Inserted using updateGeometry marker")
    else:
        # Fallback: find </script> after module
        # Find the module script
        module_script_match = re.search(r'<script type="module">(.*?)</script>', text, re.DOTALL)
        if module_script_match:
            module_content = module_script_match.group(1)
            new_module_content = module_content + new_js
            text = text.replace(module_content, new_module_content)
            print("Inserted at end of module script")
        else:
            print("Module script not found!")
            sys.exit(1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print("Dynamic swatch logic injected.")
except Exception as e:
    print(f"Error: {e}")
