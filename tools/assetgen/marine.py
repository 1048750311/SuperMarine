import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from common import *
VAR = {
 'marine':    dict(armor='#6b7a88', accent='#34363a', visor='#8fe3ff', kit='rifle'),
 'player':    dict(armor='#9c7a3e', accent='#33302a', visor='#ffd27a', kit='rifle', antenna=True),
 'flamer':    dict(armor='#8a5a3e', accent='#322c28', visor='#ffb05a', kit='flamer'),
 'rocketeer': dict(armor='#66704f', accent='#2e3128', visor='#c8ff8c', kit='rocket'),
 'medic':     dict(armor='#c4c8cc', accent='#3a3d42', visor='#8fe3ff', kit='pistol', cross=True),
}
def build(v):
    reset(); CLIPS.clear()
    A = mat('armor', hexc(v['armor']), 0.4, 0.5, tex='paintworn'); D = mat('suit', hexc(v['accent']), 0.1, 0.8, tex='suit')
    V = mat('visor', hexc(v['visor']), 0.0, 0.2, emit=hexc(v['visor']), strength=3)
    G = mat('gunmetal', hexc('#3a3d40'), 0.8, 0.4, tex='gunmetal'); Y = mat('hazard', hexc('#c99a2e'), 0.3, 0.5, tex='paint')
    R = mat('red', hexc('#c62a2a'), 0.1, 0.5)
    root = empty('root')
    hips = empty('hips', (0, 0, 11), root)
    box('pelvis', (5.5, 7.5, 3), (0, 0, 11.2), D, hips, 0.6)
    box('belt', (6, 8, 1.2), (0, 0, 12.4), A, hips, 0.3)
    torso = empty('torso', (0, 0, 12.6), hips)
    box('abdomen', (5, 6.6, 2.6), (0, 0, 14.0), D, torso, 0.5)
    box('chest', (7.2, 9.6, 5.6), (0.3, 0, 17.6), A, torso, 0.9)
    box('chest_plate', (1.2, 6.4, 3.4), (4.0, 0, 17.8), A, torso, 0.4)
    box('backpack', (3.4, 7.4, 6.2), (-4.6, 0, 17.6), D, torso, 0.6)
    box('vent', (0.6, 5.4, 1), (-6.4, 0, 19.2), Y, torso, 0.2)
    if v.get('cross'):
        box('cross_h', (0.4, 3.6, 1.1), (-6.45, 0, 17.4), R, torso); box('cross_v', (0.4, 1.1, 3.6), (-6.45, 0, 17.4), R, torso)
    if v['kit'] == 'flamer':
        for y in (-2.0, 2.0): cyl('tank', 1.5, 6.5, (-6.8, y, 17.0), mat('tank', hexc('#d06a28'), 0.4, 0.4), torso)
    head = empty('head', (0, 0, 20.6), torso)
    sph('helmet', (3.2, 3.0, 3.1), (0.2, 0, 22.4), A, head, 14, 9)
    box('visor', (1.6, 4.2, 1.5), (2.7, 0, 22.4), V, head, 0.4)
    box('jaw', (2.2, 3.6, 1.4), (1.9, 0, 20.9), D, head, 0.4)
    if v.get('antenna'): cyl('antenna', 0.25, 5, (-1.5, -2.2, 25.5), G, head)
    arms = {}
    for side, s in (('L', 1), ('R', -1)):
        sh = empty('shoulder' + side, (0.2, 5.6 * s, 19.2), torso)
        sph('pauldron' + side, (3.4, 3.0, 2.6), (0.2, 6.2 * s, 19.8), A, sh, 12, 7)
        box('pauldron_trim' + side, (5.2, 0.6, 1), (0.2, 8.6 * s, 19.0), Y if side == 'L' else A, sh, 0.2)
        if v.get('cross'):
            box('pcross_h' + side, (2.4, 0.3, 0.7), (0.2, 9.0 * s, 19.6), R, sh); box('pcross_v' + side, (0.7, 0.3, 2.4), (0.2, 9.0 * s, 19.6), R, sh)
        cyl('upperarm' + side, 1.3, 4.6, (0.2, 6.0 * s, 16.6), D, sh)
        el = empty('elbow' + side, (0.2, 6.0 * s, 14.4), sh)
        cyl('forearm' + side, 1.5, 4.2, (0.2, 6.0 * s, 12.4), A, el, bevel=0.2)
        box('glove' + side, (2, 2, 1.8), (0.2, 6.0 * s, 9.9), D, el, 0.4)
        arms[side] = (sh, el)
    legs = {}
    for side, s in (('L', 1), ('R', -1)):
        th = empty('thigh' + side, (0, 2.5 * s, 11), hips)
        cyl('thighm' + side, 1.8, 5, (0, 2.6 * s, 8.4), D, th)
        box('thighplate' + side, (1, 3, 3.6), (1.7, 2.6 * s, 8.6), A, th, 0.3)
        kn = empty('knee' + side, (0, 2.6 * s, 5.8), th)
        box('kneepad' + side, (1.6, 2.8, 2.2), (1.6, 2.6 * s, 5.8), A, kn, 0.4)
        cyl('shin' + side, 1.7, 4.2, (0, 2.6 * s, 3.6), A, kn, bevel=0.2)
        box('boot' + side, (5.2, 3.2, 2), (0.9, 2.6 * s, 1.0), D, kn, 0.5)
        legs[side] = (th, kn)
    gun = empty('gun', (5.5, -1.2, 14.6), torso)
    k = v['kit']
    if k == 'rifle':
        box('rifle_body', (9, 1.8, 2.6), (6.5, -1.2, 14.8), G, gun, 0.3)
        cyl('rifle_barrel', 0.6, 5, (13, -1.2, 15.2), G, gun, rot=(0, math.pi / 2, 0))
        box('rifle_mag', (1.6, 1.4, 3.2), (6.8, -1.2, 12.6), G, gun, 0.2, rot=(0, 0.2, 0))
        box('rifle_sight', (2.2, 1, 1), (5.5, -1.2, 16.6), Y, gun, 0.1)
    elif k == 'flamer':
        box('flamer_body', (8, 2.2, 2.6), (6.2, -1.2, 14.6), G, gun, 0.3)
        cyl('flamer_nozzle', 1.1, 3.5, (11.6, -1.2, 14.8), G, gun, rot=(0, math.pi / 2, 0), r2=0.6)
        cyl('flamer_pilot', 0.45, 0.8, (13.5, -1.2, 14.8), mat('pilot', hexc('#ff8a30'), 0, 0.3, emit=hexc('#ff7a20'), strength=6), gun, rot=(0, math.pi / 2, 0))
        cyl('flamer_hose', 0.4, 9, (0, -2.4, 15), D, gun, rot=(0, math.pi / 2, 0.4))
    elif k == 'rocket':
        box('smg_body', (6, 1.6, 2.2), (6, -1.2, 14.8), G, gun, 0.3)
        cyl('launcher', 1.6, 12, (1.5, -7.8, 21.4), mat('launcher', hexc('#3e4535'), 0.5, 0.5), arms['R'][0], rot=(0, math.pi / 2, 0))
        cyl('launcher_mouth', 1.75, 0.8, (7.6, -7.8, 21.4), Y, arms['R'][0], rot=(0, math.pi / 2, 0))
    else:
        box('pistol', (4, 1.2, 1.8), (6, -1.2, 14.8), G, gun, 0.2)
        box('medkit', (3, 2.6, 2.2), (-1.5, 5, 12), mat('white', hexc('#eeeeee'), 0, 0.6), hips, 0.3)
    world_to_local()
    # rest pose: arms forward holding the weapon
    for side, (sh, el) in arms.items():
        s = 1 if side == 'L' else -1
        sh.rotation_euler = (0.1 * s, -1.15, -0.7 * s); el.rotation_euler = (0, -0.55, 0.35 * s)
    if k == 'rocket': arms['R'][0].rotation_euler = (-0.25, -1.0, 0.35)
    # clips (30 fps)
    for f, dz in ((1, 0), (30, 0.25), (60, 0)):
        key('idle', torso, f, loc=(0, 0, dz)); key('idle', head, f, rot=(0, 0, 0.05 if f == 30 else 0))
    sw = 0.75
    for f, ph in ((1, 0), (5, 1), (10, 2), (15, 3), (19, 4)):
        a = math.sin(ph / 4 * 2 * math.pi)
        for side, s in (('L', 1), ('R', -1)):
            th, kn = legs[side]
            key('run', th, f, rot=(0, -a * sw * s, 0))
            key('run', kn, f, rot=(0, max(0, a * s) * 1.1, 0))
            key('run', arms[side][0], f, rot=(0, a * 0.12 * s, 0))
        key('run', hips, f, loc=(0, 0, -abs(math.cos(ph / 4 * 2 * math.pi)) * 0.6))
        key('run', torso, f, rot=(0, 0.16, a * 0.08))
    for f, r in ((1, 0), (2, -0.09), (7, 0)):
        key('shoot', torso, f, rot=(0, r, 0)); key('shoot', gun, f, loc=(r * 12, 0, 0))
    for f, (pitch, dz) in ((1, (0, 0)), (8, (-0.4, -1)), (18, (-1.45, -9)), (24, (-1.5, -10.5)), (30, (-1.5, -10.5))):
        key('die', root, f, rot=(0, pitch, 0), loc=(-dz * 0.3, 0, dz * 0.1))
        key('die', torso, f, rot=(0, -pitch * 0.2, 0))
    bake_clips()
out = sys.argv[sys.argv.index('--') + 1]
for name, v in VAR.items():
    build(v); export(os.path.join(out, name + '.glb')); print('exported', name)
