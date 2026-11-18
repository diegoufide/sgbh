#!/usr/bin/env python3
"""render.py <html> <png> [width] [height] [budget_ms] : screenshot with headless Chrome @2x and auto-trim."""
import sys, subprocess, os
from PIL import Image, ImageChops
html, png = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 1600
h = int(sys.argv[4]) if len(sys.argv) > 4 else 1200
budget = sys.argv[5] if len(sys.argv) > 5 else '4000'
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
tmp = png + '.raw.png'
cmd = [chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
       f'--window-size={w},{h}', f'--virtual-time-budget={budget}', '--run-all-compositor-stages-before-draw',
       f'--screenshot={tmp}', 'file://' + os.path.abspath(html)]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
im = Image.open(tmp).convert('RGB')
bg = Image.new('RGB', im.size, (255, 255, 255))
bbox = ImageChops.difference(im, bg).getbbox()
cut = bool(bbox) and (bbox[2] >= im.width - 2 or bbox[3] >= im.height - 2)
if bbox:
    pad = 24
    bbox = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
    im = im.crop(bbox)
im.save(png, dpi=(192, 192))
os.remove(tmp)
print(png, im.size, 'WARNING: CONTENT MAY BE CUT' if cut else 'ok')
