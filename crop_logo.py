"""One-time: split the scraped Capsim logo (365x60 PNG) into its two parts.

Left 0-290: blue lowercase "capsim" wordmark. Right 308-365: green mark.
Writes both as data-URI text files for build_badges.py to embed.
"""

import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent / "assets"

uri = (ROOT / "logo-datauri.txt").read_text().strip()
png = base64.b64decode(uri.split(",", 1)[1])
img = Image.open(io.BytesIO(png))

def save(box, name):
    buf = io.BytesIO()
    img.crop(box).save(buf, format="PNG")
    data = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    (ROOT / name).write_text(data)
    print(f"{name}: crop {box} -> {len(data)} chars")

save((308, 0, 365, 60), "mark-datauri.txt")
save((0, 0, 290, 60), "wordmark-datauri.txt")
