#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove o fundo cinza chapado da logo oficial (flood fill pelas bordas),
gerando versao transparente do logo completo e so-cabeca."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SRC = "C:/abdallatech/91-MARCA/export/abdalla-tech-2a-gpu.png"
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = _HERE

im = Image.open(SRC).convert("RGB")
W, H = im.size

# flood fill background -> sentinel magenta
work = im.copy()
seeds = []
for fx in (0.005, 0.5, 0.995):
    for fy in (0.005, 0.5, 0.995):
        if not (fx == 0.5 and fy == 0.5):
            seeds.append((int(fx * (W - 1)), int(fy * (H - 1))))
SENT = (255, 0, 255)
for s in seeds:
    ImageDraw.floodfill(work, s, SENT, thresh=26)

arr = np.asarray(work)
bgmask = np.all(arr == np.array(SENT), axis=-1)   # True where background

# build alpha
alpha = np.where(bgmask, 0, 255).astype(np.uint8)
am = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(1.2))  # soft edge
rgba = im.convert("RGBA")
rgba.putalpha(am)
rgba.save(f"{OUT}/logo_robot.png")

# head-only crop: alpha in top 58% rows
a = np.asarray(am)
top = a[: int(H * 0.58), :]
ys, xs = np.where(top > 20)
pad = 24
x0, x1 = max(0, xs.min() - pad), min(W, xs.max() + pad)
y0, y1 = max(0, ys.min() - pad), min(int(H * 0.58), ys.max() + pad)
head = rgba.crop((x0, y0, x1, y1))
head.save(f"{OUT}/logo_head.png")

# preview both on green bg
def prev(img, name, pad=60):
    bg = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (12, 22, 17, 255))
    bg.alpha_composite(img, (pad, pad))
    bg.convert("RGB").save(f"{OUT}/{name}")

prev(Image.open(f"{OUT}/logo_robot.png"), "prev_robot.png")
prev(head, "prev_head.png")
print("bg removed. transparent%%=%.1f" % (bgmask.mean() * 100),
      "robot=", Image.open(f"{OUT}/logo_robot.png").size, "head=", head.size)
