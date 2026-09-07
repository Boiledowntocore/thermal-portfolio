"""Re-ink the schematics from the ORIGINAL dark sources, keeping hot/cold apart.

Why from _dark-backup/ rather than the live files: the first re-ink flattened
every stroke to one ink colour, which destroyed the only record of which run was
warm and which was chilled. The dark originals still carry that information as
authored colour (#f2a53c warm, #22b8e6 chilled), so they are the reliable source
for tagging. Re-running this on the already-flattened files would tag nothing.

Output is light line art where colour means exactly one thing on a loop plate:
  red   = hot coolant
  blue  = chilled coolant
  grey  = heat rejected to air
Everything structural stays ink. The charts (FIG 3 / FIG 5) keep --correction red
for the measured finding; no plate contains both a coolant run and a chart, so
the two reds never share a frame.
"""
import re
import pathlib

MEDIA = pathlib.Path(r"E:\cowork\thermal-portfolio\assets\media")
SRC = MEDIA / "_dark-backup"

INK = "#16181a"
INK45 = "#82878c"
INK20 = "#c7cbce"
GRID = "#e9ebec"
PANEL = "#ffffff"
CORRECTION = "#cc2a1e"

HOT = "#c62f1e"     # warm coolant
COLD = "#1f6fb2"    # chilled coolant

CROP_TOP, FULL_H = 82, 560

BASE_MAP = {
    "#141d29": PANEL, "#1a2431": PANEL, "#10171f": PANEL,
    "#0e151d": PANEL, "#132132": PANEL, "#1c1410": PANEL,
    "#121a24": GRID,
    "#2b3646": INK, "#33404f": INK20, "#39485a": INK20, "#3a4757": INK20,
    "#eef2f7": INK, "#cdd9e5": INK,
    "#8493a5": INK45, "#6d7f93": INK45, "#6f7f92": INK45,
    "#5c6b7c": INK45, "#9fb0c3": INK45, "#c3c2b7": INK45,
    "#55636f": INK20,
    "#f6d27a": CORRECTION,
    "#3987e5": INK, "#3a6ea0": INK,
    "#d95926": CORRECTION, "#d0654e": CORRECTION,
    "#a4503c": CORRECTION, "#c58b7c": CORRECTION,
    "#e9b7a8": "#f0d9d5",
    "#1f7fb8": COLD, "#16357a": COLD,
}


def reink(name):
    s = (SRC / name).read_text(encoding="utf-8")

    # --- structure -----------------------------------------------------------
    s = re.sub(r'\s*<rect width="1000" height="560" fill="#0a0e14"/>', "", s)
    s = re.sub(r'\s*<rect[^>]*fill="url\(#therm\)"[^>]*/>', "", s)
    s = re.sub(r'\s*<linearGradient id="therm".*?</linearGradient>', "", s, flags=re.S)
    s = re.sub(r'\s*<text x="40" y="46"[^>]*>.*?</text>', "", s, flags=re.S)
    s = re.sub(r'\s*<text x="40" y="68"[^>]*>.*?</text>', "", s, flags=re.S)
    s = re.sub(r'\s*<text[^>]*>[^<]*not to scale[^<]*</text>', "", s)

    # --- tag the coolant runs BEFORE the palette collapses -------------------
    # Thick warm/chilled paths are the flowing runs; the thin chevrons and the
    # legend swatches share their colour and should be recoloured but not moved.
    def tag(m, cls):
        el = m.group(0)
        if 'class="' in el:
            return el
        return el[:5] + f' class="{cls}"' + el[5:]

    s = re.sub(r'<path (?=[^>]*stroke="#f2a53c")(?=[^>]*stroke-width="3")[^>]*/>',
               lambda m: tag(m, "flow flow--hot"), s)
    s = re.sub(r'<path (?=[^>]*stroke="#22b8e6")(?=[^>]*stroke-width="3")[^>]*/>',
               lambda m: tag(m, "flow flow--cold"), s)

    # the flow classes supply their own dash rhythm via CSS
    s = re.sub(r'(<path class="flow[^"]*"[^>]*?)\s*stroke-dasharray="[^"]*"', r"\1", s)

    # arrowhead markers: aA warm, aC chilled, aG heat-to-air
    s = s.replace('<marker id="aA"', '<marker id="aA" class="mk mk--hot"')
    s = s.replace('<marker id="aC"', '<marker id="aC" class="mk mk--cold"')

    # Fan blades, so they can spin.
    #
    # The invisible circle is load-bearing. CSS rotates a fill-box element about
    # its bounding-box centre, but three blades radiating from the hub give an
    # ASYMMETRIC box — measured here as ~3 units off (0,0) — so the blades would
    # orbit that offset point instead of spinning about the hub. A concentric
    # circle with no paint contributes geometry to the bbox without drawing
    # anything, forcing the box symmetric and the origin onto the hub.
    s = s.replace(
        '<g fill="#22b8e6" opacity="0.85">',
        '<g class="fan" fill="none" stroke="%s" stroke-width="1.25">'
        '<circle r="34" fill="none" stroke="none"/>' % INK)

    # --- palette -------------------------------------------------------------
    s = re.sub(r'(stroke|fill)="#f2a53c"', r'\1="%s"' % HOT, s, flags=re.I)
    s = re.sub(r'(stroke|fill)="#22b8e6"', r'\1="%s"' % COLD, s, flags=re.I)
    for old, new in BASE_MAP.items():
        s = re.sub(re.escape(old), new, s, flags=re.I)

    s = s.replace("'Inter', system-ui, -apple-system, sans-serif",
                  "Archivo, 'Helvetica Neue', Arial, sans-serif")

    # --- crop past the old title block ---------------------------------------
    new_h = FULL_H - CROP_TOP
    s = re.sub(r'height="560"', f'height="{new_h}"', s, count=1)
    s = re.sub(r'viewBox="0 0 1000 560"', f'viewBox="0 {CROP_TOP} 1000 {new_h}"', s)

    (MEDIA / name).write_text(s, encoding="utf-8")
    hot = s.count("flow--hot")
    cold = s.count("flow--cold")
    fan = s.count('class="fan"')
    print(f"{name:26} hot={hot}  cold={cold}  fans={fan}")


for n in ["prawaas-loop.svg", "architecture-loop.svg", "ctms-loop.svg",
          "sor-states.svg", "btms-capacity.svg", "rectifier-derating.svg"]:
    reink(n)
