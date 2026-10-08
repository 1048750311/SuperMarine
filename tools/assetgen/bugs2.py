import sys, os, math, random
sys.path.insert(0, os.path.dirname(__file__))
from common import *
from bugs import legs6, walk
def chit(col, name='chitin', tex='chitin', rough=0.4): return mat(name, hexc(col), 0.15, rough, tex=tex)
def glow(col, s=1.2, name='glow'): return mat(name, hexc(col), 0, 0.3, emit=hexc(col), strength=s)
def die_flip(root, legs, k=1.0, n=24):
    for f, (roll, dz) in ((1, (0, 0)), (n // 4, (1.2, 1.5)), (n // 2, (3.0, -2)), (n, (3.1, -3))):
        key('die', root, f, rot=(roll, 0, 0), loc=(0, 0, dz * k + (6 * k if roll > 2 else 0)))
    for hip, kn, i, s in legs:
        for f, a in ((1, 0), (n // 2, 0.8), (n, 0.9)): key('die', hip, f, rot=(a * s, 0, 0))
def idle_breathe(obj, amp=0.4):
    for f, z in ((1, 0), (30, amp), (60, 0)): key('idle', obj, f, loc=(0, 0, z))
def bomber():
    reset(); CLIPS.clear()
    C = chit('#5a4632'); J = chit('#2e2418', 'joint', 'chitin2'); G = glow('#c8601e', 0.55, 'volatile')
    root = empty('root'); body = empty('body', (0, 0, 5), root)
    sac = empty('sac', (-1, 0, 7.5), body)
    sph('sacm', (6, 5.6, 5.4), (-1, 0, 8), G, sac, 18, 12)
    for i in range(6):
        a = i / 6 * math.pi * 2
        seg(f'rib{i}', (-1 + math.cos(a) * 1, math.sin(a) * 5.4, 3.5), (-1 + math.cos(a) * 1.5, math.sin(a) * 4.6, 12.5), 0.6, C, sac, verts=6)
    sph('head', (2.6, 3, 2.2), (5.2, 0, 4.6), C, body, 10, 7)
    for s in (1, -1): seg(f'mand{s}', (6.8, 1 * s, 4.2), (9, 0.3 * s, 3.8), 0.5, J, body, r2=0.1, verts=5)
    legs = legs6(body, (3, -1.5), 3.2, 4, 6, 0.55, J)
    world_to_local()
    walk('run', legs, 12, 0.55); idle_breathe(sac, 0.5)
    for f, sc in ((1, 0), (6, 1.2), (10, -0.4), (14, 1.6), (18, 0)): key('attack', sac, f, loc=(0, 0, sc))
    die_flip(root, legs, 0.8, 16)
    bake_clips()
def flyer():
    reset(); CLIPS.clear()
    C = chit('#3e3a2c'); P = chit('#6b5a2a', 'stripe', 'chitin2'); J = chit('#1e1c16', 'joint', 'chitin2')
    Wm = mat('wing', hexc('#c8d0b8'), 0, 0.3)
    b = Wm.node_tree.nodes.get('Principled BSDF'); b.inputs['Alpha'].default_value = 0.35
    try: Wm.surface_render_method = 'BLENDED'
    except Exception: Wm.blend_method = 'BLEND'
    E = glow('#ff5030', 3, 'eye')
    root = empty('root'); body = empty('body', (0, 0, 22), root)
    sph('thorax', (3.6, 3.4, 3.2), (1, 0, 22), C, body, 12, 8)
    abd = empty('abdomen', (-2, 0, 22), body)
    for i in range(4):
        sph(f'abd{i}', (2.6 - i * 0.3, 2.8 - i * 0.4, 2.4 - i * 0.3), (-3.5 - i * 3, 0, 21.5 - i * 0.7), P if i % 2 else C, abd, 10, 7)
    seg('stinger', (-14, 0, 19.5), (-18, 0, 18), 0.7, J, abd, r2=0.05, verts=6)
    sph('head', (2.2, 2.6, 2), (5.4, 0, 22.4), C, body, 10, 7)
    for s in (1, -1): sph('eye', (1, 1, 1), (6.4, 1.6 * s, 23), E, body, 8, 6)
    wings = []
    for j, x in enumerate((2.2, -0.2)):
        for side, s in (('L', 1), ('R', -1)):
            w = empty(f'wing{j}{side}', (x, 2.6 * s, 24), body)
            box(f'wingm{j}{side}', (5 - j, 12 - j * 2, 0.15), (x - 1.5, (2.6 + 6 - j) * s, 24.2), Wm, w, rot=(0, 0, 0.25 * s * (1 + j)))
            wings.append((w, s))
    legs = legs6(body, (2.5, 1, -0.5), 2.4, 20.5, 5, 0.35, J, foot_z=15.5)
    world_to_local()
    for f in range(1, 6):
        for w, s in wings: key('run', w, f, rot=((0.7 if f % 2 else -0.5) * s, 0, 0))
        key('run', body, f, loc=(0, 0, 0.6 if f % 2 else 0))
    for f in range(1, 6):
        for w, s in wings: key('idle', w, f, rot=((0.7 if f % 2 else -0.5) * s, 0, 0))
    for f, (p, dz) in ((1, (0, 0)), (6, (0.35, -3)), (10, (0, 0))):
        key('attack', body, f, rot=(0, p, 0), loc=(p * 10, 0, dz)); key('attack', abd, f, rot=(0, -p * 1.5, 0))
    for f, (roll, dz) in ((1, (0, 0)), (10, (1.5, -10)), (20, (3.1, -21))):
        key('die', root, f, rot=(roll, 0, 0), loc=(0, 0, dz))
    bake_clips()
def mortar():
    reset(); CLIPS.clear()
    C = chit('#4a4636'); P = chit('#6a6040', 'plate', 'chitin2'); J = chit('#24221a', 'joint', 'chitin2'); G = glow('#8fe04a', 1.0, 'acid')
    root = empty('root'); body = empty('body', (0, 0, 8), root)
    sph('abdomen', (9, 7.5, 5.5), (-3, 0, 8.5), C, body, 16, 10)
    sph('thorax', (5, 5.5, 4), (5, 0, 8), P, body, 12, 8)
    sph('head', (2.6, 3.2, 2.4), (9.4, 0, 7.6), C, body, 10, 7)
    tube = empty('launcher', (-2, 0, 12), body)
    cyl('organ', 3.2, 9, (-2, 0, 16), P, tube, rot=(0, -0.45, 0), verts=14, r2=2.4)
    cyl('organ_mouth', 2.5, 1.2, (-4.0, 0, 20.4), G, tube, rot=(0, -0.45, 0), verts=14)
    for i in range(5): seg(f'spine{i}', (-8 + i * 3, 0, 13 - abs(i - 2) * 0.4), (-9 + i * 3, 0, 16 - abs(i - 2) * 0.6), 0.7, J, body, r2=0.1, verts=5)
    legs = legs6(body, (5, 1.5, -2, -5.5), 4, 7, 11, 0.8, J)
    world_to_local()
    walk('run', legs, 28, 0.3); idle_breathe(tube, 0.3)
    for f, (r, dz) in ((1, (0, 0)), (10, (-0.15, -1.2)), (13, (0.25, 1)), (22, (0, 0))):
        key('attack', tube, f, rot=(0, r, 0), loc=(0, 0, dz)); key('attack', body, f, loc=(0, 0, dz * 0.5))
    die_flip(root, legs, 1.2, 28)
    bake_clips()
def lancer():
    reset(); CLIPS.clear()
    C = chit('#3a3028'); P = chit('#5a4a38', 'plate', 'chitin2'); J = chit('#1e1812', 'joint', 'chitin2'); B = mat('blade', hexc('#d8cfb8'), 0.2, 0.3, tex='chitin2'); E = glow('#ff4020', 3, 'eye')
    root = empty('root'); body = empty('body', (0, 0, 5), root)
    segs = []
    for i in range(7):
        sg = empty(f'seg{i}', (2 - i * 4.2, 0, 5), body if i == 0 else segs[-1])
        sph(f'segm{i}', (2.6, 3.4 - i * 0.18, 2.2), (2 - i * 4.2, 0, 5.2), P if i % 2 else C, sg, 12, 7)
        for s in (1, -1): seg(f'sleg{i}{s}', (2 - i * 4.2, 2.6 * s, 4.6), (2.6 - i * 4.2, 6.5 * s, 0.4), 0.4, J, sg, r2=0.1, verts=5)
        segs.append(sg)
    head = empty('head', (5.5, 0, 6), body)
    sph('headm', (2.8, 3, 2.4), (6, 0, 6.4), C, head, 10, 7)
    for s in (1, -1): sph('eye', (0.6,) * 3, (8, 1.4 * s, 7.2), E, head, 6, 4)
    arms = []
    for side, s in (('L', 1), ('R', -1)):
        a = empty(f'scythe{side}', (4.5, 2.8 * s, 7), body)
        seg(f'arm{side}', (4.5, 2.8 * s, 7), (8, 4.5 * s, 12), 0.7, J, a, verts=6)
        seg(f'blade{side}', (8, 4.5 * s, 12), (15, 3.5 * s, 6), 0.9, B, a, r2=0.05, verts=4)
        arms.append((a, s))
    world_to_local()
    for f in range(1, 18, 4):
        ph = (f - 1) / 16 * 2 * math.pi
        for i, sg in enumerate(segs): key('run', sg, f, rot=(0, 0, math.sin(ph - i * 0.9) * 0.12))
    for a, s in arms:
        for f, r in ((1, 0), (5, -0.9), (9, 0.6), (14, 0)): key('attack', a, f, rot=(0, r, 0))
        for f, r in ((1, 0), (30, -0.1), (60, 0)): key('idle', a, f, rot=(0, r, 0))
    for f, (roll, dz) in ((1, (0, 0)), (10, (1.4, 1)), (20, (3.1, 2))): key('die', root, f, rot=(roll, 0, 0), loc=(0, 0, dz + (8 if roll > 2 else 0)))
    bake_clips()
def queen():
    reset(); CLIPS.clear()
    C = chit('#4a2c3e'); P = chit('#6a3e58', 'plate', 'chitin2'); J = chit('#24141e', 'joint', 'chitin2'); G = glow('#4f8a24', 0.45, 'egg'); E = glow('#c8ff8c', 3, 'eye')
    T = mat('horn', hexc('#d8c6a2'), 0.1, 0.4, tex='chitin2')
    k = 2.6
    root = empty('root'); body = empty('body', (0, 0, 7 * k), root)
    abd = empty('abdomen', (-5 * k, 0, 7.5 * k), body)
    sph('ovip', (10 * k, 7 * k, 5.5 * k), (-12 * k, 0, 7 * k), G, abd, 18, 12)
    for i in range(5): sph(f'band{i}', (1.2 * k, 7.2 * k - abs(i - 2) * 1.2 * k, 5.7 * k - abs(i - 2) * 0.9 * k), (-6 * k - i * 3.2 * k, 0, 7 * k), C, abd, 14, 8)
    sph('thorax', (6 * k, 6 * k, 4.6 * k), (0, 0, 8 * k), P, body, 16, 10)
    head = empty('head', (6 * k, 0, 9.5 * k), body)
    sph('headm', (3.6 * k, 4.2 * k, 3.4 * k), (7 * k, 0, 10 * k), C, head, 14, 9)
    for i in range(5): seg(f'crown{i}', (6 * k, (i - 2) * 1.6 * k, 12.5 * k), (3.5 * k, (i - 2) * 2.6 * k, (17 - abs(i - 2)) * k), 0.8 * k, T, head, r2=0.05, verts=6)
    for s in (1, -1):
        sph('eye', (0.8 * k,) * 3, (10 * k, 1.8 * k * s, 11 * k), E, head, 8, 5)
        seg(f'mand{s}', (10 * k, 1.6 * k * s, 8.6 * k), (14 * k, 0.6 * k * s, 8 * k), 0.8 * k, T, head, r2=0.1, verts=6)
    for i in range(5): seg(f'dspine{i}', (3 * k - i * 2 * k, 0, 11.5 * k), (2 * k - i * 2 * k, 0, 15.5 * k - i * 0.4 * k), 0.7 * k, T, body, r2=0.1, verts=6)
    legs = legs6(body, (4 * k, 1.5 * k, -1 * k, -3.5 * k), 4.5 * k, 6.5 * k, 12 * k, 0.9 * k, J)
    world_to_local()
    walk('run', legs, 32, 0.28); idle_breathe(abd, 0.6 * k)
    for f, (p, dz) in ((1, (0, 0)), (10, (-0.3, 2 * k)), (16, (0.15, -0.5 * k)), (24, (0, 0))):
        key('attack', body, f, rot=(0, p, 0), loc=(0, 0, dz)); key('attack', head, f, rot=(0, -p, 0))
    for f, sc in ((1, 0), (12, 1.2 * k), (20, 0)): key('summon', abd, f, loc=(-sc * 0.5, 0, sc))
    for f, (p, dz) in ((1, (0, 0)), (15, (0.2, -3 * k)), (30, (0.25, -5 * k)), (40, (0.25, -5 * k))): key('die', root, f, rot=(0.15, p, 0), loc=(0, 0, dz))
    bake_clips()
def burrower():
    reset(); CLIPS.clear()
    C = chit('#7a6448', 'grub', 'chitin'); J = chit('#3a2c1e', 'joint', 'chitin2'); T = mat('drill', hexc('#bfb29a'), 0.3, 0.35, tex='chitin2')
    root = empty('root'); body = empty('body', (0, 0, 3), root); segs = []
    for i in range(5):
        sg = empty(f'seg{i}', (1 - i * 2.6, 0, 3), body if i == 0 else segs[-1])
        sph(f'segm{i}', (1.7, 2.2 - i * 0.2, 1.8 - i * 0.15), (1 - i * 2.6, 0, 3), C, sg, 10, 7); segs.append(sg)
    head = empty('head', (2.6, 0, 3.2), body)
    for j in range(4):
        a = j / 4 * math.pi * 2
        seg(f'tooth{j}', (3, math.cos(a) * 1.2, 3.2 + math.sin(a) * 1.2), (5.5, math.cos(a) * 0.3, 3.2 + math.sin(a) * 0.3), 0.45, T, head, r2=0.05, verts=5)
    for i in range(4):
        for s in (1, -1): seg(f'l{i}{s}', (1 - i * 2.6, 1.6 * s, 2.2), (1.4 - i * 2.6, 3.4 * s, 0.3), 0.3, J, segs[i], r2=0.1, verts=5)
    world_to_local()
    for f in range(1, 14, 3):
        ph = (f - 1) / 12 * 2 * math.pi
        for i, sg in enumerate(segs): key('run', sg, f, rot=(0, 0, math.sin(ph - i) * 0.25), loc=(0, 0, max(0, math.sin(ph - i)) * 0.4))
    for f, r in ((1, 0), (4, 0.5), (8, 0)): key('attack', head, f, rot=(r, 0, 0), loc=(r * 2, 0, 0))
    idle_breathe(body, 0.2)
    for f, (roll, dz) in ((1, (0, 0)), (8, (1.6, 1)), (16, (3.1, 4))): key('die', root, f, rot=(roll, 0, 0), loc=(0, 0, dz))
    bake_clips()
def behemoth():
    reset(); CLIPS.clear()
    H = mat('hide', hexc('#6a5a48'), 0.1, 0.7, tex='chitin2'); P = mat('plates', hexc('#5a4a3a'), 0.2, 0.5, tex='chitin')
    T = mat('horn', hexc('#d8c8a8'), 0.1, 0.4, tex='chitin2'); E = glow('#ffb048', 3, 'eye')
    root = empty('root'); body = empty('body', (0, 0, 28), root)
    sph('torso', (30, 20, 17), (0, 0, 30), H, body, 20, 12)
    for i in range(5): sph(f'plate{i}', (7, 17 - abs(i - 2) * 2, 5), (14 - i * 7, 0, 44 - abs(i - 2) * 2), P, body, 12, 7)
    head = empty('head', (26, 0, 28), body)
    sph('headm', (12, 10, 9), (34, 0, 26), H, head, 16, 10)
    seg('horn_main', (40, 0, 31), (52, 0, 44), 3.2, T, head, r2=0.3, verts=10)
    for s in (1, -1):
        seg(f'tusk{s}', (40, 6 * s, 22), (50, 10 * s, 28), 2.2, T, head, r2=0.2, verts=8)
        sph('eye', (1.4,) * 3, (42, 6 * s, 30), E, head, 8, 5)
    legs = []
    for i, x in enumerate((16, -16)):
        for side, s in (('L', 1), ('R', -1)):
            hip = empty(f'leg{i}{side}', (x, 15 * s, 26), body)
            seg(f'thigh{i}{side}', (x, 15 * s, 26), (x + 2, 17 * s, 13), 6, H, hip, verts=10)
            kn = empty(f'knee{i}{side}', (x + 2, 17 * s, 13), hip)
            seg(f'shin{i}{side}', (x + 2, 17 * s, 13), (x, 17 * s, 2), 5, P, kn, verts=10)
            sph(f'foot{i}{side}', (6.5, 6.5, 2.4), (x + 1, 17 * s, 2), H, kn, 10, 6)
            legs.append((hip, kn, i, s))
    world_to_local()
    n = 36
    for f in range(1, n + 2, n // 6):
        ph = (f - 1) / n * 2 * math.pi
        for hip, kn, i, s in legs:
            g = 1 if (i + (0 if s > 0 else 1)) % 2 == 0 else -1
            key('run', hip, f, rot=(0, math.sin(ph) * g * 0.35, 0)); key('run', kn, f, rot=(0, max(0, -math.sin(ph) * g) * 0.4, 0))
        key('run', body, f, loc=(0, 0, abs(math.sin(ph)) * 1.2)); key('run', head, f, rot=(0, math.sin(ph * 2) * 0.05, 0))
    idle_breathe(body, 0.8)
    for f, (p, dz) in ((1, (0, 0)), (12, (-0.35, 8)), (18, (0.15, -3)), (30, (0, 0))):
        key('attack', body, f, rot=(0, p, 0), loc=(0, 0, dz)); key('attack', head, f, rot=(0, p * 0.5, 0))
    for f, (roll, dz) in ((1, (0, 0)), (20, (0.8, -10)), (40, (1.45, -14))): key('die', root, f, rot=(roll, 0, 0), loc=(0, 0, dz))
    bake_clips()
out = sys.argv[sys.argv.index('--') + 1]
for name, fn in [(n, f) for n, f in (('bomber', bomber), ('flyer', flyer), ('mortar', mortar), ('lancer', lancer), ('queen', queen), ('burrower', burrower), ('behemoth', behemoth)) if len(sys.argv) <= sys.argv.index('--') + 2 or n in sys.argv[sys.argv.index('--') + 2:]]:
    fn(); export(os.path.join(out, name + '.glb')); print('exported', name)
