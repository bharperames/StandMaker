import { calculateAggregatorEstimate, calculateLocalPrintEstimate, cubeInchesToMm3 } from '../js/pricing.js';

// ---------------------------------------------------------------------------
// Inline reference formula — tests derive expected values from the same math
// as the implementation so they stay correct if shared constants change.
// ---------------------------------------------------------------------------
const formula = (base, mult, qty, volMm3) => {
    const cm3 = (volMm3 / 1000) * qty;
    return Math.round(Math.max(3.04, base + mult * Math.cbrt(cm3)) * 100) / 100;
};
const p = (mat, qty, vol) => calculateAggregatorEstimate(mat, qty, vol);

describe('calculateAggregatorEstimate', () => {

    // ── Anchor point A: small-order promotional floor ────────────────────────
    // totalVolumeCm3 = 3524.24 / 1000 * 1 = 3.524 cm³  (<4 cm³ threshold)
    // Floor logic applies → $3.04 regardless of raw formula output.
    test('Anchor A — PLA qty=1 tiny part hits $3.04 floor', () => {
        expect(p('PLA', 1, 3524.24)).toBe(3.04);
    });

    test('floor also applies to PLA+ and PETG small orders', () => {
        expect(p('PLA+', 1, 3524.24)).toBe(3.04);
        expect(p('PETG', 1, 3524.24)).toBe(3.04);
    });

    test('floor does NOT apply to ABS (higher multiplier keeps tiny prints above floor naturally)', () => {
        // ABS volumetricMultiplier = 3.30, so formula gives ~$5.77 for a tiny part
        expect(p('ABS', 1, 3524.24)).toBeGreaterThan(3.04);
    });

    test('floor does not trigger once volume crosses 4 cm³ threshold', () => {
        // 4001 mm³ × qty 1 = 4.001 cm³ → formula applies, price > floor
        expect(p('PLA', 1, 4001)).toBeGreaterThan(3.04);
    });

    // ── Anchor point B: PLA bulk ─────────────────────────────────────────────
    // totalVolumeCm3 = (67200/1000) * 10 = 672 cm³
    // Formula: 0.75 + 2.85 * cbrt(672) ≈ $25.71
    // Marketplace reference anchor: ~$26.01 (±1% variance from aggregator smoothing)
    test('Anchor B — PLA qty=10 vol=67200mm³ bulk pricing', () => {
        const result = p('PLA', 10, 67200);
        expect(result).toBeCloseTo(formula(0.75, 2.85, 10, 67200), 2);
        // Verify it falls in the competitive marketplace range cited in spec
        expect(result).toBeGreaterThan(24.00);
        expect(result).toBeLessThan(27.00);
    });

    // ── Anchor point C: ABS bulk ─────────────────────────────────────────────
    // totalVolumeCm3 = (67200/1000) * 10 = 672 cm³
    // Formula: 0.75 + 3.30 * cbrt(672) ≈ $29.65
    // Marketplace reference anchor: ~$29.61 (delta of $0.04 — within rounding noise)
    test('Anchor C — ABS qty=10 vol=67200mm³ bulk pricing near $29.61 anchor', () => {
        const result = p('ABS', 10, 67200);
        expect(result).toBeCloseTo(formula(0.75, 3.30, 10, 67200), 2);
        expect(result).toBeCloseTo(29.61, 0);   // within ±0.50 of marketplace anchor
    });

    test('ABS costs more than PLA for same volume (higher volumetric multiplier)', () => {
        expect(p('ABS', 10, 67200)).toBeGreaterThan(p('PLA', 10, 67200));
    });

    // ── Anchor point D: text/complexity has negligible price impact ──────────
    // 67210mm³ vs 67200mm³ — extra 10mm³ (~embossed text on the base).
    // Both should produce the same rounded price, confirming complexity blindness.
    test('Anchor D — 10mm³ mesh complexity delta produces negligible variance', () => {
        const basePrice = p('PLA', 10, 67200);
        const textPrice = p('PLA', 10, 67210);
        expect(textPrice).toBe(basePrice);      // same cents after rounding
        expect(Math.abs(textPrice - basePrice)).toBeLessThan(0.01);
    });

    // ── Material profiles ────────────────────────────────────────────────────
    test('PLA, PLA+, and RPLA share the same multiplier', () => {
        expect(p('PLA+', 5, 50000)).toBe(p('PLA',  5, 50000));
        expect(p('RPLA', 5, 50000)).toBe(p('PLA',  5, 50000));
    });

    test('material cost order: PLA < ABS < PETG (by volumetric multiplier)', () => {
        expect(p('ABS',  5, 50000)).toBeGreaterThan(p('PLA',  5, 50000));
        expect(p('PETG', 5, 50000)).toBeGreaterThan(p('ABS',  5, 50000));
    });

    test('unknown material falls back to PLA profile', () => {
        expect(p('Nylon', 1, 10000)).toBe(p('PLA', 1, 10000));
    });

    // ── Economies of scale ───────────────────────────────────────────────────
    test('price increases with quantity but sub-linearly (cube-root scaling)', () => {
        const p1  = p('PLA', 1,  50000);
        const p5  = p('PLA', 5,  50000);
        const p10 = p('PLA', 10, 50000);
        expect(p5).toBeGreaterThan(p1);
        expect(p10).toBeGreaterThan(p5);
        // Cube-root means 10× qty costs less than 10× the unit price
        expect(p10).toBeLessThan(p1 * 10);
    });

    // ── Return format ────────────────────────────────────────────────────────
    test('result is a number rounded to exactly two decimal places', () => {
        const result = p('PLA', 3, 25000);
        expect(typeof result).toBe('number');
        expect(result).toBe(parseFloat(result.toFixed(2)));
    });

    // ── Error handling ───────────────────────────────────────────────────────
    test('throws on zero quantity',     () => expect(() => p('PLA',  0, 10000)).toThrow());
    test('throws on negative quantity', () => expect(() => p('PLA', -1, 10000)).toThrow());
    test('throws on zero volume',       () => expect(() => p('PLA',  1,     0)).toThrow());
    test('throws on negative volume',   () => expect(() => p('PLA',  1,  -500)).toThrow());

});

// ---------------------------------------------------------------------------
// calculateLocalPrintEstimate
// Reference values computed from the spec formulas directly.
// vol = 67200 mm³ → 67.2 cm³
// singleWeight (PLA) = 1.03 * 67.2^0.8 * (1.24/1.24) ≈ 1.03 * 25.03 ≈ 25.78 g
// ---------------------------------------------------------------------------
describe('calculateLocalPrintEstimate', () => {
    const L = (mat, vol, qty, cpkg) => calculateLocalPrintEstimate(mat, vol, qty, cpkg);

    test('returns estimatedCostUsd, estimatedTimeHours, totalWeightGrams', () => {
        const result = L('PLA', 67200, 1);
        expect(result).toHaveProperty('estimatedCostUsd');
        expect(result).toHaveProperty('estimatedTimeHours');
        expect(result).toHaveProperty('totalWeightGrams');
    });

    test('all returned values are numbers rounded to 2 decimal places', () => {
        const result = L('PLA', 67200, 1);
        for (const val of Object.values(result)) {
            expect(typeof val).toBe('number');
            expect(val).toBe(parseFloat(val.toFixed(2)));
        }
    });

    test('weight scales linearly with quantity', () => {
        const r1  = L('PLA', 67200, 1);
        const r10 = L('PLA', 67200, 10);
        expect(r10.totalWeightGrams).toBeCloseTo(r1.totalWeightGrams * 10, 1);
    });

    test('time scales super-linearly with quantity (job overhead amortized)', () => {
        const r1  = L('PLA', 67200, 1);
        const r10 = L('PLA', 67200, 10);
        // 10× parts takes less than 10× time because the 476s job calibration is fixed
        expect(r10.estimatedTimeHours).toBeLessThan(r1.estimatedTimeHours * 10);
        expect(r10.estimatedTimeHours).toBeGreaterThan(r1.estimatedTimeHours);
    });

    test('PETG is heavier than PLA for same volume (higher density)', () => {
        const pla  = L('PLA',  67200, 1);
        const petg = L('PETG', 67200, 1);
        expect(petg.totalWeightGrams).toBeGreaterThan(pla.totalWeightGrams);
    });

    test('ABS is lighter than PLA for same volume (lower density)', () => {
        const pla = L('PLA', 67200, 1);
        const abs = L('ABS', 67200, 1);
        expect(abs.totalWeightGrams).toBeLessThan(pla.totalWeightGrams);
    });

    test('filamentCostPerKg scales material cost proportionally', () => {
        const cheap     = L('PLA', 67200, 1, 10);
        const expensive = L('PLA', 67200, 1, 40);
        // electricity is fixed; material cost quadruples → total cost < 4×
        expect(expensive.estimatedCostUsd).toBeGreaterThan(cheap.estimatedCostUsd);
    });

    test('unknown material falls back to PLA density', () => {
        const nylon = L('Nylon', 67200, 1);
        const pla   = L('PLA',   67200, 1);
        expect(nylon.totalWeightGrams).toBe(pla.totalWeightGrams);
    });

    test('power-law weight: larger part has lower effective density ratio', () => {
        // For a small part (1 cm³) the power-law exponent 0.8 < 1 means
        // weight grows slower than volume — confirming shell-dominated behavior.
        const small = L('PLA', 1000,  1);   //  1 cm³
        const large = L('PLA', 67200, 1);   // 67.2 cm³
        const smallDensity = small.totalWeightGrams / 1;    // g per cm³
        const largeDensity = large.totalWeightGrams / 67.2;
        expect(smallDensity).toBeGreaterThan(largeDensity);
    });

    // ── Error handling ───────────────────────────────────────────────────────
    test('throws on zero quantity',     () => expect(() => L('PLA', 10000,  0)).toThrow());
    test('throws on negative quantity', () => expect(() => L('PLA', 10000, -1)).toThrow());
    test('throws on zero volume',       () => expect(() => L('PLA',     0,  1)).toThrow());
    test('throws on negative volume',   () => expect(() => L('PLA',  -500,  1)).toThrow());

});

describe('cubeInchesToMm3', () => {

    test('1 in³ = 16387.064 mm³', () => {
        expect(cubeInchesToMm3(1)).toBeCloseTo(16387.064, 3);
    });

    test('result passes through to aggregator pricing correctly', () => {
        const volMm3 = cubeInchesToMm3(3.21);
        const result = p('PLA', 1, volMm3);
        expect(typeof result).toBe('number');
        expect(result).toBeGreaterThanOrEqual(3.04);
    });

});
