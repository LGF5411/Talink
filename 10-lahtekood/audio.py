"""Original soundtrack generated in code (no third-party music). Usage: python3 audio.py <seconds> <pause_at> <out.wav>"""
import sys, wave, numpy as np

SR = 48000
dur, pause_at, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
n = int(SR * dur); t = np.arange(n) / SR
rng = np.random.default_rng(7)
mix = np.zeros(n)


def env(start, a, d, length=None):
    e = np.zeros(n); i0 = int(start * SR)
    L = int((length or (a + d)) * SR); seg = np.arange(L) / SR
    shape = np.where(seg < a, seg / max(a, 1e-4), np.exp(-(seg - a) / max(d, 1e-4)))
    e[i0:i0 + L] = shape[: max(0, min(L, n - i0))]
    return e


def lowpass(x, k):
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):  # one-pole
        acc += k * (x[i] - acc); y[i] = acc
    return y


# --- 1. December rush: ticking + notification pings + city rumble, accelerating
rush = t < pause_at
tick_times, tt, step = [], 0.05, 0.42
while tt < pause_at - 0.05:
    tick_times.append(tt); tt += step; step = max(0.11, step * 0.9)
for i, s in enumerate(tick_times):
    f = 2400 if i % 2 else 1900
    mix += 0.22 * np.sin(2 * np.pi * f * t) * env(s, 0.001, 0.018)
for s in np.linspace(0.6, pause_at - 0.4, 7):
    f = rng.choice([880, 988, 1175, 1318])
    e = env(s, 0.004, 0.16)
    mix += 0.16 * (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t)) * e
rumble = lowpass(rng.normal(0, 1, n), 0.02) * 1.6
ramp = np.clip(t / max(pause_at, 0.1), 0, 1) ** 1.5
mix += rumble * ramp * rush * 0.55

# --- 2. The pause: hard cut + soft click
click = int(pause_at * SR)
mix[click:] *= 0
mix += 0.5 * np.sin(2 * np.pi * 140 * t) * env(pause_at, 0.001, 0.05) + 0.25 * rng.normal(0, 1, n) * env(pause_at, 0.0005, 0.008)

# --- 3. Calm: warm pad (Dmaj9) + sea noise + chime
calm_start = pause_at + 0.9
pad = np.zeros(n)
for f in (146.83, 220.0, 277.18, 329.63, 369.99):
    detune = np.sin(2 * np.pi * 0.11 * t) * 0.6
    pad += np.sin(2 * np.pi * (f + detune) * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
pe = np.clip((t - calm_start) / 2.2, 0, 1) * np.clip((dur - t) / 1.2, 0, 1)
mix += pad / 5 * 0.32 * pe
sea = lowpass(rng.normal(0, 1, n), 0.008)
swell = 0.6 + 0.4 * np.sin(2 * np.pi * t / 5.5)
mix += sea * swell * pe * 2.2
for s, f in ((calm_start + 0.2, 1174.66), (dur - 3.6, 880.0), (dur - 3.3, 1318.5)):
    if 0 < s < dur:
        mix += 0.12 * np.sin(2 * np.pi * f * t) * env(s, 0.005, 1.4, 3.0)

mix = np.tanh(mix * 1.1) * 0.85
fade = np.clip((dur - t) / 0.4, 0, 1); mix *= fade
pcm = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("ok", out, dur, "s")
