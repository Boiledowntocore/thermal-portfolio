"""Three lower-text banner options, rendered with the profile circle overlaid.

The circle matters: LinkedIn punches it out of the lower left, so a banner can
only be judged as a composite. Each variant drops the headline sentence and
leans harder on the drawing.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

MEDIA = pathlib.Path(r"E:\cowork\thermal-portfolio\assets\media")
RAW = MEDIA / "raw"
OUT = MEDIA / "linkedin"
OUT.mkdir(exist_ok=True)
FONTS = pathlib.Path(r"C:\Windows\Fonts")

BW, BH = 1584, 396
PAPER = (242, 243, 244)
INK = (22, 24, 26)
INK45 = (130, 135, 140)
INK20 = (199, 203, 206)
GRID = (233, 235, 236)
RED = (204, 42, 30)
URL = "princechauhan-thermal.github.io"


def f(n, s):
    return ImageFont.truetype(str(FONTS / n), s)


MONO = "consola.ttf" if (FONTS / "consola.ttf").exists() else "arial.ttf"


def ground():
    b = Image.new("RGB", (BW, BH), PAPER)
    d = ImageDraw.Draw(b)
    for x in range(0, BW, 24):
        d.line([(x, 0), (x, BH)], fill=GRID)
    for y in range(0, BH, 24):
        d.line([(0, y), (BW, y)], fill=GRID)
    d.line([(0, BH - 3), (BW, BH - 3)], fill=INK20, width=3)
    return b, d


def url_mark(d, y=None):
    fs = f(MONO, 17)
    w = d.textlength(URL, font=fs)
    d.text((BW - w - 40, y or BH - 46), URL, font=fs, fill=INK45)


# ── A. Envelope only ─────────────────────────────────────────────────────────
def variant_a():
    b, d = ground()
    CX, y = 980, 200
    x0, x1 = CX - 400, CX + 380
    fm, fs = f("arial.ttf", 24), f(MONO, 22)

    w = d.textlength("65 °C", font=fm)
    d.text((CX - w / 2, y - 68), "65 °C", font=fm, fill=INK)
    d.line([(x0, y), (x1, y)], fill=INK, width=4)
    d.polygon([(x0, y), (x0 + 18, y - 10), (x0 + 18, y + 10)], fill=INK)
    d.polygon([(x1, y), (x1 - 18, y - 10), (x1 - 18, y + 10)], fill=INK)
    d.line([(x0, y - 30), (x0, y + 30)], fill=INK20, width=2)
    d.line([(x1, y - 34), (x1, y + 34)], fill=RED, width=6)
    d.text((x0 - 6, y + 36), "-10 °C", font=fs, fill=INK45)
    d.text((x1 - 78, y + 36), "+55 °C", font=fs, fill=INK45)
    url_mark(d)
    return b


# ── B. Coolant loop, drawing only ────────────────────────────────────────────
def variant_b():
    b, d = ground()
    fs = f(MONO, 16)
    L, R, T, Bm, r = 620, 1400, 120, 290, 46

    # Racetrack. PIL measures arc angles clockwise from 3 o'clock, and each
    # corner's bounding box is the 2r square tucked into that corner.
    def loop():
        d.line([(L + r, T), (R - r, T)], fill=INK, width=3)
        d.line([(L + r, Bm), (R - r, Bm)], fill=INK, width=3)
        d.line([(L, T + r), (L, Bm - r)], fill=INK, width=3)
        d.line([(R, T + r), (R, Bm - r)], fill=INK, width=3)
        for box, s, e in (((L, T, L + 2 * r, T + 2 * r), 180, 270),
                          ((R - 2 * r, T, R, T + 2 * r), 270, 360),
                          ((R - 2 * r, Bm - 2 * r, R, Bm), 0, 90),
                          ((L, Bm - 2 * r, L + 2 * r, Bm), 90, 180)):
            d.arc(box, s, e, fill=INK, width=3)

    loop()
    # flow direction, top run left-to-right and bottom run right-to-left
    for (ax, ay, dx) in ((940, T, 1), (1080, Bm, -1)):
        d.polygon([(ax + 16 * dx, ay), (ax - 7 * dx, ay - 10), (ax - 7 * dx, ay + 10)], fill=INK)

    # Unlabelled blocks: the shapes read as a loop without spending any words.
    for (cx, cy) in ((770, T), (1250, T), (1010, Bm)):
        d.rectangle([cx - 58, cy - 25, cx + 58, cy + 25],
                    fill=(255, 255, 255), outline=INK, width=3)

    # one red mark: the limit the loop is designed against
    d.line([(R, T + r - 28), (R, T + r + 28)], fill=RED, width=6)
    url_mark(d)
    return b


# ── C. Two numbers, nothing else ─────────────────────────────────────────────
def variant_c():
    b, d = ground()
    fb = f("arialbd.ttf", 84)
    fs = f(MONO, 19)
    txt_l, txt_r = "-10", "+55 °C"
    wl = d.textlength(txt_l, font=fb)
    wr = d.textlength(txt_r, font=fb)
    gap = 150                              # room for the arrow between them
    block = wl + gap + wr + 22             # +22 for the red limit tick
    x = 980 - block / 2                    # centred clear of the photo circle
    y = 150

    d.text((x, y), txt_l, font=fb, fill=INK)
    ax0, ax1 = x + wl + 42, x + wl + gap - 20
    d.line([(ax0, y + 54), (ax1, y + 54)], fill=INK, width=4)
    d.polygon([(ax1, y + 54), (ax1 - 22, y + 42), (ax1 - 22, y + 66)], fill=INK)

    xr = x + wl + gap
    d.text((xr, y), txt_r, font=fb, fill=INK)
    d.line([(xr + wr + 16, y + 8), (xr + wr + 16, y + 96)], fill=RED, width=7)

    cap = "operating envelope"
    wc = d.textlength(cap, font=fs)
    d.text((980 - wc / 2, y + 122), cap, font=fs, fill=INK45)
    url_mark(d)
    return b


# ── composite sheet ──────────────────────────────────────────────────────────
src = next((p for e in ("jpg", "jpeg", "png", "webp") for p in RAW.glob(f"portrait.{e}")), None)
im = Image.open(src).convert("RGB")
side = min(im.size)
face = im.crop(((im.width - side) // 2, int(im.height * 0.04),
                (im.width - side) // 2 + side, int(im.height * 0.04) + side))

D = 232
circ = face.resize((D, D), Image.LANCZOS)
mask = Image.new("L", (D * 4, D * 4), 0)
ImageDraw.Draw(mask).ellipse([0, 0, D * 4 - 1, D * 4 - 1], fill=255)
mask = mask.resize((D, D), Image.LANCZOS)
ringm = Image.new("L", ((D + 10) * 4,) * 2, 0)
ImageDraw.Draw(ringm).ellipse([0, 0, (D + 10) * 4 - 1, (D + 10) * 4 - 1], fill=255)
ringm = ringm.resize((D + 10, D + 10), Image.LANCZOS)
ring = Image.new("RGB", (D + 10, D + 10), (255, 255, 255))

variants = [("A", variant_a()), ("B", variant_b()), ("C", variant_c())]
LBL = 44
sheet = Image.new("RGB", (BW, (BH + LBL) * 3), (255, 255, 255))
sd = ImageDraw.Draw(sheet)
fl = f("arialbd.ttf", 24)

for i, (name, img) in enumerate(variants):
    img.save(OUT / f"banner-{name}.jpg", "JPEG", quality=92, optimize=True, subsampling=0)
    comp = img.copy()
    comp.paste(ring, (108, BH - 150), ringm)
    comp.paste(circ, (113, BH - 145), mask)
    top = i * (BH + LBL)
    sd.text((24, top + 12), {"A": "A — envelope only", "B": "B — loop drawing, no words",
                             "C": "C — two numbers"}[name], font=fl, fill=(20, 20, 20))
    sheet.paste(comp, (0, top + LBL))

sheet.save(OUT / "banner-options.jpg", "JPEG", quality=88, optimize=True)
print("wrote banner-A/B/C.jpg and banner-options.jpg")
