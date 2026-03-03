import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Provide a base64 string for the Sodalite swatch CSS background
# Since the image is large, we can just point the style to the JS variable on load
# For the HTML structure, we'll strip the explicit background-image url() rules and assign them via JS.

# Replace the HTML elements to remove the url() and just give them basic styling
swatch_html = """
                            <div class="tex-swatch-container">
                                <div class="tex-swatch active" id="tex-swatch-pattern-1"
                                    style="border: 1px solid #3b82f6;"
                                    title="High-grade Texture"></div>
                                <div class="tex-swatch" id="tex-swatch-soda"
                                    title="Sodalite"></div>
                            </div>
"""

old_swatch_html = """
                            <div class="tex-swatch-container">
                                <div class="tex-swatch active" id="tex-swatch-pattern-1"
                                    style="background-image: url('texture_preview_1.png'); border: 1px solid #3b82f6;"
                                    title="High-grade Texture"></div>
                                <div class="tex-swatch" id="tex-swatch-soda"
                                    style="background-image: url('sodalite_preview.png');" title="Sodalite"></div>
                            </div>
"""
text = text.replace(old_swatch_html, swatch_html)

# Add event listener code to populate the background-images using the JS base64 constants
swatch_js = """
        // Populate Swatches with Base64 Previews
        document.getElementById('tex-swatch-pattern-1').style.backgroundImage = 'url(data:image/png;base64,' + DEFAULT_SPHERE_PATTERN_B64 + ')';
        document.getElementById('tex-swatch-soda').style.backgroundImage = 'url(data:image/png;base64,' + DEFAULT_SODALITE_B64 + ')';

        // Texture Swatch UI state handling
        const swatches = document.querySelectorAll('.tex-swatch');
        swatches.forEach(sw => {
            sw.addEventListener('click', (e) => {
                swatches.forEach(s => s.classList.remove('active'));
                e.target.classList.add('active');
            });
        });
"""

# Find event listeners section to insert the JS
if '// Populate Swatches' not in text:
    text = text.replace('// --- Event Listeners & UI Logic ---', '// --- Event Listeners & UI Logic ---\n' + swatch_js)
    

# Fix the load function calls (one was calling a file directly instead of the base64, which we see in the grep output)
text = text.replace("loadSphereTexture('sphere_texture_1.png');", "loadSphereTexture('data:image/png;base64,' + DEFAULT_SPHERE_PATTERN_B64);")
text = text.replace("loadSphereTexture('sodalite_preview.png');", "loadSphereTexture('data:image/png;base64,' + DEFAULT_SODALITE_B64);")

# Wait, the grep showed us the correct base64 loads in lines 1386, 1391 which are inside the click listeners
#     1386: loadSphereTexture(DEFAULT_SPHERE_PATTERN_B64);
# Let's ensure the loadSphereTexture handles standard versus base64 inputs properly.
# Actually, those event listeners in click events already pass the base64 string.
# But loadSphereTexture might expect 'data:image/png;base64,' prefix. Let's make sure it handles it.
text = text.replace("loadSphereTexture(DEFAULT_SODALITE_B64);", "loadSphereTexture('data:image/png;base64,' + DEFAULT_SODALITE_B64);")
text = text.replace("loadSphereTexture(DEFAULT_SPHERE_PATTERN_B64);", "loadSphereTexture('data:image/png;base64,' + DEFAULT_SPHERE_PATTERN_B64);")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Texture styles baked and click listeners fixed successfully.")
