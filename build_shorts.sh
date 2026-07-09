#!/usr/bin/env bash
# Builds the vertical YouTube Short "Dog & Cat: Best Friends (Short)":
# renders the animation frames, synthesizes the soundtrack, assembles
# the final 1080x1920 MP4 with ffmpeg, and generates a Shorts thumbnail.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$ROOT_DIR/src"
BUILD_DIR="$ROOT_DIR/build"
OUT_DIR="$ROOT_DIR/out"
ASSETS_DIR="$ROOT_DIR/assets"

FRAMES_DIR="$BUILD_DIR/frames_shorts"
AUDIO_DIR="$BUILD_DIR/audio_shorts"
FPS=24

mkdir -p "$FRAMES_DIR" "$AUDIO_DIR" "$OUT_DIR" "$ASSETS_DIR"
cd "$SRC_DIR"

echo "==> Rendering animation frames..."
python3 render_frames_shorts.py "$FRAMES_DIR"

echo "==> Synthesizing soundtrack..."
python3 audio_shorts.py "$AUDIO_DIR"

echo "==> Generating thumbnail..."
python3 thumbnail_shorts.py "$ASSETS_DIR/thumbnail_shorts.png"

echo "==> Assembling final MP4..."
ffmpeg -y -loglevel error \
  -framerate "$FPS" -i "$FRAMES_DIR/frame_%05d.png" \
  -i "$AUDIO_DIR/soundtrack_shorts.wav" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium \
  -c:a aac -b:a 192k \
  -shortest \
  "$OUT_DIR/dog_cat_best_friends_short.mp4"

echo "==> Done: $OUT_DIR/dog_cat_best_friends_short.mp4"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUT_DIR/dog_cat_best_friends_short.mp4"
