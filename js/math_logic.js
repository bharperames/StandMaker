/**
 * math_logic.js
 * Extracted pure logic for the Sphere Stand Generator.
 * These functions have no dependencies on DOM or Three.js and can be easily tested.
 */

/**
 * Calculates the maximum mathematically safe base size for a given sphere diameter and wall thickness.
 * @param {number} diameter - Sphere outer diameter (mm).
 * @param {number} thickness - Wall thickness (mm).
 * @returns {number} The maximum base size radius (mm).
 */
export function calculateMaxBase(diameter, thickness) {
    const RSphere = diameter / 2;
    // (baseSize - thickness/2 < R_sphere) => baseSize < R_sphere + thickness/2
    return RSphere + (thickness / 2) - 0.1;
}

/**
 * Iteratively calculates the maximum safe chamfer that doesn't push the outer geometry below the z-axis.
 * @param {number} diameter - Sphere outer diameter (mm).
 * @param {number} baseSize - Base size horizontal width (mm).
 * @param {number} thickness - Wall thickness (mm).
 * @param {number} seatingHeight - Stand vertical seating height clearance (mm).
 * @returns {number} The maximum allowable chamfer (mm).
 */
export function calculateAbsoluteMaxChamfer(diameter, baseSize, thickness, seatingHeight) {
    const RSphere = diameter / 2;
    const zOffset = RSphere + seatingHeight;
    const RInner = baseSize - (thickness / 2);
    const realROuter = baseSize + (thickness / 2);

    const actualWallThickness = realROuter - Math.max(0, RInner);
    let absoluteMaxChamfer = actualWallThickness - 0.1;

    const ySphere = (rx) => zOffset - Math.sqrt(Math.max(0, RSphere ** 2 - Math.min(RSphere, rx) ** 2));

    for (let testC = 0.1; testC <= absoluteMaxChamfer; testC += 0.1) {
        let rc = Math.max(0, realROuter - testC);
        let yOuterTest = ySphere(rc) - testC;
        if (yOuterTest < 0) {
            absoluteMaxChamfer = Math.max(0, testC - 0.1);
            break;
        }
    }
    return absoluteMaxChamfer;
}

/**
 * Calculates the arc length of the sphere in contact with the stand.
 * @param {number} diameter - Sphere outer diameter (mm).
 * @param {number} baseSize - Base size horizontal width (mm).
 * @param {number} thickness - Wall thickness (mm).
 * @param {number} chamfer - The active chamfer size (mm).
 * @returns {number} Contact arc length (mm).
 */
export function calculateContactArcLength(diameter, baseSize, thickness, chamfer) {
    const RSphere = diameter / 2;
    const RInner = baseSize - (thickness / 2);
    const realROuter = baseSize + (thickness / 2);
    const rcActive = Math.max(0, realROuter - chamfer);
    
    const angleIn = Math.asin(Math.min(1.0, Math.max(0, RInner) / RSphere));
    const angleOut = Math.asin(Math.min(1.0, rcActive / RSphere));
    
    return RSphere * Math.max(0, angleOut - angleIn);
}

/**
 * Provides the optimal geometry dimensions based on the input sphere diameter.
 * @param {number} diameter - Sphere outer diameter (mm).
 * @returns {Object} { baseSize, thickness, seatingHeight, chamfer } in mm.
 */
export function calculateAutoOptimize(diameter) {
    return {
        seatingHeight: 1.0,
        baseSize: (diameter / 2) * 0.707,
        thickness: diameter * 0.1,
        chamfer: (diameter * 0.1) * 0.3
    };
}

/**
 * Calculates the optimal number of segments (tessellation density) for visual smoothness.
 * @param {number} baseSize - Base size horizontal width (mm).
 * @param {number} thickness - Wall thickness (mm).
 * @returns {number} Optimal segment count (rounded to nearest 8).
 */
export function calculateAutoDensity(baseSize, thickness) {
    const ROuter = baseSize + (thickness / 2);
    let optimalN = Math.ceil(Math.PI / Math.acos(1 - 0.025 / ROuter));
    return Math.min(256, Math.max(32, Math.ceil(optimalN / 8) * 8));
}

/**
 * Computes the volume of a closed manifold mesh using the signed tetrahedron method
 * (divergence theorem). Each triangle contributes a signed tetrahedral volume from
 * the origin; summing and taking the absolute value gives the enclosed volume.
 * @param {Float32Array|Array} positions - Flat vertex array [x0,y0,z0, x1,y1,z1, ...] in mm.
 * @param {Uint16Array|Uint32Array|Array} indices - Triangle index buffer.
 * @returns {number} Volume in mm³.
 */
export function computeMeshVolumeMm3(positions, indices) {
    let volume = 0;
    for (let i = 0; i < indices.length; i += 3) {
        const i0 = indices[i] * 3, i1 = indices[i + 1] * 3, i2 = indices[i + 2] * 3;
        const x0 = positions[i0], y0 = positions[i0 + 1], z0 = positions[i0 + 2];
        const x1 = positions[i1], y1 = positions[i1 + 1], z1 = positions[i1 + 2];
        const x2 = positions[i2], y2 = positions[i2 + 1], z2 = positions[i2 + 2];
        volume += (1 / 6) * (
            x0 * (y1 * z2 - y2 * z1) -
            x1 * (y0 * z2 - y2 * z0) +
            x2 * (y0 * z1 - y1 * z0)
        );
    }
    return Math.abs(volume);
}

/**
 * Computes the total surface area of a mesh by summing triangle areas.
 * @param {Float32Array|Array} positions - Flat vertex array [x0,y0,z0,...] in mm.
 * @param {Uint16Array|Uint32Array|Array} indices - Triangle index buffer.
 * @returns {number} Total surface area in mm².
 */
export function computeMeshSurfaceAreaMm2(positions, indices) {
    let area = 0;
    for (let i = 0; i < indices.length; i += 3) {
        const i0 = indices[i] * 3, i1 = indices[i + 1] * 3, i2 = indices[i + 2] * 3;
        const ax = positions[i1]     - positions[i0],     ay = positions[i1 + 1] - positions[i0 + 1], az = positions[i1 + 2] - positions[i0 + 2];
        const bx = positions[i2]     - positions[i0],     by = positions[i2 + 1] - positions[i0 + 1], bz = positions[i2 + 2] - positions[i0 + 2];
        const cx = ay * bz - az * by, cy = az * bx - ax * bz, cz = ax * by - ay * bx;
        area += 0.5 * Math.sqrt(cx * cx + cy * cy + cz * cz);
    }
    return area;
}

/**
 * Calculates the tip factor for a sphere resting on the stand.
 * The tipping angle is how far the sphere must tilt before its center of gravity
 * passes over the outer rim edge and it falls off. The overhang percent is the
 * fraction of sphere volume cantilevered beyond that outer rim.
 * @param {number} diameter - Sphere outer diameter (mm).
 * @param {number} baseSize - Base size horizontal width (mm).
 * @param {number} thickness - Wall thickness (mm).
 * @param {number} chamfer - The active chamfer size (mm).
 * @returns {{ tipAngle: number, overhangPercent: number, assessment: string, color: string }}
 */
export function calculateTipFactor(diameter, baseSize, thickness, chamfer) {
    const RSphere = diameter / 2;
    const ROuter = baseSize + (thickness / 2);
    // rcActive is the outermost contact radius after chamfer — the pivot point for tipping
    const rcActive = Math.min(RSphere * 0.9999, Math.max(0, ROuter - chamfer));

    // Angle sphere must tilt before CoG passes over outer rim: arctan(r / h_above_rim)
    const hAboveRim = Math.sqrt(RSphere ** 2 - rcActive ** 2);
    const tipAngle = Math.atan2(rcActive, hAboveRim) * (180 / Math.PI);

    // Volume fraction of sphere outside the cylinder of radius rcActive (closed-form integral)
    const overhangPercent = Math.pow(1 - (rcActive / RSphere) ** 2, 1.5) * 100;

    let assessment, color;
    if (tipAngle < 25)      { assessment = "UNSTABLE";  color = "#ef4444"; }
    else if (tipAngle < 40) { assessment = "LOW";       color = "#f59e0b"; }
    else if (tipAngle < 60) { assessment = "OPTIMAL";   color = "#10b981"; }
    else                    { assessment = "OVERSIZED"; color = "#3b82f6"; }

    return { tipAngle, overhangPercent, assessment, color };
}

/**
 * Procedural generation (like Three.js SphereGeometry) often outputs unstitched "seams" 
 * where indices do not connect even if their spatial coordinates are mathematically identical.
 * This exact topological deduplication stitches those micro-seams into a globally manifold object,
 * preparing it perfectly for strict 3MF validation by CraftCloud.
 */
export function deduplicateGeometry(positions, indices) {
    const uniqueVertices = [];
    const posMap = new Map();
    const indexRemap = [];
    let vCount = 0;

    for (let i = 0; i < positions.length; i += 3) {
        // We round to 6 decimal places (1e6) to weld UV seams (e.g. angle 0 vs 2*PI) 
        // strictly while avoiding the collapse of micro-bevels (which broke at 4 decimal places). 
        // We also explicitly map -0 to 0 because JS Map keys treat '-0' and '0' as distinct strings.
        const cleanCoord = (val) => {
             let r = Math.round(val * 1000000) / 1000000;
             if (r === -0) return 0;
             return r;
        };

        const x = cleanCoord(positions[i]);
        const y = cleanCoord(positions[i + 1]);
        const z = cleanCoord(positions[i + 2]);
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

    const remappedIndices = new Uint32Array(indices.length);
    for (let i = 0; i < indices.length; i += 3) {
        remappedIndices[i] = indexRemap[indices[i]];
        remappedIndices[i + 1] = indexRemap[indices[i + 1]];
        remappedIndices[i + 2] = indexRemap[indices[i + 2]];
    }

    return { uniqueVertices, indexRemap, remappedIndices };
}

/**
 * Utility to parse an array of 16-bit or 32-bit indices exactly as they will be exported,
 * interpreting them into independent `[v1, v2, v3]` arrays representing the final surface topology.
 * @param {Array|Uint16Array|Uint32Array} indices - The mesh triangle indices.
 * @returns {Array} List of [v1, v2, v3] arrays.
 */
export function buildTopologyFromIndices(indices) {
    const triangles = [];
    for (let i = 0; i < indices.length; i += 3) {
        triangles.push([indices[i], indices[i+1], indices[i+2]]);
    }
    return triangles;
}

/**
 * Validates whether an array of triangles represents a closed 2-manifold surface.
 * For the mesh to be solid and watertight, every non-degenerate structural edge 
 * must be shared precisely twice (meaning 0 open holes, 0 intersecting boundaries).
 * @param {Array} triangles List of [v1, v2, v3] arrays.
 * @returns {Object} Result of validation { isManifold: boolean, openEdges: number, nonManifoldEdges: number }
 */
export function verifyManifold(triangles) {
    const edgeCounts = new Map();

    const getEdgeKey = (a, b) => {
        return a < b ? `${a}-${b}` : `${b}-${a}`;
    };

    for (const tri of triangles) {
        if (tri[0] === tri[1] || tri[1] === tri[2] || tri[0] === tri[2]) {
            continue;
        }

        const edges = [
            getEdgeKey(tri[0], tri[1]),
            getEdgeKey(tri[1], tri[2]),
            getEdgeKey(tri[2], tri[0])
        ];

        for (const edge of edges) {
            edgeCounts.set(edge, (edgeCounts.get(edge) || 0) + 1);
        }
    }

    let openEdges = 0;
    let nonManifoldEdges = 0;

    for (const count of edgeCounts.values()) {
        if (count === 1) {
            openEdges++;
        } else if (count > 2) {
            nonManifoldEdges++;
        }
    }

    return {
        isManifold: openEdges === 0 && nonManifoldEdges === 0,
        openEdges,
        nonManifoldEdges
    };
}
