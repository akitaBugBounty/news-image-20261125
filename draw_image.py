#!/usr/bin/env python3
"""Draw the 25 November 2026 front-page image, stdlib only.

Writes entry.png (1024x1024, RGB) next to this file.
PNG encoding is done by hand with zlib + struct; the 5x7 bitmap
font below is authored for this entry.
"""
import struct
import zlib
from pathlib import Path

W = 1024
H = 1024

# ---- palette -------------------------------------------------------------
PAPER = (245, 240, 230)
NAVY = (15, 32, 64)
NAVY2 = (27, 52, 96)
GOLD = (212, 175, 55)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
SKY = (168, 208, 232)
SEA = (27, 95, 138)
SEA2 = (18, 74, 110)
SAND = (222, 196, 138)
LAND = (106, 148, 84)
GREY = (120, 128, 138)
DARK = (16, 24, 40)
RED = (192, 38, 32)
ORANGE = (240, 120, 20)
YELLOW = (250, 204, 21)
GREEN = (46, 139, 74)
BLUE = (52, 110, 190)
LIGHTBLUE = (190, 220, 245)
TEAL = (40, 150, 150)

pixels = bytearray(W * H * 3)


def set_pixel(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        pixels[i] = color[0]
        pixels[i + 1] = color[1]
        pixels[i + 2] = color[2]


def fill_rect(x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = (xx - x0) * 3 + base
            pixels[i] = color[0]
            pixels[i + 1] = color[1]
            pixels[i + 2] = color[2]


def draw_rect_border(x, y, w, h, color, t=3):
    fill_rect(x, y, w, t, color)
    fill_rect(x, y + h - t, w, t, color)
    fill_rect(x, y, t, h, color)
    fill_rect(x + w - t, y, t, h, color)


def line(x0, y0, x1, y1, color, t=1):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        for ox in range(t):
            for oy in range(t):
                set_pixel(x0 + ox, y0 + oy, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def fill_circle(cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                set_pixel(xx, yy, color)


def circle_outline(cx, cy, r, color, t=2):
    for a in range(360):
        import math
        x = int(cx + r * math.cos(math.radians(a)))
        y = int(cy + r * math.sin(math.radians(a)))
        for ox in range(t):
            for oy in range(t):
                set_pixel(x + ox, y + oy, color)


def fill_polygon(points, color):
    # Scanline fill.
    ys = [p[1] for p in points]
    for y in range(min(ys), max(ys) + 1):
        nodes = []
        n = len(points)
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            if y1 == y2:
                continue
            if (y >= min(y1, y2)) and (y < max(y1, y2)):
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                nodes.append(x)
        nodes.sort()
        for i in range(0, len(nodes) - 1, 2):
            for x in range(int(nodes[i]), int(nodes[i + 1]) + 1):
                set_pixel(x, y, color)


def starburst(cx, cy, r1, r2, color):
    import math
    pts = []
    for i in range(16):
        ang = math.radians(i * 22.5 - 90)
        r = r1 if i % 2 == 0 else r2
        pts.append((int(cx + r * math.cos(ang)), int(cy + r * math.sin(ang))))
    fill_polygon(pts, color)


# ---- 5x7 bitmap font (authored for this entry) ---------------------------
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}


def text_width(text, scale, spacing=None):
    if spacing is None:
        spacing = max(1, scale // 2)
    if not text:
        return 0
    return len(text) * (5 * scale + spacing) - spacing


def draw_text(text, x, y, scale, color, spacing=None):
    if spacing is None:
        spacing = max(1, scale // 2)
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    fill_rect(cx + col * scale, y + row * scale, scale, scale, color)
        cx += 5 * scale + spacing
    return cx


def draw_text_centered(text, cx, y, scale, color):
    w = text_width(text, scale)
    draw_text(text, cx - w // 2, y, scale, color)


def draw_lines_centered(lines, cx, y, scale, color, gap=6):
    for i, ln in enumerate(lines):
        draw_text_centered(ln, cx, y + i * (7 * scale + gap), scale, color)


# ---- PNG encoder -----------------------------------------------------------
def encode_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(pixels[y * W * 3:(y + 1) * W * 3])
    compressed = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        c += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return c

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", ihdr)
    data += chunk(b"IDAT", compressed)
    data += chunk(b"IEND", b"")
    Path(path).write_bytes(data)


# ---- scene -----------------------------------------------------------------
def draw_masthead():
    fill_rect(0, 0, W, 118, NAVY)
    fill_rect(0, 112, W, 6, GOLD)
    draw_text_centered("THE WORLD IN ONE IMAGE", W // 2, 18, 8, WHITE)
    draw_text_centered("WEDNESDAY 25 NOVEMBER 2026", W // 2, 84, 3, GOLD)


def draw_lead_panel():
    x, y, w, h = 20, 130, 984, 410
    fill_rect(x, y, w, h, WHITE)
    draw_rect_border(x, y, w, h, BLACK, 4)
    # Headline block.
    fill_rect(x + 4, y + 4, w - 8, 82, PAPER)
    draw_lines_centered(["MINES HIT TANKERS", "IN STRAIT OF HORMUZ"], x + w // 2, y + 12, 5, BLACK, gap=4)
    # Scene: sky, strait, sea.
    sy = y + 90
    fill_rect(x + 4, sy, w - 8, 150, SKY)
    fill_rect(x + 4, sy + 150, w - 8, 166, SEA)
    # Coastlines: land masses left and right forming the strait.
    fill_polygon([(x + 4, sy), (x + 190, sy), (x + 150, sy + 90), (x + 110, sy + 150),
                  (x + 4, sy + 150)], SAND)
    fill_polygon([(x + 4, sy + 30), (x + 150, sy + 30), (x + 120, sy + 90),
                  (x + 90, sy + 150), (x + 4, sy + 150)], LAND)
    fill_polygon([(x + w - 4, sy), (x + w - 210, sy), (x + w - 170, sy + 90),
                  (x + w - 120, sy + 150), (x + w - 4, sy + 150)], SAND)
    fill_polygon([(x + w - 4, sy + 30), (x + w - 170, sy + 30), (x + w - 140, sy + 90),
                  (x + w - 100, sy + 150), (x + w - 4, sy + 150)], LAND)
    # Sun.
    fill_circle(x + 520, sy + 42, 26, YELLOW)
    circle_outline(x + 520, sy + 42, 26, ORANGE, 3)
    # Waves.
    for wx in range(x + 140, x + w - 140, 70):
        line(wx, sy + 175, wx + 34, sy + 175, WHITE, 3)
        line(wx + 18, sy + 205, wx + 52, sy + 205, LIGHTBLUE, 3)
    # Oil tanker (centre of the strait).
    hx, hy = x + 330, sy + 210
    fill_rect(hx, hy, 340, 42, BLACK)          # hull
    fill_rect(hx, hy + 34, 340, 8, RED)        # waterline
    fill_rect(hx + 20, hy - 34, 150, 34, RED)  # deck tanks
    fill_rect(hx + 185, hy - 34, 70, 34, WHITE)
    fill_rect(hx + 270, hy - 62, 52, 62, WHITE)  # bridge
    fill_rect(hx + 278, hy - 54, 36, 12, NAVY2)
    fill_rect(hx + 20, hy - 52, 18, 18, YELLOW)  # funnel base
    line(hx + 29, hy - 52, hx + 18, hy - 78, GREY, 4)
    fill_circle(hx + 16, hy - 82, 8, GREY)
    fill_circle(hx + 8, hy - 94, 6, GREY)
    # Mines: spiked black spheres in the water.
    for mx, my in [(hx - 62, sy + 252), (hx + 380, sy + 262), (hx + 210, sy + 256)]:
        fill_circle(mx, my, 16, BLACK)
        for dx, dy in [(-20, 0), (20, 0), (0, -20), (0, 20), (-14, -14), (14, -14), (-14, 14), (14, 14)]:
            line(mx, my, mx + dx, my + dy, BLACK, 3)
        fill_circle(mx, my, 6, GREY)
    # Explosion where a mine hit the tanker bow.
    ex, ey = hx - 40, sy + 232
    starburst(ex, ey, 44, 20, ORANGE)
    starburst(ex, ey, 28, 12, YELLOW)
    starburst(ex, ey, 14, 6, RED)
    # Caption inside the scene.
    draw_text_centered("3 TANKERS HIT * STRAIT OF HORMUZ", x + w // 2, sy + 288, 2, WHITE)


def draw_cop_panel(x, y, w, h):
    fill_rect(x, y, w, h, WHITE)
    draw_rect_border(x, y, w, h, BLACK, 4)
    draw_lines_centered(["COP31", "COLLAPSES", "WITHOUT A", "DEAL"], x + w // 2, y + 10, 4, BLACK, gap=3)
    # Skyline.
    base = y + h - 8
    for bx, bh, col in [(x + 12, 62, GREY), (x + 62, 92, NAVY2), (x + 112, 54, GREY),
                        (x + 162, 84, BLUE), (x + 212, 48, GREY), (x + 258, 70, NAVY2)]:
        fill_rect(bx, base - bh, 42, bh, col)
        fill_rect(bx + 6, base - bh + 8, 8, 8, YELLOW)
        fill_rect(bx + 24, base - bh + 8, 8, 8, YELLOW)
    # Cracked globe above the skyline.
    gx, gy = x + w // 2, y + 178
    fill_circle(gx, gy, 34, BLUE)
    fill_circle(gx - 10, gy - 8, 14, GREEN)
    fill_circle(gx + 12, gy + 12, 10, GREEN)
    circle_outline(gx, gy, 34, BLACK, 3)
    line(gx - 8, gy - 32, gx + 4, gy - 10, BLACK, 3)
    line(gx + 4, gy - 10, gx - 10, gy + 12, BLACK, 3)
    line(gx - 10, gy + 12, gx + 8, gy + 32, BLACK, 3)
    # Wilting leaf.
    line(gx - 52, gy + 42, gx - 78, gy + 66, GREEN, 4)
    fill_polygon([(gx - 78, gy + 66), (gx - 56, gy + 52), (gx - 66, gy + 78)], GREEN)


def draw_cyber_panel(x, y, w, h):
    fill_rect(x, y, w, h, DARK)
    draw_rect_border(x, y, w, h, BLACK, 4)
    draw_lines_centered(["CIA AND", "ODNI HIT", "BY CYBER", "BREACH"], x + w // 2, y + 10, 4, WHITE, gap=3)
    # Shield with a crack.
    sx, sy = x + w // 2, y + 196
    fill_polygon([(sx - 38, sy - 30), (sx + 38, sy - 30), (sx + 38, sy + 8),
                  (sx, sy + 48), (sx - 38, sy + 8)], BLUE)
    fill_polygon([(sx - 28, sy - 22), (sx + 28, sy - 22), (sx + 28, sy + 4),
                  (sx, sy + 36), (sx - 28, sy + 4)], LIGHTBLUE)
    line(sx - 6, sy - 28, sx + 6, sy - 6, WHITE, 3)
    line(sx + 6, sy - 6, sx - 8, sy + 14, WHITE, 3)
    line(sx - 8, sy + 14, sx + 4, sy + 38, WHITE, 3)
    # Circuit / binary motif.
    line(x + 16, y + 178, x + 56, y + 178, TEAL, 3)
    line(x + 56, y + 178, x + 56, y + 214, TEAL, 3)
    fill_circle(x + 56, y + 214, 5, TEAL)
    line(x + w - 16, y + 178, x + w - 56, y + 178, TEAL, 3)
    line(x + w - 56, y + 178, x + w - 56, y + 214, TEAL, 3)
    fill_circle(x + w - 56, y + 214, 5, TEAL)
    draw_text("0101", x + 18, y + h - 28, 2, TEAL)
    draw_text("1010", x + w - 62, y + h - 28, 2, TEAL)


def draw_iowa_panel(x, y, w, h):
    fill_rect(x, y, w, h, WHITE)
    draw_rect_border(x, y, w, h, BLACK, 4)
    draw_lines_centered(["IOWA BLAST", "EVACUATION"], x + w // 2, y + 10, 4, BLACK, gap=3)
    # Explosion flash.
    ex, ey = x + w // 2, y + 150
    starburst(ex, ey, 58, 26, ORANGE)
    starburst(ex, ey, 38, 18, YELLOW)
    starburst(ex, ey, 18, 8, RED)
    fill_circle(ex, ey, 10, WHITE)
    # Smoke.
    fill_circle(ex - 52, ey - 34, 14, GREY)
    fill_circle(ex + 52, ey - 38, 12, GREY)
    fill_circle(ex + 62, ey - 58, 9, GREY)
    # Evacuation road + sign.
    fill_polygon([(x + 12, y + h - 8), (x + 130, y + 208), (x + 190, y + 208), (x + w - 12, y + h - 8)], GREY)
    line(x + w // 2, y + 212, x + w // 2, y + h - 10, YELLOW, 4)
    fill_rect(x + 22, y + h - 62, 74, 44, YELLOW)
    draw_rect_border(x + 22, y + h - 62, 74, 44, BLACK, 3)
    draw_text("EVAC", x + 30, y + h - 50, 2, BLACK)
    draw_text("!", x + 30, y + h - 34, 2, RED)


def draw_ticker():
    # Bottom ticker strip: every remaining headline, in full, three lines.
    # Line widths at scale 2 stay inside the 984 px strip when centred.
    x, y, w, h = 20, 830, 984, 88
    fill_rect(x, y, w, h, BLACK)
    draw_rect_border(x, y, w, h, BLACK, 3)
    draw_text_centered("HUAWEI GUILTY ON 10 COUNTS * GIULIANI GETS MEDAL OF FREEDOM", W // 2, y + 8, 2, YELLOW)
    draw_text_centered("RUSSIAN MISSILES BREACH POLISH AIRSPACE * HOUTHI DRONE HITS RIYADH TOWER, 11 HURT", W // 2, y + 32, 2, WHITE)
    draw_text_centered("WHO FLEES EBOLA HOSPITAL IN CONGO * THANKSGIVING RUSH * GAZA: POLLUTION RISK IN 99%", W // 2, y + 56, 2, WHITE)


def draw_footer():
    y = 930
    fill_rect(20, y, 984, 80, PAPER)
    draw_rect_border(20, y, 984, 80, BLACK, 3)
    # Small globe motif (left).
    gx, gy = 72, y + 40
    fill_circle(gx, gy, 28, BLUE)
    fill_circle(gx - 8, gy - 6, 11, GREEN)
    fill_circle(gx + 10, gy + 10, 8, GREEN)
    circle_outline(gx, gy, 28, BLACK, 3)
    # Headline (centre).
    draw_text_centered("UKRAINE: DRONE HITS CARGO SHIP AT SEA", W // 2 + 30, y + 14, 3, BLACK)
    draw_text_centered("GULF OF FINLAND * OFF LIBYA", W // 2 + 30, y + 44, 2, NAVY2)
    # Cargo ship + drone (right).
    sx, sy = 880, y + 52
    fill_rect(sx, sy, 96, 16, BLACK)
    fill_rect(sx + 8, sy - 16, 34, 16, RED)
    fill_rect(sx + 48, sy - 16, 30, 16, BLUE)
    fill_rect(sx + 66, sy - 32, 20, 16, WHITE)
    line(sx + 30, sy - 16, sx + 30, sy - 40, BLACK, 3)
    fill_circle(sx + 22, sy - 44, 4, BLACK)
    fill_circle(sx + 38, sy - 44, 4, BLACK)
    line(sx + 22, sy - 44, sx + 38, sy - 44, BLACK, 2)


def main():
    fill_rect(0, 0, W, H, PAPER)
    draw_masthead()
    draw_lead_panel()
    draw_cop_panel(20, 555, 316, 260)
    draw_cyber_panel(344, 555, 316, 260)
    draw_iowa_panel(668, 555, 336, 260)
    draw_ticker()
    draw_footer()
    out = Path(__file__).resolve().parent / "entry.png"
    encode_png(out)
    print(str(out))


if __name__ == "__main__":
    main()
