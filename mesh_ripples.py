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
    "author": "K-mocchi",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3Dviewport > Add > Mesh",
    "description": "generate unique meshes",
    "warning": "",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object"
}

# =================================================
# Add ripple mesh
# =================================================
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

# =================================================
# Add mobius ring mesh
# =================================================
def add_mobius_ring(width, radius, length, l_inc, cof_x, cof_y):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """
    
    verts = []
    for t in range(0, length, 1):
        for j in range(2):
            # equation of mobius ring
            x = ((radius+width*j)*math.cos(math.radians(t)*l_inc)+2)*math.cos(cof_x*math.radians(t)*l_inc)
            y = ((radius+width*j)*math.cos(math.radians(t)*l_inc)+2)*math.sin(cof_y*math.radians(t)*l_inc)
            z = (radius+width*j)*math.sin(math.radians(t)*l_inc)
            verts.append((x, y, z))

    faces = []
    for i in range(0, (length-1)*2, 2):
        faces.append((i, i+1, i+3, i+2))
    
    return verts, faces


class AddMobius(bpy.types.Operator, AddObjectHelper):
    bl_idname = "mesh.mobius_ring"
    bl_label = "Add mobius_ring"
    bl_options = {'REGISTER', 'UNDO'}

    width: FloatProperty(
        name="width",
        description="path width of mobius",
        min=0.1, max=200,
        default=1,
    )
    radius: FloatProperty(
        name="radius",
        description="radius of mobius",
        min=0.01, max=200,
        default=10,
    )
    length: IntProperty(
        name="length",
        description="path length of mobius",
        min=1, max=361,
        default=60,
    )
    l_inc: FloatProperty(
        name="l_inc",
        description="length increment",
        min=1, max=50,
        default=5,
    )
    cof_x: IntProperty(
        name="coefficient x",
        description="coefficient of mobius",
        min=1, max=10,
        default=1,
    )
    cof_y: IntProperty(
        name="coefficient y",
        description="coefficient of mobius",
        min=1, max=10,
        default=1,
    )

    def execute(self, context):

        verts_loc, faces = add_mobius_ring(
            self.width,
            self.radius,
            self.length,
            self.l_inc,
            self.cof_x,
            self.cof_y,
        )


        mesh = bpy.data.meshes.new("Mobius_ring")

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
    
# =================================================
# Other Settings
# =================================================

classes = {
    AddRipple,
    AddMobius,
}

def menu_func(self, context):
    self.layout.operator(AddRipple.bl_idname, icon='PROP_ON')
    self.layout.operator(AddMobius.bl_idname, icon='MOD_SCREW')


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()

    
