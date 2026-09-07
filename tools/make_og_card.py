"""Render the 1200x630 link-preview card.

This is the only part of the site that reaches someone who never opens the link —
it is what renders in a LinkedIn post, a Slack paste or a forwarded email. It
follows the page's own rules: paper ground, one hairline, ink type, and the single
red accent used exactly once, on the +55 deg C limit tick.

Runs with or without the portrait; the face is added when the file exists.
"""
from PIL import Image, ImageDraw, ImageFont
import pathlib

MEDIA = pathlib.Path(r"E:\cowork\thermal-portfolio\assets\media")
FONTS = pathlib.Path(r"C:\Windows\Fonts")

W, H = 1200, 630
PAPER = (242, 243, 244)
PANEL = (255, 255, 255)
INK = (22, 24, 26)
INK45 = (130, 135, 140)
INK20 = (199, 203, 206)
CORRECTION = (204, 42, 30)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


f_name = font("arialbd.ttf", 78)
f_role = font("arial.ttf", 30)
f_mono = font("consola.ttf", 23) if (FONTS / "consola.ttf").exists() else font("arial.ttf", 23)
f_small = font("arial.ttf", 25)

card = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(card)

portrait_path = MEDIA / "portrait.jpg"
has_face = portrait_path.exists()

# Left rule echoes the page's hanging margin.
MARGIN = 76
text_x = MARGIN

if has_face:
    # Portrait sits flush left in a white plate with a hairline, as on the page.
    box_w, box_h = 300, 400
    face = Image.open(portrait_path).convert("RGB")
    # cover-crop to 3:4, biased toward the head
    target = box_w / box_h
    src = face.width / face.height
    if src > target:
        nw = int(face.height * target)
        left = (face.width - nw) // 2
        face = face.crop((left, 0, left + nw, face.height))
    else:
        nh = int(face.width / target)
        top = int((face.height - nh) * 0.22)
        face = face.crop((0, top, face.width, top + nh))
    face = face.resize((box_w, box_h), Image.LANCZOS)

    plate_x, plate_y = MARGIN, (H - box_h) // 2
    d.rectangle([plate_x - 11, plate_y - 11, plate_x + box_w + 10, plate_y + box_h + 10],
                fill=PANEL, outline=INK20)
    card.paste(face, (plate_x, plate_y))
    d.rectangle([plate_x, plate_y, plate_x + box_w - 1, plate_y + box_h - 1], outline=INK20)
    text_x = plate_x + box_w + 66

d.text((text_x, 214), "Prince Chauhan", font=f_name, fill=INK)
d.text((text_x, 316), "Thermal engineer \u00b7 Bengaluru", font=f_role, fill=INK45)

# The operating envelope, drawn the way the page draws it.
y = 404
x0, x1 = text_x, min(W - MARGIN, text_x + 470)
d.line([(x0, y), (x1, y)], fill=INK, width=2)
d.polygon([(x0, y), (x0 + 13, y - 7), (x0 + 13, y + 7)], fill=INK)
d.polygon([(x1, y), (x1 - 13, y - 7), (x1 - 13, y + 7)], fill=INK)
d.line([(x1, y - 14), (x1, y + 14)], fill=CORRECTION, width=4)   # the one accent
d.text((x0, y + 22), "\u221210 \u00b0C", font=f_mono, fill=INK45)
d.text((x1 - 76, y + 22), "+55 \u00b0C", font=f_mono, fill=INK45)

d.text((text_x, 492), "Liquid-cooled battery & charger systems", font=f_small, fill=INK)

# Baseline rule, as on the footer.
d.line([(0, H - 5), (W, H - 5)], fill=INK20, width=2)

out = MEDIA / "og-card.jpg"
card.save(out, "JPEG", quality=90, optimize=True)
print(f"og-card.jpg  {card.size}  {out.stat().st_size // 1024} KB  face={'yes' if has_face else 'no (type only)'}")
