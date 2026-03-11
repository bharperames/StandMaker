import {
  calculateMaxBase,
  calculateAbsoluteMaxChamfer,
  calculateContactArcLength,
  calculateAutoOptimize,
  calculateAutoDensity,
  calculateTipFactor
} from '../js/math_logic.js';

describe('Math Logic Unit Tests', () => {
  
  test('calculateMaxBase', () => {
    // 50mm sphere, 5mm wall thickness
    // max_base = 25 + 2.5 - 0.1 = 27.4
    expect(calculateMaxBase(50, 5)).toBeCloseTo(27.4, 1);

    // 100mm sphere, 10mm wall thickness
    // max_base = 50 + 5 - 0.1 = 54.9
    expect(calculateMaxBase(100, 10)).toBeCloseTo(54.9, 1);
  });

  test('calculateAbsoluteMaxChamfer', () => {
    // 50mm sphere, 27.4mm base, 5mm wall, 2mm clearance
    // Ensures that chamfer does not exceed wall thickness 
    const chamfer = calculateAbsoluteMaxChamfer(50, 27.4, 5, 2.0);
    expect(chamfer).toBeLessThanOrEqual(4.9);
    expect(chamfer).toBeGreaterThan(0);
    
    // Test extreme case where chamfer might cause y to go negative
    const chamferExtreme = calculateAbsoluteMaxChamfer(50, 27.4, 15, 0.5);
    expect(chamferExtreme).toBeLessThanOrEqual(14.9);
  });

  test('calculateContactArcLength', () => {
    // 50mm sphere, 20mm base, 5mm wall, 2mm chamfer
    // RInner = 17.5, ROuter = 22.5, rcActive = 20.5
    // angleIn = asin(17.5 / 25) = 44.42 deg
    // angleOut = asin(20.5 / 25) = 55.08 deg
    // arc length = 25 * (angleOut - angleIn) in rad
    const arcLength = calculateContactArcLength(50, 20, 5, 2);
    expect(arcLength).toBeGreaterThan(0);
    expect(arcLength).toBeCloseTo(4.65, 1);
  });

  test('calculateAutoOptimize', () => {
    const opts = calculateAutoOptimize(50);
    expect(opts.seatingHeight).toBe(1.0);
    expect(opts.baseSize).toBeCloseTo(17.675, 2);
    expect(opts.thickness).toBe(5);
    expect(opts.chamfer).toBe(1.5);
  });

  test('calculateAutoDensity', () => {
    // baseSize = 20, thickness = 5 => ROuter = 22.5
    // arccos(1 - 0.025/22.5) = arccos(0.99888) = 0.04712 rad
    // Pi / 0.04712 = 66.6
    // ceil to nearest 8 => 72
    const n = calculateAutoDensity(20, 5);
    expect(n % 8).toBe(0); // Should be a multiple of 8
    expect(n).toBe(72);
  });

  test('calculateTipFactor', () => {
    // 50mm sphere, 20mm base, 5mm wall, 2mm chamfer
    // ROuter = 22.5, rcActive = 20.5
    // tipAngle = atan(20.5 / sqrt(625 - 420.25)) = atan(20.5 / 14.31) ≈ 55.1°  => OPTIMAL
    // overhangPercent = (1 - (20.5/25)^2)^1.5 * 100 ≈ 18.8%
    const r1 = calculateTipFactor(50, 20, 5, 2);
    expect(r1.tipAngle).toBeCloseTo(55.1, 0);
    expect(r1.overhangPercent).toBeCloseTo(18.8, 0);
    expect(r1.assessment).toBe('OPTIMAL');

    // 50mm sphere, 15mm base, 5mm wall, 0mm chamfer
    // ROuter = 17.5, rcActive = 17.5
    // tipAngle = atan(17.5 / sqrt(625 - 306.25)) = atan(17.5 / 17.85) ≈ 44.4°  => OPTIMAL
    // overhangPercent = (1 - (17.5/25)^2)^1.5 * 100 ≈ 36.4%
    const r2 = calculateTipFactor(50, 15, 5, 0);
    expect(r2.tipAngle).toBeCloseTo(44.4, 0);
    expect(r2.overhangPercent).toBeCloseTo(36.4, 0);
    expect(r2.assessment).toBe('OPTIMAL');

    // Very narrow base — sphere balanced on near-point, should be UNSTABLE
    const r3 = calculateTipFactor(50, 5, 1, 0);
    expect(r3.tipAngle).toBeLessThan(25);
    expect(r3.assessment).toBe('UNSTABLE');
    expect(r3.overhangPercent).toBeGreaterThan(90);

    // tipAngle and overhangPercent always in valid ranges
    const r4 = calculateTipFactor(100, 40, 8, 3);
    expect(r4.tipAngle).toBeGreaterThan(0);
    expect(r4.tipAngle).toBeLessThan(90);
    expect(r4.overhangPercent).toBeGreaterThanOrEqual(0);
    expect(r4.overhangPercent).toBeLessThanOrEqual(100);
  });

});