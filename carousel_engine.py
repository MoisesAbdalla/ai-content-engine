#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Motor reutilizavel de carrossel Abdalla Tech (1080x1350, 4:5).
Identidade: gradiente verde escuro + esmeralda + circuitos + logo robo.
Uso: from carousel_engine import build; build(spec, out_dir)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1080, 1350
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
CF = os.environ.get("FONTS_DIR", os.path.join(_HERE, "fonts"))
LOGO_PATH = os.path.join(_HERE, "impressora/logo_icon.png")
def F(n, s): return ImageFont.truetype(f"{CF}/{n}", s)

WORD, HEAD = "Tektur-Medium.ttf", "WorkSans-Bold.ttf"
BODY, BODYB, LAB = "InstrumentSans-Regular.ttf", "InstrumentSans-Bold.ttf", "InstrumentSans-Regular.ttf"

GREEN = (46, 230, 118); GRN_D = (24, 150, 84)
WHITE = (240, 246, 242); GRAY = (150, 166, 156); DIM = (96, 112, 104); INK = (9, 13, 11)
M = 92

LOGO = Image.open(LOGO_PATH).convert("RGBA")
VL, VR, VB = 78 / 720, 642 / 720, 452 / 600
def paste_logo(img, cx, cy, full_h):
    w = int(full_h * LOGO.width / LOGO.height)
    s = LOGO.resize((w, int(full_h)), Image.LANCZOS)
    img.paste(s, (int(cx - w / 2), int(cy - full_h / 2)), s)
    return w

# ---------- text utils ----------
_sc = ImageDraw.Draw(Image.new("RGB", (10, 10)))
def tracked(d, x, y, t, f, fill, tr):
    for ch in t:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + tr
def tracked_w(t, f, tr):
    return sum(_sc.textlength(c, font=f) + tr for c in t) - (tr if t else 0)
def ctracked(d, y, t, f, fill, tr):
    tracked(d, (W - tracked_w(t, f, tr)) / 2, y, t, f, fill, tr)
def wrap(t, f, mw):
    ls, cur = [], ""
    for wd in t.split():
        s = (cur + " " + wd).strip()
        if _sc.textlength(s, font=f) <= mw: cur = s
        else:
            if cur: ls.append(cur)
            cur = wd
    if cur: ls.append(cur)
    return ls
def fit(path, lines, mw, start, mins=44, tr=0):
    s = start
    while s > mins:
        f = F(path, s)
        if all(tracked_w(ln, f, tr) <= mw for ln in lines): return f
        s -= 2
    return F(path, mins)
def cham(box, c):
    x0, y0, x1, y1 = box
    return [(x0 + c, y0), (x1, y0), (x1, y1 - c), (x1 - c, y1), (x0, y1), (x0, y0 + c)]
def lh_of(s, k=1.06): return int(s * k)

def glow(img, fn, passes=(14, 7), core=True):
    l = Image.new("RGB", (W, H), (0, 0, 0)); fn(ImageDraw.Draw(l))
    for g in passes: img = ImageChops.screen(img, l.filter(ImageFilter.GaussianBlur(g)))
    if core: img = ImageChops.screen(img, l)
    return img

# ---------- background ----------
def base_bg():
    top = np.array((16, 22, 19), float); bot = np.array((9, 16, 13), float)
    g = top[None, :] + (bot - top)[None, :] * np.linspace(0, 1, H)[:, None]
    im = Image.fromarray(np.repeat(g[:, None, :], W, axis=1).astype(np.uint8), "RGB")
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([W//2 - 620, H - 300, W//2 + 620, H + 520], fill=150)
    m = m.filter(ImageFilter.GaussianBlur(210))
    im = ImageChops.screen(im, Image.composite(Image.new("RGB", (W, H), (18, 92, 56)),
                                               Image.new("RGB", (W, H), (0, 0, 0)), m))
    m2 = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m2).ellipse([-260, -260, 360, 360], fill=70)
    m2 = m2.filter(ImageFilter.GaussianBlur(200))
    im = ImageChops.screen(im, Image.composite(Image.new("RGB", (W, H), (16, 70, 46)),
                                               Image.new("RGB", (W, H), (0, 0, 0)), m2))
    im = circuits(im)
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-320, -320, W + 320, H + 320], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(260))
    im = Image.composite(im, ImageChops.multiply(im, Image.new("RGB", (W, H), (150, 150, 150))), vig)
    return im
def circuits(im):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    rng = np.random.default_rng(11)
    for _ in range(26):
        x = int(rng.integers(-40, W)); y = int(rng.integers(60, H - 60)); a = int(rng.integers(14, 40))
        col = (46, 230, 118, a); length = int(rng.integers(70, 300)); dx = 1 if rng.random() < .5 else -1
        x2 = x + dx * length; vy = int(rng.integers(35, 150)) * (1 if rng.random() < .5 else -1)
        d.line([(x, y), (x2, y)], fill=col, width=2); d.line([(x2, y), (x2, y + vy)], fill=col, width=2)
        d.ellipse([x2 - 5, y + vy - 5, x2 + 5, y + vy + 5], outline=(46, 230, 118, a + 45), width=2)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(46, 230, 118, a))
    return Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")
def scanlines(img, f=0.94):
    a = np.asarray(img).astype(np.float32); a[0::3, :, :] *= f
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")

# ---------- logo / header / footer ----------
def wordmark_beside(img, x, cy, ws, tr):
    d = ImageDraw.Draw(img); wf = F(WORD, ws); aw = tracked_w("ABDALLA", wf, tr)
    tracked(d, x, cy - ws * 0.76, "ABDALLA", wf, WHITE, tr)
    tf = F(WORD, int(ws * 0.46)); tw = tracked_w("TECH", tf, tr + 3)
    ty = cy + ws * 0.26; tcx = x + (aw - tw) / 2
    tracked(d, tcx, ty, "TECH", tf, GREEN, tr + 3)
    ly = ty + ws * 0.30
    d.line([(x, ly), (tcx - 12, ly)], fill=GRN_D, width=2)
    d.line([(tcx + tw + 12, ly), (x + aw, ly)], fill=GRN_D, width=2)
    return x + aw
def logo_cover(img, cx, cy_icon, full_h, ws):
    paste_logo(img, cx, cy_icon, full_h)
    hb = cy_icon + (VB - 0.5) * full_h; d = ImageDraw.Draw(img); tr = 4
    top = hb + ws * 0.34
    ctracked(d, top, "ABDALLA", F(WORD, ws), WHITE, tr)
    ctracked(d, top + ws * 1.02, "TECH", F(WORD, int(ws * 0.5)), GREEN, tr + 10)
    return img
def header(img, counter):
    full_h = 100; iw = full_h * LOGO.width / LOGO.height
    paste_logo(img, M + (0.5 - VL) * iw, 106, full_h)
    wordmark_beside(img, M + (VR - VL) * iw + 18, 108, 34, 2)
    d = ImageDraw.Draw(img); cf = F(WORD, 24)
    d.text((W - M - d.textlength(counter, font=cf), 90), counter, font=cf, fill=GREEN)
    lf = F(LAB, 14)
    d.text((W - M - d.textlength("CARROSSEL", font=lf), 122), "CARROSSEL", font=lf, fill=DIM)
    img = glow(img, lambda dl: dl.line([(M, 176), (W - M, 176)], fill=GREEN, width=2), passes=(8, 4))
    ImageDraw.Draw(img).rectangle([M, 173, M + 118, 179], fill=GREEN)
    return img
def footer(img, left, right=None):
    d = ImageDraw.Draw(img); y = 1274
    d.line([(M, y - 22), (W - M, y - 22)], fill=(38, 50, 44), width=1)
    d.text((M, y), left, font=F(LAB, 17), fill=DIM)
    rt = right or "WhatsApp  16 99973-0151"
    d.text((W - M - d.textlength(rt, font=F(BODYB, 17)), y), rt, font=F(BODYB, 17), fill=GRAY)
    return img

# ---------- ICONS (green line style, center cx,cy) ----------
def _r(d, b, r, **k): d.rounded_rectangle(b, r, **k)
def ic_calendar(d, x, y):
    _r(d, [x-40,y-32,x+40,y+38], 8, outline=GREEN, width=5); d.line([(x-40,y-12),(x+40,y-12)],fill=GREEN,width=5)
    d.line([(x-22,y-44),(x-22,y-24)],fill=GREEN,width=6); d.line([(x+22,y-44),(x+22,y-24)],fill=GREEN,width=6)
    for gx in (-20,0,20): d.ellipse([x+gx-5,y+4,x+gx+5,y+14],fill=GREEN)
def ic_power(d, x, y):
    d.arc([x-32,y-28,x+32,y+36],300,240,fill=GREEN,width=6); d.line([(x,y-42),(x,y-2)],fill=GREEN,width=6)
def ic_drop_warn(d, x, y):
    d.pieslice([x-30,y-18,x+18,y+28],0,180,outline=GREEN,width=5)
    d.line([(x-6,y-38),(x-30,y+2)],fill=GREEN,width=5); d.line([(x-6,y-38),(x+18,y+2)],fill=GREEN,width=5)
    d.line([(x+30,y-8),(x+30,y+12)],fill=WHITE,width=6); d.ellipse([x+26,y+20,x+34,y+28],fill=WHITE)
def ic_bottle(d, x, y):
    d.rectangle([x-9,y-42,x+9,y-30],outline=GREEN,width=5); _r(d,[x-22,y-28,x+22,y+42],10,outline=GREEN,width=5)
    _r(d,[x-22,y+8,x+22,y+42],10,fill=GREEN)
def ic_nozzle(d, x, y):
    _r(d,[x-42,y-38,x+42,y+42],8,outline=GREEN,width=5)
    for i,gx in enumerate(range(-28,38,19)): d.line([(x+gx,y-24 if i%2==0 else y-10),(x+gx,y+28)],fill=GREEN,width=6)
def ic_shield(d, x, y):
    d.polygon([(x,y-44),(x+36,y-26),(x+36,y+8),(x,y+44),(x-36,y+8),(x-36,y-26)],outline=GREEN,width=5)
    d.line([(x-15,y),(x-3,y+15)],fill=GREEN,width=6); d.line([(x-3,y+15),(x+19,y-13)],fill=GREEN,width=6)
def ic_shield_bolt(d, x, y):
    d.polygon([(x,y-44),(x+36,y-26),(x+36,y+8),(x,y+44),(x-36,y+8),(x-36,y-26)],outline=GREEN,width=5)
    d.polygon([(x+4,y-20),(x-12,y+4),(x-1,y+4),(x-6,y+22),(x+14,y-6),(x+2,y-6)],fill=GREEN)
def ic_chip(d, x, y):
    _r(d,[x-30,y-30,x+30,y+30],7,outline=GREEN,width=5)
    _r(d,[x-14,y-14,x+14,y+14],4,outline=GREEN,width=4)
    for gx in (-18,0,18):
        d.line([(x+gx,y-44),(x+gx,y-30)],fill=GREEN,width=5); d.line([(x+gx,y+30),(x+gx,y+44)],fill=GREEN,width=5)
        d.line([(x-44,y+gx),(x-30,y+gx)],fill=GREEN,width=5); d.line([(x+30,y+gx),(x+44,y+gx)],fill=GREEN,width=5)
def ic_board(d, x, y):
    _r(d,[x-42,y-34,x+42,y+38],6,outline=GREEN,width=5)
    _r(d,[x-30,y-22,x-6,y+2],3,outline=GREEN,width=4); d.rectangle([x+4,y-20,x+30,y-10],outline=GREEN,width=4)
    d.rectangle([x+4,y-2,x+30,y+8],outline=GREEN,width=4)
    for gx in range(-26,32,12): d.line([(x+gx,y+16),(x+gx,y+30)],fill=GREEN,width=4)
def ic_swap_x(d, x, y):
    d.line([(x-34,y-14),(x+22,y-14)],fill=GREEN,width=5); d.polygon([(x+22,y-24),(x+38,y-14),(x+22,y-4)],fill=GREEN)
    d.line([(x+34,y+14),(x-22,y+14)],fill=GREEN,width=5); d.polygon([(x-22,y+4),(x-38,y+14),(x-22,y+24)],fill=GREEN)
    d.line([(x+30,y-30),(x+46,y-14)],fill=WHITE,width=5); d.line([(x+46,y-30),(x+30,y-14)],fill=WHITE,width=5)
def ic_money(d, x, y):
    for i,off in enumerate((16,2,-12)):
        d.ellipse([x-30,y+off-8,x+30,y+off+8],outline=GREEN,width=4)
    d.ellipse([x-24,y-40,x+24,y-4],outline=GREEN,width=4)
    d.text((x-8,y-38),"$",font=F(BODYB,34),fill=GREEN)
def ic_microscope(d, x, y):
    d.line([(x-6,y-40),(x+14,y-14)],fill=GREEN,width=7); d.line([(x-6,y-40),(x-18,y-30)],fill=GREEN,width=6)
    d.line([(x+8,y-20),(x-8,y+10)],fill=GREEN,width=6); d.arc([x-24,y-12,x+8,y+20],20,200,fill=GREEN,width=5)
    d.line([(x-30,y+34),(x+30,y+34)],fill=GREEN,width=6); d.line([(x-6,y+10),(x-16,y+34)],fill=GREEN,width=5)
def ic_check_badge(d, x, y):
    d.ellipse([x-38,y-38,x+38,y+38],outline=GREEN,width=5)
    d.line([(x-16,y),(x-4,y+14)],fill=GREEN,width=7); d.line([(x-4,y+14),(x+18,y-14)],fill=GREEN,width=7)
def ic_restart(d, x, y):
    d.arc([x-32,y-32,x+32,y+32],40,330,fill=GREEN,width=6)
    d.polygon([(x+30,y-30),(x+34,y-6),(x+12,y-16)],fill=GREEN)
def ic_monitor(d, x, y):
    _r(d,[x-42,y-34,x+42,y+18],6,outline=GREEN,width=5); d.line([(x-16,y+18),(x-22,y+34)],fill=GREEN,width=5)
    d.line([(x+16,y+18),(x+22,y+34)],fill=GREEN,width=5); d.line([(x-26,y+34),(x+26,y+34)],fill=GREEN,width=5)
    d.line([(x-28,y-18),(x-8,y+2)],fill=GREEN,width=4); d.line([(x-8,y-18),(x-28,y+2)],fill=GREEN,width=4)
    d.line([(x+8,y-18),(x+28,y+2)],fill=GREEN,width=4); d.line([(x+28,y-18),(x+8,y+2)],fill=GREEN,width=4)
def ic_thermometer(d, x, y):
    d.rounded_rectangle([x-8,y-40,x+8,y+20],8,outline=GREEN,width=5); d.ellipse([x-16,y+16,x+16,y+44],fill=GREEN)
    d.line([(x,y-30),(x,y+20)],fill=GREEN,width=5)
def ic_sound(d, x, y):
    d.polygon([(x-30,y-12),(x-12,y-12),(x+4,y-28),(x+4,y+28),(x-12,y+12),(x-30,y+12)],outline=GREEN,width=5)
    d.arc([x-2,y-24,x+30,y+24],300,60,fill=GREEN,width=5); d.arc([x+6,y-38,x+50,y+38],300,60,fill=GREEN,width=5)
def ic_dust(d, x, y):
    d.line([(x-34,y+30),(x+34,y+30)],fill=GREEN,width=5)
    for cx,cy,rr in [(-14,4,16),(10,10,18),(-2,-14,14),(20,-6,12)]:
        d.ellipse([x+cx-rr,y+cy-rr,x+cx+rr,y+cy+rr],outline=GREEN,width=4)
def ic_syringe(d, x, y):
    d.line([(x-34,y+34),(x+30,y-30)],fill=GREEN,width=0)
    _r(d,[x-6,y-30,x+18,y+14],4,outline=GREEN,width=5)
    d.line([(x+10,y+14),(x+30,y+34)],fill=GREEN,width=5); d.line([(x-14,y-38),(x+2,y-22)],fill=GREEN,width=6)
    d.line([(x-20,y-24),(x-4,y-8)],fill=GREEN,width=4); d.ellipse([x+30,y+30,x+40,y+40],fill=GREEN)
def ic_bed(d, x, y):
    d.line([(x-40,y-6),(x-40,y+30)],fill=GREEN,width=5); d.line([(x-40,y+6),(x+40,y+6)],fill=GREEN,width=5)
    d.line([(x+40,y-2),(x+40,y+30)],fill=GREEN,width=5); d.arc([x-40,y-20,x-4,y+16],180,360,fill=GREEN,width=5)
    d.line([(x-40,y+30),(x+40,y+30)],fill=GREEN,width=5)
def ic_fan(d, x, y):
    d.ellipse([x-38,y-38,x+38,y+38],outline=GREEN,width=5)
    import math
    for k in range(3):
        a = math.radians(k*120)
        d.pieslice([x-30,y-30,x+30,y+30], int(math.degrees(a)), int(math.degrees(a))+60, outline=GREEN, width=4)
    d.ellipse([x-8,y-8,x+8,y+8],fill=GREEN)
def ic_cpu(d, x, y):
    _r(d,[x-26,y-26,x+26,y+26],5,outline=GREEN,width=5); _r(d,[x-10,y-10,x+10,y+10],3,outline=GREEN,width=4)
    for gx in (-12,12):
        d.line([(x+gx,y-40),(x+gx,y-26)],fill=GREEN,width=5); d.line([(x+gx,y+26),(x+gx,y+40)],fill=GREEN,width=5)
        d.line([(x-40,y+gx),(x-26,y+gx)],fill=GREEN,width=5); d.line([(x+26,y+gx),(x+40,y+gx)],fill=GREEN,width=5)
def ic_gauge(d, x, y):
    d.arc([x-38,y-30,x+38,y+46],180,360,fill=GREEN,width=6); d.line([(x,y+8),(x+22,y-16)],fill=GREEN,width=6)
    d.ellipse([x-6,y+2,x+6,y+14],fill=GREEN)
def ic_plug_bolt(d, x, y):
    d.rounded_rectangle([x-24,y-24,x+24,y+16],8,outline=GREEN,width=5)
    d.line([(x-12,y-38),(x-12,y-24)],fill=GREEN,width=5); d.line([(x+12,y-38),(x+12,y-24)],fill=GREEN,width=5)
    d.line([(x,y+16),(x,y+40)],fill=GREEN,width=5)
    d.polygon([(x+2,y-14),(x-10,y+2),(x-1,y+2),(x-4,y+14),(x+10,y-4),(x+1,y-4)],fill=GREEN)
def ic_brush(d, x, y):
    d.line([(x+30,y-38),(x-4,y-4)],fill=GREEN,width=8)
    _r(d,[x-24,y-6,x+8,y+16],5,fill=GREEN)
    for gx in range(-18,10,7): d.line([(x+gx,y+16),(x+gx-4,y+40)],fill=GREEN,width=4)
def ic_no_water(d, x, y):
    d.pieslice([x-24,y-14,x+18,y+30],0,180,outline=GREEN,width=5)
    d.line([(x-3,y-34),(x-24,y+2)],fill=GREEN,width=5); d.line([(x-3,y-34),(x+18,y+2)],fill=GREEN,width=5)
    d.ellipse([x-40,y-40,x+40,y+40],outline=WHITE,width=5); d.line([(x-28,y+28),(x+28,y-28)],fill=WHITE,width=5)
def ic_scale(d, x, y):
    d.line([(x,y-40),(x,y+30)],fill=GREEN,width=5); d.line([(x-34,y-30),(x+34,y-30)],fill=GREEN,width=5)
    d.line([(x-18,y+30),(x+18,y+30)],fill=GREEN,width=5)
    d.arc([x-50,y-30,x-18,y+6],0,180,fill=GREEN,width=4); d.arc([x+18,y-30,x+50,y+6],0,180,fill=GREEN,width=4)
def ic_clock(d, x, y):
    d.ellipse([x-38,y-38,x+38,y+38],outline=GREEN,width=5)
    d.line([(x,y),(x,y-22)],fill=GREEN,width=5); d.line([(x,y),(x+16,y+8)],fill=GREEN,width=5)
def ic_magnifier(d, x, y):
    d.ellipse([x-34,y-34,x+14,y+14],outline=GREEN,width=6); d.line([(x+12,y+12),(x+34,y+34)],fill=GREEN,width=8)
def ic_wrench(d, x, y):
    d.arc([x-36,y-36,x+4,y+4],120,360,fill=GREEN,width=8); d.line([(x-6,y-6),(x+30,y+30)],fill=GREEN,width=9)
def ic_refresh(d, x, y):
    d.arc([x-32,y-32,x+32,y+32],30,300,fill=GREEN,width=6); d.polygon([(x+26,y-30),(x+34,y-8),(x+12,y-12)],fill=GREEN)
def ic_bug(d, x, y):
    d.ellipse([x-20,y-14,x+20,y+30],outline=GREEN,width=5); d.ellipse([x-12,y-32,x+12,y-10],outline=GREEN,width=5)
    d.line([(x-20,y),(x-40,y-10)],fill=GREEN,width=4); d.line([(x+20,y),(x+40,y-10)],fill=GREEN,width=4)
    d.line([(x-20,y+16),(x-40,y+24)],fill=GREEN,width=4); d.line([(x+20,y+16),(x+40,y+24)],fill=GREEN,width=4)
    d.line([(x-14,y-30),(x-24,y-42)],fill=GREEN,width=4); d.line([(x+14,y-30),(x+24,y-42)],fill=GREEN,width=4)
def ic_printer(d, x, y):
    d.rectangle([x-42,y-32,x+42,y-4],outline=GREEN,width=5); _r(d,[x-50,y-8,x+50,y+32],6,outline=GREEN,width=5)
    d.rectangle([x-30,y+28,x+30,y+50],outline=GREEN,width=5); d.ellipse([x+28,y+4,x+38,y+14],fill=GREEN)

ICONS = {k[3:]: v for k, v in globals().items() if k.startswith("ic_")}

def ghost_number(img, txt):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
    f = F(HEAD, 340); tw = dl.textlength(txt, font=f)
    dl.text((W - M - tw + 6, 210), txt, font=f, fill=GREEN + (26,))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
def badge(img, cx, cy, iconfn, r=90):
    ImageDraw.Draw(img).ellipse([cx - r, cy - r, cx + r, cy + r], fill=(19, 27, 23))
    img = glow(img, lambda dl: dl.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GREEN, width=4), passes=(11, 5))
    ICONS[iconfn](ImageDraw.Draw(img), cx, cy)
    return img

# ---------- slides ----------
DEF_SEAL = "REPARO ELETRÔNICO NÍVEL COMPONENTE · FRANCA / SP"
def slide_cover(spec):
    c = spec["cover"]; img = base_bg()
    img = logo_cover(img, W / 2, 208, 252, 60); d = ImageDraw.Draw(img)
    lines = c["title"]; f = fit(HEAD, lines, W - 2 * M, 108); lh = lh_of(f.size)
    y0 = c.get("title_y", 470)
    acc = c.get("accent_last", True)
    if acc:
        img = glow(img, lambda dl: ctracked(dl, y0 + (len(lines) - 1) * lh, lines[-1], f, GREEN, 0),
                   passes=(13, 6), core=False); d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        col = GREEN if (acc and i == len(lines) - 1) else WHITE
        ctracked(d, y0 + i * lh, ln, f, col, 0)
    dy = y0 + len(lines) * lh + 26
    d.line([(W / 2 - 130, dy), (W / 2 + 130, dy)], fill=(70, 92, 82), width=3)
    ctracked(d, dy + 34, c["subtitle"], F(LAB, 27), GRAY, 1)
    ctracked(d, dy + 82, c.get("seal", DEF_SEAL), F(BODYB, 22), GREEN, 1)
    ctracked(d, 1246, "arrasta para o lado  →", F(LAB, 30), GRAY, 1)
    return scanlines(footer(img, spec["footer_left"]))
def slide_item(spec, idx, total):
    it = spec["tips"][idx]; num = idx + 1; img = base_bg()
    img = header(img, f"{num + 1:02d} / {total:02d}")
    img = ghost_number(img, f"{num:02d}")
    img = badge(img, M + 92, 336, it["icon"]); d = ImageDraw.Draw(img)
    label = spec.get("item_label", "DICA")
    d.text((M + 208, 280), f"{label} {num:02d}", font=F(WORD, 28), fill=GREEN)
    img = glow(img, lambda dl: dl.line([(M + 210, 328), (M + 470, 328)], fill=GREEN, width=3), passes=(7, 3))
    d = ImageDraw.Draw(img); d.text((M + 210, 346), it["kicker"], font=F(BODYB, 24), fill=GRAY)
    f = fit(HEAD, it["title"], W - 2 * M, 92); lh = lh_of(f.size, 1.08); ty = 566
    for ln in it["title"]:
        d.text((M, ty), ln, font=f, fill=WHITE); ty += lh
    uy = ty + 12
    img = glow(img, lambda dl: dl.line([(M + 3, uy), (M + 168, uy)], fill=GREEN, width=6), passes=(11, 5))
    d = ImageDraw.Draw(img); bf = F(BODY, 37); by = uy + 46
    for ln in wrap(it["body"], bf, W - 2 * M - 20):
        d.text((M, by), ln, font=bf, fill=(206, 216, 210)); by += 52
    return scanlines(footer(img, spec["footer_left"]))
def slide_cta(spec, total):
    c = spec["cta"]; img = base_bg(); img = header(img, f"{total:02d} / {total:02d}"); d = ImageDraw.Draw(img)
    d.text((M, 250), c.get("kicker", "PRECISA DE AJUDA?"), font=F(WORD, 26), fill=GREEN)
    lines = c["headline"]; f = fit(HEAD, lines, W - 2 * M, 96); lh = lh_of(f.size, 1.08); y0 = 306
    for i, ln in enumerate(lines):
        d.text((M, y0 + i * lh), ln, font=f, fill=WHITE if i < len(lines) - 1 else GREEN)
    yb = y0 + len(lines) * lh + 30
    d.text((M, yb), c.get("resolve_title", "A gente resolve:"), font=F(BODYB, 34), fill=GREEN)
    bf = F(BODY, 33)
    for i, itt in enumerate(c["items"]):
        y = yb + 54 + i * 54; d.ellipse([M, y + 10, M + 14, y + 24], fill=GREEN)
        d.text((M + 34, y), itt, font=bf, fill=(210, 220, 214))
    bar_y = yb + 54 + len(c["items"]) * 54 + 28
    bar = cham([M, bar_y, W - M, bar_y + 98], 20)
    img = glow(img, lambda dl: dl.polygon(bar, fill=GREEN), passes=(18, 9), core=False)
    d = ImageDraw.Draw(img); d.polygon(bar, fill=GREEN)
    gcx, gcy = M + 58, bar_y + 49
    ic = Image.new("RGBA", (80, 80), (0, 0, 0, 0)); di = ImageDraw.Draw(ic)
    di.line([(26, 26), (54, 54)], fill=INK + (255,), width=16)
    di.ellipse([12, 12, 38, 38], fill=INK + (255,)); di.ellipse([42, 42, 68, 68], fill=INK + (255,))
    di.ellipse([22, 22, 32, 32], fill=GREEN + (255,)); di.ellipse([48, 48, 58, 58], fill=GREEN + (255,))
    ic = ic.rotate(-10, resample=Image.BICUBIC, center=(40, 40)); img.paste(ic, (gcx - 40, gcy - 40), ic)
    d = ImageDraw.Draw(img); d.text((gcx + 44, bar_y + 12), "16 99973-0151", font=F(HEAD, 62), fill=INK)
    cf = F(BODY, 30); cy = bar_y + 128
    for ln in wrap(c["caption"], cf, W - 2 * M):
        d.text((M, cy), ln, font=cf, fill=GRAY); cy += 42
    return scanlines(footer(img, spec["footer_left"], "Abdalla Tech · Reparo Eletrônico"))

def build(spec, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    total = len(spec["tips"]) + 2
    slide_cover(spec).save(f"{out_dir}/slide_01.png")
    for i in range(len(spec["tips"])):
        slide_item(spec, i, total).save(f"{out_dir}/slide_{i + 2:02d}.png")
    slide_cta(spec, total).save(f"{out_dir}/slide_{total:02d}.png")
    print(f"[{spec['slug']}] {total} slides -> {out_dir}")
    return total
