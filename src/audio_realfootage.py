#!/usr/bin/env python3
"""Synthesizes an upbeat, energetic soundtrack for the real-footage
"Best Friends" edit: a driving kick/shaker rhythm, punchy bass, and a
catchy two-phrase lead melody -- all procedurally generated (no
sampled/licensed audio), tuned brighter and more percussion-driven than
the earlier chiptune-arpeggio bed.

Usage: python3 audio_realfootage.py <output_dir> <total_duration> <segB_start> <segC_start> <segD_start>
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

from audio import SR, mix_at, tone, noise_burst

# A-major-ish scale degrees (semitones from root) for the lead melody.
PHRASE_1 = [0, 3, 5, 7, 5, 3]
PHRASE_2 = [7, 10, 12, 10, 7, 5]


def _freq(root, semitones):
    return root * (2 ** (semitones / 12))


def _kick(vol=0.3):
    return tone(90, 0.12, shape="sine", vol=vol, decay=True)


def _shaker(vol=0.09):
    return noise_burst(0.05, vol=vol, lowpass=6000)


def _bass_note(freq, dur, vol=0.16):
    return tone(freq, dur, shape="triangle", vol=vol, decay=True)


def _lead_note(freq, dur, vol=0.15):
    return tone(freq, dur, shape="triangle", vol=vol, vibrato=0.01, decay=True)


def rhythm_bed(duration, root=196.0, bpm=124, energy_start=0.0):
    """Kick+shaker+bass groove. `energy_start` -- time (s) at which the
    shaker layer joins, so the track can build over the edit."""
    track = np.zeros(int(SR * duration) + SR)
    beat = 60.0 / bpm

    t = 0.0
    beat_i = 0
    while t < duration:
        mix_at(track, _kick(0.26), t)
        if t >= energy_start:
            mix_at(track, _shaker(0.09), t + beat / 2)
        beat_i += 1
        t += beat

    bar = beat * 4
    t = 0.0
    j = 0
    bass_pattern = [0, 0, 7, 5]
    while t < duration:
        freq = _freq(root, bass_pattern[j % len(bass_pattern)])
        mix_at(track, _bass_note(freq, bar * 0.85, vol=0.17), t)
        j += 1
        t += bar

    return track[: int(SR * duration)]


def lead_melody(duration, root=392.0, bpm=124, start=0.0):
    track = np.zeros(int(SR * duration) + SR)
    beat = 60.0 / bpm
    note_dur = beat / 2
    t = start
    i = 0
    phrases = PHRASE_1 + PHRASE_2
    while t < duration:
        semitone = phrases[i % len(phrases)]
        freq = _freq(root, semitone)
        mix_at(track, _lead_note(freq, note_dur * 0.9, vol=0.14), t)
        i += 1
        t += note_dur
    return track[: int(SR * duration)]


def build_soundtrack(total_duration, segB_start, segC_start, segD_start):
    track = np.zeros(int(SR * total_duration) + SR)

    mix_at(track, rhythm_bed(total_duration, energy_start=segB_start), 0.0)
    mix_at(track, lead_melody(segD_start, start=0.3), 0.0)

    # a little swell into the energetic segment, then ease for the slow-mo
    # highlight by simply letting the rhythm carry (lead melody stops at
    # segD_start so the highlight breathes under bass+kick only)

    track = track[: int(SR * total_duration)]
    peak = np.max(np.abs(track)) or 1.0
    track = track / peak * 0.88
    return track


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/realfootage"
    total_duration = float(sys.argv[2]) if len(sys.argv) > 2 else 12.0
    segB_start = float(sys.argv[3]) if len(sys.argv) > 3 else 2.5
    segC_start = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
    segD_start = float(sys.argv[5]) if len(sys.argv) > 5 else 9.5
    os.makedirs(out_dir, exist_ok=True)
    track = build_soundtrack(total_duration, segB_start, segC_start, segD_start)
    pcm = (track * 32767).astype(np.int16)
    out_path = os.path.join(out_dir, "soundtrack_realfootage.wav")
    wavfile.write(out_path, SR, pcm)
    print(f"wrote {out_path} ({len(track) / SR:.2f}s)")


if __name__ == "__main__":
    main()
