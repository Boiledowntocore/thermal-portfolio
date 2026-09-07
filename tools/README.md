# Image pipeline

Run from anywhere; the scripts use absolute paths into `assets/media/`.
Requires Pillow (`pip install Pillow`). ImageMagick is **not** installed on this
machine — do not write scripts that shell out to `magick` or `convert` (the only
`convert.exe` on PATH is the Windows NTFS tool, which will do something unrelated
and confusing).

| Script | What it does | When to re-run |
|---|---|---|
| `grade_photos.py` | Crops the certificate above its signatory block, then resizes and compresses. Colour is preserved | After adding or replacing any photograph |
| `make_og_card.py` | Renders `assets/media/og-card.jpg`, the 1200×630 link-preview card | After the portrait lands, or if the name/positioning line changes |
| `reink_svgs.py` | One-off: converted the six schematics from the old dark theme to light line art | Already applied. Only needed if restoring from `assets/media/_dark-backup/` |

## The photo rule

**Photographs are full colour.** They were desaturated for a while, on the
argument that the page rations colour to a single accent (`--correction` red,
about five appearances) and a saturated certificate becomes a competing accent.
Prince overruled that on 2026-09-07 and the reasoning holds up: the schematics
are still pure black line art, which is what actually carries the drawing-set
character, and a page whose job is to get someone hired is the wrong place to
drain the warmth out of a face.

Do not silently re-apply a greyscale grade. If it ever comes back it should be a
deliberate decision, not a tidy-up.

Run `grade_photos.py` after adding any photograph so sizes and compression stay
consistent.

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
