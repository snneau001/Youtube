# YouTube Upload Package — "Best Friends on a Walk" (real footage)

File: `out/best_friends_on_a_walk.mp4` (1080x1920, 30fps, ~9.3s, H.264/AAC — vertical Short)
Source clip: `footage/clip01_three_dogs_field.mp4` (user-provided/licensed
stock footage — not committed to git; keep a local copy to rebuild)

Edit structure: normal-speed establishing shot with a single clean
"Best Friends" title (soft-shadow caption, not a comic outline) →
mildly sped-up (1.25x), tighter-framed pass for energy → a genuinely
smooth, motion-interpolated slow-motion highlight (ffmpeg `minterpolate`,
not just frame-holding) of the most dynamic moment → branded end card
composited over a blurred frame from the footage. All four segments
crossfade together. Scored with an upbeat, percussion-driven original
soundtrack (kick/shaker rhythm + bass + lead melody, procedurally
synthesized, not licensed).

No "running" or "chasing" claims in the on-screen text — the source
clip shows the dogs moving together, not one pursuing another. The
speed/slow-mo variety is presented as stylistic editing, not a claim
about what the dogs are doing. For a video that actually shows chasing,
a clip depicting real pursuit is needed.

Revision notes: an earlier cut used a horizontal-flip on the energetic
segment for visual variety, but that broke the crossfade into a
kaleidoscope/ghosting artifact (flipped content blended against normal
orientation). Fixed by using a tighter crop for variety instead of a
flip, which keeps spatial continuity across the fades.

## Title options
1. Best Friends on a Walk 🐾 #Shorts
2. Three Best Friends, One Walk 🐶🐾 #Shorts
3. Pack Walk with My Best Friends 🐾 #Shorts

Recommended: **"Best Friends on a Walk 🐾 #Shorts"** — matches the
on-screen title card and keeps the same "Best Friends" branding as the
animated videos for channel consistency.

## Description
```
Three best friends out for an evening walk through the field. 🐾

🐾 Subscribe for more!

#Shorts #DogsOfYoutube #BestFriends #DogWalk #CuteDogs
```

## Tags
dogs on a walk, best friends dogs, white dog, dog pack walk, cute dogs
shorts, dogs in a field, great pyrenees, dog friendship, wholesome
animals, countryside dogs

## Category
Pets & Animals

## Notes
- This video uses real licensed footage (not the procedurally animated
  style of the other videos in this repo) — confirm the specific clip's
  license terms permit the intended use (monetization, redistribution)
  before publishing.
- The raw source clip lives in `footage/` locally and is git-ignored —
  keep your own backup of it if you want to rebuild or extend this edit.
- Rebuild anytime with `./build_realfootage.sh` (regenerates the title/
  end-card overlay and soundtrack; trim points are set via variables at
  the top of the script if you want to pick a different highlight range).
