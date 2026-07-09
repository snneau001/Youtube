#!/usr/bin/env bash
# Builds "Best Friends" from real uploaded footage: a normal-speed
# establishing shot, a mildly sped-up + mirrored energetic pass (for
# visual variety, honestly -- no "running/chasing" claims), and a truly
# smooth (motion-interpolated) slow-motion highlight, crossfaded
# together with a branded end card. Scored with an upbeat original
# soundtrack.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$ROOT_DIR/src"
BUILD_DIR="$ROOT_DIR/build/realfootage"
OUT_DIR="$ROOT_DIR/out"
FOOTAGE="$ROOT_DIR/footage/clip01_three_dogs_field.mp4"
FONT="/mnt/skills/examples/canvas-design/canvas-fonts/BigShoulders-Bold.ttf"

mkdir -p "$BUILD_DIR" "$OUT_DIR"
cd "$SRC_DIR"

# consistent mild punch-in crop applied to every real-footage segment
CROP="crop=1004:1786:38:67,scale=1080:1920"
# tighter punch-in for the "energetic" segment -- a flip was tried here
# for visual variety but it breaks the crossfade (flipped content
# blended against normal orientation ghosts into a kaleidoscope), so
# variety comes from framing instead of mirroring
CROP_TIGHT="crop=918:1632:81:144,scale=1080:1920"

XFD=0.4   # crossfade duration (s)

echo "==> Segment A: establishing shot, normal speed, title fade..."
ffmpeg -y -loglevel error -i "$FOOTAGE" -ss 0.1 -to 3.0 \
  -vf "scale=1080:1920,${CROP},fps=30,\
drawtext=fontfile=${FONT}:text='Best Friends':fontsize=78:fontcolor=white:shadowcolor=black@0.55:shadowx=3:shadowy=3:x=(w-text_w)/2:y=150:alpha='if(lt(t\,0.3)\,t/0.3\,if(lt(t\,1.9)\,1\,if(lt(t\,2.2)\,(2.2-t)/0.3\,0)))'" \
  -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_a.mp4"

echo "==> Segment B: energetic pass (1.25x, tighter framing for variety)..."
ffmpeg -y -loglevel error -i "$FOOTAGE" -ss 2.0 -to 5.0 \
  -vf "scale=1080:1920,${CROP_TIGHT},setpts=PTS/1.25,fps=30" \
  -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_b.mp4"

echo "==> Segment C: true smooth slow-motion highlight (motion-interpolated)..."
ffmpeg -y -loglevel error -i "$FOOTAGE" -ss 1.5 -to 4.0 \
  -vf "scale=1080:1920,${CROP},minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,setpts=2.0*PTS,fps=30" \
  -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_c.mp4"

echo "==> End card (background frame from the highlight)..."
ffmpeg -y -loglevel error -sseof -0.1 -i "$BUILD_DIR/seg_c.mp4" -frames:v 1 "$BUILD_DIR/end_bg.png"
python3 realfootage_cards.py "$BUILD_DIR/end_card.png" "$BUILD_DIR/end_bg.png"
ffmpeg -y -loglevel error -loop 1 -i "$BUILD_DIR/end_card.png" -t 3.0 \
  -vf "scale=1080:1920,fps=30" -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_d.mp4"

dur() { ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$1"; }
DUR_A=$(dur "$BUILD_DIR/seg_a.mp4")
DUR_B=$(dur "$BUILD_DIR/seg_b.mp4")
DUR_C=$(dur "$BUILD_DIR/seg_c.mp4")
DUR_D=$(dur "$BUILD_DIR/seg_d.mp4")

OFF1=$(echo "$DUR_A - $XFD" | bc -l)
DUR_AB=$(echo "$DUR_A + $DUR_B - $XFD" | bc -l)
OFF2=$(echo "$DUR_AB - $XFD" | bc -l)
DUR_ABC=$(echo "$DUR_AB + $DUR_C - $XFD" | bc -l)
OFF3=$(echo "$DUR_ABC - $XFD" | bc -l)

echo "==> Crossfading segments (offsets: $OFF1, $OFF2, $OFF3)..."
ffmpeg -y -loglevel error \
  -i "$BUILD_DIR/seg_a.mp4" -i "$BUILD_DIR/seg_b.mp4" -i "$BUILD_DIR/seg_c.mp4" -i "$BUILD_DIR/seg_d.mp4" \
  -filter_complex "\
[0][1]xfade=transition=fade:duration=${XFD}:offset=${OFF1}[v01];\
[v01][2]xfade=transition=fade:duration=${XFD}:offset=${OFF2}[v012];\
[v012][3]xfade=transition=fade:duration=${XFD}:offset=${OFF3}[vout]" \
  -map "[vout]" -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium \
  "$BUILD_DIR/video_only.mp4"

TOTAL_DUR=$(dur "$BUILD_DIR/video_only.mp4")
echo "==> Total duration: ${TOTAL_DUR}s"

echo "==> Synthesizing soundtrack..."
python3 audio_realfootage.py "$BUILD_DIR" "$TOTAL_DUR" "$OFF1" "$OFF2" "$OFF3"

echo "==> Muxing final video..."
ffmpeg -y -loglevel error -i "$BUILD_DIR/video_only.mp4" -i "$BUILD_DIR/soundtrack_realfootage.wav" \
  -c:v copy -c:a aac -b:a 192k -shortest \
  "$OUT_DIR/best_friends_on_a_walk.mp4"

echo "==> Done: $OUT_DIR/best_friends_on_a_walk.mp4"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT_DIR/best_friends_on_a_walk.mp4"
