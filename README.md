# Edge Length Measure

Blender add-on that registers selected mesh objects and displays individual edge lengths and total edge length directly in the 3D Viewport and Sidebar.

Designed for precise measurement, modeling analysis, and technical workflows. Fully supports modifier-deformed geometry using evaluated dependency graph data.

Compatible with Blender 5.0+.

---

## Purpose

This add-on was created to measure mesh edge lengths in Object Mode.

In Blender, when modifiers such as Armature, Subdivision Surface, or other deformation modifiers are applied, the mesh geometry displayed in Object Mode can differ significantly from the original mesh in Edit Mode.

Blender’s built-in measurement tools and most existing add-ons primarily operate in Edit Mode, measuring the base mesh geometry rather than the evaluated mesh that includes modifier deformation.

However, in many technical and modeling workflows, it is necessary to measure the actual visible geometry as it appears in Object Mode after modifiers are applied.

Blender does not provide a native tool to measure individual edge lengths directly in Object Mode for evaluated meshes. This add-on was developed to address that limitation.

It enables accurate measurement of edge lengths on the evaluated mesh without applying or destroying modifiers.

---

## Features

* Register multiple mesh objects
* Display individual edge lengths in the 3D Viewport (Object Mode)
* Display total edge length per object
* Display grand total edge length across all registered objects
* Real-time updates when mesh or modifiers change
* Fully supports modifier-deformed geometry (Armature, Subdivision, etc.)
* Unit-aware formatting (mm, cm, m, km based on Scene settings)
* Per-object visibility toggle
* Clean and efficient Sidebar interface

---

## Installation

1. Download the `.py` file

2. Open Blender

3. Go to:

   Edit → Preferences → Add-ons

4. Click:

   Install...

5. Select the `.py` file

6. Enable:

   Edge Length Measure

---

## Usage

Open the Sidebar:

View3D → Press `N` → Edge Length tab

Controls:

* Register Selected Mesh
  Registers selected mesh objects

* Visibility Toggle
  Show or hide edge length display in viewport

* Remove
  Remove object from registry

Displayed Information:

* Individual edge lengths in viewport
* Total edge length per object
* Grand total edge length across all registered objects

---

## Technical Notes

* Uses evaluated mesh from Blender dependency graph
* Measures the actual visible mesh in Object Mode
* Supports modifier-deformed geometry without applying modifiers
* Automatically updates when geometry or modifiers change
* Optimized with caching for performance

---

## Compatibility

Tested with:

Blender 5.0+

---

## Author

binary-angel

