
import re

path = '/Users/brettharper/Code/3d_prints/index.html'

with open(path, 'r') as f:
    content = f.read()

# --- 1. Clean up messy previous partial fixes ---
# Remove any duplicate R_sphere declarations if they exist
content = content.replace("const R_sphere = diameter / 2; const angle_out = Math.asin(Math.min(1.0, rc_test / Math.max(0.1, R_sphere)));", 
                         "const angle_out = Math.asin(Math.min(1.0, rc_test / Math.max(0.1, diameter / 2)));")

# --- 2. Centralize Global State at the top of the module ---
# Find where the script starts and declare everything needed early.
script_start = '<script type="module">'
if script_start in content:
    # We'll inject right after OrbitControls import or similar
    insertion_point = content.find('import { OrbitControls }')
    if insertion_point != -1:
        # Find the end of that line
        insertion_end = content.find('\n', insertion_point) + 1
        
        globals_block = """
        // Global State & Configuration
        let diameter = 50;
        let baseSize = 18;
        let thickness = 5;
        let chamfer = 2;
        let seatingHeight = 1.2;
        let segments = 64;
        let radialSubdivs = 8;
        let currentUnit = 'mm';
        let vizMode = 'solid';
        let baseStyle = 'plaster';
        let textureScale = 6;
        let sphereStyle = 'hide';
        let bumpIntensity = 0.5;
        let sphereTextureRotation = 0;

        const texLoader = new THREE.TextureLoader();
        """
        # Remove existing declarations of these to avoid double-declaration
        vars_to_remove = [
            "let diameter = 50;", "let baseSize = 18;", "let thickness = 5;", "let chamfer = 2;",
            "let seatingHeight = 1.2;", "let segments = 64;", "let radialSubdivs = 8;",
            "let currentUnit = 'mm';", "let vizMode = 'solid';", "let baseStyle = 'plaster';",
            "let textureScale = 6;", "let sphereStyle = 'hide';", "let bumpIntensity = 0.5;",
            "let sphereTextureRotation = 0;", "const texLoader = new THREE.TextureLoader();"
        ]
        for v in vars_to_remove:
            content = content.replace(v, "")
            
        content = content[:insertion_end] + globals_block + content[insertion_end:]

# --- 3. Fix misplaced updateGrid() ---
content = content.replace("updateGrid();", "") # Remove all calls

# --- 4. Ensure printBumpMap is created after its dependencies ---
# Find generatePrintTexture and ensure printBumpMap follows it
search_pattern = r'function generatePrintTexture.*?return tex;\s*\}'
match = re.search(search_pattern, content, re.DOTALL)
if match:
    func_end = match.end()
    # Inject printBumpMap creation here
    injection = "\n\n        const printBumpMap = generatePrintTexture(1024, textureScale);"
    # Remove old one
    content = content.replace("const printBumpMap = generatePrintTexture(1024, textureScale);", "")
    content = content[:func_end] + injection + content[func_end:]

# --- 5. Finalize updateGeometry with updateGrid ---
if "updateGeometry();" in content:
    # Find the LAST updateGeometry() call which is usually the initialization one
    last_call_idx = content.rfind("updateGeometry();")
    if last_call_idx != -1:
        content = content[:last_call_idx + 17] + "\n        updateGrid();" + content[last_call_idx + 17:]

with open(path, 'w') as f:
    f.write(content)

print("Applied comprehensive initialization fix.")
