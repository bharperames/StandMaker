import { generate3MFXML } from '../js/export_3mf.js';

describe('3MF Headless Export logic', () => {

  test('generate3MFXML creates valid deduplicated XML string', () => {
    // A simple mock square made of two triangles sharing a diagonal edge
    // By providing 6 raw vertices instead of 4, we test the deduplication engine
    const mockPositions = [
        0, 0, 0,  // v0
        10, 0, 0, // v1 
        10, 10, 0, // v2 

        0, 0, 0,  // v3 (duplicate of v0)
        10, 10, 0, // v4 (duplicate of v2)
        0, 10, 0  // v5
    ];

    const mockIndices = [
        0, 1, 2,  // Triangle 1
        3, 4, 5   // Triangle 2
    ];

    const resultXML = generate3MFXML(mockPositions, mockIndices);

    // Tests that the XML document is structured correctly
    expect(resultXML).toContain('<?xml version="1.0" encoding="UTF-8"?>');
    expect(resultXML).toContain('<model unit="millimeter"');
    
    // Tests Deduplication Logic: 
    // Even though 6 vertices were submitted, only 4 unique coordinates exist
    // so there should only be 4 <vertex> tags in the final XML.
    const vertexMatches = resultXML.match(/<vertex /g) || [];
    expect(vertexMatches.length).toBe(4);

    // Test that the exact correct deduplicated indices are remapped into the triangle
    // For Triangle 2 (originally 3, 4, 5), they should remap to absolute indices 0, 2, 3
    // Note: Due to pure +90X rotation for Z-up mapping, winding order is naturally preserved.
    expect(resultXML).toContain('<triangle v1="0" v2="2" v3="3" />');
  });

  test('generate3MFXML retains degenerate triangles to preserve topological manifolds', () => {
     const mockPositions = [
        0, 0, 0,  
        10, 0, 0,  
        10, 10, 0 
    ];

    // A completely flat, degenerate triangle where two points are identical 
    const mockIndices = [
        0, 1, 1 
    ];

    const resultXML = generate3MFXML(mockPositions, mockIndices);
    
    // We no longer skip degenerate triangles to ensure we don't tear open non-manifold holes.
    // The <triangles> block should contain the degenerate triangle.
    // Note: Winding order swap means v1="0" v2="1" v3="1" becomes v1="0" v2="1" v3="1".
    expect(resultXML).toContain('<triangle v1="0" v2="1" v3="1" />');
  });

  test('generate3MFXML throws error on bad input', () => {
      expect(() => generate3MFXML(null, null)).toThrow('Invalid geometry');
      expect(() => generate3MFXML([], [])).toThrow('Invalid geometry');
  });

});
