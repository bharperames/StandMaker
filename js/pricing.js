/**
 * pricing.js
 * Definitive pricing estimation module for a 3D printing application.
 * Coefficients are reverse-engineered from marketplace data.
 *
 * Formula:
 *   TotalVolumeCm3 = (singlePartVolumeMm3 / 1000) * quantity
 *   Price = material.baseSetupFee + material.volumetricMultiplier * cbrt(TotalVolumeCm3)
 *
 * Pricing is strictly volume-driven. Mesh complexity, poly count, text
 * emboss/engrave geometry, and vertex count never affect the estimate.
 * Cube-root scaling provides natural economies of scale for bulk orders.
 */

/** Minimum advertised price for any non-ABS order. */
const MIN_PRICE = 3.04;

/**
 * Total job volume threshold (cm³) below which non-ABS orders are anchored
 * to MIN_PRICE as a promotional floor rather than applying the raw formula.
 */
const SMALL_ORDER_THRESHOLD_CM3 = 4.0;

const IN3_TO_MM3 = 16387.064;

// Definitive material coefficients reverse-engineered from marketplace data.
const materialProfiles = {
    'PLA':             { baseSetupFee: 0.75, volumetricMultiplier: 2.85 },
    'PLA+':            { baseSetupFee: 0.75, volumetricMultiplier: 2.85 },
    'RPLA':            { baseSetupFee: 0.75, volumetricMultiplier: 2.85 },
    'PETG':            { baseSetupFee: 0.75, volumetricMultiplier: 3.40 },
    'ABS':             { baseSetupFee: 0.75, volumetricMultiplier: 3.30 },
    'fallback_default':{ baseSetupFee: 0.75, volumetricMultiplier: 2.85 },
};

/**
 * Converts cubic inches to cubic millimeters.
 * Use this before passing imperial-unit volumes to calculateEstimatedPrice.
 * @param {number} cubicInches - Volume in in³.
 * @returns {number} Equivalent volume in mm³.
 */
export function cubeInchesToMm3(cubicInches) {
    return cubicInches * IN3_TO_MM3;
}

/**
 * Calculates the estimated cost of a 3D print job.
 *
 * @param {string} material             - Material key ('PLA', 'PLA+', 'RPLA', 'PETG', 'ABS').
 *                                        Unknown materials fall back to the PLA profile.
 * @param {number} quantity             - Number of parts. Must be > 0.
 * @param {number} singlePartVolumeMm3  - Volume of one part in mm³. Must be > 0.
 *                                        Use cubeInchesToMm3() to convert from in³ first.
 * @returns {number} Estimated cost in USD, rounded to two decimal places.
 * @throws {Error} If quantity or singlePartVolumeMm3 are not positive numbers.
 */
export function calculateEstimatedPrice(material, quantity, singlePartVolumeMm3) {
    if (!Number.isFinite(quantity) || quantity <= 0) {
        throw new Error(`quantity must be a positive number, got: ${quantity}`);
    }
    if (!Number.isFinite(singlePartVolumeMm3) || singlePartVolumeMm3 <= 0) {
        throw new Error(`singlePartVolumeMm3 must be a positive number, got: ${singlePartVolumeMm3}`);
    }

    const profile        = materialProfiles[material] ?? materialProfiles['fallback_default'];
    const totalVolumeCm3 = (singlePartVolumeMm3 / 1000) * quantity;

    // Small-order promotional floor: for non-ABS jobs where the total job volume is
    // under 4 cm³, anchor to MIN_PRICE rather than applying the raw formula.
    if (material !== 'ABS' && totalVolumeCm3 < SMALL_ORDER_THRESHOLD_CM3) {
        return MIN_PRICE;
    }

    const rawPrice = profile.baseSetupFee + profile.volumetricMultiplier * Math.cbrt(totalVolumeCm3);
    return Math.round(Math.max(MIN_PRICE, rawPrice) * 100) / 100;
}
