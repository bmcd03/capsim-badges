"""One-time: extract the official CAPSIM(R) logo pieces from the Brandfetch
banner PNG (851x315, contains the uppercase CAPSIM(R) + green triangle lockup).

Color-based split: the wordmark is brand blue, the triangle mark is green;
the banner's product strip and gray tagline are excluded automatically.
Writes assets/mark-datauri.txt and assets/wordmark-datauri.txt.
"""

import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
SRC = Path(r"C:\Users\BOB~1.MCD\AppData\Local\Temp\claude\C--Users-bob-mcdonald"
           r"\e7e98b9c-f5ff-4f96-92a3-4be14101d8ef\scratchpad\capsim-bf.png")

img = Image.open(SRC).convert("RGBA")
w, h = img.size
px = img.load()

blue_box = [w, h, 0, 0]   # minx, miny, maxx, maxy
green_box = [w, h, 0, 0]

for y in range(80, h):          # skip the product-logo strip at the top
    for x in range(w):
        r, g, b, a = px[x, y]
        if a < 128:
            continue
        box = None
        if b > 120 and b > g + 30 and b > r + 60:      # brand blue
            box = blue_box
        elif g > 120 and g > r + 25 and g > b + 40:    # brand green
            box = green_box
        if box:
            box[0] = min(box[0], x); box[1] = min(box[1], y)
            box[2] = max(box[2], x); box[3] = max(box[3], y)

def save(box, name, pad=2):
    crop = img.crop((box[0]-pad, box[1]-pad, box[2]+1+pad, box[3]+1+pad))
    buf = io.BytesIO()
    crop.save(buf, format="PNG")
    data = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    (ROOT / "assets" / name).write_text(data)
    print(f"{name}: {crop.size[0]}x{crop.size[1]} -> {len(data)} chars")

save(green_box, "mark-datauri.txt")
save(blue_box, "wordmark-datauri.txt")
