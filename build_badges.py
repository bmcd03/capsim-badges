"""One-time builder: writes the two badge SVGs with the Capsim logo embedded.

The logo (assets/logo-datauri.txt) is the full-color Capsim wordmark extracted
from capsim.com/hubfs/images/capsim_logo_retina.svg (365x60 PNG inside).
Brand palette pulled from capsim.com: slate #19262F, blue #0062FF.

Layout: white center disc with the full-color logo dead center, slate outer
band carrying two arcs of ring text (program on top, designation on bottom).
"""

from pathlib import Path

ROOT = Path(__file__).parent
LOGO = (ROOT / "assets" / "logo-datauri.txt").read_text().strip()

SLATE = "#19262F"
SLATE_LIGHT = "#243542"
BLUE = "#0062FF"
GOLD = "#D9A62E"
GOLD_LIGHT = "#F2CD6B"
GOLD_DARK = "#A87B14"

# Logo native 365x60. Centered in the white disc: width 200 -> height 32.9.
LOGO_W = 200
LOGO_H = LOGO_W * 60 / 365
LOGO_X = (400 - LOGO_W) / 2
LOGO_Y = 200 - LOGO_H / 2


def badge(accent_edge: str, accent_ring: str, bottom_text_fill: str,
          label: str, label_size: int, label_spacing: float,
          extra: str = "") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="slateGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SLATE_LIGHT}"/>
      <stop offset="1" stop-color="{SLATE}"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GOLD_LIGHT}"/>
      <stop offset="0.5" stop-color="{GOLD}"/>
      <stop offset="1" stop-color="{GOLD_DARK}"/>
    </linearGradient>
    <!-- band spans r136-190; baselines placed so glyphs clear both edges -->
    <path id="arcTop" d="M 200,200 m -158,0 a 158,158 0 1,1 316,0" fill="none"/>
    <path id="arcBottom" d="M 200,200 m -170,0 a 170,170 0 1,0 340,0" fill="none"/>
  </defs>

  <!-- outer edge + slate band -->
  <circle cx="200" cy="200" r="198" fill="{accent_edge}"/>
  <circle cx="200" cy="200" r="190" fill="url(#slateGrad)"/>

  <!-- white center disc with the Capsim logo, full color, dead center -->
  <circle cx="200" cy="200" r="136" fill="#ffffff"/>
  <circle cx="200" cy="200" r="136" fill="none" stroke="{accent_ring}" stroke-width="4"/>
  <image x="{LOGO_X}" y="{LOGO_Y:.1f}" width="{LOGO_W}" height="{LOGO_H:.1f}" xlink:href="{LOGO}"/>
{extra}
  <!-- ring text: program name on top, designation on bottom -->
  <text font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="bold" fill="#ffffff" letter-spacing="1.5">
    <textPath href="#arcTop" startOffset="50%" text-anchor="middle">CAPSTONE BUSINESS SIMULATION</textPath>
  </text>
  <text font-family="Arial, Helvetica, sans-serif" font-size="{label_size}" font-weight="bold" fill="{bottom_text_fill}" letter-spacing="{label_spacing}">
    <textPath href="#arcBottom" startOffset="50%" text-anchor="middle">{label}</textPath>
  </text>

  <!-- dots at 3 and 9 o'clock separating the two arcs -->
  <circle cx="26" cy="200" r="5" fill="{bottom_text_fill}"/>
  <circle cx="374" cy="200" r="5" fill="{bottom_text_fill}"/>
</svg>
"""


GOLD_STARS = """
  <!-- champion stars inside the disc, above the logo -->
  <g fill="#D9A62E">
    <path d="M 200,98 l 8,17 18,2.5 -13,12.5 3.5,18 -16.5,-9 -16.5,9 3.5,-18 -13,-12.5 18,-2.5 z"/>
    <path d="M 152,116 l 5.5,11.5 12.5,1.7 -9,8.7 2.4,12.4 -11.4,-6.2 -11.4,6.2 2.4,-12.4 -9,-8.7 12.5,-1.7 z"/>
    <path d="M 248,116 l 5.5,11.5 12.5,1.7 -9,8.7 2.4,12.4 -11.4,-6.2 -11.4,6.2 2.4,-12.4 -9,-8.7 12.5,-1.7 z"/>
  </g>
"""

participation = badge(
    accent_edge=BLUE, accent_ring=BLUE,
    bottom_text_fill="#ffffff",
    label="PARTICIPANT", label_size=28, label_spacing=6,
)

first_place = badge(
    accent_edge="url(#goldGrad)", accent_ring=GOLD,
    bottom_text_fill=GOLD_LIGHT,
    label="FIRST PLACE TEAM", label_size=28, label_spacing=4,
    extra=GOLD_STARS,
)

(ROOT / "assets" / "badge-participation.svg").write_text(participation, encoding="utf-8")
(ROOT / "assets" / "badge-first-place.svg").write_text(first_place, encoding="utf-8")
print("Badges rebuilt: centered logo, brand colors, readable ring text.")
