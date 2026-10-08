import numpy as np, scipy.signal as sg, subprocess, os, sys
SR = 44100; rng = np.random.default_rng(11); OUT = sys.argv[1]
def note(n): return 440 * 2 ** ((n - 69) / 12)
def t(d): return np.arange(int(SR * d)) / SR
def lp(x, f, o=2): b, a = sg.butter(o, f / (SR / 2), 'low'); return sg.lfilter(b, a, x)
def hp(x, f, o=2): b, a = sg.butter(o, f / (SR / 2), 'high'); return sg.lfilter(b, a, x)
def bp(x, lo, hi): b, a = sg.butter(2, [lo / (SR / 2), hi / (SR / 2)], 'band'); return sg.lfilter(b, a, x)
def env(d, a, r): x = t(d); return np.minimum(1, x / a) * np.exp(-x / r)
def kick(): d = 0.5; x = t(d); f = 45 + 110 * np.exp(-x * 30); return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 7))
def taiko(): d = 0.9; x = t(d); f = 70 + 60 * np.exp(-x * 20); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 4.5) + lp(rng.standard_normal(len(x)), 600) * np.exp(-x * 25) * 0.5
def snare(): d = 0.35; x = t(d); return bp(rng.standard_normal(len(x)), 800, 7000) * np.exp(-x * 14) * 0.8 + np.sin(2 * np.pi * 190 * x) * np.exp(-x * 25) * 0.5
def hat(): d = 0.08; x = t(d); return hp(rng.standard_normal(len(x)), 7000) * np.exp(-x * 60) * 0.35
def saw(f, d, det=0.003, voices=3):
    x = t(d); return sum(sg.sawtooth(2 * np.pi * f * (1 + det * (v - 1)) * x + rng.random() * 6) for v in range(voices)) / voices
def place(buf, s, start):
    i = int(start * SR); e = min(len(buf), i + len(s));
    if i < len(buf): buf[i:e] += s[:e - i]
def verb(x, d=2.0, mix=0.3):
    ir = rng.standard_normal(int(SR * d)) * np.exp(-t(d) / (d / 5)); ir = lp(ir, 3000); ir /= np.sqrt((ir ** 2).sum()) * 6
    w = sg.fftconvolve(x, ir)[:len(x)]; return x * (1 - mix) + w * mix
def track(name, bpm, bars, prog, drums, bass_pat, pad_lvl, stab, dark=0.0):
    beat = 60 / bpm; bar = beat * 4; L = bars * bar
    D = np.zeros(int(SR * (L + 2))); B = D.copy(); P = D.copy(); ST = D.copy()
    for b in range(bars):
        root = prog[b % len(prog)]; t0 = b * bar
        for step in range(16):
            ts = t0 + step * beat / 4
            if drums and step in drums.get('kick', ()): place(D, kick() * 0.9, ts)
            if drums and step in drums.get('taiko', ()): place(D, taiko() * 0.8, ts)
            if drums and step in drums.get('snare', ()) and b % 8 != 7: place(D, snare() * 0.6, ts)
            if drums and step in drums.get('hat', ()): place(D, hat() * (0.7 if step % 4 else 1), ts)
        if drums and b % 8 == 7:
            for k in range(8): place(D, taiko() * (0.4 + k * 0.07), t0 + bar / 2 + k * beat / 4)
        for i, n in enumerate(bass_pat):
            if n is None: continue
            d = beat / 2; s = lp(saw(note(root - 24 + n), d, 0.002, 2), 500) * env(d, 0.005, 0.25)
            place(B, s, t0 + i * beat / 2)
        chord = [root - 12, root - 5, root + 3 - (0 if b % 2 else 0)]
        pd = sum(lp(saw(note(c), bar, 0.004, 3), 900 + 400 * np.sin(b)) for c in chord) / 3
        x = t(bar); pd *= np.minimum(1, x / 0.6) * np.minimum(1, (bar - x) / 0.3 + 0.2)
        place(P, pd * pad_lvl, t0)
        if stab and b % 2 == 0:
            for c in chord: place(ST, lp(saw(note(c + 12), beat * 1.5, 0.006, 4), 1600) * env(beat * 1.5, 0.01, 0.35) * 0.35, t0)
    drone = lp(saw(note(prog[0] - 24), L + 2, 0.002, 4), 200) * (0.25 + dark)
    mixd = verb(D, 1.2, 0.2) * 0.9 + B * 0.55 + verb(P, 2.5, 0.45) * 0.6 + verb(ST, 1.8, 0.35) * 0.6 + drone[:len(D)]
    mixd = mixd[:int(SR * L)]
    fade = int(SR * 0.05); mixd[:fade] *= np.linspace(0, 1, fade); mixd[-fade:] *= np.linspace(1, 0, fade)
    left = mixd; right = np.concatenate([np.zeros(int(SR * 0.012)), mixd[:-int(SR * 0.012)]])
    st = np.stack([left, right], 1); st = np.tanh(st / np.abs(st).max() * 1.6) * 0.85
    raw = os.path.join(OUT, name + '.raw'); st.astype(np.float32).tofile(raw)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', raw, '-c:a', 'libvorbis', '-q:a', '5', os.path.join(OUT, name + '.ogg')], check=True)
    os.remove(raw); print(name, round(L, 1), 's')
os.makedirs(OUT, exist_ok=True)
D_MIN = 50  # D3
track('menu', 70, 16, [D_MIN, 46, 41, 48], {'taiko': (0,), 'kick': (10,)}, [0, None, None, None, 7, None, None, None], 1.0, False, 0.15)
track('battle', 112, 32, [D_MIN, D_MIN, 46, 48], {'kick': (0, 6, 8, 11), 'snare': (4, 12), 'hat': tuple(range(0, 16, 2)), 'taiko': (0,)}, [0, 0, 12, 0, 0, 10, 0, 7], 0.7, True)
track('boss', 132, 32, [D_MIN, 51, 46, 49], {'kick': (0, 3, 6, 8, 10, 14), 'snare': (4, 12), 'hat': tuple(range(16)), 'taiko': (0, 8)}, [0, 0, 1, 0, 0, 1, 0, 3], 0.8, True, 0.1)
