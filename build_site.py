#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnostic Neon — Abdalla Tech site assets (local, free, PIL).

Produces on-brand placeholder imagery for the site while AI photoreal generation
is paywalled: a wide hero, three testimonial avatar tiles (stylized, non-photoreal),
and a diagnostic section band. Palette: near-black navy, one cyan signal-glow,
one warm amber accent, clinical off-white. Output -> ./site-assets/
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
CF = os.environ.get("FONTS_DIR", os.path.join(_HERE, "fonts"))
def F(n, s): return ImageFont.truetype(f"{CF}/{n}", s)
OUT = os.path.join(_HERE, "site-assets")

# ---------- Diagnostic Neon palette ----------
NAVY0 = (11, 17, 28)      # top of bg gradient
NAVY1 = (5, 8, 15)        # bottom
PANEL = (13, 20, 32)
GRID  = (23, 33, 49)
CYAN  = (74, 210, 233)    # single signal-glow
AMBER = (242, 170, 70)    # warm accent
OFFW  = (224, 233, 243)   # clinical off-white
MUTE  = (104, 124, 148)   # quiet labels
DIMC  = (32, 96, 110)

# ---------- generic helpers (take + return img) ----------
def bg(W, H):
    a = np.array(NAVY0, float); b = np.array(NAVY1, float)
    g = a[None, :] + (b - a)[None, :] * np.linspace(0, 1, H)[:, None]
    return Image.fromarray(np.repeat(g[:, None, :], W, axis=1).astype(np.uint8), "RGB")

def screen_glow(img, drawfn, passes=(20, 11, 6), core=True):
    W, H = img.size
    layer = Image.new("RGB", (W, H), (0, 0, 0))
    drawfn(ImageDraw.Draw(layer))
    for gg in passes:
        img = ImageChops.screen(img, layer.filter(ImageFilter.GaussianBlur(gg)))
    if core:
        img = ImageChops.screen(img, layer)
    return img

def clinical_light(img, cx, cy, r, inten=70, col=(180, 210, 225)):
    W, H = img.size
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([cx-r, cy-r, cx+r, cy+r], fill=inten)
    m = m.filter(ImageFilter.GaussianBlur(r*0.55))
    return ImageChops.screen(img, Image.composite(Image.new("RGB", (W, H), col),
                                                  Image.new("RGB", (W, H), (0, 0, 0)), m))

def dot_grid(img, step=36, col=GRID, x0=0, y0=0, x1=None, y1=None):
    W, H = img.size
    x1 = W if x1 is None else x1; y1 = H if y1 is None else y1
    d = ImageDraw.Draw(img)
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            d.point((x, y), fill=col)
    return img

def cham(box, c):
    x0, y0, x1, y1 = box
    return [(x0+c, y0), (x1, y0), (x1, y1-c), (x1-c, y1), (x0, y1), (x0, y0+c)]

def tracked(d, x, y, text, font, fill, tr=0):
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tr
def twidth(d, text, font, tr=0):
    return sum(d.textlength(c, font=font) + tr for c in text) - tr

def reg_ticks(img, box, col=DIMC, n=8, length=9, mono=None, labels=False):
    """Registration ticks along the top + left edges of box (oscilloscope feel)."""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    for i in range(n+1):
        x = x0 + (x1-x0)*i/n
        L = length*(1.8 if i % 4 == 0 else 1)
        d.line([(x, y0), (x, y0+L)], fill=col, width=1)
        if labels and mono and i % 4 == 0:
            tracked(d, x+3, y0+2, f"{i*10:02d}", mono, col, 1)
    for i in range(n+1):
        y = y0 + (y1-y0)*i/n
        L = length*(1.8 if i % 4 == 0 else 1)
        d.line([(x0, y), (x0+L, y)], fill=col, width=1)
    return img

def corner_brackets(img, box, col=CYAN, L=34, w=3):
    x0, y0, x1, y1 = box
    def draw(dl):
        for (cx, cy, fx, fy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
            dl.line([(cx, cy), (cx+fx*L, cy)], fill=col, width=w)
            dl.line([(cx, cy), (cx, cy+fy*L)], fill=col, width=w)
    return screen_glow(img, draw, passes=(9, 4))

def waveform(img, x0, x1, ymid, amp, col=CYAN, step=4, seed=1, glow=True):
    rng = np.random.default_rng(seed)
    pts = []
    for x in range(x0, x1, step):
        t = (x - x0) / (x1 - x0)
        y = ymid + amp*(0.6*math.sin(t*22 + seed) + 0.3*math.sin(t*61 + seed*2)
                        + 0.1*rng.standard_normal())
        pts.append((x, y))
    def draw(dl): dl.line(pts, fill=col, width=3, joint="curve")
    return screen_glow(img, draw, passes=(14, 7)) if glow else draw(ImageDraw.Draw(img)) or img

# ---------- GPU specimen (scalable) ----------
def gpu(img, box, accent_conn=AMBER, outline=CYAN):
    x0, y0, x1, y1 = box
    w, h = x1-x0, y1-y0
    sh = cham([x0, y0, x1, y1], int(h*0.11))
    ImageDraw.Draw(img).polygon(sh, fill=(18, 27, 42))
    img = screen_glow(img, lambda dl: dl.line(sh+[sh[0]], fill=outline, width=3), passes=(15, 8))
    # PCIe connector (amber)
    cw = int(w*0.42); cx0 = x0 + int(w*0.10); cyv = y1 - 4
    conn = cham([cx0, cyv-int(h*0.10), cx0+cw, cyv], 6)
    ImageDraw.Draw(img).polygon(conn, fill=(38, 28, 10))
    img = screen_glow(img, lambda dl: dl.line(conn+[conn[0]], fill=accent_conn, width=2), passes=(9, 4))
    d = ImageDraw.Draw(img)
    for tx in range(cx0+8, cx0+cw-6, max(10, int(w*0.014))):
        d.line([(tx, cyv-int(h*0.09)), (tx, cyv-4)], fill=(120, 92, 30), width=3)
    # two fans
    r = int(h*0.30); cyf = y0 + int(h*0.42)
    for cxf in (x0 + int(w*0.30), x0 + int(w*0.70)):
        img = screen_glow(img, lambda dl, cxf=cxf: dl.ellipse(
            [cxf-r, cyf-r, cxf+r, cyf+r], outline=outline, width=3), passes=(12, 6))
        dd = ImageDraw.Draw(img)
        for k in range(9):
            a = math.radians(k*40); a2 = a+0.7
            dd.line([(cxf+(r-int(r*0.19))*math.cos(a), cyf+(r-int(r*0.19))*math.sin(a)),
                     (cxf+int(r*0.28)*math.cos(a2), cyf+int(r*0.28)*math.sin(a2))],
                    fill=(0, 108, 126), width=5)
        img = screen_glow(img, lambda dl, cxf=cxf: dl.ellipse(
            [cxf-int(r*0.2), cyf-int(r*0.2), cxf+int(r*0.2), cyf+int(r*0.2)],
            outline=accent_conn, width=3), passes=(7, 4))
        ImageDraw.Draw(img).ellipse([cxf-5, cyf-5, cxf+5, cyf+5], fill=accent_conn)
    ImageDraw.Draw(img).line([((x0+x1)//2, y0+int(h*0.07)), ((x0+x1)//2, y1-int(h*0.14))],
                             fill=(38, 52, 72), width=2)
    return img

def scanlines(img, k=0.9):
    arr = np.asarray(img).astype(np.float32)
    arr[0::3, :, :] *= k
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")

# ============================================================ HERO
def build_hero():
    W, H = 1600, 900
    img = bg(W, H)
    img = dot_grid(img, 40)
    img = clinical_light(img, 1080, 430, 460, inten=64)
    M = 54
    img = reg_ticks(img, [M, M, W-M, H-M], n=16, length=8, mono=F("IBMPlexMono-Regular.ttf", 13), labels=True)
    img = corner_brackets(img, [M, M, W-M, H-M])
    # specimen
    img = gpu(img, [812, 250, 1360, 560])
    d = ImageDraw.Draw(img)
    tracked(d, 826, 214, "SPECIMEN 01 // GPU", F("IBMPlexMono-Regular.ttf", 16), MUTE, 2)
    # reticle anchored to the specimen's top-right corner
    rx0, ry0 = 1328, 208
    img = screen_glow(img, lambda dl: (dl.ellipse([rx0, ry0, rx0+30, ry0+30], outline=AMBER, width=2),
                                       dl.line([(rx0+15, ry0-6), (rx0+15, ry0+36)], fill=AMBER, width=1),
                                       dl.line([(rx0-6, ry0+15), (rx0+36, ry0+15)], fill=AMBER, width=1)),
                      passes=(7, 4))
    d = ImageDraw.Draw(img)
    stf = F("IBMPlexMono-Bold.ttf", 16); stw = twidth(d, "STATUS: OK", stf, 2)
    tracked(d, rx0 - 16 - stw, 214, "STATUS: OK", stf, CYAN, 2)
    # brand block (upper-left, negative space above)
    d = ImageDraw.Draw(img)
    tracked(d, M+18, 150, "ABDALLA TECH", F("BigShoulders-Bold.ttf", 58), OFFW, 2)
    tracked(d, M+22, 214, "ASSISTÊNCIA TÉCNICA GAMER", F("IBMPlexMono-Bold.ttf", 18), CYAN, 4)
    # headline (lower-left, condensed)
    tracked(d, M+16, 560, "REPARO DE", F("BigShoulders-Bold.ttf", 132), OFFW, 1)
    tracked(d, M+16, 676, "PLACAS DE VÍDEO", F("BigShoulders-Bold.ttf", 132), AMBER, 1)
    # support chips
    sub = F("IBMPlexMono-Bold.ttf", 20)
    tracked(d, M+20, 820, "[ NÃO LIGA ]   [ ARTEFATOS ]   [ SUPERAQUECE ]   [ TRAVA ]", sub, MUTE, 1)
    # thin baseline waveform across the foot
    img = waveform(img, M, W-M, 792, 9, col=DIMC, seed=3, glow=False)
    img = scanlines(img, 0.9)
    p = f"{OUT}/hero.png"; img.save(p); print("saved", p)

# ============================================================ AVATAR TILE
def build_avatar(name, initials, handle, accent, seed, fname):
    W = H = 520
    img = bg(W, H)
    img = dot_grid(img, 30)
    img = clinical_light(img, W//2, 210, 250, inten=52)
    M = 26
    img = reg_ticks(img, [M, M, W-M, H-M], n=8, length=7)
    img = corner_brackets(img, [M, M, W-M, H-M], L=26, w=2)
    # scope ring
    cx, cy, r = W//2, 208, 118
    img = screen_glow(img, lambda dl: dl.ellipse([cx-r, cy-r, cx+r, cy+r], outline=CYAN, width=3), passes=(14, 7))
    img = screen_glow(img, lambda dl: dl.ellipse([cx-r-12, cy-r-12, cx+r+12, cy+r+12], outline=DIMC, width=1), passes=(5,))
    d = ImageDraw.Draw(img)
    # schematic bust silhouette inside the ring (stylized, non-photoreal avatar)
    hd = 46
    d.ellipse([cx-hd, cy-58, cx+hd, cy-58+2*hd], fill=(18, 27, 42), outline=accent, width=3)      # head
    sh = cham([cx-92, cy+30, cx+92, cy+150], 30)
    ImageDraw.Draw(img).polygon(sh, fill=(16, 24, 38))
    img = screen_glow(img, lambda dl: dl.line(sh+[sh[0]], fill=accent, width=3), passes=(11, 6))
    # clip bust to ring
    ring = Image.new("L", (W, H), 0); ImageDraw.Draw(ring).ellipse([cx-r, cy-r, cx+r, cy+r], fill=255)
    base = bg(W, H); base = dot_grid(base, 30)
    img = Image.composite(img, base, ring.filter(ImageFilter.GaussianBlur(0)).point(lambda p: 255 if p > 40 else 0)) \
        if False else img  # (keep full frame; ring already reads)
    d = ImageDraw.Draw(img)
    # signal dot
    ImageDraw.Draw(img).ellipse([cx+hd-6, cy-52, cx+hd+8, cy-38], fill=accent)
    # monogram baseline mono code on ring
    tracked(d, cx-r+6, cy-r-2, "ID", F("IBMPlexMono-Regular.ttf", 13), MUTE, 1)
    # name + handle
    nm = F("BigShoulders-Bold.ttf", 46)
    nw = twidth(d, name, nm, 1); tracked(d, (W-nw)//2, 356, name, nm, OFFW, 1)
    hf = F("IBMPlexMono-Bold.ttf", 17)
    hw = twidth(d, handle, hf, 1); tracked(d, (W-hw)//2, 408, handle, hf, CYAN, 1)
    # amber 5-dot rating
    dotr = 7; gap = 30; total = 5*gap - (gap-2*dotr); sx = (W-total)//2
    for i in range(5):
        d.ellipse([sx+i*gap, 448, sx+i*gap+2*dotr, 448+2*dotr], fill=AMBER)
    # initials watermark faint behind ring top-left? keep clean.
    img = scanlines(img, 0.92)
    p = f"{OUT}/{fname}"; img.save(p); print("saved", p)

# ============================================================ SECTION BAND
def build_band():
    W, H = 1600, 420
    img = bg(W, H)
    img = dot_grid(img, 40)
    img = clinical_light(img, 800, 210, 520, inten=40)
    M = 46
    img = reg_ticks(img, [M, M, W-M, H-M], n=16, length=8, mono=F("IBMPlexMono-Regular.ttf", 13), labels=True)
    img = corner_brackets(img, [M, M, W-M, H-M])
    # big oscilloscope trace
    img = waveform(img, M+30, W-M-30, 200, 66, col=CYAN, seed=7)
    d = ImageDraw.Draw(img)
    tracked(d, M+30, 78, "DIAGNÓSTICO PRECISO", F("BigShoulders-Bold.ttf", 74), OFFW, 1)
    tracked(d, M+34, 300, "BANCADA · MICROSSOLDA · TESTE DE CARGA · GARANTIA", F("IBMPlexMono-Bold.ttf", 19), AMBER, 2)
    tracked(d, W-M-190, 78, "0x1F·GPU", F("IBMPlexMono-Regular.ttf", 16), MUTE, 2)
    img = scanlines(img, 0.9)
    p = f"{OUT}/band-diagnostico.png"; img.save(p); print("saved", p)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build_hero()
    build_avatar("LUCAS MENDES", "LM", "@setup_rgb_br", CYAN, 11, "depoimento-1.png")
    build_avatar("RAFA SOUZA",  "RS", "@rafa.plays",   AMBER, 23, "depoimento-2.png")
    build_avatar("JOÃO ALVES",  "JA", "@joao_fps",     CYAN, 37, "depoimento-3.png")
    build_band()
    print("done ->", OUT)
