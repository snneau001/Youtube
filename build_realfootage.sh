#!/usr/bin/env bash
# Builds "Best Friends on a Walk" from real uploaded footage:
# normal-speed open + slow-mo highlight replay + branded end card,
# with a synthesized soundtrack and title/subscribe overlays.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$ROOT_DIR/src"
BUILD_DIR="$ROOT_DIR/build/realfootage"
OUT_DIR="$ROOT_DIR/out"
FOOTAGE="$ROOT_DIR/footage/clip01_three_dogs_field.mp4"
FONT="/mnt/skills/examples/canvas-design/canvas-fonts/BigShoulders-Bold.ttf"

mkdir -p "$BUILD_DIR" "$OUT_DIR"
cd "$SRC_DIR"

NORMAL_IN=0.1
NORMAL_OUT=5.0
NORMAL_DUR=$(echo "$NORMAL_OUT - $NORMAL_IN" | bc)

HILITE_IN=1.5
HILITE_OUT=4.0
SLOWMO_DUR=$(echo "($HILITE_OUT - $HILITE_IN) * 2" | bc)

ENDCARD_DUR=3.5

echo "==> Segment A (normal speed, ${NORMAL_DUR}s) with title overlay..."
ffmpeg -y -loglevel error -i "$FOOTAGE" -ss "$NORMAL_IN" -to "$NORMAL_OUT" \
  -vf "scale=1080:1920,fps=30,\
drawtext=fontfile=${FONT}:text='BEST FRIENDS':fontsize=88:fontcolor=white:bordercolor=black:borderw=7:x=(w-text_w)/2:y=160:alpha='if(lt(t\,0.25)\,t/0.25\,if(lt(t\,2.6)\,1\,if(lt(t\,2.9)\,(2.9-t)/0.3\,0)))',\
drawtext=fontfile=${FONT}:text='ON A WALK':fontsize=52:fontcolor=0x78C8FF:bordercolor=black:borderw=6:x=(w-text_w)/2:y=254:alpha='if(lt(t\,0.25)\,t/0.25\,if(lt(t\,2.6)\,1\,if(lt(t\,2.9)\,(2.9-t)/0.3\,0)))'" \
  -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_a.mp4"

echo "==> Segment B (slow-mo highlight, ${SLOWMO_DUR}s) with punch-in..."
ffmpeg -y -loglevel error -i "$FOOTAGE" -ss "$HILITE_IN" -to "$HILITE_OUT" \
  -vf "scale=1080:1920,crop=972:1728:(1080-972)/2:(1920-1728)/2,scale=1080:1920,setpts=2.0*PTS,fps=30" \
  -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_b.mp4"

echo "==> End card (${ENDCARD_DUR}s)..."
python3 realfootage_cards.py "$BUILD_DIR/end_card.png"
ffmpeg -y -loglevel error -loop 1 -i "$BUILD_DIR/end_card.png" -t "$ENDCARD_DUR" \
  -vf "scale=1080:1920,fps=30" -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_c.mp4"

echo "==> Concatenating segments..."
cat > "$BUILD_DIR/concat_list.txt" <<EOF
file '$BUILD_DIR/seg_a.mp4'
file '$BUILD_DIR/seg_b.mp4'
file '$BUILD_DIR/seg_c.mp4'
EOF
ffmpeg -y -loglevel error -f concat -safe 0 -i "$BUILD_DIR/concat_list.txt" \
  -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p \
  "$BUILD_DIR/video_only.mp4"

TOTAL_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$BUILD_DIR/video_only.mp4")
echo "==> Total duration: ${TOTAL_DUR}s"

echo "==> Synthesizing soundtrack..."
python3 audio_realfootage.py "$BUILD_DIR" "$TOTAL_DUR" "$NORMAL_DUR" "$(echo "$NORMAL_DUR + $SLOWMO_DUR" | bc)"

echo "==> Muxing final video..."
ffmpeg -y -loglevel error -i "$BUILD_DIR/video_only.mp4" -i "$BUILD_DIR/soundtrack_realfootage.wav" \
  -c:v copy -c:a aac -b:a 192k -shortest \
  "$OUT_DIR/best_friends_on_a_walk.mp4"

echo "==> Done: $OUT_DIR/best_friends_on_a_walk.mp4"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT_DIR/best_friends_on_a_walk.mp4"
