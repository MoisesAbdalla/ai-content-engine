#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Abdalla Tech — Carrossel Instagram (1080x1350, 4:5)
Cuidados com impressora de jato de tinta. Estilo: escuro + limpo, acento neon."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1080, 1350
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = _HERE
os.makedirs(OUT, exist_ok=True)
CF = os.environ.get("FONTS_DIR", os.path.join(_HERE, "..", "fonts"))
def F(n, s): return ImageFont.truetype(f"{CF}/{n}", s)

# palette
CYAN  = (0, 224, 255)
PINK  = (255, 66, 150)
AMBER = (255, 186, 66)
WHITE = (238, 244, 255)
MUTE  = (150, 160, 192)
DIM   = (96, 104, 140)
INK   = (14, 11, 26)

M = 92  # side margin

# ---------- shared helpers ----------
def base_bg():
    c0 = np.array((20, 15, 38), float); c1 = np.array((7, 6, 16), float)
    g = c0[None, :] + (c1 - c0)[None, :] * np.linspace(0, 1, H)[:, None]
    im = Image.fromarray(np.repeat(g[:, None, :], W, axis=1).astype(np.uint8), "RGB")
    def nebula(cx, cy, r, col, inten):
        nonlocal im
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=inten)
        m = m.filter(ImageFilter.GaussianBlur(190))
        im = ImageChops.screen(im, Image.composite(
            Image.new("RGB", (W, H), col), Image.new("RGB", (W, H), (0, 0, 0)), m))
    nebula(970, 120, 420, CYAN, 60)
    nebula(120, 1250, 460, PINK, 55)
    return im

def glow(img, drawfn, passes=(16, 8), core=True):
    layer = Image.new("RGB", (W, H), (0, 0, 0)); dl = ImageDraw.Draw(layer); drawfn(dl)
    for g in passes:
        img = ImageChops.screen(img, layer.filter(ImageFilter.GaussianBlur(g)))
    if core:
        img = ImageChops.screen(img, layer)
    return img

def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines

def cham(box, c):
    x0, y0, x1, y1 = box
    return [(x0 + c, y0), (x1, y0), (x1, y1 - c), (x1 - c, y1), (x0, y1), (x0, y0 + c)]

def scanlines(img, factor=0.9):
    arr = np.asarray(img).astype(np.float32)
    arr[0::3, :, :] *= factor
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")

# ---------- header / footer ----------
def header(img, counter, accent=CYAN):
    d = ImageDraw.Draw(img)
    bx, by = M, 74
    lp = cham([bx, by, bx + 56, by + 56], 11)
    d.polygon(lp, fill=(26, 20, 46))
    img = glow(img, lambda dl: dl.line(lp + [lp[0]], fill=CYAN, width=3), passes=(10, 5))
    d = ImageDraw.Draw(img)
    d.rectangle([bx + 17, by + 17, bx + 39, by + 39], fill=PINK)
    d.text((bx + 74, by - 2), "ABDALLA TECH", font=F("BigShoulders-Bold.ttf", 44), fill=WHITE)
    d.text((bx + 76, by + 40), "ASSISTÊNCIA TÉCNICA", font=F("JetBrainsMono-Bold.ttf", 15), fill=accent)
    # counter right
    cf = F("JetBrainsMono-Bold.ttf", 22)
    ct = counter
    d.text((W - M - d.textlength(ct, font=cf), by + 4), ct, font=cf, fill=accent)
    d.text((W - M - d.textlength("CARROSSEL", font=F("JetBrainsMono-Regular.ttf", 14)),
            by + 34), "CARROSSEL", font=F("JetBrainsMono-Regular.ttf", 14), fill=DIM)
    # divider
    img = glow(img, lambda dl: dl.line([(M, 168), (W - M, 168)], fill=accent, width=2), passes=(9, 4))
    d = ImageDraw.Draw(img); d.rectangle([M, 165, M + 120, 171], fill=PINK)
    return img

def footer(img, text=None):
    d = ImageDraw.Draw(img)
    y = 1272
    d.line([(M, y - 22), (W - M, y - 22)], fill=(40, 34, 62), width=1)
    lf = F("JetBrainsMono-Regular.ttf", 17)
    d.text((M, y), "IMPRESSORAS · JATO DE TINTA", font=lf, fill=DIM)
    rt = text or "WhatsApp  16 99973-0151"
    d.text((W - M - d.textlength(rt, font=F("JetBrainsMono-Bold.ttf", 17)), y),
           rt, font=F("JetBrainsMono-Bold.ttf", 17), fill=MUTE)
    return img

# ---------- icons (drawn inside a badge centered at cx,cy) ----------
def badge(img, cx, cy, accent, iconfn, r=94):
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(22, 17, 40))
    img = glow(img, lambda dl: dl.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent, width=4),
               passes=(12, 6))
    iconfn(img, cx, cy, accent)
    return img

def ic_printer(img, cx, cy, col):
    d = ImageDraw.Draw(img)
    d.rectangle([cx - 44, cy - 34, cx + 44, cy - 4], outline=col, width=5)      # top paper feed
    d.rounded_rectangle([cx - 52, cy - 8, cx + 52, cy + 34], 6, outline=col, width=5)  # body
    d.rectangle([cx - 32, cy + 30, cx + 32, cy + 52], outline=col, width=5)     # output paper
    d.line([(cx - 26, cy + 40), (cx + 20, cy + 40)], fill=col, width=4)
    d.ellipse([cx + 30, cy + 6, cx + 40, cy + 16], fill=col)                    # led
    return img

def ic_calendar(img, cx, cy, col):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - 42, cy - 34, cx + 42, cy + 40], 8, outline=col, width=5)
    d.line([(cx - 42, cy - 12), (cx + 42, cy - 12)], fill=col, width=5)
    d.line([(cx - 24, cy - 46), (cx - 24, cy - 26)], fill=col, width=6)
    d.line([(cx + 24, cy - 46), (cx + 24, cy - 26)], fill=col, width=6)
    for gx in (-22, 0, 22):
        d.ellipse([cx + gx - 5, cy + 6, cx + gx + 5, cy + 16], fill=col)
    return img

def ic_power(img, cx, cy, col):
    d = ImageDraw.Draw(img)
    d.arc([cx - 34, cy - 30, cx + 34, cy + 38], start=300, end=240, fill=col, width=6)
    d.line([(cx, cy - 44), (cx, cy - 2)], fill=col, width=6)
    return img

def ic_drop_warn(img, cx, cy, col):
    d = ImageDraw.Draw(img)
    # ink drop
    d.polygon([(cx - 6, cy - 40), (cx + 20, cy + 4), (cx - 32, cy + 4)], fill=None, outline=col, width=5)
    d.pieslice([cx - 32, cy - 20, cx + 20, cy + 30], 0, 180, outline=col, width=5)
    # warning bang
    d.line([(cx + 30, cy - 6), (cx + 30, cy + 16)], fill=AMBER, width=6)
    d.ellipse([cx + 26, cy + 24, cx + 34, cy + 32], fill=AMBER)
    return img

def ic_bottle(img, cx, cy, col):
    d = ImageDraw.Draw(img)
    d.rectangle([cx - 10, cy - 44, cx + 10, cy - 30], outline=col, width=5)     # cap
    d.rounded_rectangle([cx - 24, cy - 28, cx + 24, cy + 44], 10, outline=col, width=5)  # body
    d.rectangle([cx - 24, cy + 8, cx + 24, cy + 44], fill=col)                  # ink level
    d.rounded_rectangle([cx - 24, cy + 8, cx + 24, cy + 44], 10, fill=col)
    return img

def ic_nozzle(img, cx, cy, col):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx - 44, cy - 40, cx + 44, cy + 44], 8, outline=col, width=5)
    for i, gx in enumerate(range(-30, 40, 20)):
        top = cy - 26 if i % 2 == 0 else cy - 12
        d.line([(cx + gx, top), (cx + gx, cy + 30)], fill=col, width=6)
    return img

def ic_shield(img, cx, cy, col):
    d = ImageDraw.Draw(img)
    d.polygon([(cx, cy - 46), (cx + 38, cy - 28), (cx + 38, cy + 8),
               (cx, cy + 46), (cx - 38, cy + 8), (cx - 38, cy - 28)],
              outline=col, width=5)
    d.line([(cx - 16, cy), (cx - 4, cy + 16)], fill=col, width=6)
    d.line([(cx - 4, cy + 16), (cx + 20, cy - 14)], fill=col, width=6)
    return img

# ---------- big ghost number ----------
def ghost_number(img, txt, accent):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(layer)
    f = F("BigShoulders-Bold.ttf", 430)
    tw = dl.textlength(txt, font=f)
    dl.text((W - M - tw + 10, 150), txt, font=f, fill=accent + (34,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB"), (0, 0))
    return img

# ================= SLIDE BUILDERS =================
def slide_cover():
    img = base_bg()
    img = header(img, "01 / 08")
    d = ImageDraw.Draw(img)
    d.text((M, 236), "GUIA RÁPIDO · ASSISTÊNCIA", font=F("JetBrainsMono-Bold.ttf", 22), fill=CYAN)
    # headline
    hf = F("BigShoulders-Bold.ttf", 150)
    for i, ln in enumerate(["6 CUIDADOS", "COM A SUA", "IMPRESSORA"]):
        d.text((M - 4, 300 + i * 132), ln, font=hf, fill=WHITE)
    # accent word
    img = glow(img, lambda dl: dl.text((M - 4, 300 + 3 * 132), "DE JATO DE TINTA",
               font=F("BigShoulders-Bold.ttf", 96), fill=CYAN), passes=(14, 7), core=False)
    d = ImageDraw.Draw(img)
    d.text((M - 4, 300 + 3 * 132), "DE JATO DE TINTA", font=F("BigShoulders-Bold.ttf", 96), fill=CYAN)
    # subtitle
    sf = F("InstrumentSans-Regular.ttf", 34)
    sub = "Dicas simples pra ela durar muito mais e você não gastar com conserto."
    for i, ln in enumerate(wrap(d, sub, sf, W - 2 * M)):
        d.text((M, 870 + i * 46), ln, font=sf, fill=MUTE)
    # printer illustration
    img = badge(img, W - 210, 1035, CYAN, ic_printer, r=118)
    # arraste pill
    pill = cham([M, 1150, M + 300, 1216], 16)
    img = glow(img, lambda dl: dl.polygon(pill, outline=CYAN, width=3), passes=(12, 6))
    d = ImageDraw.Draw(img)
    d.text((M + 34, 1163), "ARRASTE", font=F("BigShoulders-Bold.ttf", 46), fill=WHITE)
    d.text((M + 214, 1160), "→", font=F("BigShoulders-Bold.ttf", 54), fill=CYAN)
    img = footer(img)
    return scanlines(img)

def slide_tip(num, counter, accent, iconfn, kicker, title_lines, body):
    img = base_bg()
    img = header(img, counter, accent)
    img = ghost_number(img, f"{num:02d}", accent)
    img = badge(img, M + 96, 330, accent, iconfn)
    d = ImageDraw.Draw(img)
    # kicker
    d.text((M + 214, 268), f"DICA {num:02d}", font=F("JetBrainsMono-Bold.ttf", 26), fill=accent)
    img = glow(img, lambda dl: dl.line([(M + 216, 312), (M + 470, 312)], fill=accent, width=3),
               passes=(8, 4))
    d = ImageDraw.Draw(img)
    kf = F("InstrumentSans-Bold.ttf", 24)
    d.text((M + 216, 330), kicker, font=kf, fill=MUTE)
    # title
    hf = F("BigShoulders-Bold.ttf", 118)
    ty = 560
    for ln in title_lines:
        d.text((M - 4, ty), ln, font=hf, fill=WHITE)
        ty += 104
    # accent underline
    img = glow(img, lambda dl: dl.line([(M, ty + 14), (M + 180, ty + 14)], fill=accent, width=6),
               passes=(12, 6))
    d = ImageDraw.Draw(img)
    # body
    bf = F("InstrumentSans-Regular.ttf", 37)
    by = ty + 66
    for ln in wrap(d, body, bf, W - 2 * M - 20):
        d.text((M, by), ln, font=bf, fill=(206, 214, 236))
        by += 52
    img = footer(img)
    return scanlines(img)

def slide_cta():
    img = base_bg()
    img = header(img, "08 / 08", PINK)
    d = ImageDraw.Draw(img)
    d.text((M, 240), "PRECISA DE AJUDA?", font=F("JetBrainsMono-Bold.ttf", 24), fill=PINK)
    hf = F("BigShoulders-Bold.ttf", 118)
    for i, ln in enumerate(["DEU PROBLEMA", "NA SUA", "IMPRESSORA?"]):
        d.text((M - 4, 292 + i * 104), ln, font=hf, fill=WHITE)
    # services list
    bf = F("InstrumentSans-Regular.ttf", 34)
    d.text((M, 640), "A gente resolve:", font=F("InstrumentSans-Bold.ttf", 34), fill=CYAN)
    items = ["Entupimento e cabeçote que não imprime",
             "Puxando papel errado ou atolando",
             "Erro de cartucho / não reconhece a tinta",
             "Impressão falhada, riscada ou desbotada"]
    for i, it in enumerate(items):
        y = 700 + i * 56
        d.ellipse([M, y + 10, M + 14, y + 24], fill=CYAN)
        d.text((M + 34, y), it, font=bf, fill=(210, 218, 238))
    # whatsapp bar
    bar = cham([M, 968, W - M, 1066], 20)
    img = glow(img, lambda dl: dl.polygon(bar, fill=(37, 211, 102)), passes=(20, 10), core=False)
    d = ImageDraw.Draw(img); d.polygon(bar, fill=(37, 211, 102))
    # handset glyph
    gcx, gcy = M + 58, 1017
    ic = Image.new("RGBA", (80, 80), (0, 0, 0, 0)); di = ImageDraw.Draw(ic)
    di.line([(26, 26), (54, 54)], fill=INK + (255,), width=16)
    di.ellipse([12, 12, 38, 38], fill=INK + (255,)); di.ellipse([42, 42, 68, 68], fill=INK + (255,))
    di.ellipse([22, 22, 32, 32], fill=(37, 211, 102, 255)); di.ellipse([48, 48, 58, 58], fill=(37, 211, 102, 255))
    ic = ic.rotate(-10, resample=Image.BICUBIC, center=(40, 40))
    img.paste(ic, (gcx - 40, gcy - 40), ic)
    d = ImageDraw.Draw(img)
    d.text((gcx + 44, 976), "16 99973-0151", font=F("BigShoulders-Bold.ttf", 76), fill=INK)
    # caption
    cf = F("InstrumentSans-Regular.ttf", 30)
    cap = "Chama no WhatsApp, manda uma foto do problema. Orçamento sem compromisso."
    for i, ln in enumerate(wrap(d, cap, cf, W - 2 * M)):
        d.text((M, 1110 + i * 42), ln, font=cf, fill=MUTE)
    img = footer(img, "Abdalla Tech · Assistência Técnica")
    return scanlines(img)

# ================= CONTENT =================
TIPS = [
    (1, "02 / 08", CYAN, ic_calendar, "Não deixe ela parada",
     ["IMPRIMA COM", "FREQUÊNCIA"],
     "Imprima pelo menos uma vez por semana, de preferência algo colorido. "
     "Parada por muito tempo, a tinta seca e entope os bicos do cabeçote."),
    (2, "03 / 08", CYAN, ic_power, "Deixe ela selar o cabeçote",
     ["DESLIGUE", "PELO BOTÃO"],
     "Sempre desligue no botão da própria impressora, nunca cortando direto na "
     "tomada ou no filtro de linha. Assim ela estaciona e protege o cabeçote."),
    (3, "04 / 08", AMBER, ic_drop_warn, "Nunca rode no seco",
     ["NÃO IMPRIMA", "SEM TINTA"],
     "Não imprima com o cartucho ou o tanque vazio nem quase no fim. Rodar seco "
     "superaquece e pode queimar o cabeçote, o conserto mais caro que existe."),
    (4, "05 / 08", CYAN, ic_bottle, "Tinta boa protege a máquina",
     ["USE TINTA", "DE QUALIDADE"],
     "Fuja de tinta muito barata e de origem duvidosa. Tinta ruim entope os bicos "
     "e mancha a folha. Use a tinta recomendada para o seu modelo."),
    (5, "06 / 08", CYAN, ic_nozzle, "Só quando realmente precisar",
     ["LIMPEZA NA", "MEDIDA CERTA"],
     "Notou falha ou risco na impressão? Rode o teste de bicos e a limpeza pelo "
     "software da impressora. Mas sem exagero: cada limpeza gasta muita tinta."),
    (6, "07 / 08", CYAN, ic_shield, "Ambiente e papel certos",
     ["CUIDE DO LOCAL", "E DO PAPEL"],
     "Mantenha a tampa fechada, longe de poeira, sol forte e calor. Use papel liso "
     "e sem dobras para não atolar e não danificar o rolo de tração."),
]

def main():
    slide_cover().save(f"{OUT}/slide_01.png")
    print("slide_01 (capa) ok")
    for t in TIPS:
        num, counter, accent, iconfn, kicker, title, body = t
        slide_tip(num, counter, accent, iconfn, kicker, title, body).save(
            f"{OUT}/slide_{num+1:02d}.png")
        print(f"slide_{num+1:02d} (dica {num}) ok")
    slide_cta().save(f"{OUT}/slide_08.png")
    print("slide_08 (cta) ok")

if __name__ == "__main__":
    main()
