#!/usr/bin/env bash
# Builds "Best Friends" from real uploaded footage: a walking segment at
# normal speed, a sped-up running segment, a slow-motion "playing
# together" highlight (the closest thing to chasing in this clip), and
# a branded end card -- scored with an original continuous music bed.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$ROOT_DIR/src"
BUILD_DIR="$ROOT_DIR/build/realfootage"
OUT_DIR="$ROOT_DIR/out"
FOOTAGE="$ROOT_DIR/footage/clip01_three_dogs_field.mp4"
FONT="/mnt/skills/examples/canvas-design/canvas-fonts/BigShoulders-Bold.ttf"

mkdir -p "$BUILD_DIR" "$OUT_DIR"
cd "$SRC_DIR"

# --- source trim points (seconds into the 5.17s source clip) ----------
WALK_IN=0.1; WALK_OUT=1.8
RUN_IN=1.8;  RUN_OUT=5.0;  RUN_SPEED=1.35   # playback speed multiplier
CHASE_IN=1.5; CHASE_OUT=4.0; CHASE_SLOW=2.2  # slow-mo factor

WALK_DUR=$(echo "$WALK_OUT - $WALK_IN" | bc)
RUN_DUR=$(echo "($RUN_OUT - $RUN_IN) / $RUN_SPEED" | bc -l)
CHASE_DUR=$(echo "($CHASE_OUT - $CHASE_IN) * $CHASE_SLOW" | bc -l)
ENDCARD_DUR=3.0

echo "==> Segment A: WALKING (${WALK_DUR}s, normal speed)..."
ffmpeg -y -loglevel error -i "$FOOTAGE" -ss "$WALK_IN" -to "$WALK_OUT" \
  -vf "scale=1080:1920,fps=30,\
drawtext=fontfile=${FONT}:text='BEST FRIENDS':fontsize=88:fontcolor=white:bordercolor=black:borderw=7:x=(w-text_w)/2:y=160:alpha='if(lt(t\,0.2)\,t/0.2\,1)',\
drawtext=fontfile=${FONT}:text='WALKING...':fontsize=52:fontcolor=0x78C8FF:bordercolor=black:borderw=6:x=(w-text_w)/2:y=254:alpha='if(lt(t\,0.2)\,t/0.2\,1)'" \
  -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_walk.mp4"

echo "==> Segment B: RUNNING (${RUN_DUR}s, ${RUN_SPEED}x speed)..."
ffmpeg -y -loglevel error -i "$FOOTAGE" -ss "$RUN_IN" -to "$RUN_OUT" \
  -vf "scale=1080:1920,setpts=PTS/${RUN_SPEED},fps=30,\
drawtext=fontfile=${FONT}:text='...THEN RUNNING!':fontsize=64:fontcolor=white:bordercolor=black:borderw=7:x=(w-text_w)/2:y=180:alpha='if(lt(t\,0.2)\,t/0.2\,if(lt(t\,$(echo "$RUN_DUR-0.3"|bc)\)\,1\,(($RUN_DUR-t)/0.3)))'" \
  -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_run.mp4"

echo "==> Segment C: PLAYING TOGETHER, slow-mo highlight (${CHASE_DUR}s, punch-in)..."
ffmpeg -y -loglevel error -i "$FOOTAGE" -ss "$CHASE_IN" -to "$CHASE_OUT" \
  -vf "scale=1080:1920,crop=940:1672:(1080-940)/2:(1920-1672)/2,scale=1080:1920,setpts=${CHASE_SLOW}*PTS,fps=30,\
drawtext=fontfile=${FONT}:text='BEST OF FRIENDS':fontsize=64:fontcolor=0x78C8FF:bordercolor=black:borderw=7:x=(w-text_w)/2:y=1650:alpha='if(lt(t\,0.4)\,t/0.4\,if(lt(t\,$(echo "$CHASE_DUR-0.5"|bc)\)\,1\,(($CHASE_DUR-t)/0.5)))'" \
  -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_chase.mp4"

echo "==> End card (${ENDCARD_DUR}s)..."
python3 realfootage_cards.py "$BUILD_DIR/end_card.png"
ffmpeg -y -loglevel error -loop 1 -i "$BUILD_DIR/end_card.png" -t "$ENDCARD_DUR" \
  -vf "scale=1080:1920,fps=30" -r 30 -pix_fmt yuv420p -c:v libx264 -crf 16 -preset medium -an \
  "$BUILD_DIR/seg_end.mp4"

echo "==> Concatenating segments..."
cat > "$BUILD_DIR/concat_list.txt" <<EOF
file '$BUILD_DIR/seg_walk.mp4'
file '$BUILD_DIR/seg_run.mp4'
file '$BUILD_DIR/seg_chase.mp4'
file '$BUILD_DIR/seg_end.mp4'
EOF
ffmpeg -y -loglevel error -f concat -safe 0 -i "$BUILD_DIR/concat_list.txt" \
  -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p \
  "$BUILD_DIR/video_only.mp4"

TOTAL_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$BUILD_DIR/video_only.mp4")
WALK_END="$WALK_DUR"
RUN_END=$(echo "$WALK_DUR + $RUN_DUR" | bc -l)
CHASE_END=$(echo "$RUN_END + $CHASE_DUR" | bc -l)
echo "==> Total duration: ${TOTAL_DUR}s (walk_end=${WALK_END} run_end=${RUN_END} chase_end=${CHASE_END})"

echo "==> Synthesizing soundtrack..."
python3 audio_realfootage.py "$BUILD_DIR" "$TOTAL_DUR" "$WALK_END" "$RUN_END" "$CHASE_END"

echo "==> Muxing final video..."
ffmpeg -y -loglevel error -i "$BUILD_DIR/video_only.mp4" -i "$BUILD_DIR/soundtrack_realfootage.wav" \
  -c:v copy -c:a aac -b:a 192k -shortest \
  "$OUT_DIR/best_friends_on_a_walk.mp4"

echo "==> Done: $OUT_DIR/best_friends_on_a_walk.mp4"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT_DIR/best_friends_on_a_walk.mp4"
