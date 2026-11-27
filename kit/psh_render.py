"""Plata Sin Humo carousel renderer v2 (portadas rotativas).
Usage: python3 psh_render.py FONT OUTDIR SPEC.json

Portadas: la portada rota entre 4 variantes para que el feed no sea un bloque naranja.
A "orange": fondo naranja, texto negro (la clásica).
B "ink": fondo negro, cifra naranja gigante centrada, etiqueta naranja arriba.
C "bone": fondo hueso, tarjeta negra con la cifra en naranja (efecto recibo).
D "split": mitad superior naranja (pregunta), mitad inferior negra (cifra).
Si el slide trae "variant" se usa esa; si no, se toma por el número de día: (day-1) % 4.
El naranja siempre está presente (fondo, cifra o etiqueta): la marca no se pierde.
"""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont

FONT, OUT, SPEC = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(OUT, exist_ok=True)
W, H, M = 1080, 1350, 96
ORANGE, INK, BONE, GREY, LINE = "#FF5B1F", "#121212", "#F2EEE6", "#6B6B6B", "#CFC9BD"
BG = {"orange": ORANGE, "ink": INK, "bone": BONE}
FG = {"orange": INK, "ink": BONE, "bone": INK}
ACC = {"orange": INK, "ink": ORANGE, "bone": ORANGE}
VARIANTS = ["orange", "ink", "bone", "split"]

def font(size, weight=800):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight, 100])
    return f

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for word in text.split(" "):
        test = (cur + " " + word).strip()
        if d.textlength(test, font=f) <= maxw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def block(d, x, y, text, f, fill, maxw=W - 2 * M, lh=1.1, align="left"):
    for para in text.split("\n"):
        if not para:
            y += int(f.size * lh * 0.6); continue
        for line in wrap(d, para, f, maxw):
            lx = x
            if align == "center":
                lx = x + (maxw - d.textlength(line, font=f)) / 2
            d.text((lx, y), line, font=f, fill=fill)
            y += int(f.size * lh)
    return y

def text_h(d, text, f, maxw, lh=1.1):
    n = 0
    for para in text.split("\n"):
        n += len(wrap(d, para, f, maxw)) if para else 0.6
    return int(n * f.size * lh)

def fit_big(d, text, maxw, start=250, floor=80):
    s = start
    while s > floor and d.textlength(text, font=font(s, 900)) > maxw:
        s -= 6
    return font(s, 900)

def footer(d, n, total, fg):
    f = font(26, 800)
    d.text((M, H - 92), "PLATA SIN HUMO", font=f, fill=fg)
    t = f"{n}/{total}"
    d.text((W - M - d.textlength(t, font=f), H - 92), t, font=f, fill=fg)

def pill(d, x, y, text, bg, fg, size=30):
    f = font(size, 900)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((x, y, x + tw + 48, y + size + 30), radius=(size + 30) // 2, fill=bg)
    d.text((x + 24, y + 13), text, font=f, fill=fg)
    return y + size + 30

def _orange_draw(d, s, y0):
    fg = INK
    y = y0
    if s.get("tag"):
        y = pill(d, M, y, s["tag"].upper(), INK, ORANGE) + 50
    y = block(d, M, y, s["pre"], font(64, 800), fg) + 60
    if s.get("lead"):
        y = block(d, M, y, s["lead"], font(70, 900), fg, lh=1.05) + 10
    fb = fit_big(d, s["big"], W - 2 * M + 16)
    d.text((M - 8, y), s["big"], font=fb, fill=fg); y += int(fb.size * 1.15)
    y = block(d, M, y, s["post"], font(52, 700), fg)
    return y

def cover_orange(d, s):
    dry = ImageDraw.Draw(Image.new("RGB", (W, H)))
    end = _orange_draw(dry, s, 140)
    content = end - 140
    y0 = max(140, (H - 160 - content) // 2)
    _orange_draw(d, s, y0)
    return INK

def cover_ink(d, s):
    y = 150
    if s.get("tag"):
        y = pill(d, M, y, s["tag"].upper(), ORANGE, INK) + 50
    fpre = font(56, 800)
    y = block(d, M, y, s["pre"], fpre, BONE, lh=1.12) + 30
    if s.get("lead"):
        y = block(d, M, y, s["lead"], font(44, 700), "#BDB7AA", lh=1.1) + 10
    fb = fit_big(d, s["big"], W - 2 * M + 16, start=300)
    bh = int(fb.size * 1.1)
    fpost = font(50, 800)
    ph = text_h(d, s["post"], fpost, W - 2 * M, 1.15)
    top = max(y + 30, (H - 140 - (bh + 40 + ph)) // 2 + 60)
    d.line((M, top - 30, M + 160, top - 30), fill=ORANGE, width=8)
    d.text((M - 8, top), s["big"], font=fb, fill=ORANGE)
    block(d, M, top + bh + 40, s["post"], fpost, BONE, lh=1.15)
    return BONE

def cover_bone(d, s):
    y = 150
    if s.get("tag"):
        y = pill(d, M, y, s["tag"].upper(), ORANGE, INK) + 50
    y = block(d, M, y, s["pre"], font(60, 800), INK, lh=1.12) + 50
    fb = fit_big(d, s["big"], W - 2 * M - 120, start=240)
    lead = s.get("lead", "")
    flead = font(40, 700)
    card_h = 90 + (text_h(d, lead, flead, W - 2 * M - 120) + 24 if lead else 0) + int(fb.size * 1.1) + 70
    d.rounded_rectangle((M, y, W - M, y + card_h), radius=36, fill=INK)
    cy = y + 60
    if lead:
        cy = block(d, M + 60, cy, lead, flead, "#BDB7AA", maxw=W - 2 * M - 120) + 24
    d.text((M + 52, cy), s["big"], font=fb, fill=ORANGE)
    y = y + card_h + 50
    block(d, M, y, s["post"], font(50, 800), INK, lh=1.15)
    return INK

def cover_split(d, s):
    cut = s.get("cut", 640)
    d.rectangle((0, 0, W, cut), fill=ORANGE)
    d.rectangle((0, cut, W, H), fill=INK)
    y = 150
    if s.get("tag"):
        y = pill(d, M, y, s["tag"].upper(), INK, ORANGE) + 50
    y = block(d, M, y, s["pre"], font(62, 900), INK, lh=1.1)
    if s.get("lead"):
        block(d, M, y + 30, s["lead"], font(44, 700), INK, lh=1.1)
    fb = fit_big(d, s["big"], W - 2 * M + 16, start=260)
    y2 = cut + 90
    d.text((M - 8, y2), s["big"], font=fb, fill=ORANGE)
    y2 += int(fb.size * 1.12)
    block(d, M, y2, s["post"], font(50, 800), BONE, lh=1.15)
    return BONE

COVERS = {"orange": cover_orange, "ink": cover_ink, "bone": cover_bone, "split": cover_split}

def render(s, n, total, day=1):
    k = s["type"]
    if k == "cover":
        v = s.get("variant") or VARIANTS[(day - 1) % 4]
        base = {"orange": ORANGE, "ink": INK, "bone": BONE, "split": INK}[v]
        im = Image.new("RGB", (W, H), base); d = ImageDraw.Draw(im)
        fg = COVERS[v](d, s)
        footer(d, n, total, fg)
        return im
    bg = s.get("bg", "bone")
    im = Image.new("RGB", (W, H), BG[bg]); d = ImageDraw.Draw(im)
    fg, acc = FG[bg], ACC[bg]
    if k == "statement":
        y = s.get("y", 300)
        y = block(d, M, y, s["a"], font(s.get("size", 78), 900), fg) + 60
        if s.get("b"):
            block(d, M, y, s["b"], font(s.get("size", 78), 900), acc)
    elif k == "rows":
        y = 150
        y = block(d, M, y, s["title"], font(62, 900), fg) + 60
        for label, val, hi in s["rows"]:
            fl = font(44, 700)
            fv = font(s.get("vsize", 110), 900)
            vh = fv.size
            d.text((M, y + vh * 0.35), label, font=fl, fill=fg)
            d.text((W - M - d.textlength(val, font=fv), y), val, font=fv, fill=acc if hi else fg)
            y += int(vh * 1.3)
            d.line((M, y - 14, W - M, y - 14), fill=LINE if bg == "bone" else "#3A3A3A", width=3)
        if s.get("note"):
            block(d, M, y + 40, s["note"], font(54, 900), fg)
    elif k == "cards":
        y = 150
        y = block(d, M, y, s["title"], font(60, 900), fg) + 50
        for label, left, right, hi in s["cards"]:
            cbg, cfg = (ORANGE, INK) if hi else (INK, BONE)
            d.rounded_rectangle((M, y, W - M, y + 230), radius=24, fill=cbg)
            d.text((M + 44, y + 36), label, font=font(44, 800), fill=cfg)
            fl = font(s.get("lsize", 84), 900)
            d.text((M + 44, y + 104), left, font=fl, fill=cfg)
            d.text((W - M - 44 - d.textlength(right, font=fl), y + 104), right, font=fl, fill=cfg)
            y += 262
        if s.get("legend"):
            d.text((M, y + 6), s["legend"], font=font(34, 700), fill=GREY)
    elif k == "bigstat":
        y = s.get("y", 220)
        y = block(d, M, y, s["pre"], font(64, 800), fg) + 60
        fb = fit_big(d, s["big"], W - 2 * M + 16)
        d.text((M - 8, y), s["big"], font=fb, fill=acc); y += int(fb.size * 1.2)
        block(d, M, y, s["post"], font(64, 900), fg)
    elif k == "steps":
        y = 140
        y = block(d, M, y, s["title"], font(62, 900), fg) + 50
        for i, txt in enumerate(s["steps"], 1):
            d.ellipse((M, y + 4, M + 76, y + 80), fill=ORANGE)
            fn = font(48, 900); t = str(i)
            d.text((M + 38 - d.textlength(t, font=fn) / 2, y + 12), t, font=fn, fill=INK)
            y = block(d, M + 110, y + 6, txt, font(s.get("tsize", 42), 700), fg, maxw=W - 2 * M - 110, lh=1.2) + 48
        if s.get("box"):
            fb = font(38, 800)
            lines = wrap(d, s["box"], fb, W - 2 * M - 80)
            hgt = 68 + len(lines) * int(38 * 1.2)
            d.rounded_rectangle((M, y, W - M, y + hgt), radius=20, fill=INK)
            block(d, M + 40, y + 34, s["box"], fb, BONE, maxw=W - 2 * M - 80, lh=1.2)
    elif k == "assumptions":
        y = 240
        y = block(d, M, y, "Sin humo: así hicimos la cuenta", font(64, 900), fg) + 60
        y = block(d, M, y, s["text"], font(42, 600), fg, lh=1.3) + 60
        block(d, M, y, "Contenido educativo. No es asesoría financiera personalizada.", font(32, 600), GREY, lh=1.3)
    elif k == "cta":
        y = 300
        y = block(d, M, y, s["a"], font(76, 900), fg) + 80
        block(d, M, y, s["b"], font(48, 700), fg, lh=1.2)
    footer(d, n, total, fg)
    return im

if __name__ == "__main__":
    spec = json.load(open(SPEC))
    for day in spec:
        slides = day["slides"]
        for i, s in enumerate(slides, 1):
            render(s, i, len(slides), day["day"]).save(os.path.join(OUT, f"dia{day['day']:02d}-{i:02d}.png"))
        sheet = Image.new("RGB", (4 * 280 + 10, 2 * 348 + 10), "white")
        for i in range(len(slides)):
            im = Image.open(os.path.join(OUT, f"dia{day['day']:02d}-{i+1:02d}.png")).resize((270, 338))
            sheet.paste(im, (10 + (i % 4) * 280, 10 + (i // 4) * 348))
        sheet.save(os.path.join(OUT, f"sheet-{day['day']:02d}.jpg"), quality=80)
