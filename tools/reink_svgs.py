"""Re-ink the portfolio SVGs from the old dark theme to the Plate Set light theme.

Colour is removed as an information channel (spec: encode flow with arrowheads and
linetype, not hue), so the chilled-coolant runs get a dash pattern before the
palette collapses to ink.
"""
import re
import pathlib

MEDIA = pathlib.Path(r"E:\cowork\thermal-portfolio\assets\media")

INK = "#16181a"
INK70 = "#4a4e52"
INK45 = "#82878c"
INK20 = "#c7cbce"
GRID = "#e9ebec"
PANEL = "#ffffff"
CORRECTION = "#cc2a1e"

COLOR_MAP = {
    # surfaces -> white plate
    "#141d29": PANEL, "#1a2431": PANEL, "#10171f": PANEL,
    "#0e151d": PANEL, "#132132": PANEL, "#1c1410": PANEL,
    # grid
    "#121a24": GRID,
    # borders
    "#2b3646": INK, "#33404f": INK20, "#39485a": INK20, "#3a4757": INK20,
    # text
    "#eef2f7": INK, "#cdd9e5": INK,
    "#8493a5": INK45, "#6d7f93": INK45, "#6f7f92": INK45,
    "#5c6b7c": INK45, "#9fb0c3": INK45, "#c3c2b7": INK45,
    "#55636f": INK20,
    # flow accents collapse to ink
    "#22b8e6": INK, "#f2a53c": INK, "#1f7fb8": INK, "#16357a": INK,
    # findings keep the single accent
    "#f6d27a": CORRECTION,
    # charts: rated/datasheet = ink, measured = correction
    "#3987e5": INK, "#3a6ea0": INK,
    "#d95926": CORRECTION, "#d0654e": CORRECTION,
    "#a4503c": CORRECTION, "#c58b7c": CORRECTION,
    "#e9b7a8": "#f0d9d5",
}


def reink(path):
    s = path.read_text(encoding="utf-8")

    # 1. Chilled-coolant runs become dashed while they are still identifiable by hue.
    s = re.sub(
        r'(stroke="#22b8e6"\s+stroke-width="3")(?![^>]*stroke-dasharray)',
        r'\1 stroke-dasharray="11 6"',
        s,
    )

    # 2. Drop the dark page ground and the cyan->amber gradient rule.
    s = re.sub(r'\s*<rect width="1000" height="560" fill="#0a0e14"/>', "", s)
    s = re.sub(r'\s*<rect[^>]*fill="url\(#therm\)"[^>]*/>', "", s)
    s = re.sub(r'\s*<linearGradient id="therm".*?</linearGradient>', "", s, flags=re.S)

    # 3. Collapse the palette.
    for old, new in COLOR_MAP.items():
        s = re.sub(re.escape(old), new, s, flags=re.I)

    # 4. Type: the page face, and mono stays mono.
    s = s.replace("'Inter', system-ui, -apple-system, sans-serif",
                  "Archivo, 'Helvetica Neue', Arial, sans-serif")

    # 5. Fan blades and similar solid accent fills read as smudges once inked;
    #    open them up so they stay line art.
    s = s.replace(f'<g fill="{INK}" opacity="0.85">',
                  f'<g fill="none" stroke="{INK}" stroke-width="1.25">')

    path.write_text(s, encoding="utf-8")
    return path.name


for name in ["prawaas-loop.svg", "architecture-loop.svg", "ctms-loop.svg",
             "sor-states.svg", "btms-capacity.svg", "rectifier-derating.svg"]:
    print("re-inked", reink(MEDIA / name))
