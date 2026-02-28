"""
SPC Image Generator – Sovereign Proof Certificate

Generates a visual PNG certificate with:
- Gold GCSLC seal (when available)
- 1m x 1m Steel watermark

© GCSLC. Proprietary.
"""

import io
import os
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


def generate_spc_image(seal_path: Optional[str] = None, width: int = 1000, height: int = 700) -> io.BytesIO:
    """Generate an in-memory PNG Sovereign Proof Certificate image."""
    img = Image.new("RGB", (width, height), color=(0, 33, 71))  # Lustrous Navy
    draw = ImageDraw.Draw(img)

    # Fonts (fallback to default if custom not available)
    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_body = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()

    gold = (212, 175, 55)

    # Title
    title = "SOVEREIGN PROOF CERTIFICATE"
    tw, th = draw.textsize(title, font=font_title)
    draw.text(((width - tw) / 2, 40), title, fill=gold, font=font_title)

    # Optional seal
    if seal_path and os.path.isfile(seal_path):
        try:
            seal = Image.open(seal_path).convert("RGBA")
            seal = seal.resize((140, 140))
            img.paste(seal, ((width - 140) // 2, 100), seal)
        except Exception:
            pass

    # D1–D8 map
    body_y = 270
    body_text = (
        "D1 Refine → D2 Reset → D3 Research → D4 Restructure → "
        "D5 Resuscitate → D6 Revitalize → D7 Re-engineer → D8 Retain"
    )
    bw, _ = draw.textsize(body_text, font=font_body)
    draw.text(((width - bw) / 2, body_y), body_text, fill=gold, font=font_body)

    # Talon Lock metric
    metric = "🔒 95% Legacy Retention / Talon Lock — Primary Security Metric for this Strike"
    mw, _ = draw.textsize(metric, font=font_body)
    draw.text(((width - mw) / 2, body_y + 60), metric, fill=(232, 197, 71), font=font_body)

    # Universality footer
    footer = (
        "This Certificate validates the Scientific Universality of the 8R Stealth Paradigm "
        "across Human, Economic, and AI Systems."
    )
    draw.text((60, height - 130), footer, fill=gold, font=font_small)

    # 1m x 1m Steel watermark
    watermark = "1m x 1m Steel — Proprietary Nodal Logic of GCSLC"
    ww, wh = draw.textsize(watermark, font=font_small)
    # Diagonal watermark (approximate by rotated image)
    mark_img = Image.new("RGBA", (ww + 20, wh + 20), (0, 0, 0, 0))
    mark_draw = ImageDraw.Draw(mark_img)
    mark_draw.text((10, 10), watermark, fill=(212, 175, 55, 60), font=font_small)
    mark_img = mark_img.rotate(30, expand=1)
    img.paste(mark_img, ((width - mark_img.width) // 2, (height - mark_img.height) // 2), mark_img)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

