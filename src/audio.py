#!/usr/bin/env python3
"""Synthesizes every sound in the video from scratch with numpy -- comic
boings, barks, meows, squeaks, chase percussion, and a xylophone jingle.
No sampled/licensed audio anywhere.

Usage: python3 audio.py <output_dir>
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

SR = 44100
TOTAL_DURATION = 40.0


def _fade(n, edge=200):
    env = np.ones(n)
    e = min(edge, n // 2)
    if e > 0:
        env[:e] = np.linspace(0, 1, e)
        env[-e:] = np.linspace(1, 0, e)
    return env


def tone(freq, dur, shape="sine", vol=0.3, vibrato=0.0, decay=True):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = freq * (1 + vibrato * np.sin(2 * np.pi * 6 * t)) if vibrato else freq
    if shape == "sine":
        w = np.sin(2 * np.pi * f * t)
    elif shape == "square":
        w = np.sign(np.sin(2 * np.pi * f * t))
    elif shape == "saw":
        w = 2 * (t * f - np.floor(0.5 + t * f))
    elif shape == "triangle":
        w = 2 * np.abs(2 * (t * f - np.floor(t * f + 0.5))) - 1
    else:
        w = np.sin(2 * np.pi * f * t)
    if decay:
        w *= np.exp(-3.0 * t / dur)
    w *= _fade(n)
    return (w * vol).astype(np.float64)


def sweep(f0, f1, dur, shape="sine", vol=0.3):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = np.linspace(f0, f1, n)
    phase = 2 * np.pi * np.cumsum(f) / SR
    if shape == "square":
        w = np.sign(np.sin(phase))
    else:
        w = np.sin(phase)
    w *= _fade(n, edge=100)
    return (w * vol).astype(np.float64)


def noise_burst(dur, vol=0.2, lowpass=None):
    n = int(SR * dur)
    w = np.random.uniform(-1, 1, n)
    if lowpass:
        k = max(1, int(SR / lowpass))
        kernel = np.ones(k) / k
        w = np.convolve(w, kernel, mode="same")
    w *= _fade(n)
    w *= np.exp(-4.0 * np.arange(n) / n)
    return (w * vol).astype(np.float64)


def silence(dur):
    return np.zeros(int(SR * dur))


def mix_at(track, clip, start_time):
    start = int(start_time * SR)
    end = start + len(clip)
    if end > len(track):
        clip = clip[: len(track) - start]
        end = len(track)
    track[start:end] += clip
    return track


# --- comedic sound effects ------------------------------------------------

def sfx_boing(vol=0.35):
    return sweep(220, 700, 0.28, shape="triangle", vol=vol)


def sfx_boing_down(vol=0.3):
    return sweep(700, 140, 0.35, shape="triangle", vol=vol)


def sfx_bark(vol=0.3):
    a = sweep(320, 180, 0.11, shape="square", vol=vol)
    b = noise_burst(0.05, vol=vol * 0.4)
    b = np.pad(b, (0, max(0, len(a) - len(b))))[: len(a)]
    return a + b


def sfx_meow(vol=0.25):
    clip = np.zeros(int(SR * 0.42))
    mix_at(clip, sweep(520, 780, 0.22, shape="sine", vol=vol), 0.0)
    mix_at(clip, sweep(780, 420, 0.18, shape="sine", vol=vol * 0.8), 0.2)
    return clip


def sfx_squeak(vol=0.28):
    return sweep(900, 1400, 0.09, shape="sine", vol=vol)


def sfx_record_scratch(vol=0.3):
    return noise_burst(0.35, vol=vol, lowpass=3500) * np.sign(np.sin(2 * np.pi * 40 * np.arange(int(SR * 0.35)) / SR))


def sfx_whoosh(vol=0.25):
    return sweep(1200, 300, 0.3, shape="sine", vol=vol) * np.linspace(0.2, 1, int(SR * 0.3))


def sfx_crash(vol=0.32):
    return noise_burst(0.3, vol=vol, lowpass=1800)


def sfx_twinkle(vol=0.22):
    notes = [1046, 1318, 1568]
    clip = np.zeros(int(SR * 0.9))
    for i, f in enumerate(notes):
        mix_at(clip, tone(f, 0.28, shape="sine", vol=vol), i * 0.18)
    return clip


def sfx_kazoo_riff(vol=0.22):
    seq = [392, 440, 494, 440, 392, 349, 392, 494]
    clip = np.zeros(int(SR * 2.4))
    for i, f in enumerate(seq):
        mix_at(clip, tone(f, 0.28, shape="saw", vol=vol, vibrato=0.03), i * 0.3)
    return clip


def sfx_deflate(vol=0.25):
    return sweep(500, 90, 0.6, shape="triangle", vol=vol)


def sfx_uhoh(vol=0.25):
    clip = np.zeros(int(SR * 0.5))
    mix_at(clip, tone(300, 0.18, shape="square", vol=vol), 0.0)
    mix_at(clip, tone(220, 0.22, shape="square", vol=vol), 0.2)
    return clip


def sfx_outro_jingle(vol=0.28):
    notes = [523, 659, 784, 1046, 784, 1046]
    clip = np.zeros(int(SR * 2.2))
    for i, f in enumerate(notes):
        mix_at(clip, tone(f, 0.4, shape="triangle", vol=vol), i * 0.28)
    return clip


def sfx_footstep_pat(vol=0.12):
    return noise_burst(0.05, vol=vol, lowpass=800)


def sfx_punch(vol=0.28):
    clip = np.zeros(int(SR * 0.14))
    mix_at(clip, tone(150, 0.09, shape="square", vol=vol), 0.0)
    mix_at(clip, noise_burst(0.07, vol=vol * 0.7, lowpass=650), 0.0)
    return clip


def build_soundtrack():
    track = np.zeros(int(SR * TOTAL_DURATION) + SR)

    # 0-3 title
    mix_at(track, sfx_boing(0.32), 0.15)

    # 3-6 standoff
    mix_at(track, sfx_record_scratch(0.28), 3.05)
    mix_at(track, sfx_bark(0.28), 4.1)

    # 6-11 dash
    mix_at(track, sfx_whoosh(0.3), 6.1)
    mix_at(track, sfx_whoosh(0.26), 6.4)
    for i in range(10):
        mix_at(track, sfx_footstep_pat(0.1), 6.2 + i * 0.42)

    # 11-17 tug of war: rhythmic squeaks + grunts
    tt = 11.2
    while tt < 16.8:
        mix_at(track, sfx_squeak(0.22), tt)
        tt += 0.5
    mix_at(track, sfx_bark(0.2), 12.5)
    mix_at(track, sfx_meow(0.18), 14.5)

    # 17-20 snap: boing + crash + wobble
    mix_at(track, sfx_boing_down(0.3), 17.05)
    mix_at(track, sfx_crash(0.32), 17.3)
    mix_at(track, sfx_crash(0.28), 17.5)

    # 20-24 daze: twinkles
    mix_at(track, sfx_twinkle(0.24), 20.3)
    mix_at(track, sfx_twinkle(0.2), 21.6)
    mix_at(track, sfx_twinkle(0.18), 22.9)

    # 24-30 round two: pounce, scuffle punches, dizzy separation
    mix_at(track, sfx_boing(0.26), 24.1)  # pounce takeoff
    mix_at(track, sfx_crash(0.24), 25.05)  # both land / collide
    for btime in [0.28, 0.37, 0.47, 0.56, 0.65, 0.74, 0.82]:
        mix_at(track, sfx_punch(0.24), 24.0 + btime * 6.0)
    mix_at(track, sfx_bark(0.16), 25.4)
    mix_at(track, sfx_meow(0.16), 26.1)
    mix_at(track, sfx_bark(0.14), 27.3)
    mix_at(track, sfx_meow(0.14), 28.1)
    mix_at(track, sfx_boing_down(0.22), 29.05)  # burst apart
    mix_at(track, sfx_twinkle(0.16), 29.3)

    # 30-35 the draw: deflate + pant tones
    mix_at(track, sfx_deflate(0.22), 30.1)

    # 35-40 punchline
    mix_at(track, sfx_uhoh(0.26), 35.3)
    mix_at(track, sfx_outro_jingle(0.26), 36.6)

    track = track[: int(SR * TOTAL_DURATION)]
    peak = np.max(np.abs(track)) or 1.0
    track = track / peak * 0.85
    return track


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/audio"
    os.makedirs(out_dir, exist_ok=True)
    track = build_soundtrack()
    pcm = (track * 32767).astype(np.int16)
    out_path = os.path.join(out_dir, "soundtrack.wav")
    wavfile.write(out_path, SR, pcm)
    print(f"wrote {out_path} ({len(track) / SR:.2f}s)")


if __name__ == "__main__":
    main()
