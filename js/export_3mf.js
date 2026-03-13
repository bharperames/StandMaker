/**
 * export_3mf.js
 * Extracted logic for generating 3MF file XML strings securely and headlessly.
 */

import { deduplicateGeometry } from './math_logic.js';

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
    const { uniqueVertices, indexRemap } = deduplicateGeometry(positions, indices);

    let v = "";
    for (let i = 0; i < uniqueVertices.length; i++) {
        // 3MF standard expects Z-up right-handed coordinate systems. Three.js is Y-up right-handed.
        // We must apply a +90 degree rotation around the local X-axis: 
        // XML X = Three x, XML Y = -Three z, XML Z = Three y.
        // This avoids mirroring the mesh and breaking the CCW geometric winding sequence.
        const px = uniqueVertices[i].x;
        const py = uniqueVertices[i].z === 0 ? 0 : -uniqueVertices[i].z;
        const pz = uniqueVertices[i].y;
        v += `<vertex x="${px.toFixed(6)}" y="${py.toFixed(6)}" z="${pz.toFixed(6)}" />`;
    }

    let t = "";
    for (let i = 0; i < indices.length; i += 3) {
        const map1 = indexRemap[indices[i]];
        const map2 = indexRemap[indices[i + 1]];
        const map3 = indexRemap[indices[i + 2]];

        // 3MF spec §4.1.4: a triangle MUST NOT have two vertices with the same index.
        // Degenerate triangles (collapsed by vertex deduplication) have no area and no valid edges —
        // they cannot close any manifold edge, so omitting them is safe and spec-compliant.
        if (map1 === map2 || map2 === map3 || map1 === map3) continue;

        t += `<triangle v1="${map1}" v2="${map2}" v3="${map3}" />`;
    }

    const xml = `<?xml version="1.0" encoding="UTF-8"?><model unit="${exportUnit}" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources><object id="1" type="model"><mesh><vertices>${v}</vertices><triangles>${t}</triangles></mesh></object></resources><build><item objectid="1" /></build></model>`;
    return xml;
}
