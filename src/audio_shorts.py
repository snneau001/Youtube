#!/usr/bin/env python3
"""Synthesizes the soundtrack for the vertical "Dog & Cat: Best Friends"
YouTube Short -- same warm/cheerful palette as audio_bff.py, retimed to
the tighter ~26.5s Shorts cut (hook-first, no lead-in silence).

Usage: python3 audio_shorts.py <output_dir>
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

from audio import (
    SR, mix_at,
    sfx_twinkle, sfx_kazoo_riff, sfx_bark, sfx_meow, sfx_whoosh,
    sfx_outro_jingle, sfx_boing, sfx_footstep_pat,
)
from audio_bff import sfx_nom, sfx_purr, sfx_soft_chime

TOTAL_DURATION = 26.5


def build_soundtrack():
    track = np.zeros(int(SR * TOTAL_DURATION) + SR)

    # 0-9 chase: hook sting right at frame 0, riff loops, chirps, hedge-hop boings
    mix_at(track, sfx_twinkle(0.22), 0.05)
    riff_t = 0.3
    while riff_t < 8.6:
        mix_at(track, sfx_kazoo_riff(0.17), riff_t)
        riff_t += 2.3
    mix_at(track, sfx_bark(0.14), 1.0)
    mix_at(track, sfx_meow(0.13), 3.2)
    mix_at(track, sfx_bark(0.12), 5.4)
    mix_at(track, sfx_meow(0.12), 7.4)
    mix_at(track, sfx_boing(0.15), 1.96)
    mix_at(track, sfx_boing(0.14), 5.87)
    fp = 0.3
    while fp < 8.8:
        mix_at(track, sfx_footstep_pat(0.05), fp)
        fp += 0.28

    # 9-10.5 heading in
    mix_at(track, sfx_whoosh(0.2), 9.1)

    # 10.5-11.5 cut indoors
    mix_at(track, sfx_soft_chime(0.18), 10.6)

    # 11.5-18 sharing the bowl
    mix_at(track, sfx_bark(0.1), 11.6)
    nt = 12.8
    while nt < 15.2:
        mix_at(track, sfx_nom(0.15), nt)
        nt += 0.3
    mix_at(track, sfx_meow(0.1), 15.3)
    nt = 15.6
    while nt < 17.7:
        mix_at(track, sfx_nom(0.14), nt)
        nt += 0.3
    mix_at(track, sfx_purr(0.07, dur=5.0), 12.0)

    # 18-21.5 nuzzle
    mix_at(track, sfx_twinkle(0.16), 18.5)
    mix_at(track, sfx_purr(0.09, dur=2.8), 18.7)

    # 21.5-26.5 punchline / end card
    mix_at(track, sfx_outro_jingle(0.26), 22.2)

    track = track[: int(SR * TOTAL_DURATION)]
    peak = np.max(np.abs(track)) or 1.0
    track = track / peak * 0.85
    return track


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/audio_shorts"
    os.makedirs(out_dir, exist_ok=True)
    track = build_soundtrack()
    pcm = (track * 32767).astype(np.int16)
    out_path = os.path.join(out_dir, "soundtrack_shorts.wav")
    wavfile.write(out_path, SR, pcm)
    print(f"wrote {out_path} ({len(track) / SR:.2f}s)")


if __name__ == "__main__":
    main()
