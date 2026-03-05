# Sphere Stand Generator Configuration

This document outlines the minimum and maximum physical limits for the configurable dimensions in the Sphere Stand Generator, along with the mathematical inter-dependencies that prevent physically impossible meshes from generating.

## Configuration Parameters

### 1. Sphere Diameter
*   **Min**: 5 mm
*   **Max**: 500 mm
*   **Dependencies**: This is the master reference variable. It dictates the maximum viable limits for almost everything else. If you shrink the diameter significantly, it will force the **Base Size** to scale down with it, because the stand's base mathematically cannot be wider than the physical sphere it's supporting (plus the wall thickness).

### 2. Sphere Height (Z-Clearance)
*   **Min**: 2.0 mm
*   **Max**: 100 mm 
*   **Dependencies**: This acts mostly independently as a vertical Z-offset for the sphere's geometric origin point. However, it implicitly affects the **Sphere Contact Arc Length** calculations. If you raise the sphere incredibly high while keeping the Base Size small, the stand will mathematically have to generate a taller, steeper inner support ring to reach it. This physically reduces the surface area where the sphere touches the stand, destabilizing the print.

### 3. Base Size
*   **Min**: 5 mm
*   **Max**: 300 mm
*   **Dependencies**: Highly interconnected. The geometry engine enforces a strict maximum rule: `baseSize < (Sphere Radius) + (Wall Thickness / 2)`. 
    *   **Side Effect:** If you manually increase the Base Size slider beyond the mathematical radius of your sphere, the engine will instantly override your manual input and snap the slider back down to the maximum mathematically safe limit. This physically prevents the stand walls from protruding horizontally past the "equator" of the sphere, which would trap the sphere permanently inside the print.

### 4. Wall Thickness
*   **Min**: 0.5 mm
*   **Max**: 50 mm
*   **Dependencies**: Acts as a subtle modifier for the maximum Base Size, but its primary function is a hard maximum limit on the **Top Edge Chamfer**.
    *   **Side Effect**: Because the chamfer geometry is an angled geometric cut carved out of the outer wall mesh, the code strictly enforces that `chamferLimit = thickness - 0.1`. If you shrink your Wall Thickness slider down to `2mm`, your Chamfer slider will automatically hit an invisible brick wall at `1.9mm` to prevent non-manifold meshes.

### 5. Top Edge Chamfer
*   **Min**: 0.0 mm
*   **Max**: 10.0 mm (Hard UI Limit)
*   **Dependencies**: As detailed above, it is physically constrained by the **Wall Thickness** at all times. It is additionally mathematically constrained by the vertical Y-axis height of the outer wall dropping at that specific radial distance (`safeChamfer`).
    *   **Side Effect**: If you try to drag the Chamfer slider up to `5mm`, but your Wall Thickness is only `3mm`, the Javascript constraint engine will instantly intercept the input, overriding the UI limit and freezing the slider value at exactly `2.9mm`. This is a critical safety check to prevent the geometry from physically turning inside out, crossing over its own vertices, and generating non-printable 3D artifacts.

## Feature Overview

### 1. Parametric Base Generation
The core purpose of this tool is to design fully customizable, 3D printable display stands for spherical objects. Every dimension—from the overall footprint to the inner wall chamfers—can be dynamically adjusted to create the perfect custom fit for your sphere.

### 2. Slicer-Ready 3MF Export
Once you have designed your perfect stand parameters, the application can instantly compile your bespoke geometry and trigger a download for a clean, manifold 3MF file. This file is immediately ready to be dropped into Prusaslicer, Cura, or Bambu Studio for 3D printing.

### 3. Dimensional Overlays
To help easily visualize the physical scale of your custom stand before exporting, you can toggle dynamic 3D dimension lines directly on top of the physical scene. 

### 4. Built-In Context Textures
To help visualize what your final display might look like, the generator includes several high-quality built-in stone textures (like Labradorite and Tigers Eye) that wrap around the digital reference sphere. You can also dynamically load your own custom photos to preview unique setups.

---

## Application Visuals

### Dimensional Overlays & Base Calculation
![Base Measurements & Optimization](assets/base_measurements.png)

### Slicer-Ready 3MF Export
![3MF Export Capability](assets/export_3mf.png)

### Selectable 3D Visual Context
![Rose Quartz Verify](assets/rose_quartz_render.png)

### Real-Time 3D Rendering & Swatches
![Tigers Eye Solid Render](assets/tigers_eye_solid_render.png)
