import re

file_path = '/Users/brettharper/Code/3d_prints/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix R_inner Geometry Building
old_r_calc = "const r = R_inner + (real_R_outer - R_inner) * (j / radialSubdivs);"
new_r_calc = """const safe_R_inner = Math.max(0.0, R_inner);
                const r = safe_R_inner + (real_R_outer - safe_R_inner) * (j / radialSubdivs);"""

if old_r_calc in text:
    text = text.replace(old_r_calc, new_r_calc)
else:
    print("Warning: old_r_calc not found.")

# 2. Add Deduplication to download3MF
old_3mf_export = """            const p = m.geometry.attributes.position.array;
            const idx = m.geometry.index.array;
            let v = ""; for (let i = 0; i < p.length; i += 3) v += `<vertex x="${p[i].toFixed(4)}" y="${p[i + 2].toFixed(4)}" z="${p[i + 1].toFixed(4)}" />`;
            let f = ""; for (let i = 0; i < idx.length; i += 3) f += `<triangle v1="${idx[i]}" v2="${idx[i + 1]}" v3="${idx[i + 2]}" />`;
            const mx = `<?xml version="1.0" encoding="UTF-8"?><model unit="${currentUnit === 'in' ? 'inch' : 'millimeter'}" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources><object id="1" type="model"><mesh><vertices>${v}</vertices><triangles>${f}</triangles></mesh></object></resources><build><item objectid="1"/></build></model>`;
"""

new_3mf_export = """            const p = m.geometry.attributes.position.array;
            const idx = m.geometry.index.array;
            
            // --- Vertex Deduplication (Manifold Mesh Fix) ---
            const uniqueVertices = [];
            const posMap = new Map();
            const indexRemap = [];
            let vCount = 0;
            
            for (let i = 0; i < p.length; i += 3) {
                // Round to 4 decimal places to catch floating point seam drift
                const x = parseFloat(p[i].toFixed(4));
                const y = parseFloat(p[i + 1].toFixed(4));
                const z = parseFloat(p[i + 2].toFixed(4));
                const key = `${x},${y},${z}`;
                
                if (posMap.has(key)) {
                    indexRemap.push(posMap.get(key));
                } else {
                    posMap.set(key, vCount);
                    indexRemap.push(vCount);
                    uniqueVertices.push({x, y, z});
                    vCount++;
                }
            }
            
            let v = ""; 
            for (let i = 0; i < uniqueVertices.length; i++) {
                v += `<vertex x="${uniqueVertices[i].x.toFixed(4)}" y="${uniqueVertices[i].z.toFixed(4)}" z="${uniqueVertices[i].y.toFixed(4)}" />`;
            }
            
            let f = ""; 
            for (let i = 0; i < idx.length; i += 3) {
                const map1 = indexRemap[idx[i]];
                const map2 = indexRemap[idx[i + 1]];
                const map3 = indexRemap[idx[i + 2]];
                // Only add triangle if it has area (not mathematically collapsed by pinching center point)
                if (map1 !== map2 && map2 !== map3 && map1 !== map3) {
                    f += `<triangle v1="${map1}" v2="${map2}" v3="${map3}" />`;
                }
            }
            const mx = `<?xml version="1.0" encoding="UTF-8"?><model unit="${currentUnit === 'in' ? 'inch' : 'millimeter'}" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources><object id="1" type="model"><mesh><vertices>${v}</vertices><triangles>${f}</triangles></mesh></object></resources><build><item objectid="1"/></build></model>`;
"""

if old_3mf_export in text:
    text = text.replace(old_3mf_export, new_3mf_export)
else:
    print("Warning: old_3mf_export not found. Trying regex.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied watertight geometry fixes.")
