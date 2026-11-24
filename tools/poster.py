#!/usr/bin/env python3
"""Draw the entry image: "The world, Tuesday 24 November 2026" - one day, six regions.

Each panel is a story first carried on 24 November 2026, from the wire copy read while
building it:

  Strait of Hormuz  Iran's IRGC says three oil tankers caught fire after hitting naval
                    mines in the strait (Al Jazeera live, 24 Nov 2026).
  United States     Nvidia added almost $1tn of value as Jensen Huang was reinstated as
                    chief executive; the Nasdaq rose 6.5% (BBC, 23-24 Nov 2026).
  Indonesia         Fire at a candy factory; 24 dead, dozens missing (NYT / DW, 23-24 Nov).
  Libya             Ukrainian naval drones struck two Russian ships and sank the warship
                    Merkury at a naval base in Libya (BBC / Guardian, 23-24 Nov 2026).
  Colombia          Car bomb at the Meta governor's office in Villavicencio, 12 hurt
                    (Al Jazeera / Anadolu, 24 Nov 2026).
  Bangladesh        Sheikh Hasina says she plans to return on 16 December (BBC, 24 Nov).

Usage:  python3 tools/poster.py [--preview 300]
Writes entry.png (1024x1024, well under 1 MiB) at the repository root.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 40
FONT_DIR = "/usr/share/fonts/TTF"

INK = (16, 21, 28, 255)
NIGHT = (11, 15, 21, 255)
PAPER = (253, 250, 242, 255)
CREAM = (240, 234, 221, 255)
MUTED = (138, 148, 166, 255)
EMBER = (226, 84, 44, 255)
GOLD = (242, 178, 62, 255)
TEAL = (42, 157, 143, 255)
STEEL = (124, 136, 152, 255)
SEA = (24, 45, 62, 255)
SMOKE = (104, 112, 126, 200)

F_BOLD = "DejaVuSansCondensed-Bold.ttf"
F_SANS = "DejaVuSans.ttf"
F_SANS_B = "DejaVuSans-Bold.ttf"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def text_w(draw: ImageDraw.ImageDraw, s: str, f: ImageFont.FreeTypeFont) -> float:
    return draw.textlength(s, font=f)


def tracked(draw, xy, s, f, fill, tracking=2.0):
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += text_w(draw, ch, f) + tracking
    return x


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def star(cx, cy, spokes, outer, inner, fill):
    pts = []
    for k in range(spokes * 2):
        r = outer if k % 2 == 0 else inner
        a = math.pi * k / spokes
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# --------------------------------------------------------------------------- icons
# Drawn on a 4x canvas and shrunk, which is cheap anti-aliasing. No two panels share a
# motif: fire on the water, a chip, a smoking plant, a drone's radar, a shockwave, a jet.


def icon_tanker_fire(d: ImageDraw.ImageDraw, S: int = 300) -> None:
    """Tanker ablaze in a narrow strait, mines in the water."""
    d.rectangle([0, 190, S, S], fill=SEA)
    for y in (222, 252, 280):
        d.line([10, y, S - 10, y], fill=(40, 76, 98, 255), width=5)
    d.polygon([(0, 118), (44, 148), (70, 190), (0, 190)], fill=(56, 66, 80, 255))
    d.polygon([(S, 100), (S - 54, 138), (S - 88, 190), (S, 190)], fill=(56, 66, 80, 255))
    # smoke leans away from the fire
    for cx, cy, r in ((136, 52, 30), (176, 36, 24), (212, 26, 17)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    # flames, short and near the deck
    for fx, top in ((96, 148), (132, 132), (168, 142)):
        d.polygon([(fx - 17, 192), (fx, top), (fx + 17, 192)], fill=EMBER)
    d.polygon([(66, 192), (268, 192), (252, 234), (96, 234), (58, 214)], fill=(20, 26, 34, 255))
    d.rectangle([196, 150, 244, 192], fill=(230, 224, 210, 255))
    d.rectangle([202, 160, 212, 176], fill=INK)
    d.rectangle([218, 160, 228, 176], fill=INK)
    d.line([250, 130, 250, 192], fill=(230, 224, 210, 255), width=6)
    d.polygon([(250, 130), (280, 140), (250, 150)], fill=EMBER)
    for mx, my in ((36, 264), (270, 274)):
        d.ellipse([mx - 10, my - 10, mx + 10, my + 10], fill=(28, 32, 40, 255))
        for a in (0.4, 1.6, 2.8, 4.0, 5.2):
            d.line([mx, my - 8, mx + 16 * math.cos(a), my - 8 + 16 * math.sin(a)],
                   fill=(28, 32, 40, 255), width=4)


def icon_chip_chart(d: ImageDraw.ImageDraw, S: int = 300) -> None:
    """A chip and the rally it set off."""
    d.line([(28, 268), (104, 212), (166, 236), (250, 128)], fill=TEAL, width=16, joint="curve")
    d.polygon([(256, 110), (282, 146), (238, 150)], fill=TEAL)
    for i in range(4):
        p = 96 + i * 34
        d.rectangle([p, 58, p + 16, 88], fill=STEEL)
        d.rectangle([p, 228, p + 16, 258], fill=STEEL)
        d.rectangle([44, p, 74, p + 16], fill=STEEL)
        d.rectangle([214, p, 244, p + 16], fill=STEEL)
    d.rounded_rectangle([74, 88, 214, 228], radius=18, fill=INK)
    d.rounded_rectangle([100, 114, 188, 202], radius=10, outline=GOLD, width=8)
    d.rectangle([138, 138, 150, 178], fill=GOLD)
    d.rectangle([112, 158, 124, 178], fill=EMBER)
    d.rectangle([164, 120, 176, 178], fill=EMBER)


def icon_factory_smoke(d: ImageDraw.ImageDraw, S: int = 300) -> None:
    """A plant with fire in its windows and a column of smoke."""
    for cx, cy, r in ((222, 52, 26), (188, 40, 20), (154, 52, 14)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    d.rectangle([40, 170, 258, 262], fill=INK)
    for i, x in enumerate((40, 80, 120)):
        d.polygon([(x, 170), (x + 40, 118), (x + 40, 170)], fill=INK)
    d.rectangle([196, 92, 228, 170], fill=INK)
    for wx in (56, 88, 120):
        d.rectangle([wx, 186, wx + 22, 214], fill=EMBER)
    d.rectangle([188, 196, 246, 262], fill=(92, 100, 114, 255))
    d.rectangle([196, 226, 238, 262], fill=PAPER)


def icon_warship_drone(d: ImageDraw.ImageDraw, S: int = 300) -> None:
    """A hull holed and listing, smoke coming off it, the drone that hit it above."""
    d.ellipse([0, 168, S, 256], fill=SEA)
    for y in (250, 272):
        d.line([8, y, S - 8, y], fill=(40, 76, 98, 255), width=5)

    ship = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(ship)
    sd.polygon([(30, 176), (272, 176), (242, 222), (56, 222)], fill=(96, 106, 120, 255))
    sd.polygon([(30, 176), (272, 176), (268, 186), (34, 186)], fill=(74, 82, 96, 255))
    sd.polygon([(126, 136), (200, 136), (200, 176), (126, 176)], fill=(74, 82, 96, 255))
    sd.rectangle([136, 96, 150, 136], fill=(74, 82, 96, 255))
    sd.line([143, 96, 198, 108], fill=(74, 82, 96, 255), width=5)
    sd.rectangle([210, 152, 248, 176], fill=(74, 82, 96, 255))
    sd.line([248, 164, 284, 158], fill=(74, 82, 96, 255), width=7)
    # the breach, and what comes out of it
    sd.polygon([(148, 176), (182, 176), (176, 200), (154, 200), (146, 188)], fill=(12, 16, 22, 255))
    for cx, cy, r in ((168, 128, 20), (186, 108, 15), (200, 94, 10)):
        sd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(112, 120, 134, 215))
    for k in range(4):
        sd.line([(164 + k * 5, 176), (150 + k * 12, 132)], fill=EMBER, width=6)
    ship = ship.rotate(-9, resample=Image.BICUBIC, center=(150, 180))
    d._image.alpha_composite(ship)  # same canvas: the hull rides at an angle, stern low

    # the drone above, still circling
    d.polygon(star(70, 58, 3, 25, 9, (226, 232, 238, 240)))
    for dx, dy in ((-56, 116), (-22, 96), (8, 80)):
        d.line([(70 + dx, 58 + dy), (70 + dx * 0.8, 58 + dy * 0.8)],
               fill=(226, 232, 238, 115), width=3)


def icon_car_bomb(d: ImageDraw.ImageDraw, S: int = 300) -> None:
    """A car bomb: smoke, a lifted wreck, a damaged building."""
    d.rectangle([150, 56, 290, 268], fill=(72, 80, 94, 255))
    for row in range(3):
        for col in range(2):
            x, y = 168 + col * 62, 82 + row * 62
            broken = (row, col) in ((0, 0), (2, 1), (1, 0))
            d.rectangle([x, y, x + 44, y + 42], fill=INK if broken else (222, 216, 202, 255))
    # smoke and flash behind the car
    for cx, cy, r in ((96, 104, 34), (128, 78, 26), (66, 78, 22)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(112, 120, 134, 205))
    d.ellipse([62, 108, 122, 168], fill=GOLD)

    car = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cd = ImageDraw.Draw(car)
    cd.rounded_rectangle([26, 178, 168, 232], radius=16, fill=INK)
    cd.rounded_rectangle([58, 144, 136, 186], radius=12, fill=INK)
    cd.rectangle([68, 152, 98, 178], fill=(222, 216, 202, 255))
    cd.polygon([(104, 152), (128, 152), (128, 178), (104, 178)], fill=(226, 84, 44, 255))
    for wx in (54, 140):
        cd.ellipse([wx - 16, 216, wx + 16, 248], fill=(30, 34, 42, 255))
        cd.ellipse([wx - 7, 225, wx + 7, 239], fill=STEEL)
    car = car.rotate(-13, resample=Image.BICUBIC, center=(100, 210))
    d._image.alpha_composite(car)
    for dx, dy, s in ((176, 236, 12), (196, 210, 9), (24, 150, 8), (44, 128, 7)):
        d.polygon([(dx, dy), (dx + s, dy + s * 0.6), (dx + s * 0.6, dy + s)], fill=STEEL)


def icon_plane_flag(d: ImageDraw.ImageDraw, S: int = 300) -> None:
    """Flag on the left, a flight arcing home to it."""
    d.rectangle([40, 66, 168, 158], fill=(0, 106, 78, 255))
    d.ellipse([82, 88, 132, 138], fill=(244, 42, 65, 255))
    d.line([34, 52, 34, 276], fill=(72, 80, 94, 255), width=11)
    # the flight path: it came in from the far corner and is heading for the flag
    for k in range(8):
        t = k / 7
        x = 296 - 46 * math.sin(t * 1.4)
        y = 258 - 108 * t
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(232, 226, 212, 195))
    # the jet, nose left, swept wings, tail behind: flying toward Bangladesh
    d.polygon([(198, 130), (218, 121), (288, 120), (296, 128), (290, 137), (218, 141)], fill=INK)
    d.polygon([(234, 128), (266, 86), (286, 92), (258, 132)], fill=INK)
    d.polygon([(234, 134), (266, 176), (286, 170), (258, 130)], fill=INK)
    d.polygon([(276, 123), (300, 96), (308, 103), (290, 130)], fill=INK)


ICONS = [icon_tanker_fire, icon_chip_chart, icon_factory_smoke, icon_warship_drone,
         icon_car_bomb, icon_plane_flag]


# --------------------------------------------------------------------------- cards

STORIES = [
    ("STRAIT OF HORMUZ", "MINES SET 3 TANKERS ABLAZE"),
    ("UNITED STATES", "NVIDIA ADDS NEARLY $1TN AS HUANG RETURNS"),
    ("INDONESIA", "CANDY FACTORY FIRE KILLS 24"),
    ("LIBYA", "RUSSIAN WARSHIP SUNK IN PORT"),
    ("COLOMBIA", "CAR BOMB AT A GOVERNOR'S OFFICE"),
    ("BANGLADESH", "HASINA TO RETURN ON 16 DECEMBER"),
]


def draw_card(canvas: Image.Image, x0: int, y0: int, w: int, h: int, idx: int) -> None:
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=14, fill=PAPER)
    kicker, headline = STORIES[idx]

    side = int(h - 74)
    art = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
    ICONS[idx](ImageDraw.Draw(art), 300)
    art = art.resize((side, side), Image.LANCZOS)
    canvas.alpha_composite(art, (x0 + 22, y0 + (h - side) // 2))

    tx = x0 + 22 + side + 16
    tw = x0 + w - 22 - tx
    tracked(d, (tx, y0 + 24), kicker, font(F_BOLD, 15), EMBER, tracking=1.6)

    num = f"{idx + 1:02d}"
    fn = font(F_BOLD, 18)
    d.text((x0 + w - 22 - text_w(d, num, fn), y0 + 21), num, font=fn, fill=(198, 190, 174, 255))

    size, fh, lines = 37, None, []
    while size > 24:
        fh = font(F_BOLD, size)
        lines = wrap(d, headline, fh, tw)
        if len(lines) <= 3:
            break
        size -= 1
    lead = int(size * 1.1)
    y = y0 + 24 + 30 + max(0, (h - 24 - 30 - 12 - len(lines) * lead) // 2)
    for line in lines:
        d.text((tx, y), line, font=fh, fill=INK)
        y += lead


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", type=int, default=0, help="also write a downscaled preview")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / "entry.png"))
    args = ap.parse_args()

    canvas = Image.new("RGBA", (W, H), NIGHT)
    d = ImageDraw.Draw(canvas)

    tracked(d, (MARGIN, 40), "WORLD NEWS", font(F_SANS_B, 17), MUTED, tracking=3.4)
    right = "TUESDAY"
    fr = font(F_SANS_B, 17)
    d.text((W - MARGIN - text_w(d, right, fr) - 3.4 * len(right), 40), right, font=fr, fill=MUTED)

    fdate = font(F_BOLD, 84)
    date = "24 NOVEMBER 2026"
    tw_date = text_w(d, date, fdate)
    if tw_date > W - 2 * MARGIN:
        fdate = font(F_BOLD, int(84 * (W - 2 * MARGIN) / tw_date))
    d.text((MARGIN, 74), date, font=fdate, fill=CREAM)
    d.rectangle([MARGIN, 186, W - MARGIN, 190], fill=EMBER)
    tracked(d, (MARGIN, 204), "SIX STORIES, SIX REGIONS  ·  ONE DAY", font(F_SANS_B, 16), TEAL, tracking=2.6)

    top, bottom, gap = 248, 966, 16
    card_h = (bottom - top - 2 * gap) // 3
    card_w = (W - 2 * MARGIN - 20) // 2
    for i in range(6):
        col, row = i % 2, i // 2
        draw_card(canvas, MARGIN + col * (card_w + 20), top + row * (card_h + gap), card_w, card_h, i)

    tracked(d, (MARGIN, 986), "THE DAY IN SIX STORIES", font(F_SANS_B, 13), MUTED, tracking=2.2)
    src = "BBC  ·  AL JAZEERA  ·  NPR  ·  NYT"
    fs = font(F_SANS, 13)
    d.text((W - MARGIN - text_w(d, src, fs) - 2.2 * len(src), 986), src, font=fs, fill=MUTED)

    out = Image.new("RGB", (W, H), NIGHT[:3])
    out.paste(canvas, (0, 0), canvas)
    out.save(args.out, "PNG", optimize=True)
    if args.preview:
        out.resize((args.preview, args.preview), Image.LANCZOS).save(
            args.out.replace(".png", f"-{args.preview}.png"))
    print(f"wrote {args.out} ({os.path.getsize(args.out)} bytes, limit 1048576)")


if __name__ == "__main__":
    main()
