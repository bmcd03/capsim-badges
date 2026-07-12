"""One-time builder: writes the two badge SVGs with the Capsim logo embedded.

The logo (assets/logo-datauri.txt) is the white Capsim wordmark extracted from
capsim.com/hubfs/images/capsim_logo_retina.svg (365x60 PNG inside).
Brand palette pulled from capsim.com: slate #19262F, blue #0062FF.
"""

from pathlib import Path

ROOT = Path(__file__).parent
LOGO = (ROOT / "assets" / "logo-datauri.txt").read_text().strip()

SLATE = "#19262F"
SLATE_LIGHT = "#243542"
BLUE = "#0062FF"
BLUE_LIGHT = "#5C9DFF"
GOLD = "#D9A62E"
GOLD_LIGHT = "#F2CD6B"
GOLD_DARK = "#A87B14"

# Logo box: native 365x60 -> render 168x27.6, centered
LOGO_W, LOGO_H = 168, 27.6
LOGO_X = (400 - LOGO_W) / 2

COMMON_DEFS = f"""
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
    <path id="ringTop" d="M 200,200 m -152,0 a 152,152 0 1,1 304,0" fill="none"/>
    <path id="ringBottom" d="M 200,200 m -149,0 a 149,149 0 1,0 298,0" fill="none"/>
    <!-- capsim.com serves a full-color logo; whiten it for dark backgrounds
         (same treatment the site header applies) -->
    <filter id="whiten">
      <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1 0"/>
    </filter>
  </defs>
"""

PARTICIPATION = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 400 400" width="400" height="400">
{COMMON_DEFS}
  <!-- outer badge -->
  <circle cx="200" cy="200" r="197" fill="{BLUE}"/>
  <circle cx="200" cy="200" r="188" fill="url(#slateGrad)"/>
  <circle cx="200" cy="200" r="128" fill="none" stroke="{BLUE}" stroke-width="3"/>
  <circle cx="200" cy="200" r="122" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.3"/>

  <!-- ring text: white on slate, high contrast -->
  <text font-family="Arial, Helvetica, sans-serif" font-size="25" font-weight="bold" fill="#ffffff" letter-spacing="3.5">
    <textPath href="#ringTop" startOffset="50%" text-anchor="middle">CAPSTONE BUSINESS SIMULATION</textPath>
  </text>
  <text font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="{BLUE_LIGHT}" letter-spacing="5">
    <textPath href="#ringBottom" startOffset="50%" text-anchor="middle">B U S I N E S S &#160; A C U M E N</textPath>
  </text>

  <!-- Capsim logo, whitened for the dark badge -->
  <image x="{LOGO_X}" y="118" width="{LOGO_W}" height="{LOGO_H}" filter="url(#whiten)" xlink:href="{LOGO}"/>

  <!-- rising bar chart motif -->
  <g fill="{BLUE}">
    <rect x="148" y="218" width="21" height="42" rx="3"/>
    <rect x="177" y="200" width="21" height="60" rx="3"/>
    <rect x="206" y="180" width="21" height="80" rx="3"/>
    <rect x="235" y="158" width="21" height="102" rx="3"/>
  </g>
  <polyline points="152,206 186,188 216,166 244,140" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <polygon points="248,136 226,140 242,156" fill="#ffffff"/>

  <!-- banner -->
  <rect x="92" y="280" width="216" height="42" rx="6" fill="{BLUE}"/>
  <text x="200" y="308" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="bold" fill="#ffffff" text-anchor="middle" letter-spacing="3">PARTICIPANT</text>
</svg>
"""

FIRST_PLACE = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 400 400" width="400" height="400">
{COMMON_DEFS}
  <!-- outer badge -->
  <circle cx="200" cy="200" r="197" fill="url(#goldGrad)"/>
  <circle cx="200" cy="200" r="186" fill="url(#slateGrad)"/>
  <circle cx="200" cy="200" r="128" fill="none" stroke="{GOLD}" stroke-width="3"/>
  <circle cx="200" cy="200" r="122" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.3"/>

  <!-- ring text: light gold on slate -->
  <text font-family="Arial, Helvetica, sans-serif" font-size="25" font-weight="bold" fill="{GOLD_LIGHT}" letter-spacing="3.5">
    <textPath href="#ringTop" startOffset="50%" text-anchor="middle">CAPSTONE BUSINESS SIMULATION</textPath>
  </text>
  <text font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="bold" fill="{GOLD_LIGHT}" letter-spacing="5">
    <textPath href="#ringBottom" startOffset="50%" text-anchor="middle">C H A M P I O N &#160; T E A M</textPath>
  </text>

  <!-- Capsim logo, whitened for the dark badge -->
  <image x="{LOGO_X}" y="118" width="{LOGO_W}" height="{LOGO_H}" filter="url(#whiten)" xlink:href="{LOGO}"/>

  <!-- laurel branches -->
  <g stroke="{GOLD}" stroke-width="4" fill="none" stroke-linecap="round">
    <path d="M 120,252 q -18,-40 2,-84"/>
    <path d="M 280,252 q 18,-40 -2,-84"/>
  </g>
  <g fill="{GOLD}">
    <ellipse cx="114" cy="240" rx="12" ry="5" transform="rotate(-55 114 240)"/>
    <ellipse cx="108" cy="212" rx="12" ry="5" transform="rotate(-75 108 212)"/>
    <ellipse cx="110" cy="184" rx="12" ry="5" transform="rotate(-95 110 184)"/>
    <ellipse cx="286" cy="240" rx="12" ry="5" transform="rotate(55 286 240)"/>
    <ellipse cx="292" cy="212" rx="12" ry="5" transform="rotate(75 292 212)"/>
    <ellipse cx="290" cy="184" rx="12" ry="5" transform="rotate(95 290 184)"/>
  </g>

  <!-- trophy -->
  <g>
    <path d="M 164,158 h 72 v 30 a 36,36 0 0 1 -72,0 z" fill="url(#goldGrad)"/>
    <path d="M 164,166 h -18 a 24,24 0 0 0 24,26" fill="none" stroke="{GOLD}" stroke-width="6"/>
    <path d="M 236,166 h 18 a 24,24 0 0 1 -24,26" fill="none" stroke="{GOLD}" stroke-width="6"/>
    <rect x="193" y="222" width="14" height="18" fill="{GOLD}"/>
    <rect x="175" y="240" width="50" height="11" rx="3" fill="url(#goldGrad)"/>
    <text x="200" y="192" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="bold" fill="{SLATE}" text-anchor="middle">1</text>
  </g>

  <!-- banner -->
  <rect x="82" y="274" width="236" height="44" rx="6" fill="url(#goldGrad)"/>
  <text x="200" y="303" font-family="Arial, Helvetica, sans-serif" font-size="20" font-weight="bold" fill="{SLATE}" text-anchor="middle" letter-spacing="2">FIRST PLACE TEAM</text>
</svg>
"""

(ROOT / "assets" / "badge-participation.svg").write_text(PARTICIPATION, encoding="utf-8")
(ROOT / "assets" / "badge-first-place.svg").write_text(FIRST_PLACE, encoding="utf-8")
print("Badges rebuilt with Capsim brand colors + logo.")
