"""Render LinkedIn profile photo + banner in the portfolio's visual language.

The point is continuity: a recruiter who sees the LinkedIn header and then opens
the site should recognise the same system — cool grey ground, ink line art, the
operating envelope, and exactly one red mark at the design limit.

Banner is 1584x396 (LinkedIn's 4:1). Two layout constraints drive the design:
  * the profile photo punches a circle out of the lower LEFT, so nothing
    meaningful may sit there;
  * mobile crops the banner in from both sides, so the payload is kept toward
    the centre rather than flush right.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

MEDIA = pathlib.Path(r"E:\cowork\thermal-portfolio\assets\media")
RAW = MEDIA / "raw"
OUT = MEDIA / "linkedin"
OUT.mkdir(exist_ok=True)
FONTS = pathlib.Path(r"C:\Windows\Fonts")

PAPER = (242, 243, 244)
INK = (22, 24, 26)
INK45 = (130, 135, 140)
INK20 = (199, 203, 206)
GRID = (233, 235, 236)
CORRECTION = (204, 42, 30)


def f(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


# ---------------------------------------------------------------- profile photo
src = next((p for e in ("jpg", "jpeg", "png", "webp") for p in RAW.glob(f"portrait.{e}")), None)
if not src:
    raise SystemExit("no raw/portrait.* found")

im = Image.open(src).convert("RGB")
W, H = im.size

# Square crop centred on the face. The face sits high in this frame, so the box
# is anchored near the top with a little headroom rather than centred vertically
# — a centred crop would put his chin in the middle of the circle.
side = min(W, H)
left = (W - side) // 2
top = int(H * 0.04)
if top + side > H:
    top = H - side
face = im.crop((left, top, left + side, top + side)).resize((800, 800), Image.LANCZOS)
face.save(OUT / "profile-photo.jpg", "JPEG", quality=92, optimize=True, subsampling=0)
print("profile-photo.jpg   800x800  %d KB" % ((OUT / "profile-photo.jpg").stat().st_size // 1024))

# ---------------------------------------------------------------------- banner
BW, BH = 1584, 396
b = Image.new("RGB", (BW, BH), PAPER)
d = ImageDraw.Draw(b)

# 8px quadrille, as inside the figure plates. Kept very light so it reads as
# paper texture rather than as a chart.
for x in range(0, BW, 24):
    d.line([(x, 0), (x, BH)], fill=GRID)
for y in range(0, BH, 24):
    d.line([(0, y), (BW, y)], fill=GRID)

f_big = f("arialbd.ttf", 38)
f_mid = f("arial.ttf", 21)
f_mono = f("consola.ttf", 19) if (FONTS / "consola.ttf").exists() else f("arial.ttf", 19)
f_small = f("consola.ttf", 17) if (FONTS / "consola.ttf").exists() else f("arial.ttf", 17)

CX = 980          # optical centre, pushed right of the profile-photo circle
x0, x1 = CX - 355, CX + 325
y = 232           # sits low enough that the block reads centred, not top-heavy

# --- statement ---------------------------------------------------------------
line = "Liquid-cooled battery & charger thermal systems"
w = d.textlength(line, font=f_big)
d.text((CX - w / 2, y - 148), line, font=f_big, fill=INK)

# --- the operating envelope, drawn as a real dimension line -------------------
span = "65 \u00b0C"
w = d.textlength(span, font=f_mid)
d.text((CX - w / 2, y - 62), span, font=f_mid, fill=INK)

d.line([(x0, y), (x1, y)], fill=INK, width=3)
d.polygon([(x0, y), (x0 + 16, y - 9), (x0 + 16, y + 9)], fill=INK)
d.polygon([(x1, y), (x1 - 16, y - 9), (x1 - 16, y + 9)], fill=INK)
d.line([(x0, y - 26), (x0, y + 26)], fill=INK20, width=2)
d.line([(x1, y - 26), (x1, y + 26)], fill=INK20, width=2)
# the single red mark: the +55 C design limit
d.line([(x1, y - 30), (x1, y + 30)], fill=CORRECTION, width=5)

d.text((x0 - 4, y + 30), "-10 \u00b0C", font=f_mono, fill=INK45)
d.text((x1 - 66, y + 30), "+55 \u00b0C", font=f_mono, fill=INK45)

# --- measurement scale along the base -----------------------------------------
# Fills the lower band with something that means something rather than padding,
# and starts right of x=430 so the profile-photo circle never sits on top of it.
sy = BH - 58
for i, sx in enumerate(range(440, BW - 30, 22)):
    major = i % 5 == 0
    d.line([(sx, sy), (sx, sy + (14 if major else 7))],
           fill=INK20 if major else GRID, width=2 if major else 1)

# --- portfolio URL, above the scale on the right ------------------------------
url = "princechauhan-thermal.github.io"
w = d.textlength(url, font=f_small)
d.text((BW - w - 40, sy - 34), url, font=f_small, fill=INK45)

# --- baseline rule, echoing the site footer ----------------------------------
d.line([(0, BH - 3), (BW, BH - 3)], fill=INK20, width=3)

b.save(OUT / "banner.jpg", "JPEG", quality=92, optimize=True, subsampling=0)
print("banner.jpg          1584x396  %d KB" % ((OUT / "banner.jpg").stat().st_size // 1024))

# ------------------------------------------------- how they actually appear
# LinkedIn circle-crops the photo and overlays it on the banner's lower left.
# Rendering that composite is the only way to check the two do not collide.
prev = b.copy()
D = 232
circ = face.resize((D, D), Image.LANCZOS)
mask = Image.new("L", (D * 4, D * 4), 0)
ImageDraw.Draw(mask).ellipse([0, 0, D * 4 - 1, D * 4 - 1], fill=255)
mask = mask.resize((D, D), Image.LANCZOS)
ring = Image.new("RGB", (D + 10, D + 10), (255, 255, 255))
rmask = Image.new("L", ((D + 10) * 4, (D + 10) * 4), 0)
ImageDraw.Draw(rmask).ellipse([0, 0, (D + 10) * 4 - 1, (D + 10) * 4 - 1], fill=255)
rmask = rmask.resize((D + 10, D + 10), Image.LANCZOS)
prev.paste(ring, (108, BH - 150), rmask)
prev.paste(circ, (113, BH - 145), mask)
prev.save(OUT / "preview-composite.jpg", "JPEG", quality=90, optimize=True)
print("preview-composite.jpg  (banner + circular photo as LinkedIn renders it)")
