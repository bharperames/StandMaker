import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure grid doesn't exist
if 'new THREE.GridHelper' not in text:
    # Find scene setup
    scene_setup = "const scene = new THREE.Scene();"
    if scene_setup in text:
        grid_code = """
        // Scene setup
        // Add ground grid
        const gridHelper = new THREE.GridHelper(500, 50, 0x334455, 0x112233);
        gridHelper.position.y = 0;
        gridHelper.material.opacity = 0.5;
        gridHelper.material.transparent = true;
        scene.add(gridHelper);
"""
        text = text.replace(scene_setup, scene_setup + grid_code)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("GridHelper added to scene.")
    else:
        print("Could not find const scene = new THREE.Scene();")
else:
    print("Grid already exists in the file.")
