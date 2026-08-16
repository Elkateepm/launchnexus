#!/usr/bin/env python3
"""Resize and re-encode screenshots in assets/work/ for the web.

Usage:  python3 tools/optimise-shots.py
"""
import os, sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow needed:  pip install pillow")

MAX_WIDTH = 1600
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "work")

for name in sorted(os.listdir(ROOT)):
    if not name.lower().endswith((".png", ".jpg", ".jpeg")):
        continue
    path = os.path.join(ROOT, name)
    before = os.path.getsize(path)
    im = Image.open(path)

    if im.width > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)

    # Drop any EXIF/metadata the capture tool attached
    clean = Image.new(im.mode, im.size)
    clean.putdata(list(im.getdata()))

    if name.lower().endswith(".png"):
        clean.convert("RGB").quantize(colors=256, method=Image.FASTOCTREE).save(path, optimize=True)
    else:
        clean.convert("RGB").save(path, quality=86, optimize=True, progressive=True)

    after = os.path.getsize(path)
    print("%-40s %6d KB -> %5d KB" % (name, before // 1024, after // 1024))
