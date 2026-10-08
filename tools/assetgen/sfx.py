import numpy as np, scipy.signal as sg, subprocess, os, sys
SR = 44100; rng = np.random.default_rng(7); OUT = sys.argv[1]
def t(d): return np.arange(int(SR * d)) / SR
def noise(d): return rng.standard_normal(int(SR * d))
def env(d, a=0.002, decay=0.2, curve=4):
    x = t(d); e = np.minimum(1, x / max(a, 1e-4)) * np.exp(-np.maximum(0, x - a) / decay * (curve / 4)); return e
def lp(x, f, o=4): b, a = sg.butter(o, min(f, SR / 2 - 100) / (SR / 2), 'low'); return sg.lfilter(b, a, x)
def hp(x, f, o=2): b, a = sg.butter(o, f / (SR / 2), 'high'); return sg.lfilter(b, a, x)
def bp(x, lo, hi, o=2): b, a = sg.butter(o, [lo / (SR / 2), hi / (SR / 2)], 'band'); return sg.lfilter(b, a, x)
def sweep(d, f0, f1, shape='exp'):
    x = t(d); f = f0 * (f1 / f0) ** (x / d) if shape == 'exp' else f0 + (f1 - f0) * x / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def dist(x, k=3): return np.tanh(x * k) / np.tanh(k)
def verb(x, d=0.8, mix=0.25, damp=3000):
    ir = noise(d) * np.exp(-t(d) / (d / 5)); ir = lp(ir, damp); ir /= np.abs(ir).sum() ** 0.5 * 8
    w = sg.fftconvolve(x, ir)[:len(x) + int(SR * d)]; y = np.pad(x, (0, len(w) - len(x)))
    return y * (1 - mix) + w * mix
def pad(x, d): return np.pad(x, (0, max(0, int(SR * d) - len(x))))
def mix(*xs):
    n = max(len(x) for x in xs); return sum(np.pad(x, (0, n - len(x))) for x in xs)
def save(name, x, gain=0.9, stereo=False):
    x = x / (np.abs(x).max() + 1e-9) * gain
    raw = os.path.join(OUT, name + '.raw'); (x.astype(np.float32)).tofile(raw)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', raw] + (['-ac', '2'] if stereo else []) +
                   ['-c:a', 'libvorbis', '-q:a', '4', os.path.join(OUT, name + '.ogg')], check=True)
    os.remove(raw)
def gunshot(d=0.35, body=180, crack=6000, tail=0.12, k=2.5):
    c = hp(noise(d), 2000) * env(d, 0.0005, 0.012); b = lp(noise(d), 1200) * env(d, 0.001, tail)
    thump = sweep(d, body, 50) * env(d, 0.001, 0.05)
    return verb(dist(c * 0.8 + b * 1.2 + thump * 0.9, k), 0.6, 0.18)
def explosion(d=2.2, big=True):
    n = noise(d); low = lp(n, 220 if big else 500) * env(d, 0.005, 0.7 if big else 0.3)
    mid = bp(n, 300, 2500) * env(d, 0.002, 0.18)
    boom = sweep(d, 90 if big else 140, 28) * env(d, 0.004, 0.35 if big else 0.18)
    deb = hp(noise(d), 3000) * env(d, 0.05, 0.6) * (rng.random(int(SR * d)) > 0.995) * 3
    return verb(dist(low * 1.6 + mid * 0.7 + boom * 1.3 + deb, 2), 1.4, 0.3, 2500)
def squelch(d=0.4, f0=500, f1=120, wet=0.6):
    x = t(d); fm = np.sin(2 * np.pi * 30 * x) * 60
    tone = np.sin(2 * np.pi * np.cumsum(f0 * (f1 / f0) ** (x / d) + fm) / SR) * env(d, 0.01, d / 3)
    gl = bp(noise(d), 300, 1800) * env(d, 0.005, d / 4) * (0.5 + 0.5 * np.sin(2 * np.pi * 22 * x))
    return verb(tone * 0.7 + gl * wet, 0.5, 0.2)
def roar(d=2.2, f=70):
    x = t(d); vib = np.sin(2 * np.pi * 6 * x) * 8
    saw = sg.sawtooth(2 * np.pi * np.cumsum(f + vib + 30 * np.sin(np.pi * x / d)) / SR)
    form = bp(saw, 250, 900) + bp(saw, 1200, 2600) * 0.5 + bp(noise(d), 400, 3000) * 0.6
    e = np.minimum(1, x / 0.25) * np.minimum(1, (d - x) / 0.6)
    return verb(dist(form * e, 2.5), 1.6, 0.35, 2000)
os.makedirs(OUT, exist_ok=True)
save('marine_shot', gunshot(0.28, 220, k=2))
save('shotgun', mix(gunshot(0.6, 120, tail=0.22, k=3.5), pad(lp(noise(0.5), 3000) * env(0.5, 0.001, 0.06) * 0.6, 0.6)))
save('plasma', verb(sweep(0.4, 2400, 300) * env(0.4, 0.002, 0.12) + bp(noise(0.4), 2000, 6000) * env(0.4, 0.001, 0.05) * 0.5 + np.sin(2 * np.pi * 90 * t(0.4)) * env(0.4, 0.001, 0.08), 0.5, 0.25))
save('rocket', verb(lp(noise(1.2), 1800) * env(1.2, 0.02, 0.5) * (1 + 0.3 * np.sin(2 * np.pi * 40 * t(1.2))) + sweep(1.2, 220, 80) * env(1.2, 0.01, 0.2) * 0.6, 0.8, 0.2))
save('turret', gunshot(0.4, 140, tail=0.15, k=3))
save('explosion_big', explosion(2.6, True))
save('explosion_small', explosion(1.2, False))
save('grenade_throw', hp(noise(0.25), 1500) * env(0.25, 0.03, 0.05) * 0.5 + np.sin(2 * np.pi * 900 * t(0.25)) * env(0.25, 0.001, 0.02))
save('flamer_loop', lp(noise(2.0), 1400) * (0.75 + 0.25 * np.sin(2 * np.pi * 7 * t(2.0))) + hp(noise(2.0), 4000) * 0.15 * (rng.random(int(SR * 2)) > 0.97))
save('acid_charge', squelch(0.7, 120, 420, 0.8))
save('acid_spit', squelch(0.35, 600, 160, 0.6))
save('acid_hit', mix(squelch(0.3, 300, 90, 1.0), hp(noise(0.3), 3000) * env(0.3, 0.001, 0.08) * 0.4))
save('bug_bite', mix(hp(noise(0.15), 2500) * env(0.15, 0.001, 0.02), squelch(0.2, 400, 200, 0.4)))
save('bug_die', mix(squelch(0.6, 700, 90, 1.0), lp(noise(0.6), 800) * env(0.6, 0.002, 0.1)))
save('bug_screech', verb(dist(bp(sg.sawtooth(2 * np.pi * np.cumsum(900 + 300 * np.sin(2 * np.pi * 13 * t(0.8))) / SR), 800, 4000) * env(0.8, 0.02, 0.3), 3), 0.6, 0.25))
save('queen_roar', roar(2.6, 60))
save('behemoth_roar', roar(2.4, 38))
save('player_hurt', mix(lp(noise(0.25), 900) * env(0.25, 0.001, 0.05), np.sin(2 * np.pi * 160 * t(0.25)) * env(0.25, 0.001, 0.08) * 0.6))
save('player_die', verb(mix(explosion(1.0, False) * 0.5, sweep(1.2, 300, 60) * env(1.2, 0.01, 0.5) * 0.6), 1.0, 0.3))
dl = 4.0; xx = t(dl)
save('dropship', verb(lp(noise(dl), 600) * (0.6 + 0.4 * np.sin(np.pi * xx / dl)) + sg.sawtooth(2 * np.pi * np.cumsum(55 + 25 * np.sin(np.pi * xx / dl)) / SR) * 0.25 * np.sin(np.pi * xx / dl), 1.0, 0.3))
save('repair_loop', bp(noise(1.5), 2500, 6000) * (0.5 + 0.5 * (np.sin(2 * np.pi * 18 * t(1.5)) > 0)) * 0.6 + np.sin(2 * np.pi * 1320 * t(1.5)) * 0.15)
save('heal_loop', sum(np.sin(2 * np.pi * f * t(2.0)) for f in (523, 659, 784)) * (0.6 + 0.4 * np.sin(2 * np.pi * 1.5 * t(2.0))) * 0.4)
save('ui_click', hp(noise(0.05), 2000) * env(0.05, 0.0005, 0.008) + np.sin(2 * np.pi * 2200 * t(0.05)) * env(0.05, 0.0005, 0.01))
save('ui_buy', mix(np.sin(2 * np.pi * 880 * t(0.12)) * env(0.12, 0.002, 0.05), pad(np.zeros(int(SR * 0.08)), 0) , np.concatenate([np.zeros(int(SR * 0.08)), np.sin(2 * np.pi * 1320 * t(0.18)) * env(0.18, 0.002, 0.08)])))
save('ui_denied', sg.square(2 * np.pi * 140 * t(0.25)) * env(0.25, 0.002, 0.1) * 0.5)
save('capture', verb(np.concatenate([np.sin(2 * np.pi * f * t(0.14)) * env(0.14, 0.003, 0.08) for f in (440, 554, 659, 880)]), 0.8, 0.3))
save('win', verb(np.concatenate([mix(*(np.sin(2 * np.pi * f * m * t(0.5)) * env(0.5, 0.01, 0.4) for m in (1, 1.5, 2))) for f in (262, 330, 392, 523)]), 1.5, 0.35))
save('lose', verb(np.concatenate([sg.sawtooth(2 * np.pi * f * t(0.6)) * env(0.6, 0.01, 0.4) * 0.6 for f in (196, 165, 131)]), 1.5, 0.35))
print('ok', len([f for f in os.listdir(OUT) if f.endswith('.ogg')]))
