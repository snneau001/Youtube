#!/usr/bin/env python3
"""Generates the vertical (1080x1920) YouTube Shorts thumbnail for
"Dog & Cat: Best Friends" from a warm frame of the animation.

Usage: python3 thumbnail_shorts.py <output_path>
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

from anim_common import SHORT_WIDTH, SHORT_HEIGHT, font, text_center, TITLE_FONT_PATH, INK
from render_frames_shorts import get_frame


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "assets/thumbnail_shorts.png"
    img = get_frame(13.5).convert("RGB")  # happy bowl-sharing moment

    vignette = Image.new("L", (SHORT_WIDTH, SHORT_HEIGHT), 0)
    vd = ImageDraw.Draw(vignette)
    vd.rectangle([0, 0, SHORT_WIDTH, 220], fill=110)
    vignette = vignette.filter(ImageFilter.GaussianBlur(50))
    dark = Image.new("RGB", (SHORT_WIDTH, SHORT_HEIGHT), (0, 0, 0))
    img = Image.composite(dark, img, vignette)

    draw = ImageDraw.Draw(img, "RGBA")
    big = font(TITLE_FONT_PATH, 118)
    text_center(draw, SHORT_WIDTH / 2, 120, "BEST FRIENDS!", big, fill=(255, 255, 255),
                stroke_fill=INK, stroke_width=11)

    img.save(out_path)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
