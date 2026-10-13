#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnostic Neon — Abdalla Tech GPU repair promo (1080x1080)."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 1080
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
CF = os.environ.get("FONTS_DIR", os.path.join(_HERE, "fonts"))

def F(name, size):
    return ImageFont.truetype(f"{CF}/{name}", size)

# Palette
BG_TOP  = (9, 13, 20)
BG_BOT  = (13, 20, 32)
CYAN    = (34, 224, 255)
CYAN_D  = (20, 110, 140)
AMBER   = (255, 150, 44)
WHITE   = (240, 248, 255)
MUTE    = (120, 140, 165)
GRID    = (23, 32, 46)
PANEL   = (20, 27, 39)
PANEL_L = (32, 43, 60)

# ---------- background gradient ----------
top = np.array(BG_TOP, float); bot = np.array(BG_BOT, float)
grad = (top[None,:] + (bot-top)[None,:]*np.linspace(0,1,S)[:,None])
bg = np.repeat(grad[:,None,:], S, axis=1).astype(np.uint8)
img = Image.fromarray(bg, "RGB")

# ---------- cyan radial glow behind hero ----------
glow = Image.new("L", (S, S), 0)
ImageDraw.Draw(glow).ellipse([200, 170, 880, 600], fill=90)
glow = glow.filter(ImageFilter.GaussianBlur(150))
img = Image.composite(Image.new("RGB",(S,S),CYAN), img, glow.point(lambda p: int(p*0.42)))

d = ImageDraw.Draw(img)

# ---------- faint technical grid ----------
for x in range(0, S+1, 60):
    d.line([(x,0),(x,S)], fill=GRID, width=1)
for y in range(0, S+1, 60):
    d.line([(0,y),(S,y)], fill=GRID, width=1)

M = 84  # margin

# ---------- corner registration ticks ----------
def ticks(cx, cy, fx=1, fy=1):
    L=26
    d.line([(cx,cy),(cx+fx*L,cy)], fill=CYAN, width=3)
    d.line([(cx,cy),(cx,cy+fy*L)], fill=CYAN, width=3)
for (cx,cy,fx,fy) in [(M,M,1,1),(S-M,M,-1,1),(M,S-M,1,-1),(S-M,S-M,-1,-1)]:
    ticks(cx,cy,fx,fy)

def spaced(draw, xy, text, font, fill, tracking=0, anchor_left=True):
    x, y = xy
    if not anchor_left:
        w = sum(draw.textlength(c, font=font)+tracking for c in text) - tracking
        x -= w
    for c in text:
        draw.text((x, y), c, font=font, fill=fill)
        x += draw.textlength(c, font=font) + tracking

def center(draw, y, text, font, fill, tracking=0):
    w = sum(draw.textlength(c, font=font)+tracking for c in text) - tracking
    x = (S - w)/2
    for c in text:
        draw.text((x, y), c, font=font, fill=fill); x += draw.textlength(c,font=font)+tracking
    return w

# ================= HEADER =================
brand = F("Tektur-Medium.ttf", 46)
mono  = F("JetBrainsMono-Bold.ttf", 22)
monos = F("JetBrainsMono-Regular.ttf", 20)

lx, ly = M+4, 128
d.rounded_rectangle([lx, ly, lx+56, ly+56], radius=12, outline=CYAN, width=4)
d.rounded_rectangle([lx+14, ly+14, lx+42, ly+42], radius=5, fill=AMBER)
spaced(d, (lx+76, ly-4), "ABDALLA TECH", brand, WHITE, tracking=2)
spaced(d, (lx+78, ly+40), "ASSISTÊNCIA TÉCNICA GAMER", monos, CYAN, tracking=3)
spaced(d, (S-M, ly+2), "GPU // REPAIR LAB", mono, MUTE, tracking=1, anchor_left=False)
spaced(d, (S-M, ly+34), "REF · 2026", monos, CYAN_D, tracking=2, anchor_left=False)
d.line([(M, 214),(S-M, 214)], fill=(40,54,74), width=2)
d.rectangle([M, 213, M+120, 215], fill=CYAN)

# ================= HERO: GPU illustration =================
bx0, by0, bx1, by1 = 250, 300, 830, 520
sh = Image.new("L",(S,S),0); ImageDraw.Draw(sh).rounded_rectangle([bx0+8,by0+18,bx1+8,by1+18],radius=22,fill=120)
sh = sh.filter(ImageFilter.GaussianBlur(22))
img = Image.composite(Image.new("RGB",(S,S),(0,0,0)), img, sh); d = ImageDraw.Draw(img)

gc_x0 = bx0+40
d.rectangle([gc_x0, by1-6, gc_x0+300, by1+34], fill=(200,150,60))
for tx in range(gc_x0+6, gc_x0+300, 16):
    d.rectangle([tx, by1+14, tx+8, by1+34], fill=BG_TOP)
d.rectangle([bx0-26, by0+10, bx0+2, by1], fill=PANEL_L)
for sy in range(by0+26, by1-20, 34):
    d.rounded_rectangle([bx0-22, sy, bx0-6, sy+22], radius=3, outline=MUTE, width=2)

d.rounded_rectangle([bx0, by0, bx1, by1], radius=22, fill=PANEL, outline=CYAN, width=3)
d.rounded_rectangle([bx0+6, by0+6, bx1-6, by0+30], radius=12, fill=PANEL_L)
d.rounded_rectangle([bx1-150, by0-16, bx1-70, by0+6], radius=6, fill=PANEL_L, outline=MUTE, width=2)
d.rounded_rectangle([bx1-64, by0-16, bx1-6, by0+6], radius=6, fill=PANEL_L, outline=MUTE, width=2)

def fan(cx, cy, r):
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(12,18,27), outline=CYAN, width=3)
    d.ellipse([cx-r+10, cy-r+10, cx+r-10, cy+r-10], outline=(24,60,80), width=2)
    for k in range(9):
        a = math.radians(k*40); a2 = a + 0.75
        x1,y1 = cx+(r-14)*math.cos(a), cy+(r-14)*math.sin(a)
        x2,y2 = cx+20*math.cos(a2), cy+20*math.sin(a2)
        d.line([(x1,y1),(x2,y2)], fill=(30,90,120), width=5)
    d.ellipse([cx-16, cy-16, cx+16, cy+16], fill=PANEL_L, outline=CYAN, width=2)
    d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=AMBER)
fan(400, 410, 78); fan(680, 410, 78)
d.line([(540, 330),(540, 490)], fill=(40,54,74), width=2)
d.ellipse([533, 356, 547, 370], fill=CYAN)

d.line([(bx1+18, by0),(bx1+18, by1)], fill=(40,54,74), width=1)
spaced(d, (bx1+26, by0+2), "DIAG", monos, CYAN_D, tracking=2)

wy = by1+58
d.line([(bx0, wy),(bx0+300, wy)], fill=(40,54,74), width=2)
pts=[(bx0+i, wy-14*math.sin(i/12.0)*math.exp(-((i-150)**2)/12000)) for i in range(0,301,6)]
d.line(pts, fill=CYAN, width=2, joint="curve")
spaced(d, (bx0+312, wy-12), "SIGNAL OK", monos, CYAN, tracking=2)

# ================= HEADLINE =================
h1 = F("BigShoulders-Bold.ttf", 132)
center(d, 620, "REPARO DE PLACAS", h1, WHITE, tracking=1)
center(d, 620+118, "DE VÍDEO", h1, CYAN, tracking=1)
uw = 250
d.rectangle([(S-uw)/2, 620+118+140, (S+uw)/2, 620+118+148], fill=AMBER)

# ================= SUPPORT LINE =================
sub = F("JetBrainsMono-Bold.ttf", 24)
sub_txt = "NÃO LIGA  ·  ARTEFATOS  ·  SUPERAQUECE  ·  TRAVA"
sw = d.textlength(sub_txt, font=sub)
d.text(((S-sw)/2, 916), sub_txt, font=sub, fill=MUTE)

# ================= CTA WhatsApp pill =================
pill_y0, pill_y1 = 968, 1032
pw = 560
px0 = (S-pw)/2; px1 = px0+pw
pg = Image.new("L",(S,S),0); ImageDraw.Draw(pg).rounded_rectangle([px0,pill_y0,px1,pill_y1],radius=32,fill=120)
pg=pg.filter(ImageFilter.GaussianBlur(24))
img=Image.composite(Image.new("RGB",(S,S),CYAN), img, pg.point(lambda p:int(p*0.5))); d=ImageDraw.Draw(img)
d.rounded_rectangle([px0, pill_y0, px1, pill_y1], radius=32, fill=CYAN)

# whatsapp handset icon (vector)
gcx, gcy, gr = int(px0+48), int((pill_y0+pill_y1)/2), 27
d.ellipse([gcx-gr, gcy-gr, gcx+gr, gcy+gr], fill=BG_TOP)
ic = Image.new("RGBA",(72,72),(0,0,0,0)); di = ImageDraw.Draw(ic)
di.line([(24,24),(48,48)], fill=CYAN+(255,), width=15)
di.ellipse([12,12,34,34], fill=CYAN+(255,))
di.ellipse([38,38,60,60], fill=CYAN+(255,))
di.ellipse([21,21,29,29], fill=BG_TOP+(255,))
di.ellipse([47,47,55,55], fill=BG_TOP+(255,))
ic = ic.rotate(-12, resample=Image.BICUBIC, center=(36,36))
img.paste(ic, (gcx-36, gcy-36), ic); d = ImageDraw.Draw(img)

num = F("BigShoulders-Bold.ttf", 66)
d.text((gcx+gr+22, gcy-40), "16 99973-0151", font=num, fill=BG_TOP)

# tiny caption
cap = F("JetBrainsMono-Regular.ttf", 19)
cap_txt = "ORÇAMENTO SEM COMPROMISSO  ·  ENVIE FOTOS NO WHATSAPP"
cw = d.textlength(cap_txt, font=cap)
d.text(((S-cw)/2, pill_y1+14), cap_txt, font=cap, fill=MUTE)

img.save(os.path.join(_HERE, "abdalla-tech-reparo-gpu.png"))
print("saved")
