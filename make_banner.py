"""Generate banner.svg: a fastfetch-style terminal window for the GitHub profile README.

Edit INFO (and LOGO_TEXT) below, then run:  python make_banner.py
Pure standard library; the output is a static SVG that GitHub renders as an image.
"""

from html import escape

# ── content ──────────────────────────────────────────────────────────────────
USER, HOST = "isaac", "busan"
LOGO_TEXT = "ISAAC"
INFO = [  # (key, value); key None = plain line (title / separator)
    (None, "isaac@github"),
    (None, "-" * 12),
    ("Role", "Undergraduate ML researcher"),
    ("University", "Pusan National University"),
    ("Location", "Busan, South Korea"),
    ("Focus", "Auditing what vision models actually learn"),
    ("Research", "Child-detector skin-tone audit (preregistered)"),
    ("", "Shortcut learning in person re-ID (Market-1501)"),
    ("Experience", "Research intern, IDOLL Robotics"),
    ("Methods", "Linear probes, bootstrap CIs, permutation tests"),
    ("Stack", "Python, PyTorch, OpenCLIP, Hugging Face"),
    ("Also", "C, Kotlin, JavaScript, Django"),
]

# ── 7-row pixel font (only the letters needed); '#' = filled cell ──────────────
FONT = {
    "I": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "C": [" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"],
    "M": ["#   #", "## ##", "# # #", "#   #", "#   #", "#   #", "#   #"],
}
CELL, GAP = 15, 2          # pixel size and gap between pixels (SVG units)

# ── style ────────────────────────────────────────────────────────────────────
BG, WIN, BAR, EDGE = "#0b0e12", "#11161c", "#1b222a", "#2a343e"
INK, MUTED, KEY, PROMPT_USER, PROMPT_PATH = "#e6e3dc", "#98a2ab", "#7aa5c4", "#7fa88b", "#7aa5c4"
LOGO_GRADIENT = ["#7aa5c4", "#7fa9bc", "#86adb0", "#8aafa2", "#84ab93", "#93b286", "#a7b87a"]
SWATCHES = ["#cc4b3f", "#e0a43c", "#7fa88b", "#7aa5c4", "#a88bc4", "#6fb8b0", "#e6e3dc"]
FONT_FAMILY = "'JetBrains Mono','SF Mono','Source Code Pro',Menlo,Consolas,monospace"
FS, LH, CW = 22, 34, 13.2   # font size, line height, approx monospace char width


def logo_rects(text, x0, y0):
    """SVG rects drawing `text` in the pixel font, one colour per row."""
    rects, x = [], x0
    for ch in text:
        for r, row in enumerate(FONT[ch]):
            for c, cell in enumerate(row):
                if cell == "#":
                    rects.append(f'<rect x="{x + c * CELL}" y="{y0 + r * CELL}" width="{CELL - GAP}" '
                                 f'height="{CELL - GAP}" rx="2" fill="{LOGO_GRADIENT[r]}"/>')
        x += (len(FONT[ch][0]) + 1) * CELL
    return rects, x - x0 - CELL


def main():
    logo_w = sum((len(FONT[ch][0]) + 1) * CELL for ch in LOGO_TEXT) - CELL
    pad, top = 48, 70
    info_x = pad + logo_w + 56
    info_w = max(len(f"{k}: {v}") if k is not None else len(v) for k, v in INFO) * CW
    W = int(info_x + info_w + pad + 60)
    body_top = top + 70
    H = int(body_top + LH * (len(INFO) + 3) + 30)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="{FONT_FAMILY}" font-size="{FS}" role="img" '
           f'aria-label="Terminal-style profile summary for Isaac Mutuma">',
           f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>',
           f'<rect x="12" y="12" width="{W-24}" height="{H-24}" rx="12" fill="{WIN}" stroke="{EDGE}"/>',
           f'<path d="M12 24 a12 12 0 0 1 12 -12 H{W-24} a12 12 0 0 1 12 12 V56 H12 Z" fill="{BAR}"/>',
           f'<rect x="12" y="56" width="{W-24}" height="1" fill="{EDGE}"/>']
    for i, c in enumerate(["#cc4b3f", "#e0a43c", "#7fa88b"]):
        out.append(f'<circle cx="{38 + 24 * i}" cy="34" r="7" fill="{c}"/>')
    out.append(f'<text x="{W/2}" y="40" text-anchor="middle" font-size="18" fill="{MUTED}">'
               f'{USER}@{HOST}: ~</text>')
    # prompt line
    out.append(f'<text x="{pad}" y="{top + 38}" xml:space="preserve">'
               f'<tspan fill="{PROMPT_USER}" font-weight="bold">{USER}@{HOST}</tspan>'
               f'<tspan fill="{MUTED}">:</tspan><tspan fill="{PROMPT_PATH}" font-weight="bold">~</tspan>'
               f'<tspan fill="{MUTED}">$ </tspan><tspan fill="{INK}">fastfetch</tspan></text>')
    # logo, vertically centred against the info block
    logo_top = body_top - FS + (len(INFO) * LH - 7 * CELL) / 2
    rects, _ = logo_rects(LOGO_TEXT, pad, round(logo_top))
    out.append('<g aria-hidden="true">' + "".join(rects) + "</g>")
    # info block
    for i, (k, v) in enumerate(INFO):
        y = body_top + i * LH
        if k is None:
            color = PROMPT_USER if i == 0 else MUTED
            weight = ' font-weight="bold"' if i == 0 else ""
            out.append(f'<text x="{info_x:.0f}" y="{y}" fill="{color}"{weight}>{escape(v)}</text>')
        else:
            key = f"{k}:" if k else ""
            out.append(f'<text x="{info_x:.0f}" y="{y}" xml:space="preserve">'
                       f'<tspan fill="{KEY}" font-weight="bold">{escape(key):<12}</tspan>'
                       f'<tspan fill="{INK}">{escape(v)}</tspan></text>')
    # colour swatches, fastfetch style
    sy = body_top + (len(INFO) + 0.6) * LH
    for i, c in enumerate(SWATCHES):
        out.append(f'<rect x="{info_x + i * 40:.0f}" y="{sy:.0f}" width="36" height="22" rx="3" fill="{c}"/>')
    # blinking cursor on a final prompt
    cy = sy + LH * 1.6
    out.append(f'<text x="{pad}" y="{cy:.0f}" xml:space="preserve"><tspan fill="{PROMPT_USER}" '
               f'font-weight="bold">{USER}@{HOST}</tspan><tspan fill="{MUTED}">:</tspan>'
               f'<tspan fill="{PROMPT_PATH}" font-weight="bold">~</tspan><tspan fill="{MUTED}">$ </tspan></text>')
    cx = pad + (len(f"{USER}@{HOST}:~$ ") + 0.2) * CW
    out.append(f'<rect x="{cx:.0f}" y="{cy - FS + 4:.0f}" width="12" height="{FS}" fill="{INK}">'
               f'<animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></rect>')
    out.append("</svg>")
    H_needed = cy + 40
    svg = "\n".join(out).replace(f'height="{H}" viewBox="0 0 {W} {H}"',
                                 f'height="{H_needed:.0f}" viewBox="0 0 {W} {H_needed:.0f}"', 1)
    svg = svg.replace(f'<rect width="{W}" height="{H}"', f'<rect width="{W}" height="{H_needed:.0f}"', 1)
    svg = svg.replace(f'height="{H-24}"', f'height="{H_needed - 24:.0f}"', 1)
    open("banner.svg", "w").write(svg + "\n")
    print(f"banner.svg {W}x{H_needed:.0f}")


if __name__ == "__main__":
    main()
