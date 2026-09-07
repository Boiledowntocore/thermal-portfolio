"""Prepare the site's photographs: crop, resize, compress. Colour is preserved.

HISTORY / DO NOT "FIX" THIS BACK:
An earlier version desaturated every photograph to keep the page's single red
accent unique. Prince asked for colour (2026-09-07) and that decision stands —
a colourless portfolio reads cold, and the photographs are the one place on a
hiring page where warmth is worth spending contrast on. The schematics are still
pure black line art, so the drawing-set character survives without the grade.

The certificate crop is NOT an aesthetic choice and must be preserved:
it cuts above the signatory block so a colleague's handwritten signature, the
company seal, and her name and title stay out of frame. Nothing is painted over
— what is withheld is simply not photographed into the crop.
"""
from PIL import Image
import pathlib

MEDIA = pathlib.Path(r"E:\cowork\thermal-portfolio\assets\media")
RAW = MEDIA / "raw"

# Cut line found by scanning for the topmost seal ink; see git history.
CERT_CROP = (205, 140, 1352, 667)


def emit(im, out_name, max_w, quality=88):
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    out = MEDIA / out_name
    im.save(out, "JPEG", quality=quality, optimize=True, subsampling=0)
    print(f"{out_name:26} {im.size}  {out.stat().st_size // 1024} KB")


cert = Image.open(RAW / "recognition.webp").convert("RGB").crop(CERT_CROP)
emit(cert, "award-certificate.jpg", 1147)

emit(Image.open(RAW / "trophy.webp").convert("RGB"), "award-trophy.jpg", 900)

portrait_src = next((p for ext in ("jpg", "jpeg", "png", "webp")
                     for p in RAW.glob(f"portrait.{ext}")), None)
if portrait_src:
    emit(Image.open(portrait_src).convert("RGB"), "portrait.jpg", 768)
else:
    print("portrait.jpg           -- not found in raw/, skipped")
