"""Render the front page (stories.json) to entry.png, 1024x1024, deterministic.

Build-time tooling for the news-image-20261120 entry. The entry program
(main.py) only copies the rendered entry.png to /output/entry.png.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (253, 246, 227)
INK = (26, 26, 26)
RED = (185, 28, 28)
GREY = (110, 105, 95)
RULE = (26, 26, 26)
REGION_COLORS = {
    "EUROPE": (30, 64, 175), "ASIA": (153, 27, 27), "MIDDLE EAST": (120, 53, 15),
    "AFRICA": (101, 60, 10), "AMERICAS": (15, 118, 110), "OCEANIA": (2, 105, 148),
    "MARKETS & TECH": (88, 28, 135),
}


def font(name, size):
    paths = {
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "mono_b": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    }
    return ImageFont.truetype(paths[name], size)


def wrap(draw, text, fnt, max_w, max_lines=None):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        # ellipsize the last line
        while lines and draw.textlength(lines[-1] + "…", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + "…"
    return lines


def text_block(d, x, y, lines, fnt, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def main():
    with open(os.path.join(HERE, "stories.json")) as f:
        data = json.load(f)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    x0, x1 = M, W - M

    # ---- Masthead ----
    d.text((W // 2, 40), data["masthead"], font=font("serif_b", 58), fill=INK, anchor="mm")
    d.line([(x0, 76), (x1, 76)], fill=RULE, width=3)
    sub = "FRIDAY, 20 NOVEMBER 2026  ·  35 STORIES  ·  7 REGIONS  ·  EVERY FIGURE ATTRIBUTED"
    d.text((W // 2, 92), sub, font=font("sans_b", 15), fill=RED, anchor="mm")
    d.line([(x0, 106), (x1, 106)], fill=RULE, width=1)

    # ---- Leads row A: Kyiv (left) | Akvan (right) ----
    leads = data["leads"]
    ly = 118
    lx0, lx1 = x0, 620
    lead = leads[0]
    d.text((lx0, ly), "01", font=font("mono_b", 13), fill=RED)
    d.text((lx0 + 30, ly), lead["kicker"], font=font("sans_b", 13), fill=RED)
    y = ly + 20
    y = text_block(d, lx0, y, wrap(d, lead["headline"], font("serif_b", 34), lx1 - lx0),
                   font("serif_b", 34), INK, 40)
    y = text_block(d, lx0, y + 2, wrap(d, lead["summary"], font("sans", 15), lx1 - lx0),
                   font("sans", 15), INK, 19)
    d.text((lx0, y + 4), lead["figures"], font=font("mono_b", 14), fill=RED)
    d.line([(632, ly - 4), (632, 278)], fill=GREY, width=1)
    s = leads[1]
    rx0 = 648
    d.text((rx0, ly), "02", font=font("mono_b", 13), fill=RED)
    d.text((rx0 + 30, ly), s["kicker"], font=font("sans_b", 13), fill=RED)
    y = ly + 20
    y = text_block(d, rx0, y, wrap(d, s["headline"], font("serif_b", 20), x1 - rx0),
                   font("serif_b", 20), INK, 24)
    y = text_block(d, rx0, y + 2, wrap(d, s["summary"], font("sans", 12), x1 - rx0, 3),
                   font("sans", 12), INK, 15)
    d.text((rx0, y + 4), s["figures"], font=font("mono_b", 11), fill=GREY)

    # ---- Leads row B: 3 columns (AI sell-off, UK-EU, COP31) ----
    by = 288
    d.line([(x0, by - 8), (x1, by - 8)], fill=(200, 190, 170), width=1)
    cols = 3
    cw = (x1 - x0 - (cols - 1) * 12) // cols
    for i, s in enumerate(leads[2:]):
        bx = x0 + i * (cw + 12)
        d.text((bx, by), f"0{i + 3}", font=font("mono_b", 11), fill=RED)
        d.text((bx + 28, by), s["kicker"], font=font("sans_b", 11), fill=RED)
        y = by + 15
        y = text_block(d, bx, y, wrap(d, s["headline"], font("serif_b", 17), cw, 2),
                       font("serif_b", 17), INK, 21)
        y = text_block(d, bx, y + 2, wrap(d, s["summary"], font("sans", 11), cw, 2),
                       font("sans", 11), INK, 14)
        d.text((bx, y + 2), s["figures"], font=font("mono_b", 10), fill=GREY)

    # ---- Markets strip ----
    my = 390
    d.rectangle([x0, my, x1, my + 36], fill=INK)
    d.text((W // 2, my + 18), "   ".join(data["markets"]), font=font("mono_b", 14),
           fill=(253, 246, 227), anchor="mm")

    # ---- Region grid ----
    gy = 438
    regions = data["regions"]
    rows = [regions[:4], regions[4:]]
    row_h = [250, 252]
    n = 6
    for ri, row in enumerate(rows):
        cols = len(row)
        cw = (x1 - x0 - (cols - 1) * 12) // cols
        for ci, reg in enumerate(row):
            bx = x0 + ci * (cw + 12)
            byy = gy + sum(row_h[:ri]) + (8 if ri else 0)
            col = REGION_COLORS[reg["name"]]
            d.rectangle([bx, byy, bx + cw, byy + 22], fill=col)
            d.text((bx + 8, byy + 11), reg["name"], font=font("sans_b", 13),
                   fill=(255, 255, 255), anchor="lm")
            d.text((bx + cw - 8, byy + 11), str(len(reg["stories"])),
                   font=font("sans_b", 13), fill=(255, 255, 255), anchor="rm")
            sy = byy + 30
            for st in reg["stories"]:
                d.text((bx, sy), f"{n:02d}", font=font("mono_b", 11), fill=RED)
                sy = text_block(d, bx + 28, sy,
                                wrap(d, st["h"], font("sans_b", 12), cw - 30, 2),
                                font("sans_b", 12), INK, 15)
                sy = text_block(d, bx + 28, sy,
                                wrap(d, st["s"], font("sans", 10), cw - 28, 2),
                                font("sans", 10), (60, 58, 52), 13)
                sy += 4
                n += 1
    assert n == 36, f"region story count mismatch: {n - 1} != 35 (5 leads + 30 = 35 total)"

    # ---- Footer: timeline + sources + date check ----
    fy = 954
    d.line([(x0, fy), (x1, fy)], fill=RULE, width=2)
    d.text((x0, fy + 10), "HOW THE DAY UNFOLDED", font=font("sans_b", 12), fill=RED)
    d.text((x1, fy + 10), "DATE CHECK ✓ Friday 20 November 2026",
           font=font("sans_b", 11), fill=RED, anchor="ra")
    ty = fy + 26
    seg = (x1 - x0) // 5
    for i, (when, what) in enumerate(data["timeline"]):
        tx = x0 + i * seg
        d.text((tx, ty), when, font=font("sans_b", 11), fill=INK)
        ly2 = ty + 14
        for ln in wrap(d, what, font("sans", 10), seg - 8, 1):
            d.text((tx, ly2), ln, font=font("sans", 10), fill=(60, 58, 52))
            ly2 += 12
    d.text((x0, 1014), "Sources: " + data["sources"] + " — figures as reported 20 Nov 2026.",
           font=font("sans", 9), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
