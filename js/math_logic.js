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
