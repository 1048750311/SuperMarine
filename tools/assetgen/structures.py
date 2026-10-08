import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from common import _finish
from mathutils import noise
def blob(name, size, loc, m, parent=None, sub=3, amp=0.25, freq=1.5, seed=0, flat=False):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1, location=loc)
    o = bpy.context.object; o.name = name
    off = Vector((seed * 7.3, seed * 3.1, seed * 5.7))
    for v in o.data.vertices:
        n = noise.fractal(v.co * freq + off, 0.6, 2.0, 4)
        v.co = v.co * (1 + n * amp)
        if flat and v.co.z < -0.2: v.co.z = -0.2 - (v.co.z + 0.2) * 0.1
    o.scale = size; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(o, m, parent, 0, True)
def mats_h():
    return dict(A=mat('armor', hexc('#8a929a'), 0.5, 0.45, tex='panels'), C=mat('concrete', hexc('#8a8780'), 0.0, 0.9, tex='concrete'),
        D=mat('steel', hexc('#6a6f75'), 0.7, 0.4, tex='panels2'), Y=mat('hazard', hexc('#c99a2e'), 0.3, 0.5, tex='paint'),
        G=mat('glass', hexc('#9fe3ff'), 0, 0.15, emit=hexc('#6fc8ff'), strength=2), R=mat('beacon', hexc('#ff5a3a'), 0, 0.3, emit=hexc('#ff3a1a'), strength=5),
        S=mat('sandbag', hexc('#8a7a5a'), 0, 0.9, tex='suit'))
def base():
    reset(); CLIPS.clear(); UVS['scale'] = 36.0; M = mats_h(); root = empty('root')
    box('plinth', (380, 220, 10), (0, 0, 5), M['C'], root, 3)
    box('main', (300, 170, 44), (0, 0, 32), M['A'], root, 6)
    box('roof', (270, 140, 6), (0, 0, 57), M['D'], root, 2)
    for x in (-110, -40, 30, 100):
        box(f'vent{x}', (34, 20, 8), (x, 40, 64), M['D'], root, 2)
        cyl(f'fan{x}', 8, 2, (x, 40, 68.5), M['D'], root, verts=16)
    box('hangar_door', (4, 120, 34), (152, 0, 27), M['D'], root, 1)
    box('stripe', (302, 172, 4), (0, 0, 14), M['Y'], root, 0.5)
    tower = empty('tower', (-90, -50, 60), root)
    cyl('tower_shaft', 18, 60, (-90, -50, 90), M['A'], tower, verts=16)
    box('tower_cab', (56, 56, 22), (-90, -50, 128), M['D'], tower, 4)
    box('tower_glass', (58, 58, 8), (-90, -50, 130), M['G'], tower, 2)
    dish = empty('radar', (-90, -50, 146), tower)
    cyl('dish_mast', 2.5, 16, (-90, -50, 146), M['D'], dish, verts=8)
    cyl('dish', 20, 4, (-80, -50, 156), M['A'], dish, rot=(0, 1.1, 0), verts=20, r2=6)
    cyl('antenna', 1.2, 70, (60, -55, 95), M['D'], root, verts=6)
    sph('beacon', (3, 3, 3), (60, -55, 131), M['R'], root, 8, 6)
    for x in (-150, 150):
        for y in (-95, 95): sph(f'light{x}{y}', (3, 3, 3), (x, y, 12), M['G'], root, 8, 6)
    for i in range(4): cyl(f'pipe{i}', 3, 90, (-20 + i * 9, 88, 30), M['D'], root, rot=(0, math.pi / 2, 0), verts=8)
    world_to_local()
    for f, r in ((1, 0), (120, math.pi * 2)): key('idle', dish, f, rot=(0, 0, r))
    bake_clips()
def barracks():
    reset(); CLIPS.clear(); UVS['scale'] = 40.0; M = mats_h(); root = empty('root')
    box('pad', (190, 150, 6), (0, 0, 3), M['C'], root, 2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=55, depth=150, location=(0, 0, 6), rotation=(math.pi / 2, 0, 0))
    q = bpy.context.object; q.name = 'quonset'
    for v in q.data.vertices:
        if v.co.y < 0: v.co.y = 0
    _finish(q, M['A'], root, 0, True)
    bpy.ops.object.select_all(action='DESELECT')
    box('front_wall', (6, 100, 52), (0, 74, 30), M['D'], root, 1)
    box('door', (2, 40, 34), (0, 77.5, 23), M['Y'], root, 0.5)
    for i in range(-3, 4): box(f'rib{i}', (4, 4, 4), (i * 20, 0, 62), M['D'], root, 1)
    for i in range(6): box(f'bag{i}', (14, 8, 7), (-60 + i * 24, 72, 9), M['S'], root, 3)
    cyl('chimney', 4, 30, (30, -40, 60), M['D'], root, verts=10)
    world_to_local(); bake_clips()
def armory():
    reset(); CLIPS.clear(); UVS['scale'] = 30.0; M = mats_h(); root = empty('root')
    box('floor', (120, 120, 4), (0, 0, 2), M['D'], root, 1)
    for x, y in ((-55, -55), (55, -55), (-55, 55), (55, 55)): cyl(f'post{x}{y}', 3, 46, (x, y, 27), M['A'], root, verts=8)
    box('roof', (128, 128, 4), (0, 0, 52), M['A'], root, 1)
    box('rack', (8, 80, 28), (-48, 0, 18), M['D'], root, 1)
    for i in range(5): box(f'gun{i}', (2, 3, 22), (-43, -30 + i * 15, 20), M['D'], root, 0.3)
    for i, (x, y, s) in enumerate(((30, 30, 18), (30, 8, 14), (10, 34, 14), (36, 40, 12))): box(f'crate{i}', (s, s, s), (x, y, 4 + s / 2), M['S'] if i % 2 else M['A'], root, 1.2)
    world_to_local(); bake_clips()
def outpost():
    reset(); CLIPS.clear(); UVS['scale'] = 30.0; M = mats_h(); root = empty('root')
    cyl('platform', 60, 6, (0, 0, 3), M['C'], root, verts=6)
    for i in range(6):
        a = i / 6 * math.pi * 2 + math.pi / 6
        box(f'barrier{i}', (40, 6, 10), (math.cos(a) * 52, math.sin(a) * 52, 11), M['C'], root, 2, rot=(0, 0, a + math.pi / 2))
    cyl('mast', 1.5, 70, (30, -30, 41), M['D'], root, verts=6)
    flag = empty('flag', (30, -30, 72), root)
    box('flagm', (24, 1, 14), (42, -30, 70), M['Y'], flag, 0.2)
    world_to_local()
    for f, r in ((1, 0), (30, 0.12), (60, 0)): key('idle', flag, f, rot=(0, 0, r))
    bake_clips()
def mats_b():
    return dict(F=mat('flesh', hexc('#4a2a3e'), 0.1, 0.55, tex='organic'), H=mat('husk', hexc('#3a2a24'), 0.15, 0.5, tex='chitin2'),
        G=mat('core', hexc('#6fb83a'), 0, 0.3, emit=hexc('#5ab020'), strength=0.9), E=mat('egg', hexc('#8a9a5a'), 0, 0.35, emit=hexc('#4a7a1a'), strength=0.35),
        T=mat('spine', hexc('#c8b896'), 0.1, 0.4, tex='chitin2'))
def nest():
    reset(); CLIPS.clear(); UVS['scale'] = 60.0; M = mats_b(); root = empty('root'); random.seed(3)
    blob('mound', (190, 150, 110), (0, 0, 10), M['F'], root, 4, 0.22, 1.4, 1, flat=True)
    for i in range(9):
        a = i / 9 * math.pi * 2; r = 120 + random.random() * 40
        blob(f'lobe{i}', (50, 44, 34), (math.cos(a) * r, math.sin(a) * r * 0.78, 8), M['H'], root, 3, 0.3, 1.8, i + 2, flat=True)
    core = empty('core', (20, 0, 100), root)
    blob('coreorb', (44, 44, 40), (20, 0, 100), M['G'], core, 3, 0.15, 2, 9)
    for i in range(7):
        a = i / 7 * math.pi * 2
        seg(f'spire{i}', (math.cos(a) * 100, math.sin(a) * 78, 60), (math.cos(a) * 130, math.sin(a) * 105, 170 + random.random() * 50), 14, M['T'], root, r2=1, verts=8)
    world_to_local()
    for f, z in ((1, 0), (45, 4), (90, 0)): key('idle', core, f, loc=(0, 0, z))
    bake_clips()
def hatchery():
    reset(); CLIPS.clear(); UVS['scale'] = 40.0; M = mats_b(); root = empty('root'); random.seed(5)
    for i in range(8):
        a = i / 8 * math.pi * 2
        blob(f'rim{i}', (34, 30, 22), (math.cos(a) * 70, math.sin(a) * 70, 6), M['F'], root, 3, 0.3, 1.8, i, flat=True)
    cyl('pit', 62, 4, (0, 0, 1), M['H'], root, verts=24)
    eggs = empty('eggs', (0, 0, 4), root)
    for i in range(9):
        a = i / 9 * math.pi * 2; r = 18 + (i % 3) * 12
        blob(f'egg{i}', (9, 9, 14), (math.cos(a) * r, math.sin(a) * r, 14), M['E'], eggs, 2, 0.12, 2, i + 20)
    world_to_local()
    for f, z in ((1, 0), (30, 1.5), (60, 0)): key('idle', eggs, f, loc=(0, 0, z))
    bake_clips()
def bug_tower():
    reset(); CLIPS.clear(); UVS['scale'] = 30.0; M = mats_b(); root = empty('root'); random.seed(7)
    blob('base', (50, 50, 24), (0, 0, 6), M['F'], root, 3, 0.3, 1.6, 4, flat=True)
    seg('trunk', (0, 0, 10), (0, 0, 70), 16, M['H'], root, r2=7, verts=10)
    for i in range(8):
        a = i / 8 * math.pi * 2
        seg(f'thorn{i}', (math.cos(a) * 12, math.sin(a) * 12, 20 + (i % 2) * 20), (math.cos(a) * 46, math.sin(a) * 46, 30 + (i % 2) * 30), 4, M['T'], root, r2=0.4, verts=6)
    core = empty('core', (0, 0, 74), root)
    blob('coreorb', (12, 12, 12), (0, 0, 76), M['G'], core, 2, 0.15, 2, 11)
    world_to_local()
    for f, s in ((1, 0), (30, 3), (60, 0)): key('idle', core, f, loc=(0, 0, s))
    bake_clips()
def rocks():
    out = []
    for i in range(6):
        reset(); CLIPS.clear(); UVS['scale'] = 16.0
        M = mat('rock', hexc(['#7a6a58', '#6a5e50', '#857462', '#5e5448', '#7e7060', '#6e6050'][i]), 0.0, 0.85, tex='rock' if i % 2 else 'rock2')
        root = empty('root')
        sx, sy, sz = [(30, 24, 18), (18, 16, 12), (44, 30, 22), (12, 10, 9), (26, 30, 24), (60, 38, 20)][i]
        blob('rock', (sx, sy, sz), (0, 0, sz * 0.45), M, root, 3, 0.35, 1.2, i + 40, flat=True)
        world_to_local(); bake_clips(); out.append(f'rock_{i + 1}')
        export(os.path.join(OUT, f'rock_{i + 1}.glb'))
    return out
OUT = sys.argv[sys.argv.index('--') + 1]
for name, fn in (('base', base), ('barracks', barracks), ('armory', armory), ('outpost', outpost), ('nest', nest), ('hatchery', hatchery), ('bug_tower', bug_tower)):
    fn(); export(os.path.join(OUT, name + '.glb')); print('exported', name)
rocks(); print('exported rocks')
