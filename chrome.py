"""Shared chrome for the v2 look: left azure rail with a vertical stepper, kicker + title, indigo lower-third caption."""
import math
from functools import lru_cache
from PIL import Image, ImageDraw
from lib import *
import content

NAVS = [s["nav"] for s in content.SCENES]
RAIL = 104
CX0, CX1 = 150, 1870          # content area (left edge after the rail, right margin)
SLATE = (86, 100, 122)


@lru_cache(None)
def canvas():
    """Near-white canvas with a faint azure dot matrix in the top-right corner."""
    img = Image.new("RGB", (W, H), BG)
    ov = SS(W, H, k=1)
    for y in range(36, 520, 26):
        for x in range(1320, W, 26):
            a = int(52 * (1 - (y - 36) / 484) * min(1.0, (x - 1320) / 320))
            if a > 3: ov.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(*AZURE, a))
    d = ov.done(); img.paste(d, (0, 0), d); return img


@lru_cache(None)
def shell(nav):
    img = canvas().copy()
    col = Image.new("RGB", (1, H))
    for y in range(H): col.putpixel((0, y), mix(AZURE, VIOLET, y / H))
    img.paste(col.resize((RAIL, H)), (0, 0))
    ov = SS(W, 130)
    ov.rr((14, 22, RAIL - 14, 58), 10, fill=WHITE); ov.text((RAIL / 2, 41), "SAP", 22, AZURE, bold=True, anchor="mm")
    ov.rr((9, 66, RAIL - 9, 100), 10, fill=ACC); ov.text((RAIL / 2, 84), "Agents", 18, WHITE, bold=True, anchor="mm")
    k = NAVS.index(nav)
    ov.text((CX0, 44), f"{k + 1:02d}   {nav.upper()}", 20, ACC, bold=True, spacing=2)
    o = ov.done(); img.paste(o, (0, 0), o)
    st = SS(RAIL, H - 130); n = len(NAVS); y0, step = 40, 56
    st.line([(RAIL / 2, y0), (RAIL / 2, y0 + (n - 1) * step)], (255, 255, 255, 80), 2)
    for i in range(n):
        y = y0 + i * step; c = RAIL / 2
        if i == k:
            st.ellipse((c - 16, y - 16, c + 16, y + 16), fill=ACC, outline=WHITE, width=3); st.text((c, y + 1), str(i + 1), 15, WHITE, bold=True, anchor="mm")
        elif i < k: st.ellipse((c - 7, y - 7, c + 7, y + 7), fill=WHITE)
        else: st.ellipse((c - 7, y - 7, c + 7, y + 7), outline=(255, 255, 255, 150), width=2)
    s = st.done(); img.paste(s, (0, 130), s)
    return img


def title(text, sub=None):
    ls = [text_layer(CX0, 74, text, 44, INK, bold=True)]
    if sub: ls.append(text_layer(CX0 + 2, 132, sub, 25, MUTE))
    return ls


@lru_cache(None)
def cap_layer(text):
    lines = wrap(text, 29, 1600); h = 24 + len(lines) * 39 + 8; w = CX1 - CX0
    s = SS(w, h); s.rr((0, 0, w, h), 14, fill=(*INDIGO, 244)); s.rr((0, 0, 12, h), 6, fill=ACC)
    for i, l in enumerate(lines): s.text((40, 16 + i * 39), l, 29, WHITE)
    return L(s.done(), CX0, 1058 - h)


def draw_caption(frame, t, st, sentences):
    k = -1
    for j, s in enumerate(st):
        if t >= s - 0.05: k = j
    if k < 0: return
    a = prog(t, st[k] - 0.05, 0.25); blit(frame, cap_layer(sentences[k]), a=a, dx=-int((1 - a) * 18))


def pop(frame, lay, t, t0, dur=0.5):
    p = prog(t, t0, dur)
    if p <= 0: return
    e = ease_out(p); sc = 0.9 + 0.1 * e
    im = lay.im.resize((max(1, int(lay.w * sc)), max(1, int(lay.h * sc))), Image.LANCZOS); m = im.getchannel("A").point(lambda v: int(v * e))
    frame.paste(im, (lay.x + (lay.w - im.width) // 2, lay.y + (lay.h - im.height) // 2), m)


def shot_card(name, x, y, w, h=None, crop=None):
    """Real screenshot in a card. Returns (layer, scale, (img_x, img_y)) where img_x/y is the screenshot's top-left on the frame."""
    img, sc, (ox, oy) = shot(name, w, h, crop=crop)
    c = card(x, y, img.width, img.height, r=14, pad=24); c.im.alpha_composite(img, (24, 24))
    return c, sc, (x + ox, y + oy)


def callout(f, t, t0, box, sc, origin, crop0=(0, 0), col=ACC, num=None, width=4):
    """Draw an animated highlight rectangle over source-pixel box (x0,y0,x1,y1) of a screenshot."""
    p = ease_out(prog(t, t0, 0.5))
    if p <= 0: return
    x0 = origin[0] + (box[0] - crop0[0]) * sc; y0 = origin[1] + (box[1] - crop0[1]) * sc
    x1 = origin[0] + (box[2] - crop0[0]) * sc; y1 = origin[1] + (box[3] - crop0[1]) * sc
    d = ImageDraw.Draw(f); d.rounded_rectangle((x0 - 6, y0 - 5, x0 - 6 + (x1 - x0 + 12) * p, y1 + 5), 8, outline=col, width=width)
    if num and p > 0.9:
        cx, cy = x1 + 26, (y0 + y1) / 2
        d.ellipse((cx - 17, cy - 17, cx + 17, cy + 17), fill=col, outline=WHITE, width=3); d.text((cx, cy), str(num), font=F(21, True), fill=WHITE, anchor="mm")


def icon(kind, size=64, bg=AZURE):
    s = SS(size, size); s.ellipse((0, 0, size, size), fill=bg); c = size / 2; w = (255, 255, 255, 255)
    if kind == "db":
        s.rect((size * .28, size * .32, size * .72, size * .66), fill=w)
        for k in range(3): s.ellipse((size * .28, size * (.27 + k * .17), size * .72, size * (.39 + k * .17)), fill=w, outline=bg, width=2)
    elif kind == "cloud":
        s.ellipse((size * .22, size * .42, size * .50, size * .68), fill=w); s.ellipse((size * .34, size * .26, size * .66, size * .62), fill=w)
        s.ellipse((size * .50, size * .38, size * .78, size * .67), fill=w); s.rect((size * .36, size * .50, size * .66, size * .67), fill=w)
    elif kind == "shield":
        s.poly([(c, size * .2), (size * .75, size * .32), (size * .71, size * .6), (c, size * .8), (size * .29, size * .6), (size * .25, size * .32)], w)
        s.line([(size * .38, size * .5), (size * .47, size * .6), (size * .63, size * .41)], bg, 4)
    elif kind == "chat":
        s.rr((size * .22, size * .27, size * .78, size * .62), 8, fill=w); s.poly([(size * .34, size * .62), (size * .34, size * .77), (size * .5, size * .62)], w)
    elif kind == "gear":
        for a in range(0, 360, 45):
            x = c + math.cos(math.radians(a)) * size * .26; y = c + math.sin(math.radians(a)) * size * .26; s.ellipse((x - size * .08, y - size * .08, x + size * .08, y + size * .08), fill=w)
        s.ellipse((size * .3, size * .3, size * .7, size * .7), fill=w); s.ellipse((size * .42, size * .42, size * .58, size * .58), fill=bg)
    elif kind == "book":
        s.rr((size * .25, size * .24, size * .75, size * .76), 5, fill=w)
        for k in range(3): s.line([(size * .34, size * (.38 + k * .12)), (size * .66, size * (.38 + k * .12))], bg, 3)
    elif kind == "key":
        s.ellipse((size * .22, size * .36, size * .5, size * .64), outline=w, width=5); s.line([(size * .5, size * .5), (size * .78, size * .5)], w, 5)
        s.line([(size * .7, size * .5), (size * .7, size * .62)], w, 5)
    return s.done()


def node(x0, y0, x1, y1, ttl, sub, accent=AZURE, fill=WHITE, dashed=False, ic=None, badge=None):
    """Architecture box: title + up to two sub lines, optional icon and corner badge."""
    w, h = x1 - x0, y1 - y0; c = card(x0, y0, w, h, r=14, fill=fill, shadow=not dashed, outline=MUTE if dashed else LINE, accent=None if dashed else accent); s = SS(w, h)
    if dashed: s.rr((3, 3, w - 3, h - 3), 12, outline=MUTE, width=3)
    tx = 22 + (60 if ic else 0)
    s.text((tx, 20), ttl, 23, INK, bold=True)
    for j, l in enumerate(wrap(sub, 19, w - tx - 14)[:2]): s.text((tx, 54 + j * 24), l, 19, MUTE)
    if badge: bw = tw(badge, 15, True) + 18; s.rr((w - bw - 10, 10, w - 10, 34), 12, fill=ACC); s.text((w - 10 - bw / 2, 22), badge, 15, WHITE, bold=True, anchor="mm")
    c.im.alpha_composite(s.done(), (26, 26))
    if ic: c.im.alpha_composite(icon(ic, 46, accent), (26 + 14, 26 + 20))
    return c


def label(x, y, text, size=19, fg=INK, bg=WHITE, outline=None, bold=True):
    w = int(tw(text, size, bold)) + 24; h = int(size * 1.3) + 10
    s = SS(w + 4, h + 4); s.rr((2, 2, 2 + w, 2 + h), 9, fill=bg, outline=outline, width=2); s.text((2 + w / 2, 2 + h / 2 + 1), text, size, fg, bold=bold, anchor="mm")
    return L(s.done(), int(x - w / 2 - 2), int(y - h / 2 - 2))


def mono_card(x, y, w, lines, size=21, fill=(28, 34, 74), fg=(225, 235, 255), head=None):
    """Dark terminal-style card (indigo) for commands and outputs."""
    h = 28 + (34 if head else 0) + len(lines) * int(size * 1.45) + 12
    c = card(x, y, w, h, r=14, fill=fill, outline=fill); s = SS(w, h); yy = 18
    if head:
        for k, col in enumerate(((237, 85, 101), (245, 190, 70), (70, 200, 120))): s.ellipse((20 + k * 22, 18, 34 + k * 22, 32), fill=col)
        s.text((100, 14), head, 18, (170, 185, 225), mono=True); yy += 34
    for i, l in enumerate(lines):
        col = fg
        if isinstance(l, tuple): l, col = l
        s.text((22, yy + i * int(size * 1.45)), l, size, col, bold=True, mono=True)
    c.im.alpha_composite(s.done(), (26, 26)); return c
