import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper
import math

from bpy.props import (
    FloatProperty,
    IntProperty,
)

bl_info = {
    "name": "ripple mesh maker",
    "author": "mocchi",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3Dviewport > Add > Mesh",
    "description": "making ripple",
    "warning": "",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object"
}

def add_ripple_mesh(dots, freq, amp, phase):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    verts = []
    for i in range(-dots, dots, 1):
        for j in range(-dots, dots, 1):
            verts.append((i, j, amp * math.sin(math.radians(math.sqrt(i**2 + j**2) * freq) + phase )))

    faces = []
    for i in range(dots*2-1):
        for j in range(dots*2-1):
            faces.append((j + i*2*dots, j+1 + i*2*dots, j+1+dots*2 + i*2*dots, j+dots*2 + i*2*dots))

    return verts, faces


class AddRipple(bpy.types.Operator, AddObjectHelper):
    """Add a ripple mesh"""
    bl_idname = "mesh.ripple_add"
    bl_label = "Add ripple mesh"
    bl_options = {'REGISTER', 'UNDO'}

    dots: IntProperty(
        name="dots",
        description="Number of dots",
        min=2, max=100,
        default=5,
    )
    freq: FloatProperty(
        name="frequency",
        description="Frequency of ripple",
        min=0, max=200,
        default=20,
    )
    amp: FloatProperty(
        name="amplitude",
        description="amplitude of ripple",
        min=0, max=50,
        default=1,
    )
    phase: FloatProperty(
        name="phase",
        description="phase of ripple",
        min=-180, max=180,
        default=0,
    )

    def execute(self, context):

        verts_loc, faces = add_ripple_mesh(
            self.dots,
            self.freq,
            self.amp,
            self.phase,
        )

        mesh = bpy.data.meshes.new("Ripple")

        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.new(v_co)

        bm.verts.ensure_lookup_table()
        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddRipple.bl_idname, icon='PROP_ON')


def register():
    bpy.utils.register_class(AddRipple)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddRipple)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()

    