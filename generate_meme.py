#!/usr/bin/env python3
"""Render the GTA6-MEME-X-01 v2 meme: a parcel delivery-tracking notice.

Pure PIL, deterministic: no randomness, no timestamps, no network.
Output: assets/meme.png, 1200x675, <=1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(ASSETS, "meme.png")

W, H = 1200, 675

BG = (233, 231, 242)          # soft lavender-gray backdrop
CARD = (255, 255, 255)        # clean white card
NAVY = (27, 31, 59)           # dark navy text
GRAY = (96, 99, 122)          # muted gray text
MAGENTA = (230, 0, 126)       # make.fun magenta ~#E6007E
LIGHT_LINE = (226, 224, 236)  # hairline divider
TRACK_BG = (243, 242, 248)    # progress track
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- card ----
    d.rounded_rectangle([24, 16, 1176, 659], radius=20, fill=CARD)

    # ---- header ----
    ghost = Image.open(os.path.join(ASSETS, "ghost.png")).convert("RGBA")
    ghost_h = ghost.resize((84, 84), Image.LANCZOS)
    img.paste(ghost_h, (48, 34), ghost_h)

    f_word = font(BOLD, 46)
    d.text((142, 52), "make.fun", font=f_word, fill=NAVY)

    f_label = font(BOLD, 26)
    f_track = font(BOLD, 32)
    label = "TRACK YOUR PARCEL"
    track = "GTA6-2013-VC"
    d.text((1152 - text_w(d, label, f_label), 40), label, font=f_label, fill=GRAY)
    d.text((1152 - text_w(d, track, f_track), 72), track, font=f_track, fill=MAGENTA)

    # divider
    d.line([(48, 138), (1152, 138)], fill=LIGHT_LINE, width=2)

    # ---- title + subheader ----
    f_title = font(BOLD, 60)
    d.text((48, 152), "GTA VI \u2014 OUT FOR DELIVERY", font=f_title, fill=NAVY)
    f_sub = font(REG, 30)
    d.text((48, 224), "13 years in transit \u2014 finally here.", font=f_sub, fill=GRAY)

    # ---- timeline ----
    rows = [
        ("17 SEP 2013", "Order placed", "Rockstar Depot, Vice City", False),
        ("02 FEB 2022", "Parcel being prepared", "Rockstar HQ", False),
        ("05 DEC 2023", "Departed facility", "Trailer #1 shipped", False),
        ("06 MAY 2025", "Delayed in transit", "New ETA 19 Nov 2026", False),
        ("19 NOV 2026", "Out for delivery", "Leonida", False),
        ("19 NOV 2026", "DELIVERED", "Signed for by my AI agent", True),
    ]
    x_line = 62
    y0 = 288
    row_h = 40
    y_first = y0 + 14
    y_last = y0 + 5 * row_h + 14
    d.line([(x_line, y_first), (x_line, y_last)], fill=LIGHT_LINE, width=3)

    f_date = font(BOLD, 26)
    f_status = font(BOLD, 26)
    f_loc = font(REG, 26)
    for i, (date, status, loc, done) in enumerate(rows):
        cy = y0 + i * row_h + 14
        color = MAGENTA if done else NAVY
        r = 10 if done else 8
        d.ellipse([x_line - r, cy - r, x_line + r, cy + r],
                  fill=color if done else WHITE,
                  outline=(MAGENTA if done else NAVY), width=3)
        d.text((88, cy - 14), date, font=f_date, fill=color)
        d.text((300, cy - 14), status, font=f_status, fill=color)
        d.text((640, cy - 14), loc, font=f_loc, fill=GRAY if not done else MAGENTA)

    # ---- progress bar ----
    f_prog = font(BOLD, 26)
    prog_label = "6 of 6 checkpoints \u2014 DELIVERED"
    d.text((48, 536), prog_label, font=f_prog, fill=MAGENTA)
    d.rounded_rectangle([48, 570, 1152, 588], radius=9, fill=TRACK_BG)
    d.rounded_rectangle([48, 570, 1152, 588], radius=9, fill=MAGENTA)

    # ---- footer banner ----
    d.rounded_rectangle([24, 600, 1176, 659], radius=18, fill=MAGENTA)
    # square off the top edge of the banner so it meets the card cleanly
    d.rectangle([24, 600, 1176, 620], fill=MAGENTA)
    f_foot = font(BOLD, 32)
    foot = "DELIVERY FEE PAID BY MY AI AGENT ON MAKE.FUN"
    d.text((48, 616), foot, font=f_foot, fill=WHITE)
    ghost_f = ghost.resize((40, 40), Image.LANCZOS)
    img.paste(ghost_f, (1096, 609), ghost_f)

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
