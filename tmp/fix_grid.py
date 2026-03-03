file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Strip the GridHelper
grid_helper_code = """        const gridHelper = new THREE.GridHelper(500, 50, 0x334455, 0x112233);
        gridHelper.position.y = 0;
        gridHelper.material.opacity = 0.5;
        gridHelper.material.transparent = true;
        scene.add(gridHelper);"""
if grid_helper_code in text:
    text = text.replace(grid_helper_code, '')

# 2. Fix the Ground Plane Material
old_mat = "const groundMat = new THREE.MeshPhongMaterial({ color: 0x1a1a1a, shininess: 0 });"
new_mat = "const groundMat = new THREE.MeshBasicMaterial({ color: 0xffffff }); // Use BasicMaterial so texture isn't multiplied by dark base color"
if old_mat in text:
    text = text.replace(old_mat, new_mat)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Grid fix applied.")
