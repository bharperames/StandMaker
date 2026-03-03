import os

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r') as f:
    lines = f.readlines()

new_grid_func = """        function generateGridTexture(unit = 'mm') {
            const size = 1024;
            const canvas = document.createElement('canvas');
            canvas.width = size;
            canvas.height = size;
            const ctx = canvas.getContext('2d');

            ctx.fillStyle = '#050505';
            ctx.fillRect(0, 0, size, size);

            const mmScale = size / 100;
            
            let minorStep, mediumStep, majorStep;
            if (unit === 'mm') {
                minorStep = 1;
                mediumStep = 5;
                majorStep = 10;
            } else {
                minorStep = 25.4 / 8; // 1/8"
                mediumStep = 25.4 / 4; // 1/4"
                majorStep = 25.4;     // 1"
            }

            // 1. Minor Lines (Very Subtle)
            ctx.lineWidth = 1;
            ctx.strokeStyle = '#151515';
            for (let i = 0; i <= 100; i += minorStep) {
                const pos = i * mmScale;
                ctx.beginPath(); ctx.moveTo(pos, 0); ctx.lineTo(pos, size); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(0, pos); ctx.lineTo(size, pos); ctx.stroke();
            }

            // 2. Medium Lines (Noticeable)
            ctx.lineWidth = 1;
            ctx.strokeStyle = '#252525';
            for (let i = 0; i <= 100; i += mediumStep) {
                const pos = i * mmScale;
                ctx.beginPath(); ctx.moveTo(pos, 0); ctx.lineTo(pos, size); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(0, pos); ctx.lineTo(size, pos); ctx.stroke();
            }

            // 3. Major Lines (Vibrant)
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#0044aa'; 
            for (let i = 0; i <= 100; i += majorStep) {
                const pos = i * mmScale;
                ctx.beginPath(); ctx.moveTo(pos, 0); ctx.lineTo(pos, size); ctx.stroke();
                ctx.beginPath(); ctx.moveTo(0, pos); ctx.lineTo(size, pos); ctx.stroke();
            }

            const texture = new THREE.CanvasTexture(canvas);
            texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
            texture.repeat.set(10, 10); // 1000mm total size
            texture.anisotropy = renderer.capabilities.getMaxAnisotropy();
            return texture;
        }
"""

# The function start was at 760 and end (disposable lines) at 793.
# Let's find it more robustly by looking for "function generateGridTexture"
start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "function generateGridTexture(unit = 'mm')" in line:
        start_idx = i
    if start_idx != -1 and "return texture;" in line:
        # The next line is the closing brace
        if "}" in lines[i+1]:
            end_idx = i + 1
            break

if start_idx != -1 and end_idx != -1:
    print(f"Replacing lines {start_idx+1} to {end_idx+1}")
    lines[start_idx:end_idx+1] = [new_grid_func]
    with open(file_path, 'w') as f:
        f.writelines(lines)
    print("Success")
else:
    print("Could not find function markers")
