bl_info = {
    "name": "Edge Length Measure",
    "author": "binary-angel",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Edge Length",
    "description": "Register meshes and display edge lengths",
    "category": "3D View",
}

import bpy
import blf

from bpy.props import CollectionProperty, BoolProperty, StringProperty
from bpy.types import PropertyGroup, Operator, Panel
from bpy_extras.view3d_utils import location_3d_to_region_2d


draw_handler = None
edge_cache = {}
grand_total_cache = 0.0
grand_total_dirty = True


def redraw_all_viewports():
    wm = bpy.context.window_manager
    for window in wm.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def format_length(value, unit_settings):
    scale = unit_settings.scale_length
    system = unit_settings.system
    unit = unit_settings.length_unit

    scaled = value * scale

    if system == 'METRIC':
        if unit == 'MILLIMETERS':
            display_value = scaled * 1000
            suffix = "mm"
        elif unit == 'CENTIMETERS':
            display_value = scaled * 100
            suffix = "cm"
        elif unit == 'METERS':
            display_value = scaled
            suffix = "m"
        elif unit == 'KILOMETERS':
            display_value = scaled / 1000
            suffix = "km"
        else:
            display_value = scaled
            suffix = "m"
    else:
        display_value = scaled
        suffix = ""

    return f"{display_value:.2f} {suffix}", display_value


def compute_edge_data(obj, depsgraph):
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()

    edges = []
    total = 0.0

    mat = eval_obj.matrix_world
    verts = mesh.vertices

    for e in mesh.edges:
        v1 = mat @ verts[e.vertices[0]].co
        v2 = mat @ verts[e.vertices[1]].co

        mid = (v1 + v2) * 0.5
        length = (v2 - v1).length

        edges.append((mid, length))
        total += length

    eval_obj.to_mesh_clear()

    return edges, total


def ensure_cache(obj, depsgraph):
    global edge_cache, grand_total_dirty

    name = obj.name

    if name not in edge_cache:
        edges, total = compute_edge_data(obj, depsgraph)

        edge_cache[name] = {
            "edges": edges,
            "total": total,
            "dirty": False,
        }

        grand_total_dirty = True

    elif edge_cache[name]["dirty"]:
        edges, total = compute_edge_data(obj, depsgraph)

        edge_cache[name]["edges"] = edges
        edge_cache[name]["total"] = total
        edge_cache[name]["dirty"] = False

        grand_total_dirty = True


def get_grand_total(scene, depsgraph):
    global grand_total_cache, grand_total_dirty

    if grand_total_dirty:
        total = 0.0

        for item in scene.edge_length_items:
            obj = bpy.data.objects.get(item.name)

            if obj and obj.type == 'MESH':
                ensure_cache(obj, depsgraph)
                total += edge_cache[obj.name]["total"]

        grand_total_cache = total
        grand_total_dirty = False

    return grand_total_cache


def depsgraph_update(scene, depsgraph):
    global edge_cache, grand_total_dirty

    updated = {
        update.id.name
        for update in depsgraph.updates
        if hasattr(update.id, "name")
    }

    for name in updated:
        if name in edge_cache:
            edge_cache[name]["dirty"] = True
            grand_total_dirty = True

    redraw_all_viewports()


def draw_callback():
    context = bpy.context
    scene = context.scene
    depsgraph = context.evaluated_depsgraph_get()

    region = context.region
    rv3d = context.region_data

    if not rv3d:
        return

    unit_settings = scene.unit_settings

    font_id = 0
    blf.size(font_id, 14)

    for item in scene.edge_length_items:

        if not item.visible:
            continue

        obj = bpy.data.objects.get(item.name)

        if not obj or obj.type != 'MESH':
            continue

        ensure_cache(obj, depsgraph)

        cache = edge_cache[obj.name]

        for midpoint, length in cache["edges"]:

            text, _ = format_length(length, unit_settings)

            coord = location_3d_to_region_2d(
                region,
                rv3d,
                midpoint,
            )

            if coord:
                blf.position(font_id, coord.x, coord.y, 0)
                blf.draw(font_id, text)


class EdgeLengthItem(PropertyGroup):

    name: StringProperty()

    visible: BoolProperty(
        default=True,
        update=lambda self, context: redraw_all_viewports()
    )


class EDGE_OT_Register(Operator):

    bl_idname = "edge_length.register"
    bl_label = "Register Selected Mesh"

    def execute(self, context):

        scene = context.scene
        depsgraph = context.evaluated_depsgraph_get()

        for obj in context.selected_objects:

            if obj.type != 'MESH':
                continue

            if not any(
                item.name == obj.name
                for item in scene.edge_length_items
            ):
                item = scene.edge_length_items.add()
                item.name = obj.name
                item.visible = True

                ensure_cache(obj, depsgraph)

        enable_draw_handler()
        redraw_all_viewports()

        return {'FINISHED'}


class EDGE_OT_Remove(Operator):

    bl_idname = "edge_length.remove"
    bl_label = "Remove Mesh"

    name: StringProperty()

    def execute(self, context):

        global edge_cache, grand_total_dirty

        scene = context.scene

        for i, item in enumerate(scene.edge_length_items):
            if item.name == self.name:
                scene.edge_length_items.remove(i)
                break

        if self.name in edge_cache:
            del edge_cache[self.name]

        grand_total_dirty = True

        redraw_all_viewports()

        return {'FINISHED'}


class EDGE_OT_Toggle(Operator):

    bl_idname = "edge_length.toggle"
    bl_label = "Toggle Visibility"

    name: StringProperty()

    def execute(self, context):

        scene = context.scene

        for item in scene.edge_length_items:
            if item.name == self.name:
                item.visible = not item.visible
                break

        redraw_all_viewports()

        return {'FINISHED'}


def enable_draw_handler():

    global draw_handler

    if draw_handler is None:
        draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            draw_callback,
            (),
            'WINDOW',
            'POST_PIXEL',
        )


def disable_draw_handler():

    global draw_handler

    if draw_handler:
        bpy.types.SpaceView3D.draw_handler_remove(
            draw_handler,
            'WINDOW',
        )

        draw_handler = None


class EDGE_PT_MainPanel(Panel):

    bl_label = "Edge Length Measure"
    bl_idname = "EDGE_PT_main_panel"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Edge Length"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        depsgraph = context.evaluated_depsgraph_get()
        unit_settings = scene.unit_settings

        layout.operator(
            "edge_length.register",
            text="Register Selected Mesh",
        )

        layout.separator()

        for item in scene.edge_length_items:

            row = layout.row()

            obj = bpy.data.objects.get(item.name)

            if obj and obj.type == 'MESH':

                ensure_cache(obj, depsgraph)

                total = edge_cache[obj.name]["total"]

                text, _ = format_length(
                    total,
                    unit_settings,
                )

                row.label(
                    text=f"{item.name} (Total: {text})"
                )

            else:
                row.label(text=item.name)

            icon = 'HIDE_OFF' if item.visible else 'HIDE_ON'

            op = row.operator(
                "edge_length.toggle",
                text="",
                icon=icon,
            )
            op.name = item.name

            op = row.operator(
                "edge_length.remove",
                text="",
                icon='X',
            )
            op.name = item.name

        layout.separator()
        layout.separator()

        grand = get_grand_total(
            scene,
            depsgraph,
        )

        text, _ = format_length(
            grand,
            unit_settings,
        )

        box = layout.box()

        box.label(
            text=f"Grand Total: {text}"
        )


classes = (
    EdgeLengthItem,
    EDGE_OT_Register,
    EDGE_OT_Remove,
    EDGE_OT_Toggle,
    EDGE_PT_MainPanel,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.edge_length_items = CollectionProperty(
        type=EdgeLengthItem
    )

    bpy.app.handlers.depsgraph_update_post.append(
        depsgraph_update
    )


def unregister():

    disable_draw_handler()

    if depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(
            depsgraph_update
        )

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.edge_length_items


if __name__ == "__main__":
    register()
