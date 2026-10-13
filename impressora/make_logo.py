#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recria a logo oficial Abdalla Tech — robô neumórfico com dois 'olhos' verdes.
Renderiza um sprite RGBA transparente (logo_icon.png) em alta resolução."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import os
_HERE = os.path.dirname(os.path.abspath(__file__))

SS = 3                      # supersample
CW, CH = 720, 600           # canvas (final)
GREEN = (46, 230, 118)
GREEN_HI = (198, 255, 224)

def rr_mask(size, box, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle(box, r, fill=255)
    return m

def vgrad(size, top, bot):
    w, h = size
    base = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        base.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return base.resize((w, h))

def build():
    W, H = CW * SS, CH * SS
    spr = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    def S(v): return int(v * SS)
    cx = W // 2

    # ----- geometry (final coords *SS) -----
    bezel = [S(78), S(70), S(642), S(430)]
    panel = [S(120), S(104), S(600), S(418)]
    eye_cy = S(248)
    eye_r  = S(92)
    lx, rx = S(268), S(452)
    dot_r  = S(30)
    r_bez, r_pan = S(90), S(70)

    # ----- drop shadow -----
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rounded_rectangle(
        [bezel[0], bezel[1] + S(24), bezel[2], bezel[3] + S(24)], r_bez, fill=190)
    sh = sh.filter(ImageFilter.GaussianBlur(S(26)))
    spr = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 235)),
                          spr, sh)

    # ----- bezel (raised frame) -----
    bez_grad = vgrad((W, H), (66, 72, 81), (34, 38, 45))
    bmask = rr_mask((W, H), bezel, r_bez)
    spr.paste(bez_grad, (0, 0), bmask)
    # top highlight on bezel
    hl = Image.new("L", (W, H), 0)
    ImageDraw.Draw(hl).rounded_rectangle(
        [bezel[0] + S(6), bezel[1] + S(5), bezel[2] - S(6), bezel[1] + S(70)], r_bez, fill=120)
    hl = ImageChops.multiply(hl.filter(ImageFilter.GaussianBlur(S(10))), bmask)
    spr.paste(Image.new("RGBA", (W, H), (150, 158, 168, 255)), (0, 0), hl)
    # bottom inner shadow on bezel
    bs = Image.new("L", (W, H), 0)
    ImageDraw.Draw(bs).rounded_rectangle(
        [bezel[0] + S(6), bezel[3] - S(60), bezel[2] - S(6), bezel[3] - S(4)], r_bez, fill=120)
    bs = ImageChops.multiply(bs.filter(ImageFilter.GaussianBlur(S(12))), bmask)
    spr.paste(Image.new("RGBA", (W, H), (14, 16, 20, 220)), (0, 0), bs)

    # ----- front panel (inset, darker) -----
    pan_grad = vgrad((W, H), (44, 49, 57), (26, 30, 36))
    pmask = rr_mask((W, H), panel, r_pan)
    spr.paste(pan_grad, (0, 0), pmask)
    # panel inner top shadow (recessed feel)
    ps = Image.new("L", (W, H), 0)
    ImageDraw.Draw(ps).rounded_rectangle(
        [panel[0], panel[1], panel[2], panel[1] + S(56)], r_pan, fill=150)
    ps = ImageChops.multiply(ps.filter(ImageFilter.GaussianBlur(S(14))), pmask)
    spr.paste(Image.new("RGBA", (W, H), (12, 14, 18, 210)), (0, 0), ps)
    # panel bottom highlight
    pb = Image.new("L", (W, H), 0)
    ImageDraw.Draw(pb).rounded_rectangle(
        [panel[0], panel[3] - S(46), panel[2], panel[3]], r_pan, fill=90)
    pb = ImageChops.multiply(pb.filter(ImageFilter.GaussianBlur(S(12))), pmask)
    spr.paste(Image.new("RGBA", (W, H), (70, 78, 88, 200)), (0, 0), pb)

    # ----- tabs (bottom feet) -----
    for tx0 in (S(214), S(292)):
        tb = [tx0, S(410), tx0 + S(56), S(452)]
        tmask = rr_mask((W, H), tb, S(12))
        spr.paste(vgrad((W, H), (34, 38, 45), (22, 25, 30)), (0, 0), tmask)
        ts = Image.new("L", (W, H), 0)
        ImageDraw.Draw(ts).rounded_rectangle([tb[0], tb[1], tb[2], tb[1] + S(16)], S(12), fill=140)
        ts = ImageChops.multiply(ts.filter(ImageFilter.GaussianBlur(S(6))), tmask)
        spr.paste(Image.new("RGBA", (W, H), (10, 12, 15, 220)), (0, 0), ts)

    # ----- eyes (recessed sockets) -----
    def socket(ecx):
        emask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(emask).ellipse([ecx - eye_r, eye_cy - eye_r, ecx + eye_r, eye_cy + eye_r], fill=255)
        # base fill radial-ish (dark center)
        spr.paste(Image.new("RGBA", (W, H), (20, 23, 28, 255)), (0, 0), emask)
        # inner top shadow
        sh2 = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh2).ellipse([ecx - eye_r, eye_cy - eye_r - S(6),
                                     ecx + eye_r, eye_cy + eye_r - S(30)], fill=200)
        sh2 = ImageChops.multiply(sh2.filter(ImageFilter.GaussianBlur(S(20))), emask)
        spr.paste(Image.new("RGBA", (W, H), (8, 9, 12, 255)), (0, 0), sh2)
        # bottom rim light
        rim = Image.new("L", (W, H), 0)
        ImageDraw.Draw(rim).ellipse([ecx - eye_r + S(8), eye_cy - eye_r + S(30),
                                     ecx + eye_r - S(8), eye_cy + eye_r + S(4)], outline=180, width=S(10))
        rim = ImageChops.multiply(rim.filter(ImageFilter.GaussianBlur(S(9))), emask)
        spr.paste(Image.new("RGBA", (W, H), (58, 64, 74, 255)), (0, 0), rim)
        # green glow halo
        gl = Image.new("L", (W, H), 0)
        ImageDraw.Draw(gl).ellipse([ecx - S(46), eye_cy - S(46), ecx + S(46), eye_cy + S(46)], fill=255)
        gl = ImageChops.multiply(gl.filter(ImageFilter.GaussianBlur(S(30))), emask)
        spr.paste(Image.new("RGBA", (W, H), GREEN + (255,)), (0, 0), ImageChops.multiply(
            gl, Image.new("L", (W, H), 150)))
        # green dot core
        dot = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dot)
        dd.ellipse([ecx - dot_r, eye_cy - dot_r, ecx + dot_r, eye_cy + dot_r], fill=GREEN + (255,))
        dd.ellipse([ecx - dot_r + S(6), eye_cy - dot_r + S(4), ecx + S(6), eye_cy + S(6)], fill=GREEN_HI + (255,))
        spr = None  # placeholder
        return dot
    # composite sockets (need spr mutable; do inline)
    for ecx in (lx, rx):
        emask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(emask).ellipse([ecx - eye_r, eye_cy - eye_r, ecx + eye_r, eye_cy + eye_r], fill=255)
        spr.paste(Image.new("RGBA", (W, H), (20, 23, 28, 255)), (0, 0), emask)
        sh2 = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh2).ellipse([ecx - eye_r, eye_cy - eye_r - S(6),
                                     ecx + eye_r, eye_cy + eye_r - S(34)], fill=220)
        sh2 = ImageChops.multiply(sh2.filter(ImageFilter.GaussianBlur(S(22))), emask)
        spr.paste(Image.new("RGBA", (W, H), (7, 8, 11, 255)), (0, 0), sh2)
        rim = Image.new("L", (W, H), 0)
        ImageDraw.Draw(rim).ellipse([ecx - eye_r + S(8), eye_cy - eye_r + S(34),
                                     ecx + eye_r - S(8), eye_cy + eye_r + S(6)], outline=180, width=S(11))
        rim = ImageChops.multiply(rim.filter(ImageFilter.GaussianBlur(S(9))), emask)
        spr.paste(Image.new("RGBA", (W, H), (56, 62, 72, 255)), (0, 0), rim)
        gl = Image.new("L", (W, H), 0)
        ImageDraw.Draw(gl).ellipse([ecx - S(50), eye_cy - S(50), ecx + S(50), eye_cy + S(50)], fill=170)
        gl = ImageChops.multiply(gl.filter(ImageFilter.GaussianBlur(S(30))), emask)
        spr.paste(Image.new("RGBA", (W, H), GREEN + (255,)), (0, 0), gl)
        d = ImageDraw.Draw(spr)
        d.ellipse([ecx - dot_r, eye_cy - dot_r, ecx + dot_r, eye_cy + dot_r], fill=GREEN + (255,))
        d.ellipse([ecx - dot_r + S(7), eye_cy - dot_r + S(5), ecx + S(5), eye_cy + S(7)], fill=GREEN_HI + (255,))

    spr = spr.resize((CW, CH), Image.LANCZOS)
    spr.save(os.path.join(_HERE, "logo_icon.png"))
    print("logo_icon.png saved", spr.size)

if __name__ == "__main__":
    build()
