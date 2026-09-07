# Image pipeline

Run from anywhere; the scripts use absolute paths into `assets/media/`.
Requires Pillow (`pip install Pillow`). ImageMagick is **not** installed on this
machine — do not write scripts that shell out to `magick` or `convert` (the only
`convert.exe` on PATH is the Windows NTFS tool, which will do something unrelated
and confusing).

| Script | What it does | When to re-run |
|---|---|---|
| `grade_photos.py` | Crops the certificate above its signatory block and grades **every** photograph to the same cool greyscale | After adding or replacing any photograph |
| `make_og_card.py` | Renders `assets/media/og-card.jpg`, the 1200×630 link-preview card | After the portrait lands, or if the name/positioning line changes |
| `reink_svgs.py` | One-off: converted the six schematics from the old dark theme to light line art | Already applied. Only needed if restoring from `assets/media/_dark-backup/` |

## The photo law

Every photograph on this site is greyscale. This is not a style preference — the
page rations colour to a single accent (`--correction` red, about five
appearances). A saturated gold certificate and a warm trophy shot were becoming a
second and third accent and quietly breaking that discipline.

Grading them identically also means there is **one** rule for photographs rather
than one rule per image, and it drops the SUN Mobility logo on the certificate to
a neutral value, which the sanitization boundary wants anyway.

If you add a photograph, run `grade_photos.py`. Do not hand-place a colour image.

## Adding the portrait

1. Save the original (full colour, any size, portrait orientation) to
   `assets/media/raw/portrait.jpg`
2. `python tools/grade_photos.py` — writes the graded `assets/media/portrait.jpg`
3. `python tools/make_og_card.py` — rebuilds the link card with the face in it

The page injects the portrait only after confirming the file loads, so it is safe
to deploy before the photograph exists — no gap, no broken-image icon.

## The certificate

`award-certificate.jpg` is cropped **above** the signatory block. The signature,
the company seal and the signing colleague's name and title are out of frame —
not painted over. Nothing is fabricated; what is withheld is simply not shown.
If you re-crop it, keep that boundary: a handwritten signature should not be
republished, and the colleague did not consent to appearing here.
