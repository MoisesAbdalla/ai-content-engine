#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Abdalla Tech — Carrossel Instagram (1080x1350, 4:5)
Cuidados com impressora de jato de tinta.
Identidade oficial: gradiente verde escuro + acento esmeralda + circuitos."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1080, 1350
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = _HERE
os.makedirs(OUT, exist_ok=True)
CF = os.environ.get("FONTS_DIR", os.path.join(_HERE, "..", "fonts"))
def F(n, s): return ImageFont.truetype(f"{CF}/{n}", s)

# fonts
WORD  = "Tektur-Medium.ttf"          # wordmark / techy labels
HEAD  = "WorkSans-Bold.ttf"          # headlines
BODY  = "InstrumentSans-Regular.ttf"
BODYB = "InstrumentSans-Bold.ttf"
LAB   = "InstrumentSans-Regular.ttf"

# palette
GREEN = (46, 230, 118)
GRN_D = (24, 150, 84)
WHITE = (240, 246, 242)
GRAY  = (150, 166, 156)
DIM   = (96, 112, 104)
INK   = (9, 13, 11)

M = 92

# ---------------- official logo sprite ----------------
LOGO = Image.open(f"{OUT}/logo_icon.png").convert("RGBA")
# visible head bounds within sprite (fraction of canvas): left/right/bottom
VL, VR, VB = 78 / 720, 642 / 720, 452 / 600
def paste_logo(img, cx, cy, full_h):
    w = int(full_h * LOGO.width / LOGO.height)
    s = LOGO.resize((w, int(full_h)), Image.LANCZOS)
    img.paste(s, (int(cx - w / 2), int(cy - full_h / 2)), s)
    return w

# ---------------- text utils ----------------
_scratch = ImageDraw.Draw(Image.new("RGB", (10, 10)))
def tracked(d, x, y, text, font, fill, tr):
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tr
def tracked_w(text, font, tr):
    return sum(_scratch.textlength(c, font=font) + tr for c in text) - (tr if text else 0)
def ctracked(d, y, text, font, fill, tr):
    w = tracked_w(text, font, tr)
    tracked(d, (W - w) / 2, y, text, font, fill, tr)
def wrap(text, font, maxw):
    lines, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if _scratch.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines
def fit(path, lines, maxw, start, mins=44, tr=0):
    s = start
    while s > mins:
        f = F(path, s)
        if all(tracked_w(ln, f, tr) <= maxw for ln in lines):
            return f
        s -= 2
    return F(path, mins)
def cham(box, c):
    x0, y0, x1, y1 = box
    return [(x0 + c, y0), (x1, y0), (x1, y1 - c), (x1 - c, y1), (x0, y1), (x0, y0 + c)]

# ---------------- glow ----------------
def glow(img, drawfn, passes=(14, 7), core=True):
    layer = Image.new("RGB", (W, H), (0, 0, 0)); drawfn(ImageDraw.Draw(layer))
    for g in passes:
        img = ImageChops.screen(img, layer.filter(ImageFilter.GaussianBlur(g)))
    if core:
        img = ImageChops.screen(img, layer)
    return img

# ---------------- background ----------------
def base_bg():
    top = np.array((16, 22, 19), float); bot = np.array((9, 16, 13), float)
    g = top[None, :] + (bot - top)[None, :] * np.linspace(0, 1, H)[:, None]
    im = Image.fromarray(np.repeat(g[:, None, :], W, axis=1).astype(np.uint8), "RGB")
    # bottom-center emerald glow
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([W//2 - 620, H - 300, W//2 + 620, H + 520], fill=150)
    m = m.filter(ImageFilter.GaussianBlur(210))
    im = ImageChops.screen(im, Image.composite(
        Image.new("RGB", (W, H), (18, 92, 56)), Image.new("RGB", (W, H), (0, 0, 0)), m))
    # faint top-left glow
    m2 = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m2).ellipse([-260, -260, 360, 360], fill=70)
    m2 = m2.filter(ImageFilter.GaussianBlur(200))
    im = ImageChops.screen(im, Image.composite(
        Image.new("RGB", (W, H), (16, 70, 46)), Image.new("RGB", (W, H), (0, 0, 0)), m2))
    im = circuits(im)
    # corner vignette
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-320, -320, W + 320, H + 320], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(260))
    im = Image.composite(im, ImageChops.multiply(im, Image.new("RGB", (W, H), (150, 150, 150))),
                         vig)
    return im

def circuits(im):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    rng = np.random.default_rng(11)
    for _ in range(26):
        x = int(rng.integers(-40, W)); y = int(rng.integers(60, H - 60))
        a = int(rng.integers(14, 40))
        col = (46, 230, 118, a)
        length = int(rng.integers(70, 300))
        dirx = 1 if rng.random() < 0.5 else -1
        x2 = x + dirx * length
        d.line([(x, y), (x2, y)], fill=col, width=2)
        vy = int(rng.integers(35, 150)) * (1 if rng.random() < 0.5 else -1)
        d.line([(x2, y), (x2, y + vy)], fill=col, width=2)
        d.ellipse([x2 - 5, y + vy - 5, x2 + 5, y + vy + 5], outline=(46, 230, 118, a + 45), width=2)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(46, 230, 118, a))
    im = Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")
    return im

def scanlines(img, factor=0.94):
    arr = np.asarray(img).astype(np.float32)
    arr[0::3, :, :] *= factor
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")

# ---------------- brand logo (official sprite) ----------------
def wordmark_beside(img, x, cy, word_size, tr):
    """ABDALLA (white) with —TECH— (green) under it, left edge at x. Returns right edge."""
    d = ImageDraw.Draw(img)
    wf = F(WORD, word_size)
    aw = tracked_w("ABDALLA", wf, tr)
    ay = cy - word_size * 0.76
    tracked(d, x, ay, "ABDALLA", wf, WHITE, tr)
    tf = F(WORD, int(word_size * 0.46))
    tw = tracked_w("TECH", tf, tr + 3)
    ty = cy + word_size * 0.26
    tcx = x + (aw - tw) / 2
    tracked(d, tcx, ty, "TECH", tf, GREEN, tr + 3)
    ly = ty + word_size * 0.30
    d.line([(x, ly), (tcx - 12, ly)], fill=GRN_D, width=2)
    d.line([(tcx + tw + 12, ly), (x + aw, ly)], fill=GRN_D, width=2)
    return x + aw

def logo_cover(img, cx, cy_icon, full_h, word_size):
    iw = paste_logo(img, cx, cy_icon, full_h)
    head_bottom = cy_icon + (VB - 0.5) * full_h
    d = ImageDraw.Draw(img)
    tr = 4
    top = head_bottom + word_size * 0.34
    ctracked(d, top, "ABDALLA", F(WORD, word_size), WHITE, tr)
    tf = F(WORD, int(word_size * 0.5))
    ctracked(d, top + word_size * 1.02, "TECH", tf, GREEN, tr + 10)
    return img

# ---------------- header / footer ----------------
def header(img, counter):
    full_h = 100
    iw = full_h * LOGO.width / LOGO.height
    icx = M + (0.5 - VL) * iw
    paste_logo(img, icx, 106, full_h)
    redge = M + (VR - VL) * iw + 18
    wordmark_beside(img, redge, 108, 34, 2)
    d = ImageDraw.Draw(img)
    cf = F(WORD, 24)
    d.text((W - M - d.textlength(counter, font=cf), 90), counter, font=cf, fill=GREEN)
    lf = F(LAB, 14)
    d.text((W - M - d.textlength("CARROSSEL", font=lf), 122), "CARROSSEL", font=lf, fill=DIM)
    img = glow(img, lambda dl: dl.line([(M, 176), (W - M, 176)], fill=GREEN, width=2), passes=(8, 4))
    d = ImageDraw.Draw(img); d.rectangle([M, 173, M + 118, 179], fill=GREEN)
    return img

def footer(img, right=None):
    d = ImageDraw.Draw(img)
    y = 1274
    d.line([(M, y - 22), (W - M, y - 22)], fill=(38, 50, 44), width=1)
    d.text((M, y), "FRANCA / SP · JATO DE TINTA", font=F(LAB, 17), fill=DIM)
    rt = right or "WhatsApp  16 99973-0151"
    d.text((W - M - d.textlength(rt, font=F(BODYB, 17)), y), rt, font=F(BODYB, 17), fill=GRAY)
    return img

# ---------------- icons (line, green) ----------------
def badge(img, cx, cy, iconfn, r=90):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(19, 27, 23))
    img = glow(img, lambda dl: dl.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GREEN, width=4),
               passes=(11, 5))
    iconfn(ImageDraw.Draw(img), cx, cy)
    return img

def ic_printer(d, cx, cy):
    d.rectangle([cx - 42, cy - 32, cx + 42, cy - 4], outline=GREEN, width=5)
    d.rounded_rectangle([cx - 50, cy - 8, cx + 50, cy + 32], 6, outline=GREEN, width=5)
    d.rectangle([cx - 30, cy + 28, cx + 30, cy + 50], outline=GREEN, width=5)
    d.line([(cx - 24, cy + 38), (cx + 18, cy + 38)], fill=GREEN, width=4)
    d.ellipse([cx + 28, cy + 4, cx + 38, cy + 14], fill=GREEN)
def ic_calendar(d, cx, cy):
    d.rounded_rectangle([cx - 40, cy - 32, cx + 40, cy + 38], 8, outline=GREEN, width=5)
    d.line([(cx - 40, cy - 12), (cx + 40, cy - 12)], fill=GREEN, width=5)
    d.line([(cx - 22, cy - 44), (cx - 22, cy - 24)], fill=GREEN, width=6)
    d.line([(cx + 22, cy - 44), (cx + 22, cy - 24)], fill=GREEN, width=6)
    for gx in (-20, 0, 20):
        d.ellipse([cx + gx - 5, cy + 4, cx + gx + 5, cy + 14], fill=GREEN)
def ic_power(d, cx, cy):
    d.arc([cx - 32, cy - 28, cx + 32, cy + 36], start=300, end=240, fill=GREEN, width=6)
    d.line([(cx, cy - 42), (cx, cy - 2)], fill=GREEN, width=6)
def ic_drop_warn(d, cx, cy):
    d.pieslice([cx - 30, cy - 18, cx + 18, cy + 28], 0, 180, outline=GREEN, width=5)
    d.line([(cx - 6, cy - 38), (cx - 30, cy + 2)], fill=GREEN, width=5)
    d.line([(cx - 6, cy - 38), (cx + 18, cy + 2)], fill=GREEN, width=5)
    d.line([(cx + 30, cy - 8), (cx + 30, cy + 12)], fill=WHITE, width=6)
    d.ellipse([cx + 26, cy + 20, cx + 34, cy + 28], fill=WHITE)
def ic_bottle(d, cx, cy):
    d.rectangle([cx - 9, cy - 42, cx + 9, cy - 30], outline=GREEN, width=5)
    d.rounded_rectangle([cx - 22, cy - 28, cx + 22, cy + 42], 10, outline=GREEN, width=5)
    d.rounded_rectangle([cx - 22, cy + 8, cx + 22, cy + 42], 10, fill=GREEN)
def ic_nozzle(d, cx, cy):
    d.rounded_rectangle([cx - 42, cy - 38, cx + 42, cy + 42], 8, outline=GREEN, width=5)
    for i, gx in enumerate(range(-28, 38, 19)):
        top = cy - 24 if i % 2 == 0 else cy - 10
        d.line([(cx + gx, top), (cx + gx, cy + 28)], fill=GREEN, width=6)
def ic_shield(d, cx, cy):
    d.polygon([(cx, cy - 44), (cx + 36, cy - 26), (cx + 36, cy + 8),
               (cx, cy + 44), (cx - 36, cy + 8), (cx - 36, cy - 26)], outline=GREEN, width=5)
    d.line([(cx - 15, cy), (cx - 3, cy + 15)], fill=GREEN, width=6)
    d.line([(cx - 3, cy + 15), (cx + 19, cy - 13)], fill=GREEN, width=6)

def ghost_number(img, txt):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(layer)
    f = F(HEAD, 340)
    tw = dl.textlength(txt, font=f)
    dl.text((W - M - tw + 6, 210), txt, font=f, fill=GREEN + (26,))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

def lh_of(size, k=0.98):
    return int(size * k)

# ================= SLIDES =================
def slide_cover():
    img = base_bg()
    img = logo_cover(img, W / 2, 208, 252, 60)
    d = ImageDraw.Draw(img)
    lines = ["6 CUIDADOS COM", "A IMPRESSORA", "DE JATO DE TINTA"]
    cols = [WHITE, WHITE, GREEN]
    f = fit(HEAD, lines, W - 2 * M, 108)
    lh = lh_of(f.size, 1.06)
    y0 = 470
    if cols[2] == GREEN:
        img = glow(img, lambda dl: ctracked(dl, y0 + 2 * lh, lines[2], f, GREEN, 0),
                   passes=(13, 6), core=False)
        d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        ctracked(d, y0 + i * lh, ln, f, cols[i], 0)
    dy = y0 + 3 * lh + 26
    d.line([(W / 2 - 130, dy), (W / 2 + 130, dy)], fill=(70, 92, 82), width=3)
    ctracked(d, dy + 34, "PRA NÃO ENTUPIR E NÃO GASTAR COM CONSERTO", F(LAB, 27), GRAY, 1)
    ctracked(d, dy + 82, "REPARO ELETRÔNICO NÍVEL COMPONENTE · FRANCA / SP", F(BODYB, 22), GREEN, 1)
    ctracked(d, 1246, "arrasta para o lado  →", F(LAB, 30), GRAY, 1)
    img = footer(img)
    return scanlines(img)

def slide_tip(num, counter, iconfn, kicker, title_lines, body):
    img = base_bg()
    img = header(img, counter)
    img = ghost_number(img, f"{num:02d}")
    img = badge(img, M + 92, 336, iconfn)
    d = ImageDraw.Draw(img)
    d.text((M + 208, 280), f"DICA {num:02d}", font=F(WORD, 28), fill=GREEN)
    img = glow(img, lambda dl: dl.line([(M + 210, 328), (M + 470, 328)], fill=GREEN, width=3),
               passes=(7, 3))
    d = ImageDraw.Draw(img)
    d.text((M + 210, 346), kicker, font=F(BODYB, 24), fill=GRAY)
    f = fit(HEAD, title_lines, W - 2 * M, 92)
    lh = lh_of(f.size, 1.08)
    ty = 566
    for ln in title_lines:
        d.text((M, ty), ln, font=f, fill=WHITE)
        ty += lh
    uy = ty + 12
    img = glow(img, lambda dl: dl.line([(M + 3, uy), (M + 168, uy)], fill=GREEN, width=6),
               passes=(11, 5))
    d = ImageDraw.Draw(img)
    bf = F(BODY, 37)
    by = uy + 46
    for ln in wrap(body, bf, W - 2 * M - 20):
        d.text((M, by), ln, font=bf, fill=(206, 216, 210))
        by += 52
    img = footer(img)
    return scanlines(img)

def slide_cta():
    img = base_bg()
    img = header(img, "08 / 08")
    d = ImageDraw.Draw(img)
    d.text((M, 250), "PRECISA DE AJUDA?", font=F(WORD, 26), fill=GREEN)
    lines = ["DEU PROBLEMA", "NA SUA", "IMPRESSORA?"]
    f = fit(HEAD, lines, W - 2 * M, 96)
    lh = lh_of(f.size, 1.08)
    y0 = 306
    for i, ln in enumerate(lines):
        d.text((M, y0 + i * lh), ln, font=f, fill=WHITE if i < 2 else GREEN)
    yb = y0 + 3 * lh + 30
    d.text((M, yb), "A gente resolve:", font=F(BODYB, 34), fill=GREEN)
    items = ["Entupimento e cabeçote que não imprime",
             "Puxando papel errado ou atolando",
             "Erro de cartucho / não reconhece a tinta",
             "Impressão falhada, riscada ou desbotada"]
    bf = F(BODY, 33)
    for i, it in enumerate(items):
        y = yb + 54 + i * 54
        d.ellipse([M, y + 10, M + 14, y + 24], fill=GREEN)
        d.text((M + 34, y), it, font=bf, fill=(210, 220, 214))
    # whatsapp bar (brand green)
    bar_y = yb + 54 + 4 * 54 + 28
    bar = cham([M, bar_y, W - M, bar_y + 98], 20)
    img = glow(img, lambda dl: dl.polygon(bar, fill=GREEN), passes=(18, 9), core=False)
    d = ImageDraw.Draw(img); d.polygon(bar, fill=GREEN)
    gcx, gcy = M + 58, bar_y + 49
    ic = Image.new("RGBA", (80, 80), (0, 0, 0, 0)); di = ImageDraw.Draw(ic)
    di.line([(26, 26), (54, 54)], fill=INK + (255,), width=16)
    di.ellipse([12, 12, 38, 38], fill=INK + (255,)); di.ellipse([42, 42, 68, 68], fill=INK + (255,))
    di.ellipse([22, 22, 32, 32], fill=GREEN + (255,)); di.ellipse([48, 48, 58, 58], fill=GREEN + (255,))
    ic = ic.rotate(-10, resample=Image.BICUBIC, center=(40, 40))
    img.paste(ic, (gcx - 40, gcy - 40), ic)
    d = ImageDraw.Draw(img)
    d.text((gcx + 44, bar_y + 12), "16 99973-0151", font=F(HEAD, 62), fill=INK)
    cf = F(BODY, 30)
    cap = "Chama no WhatsApp e manda uma foto do problema. Orçamento sem compromisso."
    cy = bar_y + 128
    for ln in wrap(cap, cf, W - 2 * M):
        d.text((M, cy), ln, font=cf, fill=GRAY); cy += 42
    img = footer(img, "Abdalla Tech · Reparo Eletrônico")
    return scanlines(img)

TIPS = [
    (1, "02 / 08", ic_calendar, "Não deixe ela parada",
     ["IMPRIMA COM", "FREQUÊNCIA"],
     "Imprima pelo menos uma vez por semana, de preferência algo colorido. "
     "Parada por muito tempo, a tinta seca e entope os bicos do cabeçote."),
    (2, "03 / 08", ic_power, "Deixe ela selar o cabeçote",
     ["DESLIGUE PELO", "BOTÃO"],
     "Sempre desligue no botão da própria impressora, nunca cortando direto na "
     "tomada ou no filtro de linha. Assim ela estaciona e protege o cabeçote."),
    (3, "04 / 08", ic_drop_warn, "Nunca rode no seco",
     ["NÃO IMPRIMA", "SEM TINTA"],
     "Não imprima com o cartucho ou o tanque vazio nem quase no fim. Rodar seco "
     "superaquece e pode queimar o cabeçote, o conserto mais caro que existe."),
    (4, "05 / 08", ic_bottle, "Tinta boa protege a máquina",
     ["USE TINTA DE", "QUALIDADE"],
     "Fuja de tinta muito barata e de origem duvidosa. Tinta ruim entope os bicos "
     "e mancha a folha. Use a tinta recomendada para o seu modelo."),
    (5, "06 / 08", ic_nozzle, "Só quando realmente precisar",
     ["LIMPEZA NA", "MEDIDA CERTA"],
     "Notou falha ou risco na impressão? Rode o teste de bicos e a limpeza pelo "
     "software da impressora. Mas sem exagero: cada limpeza gasta muita tinta."),
    (6, "07 / 08", ic_shield, "Ambiente e papel certos",
     ["CUIDE DO LOCAL", "E DO PAPEL"],
     "Mantenha a tampa fechada, longe de poeira, sol forte e calor. Use papel liso "
     "e sem dobras para não atolar e não danificar o rolo de tração."),
]

def main():
    slide_cover().save(f"{OUT}/slide_01.png"); print("capa ok")
    for t in TIPS:
        num, counter, iconfn, kicker, title, body = t
        slide_tip(num, counter, iconfn, kicker, title, body).save(f"{OUT}/slide_{num+1:02d}.png")
        print(f"dica {num} ok")
    slide_cta().save(f"{OUT}/slide_08.png"); print("cta ok")

if __name__ == "__main__":
    main()
