#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cyberpunk — Abdalla Tech GPU repair promo (1080x1080), neon glitch HUD."""
import math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

S = 1080
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
CF = os.environ.get("FONTS_DIR", os.path.join(_HERE, "fonts"))
def F(n,s): return ImageFont.truetype(f"{CF}/{n}", s)

PINK=(255,42,138); CYAN=(0,238,255); YEL=(250,232,18)
WHITE=(236,243,255); MUTE=(140,120,180); DIM=(0,150,175)
P_DARK=(18,12,32); P_DK2=(24,16,42)

# ---- background: deep purple→black + corner nebulas ----
c0=np.array((14,9,26),float); c1=np.array((4,3,10),float)
g=(c0[None,:]+(c1-c0)[None,:]*np.linspace(0,1,S)[:,None])
img=Image.fromarray(np.repeat(g[:,None,:],S,axis=1).astype(np.uint8),"RGB")
def nebula(cx,cy,r,col,inten):
    global img
    m=Image.new("L",(S,S),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=inten)
    m=m.filter(ImageFilter.GaussianBlur(160))
    img=ImageChops.screen(img, Image.composite(Image.new("RGB",(S,S),col),Image.new("RGB",(S,S),(0,0,0)),m))
nebula(120,120,360,PINK,110); nebula(980,180,360,CYAN,110); nebula(540,980,420,(120,40,200),90)

def neon(drawfn, passes=(22,12,6), core=True):
    global img
    layer=Image.new("RGB",(S,S),(0,0,0)); dl=ImageDraw.Draw(layer); drawfn(dl)
    for gg in passes: img=ImageChops.screen(img, layer.filter(ImageFilter.GaussianBlur(gg)))
    if core: img=ImageChops.screen(img, layer)

def cham(box,c):
    x0,y0,x1,y1=box
    return [(x0+c,y0),(x1,y0),(x1,y1-c),(x1-c,y1),(x0,y1),(x0,y0+c)]
def fillp(pts,col): ImageDraw.Draw(img).polygon(pts,fill=col)
def tracked(dl,x,y,text,font,fill,tr):
    for ch in text: dl.text((x,y),ch,font=font,fill=fill); x+=dl.textlength(ch,font=font)+tr
def twidth(text,font,tr):
    d=ImageDraw.Draw(img); return sum(d.textlength(c,font=font)+tr for c in text)-tr

# ================= HUD corner brackets =================
def bracket(cx,cy,fx,fy,col):
    L=42
    neon(lambda dl:(dl.line([(cx,cy),(cx+fx*L,cy)],fill=col,width=4),
                    dl.line([(cx,cy),(cx,cy+fy*L)],fill=col,width=4)), passes=(10,5))
for (cx,cy,fx,fy,col) in [(70,70,1,1,CYAN),(S-70,70,-1,1,PINK),(70,S-70,1,-1,PINK),(S-70,S-70,-1,-1,CYAN)]:
    bracket(cx,cy,fx,fy,col)

# ================= HEADER =================
brand=F("BigShoulders-Bold.ttf",60); tag=F("JetBrainsMono-Bold.ttf",20); mono=F("JetBrainsMono-Regular.ttf",19)
bx,by=100,112
# logo: chamfered chip, cyan neon border, pink core mark
lp=cham([bx,by,bx+78,by+78],14); fillp(lp,P_DK2)
neon(lambda dl: dl.line(lp+[lp[0]],fill=CYAN,width=3), passes=(14,7))
neon(lambda dl: dl.rectangle([bx+22,by+22,bx+56,by+56],fill=PINK), passes=(12,6))
# brand with chromatic aberration
btxt="ABDALLA TECH"; hx=bx+104; hy=by+2
d=ImageDraw.Draw(img)
tracked(d,hx-4,hy,btxt,brand,PINK,2); tracked(d,hx+4,hy,btxt,brand,CYAN,2); tracked(d,hx,hy,btxt,brand,WHITE,2)
tracked(d,hx+3,hy+56,"ASSISTÊNCIA TÉCNICA GAMER",tag,DIM,3)
# right mono + barcode
tw=twidth("SYS.GPU // REPAIR",mono,1)
tracked(d,S-100-tw,by+8,"SYS.GPU // REPAIR",mono,CYAN,1)
bxr=S-100-150
for i,wd in enumerate([3,1,2,1,4,1,2,3,1,2,1,3,2,1,4,1,2,1,3,1,2]):
    col=WHITE if i%2==0 else P_DARK
    d.rectangle([bxr,by+40,bxr+wd,by+58],fill=col); bxr+=wd+2
# neon divider
neon(lambda dl: dl.line([(100,214),(S-100,214)],fill=PINK,width=3), passes=(16,8))
d=ImageDraw.Draw(img); d.rectangle([100,210,240,218],fill=CYAN)

# ================= CENTER PANEL =================
pnl=cham([140,286,940,616],36); fillp(pnl,(12,9,24))
# inner tech grid
d=ImageDraw.Draw(img)
for gx in range(160,940,44): d.line([(gx,300),(gx,602)],fill=(30,22,52),width=1)
for gy in range(304,616,44): d.line([(150,gy),(930,gy)],fill=(30,22,52),width=1)
neon(lambda dl: dl.line(pnl+[pnl[0]],fill=CYAN,width=3), passes=(20,10))

# ---- GPU ----
sh=cham([238,332,842,560],24); fillp(sh,(20,13,38))
neon(lambda dl: dl.line(sh+[sh[0]],fill=PINK,width=3), passes=(16,8))
# top power connectors
d=ImageDraw.Draw(img)
for px in (700,772):
    pc=cham([px,320,px+58,344],6); d.polygon(pc,fill=P_DK2)
    neon(lambda dl,pc=pc: dl.line(pc+[pc[0]],fill=DIM,width=2), passes=(6,))
# PCIe connector — yellow neon
conn=cham([305,560,615,590],8); fillp(conn,(30,26,6))
neon(lambda dl: dl.line(conn+[conn[0]],fill=YEL,width=2), passes=(10,5))
d=ImageDraw.Draw(img)
for tx in range(318,608,15): d.line([(tx,572),(tx,590)],fill=(120,110,20),width=3)
# fans
def fan(cx,cy,r):
    neon(lambda dl: dl.ellipse([cx-r,cy-r,cx+r,cy+r],outline=CYAN,width=3), passes=(14,7))
    dd=ImageDraw.Draw(img)
    for k in range(9):
        a=math.radians(k*40); a2=a+0.7
        dd.line([(cx+(r-15)*math.cos(a),cy+(r-15)*math.sin(a)),(cx+22*math.cos(a2),cy+22*math.sin(a2))],
                fill=(0,120,140),width=6)
    neon(lambda dl: dl.ellipse([cx-16,cy-16,cx+16,cy+16],outline=YEL,width=3), passes=(8,4))
    ImageDraw.Draw(img).ellipse([cx-6,cy-6,cx+6,cy+6],fill=YEL)
fan(398,446,80); fan(682,446,80)
d=ImageDraw.Draw(img); d.line([(540,352),(540,540)],fill=(40,30,66),width=2)
# HUD label + reticle on panel
tracked(d,610,336,"DIAG//OK",mono,CYAN,2)
neon(lambda dl:(dl.ellipse([876,300,912,336],outline=PINK,width=2),
                dl.line([(894,296),(894,340)],fill=PINK,width=1),
                dl.line([(872,318),(916,318)],fill=PINK,width=1)), passes=(8,4))
d=ImageDraw.Draw(img); tracked(d,168,596,"0x1F.GPU",mono,DIM,2)

# ================= HEADLINE (chromatic aberration) =================
def cyber_center(y,text,path,start,core,tr=1,split=6,glow=None):
    s=start
    while s>10:
        f=F(path,s); w=twidth(text,f,tr)
        if w<=884: break
        s-=2
    x=(S-w)/2
    if glow: neon(lambda dl,f=f,x=x: tracked(dl,x,y,text,f,glow,tr), passes=(18,9), core=False)
    d=ImageDraw.Draw(img)
    tracked(d,x-split,y,text,f,PINK,tr); tracked(d,x+split,y,text,f,CYAN,tr); tracked(d,x,y,text,f,core,tr)
cyber_center(636,"REPARO DE PLACAS","BigShoulders-Bold.ttf",132,WHITE,split=6)
cyber_center(636+118,"DE VÍDEO","BigShoulders-Bold.ttf",132,YEL,split=7,glow=PINK)

# glitch slivers framing the headline (not crossing letters)
d=ImageDraw.Draw(img)
d.rectangle([100, 620, 360, 624], fill=CYAN)          # short, upper-left
d.rectangle([S-360, 892, S-100, 896], fill=PINK)      # short, lower-right
d.rectangle([S-230, 626, S-100, 629], fill=YEL)       # tiny accent upper-right

# ================= SUPPORT LINE =================
sub=F("JetBrainsMono-Bold.ttf",23)
st="[ NÃO LIGA ]  [ ARTEFATOS ]  [ SUPERAQUECE ]  [ TRAVA ]"
sw=twidth(st,sub,0); d.text(((S-sw)/2,876),st,font=sub,fill=CYAN)

# ================= CTA — yellow angular bar =================
cta=cham([250,930,830,1006],20)
neon(lambda dl: dl.polygon(cta,fill=YEL), passes=(20,10), core=False)  # yellow glow halo
fillp(cta,YEL)
d=ImageDraw.Draw(img)
# thin pink edge accent
d.line(cta+[cta[0]],fill=(255,255,255),width=1)
# whatsapp handset (black on yellow)
gcx,gcy,gr=316,968,26
d.ellipse([gcx-gr,gcy-gr,gcx+gr,gcy+gr],fill=(12,9,20))
ic=Image.new("RGBA",(72,72),(0,0,0,0)); di=ImageDraw.Draw(ic)
di.line([(24,24),(48,48)],fill=YEL+(255,),width=14); di.ellipse([12,12,34,34],fill=YEL+(255,)); di.ellipse([38,38,60,60],fill=YEL+(255,))
di.ellipse([21,21,29,29],fill=(12,9,20,255)); di.ellipse([47,47,55,55],fill=(12,9,20,255))
ic=ic.rotate(-12,resample=Image.BICUBIC,center=(36,36)); img.paste(ic,(gcx-36,gcy-36),ic)
d=ImageDraw.Draw(img)
num=F("BigShoulders-Bold.ttf",64)
d.text((gcx+gr+20,gcy-40),"16 99973-0151",font=num,fill=(12,9,20))

# caption
cap=F("JetBrainsMono-Regular.ttf",19)
ct="> ORÇAMENTO SEM COMPROMISSO · ENVIE FOTOS NO WHATSAPP"
cw=twidth(ct,cap,0); d.text(((S-cw)/2,1028),ct,font=cap,fill=MUTE)

# ================= scanlines =================
arr=np.asarray(img).astype(np.float32)
arr[0::3,:,:]*=0.82
img=Image.fromarray(np.clip(arr,0,255).astype(np.uint8),"RGB")

img.save(os.path.join(_HERE, "abdalla-tech-reparo-gpu-cyber.png"))
print("saved")
