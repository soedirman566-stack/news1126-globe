#!/usr/bin/env python3
"""Draw "The Daily Globe" front page for Thursday 26 November 2026.

A one-page broadsheet that sums up the day's world news as a single
1024x1024 PNG: the Hormuz tanker crisis as the lead story, Ukraine and
Cairo beside it, US-India tariffs and the Shenzhou-24 launch below, a
markets strip and a world briefs column along the bottom.

Everything is drawn with Pillow primitives -- masthead, rules, the
hand-drawn strait-of-Hormuz panel, headlines and columns -- so the page
is an original composition, not a photograph or a collage.

Run locally:  python3 make_front_page.py   (writes entry.png beside it)
The grader never runs this file; main.py copies the committed entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36
RIGHT = W - MARGIN

PAPER = (246, 241, 230)
INK = (18, 18, 20)
FAINT = (92, 86, 74)
RED = (164, 22, 27)
NAVY = (15, 40, 66)
SEA = (24, 60, 96)
LAND = (198, 170, 122)
FLAME = (233, 120, 32)
GOLD = (214, 164, 40)
WHITE = (250, 248, 242)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def serif(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif_text(size):
    return font("DejaVuSerif.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def sans_bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def mono_bold(size):
    return font("DejaVuSansMono-Bold.ttf", size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap: return the lines of text that fit in width px."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading):
    """Draw wrapped text at xy; return the y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, weight=3, fill=INK, x0=MARGIN, x1=RIGHT):
    draw.rectangle([x0, y, x1, y + weight - 1], fill=fill)


def kicker(draw, xy, text, fill=RED):
    draw.text(xy, text, font=sans_bold(21), fill=fill)


# ---------------------------------------------------------------- masthead

def draw_masthead(d):
    d.text((MARGIN, 14), "VOL. I · No. 1", font=sans_bold(15), fill=FAINT)
    tag = "ONE PAGE · THE WHOLE DAY"
    d.text((RIGHT - d.textlength(tag, font=sans_bold(15)), 14),
           tag, font=sans_bold(15), fill=FAINT)
    rule(d, 40, 2)
    name = "The Daily Globe"
    f = serif(88)
    d.text(((W - d.textlength(name, font=f)) / 2, 44), name, font=f, fill=INK)
    rule(d, 144, 5)
    # Date bar: the day, named as loudly as the masthead allows.
    d.rectangle([MARGIN, 156, RIGHT, 202], fill=INK)
    date = "THURSDAY 26 NOVEMBER 2026"
    f = sans_bold(33)
    d.text(((W - d.textlength(date, font=f)) / 2, 163), date, font=f, fill=WHITE)
    d.text((MARGIN + 14, 170), "LATE", font=sans_bold(18), fill=GOLD)
    d.text((RIGHT - 14 - d.textlength("WORLD NEWS", font=sans_bold(18)), 170),
           "WORLD NEWS", font=sans_bold(18), fill=GOLD)


# ------------------------------------------------------- lead illustration

def draw_hormuz_panel(d, x0, y0, x1, y1):
    """A stylised map panel: the strait, two coasts, a tanker, mines, fire."""
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    # Land masses: Iran as a band along the top, Arabia/Oman along the
    # bottom, so a clear diagonal channel of sea runs between them.
    d.polygon([(x0, y0), (x1, y0), (x1, y0 + 42),
               (x0 + 360, y0 + 64), (x0 + 140, y0 + 50), (x0, y0 + 68)],
              fill=LAND)
    d.polygon([(x0, y1), (x0, y1 - 50), (x0 + 190, y1 - 62),
               (x0 + 430, y1 - 42), (x1, y1 - 80), (x1, y1)], fill=LAND)
    # The Musandam tip poking up from Oman into the narrows.
    d.polygon([(x0 + 428, y1), (x0 + 484, y0 + 102), (x0 + 542, y1)],
              fill=LAND)
    d.text((x0 + 26, y0 + 14), "I R A N", font=sans_bold(22), fill=INK)
    d.text((x0 + 30, y1 - 36), "O M A N", font=sans_bold(22), fill=INK)
    # Dashed shipping lane through the channel.
    for i in range(9):
        sx = x0 + 34 + i * 58
        sy = y0 + 92 - (i % 3) * 4
        d.line([sx, sy, sx + 30, sy - 3], fill=WHITE, width=3)
    # The tanker, mid-channel: hull, deck line, superstructure, funnel.
    tx, ty = x0 + 150, y0 + 66
    d.polygon([(tx, ty + 24), (tx + 156, ty + 24), (tx + 140, ty + 42),
               (tx + 14, ty + 42)], fill=(30, 30, 34))
    d.rectangle([tx + 8, ty + 17, tx + 148, ty + 25], fill=(58, 60, 66))
    d.rectangle([tx + 112, ty - 6, tx + 140, ty + 18], fill=(226, 222, 210))
    d.rectangle([tx + 120, ty - 17, tx + 133, ty - 6], fill=RED)
    for cx in (26, 54, 82):
        d.ellipse([tx + cx, ty + 6, tx + cx + 17, ty + 17], outline=GOLD, width=3)
    # The explosion where the mine went off, just off the bow.
    ex, ey = tx + 182, ty + 32
    for dx, dy in ((-38, -22), (-44, 4), (-34, 28), (30, -30), (42, -6),
                   (34, 24)):
        d.line([ex, ey, ex + dx, ey + dy], fill=FLAME, width=5)
    for r, col in ((27, FLAME), (18, (244, 178, 60)), (10, (250, 226, 150))):
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)
    d.line([ex - 40, ey + 24, ex + 36, ey + 27], fill=WHITE, width=3)
    # Two more mines bobbing in the lane.
    for mx, my in ((x0 + 66, y0 + 110), (x0 + 524, y0 + 84)):
        d.ellipse([mx - 13, my - 13, mx + 13, my + 13], fill=(24, 24, 28))
        for dx, dy in ((-20, 0), (20, 0), (0, -20), (0, 20),
                       (-14, -14), (14, -14), (-14, 14), (14, 14)):
            d.line([mx, my, mx + dx, my + dy], fill=(24, 24, 28), width=4)
    label = "STRAIT OF HORMUZ"
    f = sans_bold(20)
    d.rectangle([x0 + 330, y1 - 36, x0 + 330 + d.textlength(label, font=f) + 18,
                 y1 - 8], fill=NAVY)
    d.text((x0 + 339, y1 - 33), label, font=f, fill=WHITE)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)


# ------------------------------------------------------------- page layout

LEAD_W = 596           # lead column: x MARGIN .. MARGIN+LEAD_W
RAIL_X = 664           # right rail starts here
RAIL_W = RIGHT - RAIL_X
TOP = 218              # first content row, below the date bar


def draw_lead(d):
    y = TOP
    kicker(d, (MARGIN, y), "STRAIT OF HORMUZ · ENERGY CRISIS")
    y += 30
    y = text_block(d, (MARGIN, y),
                   "Iran: Tankers Strike Mines in the Strait of Hormuz",
                   serif(50), INK, LEAD_W, 57)
    y += 10
    draw_hormuz_panel(d, MARGIN, y, MARGIN + LEAD_W, y + 180)
    y += 188
    text_block(d, (MARGIN, y),
               "A tanker burns after striking a mine in the strait — the "
               "chokepoint for a fifth of the world's seaborne oil. Tehran "
               "says a container ship was also attacked and disabled.",
               sans(16), FAINT, LEAD_W, 21)


def draw_rail(d):
    y = TOP
    kicker(d, (RAIL_X, y), "UKRAINE WAR")
    y += 28
    y = text_block(d, (RAIL_X, y),
                   "Kyiv Hits Russian Airfield, Refineries",
                   serif(28), INK, RAIL_W, 34)
    y += 4
    y = text_block(d, (RAIL_X, y),
                   "Ukraine said its strikes destroyed five jets at a "
                   "Russian airfield and set two Samara refineries ablaze. "
                   "Russian attacks left five regions without power, and "
                   "Poland urged NATO to down Russian missiles at its "
                   "border.",
                   sans(16), INK, RAIL_W, 21)
    y += 12
    d.line([RAIL_X, y, RIGHT, y], fill=INK, width=2)
    y += 10
    kicker(d, (RAIL_X, y), "CAIRO · EGYPT")
    y += 28
    y = text_block(d, (RAIL_X, y),
                   "30 Die in Cairo Fuel-Tanker Fire",
                   serif(28), INK, RAIL_W, 34)
    y += 4
    text_block(d, (RAIL_X, y),
               "A petroleum tanker overturned and burst into flames on "
               "the Ring Road in Giza's Warraq district. The health "
               "ministry said at least 30 died and 15 were injured.",
               sans(16), INK, RAIL_W, 21)


def draw_second_row(d):
    y = 702
    rule(d, y - 12, 3)
    half = (RIGHT - MARGIN - 28) // 2
    kicker(d, (MARGIN, y), "TRADE · WASHINGTON")
    y2 = text_block(d, (MARGIN, y + 26),
                    "US Proposes Tariffs of Up to 25% on India",
                    serif(26), INK, half, 31)
    text_block(d, (MARGIN, y2 + 2),
               "India is among 14 economies facing Section 301 duties "
               "over 'excess capacity', with 17% on offer if a trade "
               "deal is struck. New Delhi rejects the finding outright.",
               sans(15), INK, half, 20)
    x2 = MARGIN + half + 28
    kicker(d, (x2, y), "SPACE · CHINA")
    y2 = text_block(d, (x2, y + 26),
                    "Shenzhou-24 Lifts Off With a First Foreign Astronaut",
                    serif(26), INK, half, 31)
    text_block(d, (x2, y2 + 2),
               "China's crewed Shenzhou-24 mission blasted off carrying "
               "a Pakistani citizen — the first astronaut from another "
               "country to fly on a Chinese spacecraft.",
               sans(15), INK, half, 20)


def draw_markets(d):
    y = 864
    d.rectangle([MARGIN, y, RIGHT, y + 36], fill=INK)
    line = ("MARKETS · BRENT $94.84 ▲0.2% · WTI $84.23 ▲0.7% · "
            "GOLD $3,576 ▲ · WALL ST CLOSED — THANKSGIVING")
    f = mono_bold(16)
    d.text(((W - d.textlength(line, font=f)) / 2, y + 8), line,
           font=f, fill=WHITE)


BRIEFS = [
    "JERUSALEM — Judges urge dropping the bribery charge against "
    "Netanyahu.",
    "CARTAGENA — Police free 30 hostages after a 17-hour supermarket "
    "siege.",
    "HONIARA — Australia and the Solomon Islands sign a sweeping "
    "new treaty.",
    "MISSISSIPPI — Six die, two of them children, in a plane crash "
    "off the coast.",
    "SAN JUAN — Puerto Rico's Jennifer Barreto is crowned Miss "
    "Universe 2026.",
    "LAGOS — Nigeria seizes $220m of meth; five Mexican suspects "
    "held.",
]


def draw_briefs(d):
    y = 908
    rule(d, y, 3)
    d.text((MARGIN, y + 6), "THE WORLD IN BRIEF",
           font=sans_bold(17), fill=INK)
    y += 32
    col_w = (RIGHT - MARGIN - 2 * 24) // 3
    for i, brief in enumerate(BRIEFS):
        cx = MARGIN + (i % 3) * (col_w + 24)
        cy = y + (i // 3) * 40
        text_block(d, (cx, cy), brief, sans(14), INK, col_w, 16)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_rail(d)
    draw_second_row(d)
    draw_markets(d)
    draw_briefs(d)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
