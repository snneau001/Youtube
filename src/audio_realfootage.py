#!/usr/bin/env python3
"""Synthesizes the soundtrack for the real-footage "Best Friends" edit:
a continuous original instrumental music bed (procedurally generated,
not sampled/licensed) plus the existing warm SFX palette layered on
top, timed to the walking / running / slow-mo highlight / end-card cut.

Usage: python3 audio_realfootage.py <output_dir> <total_duration> <walk_end> <run_end> <chase_end>
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

from audio import SR, mix_at, tone, sfx_twinkle, sfx_bark, sfx_meow, sfx_outro_jingle, sfx_whoosh
from audio_bff import sfx_purr

# A-major pentatonic-ish scale (semitone offsets from root) -- cheerful,
# consonant, and generic enough to never resemble any specific melody.
ARPEGGIO_STEPS = [0, 4, 7, 12, 7, 4]


def _note_freq(root, semitones):
    return root * (2 ** (semitones / 12))


def music_bed(duration, root=220.0, bpm=104, vol=0.13):
    """A simple, fully-original looping instrumental: plucky triangle-wave
    arpeggio over a soft sine bass pulse. No sampled or licensed audio."""
    track = np.zeros(int(SR * duration) + SR)
    beat = 60.0 / bpm
    step_dur = beat / 2

    t = 0.0
    i = 0
    while t < duration:
        semitone = ARPEGGIO_STEPS[i % len(ARPEGGIO_STEPS)]
        freq = _note_freq(root * 2, semitone)
        note = tone(freq, step_dur * 0.92, shape="triangle", vol=vol, decay=True)
        mix_at(track, note, t)
        i += 1
        t += step_dur

    t = 0.0
    bar = beat * 4
    j = 0
    while t < duration:
        bass_freq = root if j % 2 == 0 else _note_freq(root, 7)
        note = tone(bass_freq, bar * 0.9, shape="sine", vol=vol * 0.8, decay=True)
        mix_at(track, note, t)
        j += 1
        t += bar

    return track[: int(SR * duration)]


def build_soundtrack(total_duration, walk_end, run_end, chase_end):
    track = np.zeros(int(SR * total_duration) + SR)

    # continuous original music bed under the whole video
    bed = music_bed(total_duration)
    mix_at(track, bed, 0.0)

    # walking
    mix_at(track, sfx_twinkle(0.2), 0.1)
    mix_at(track, sfx_bark(0.12), max(0.3, walk_end - 0.6))

    # running -- energetic whoosh as the pace picks up
    mix_at(track, sfx_whoosh(0.22), walk_end + 0.05)
    mix_at(track, sfx_meow(0.1) if False else sfx_bark(0.1), (walk_end + run_end) / 2)

    # slow-mo highlight -- gentle purr under the held moment
    mix_at(track, sfx_purr(0.09, dur=max(0.5, chase_end - run_end)), run_end + 0.1)

    # end card
    mix_at(track, sfx_outro_jingle(0.24), chase_end + 0.3)

    track = track[: int(SR * total_duration)]
    peak = np.max(np.abs(track)) or 1.0
    track = track / peak * 0.85
    return track


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/realfootage"
    total_duration = float(sys.argv[2]) if len(sys.argv) > 2 else 13.4
    walk_end = float(sys.argv[3]) if len(sys.argv) > 3 else 1.9
    run_end = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
    chase_end = float(sys.argv[5]) if len(sys.argv) > 5 else 10.3
    os.makedirs(out_dir, exist_ok=True)
    track = build_soundtrack(total_duration, walk_end, run_end, chase_end)
    pcm = (track * 32767).astype(np.int16)
    out_path = os.path.join(out_dir, "soundtrack_realfootage.wav")
    wavfile.write(out_path, SR, pcm)
    print(f"wrote {out_path} ({len(track) / SR:.2f}s)")


if __name__ == "__main__":
    main()
