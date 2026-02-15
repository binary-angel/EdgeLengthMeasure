# Edge Length Measure

Blender add-on that registers selected mesh objects and displays individual edge lengths and total edge length directly in the 3D Viewport and Sidebar.

Designed for precise measurement, modeling analysis, and technical workflows. Fully supports modifiers (including Armature deformation) using evaluated dependency graph data.

Compatible with Blender 5.0+.

---

## Features

* Register multiple mesh objects
* Display individual edge lengths in the 3D Viewport
* Display total edge length per object
* Display grand total edge length across all registered objects
* Real-time updates when mesh or modifiers change
* Supports Armature, Subdivision, and other modifiers
* Unit-aware formatting (mm, cm, m, km based on Scene settings)
* Per-object visibility toggle
* Clean Sidebar interface

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
  Show or hide edge length display
* Remove
  Remove object from registry

Displayed Information:
* Individual edge lengths in viewport
* Total edge length per object
* Grand total edge length across all registered objects

---

## Notes

* Uses evaluated mesh from dependency graph
* Supports modifier-deformed geometry
* No need to apply modifiers
* Updates automatically when geometry changes

---

## Compatibility

Tested with:
Blender 5.0+

---

## Author
binary-angel

---

## License
MIT License

---

## Repository
https://github.com/YOUR_USERNAME/edge-length-measure
