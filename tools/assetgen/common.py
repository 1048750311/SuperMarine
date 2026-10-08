import bpy, math, sys, os, bmesh
TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'textures')
UVS = {'scale': 8.0}
from mathutils import Vector, Euler
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _mats.clear(); PENDING.clear()
_mats = {}
PENDING = []
def _img(path, noncolor=False):
    im = bpy.data.images.load(path, check_existing=True)
    if noncolor: im.colorspace_settings.name = 'Non-Color'
    return im
def mat(name, color, metal=0.0, rough=0.6, emit=None, strength=4.0, tex=None):
    key = (name,)
    if key in _mats: return _mats[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = (*color, 1)
    if tex:
        ic = nt.nodes.new('ShaderNodeTexImage'); ic.image = _img(os.path.join(TEX, tex + '_color.jpg'))
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
        mix.inputs['Factor'].default_value = 1.0
        mix.inputs[7].default_value = (*color, 1)
        nt.links.new(ic.outputs['Color'], mix.inputs[6]); nt.links.new(mix.outputs[2], b.inputs['Base Color'])
        ir = nt.nodes.new('ShaderNodeTexImage'); ir.image = _img(os.path.join(TEX, tex + '_rough.jpg'), True)
        nt.links.new(ir.outputs['Color'], b.inputs['Roughness'])
        inn = nt.nodes.new('ShaderNodeTexImage'); inn.image = _img(os.path.join(TEX, tex + '_normal.jpg'), True)
        nm = nt.nodes.new('ShaderNodeNormalMap'); nt.links.new(inn.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1)
        b.inputs['Emission Strength'].default_value = strength
    _mats[key] = m; return m
def hexc(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)
def empty(name, loc=(0,0,0), parent=None):
    o = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(o)
    o.location = loc
    if parent: PENDING.append((o, parent))
    o.rotation_mode = 'XYZ'
    return o
def uv_box(o, scale):
    bm = bmesh.new(); bm.from_mesh(o.data)
    uv = bm.loops.layers.uv.verify()
    for f in bm.faces:
        n = f.normal; ax = max(range(3), key=lambda i: abs(n[i]))
        a, b = [(1, 2), (0, 2), (0, 1)][ax]
        for l in f.loops:
            co = l.vert.co + o.location
            l[uv].uv = (co[a] / scale, co[b] / scale)
    bm.to_mesh(o.data); bm.free()
def _finish(o, m, parent, bevel, smooth):
    uv_box(o, UVS['scale'])
    if m: o.data.materials.append(m)
    if bevel:
        bm = o.modifiers.new('bev', 'BEVEL'); bm.width = bevel; bm.segments = 1; bm.limit_method = 'ANGLE'
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
    if parent: PENDING.append((o, parent))
    return o
def box(name, size, loc, m, parent=None, bevel=0.0, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, m, parent, bevel, False)
def cyl(name, r, depth, loc, m, parent=None, rot=(0,0,0), verts=12, bevel=0.0, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    return _finish(o, m, parent, bevel, True)
def sph(name, size, loc, m, parent=None, seg=12, rings=8, rot=(0,0,0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, m, parent, 0, True)
def world_to_local(objs=None):
    bpy.context.view_layer.update()
    W = {o.name: o.matrix_world.copy() for o, _ in PENDING}
    W.update({p.name: p.matrix_world.copy() for _, p in PENDING})
    for o, p in PENDING:
        o.parent = p; o.matrix_parent_inverse = W[p.name].inverted()
    bpy.context.view_layer.update()
CLIPS = {}
def key(clip, obj, frame, rot=None, loc=None):
    CLIPS.setdefault(clip, {}).setdefault(obj.name, []).append((frame, rot, loc))
def bake_clips(fps=30):
    scn = bpy.context.scene; scn.render.fps = fps
    for clip, per in CLIPS.items():
        for oname, keys in per.items():
            o = bpy.data.objects[oname]
            base_rot = tuple(o.get('_r0', o.rotation_euler)); base_loc = tuple(o.get('_l0', o.location))
            o['_r0'] = base_rot; o['_l0'] = base_loc
            if not o.animation_data: o.animation_data_create()
            act = bpy.data.actions.new(f"{clip}_{oname}")
            o.animation_data.action = act
            for (f, rot, loc) in keys:
                o.rotation_euler = Euler([base_rot[i] + (rot[i] if rot else 0) for i in range(3)])
                o.location = Vector([base_loc[i] + (loc[i] if loc else 0) for i in range(3)])
                o.keyframe_insert('rotation_euler', frame=f); o.keyframe_insert('location', frame=f)
            tr = o.animation_data.nla_tracks.new(); tr.name = clip
            st = tr.strips.new(clip, int(keys[0][0]), act)
            o.animation_data.action = None
            o.rotation_euler = Euler(base_rot); o.location = Vector(base_loc)
def export(path):
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', export_apply=True,
        export_animations=True, export_animation_mode='NLA_TRACKS', export_force_sampling=True,
        export_optimize_animation_size=True, export_yup=True)
def seg(name, a, b, r, m, parent=None, r2=None, verts=7):
    a = Vector(a); b = Vector(b); d = b - a; mid = (a + b) / 2
    rot = Vector((0, 0, 1)).rotation_difference(d.normalized()).to_euler()
    return cyl(name, r, d.length, tuple(mid), m, parent, rot=tuple(rot), verts=verts, r2=r2)
