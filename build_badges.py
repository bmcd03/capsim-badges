"""One-time builder: writes the two badge SVGs with the Capsim logo embedded.

Logo pieces come from capsim.com's capsim_logo_retina.svg (365x60 PNG inside),
split by crop_logo.py into the green mark (assets/mark-datauri.txt) and the
blue bold "capsim" wordmark (assets/wordmark-datauri.txt).
Brand palette pulled from capsim.com: slate #19262F, blue #0062FF.

Disc hierarchy: green mark large and centered (H1), wordmark beneath it (H2).
Slate outer band carries two arcs of ring text.
"""

from pathlib import Path

ROOT = Path(__file__).parent
MARK = (ROOT / "assets" / "mark-datauri.txt").read_text().strip()      # 63x68
WORDMARK = (ROOT / "assets" / "wordmark-datauri.txt").read_text().strip()  # 331x47

SLATE = "#19262F"
SLATE_LIGHT = "#243542"
BLUE = "#0062FF"
GOLD = "#D9A62E"
GOLD_LIGHT = "#F2CD6B"
GOLD_DARK = "#A87B14"


def centered(width: float, native_w: int, native_h: int, y: float) -> str:
    h = width * native_h / native_w
    x = (400 - width) / 2
    return f'x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{h:.1f}"'


def badge(accent_edge: str, accent_ring: str, bottom_text_fill: str,
          label: str, label_spacing: float,
          mark_w: float, mark_y: float, word_w: float, word_y: float,
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

  <!-- white center disc: green Capsim mark as focal point, wordmark beneath -->
  <circle cx="200" cy="200" r="136" fill="#ffffff"/>
  <circle cx="200" cy="200" r="136" fill="none" stroke="{accent_ring}" stroke-width="4"/>
  <image {centered(mark_w, 63, 68, mark_y)} xlink:href="{MARK}"/>
  <image {centered(word_w, 331, 47, word_y)} xlink:href="{WORDMARK}"/>
{extra}
  <!-- ring text: program name on top, designation on bottom -->
  <text font-family="Arial, Helvetica, sans-serif" font-size="23" font-weight="bold" fill="#ffffff" letter-spacing="1.5">
    <textPath href="#arcTop" startOffset="50%" text-anchor="middle">CAPSTONE BUSINESS SIMULATION</textPath>
  </text>
  <text font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" fill="{bottom_text_fill}" letter-spacing="{label_spacing}">
    <textPath href="#arcBottom" startOffset="50%" text-anchor="middle">{label}</textPath>
  </text>

  <!-- dots at 3 and 9 o'clock separating the two arcs -->
  <circle cx="26" cy="200" r="5" fill="{bottom_text_fill}"/>
  <circle cx="374" cy="200" r="5" fill="{bottom_text_fill}"/>
</svg>
"""


GOLD_STARS = """
  <!-- champion stars inside the disc, above the mark -->
  <g fill="#D9A62E">
    <path d="M 200,86 l 7,15 16,2 -11,11 3,16 -15,-8 -15,8 3,-16 -11,-11 16,-2 z"/>
    <path d="M 154,102 l 5,10 11,1.5 -8,8 2,11 -10,-5.5 -10,5.5 2,-11 -8,-8 11,-1.5 z"/>
    <path d="M 246,102 l 5,10 11,1.5 -8,8 2,11 -10,-5.5 -10,5.5 2,-11 -8,-8 11,-1.5 z"/>
  </g>
"""

participation = badge(
    accent_edge=BLUE, accent_ring=BLUE,
    bottom_text_fill="#ffffff",
    label="PARTICIPANT", label_spacing=6,
    mark_w=97, mark_y=124, word_w=190, word_y=250,
)

first_place = badge(
    accent_edge="url(#goldGrad)", accent_ring=GOLD,
    bottom_text_fill=GOLD_LIGHT,
    label="FIRST PLACE TEAM", label_spacing=4,
    mark_w=84, mark_y=150, word_w=175, word_y=256,
    extra=GOLD_STARS,
)

(ROOT / "assets" / "badge-participation.svg").write_text(participation, encoding="utf-8")
(ROOT / "assets" / "badge-first-place.svg").write_text(first_place, encoding="utf-8")
print("Badges rebuilt: green mark focal, wordmark beneath, stars kept.")
