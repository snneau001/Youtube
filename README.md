# Dog & Cat: Funny Fights

A short (40s), fully original, procedurally-animated cartoon of a dog and
cat comedic "fight" — built end-to-end in code, ready to upload to
YouTube. No stock footage, no sampled audio: every frame is drawn with
Pillow and every sound is synthesized with numpy.

- **Final video:** `out/dog_cat_funny_fights.mp4` (1280x720, 24fps, H.264/AAC)
- **Thumbnail:** `assets/thumbnail.png`
- **Storyboard / script:** `storyboard.md`
- **YouTube title/description/tags:** `youtube_metadata.md`

## Rebuild from source

```bash
./build.sh
```

This renders all 960 animation frames (`src/render_frames.py`),
synthesizes the sound effects and jingles (`src/audio.py`), generates
the thumbnail (`src/thumbnail.py`), and assembles the final MP4 with
ffmpeg. Requires `ffmpeg` and the Python packages `pillow`, `numpy`,
`scipy`.

## Project layout

```
storyboard.md          scene-by-scene script and timing
src/anim_common.py      shared constants, easing helpers, drawing primitives
src/characters.py       procedural Rex (dog) / Whiskers (cat) character rigs
src/render_frames.py    scene timeline -> PNG frame sequence
src/audio.py            synthesized SFX + jingle -> soundtrack.wav
src/thumbnail.py        generates the YouTube thumbnail
build.sh                orchestrates the full render -> video pipeline
out/                    final rendered MP4
assets/                 thumbnail
```

## Editing the video

Everything is parametric, so changes are made in code rather than a
timeline editor:
- Adjust pacing/scenes: edit the timeline constants and per-scene blocks
  in `src/render_frames.py` (`T_TITLE`, `T_STANDOFF`, `T_DASH`, etc).
- Adjust character look: edit `src/characters.py`.
- Adjust sound: edit `src/audio.py`.
- Re-run `./build.sh` after any change.
