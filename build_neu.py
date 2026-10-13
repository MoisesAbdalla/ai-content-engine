#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Neumorphism — Abdalla Tech GPU repair promo (1080x1080), soft-UI."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

S = 1080
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
CF = os.environ.get("FONTS_DIR", os.path.join(_HERE, "fonts"))
def F(n,s): return ImageFont.truetype(f"{CF}/{n}", s)

# ---- soft-UI palette ----
BASE   = (226, 231, 240)
DARK   = (166, 178, 198)   # bottom-right shadow
LIGHT  = (255, 255, 255)   # top-left highlight
MID    = (196, 205, 220)
TEXT   = (58, 74, 101)
MUTE   = (140, 153, 174)
ACCENT = (245, 124, 31)
ACC_D  = (208, 100, 16)

img = Image.new("RGB", (S, S), BASE)

def rr_mask(box, radius):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle(box, radius=radius, fill=255)
    return m
def el_mask(box):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse(box, fill=255)
    return m

def neu(mask, dist=16, blur=22, raised=True, sd=0.55, sl=0.95, surface=None):
    """Apply neumorphic raised/inset shading for a shape mask onto global img."""
    global img
    bl = mask.filter(ImageFilter.GaussianBlur(blur))
    if raised:
        d_off = ImageChops.offset(bl, dist, dist)
        l_off = ImageChops.offset(bl, -dist, -dist)
        img = Image.composite(Image.new("RGB",(S,S),DARK),  img, d_off.point(lambda p:int(p*sd)))
        img = Image.composite(Image.new("RGB",(S,S),LIGHT), img, l_off.point(lambda p:int(p*sl)))
        fill = surface if surface is not None else Image.new("RGB",(S,S),BASE)
        img = Image.composite(fill, img, mask)
    else:  # inset / pressed
        fill = surface if surface is not None else Image.new("RGB",(S,S),BASE)
        img = Image.composite(fill, img, mask)
        sd_m = ImageChops.offset(mask, dist, dist)
        sl_m = ImageChops.offset(mask, -dist, -dist)
        inner_d = ImageChops.multiply(ImageChops.subtract(mask, sd_m).filter(ImageFilter.GaussianBlur(blur)), mask)
        inner_l = ImageChops.multiply(ImageChops.subtract(mask, sl_m).filter(ImageFilter.GaussianBlur(blur)), mask)
        img = Image.composite(Image.new("RGB",(S,S),DARK),  img, inner_d.point(lambda p:int(p*0.75)))
        img = Image.composite(Image.new("RGB",(S,S),LIGHT), img, inner_l.point(lambda p:int(p*0.9)))

def vgrad(c1, c2):
    a=np.array(c1,float); b=np.array(c2,float)
    g=(a[None,:]+(b-a)[None,:]*np.linspace(0,1,S)[:,None])
    return Image.fromarray(np.repeat(g[:,None,:],S,axis=1).astype(np.uint8),"RGB")

# soft vignette on background for depth
vg = Image.new("L",(S,S),0); ImageDraw.Draw(vg).rounded_rectangle([40,40,S-40,S-40],radius=60,fill=255)
vg = ImageChops.invert(vg).filter(ImageFilter.GaussianBlur(60))
img = Image.composite(Image.new("RGB",(S,S),(210,216,227)), img, vg.point(lambda p:int(p*0.5)))

# ================= HEADER =================
lx, ly = 96, 118
neu(rr_mask([lx, ly, lx+96, ly+96], 26), dist=10, blur=16, raised=True)
neu(rr_mask([lx+22, ly+22, lx+74, ly+74], 14), dist=8, blur=10, raised=True,
    surface=vgrad(ACCENT, ACC_D))

def draw_text(xy, text, font, fill, tracking=0, hl=True, anchor_left=True):
    d = ImageDraw.Draw(img)
    x,y = xy
    if not anchor_left:
        w = sum(d.textlength(c,font=font)+tracking for c in text)-tracking
        x -= w
    for c in text:
        if hl:
            d.text((x+1.5,y+1.6), c, font=font, fill=LIGHT)
        d.text((x,y), c, font=font, fill=fill)
        x += d.textlength(c,font=font)+tracking

brand = F("Outfit-Bold.ttf", 52)
tag   = F("JetBrainsMono-Bold.ttf", 20)
draw_text((lx+120, ly+8), "ABDALLA TECH", brand, TEXT, tracking=1)
draw_text((lx+123, ly+60), "ASSISTÊNCIA TÉCNICA GAMER", tag, MUTE, tracking=3, hl=False)
draw_text((S-96, ly+22), "GPU // REPAIR LAB", tag, MUTE, tracking=1, hl=False, anchor_left=False)

# ================= CENTER CARD =================
cbox = [150, 292, 930, 612]
neu(rr_mask(cbox, 42), dist=20, blur=30, raised=True, surface=vgrad((232,237,246), BASE))

d = ImageDraw.Draw(img)
# ---- GPU: raised shroud on card ----
sbox = [230, 336, 850, 556]
neu(rr_mask(sbox, 30), dist=12, blur=18, raised=True, surface=vgrad((234,239,247), (219,225,236)))
d = ImageDraw.Draw(img)

# PCIe connector (raised bar under shroud)
neu(rr_mask([300, 556, 600, 588], 8), dist=7, blur=10, raised=True, surface=vgrad(ACCENT,(230,170,90)))
d = ImageDraw.Draw(img)
for tx in range(312, 588, 16):
    d.line([(tx,570),(tx,588)], fill=(160,120,60), width=3)

# fans: inset pressed circles with soft blades + raised hub
def fan(cx, cy, r):
    global img
    neu(el_mask([cx-r,cy-r,cx+r,cy+r]), dist=10, blur=16, raised=False)
    dd = ImageDraw.Draw(img)
    for k in range(9):
        a=math.radians(k*40); a2=a+0.7
        x1,y1=cx+(r-16)*math.cos(a), cy+(r-16)*math.sin(a)
        x2,y2=cx+24*math.cos(a2), cy+24*math.sin(a2)
        dd.line([(x1,y1),(x2,y2)], fill=MID, width=7)
    neu(el_mask([cx-22,cy-22,cx+22,cy+22]), dist=6, blur=9, raised=True)
    ImageDraw.Draw(img).ellipse([cx-8,cy-8,cx+8,cy+8], fill=ACCENT)
fan(400, 446, 80); fan(680, 446, 80)
d = ImageDraw.Draw(img)
# center emblem strip
d.line([(540,360),(540,532)], fill=MID, width=3)

# ================= HEADLINE =================
def fit(text, path, maxw, start, tracking=1):
    s=start
    while s>10:
        f=F(path,s); d=ImageDraw.Draw(img)
        w=sum(d.textlength(c,font=f)+tracking for c in text)-tracking
        if w<=maxw: return f,w
        s-=2
    return F(path,10),0
def center_txt(y, text, path, fill, maxw=884, start=120, tracking=1, hl=True):
    f,w = fit(text,path,maxw,start,tracking)
    x=(S-w)/2; d=ImageDraw.Draw(img)
    for c in text:
        if hl: d.text((x+2,y+2),c,font=f,fill=LIGHT)
        d.text((x,y),c,font=f,fill=fill); x+=d.textlength(c,font=f)+tracking
    return f

f1 = center_txt(646, "REPARO DE PLACAS", "Outfit-Bold.ttf", TEXT, start=100)
center_txt(646+92, "DE VÍDEO", "Outfit-Bold.ttf", ACCENT, start=100)

# ================= SUPPORT LINE =================
sub = F("JetBrainsMono-Bold.ttf", 22)
d = ImageDraw.Draw(img)
st = "NÃO LIGA   ·   ARTEFATOS   ·   SUPERAQUECE   ·   TRAVA"
sw = d.textlength(st, font=sub)
draw_text(((S-sw)/2, 872), st, sub, MUTE, hl=False)

# ================= CTA WhatsApp pill =================
pbox = [260, 930, 820, 1004]
neu(rr_mask(pbox, 37), dist=14, blur=20, raised=True, surface=vgrad(ACCENT, ACC_D))
d = ImageDraw.Draw(img)
# whatsapp handset (white on accent)
gcx, gcy, gr = 320, 967, 26
d.ellipse([gcx-gr,gcy-gr,gcx+gr,gcy+gr], fill=(255,255,255))
ic=Image.new("RGBA",(72,72),(0,0,0,0)); di=ImageDraw.Draw(ic)
di.line([(24,24),(48,48)], fill=ACC_D+(255,), width=14)
di.ellipse([12,12,34,34], fill=ACC_D+(255,)); di.ellipse([38,38,60,60], fill=ACC_D+(255,))
di.ellipse([21,21,29,29], fill=(255,255,255,255)); di.ellipse([47,47,55,55], fill=(255,255,255,255))
ic=ic.rotate(-12, resample=Image.BICUBIC, center=(36,36))
img.paste(ic,(gcx-36,gcy-36),ic); d=ImageDraw.Draw(img)
num = F("BigShoulders-Bold.ttf", 62)
d.text((gcx+gr+20, gcy-38), "16 99973-0151", font=num, fill=(255,255,255))

# caption
cap = F("JetBrainsMono-Regular.ttf", 19)
ct = "ORÇAMENTO SEM COMPROMISSO  ·  ENVIE FOTOS NO WHATSAPP"
cw = d.textlength(ct, font=cap)
d.text(((S-cw)/2, 1026), ct, font=cap, fill=MUTE)

img.save(os.path.join(_HERE, "abdalla-tech-reparo-gpu-neu.png"))
print("saved")
