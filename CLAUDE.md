# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm test        # Run all Jest tests
npm start       # Serve locally via npx serve .
make test       # Alias for npm test
make serve      # Alias for npm start
```

Run a single test file:
```bash
node --experimental-vm-modules node_modules/jest/bin/jest.js tests/math_logic.test.js
```

`--experimental-vm-modules` is required because the project uses ES modules (`"type": "module"` in package.json).

## Architecture

A single-page web app for designing 3D-printable sphere display stands. Users configure dimensions via sliders, preview in real-time with Three.js, and export to 3MF or STL.

### File overview

- **`index.html`** — The entire application (~2000 lines). Contains all CSS, Three.js scene setup, OrbitControls, material/texture/lighting systems, UI event handlers, geometry constraint enforcement, dimension overlay rendering, localStorage config persistence, and export orchestration. All DOM and Three.js interactions live here.
- **`js/math_logic.js`** — Pure exported functions, no DOM or Three.js dependencies. Tested directly by Jest.
- **`js/export_3mf.js`** — Pure function `generate3MFXML(positions, indices, exportUnit)`. Takes Three.js geometry arrays, deduplicates vertices, swaps Y/Z axes for the 3MF coordinate system, returns XML string.
- **`tests/math_logic.test.js`** — Jest tests for all math_logic.js exports.
- **`tests/export_3mf.test.js`** — Jest tests for generate3MFXML.

### math_logic.js exports

| Function | Purpose |
|---|---|
| `calculateMaxBase(diameter, thickness)` | Max safe base radius before stand traps the sphere |
| `calculateAbsoluteMaxChamfer(diameter, baseSize, thickness, seatingHeight)` | Max chamfer before outer geometry drops below z=0 |
| `calculateContactArcLength(diameter, baseSize, thickness, chamfer)` | Arc length where sphere surface contacts the stand rim |
| `calculateAutoOptimize(diameter)` | Returns `{ baseSize, thickness, seatingHeight, chamfer }` optimal for a given diameter |
| `calculateAutoDensity(baseSize, thickness)` | Segment count for smooth tessellation, rounded to nearest 8, clamped 32–256 |
| `calculateTipFactor(diameter, baseSize, thickness, chamfer)` | Returns `{ tipAngle, overhangPercent, assessment, color }` — tipping angle is `arctan(rcActive / sqrt(R²-rcActive²))`; overhang is `(1-(rcActive/R)²)^1.5 × 100%` |
| `deduplicateGeometry(positions, indices)` | Welds UV seam vertices (rounds to 6 decimal places) to produce a globally manifold mesh for 3MF validation |
| `buildTopologyFromIndices(indices)` | Converts flat index buffer to `[v1,v2,v3]` triangle list |
| `verifyManifold(triangles)` | Returns `{ isManifold, openEdges, nonManifoldEdges }` — every edge must appear exactly twice for a valid solid |

### Key geometry parameters

All sliders are interdependent. Constraint enforcement runs on every change:
- `baseSize` is clamped by `calculateMaxBase` (prevents stand from trapping the sphere past its equator)
- `chamfer` is clamped by `calculateAbsoluteMaxChamfer` (prevents geometry inverting below z=0)
- `seatingHeight` is the vertical clearance between the stand base and the bottom of the sphere
- Contact radius for tipping analysis: `rcActive = max(0, baseSize + thickness/2 - chamfer)`

### index.html systems

- **Geometry rebuild** — triggered on every slider change; rebuilds Three.js BufferGeometry, runs manifold verification, updates all assessment labels (Solidity, Stability, Tessellation Granularity)
- **Stability assessment** — calls `calculateTipFactor`; drives the colored gauge bar (0°–90° tipping angle scale: red < 25° / yellow 25–40° / green 40–60° / blue > 60°)
- **Texture system** — built-in mineral textures (loaded as base64 data URLs) plus custom photo upload; sphere material switches between wireframe, photo, and solid modes
- **Dimension overlays** — `buildDim()` / `makeTextSprite()` draw 3D measurement annotations toggled by a checkbox
- **Export** — `download3MF()` calls `generate3MFXML` then packages it into a ZIP via JSZip; `downloadSTL()` writes a binary STL directly
- **Persistence** — `saveConfig()` / `loadConfig()` round-trip all slider values and camera position through localStorage
