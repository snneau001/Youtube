#!/usr/bin/env python3
"""Synthesizes the soundtrack for the real-footage "Best Friends on a
Walk" edit -- same warm/cheerful synth palette as the animated videos'
soundtracks, timed to the real clip's edit (normal-speed open, slow-mo
highlight, end card).

Usage: python3 audio_realfootage.py <output_dir> <total_duration_seconds>
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

from audio import SR, mix_at, sfx_twinkle, sfx_kazoo_riff, sfx_bark, sfx_outro_jingle
from audio_bff import sfx_purr


def build_soundtrack(total_duration, normal_end, slowmo_end):
    track = np.zeros(int(SR * total_duration) + SR)

    mix_at(track, sfx_twinkle(0.22), 0.1)
    mix_at(track, sfx_bark(0.12), 1.2)
    riff_t = 0.4
    while riff_t < normal_end:
        mix_at(track, sfx_kazoo_riff(0.14), riff_t)
        riff_t += 2.4

    mix_at(track, sfx_purr(0.08, dur=max(0.5, slowmo_end - normal_end)), normal_end + 0.1)

    mix_at(track, sfx_outro_jingle(0.24), slowmo_end + 0.3)

    track = track[: int(SR * total_duration)]
    peak = np.max(np.abs(track)) or 1.0
    track = track / peak * 0.85
    return track


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/realfootage"
    total_duration = float(sys.argv[2]) if len(sys.argv) > 2 else 13.4
    normal_end = float(sys.argv[3]) if len(sys.argv) > 3 else 4.9
    slowmo_end = float(sys.argv[4]) if len(sys.argv) > 4 else 9.9
    os.makedirs(out_dir, exist_ok=True)
    track = build_soundtrack(total_duration, normal_end, slowmo_end)
    pcm = (track * 32767).astype(np.int16)
    out_path = os.path.join(out_dir, "soundtrack_realfootage.wav")
    wavfile.write(out_path, SR, pcm)
    print(f"wrote {out_path} ({len(track) / SR:.2f}s)")


if __name__ == "__main__":
    main()
