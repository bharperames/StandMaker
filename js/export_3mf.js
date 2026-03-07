/**
 * export_3mf.js
 * Extracted logic for generating 3MF file XML strings securely and headlessly.
 */

/**
 * Validates, deduplicates, and generates the core `model.model` XML string required for a 3MF container.
 * @param {Float32Array|Array} positions - Flat array of [x,y,z, x,y,z...] vertex coordinates.
 * @param {Uint16Array|Uint32Array|Array} indices - Flat array of vertex indices forming triangles.
 * @param {string} exportUnit - The unit string to embed in the 3MF file (default: 'millimeter').
 * @returns {string} The fully formed XML string for the 3D model.
 */
export function generate3MFXML(positions, indices, exportUnit = 'millimeter') {
    if (!positions || !indices || positions.length === 0 || indices.length === 0) {
        throw new Error("Invalid geometry arrays provided for 3MF export.");
    }

    // --- Vertex Deduplication (Manifold Mesh Fix) ---
    const uniqueVertices = [];
    const posMap = new Map();
    const indexRemap = [];
    let vCount = 0;

    for (let i = 0; i < positions.length; i += 3) {
        // We round to 4 decimal places to fix floating point drift when deduplicating shared edges
        const x = parseFloat(positions[i].toFixed(4));
        const y = parseFloat(positions[i + 1].toFixed(4));
        const z = parseFloat(positions[i + 2].toFixed(4));
        const key = `${x},${y},${z}`;

        if (posMap.has(key)) {
            indexRemap.push(posMap.get(key));
        } else {
            posMap.set(key, vCount);
            indexRemap.push(vCount);
            uniqueVertices.push({ x, y, z });
            vCount++;
        }
    }

    let v = "";
    for (let i = 0; i < uniqueVertices.length; i++) {
        // 3MF standard expects Y-up coordinate systems. Three.js is also Y-up, 
        // but historically exports often flip Z/Y manually depending on Slicer target. 
        // We maintain the mapping that was present in the original codebase:
        // XML X = Three x, XML Y = Three z, XML Z = Three y
        v += `<vertex x="${uniqueVertices[i].x.toFixed(4)}" y="${uniqueVertices[i].z.toFixed(4)}" z="${uniqueVertices[i].y.toFixed(4)}" />`;
    }

    let t = "";
    for (let i = 0; i < indices.length; i += 3) {
        const map1 = indexRemap[indices[i]];
        const map2 = indexRemap[indices[i + 1]];
        const map3 = indexRemap[indices[i + 2]];
        
        // Prevent degenerate zero-area triangles from sneaking into the 3MF file
        if (map1 !== map2 && map2 !== map3 && map1 !== map3) {
            t += `<triangle v1="${map1}" v2="${map2}" v3="${map3}" />`;
        }
    }

    const xml = `<?xml version="1.0" encoding="UTF-8"?><model unit="${exportUnit}" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources><object id="1" type="model"><mesh><vertices>${v}</vertices><triangles>${t}</triangles></mesh></object></resources><build><item objectid="1" /></build></model>`;
    return xml;
}
