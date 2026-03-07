import re
import base64
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure assets directory exists
os.makedirs('assets', exist_ok=True)

# Define the textures we expect and their original MIME types/extensions
textures = {
    'NEW_TEXTURE_B64': 'jpeg',
    'EARTH_MAP_B64': 'jpeg',
    'ROSE_QUARTZ_B64': 'jpeg',
    'TIGERS_EYE_B64': 'jpeg',
    'LABRADORITE_B64': 'jpeg',
    'DEFAULT_SPHERE_PATTERN_B64': 'png',
    'DEFAULT_MOON_B64': 'jpeg',
    'DEFAULT_SODALITE_B64': 'png',
    'REFLECTION_MAP_B64': 'png'
}

for var_name, ext in textures.items():
    # Find the const declaration
    # e.g., const EARTH_MAP_B64 = "base64string";
    # Need to handle both single and double quotes
    pattern = rf'const\s+{var_name}\s*=\s*(["\'])(.*?)\1\s*;'
    match = re.search(pattern, html)
    
    if match:
        b64_data = match.group(2)
        
        # Save to assets folder
        filename = f"{var_name.lower().replace('_b64', '')}.{ext}"
        filepath = os.path.join('assets', filename)
        
        with open(filepath, 'wb') as img_f:
            img_f.write(base64.b64decode(b64_data))
        
        print(f"Saved {filepath}")
        
        # Remove the large base64 string variable from index.html
        html = html.replace(match.group(0), f"// Removed {var_name}")
        
        # Replace the usages
        # url: 'data:image/...;base64,' + VAR
        usage_pattern = rf'(["\'])data:image/[a-zA-Z]+;base64,["\']\s*\+\s*{var_name}'
        html = re.sub(usage_pattern, f"'assets/{filename}'", html)
    else:
        print(f"Warning: {var_name} not found in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Extraction and index.html update complete!")
