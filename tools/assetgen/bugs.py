import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from common import *
def legs6(parent_body, xs, y0, z0, length, thick, M, spread=1.0, prefix='leg', foot_z=0.4):
    out = []
    n = len(xs)
    for i, x in enumerate(xs):
        dx = (1 - i) * length * 0.32 * spread if n == 3 else ((0.5 - i) * length * 0.5 * spread)
        for side, s in (('L', 1), ('R', -1)):
            H = (x, y0 * s, z0)
            K = (x + dx * 0.6, (y0 + length * 0.5) * s, z0 + length * 0.35)
            F = (x + dx * 1.3, (y0 + length * 0.95) * s, foot_z if foot_z is not None else 0.4)
            hip = empty(f'{prefix}{i}{side}', H, parent_body)
            seg(f'{prefix}{i}{side}_a', H, K, thick, M, hip)
            kn = empty(f'{prefix}{i}{side}_k', K, hip)
            seg(f'{prefix}{i}{side}_b', K, F, thick * 0.8, M, kn, r2=thick * 0.2)
            out.append((hip, kn, i, s))
    return out
def walk(clip, legs, frames=16, amp=0.45):
    for f in range(1, frames + 2, frames // 4):
        ph = (f - 1) / frames * 2 * math.pi
        for hip, kn, i, s in legs:
            g = 1 if (i + (0 if s > 0 else 1)) % 2 == 0 else -1  # tripod gait
            key(clip, hip, f, rot=(max(0, math.sin(ph) * g) * 0.35 * s, 0, math.cos(ph) * g * amp))
def build_beetle(heavy=False):
    reset(); CLIPS.clear()
    C = mat('chitin', hexc('#6e4a30' if not heavy else '#4c3626'), 0.15, 0.4, tex='chitin')
    C2 = mat('plate', hexc('#8a6040' if not heavy else '#5e4430'), 0.2, 0.35, tex='chitin2')
    J = mat('joint', hexc('#3a2618'), 0.1, 0.6, tex='chitin2')
    T = mat('tusk', hexc('#d8c6a2'), 0.1, 0.4)
    E = mat('eye', hexc('#ffb040'), 0, 0.2, emit=hexc('#ff8a20'), strength=4)
    k = 1.6 if heavy else 1.0
    root = empty('root'); body = empty('body', (0, 0, 5 * k), root)
    sph('abdomen', (8 * k, 6.5 * k, 4.4 * k), (-4 * k, 0, 5.6 * k), C, body, 14, 8)
    for i in range(3):
        sph(f'shell{i}', (3.2 * k, 6.0 * k - i * 0.6 * k, 1.6 * k), (-1.5 * k - i * 3.6 * k, 0, 8.6 * k - i * 0.5 * k), C2, body, 10, 6)
    sph('thorax', (4.2 * k, 4.6 * k, 3.4 * k), (3.2 * k, 0, 5.4 * k), C2, body, 12, 7)
    head = empty('head', (6.6 * k, 0, 5.2 * k), body)
    sph('headm', (2.8 * k, 3.2 * k, 2.4 * k), (7.6 * k, 0, 5.2 * k), C, head, 10, 7)
    for s in (1, -1):
        sph('eye', (0.6 * k,) * 3, (9.4 * k, 1.5 * k * s, 6.0 * k), E, head, 6, 4)
        jaw = empty(f'jaw{s}', (9.6 * k, 1.4 * k * s, 4.6 * k), head)
        cyl(f'mand{s}', 0.7 * k, 5 * k, (11.6 * k, 0.6 * k * s, 4.4 * k), T, jaw, rot=(0, math.pi / 2, -0.45 * s), verts=6, r2=0.1)
    if heavy:
        cyl('horn', 1.4 * k, 8 * k, (10.5 * k, 0, 8 * k), T, head, rot=(0, 1.0, 0), verts=8, r2=0.2)
        for i in range(4):
            cyl(f'spike{i}', 0.9 * k, 3 * k, (-1 * k - i * 3 * k, 0, 10.4 * k - i * 0.4 * k), T, body, verts=6, r2=0.1)
    legs = legs6(body, (3 * k, 0.5 * k, -2.2 * k), 3.2 * k, 4.6 * k, 9 * k, 0.75 * k, J)
    world_to_local()
    walk('run', legs, 16 if not heavy else 24, 0.45 if not heavy else 0.35)
    for f in (1, 17 if not heavy else 25): key('run', body, f, loc=(0, 0, 0))
    key('run', body, 5 if not heavy else 7, loc=(0, 0, 0.4 * k)); key('run', body, 13 if not heavy else 19, loc=(0, 0, 0.4 * k))
    for f, r in ((1, 0), (30, 0.04), (60, 0)): key('idle', body, f, loc=(0, 0, r * 10 * k)); key('idle', head, f, rot=(0, 0, r * 3))
    for f, (lean, jaw) in ((1, (0, 0)), (4, (-0.15, 0.5)), (8, (0.25, -0.2)), (14, (0, 0))):
        key('attack', body, f, rot=(0, lean, 0), loc=(lean * 8 * k, 0, 0))
        for s in (1, -1): key('attack', bpy.data.objects[f'jaw{s}'], f, rot=(0, 0, jaw * s))
    for f, (roll, dz) in ((1, (0, 0)), (6, (1.2, 1.5)), (12, (3.0, -2)), (24, (3.1, -3.5))):
        key('die', root, f, rot=(roll, 0, 0), loc=(0, 0, dz * k + (6 * k if roll > 2 else 0)))
    for hip, kn, i, s in legs:
        for f, a in ((1, 0), (12, 0.8), (24, 0.9)): key('die', hip, f, rot=(a * s, 0, 0))
    bake_clips()
def build_spitter():
    reset(); CLIPS.clear()
    C = mat('chitin', hexc('#56683a'), 0.15, 0.4, tex='chitin'); J = mat('joint', hexc('#2e3a1c'), 0.1, 0.6, tex='chitin2')
    S = mat('sac', hexc('#6fae36'), 0, 0.3, emit=hexc('#4a9a18'), strength=0.45)
    E = mat('eye', hexc('#d8ff9a'), 0, 0.2, emit=hexc('#b8ff6a'), strength=4)
    root = empty('root'); body = empty('body', (0, 0, 6), root)
    sph('thorax', (5, 5, 4), (2.5, 0, 6.5), C, body, 12, 7)
    sac = empty('sacpivot', (-4, 0, 8), body)
    sph('sac', (6.5, 6, 6), (-5, 0, 8.5), S, sac, 16, 10)
    for i in range(5):
        a = i / 5 * math.pi * 2
        sph(f'vein{i}', (5.2, 0.5, 0.5), (-5, math.cos(a) * 4.2, 8.5 + math.sin(a) * 4.2), C, sac, 8, 4, rot=(a, 0, 0))
    head = empty('head', (6.5, 0, 6.5), body)
    sph('headm', (2.6, 3, 2.4), (7.4, 0, 6.6), C, head, 10, 7)
    cyl('spout', 1.4, 3.6, (10, 0, 6.8), C, head, rot=(0, math.pi / 2, 0), verts=10, r2=0.9)
    cyl('spout_glow', 0.8, 0.4, (11.9, 0, 6.8), S, head, rot=(0, math.pi / 2, 0), verts=10)
    for s in (1, -1): sph('eye', (0.5,) * 3, (8.8, 1.6 * s, 7.6), E, head, 6, 4)
    legs = legs6(body, (3.5, 1.0, -1.5), 3.0, 5.2, 8, 0.6, J)
    world_to_local()
    walk('run', legs, 20, 0.4)
    for f, sc in ((1, 0), (30, 0.6), (60, 0)): key('idle', sac, f, loc=(0, 0, sc))
    # charge: sac swells then head snaps forward (shoot)
    for f, (sw, lean) in ((1, (0, 0)), (12, (1.2, -0.12)), (16, (-0.6, 0.2)), (24, (0, 0))):
        key('attack', sac, f, loc=(-sw, 0, sw)); key('attack', head, f, rot=(0, -lean, 0)); key('attack', body, f, rot=(0, lean * 0.5, 0))
    for f, (roll, dz) in ((1, (0, 0)), (8, (1.4, 1)), (20, (3.1, 2))):
        key('die', root, f, rot=(roll, 0, 0), loc=(0, 0, dz + (7 if roll > 2 else 0)))
    bake_clips()
def build_mech():
    reset(); CLIPS.clear()
    A = mat('armor', hexc('#6e7a84'), 0.45, 0.5, tex='paintworn'); D = mat('dark', hexc('#4a4f55'), 0.7, 0.45, tex='plate')
    Y = mat('hazard', hexc('#c99a2e'), 0.3, 0.5, tex='paint'); V = mat('glass', hexc('#9fe3ff'), 0, 0.15, emit=hexc('#6fc8ff'), strength=2.5)
    B = mat('blue', hexc('#4a6680'), 0.45, 0.5, tex='paintworn')
    root = empty('root'); pelvis = empty('pelvis', (0, 0, 22), root)
    box('hipblock', (10, 14, 5), (0, 0, 22), D, pelvis, 0.8)
    cab = empty('cabin', (0, 0, 24), pelvis)
    box('cab', (18, 20, 11), (1, 0, 30), A, cab, 1.6)
    box('cab_top', (12, 14, 3), (0, 0, 36.5), B, cab, 0.8)
    box('canopy', (3, 12, 4.5), (10.4, 0, 31.5), V, cab, 0.8)
    box('stripe', (18.4, 20.4, 1.2), (1, 0, 26), Y, cab, 0.2)
    box('engine', (6, 12, 7), (-10, 0, 31), D, cab, 0.8)
    for s in (1, -1):
        for j in range(2): cyl('exhaust', 1.2, 4, (-12, (3 - j * 6) * 0.9, 36), D, cab, verts=8)
        g = empty(f'gun{s}', (4, 12.5 * s, 29), cab)
        box(f'gunpod{s}', (12, 5, 5), (6, 12.5 * s, 29), A, g, 0.7)
        for j in (-1, 1): cyl(f'barrel{s}{j}', 0.8, 9, (16, (12.5 + j * 1.3) * s, 29), D, g, rot=(0, math.pi / 2, 0), verts=8)
    legs = {}
    for side, s in (('L', 1), ('R', -1)):
        th = empty('thigh' + side, (0, 6.5 * s, 22), pelvis)
        box('thighm' + side, (5, 4, 11), (2.2, 6.8 * s, 17.5), A, th, 0.8, rot=(0, 0.45, 0))
        kn = empty('knee' + side, (4.2, 6.8 * s, 12.5), th)
        cyl('kneecyl' + side, 2.6, 5, (4.2, 6.8 * s, 12.5), D, kn, rot=(math.pi / 2, 0, 0), verts=10)
        box('shin' + side, (4, 3.6, 11), (1.0, 6.8 * s, 7.5), A, kn, 0.7, rot=(0, -0.5, 0))
        an = empty('ankle' + side, (-1.6, 6.8 * s, 2.4), kn)
        box('foot' + side, (11, 6, 2.6), (0.4, 6.8 * s, 1.3), D, an, 0.6)
        legs[side] = (th, kn, an)
    world_to_local()
    n = 30
    for f in range(1, n + 2, n // 6):
        ph = (f - 1) / n * 2 * math.pi
        for side, s in (('L', 1), ('R', -1)):
            th, kn, an = legs[side]; a = math.sin(ph) * s
            key('run', th, f, rot=(0, -a * 0.45, 0)); key('run', kn, f, rot=(0, max(0, math.cos(ph) * s) * 0.5, 0)); key('run', an, f, rot=(0, a * 0.3, 0))
        key('run', pelvis, f, loc=(0, 0, -abs(math.sin(ph)) * 1.4)); key('run', cab, f, rot=(math.sin(ph) * 0.04, 0, 0))
    for f, z in ((1, 0), (30, 0.5), (60, 0)): key('idle', cab, f, loc=(0, 0, z))
    for f, r in ((1, 0), (2, -1.6), (6, 0)):
        for s in (1, -1): key('shoot', bpy.data.objects[f'gun{s}'], f, loc=(r, 0, 0))
    for f, (pitch, dz) in ((1, (0, 0)), (10, (0.3, -6)), (20, (0.5, -14)), (30, (0.5, -14))):
        key('die', root, f, rot=(0, pitch, 0), loc=(0, 0, dz * 0.4))
    bake_clips()
def build_turret():
    reset(); CLIPS.clear()
    UVS['scale'] = 40.0
    A = mat('armor', hexc('#6e767c'), 0.45, 0.5, tex='paintworn'); D = mat('dark', hexc('#55595e'), 0.6, 0.5, tex='concrete')
    Y = mat('hazard', hexc('#c99a2e'), 0.3, 0.5, tex='paint'); B = mat('blue', hexc('#4a6680'), 0.45, 0.5, tex='paintworn'); V = mat('glass', hexc('#9fe3ff'), 0, 0.15, emit=hexc('#6fc8ff'), strength=2.5)
    root = empty('root')
    box('base', (80, 80, 12), (0, 0, 6), D, root, 2)
    box('base_top', (66, 66, 6), (0, 0, 14), A, root, 2)
    for x, y in ((-34, -34), (34, -34), (-34, 34), (34, 34)): box('corner', (10, 10, 7), (x, y, 15), Y, root, 1)
    cyl('ring', 24, 6, (0, 0, 19), D, root, verts=24)
    head = empty('turret_head', (0, 0, 22), root)
    cyl('dome', 20, 12, (0, 0, 28), B, head, verts=24, r2=15)
    box('mantlet', (14, 22, 12), (14, 0, 29), A, head, 2)
    box('sensor', (4, 10, 3), (8, 0, 35.5), V, head, 0.6)
    for s in (1, -1):
        cyl(f'barrel{s}', 2.2, 34, (34, 6 * s, 29), D, head, rot=(0, math.pi / 2, 0), verts=10)
        cyl(f'muzzle{s}', 3.0, 4, (50, 6 * s, 29), A, head, rot=(0, math.pi / 2, 0), verts=10)
    world_to_local(); bake_clips()
if __name__ == '__main__':
  out = sys.argv[sys.argv.index('--') + 1]
  for name, fn in (('beetle', lambda: build_beetle(False)), ('brute', lambda: build_beetle(True)), ('spitter', build_spitter), ('mech', build_mech), ('tower', build_turret)):
    fn(); export(os.path.join(out, name + '.glb')); print('exported', name)
