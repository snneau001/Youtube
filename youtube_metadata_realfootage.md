# YouTube Upload Package — "Best Friends on a Walk" (real footage)

File: `out/best_friends_on_a_walk.mp4` (1080x1920, 30fps, ~10.9s, H.264/AAC — vertical Short)
Source clip: `footage/clip01_three_dogs_field.mp4` (user-provided/licensed
stock footage — not committed to git; keep a local copy to rebuild)

Edit structure: normal-speed open with branded title overlay (4.9s) →
2x slow-motion punch-in replay of the highlight (5.0s) → branded end
card (3.5s), scored with an original synthesized soundtrack.

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
