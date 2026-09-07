"""One photo law for the whole document: photographs are greyscale.

The page rations colour to a single accent (--correction red, ~5 appearances).
A saturated gold certificate and a warm trophy shot were quietly becoming a
second and third accent, and a greyscale portrait alongside them would have left
two contradictory rules for the same class of object. Grading every photograph
the same way restores the discipline — and drops the SUN Mobility logo back to a
neutral value, which the sanitization boundary wants anyway.

Slightly cool-tinted rather than neutral grey so the images sit with --paper
#f2f3f4 instead of floating warm against it.
"""
from PIL import Image, ImageEnhance, ImageOps
import pathlib

MEDIA = pathlib.Path(r"E:\cowork\thermal-portfolio\assets\media")
RAW = MEDIA / "raw"

# a hair cooler than neutral, matching the paper's blue lean
COOL_BLACK = (14, 16, 18)
COOL_WHITE = (250, 251, 252)


def grade(im, contrast=1.06):
    g = ImageOps.grayscale(im)
    g = ImageEnhance.Contrast(g).enhance(contrast)
    return ImageOps.colorize(g, black=COOL_BLACK, white=COOL_WHITE).convert("RGB")


def emit(src_img, out_name, max_w, quality=86):
    im = src_img
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    im = grade(im)
    out = MEDIA / out_name
    im.save(out, "JPEG", quality=quality, optimize=True)
    print(f"{out_name:26} {im.size}  {out.stat().st_size // 1024} KB")


# Certificate: re-crop from the original so the grade is applied once, not twice.
cert = Image.open(RAW / "recognition.webp").convert("RGB").crop((205, 140, 1352, 667))
emit(cert, "award-certificate.jpg", 1147)

trophy = Image.open(RAW / "trophy.webp").convert("RGB")
emit(trophy, "award-trophy.jpg", 900)

# Portrait. Accept whatever extension it was saved with; the page always
# references portrait.jpg, so the graded output is normalised to that.
portrait_src = next((p for ext in ("jpg", "jpeg", "png", "webp")
                     for p in RAW.glob(f"portrait.{ext}")), None)
if portrait_src:
    emit(Image.open(portrait_src).convert("RGB"), "portrait.jpg", 768)
else:
    print("portrait.jpg           -- not yet saved to raw/, skipped")
