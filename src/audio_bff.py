#!/usr/bin/env python3
"""Synthesizes the "Dog & Cat: Best Friends" soundtrack from scratch with
numpy -- warm chimes, an upbeat chase jingle, gentle eating sounds, and a
cozy outro. Reuses the base synth primitives from audio.py but tuned
brighter/gentler -- no fighting SFX, no licensed/sampled audio anywhere.

Usage: python3 audio_bff.py <output_dir>
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

from audio import (
    SR, tone, sweep, noise_burst, mix_at,
    sfx_twinkle, sfx_kazoo_riff, sfx_bark, sfx_meow, sfx_whoosh,
    sfx_outro_jingle, sfx_boing, sfx_footstep_pat,
)

TOTAL_DURATION = 32.0


def sfx_nom(vol=0.16):
    """A soft, happy chomp/crunch."""
    clip = np.zeros(int(SR * 0.12))
    mix_at(clip, noise_burst(0.07, vol=vol, lowpass=1400), 0.0)
    mix_at(clip, tone(340, 0.05, shape="sine", vol=vol * 0.5), 0.0)
    return clip


def sfx_purr(vol=0.1, dur=1.2):
    n = int(SR * dur)
    t = np.arange(n) / SR
    w = np.sin(2 * np.pi * 85 * t + 0.3 * np.sin(2 * np.pi * 14 * t))
    env = np.ones(n)
    edge = int(SR * 0.15)
    env[:edge] = np.linspace(0, 1, edge)
    env[-edge:] = np.linspace(1, 0, edge)
    return (w * env * vol).astype(np.float64)


def sfx_soft_chime(vol=0.2):
    return tone(1318, 0.35, shape="sine", vol=vol)


def build_soundtrack():
    track = np.zeros(int(SR * TOTAL_DURATION) + SR)

    # 0-3 title: warm welcoming chime
    mix_at(track, sfx_twinkle(0.24), 0.3)

    # 3-13.5 happy chase: cheerful riff loops, yips/chirps, soft hedge-hop boings
    riff_t = 3.2
    while riff_t < 13.0:
        mix_at(track, sfx_kazoo_riff(0.16), riff_t)
        riff_t += 2.5
    mix_at(track, sfx_bark(0.14), 4.0)
    mix_at(track, sfx_meow(0.13), 5.6)
    mix_at(track, sfx_bark(0.12), 7.8)
    mix_at(track, sfx_meow(0.12), 10.2)
    mix_at(track, sfx_boing(0.14), 5.1)
    mix_at(track, sfx_boing(0.13), 9.3)
    fp = 3.3
    while fp < 13.2:
        mix_at(track, sfx_footstep_pat(0.05), fp)
        fp += 0.3

    # 13.5-15.5 heading in
    mix_at(track, sfx_whoosh(0.2), 13.6)

    # 15.5-17.0 cut indoors
    mix_at(track, sfx_soft_chime(0.18), 15.6)

    # 17.0-23.0 sharing the bowl: gentle noms + a purr hum + a couple of chirps
    mix_at(track, sfx_bark(0.1), 17.1)
    nt = 18.6
    while nt < 20.9:
        mix_at(track, sfx_nom(0.15), nt)
        nt += 0.32
    mix_at(track, sfx_meow(0.1), 20.9)
    nt = 21.2
    while nt < 22.8:
        mix_at(track, sfx_nom(0.14), nt)
        nt += 0.32
    mix_at(track, sfx_purr(0.07, dur=5.5), 17.5)

    # 23.0-27.5 nuzzle: soft aww + purr
    mix_at(track, sfx_twinkle(0.16), 23.6)
    mix_at(track, sfx_purr(0.09, dur=3.8), 23.8)

    # 27.5-32.0 punchline: warm outro jingle
    mix_at(track, sfx_outro_jingle(0.26), 28.0)

    track = track[: int(SR * TOTAL_DURATION)]
    peak = np.max(np.abs(track)) or 1.0
    track = track / peak * 0.85
    return track


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/audio_bff"
    os.makedirs(out_dir, exist_ok=True)
    track = build_soundtrack()
    pcm = (track * 32767).astype(np.int16)
    out_path = os.path.join(out_dir, "soundtrack_bff.wav")
    wavfile.write(out_path, SR, pcm)
    print(f"wrote {out_path} ({len(track) / SR:.2f}s)")


if __name__ == "__main__":
    main()
