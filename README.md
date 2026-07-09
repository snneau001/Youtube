# Dog & Cat: Original Animated Videos

Two short, fully original, procedurally-animated videos starring Rex
(dog) and Whiskers (cat) — built end-to-end in code, ready to upload to
YouTube. No stock footage, no sampled audio: every frame is drawn with
Pillow and every sound is synthesized with numpy.

## 1. "Dog & Cat: Funny Fights" (40s)

A comedic squeaky-toy tug-of-war and scuffle brawl — golden Rex vs.
grey tabby Whiskers.

- **Final video:** `out/dog_cat_funny_fights.mp4` (1280x720, 24fps, H.264/AAC)
- **Thumbnail:** `assets/thumbnail.png`
- **Storyboard / script:** `storyboard.md`
- **YouTube title/description/tags:** `youtube_metadata.md`
- **Rebuild:** `./build.sh`

## 2. "Dog & Cat: Best Friends" (32s)

The wholesome companion piece — same characters, recolored white, no
conflict: a happy chase around the yard (with a hedge to hop over),
then heading inside to share a bowl of food together.

- **Final video:** `out/dog_cat_best_friends.mp4` (1280x720, 24fps, H.264/AAC)
- **Thumbnail:** `assets/thumbnail_bff.png`
- **Storyboard / script:** `storyboard_bff.md`
- **YouTube title/description/tags:** `youtube_metadata_bff.md`
- **Rebuild:** `./build_bff.sh`

## 3. "Dog & Cat: Best Friends" — YouTube Short (26.5s, vertical)

A hook-first, vertically-reframed cut of the Best Friends video, built
for the YouTube Shorts feed: action starts at frame 0 (no static title
card), tighter scene pacing, 1080x1920.

- **Final video:** `out/dog_cat_best_friends_short.mp4` (1080x1920, 24fps, H.264/AAC)
- **Thumbnail:** `assets/thumbnail_shorts.png`
- **YouTube title/description/tags:** `youtube_metadata_shorts.md`
- **Rebuild:** `./build_shorts.sh`

## Rebuild from source

```bash
./build.sh          # Funny Fights
./build_bff.sh      # Best Friends (landscape)
./build_shorts.sh   # Best Friends (vertical Short)
```

Each script renders the animation frames, synthesizes the soundtrack,
generates the thumbnail, and assembles the final MP4 with ffmpeg.
Requires `ffmpeg` and the Python packages `pillow`, `numpy`, `scipy`.

## Project layout

```
storyboard.md              Funny Fights scene-by-scene script and timing
storyboard_bff.md           Best Friends scene-by-scene script and timing
src/anim_common.py          shared constants, easing helpers, drawing primitives
                             (living room + yard backgrounds, props, FX)
src/characters.py           procedural Rex (dog) / Whiskers (cat) rigs --
                             color-overridable so both videos share one rig
src/render_frames.py        Funny Fights timeline -> PNG frame sequence
src/render_frames_bff.py    Best Friends (landscape) timeline -> PNG frame sequence
src/render_frames_shorts.py Best Friends (vertical Short) timeline -> PNG frame sequence
src/audio.py                Funny Fights SFX + jingles -> soundtrack.wav
src/audio_bff.py            Best Friends SFX + jingles (reuses audio.py's
                             synth primitives) -> soundtrack_bff.wav
src/audio_shorts.py         Shorts cut SFX (reuses audio.py/audio_bff.py) -> soundtrack_shorts.wav
src/thumbnail.py            Funny Fights thumbnail generator
src/thumbnail_bff.py        Best Friends (landscape) thumbnail generator
src/thumbnail_shorts.py     Best Friends (vertical) thumbnail generator
build.sh / build_bff.sh /   orchestrate each render -> video pipeline
build_shorts.sh
out/                        final rendered MP4s
assets/                     thumbnails
```

## Editing the videos

Everything is parametric, so changes are made in code rather than a
timeline editor:
- Adjust pacing/scenes: edit the timeline constants and per-scene blocks
  in `src/render_frames.py` or `src/render_frames_bff.py` (`T_TITLE`,
  `T_CHASE`, etc).
- Adjust character look: edit `src/characters.py` (shared rig; color
  variants are passed in as keyword overrides, e.g. `DOG_KW`/`CAT_KW`
  in `render_frames_bff.py`).
- Adjust sound: edit `src/audio.py` or `src/audio_bff.py`.
- Re-run the matching `build*.sh` after any change.
