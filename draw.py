#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: a one-page newspaper-style
infographic summing up Monday 23 November 2026. All facts verified
against Reuters / CNN / BBC / DW / AP reporting of 23 Nov 2026.
Output: entry.png, 1024x1024, deterministic."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (22, 50, 79)
RED = (179, 38, 30)
GREY = (90, 88, 82)
LIGHT = (255, 255, 255)
ORANGE = (214, 106, 24)
GREEN = (46, 125, 50)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def icon_globe(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=NAVY, width=5)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=NAVY, width=3)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=NAVY, width=3)
    d.arc([x - s * 0.25, y + s * 0.18, x + s * 1.25, y + s * 0.82],
          300, 60, fill=NAVY, width=3)
    d.line([x - 6, y + s + 6, x + s + 6, y - 6], fill=RED, width=7)


def icon_ship(d, x, y, s):
    # hull
    d.polygon([(x, y + s * 0.62), (x + s, y + s * 0.62),
               (x + s * 0.88, y + s * 0.92), (x + s * 0.12, y + s * 0.92)],
              fill=NAVY)
    # containers
    d.rectangle([x + s * 0.18, y + s * 0.34, x + s * 0.42, y + s * 0.60],
                fill=RED)
    d.rectangle([x + s * 0.46, y + s * 0.34, x + s * 0.70, y + s * 0.60],
                fill=ORANGE)
    d.rectangle([x + s * 0.58, y + s * 0.12, x + s * 0.82, y + s * 0.32],
                fill=GREY)
    # smoke
    for cx, cy, r in [(0.30, 0.10, 9), (0.42, 0.02, 7), (0.20, 0.20, 6)]:
        d.ellipse([x + s * cx - r, y + s * cy - r,
                   x + s * cx + r, y + s * cy + r], fill=(150, 148, 140))
    # water
    d.line([x, y + s * 0.98, x + s, y + s * 0.98], fill=NAVY, width=3)


def icon_building(d, x, y, s):
    d.rectangle([x + s * 0.15, y + s * 0.25, x + s * 0.85, y + s * 0.95],
                fill=(120, 118, 110))
    d.polygon([(x + s * 0.15, y + s * 0.25), (x + s * 0.55, y + s * 0.25),
               (x + s * 0.40, y + s * 0.45), (x + s * 0.15, y + s * 0.45)],
              fill=PAPER)
    for r in range(3):
        for c in range(3):
            wx = x + s * (0.25 + c * 0.22)
            wy = y + s * (0.52 + r * 0.15)
            d.rectangle([wx, wy, wx + s * 0.10, wy + s * 0.08], fill=NAVY)
    for cx, cy, r in [(0.45, 0.10, 8), (0.58, 0.03, 6)]:
        d.ellipse([x + s * cx - r, y + s * cy - r,
                   x + s * cx + r, y + s * cy + r], fill=(150, 148, 140))


def icon_factory(d, x, y, s):
    d.polygon([(x, y + s * 0.95), (x, y + s * 0.55), (x + s * 0.33, y + s * 0.30),
               (x + s * 0.33, y + s * 0.55), (x + s * 0.66, y + s * 0.30),
               (x + s * 0.66, y + s * 0.55), (x + s, y + s * 0.55),
               (x + s, y + s * 0.95)], fill=(120, 118, 110))
    d.rectangle([x + s * 0.78, y + s * 0.10, x + s * 0.90, y + s * 0.55],
                fill=NAVY)
    # flame
    d.polygon([(x + s * 0.45, y + s * 0.28), (x + s * 0.55, y + s * 0.02),
               (x + s * 0.62, y + s * 0.28)], fill=ORANGE)
    d.polygon([(x + s * 0.48, y + s * 0.28), (x + s * 0.55, y + s * 0.12),
               (x + s * 0.60, y + s * 0.28)], fill=RED)


def icon_flags(d, x, y, s):
    # Nepal (crimson with blue border, simplified) and India (tricolour)
    d.rectangle([x, y + s * 0.15, x + s * 0.44, y + s * 0.85],
                outline=NAVY, width=4, fill=(220, 20, 60))
    d.rectangle([x + s * 0.56, y + s * 0.15, x + s, y + s * 0.85],
                outline=INK, width=2)
    d.rectangle([x + s * 0.56, y + s * 0.15, x + s, y + s * 0.38],
                fill=(255, 153, 51))
    d.rectangle([x + s * 0.56, y + s * 0.38, x + s, y + s * 0.62],
                fill=LIGHT)
    d.rectangle([x + s * 0.56, y + s * 0.62, x + s, y + s * 0.85],
                fill=(19, 136, 8))
    d.ellipse([x + s * 0.71, y + s * 0.42, x + s * 0.85, y + s * 0.58],
              outline=NAVY, width=3)


def icon_ball(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=INK, width=4, fill=LIGHT)
    cx, cy, r = x + s / 2, y + s / 2, s * 0.20
    pts = []
    import math
    for k in range(5):
        a = math.radians(-90 + k * 72)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=INK)
    for k in range(5):
        a = math.radians(-90 + k * 72)
        d.line([cx + r * math.cos(a), cy + r * math.sin(a),
                cx + s * 0.48 * math.cos(a), cy + s * 0.48 * math.sin(a)],
               fill=INK, width=3)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# top red bar
d.rectangle([0, 0, W, 10], fill=RED)

# masthead
f_mast = font(FSB, 64)
f_date = font(FB, 32)
f_tag = font(FB, 17)
title = "THE WORLD TODAY"
tw = d.textlength(title, font=f_mast)
d.text(((W - tw) / 2, 24), title, font=f_mast, fill=INK)
date = "MONDAY  23  NOVEMBER  2026"
dw = d.textlength(date, font=f_date)
d.text(((W - dw) / 2, 100), date, font=f_date, fill=RED)
d.line([28, 148, W - 28, 148], fill=INK, width=3)
d.line([28, 154, W - 28, 154], fill=INK, width=1)

# ---- lead story: COP31 ----
f_lead_h = font(FB, 37)
f_lead_b = font(FR, 21)
lx, ly, lw, lh = 28, 168, W - 56, 192
d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2, fill=LIGHT)
icon_globe(d, lx + 22, ly + 52, 110)
tx = lx + 160
d.text((tx, ly + 16), "CLIMATE  ·  ANTALYA, TURKEY", font=f_tag, fill=RED)
y = para(d, tx, ly + 44, "COP31 collapses — no climate deal",
         f_lead_h, INK, lw - 190, 44)
para(d, tx, y + 6,
     "Nearly 200 nations leave the UN talks with no agreement after the "
     "final draft dropped every mention of fossil fuels — the longest COP "
     "ever, and the first to fail since Copenhagen in 2009.",
     f_lead_b, INK, lw - 190, 27)

# ---- story grid: 3 cols x 2 rows ----
cards = [
    ("BALTIC SEA", "Drone-hit Russian ship towed out of Finnish waters",
     "Hit by drones on Saturday, the Sparta II is towed out after two days "
     "of firefighting. All 16 crew evacuated.",
     icon_ship),
    ("UKRAINE", "14 missing after drone hits Kyiv-region flats",
     "A Russian drone partly destroys a block of flats in Dymer. Nine "
     "pulled out; rescuers search the rubble.",
     icon_building),
    ("INDONESIA", "Factory fire: 3 dead, dozens missing",
     "A blaze tears through a candy factory in Banten, west Java. About "
     "50 workers are unaccounted for.",
     icon_factory),
    ("INDIA · NEPAL", "Nepal's PM meets Modi in Delhi",
     "Balendra Shah, PM since March, holds talks on flood rebuilding, "
     "trade and energy on his first trip abroad.",
     icon_flags),
    ("SPORT", "Liverpool 4–0 Man Utd: Pochettino routed on debut",
     "United lose a man after 8 minutes and concede twice by the 13th in "
     "the new boss's first match.",
     icon_ball),
]
f_kick = font(FB, 16)
f_card_h = font(FB, 22)
f_card_b = font(FR, 18)
gx, gy = 28, 376
cw, ch, gap = 310, 280, 14
for i, (kick, head, body, icon) in enumerate(cards):
    cx = gx + (i % 3) * (cw + gap)
    cy = gy + (i // 3) * (ch + gap)
    d.rectangle([cx, cy, cx + cw, cy + ch], outline=INK, width=2, fill=LIGHT)
    icon(d, cx + 16, cy + 14, 62)
    d.text((cx + 92, cy + 22), kick, font=f_kick, fill=RED)
    y = para(d, cx + 16, cy + 88, head, f_card_h, INK, cw - 32, 27)
    para(d, cx + 16, y + 8, body, f_card_b, INK, cw - 32, 22)

# ---- sources box (6th slot) ----
sx = gx + 2 * (cw + gap)
sy = gy + 1 * (ch + gap)
d.rectangle([sx, sy, sx + cw, sy + ch], outline=INK, width=2, fill=NAVY)
d.text((sx + 16, sy + 18), "THE DAY, AS REPORTED", font=f_kick, fill=(255, 210, 90))
para(d, sx + 16, sy + 52,
     "Events of 22–23 Nov 2026, as reported on 23 Nov.",
     font(FB, 18), LIGHT, cw - 32, 24)
para(d, sx + 16, sy + 142,
     "Sources: Reuters, CNN, BBC, DW, AP.",
     font(FR, 18), LIGHT, cw - 32, 24)
d.text((sx + 16, sy + ch - 40), "One image. One day. The world.",
     font=font(FB, 16), fill=(255, 210, 90))

# footer
d.line([28, 984, W - 28, 984], fill=INK, width=1)
d.text((28, 992), "THE WORLD TODAY — 23 NOVEMBER 2026",
       font=font(FB, 15), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
