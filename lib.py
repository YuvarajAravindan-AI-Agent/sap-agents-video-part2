"""Drawing helpers for the SAP Agents v2 video (Horizon-style left-rail look): anti-aliased layers, easing, cards, screenshots."""
import os, math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = [os.path.join(HERE, "fonts"), "/usr/share/fonts/truetype/freefont"]
W, H, FPS = 1920, 1080, 20
ASSETS = os.path.join(HERE, "assets")

# Horizon-style palette: azure + indigo on white, teal highlight (distinct from the gold-highlight Fiori look of video 1)
AZURE = (0, 112, 242); INDIGO = (31, 38, 102); VIOLET = (72, 52, 190); SKY = (0, 168, 255); ACC = (0, 160, 170)
INK = (24, 32, 60); TEXT = (46, 54, 72); MUTE = (100, 112, 132)
GREEN = (18, 140, 90); RED = (205, 30, 60); AMBER = (225, 135, 0)
BG = (250, 251, 254); WHITE = (255, 255, 255); LINE = (214, 222, 234); PALE = (230, 241, 255)
PALEACC = (218, 246, 246); PALEAMB = (255, 240, 214); PALEGREEN = (224, 245, 236); PALERED = (252, 230, 234)
BLUE = AZURE; GOLD = ACC   # names kept so shared helpers read the same; GOLD is the teal highlight here

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, d): return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)
def ease_out(p): return 1 - (1 - p) ** 3
def ease_io(p): return 3 * p * p - 2 * p ** 3
def lerp(a, b, p): return a + (b - a) * p
def mix(c1, c2, p): return tuple(int(lerp(c1[i], c2[i], p)) for i in range(3))

@lru_cache(None)
def F(size, bold=False, mono=False):
    name = ("FreeMonoBold" if bold else "FreeMono") if mono else ("FreeSansBold" if bold else "FreeSans")
    for d in FONTS:
        p = os.path.join(d, name + ".ttf")
        if os.path.exists(p): return ImageFont.truetype(p, int(size))
    raise FileNotFoundError(name)

def tw(t, size, bold=False, mono=False): return F(size, bold, mono).getlength(t)

def wrap(t, size, width, bold=False, mono=False):
    lines, cur = [], ""
    for w in t.split():
        c = (cur + " " + w).strip()
        if tw(c, size, bold, mono) <= width: cur = c
        else:
            if cur: lines.append(cur)
            cur = w
    return lines + [cur] if cur else lines


class SS:
    """Supersampled RGBA canvas (draw at 2x, shrink with LANCZOS) -> smooth edges."""
    def __init__(s, w, h, k=2):
        s.w, s.h, s.k = int(w), int(h), k
        s.im = Image.new("RGBA", (s.w * k, s.h * k), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im)
    def _c(s, box): return [c * s.k for c in box]
    def rr(s, box, r=16, fill=None, outline=None, width=1):
        s.d.rounded_rectangle(s._c(box), r * s.k, fill=fill, outline=outline, width=int(width * s.k))
    def rect(s, box, fill=None, outline=None, width=1): s.d.rectangle(s._c(box), fill=fill, outline=outline, width=int(width * s.k))
    def ellipse(s, box, fill=None, outline=None, width=1): s.d.ellipse(s._c(box), fill=fill, outline=outline, width=int(width * s.k))
    def line(s, pts, fill, width=3, dash=None):
        pts = [(p[0] * s.k, p[1] * s.k) for p in pts]
        if not dash:
            s.d.line(pts, fill=fill, width=int(width * s.k), joint="curve"); return
        for a, b in zip(pts, pts[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1]); n = int(L // ((dash[0] + dash[1]) * s.k)) + 1
            ux, uy = (b[0] - a[0]) / (L or 1), (b[1] - a[1]) / (L or 1)
            for i in range(n):
                p0 = i * (dash[0] + dash[1]) * s.k; p1 = min(p0 + dash[0] * s.k, L)
                s.d.line([(a[0] + ux * p0, a[1] + uy * p0), (a[0] + ux * p1, a[1] + uy * p1)], fill=fill, width=int(width * s.k))
    def poly(s, pts, fill): s.d.polygon([(p[0] * s.k, p[1] * s.k) for p in pts], fill=fill)
    def text(s, xy, t, size, fill, bold=False, mono=False, anchor="la", spacing=0):
        if spacing:
            x = xy[0]
            for ch in t:
                s.d.text((x * s.k, xy[1] * s.k), ch, font=F(size * s.k, bold, mono), fill=fill, anchor=anchor); x += tw(ch, size, bold, mono) + spacing
            return
        s.d.text((xy[0] * s.k, xy[1] * s.k), t, font=F(size * s.k, bold, mono), fill=fill, anchor=anchor)
    def done(s): return s.im.resize((s.w, s.h), Image.LANCZOS)


class L:
    """A pre-rendered RGBA layer placed at (x, y)."""
    def __init__(s, im, x, y): s.im, s.x, s.y = im.convert("RGBA"), int(x), int(y); s._a = s.im.getchannel("A"); s._m = {}
    def mask(s, a):
        q = int(round(clamp(a) * 16))
        if q not in s._m: s._m[q] = s._a.point([int(v * q / 16) for v in range(256)])
        return s._m[q]
    @property
    def w(s): return s.im.width
    @property
    def h(s): return s.im.height

def blit(frame, lay, a=1.0, dx=0, dy=0, clip=None):
    if a <= 0.01: return
    im, m = lay.im, lay.mask(a)
    if clip:  # (x0, y0, x1, y1) in layer coordinates
        im, m = im.crop(clip), m.crop(clip); frame.paste(im, (lay.x + dx + clip[0], lay.y + dy + clip[1]), m)
    else: frame.paste(im, (lay.x + dx, lay.y + dy), m)

def appear(frame, lay, t, t0, dur=0.45, rise=0, slide=44):
    """Slide in from the left while fading (v2 motion); rise adds an optional vertical offset."""
    p = prog(t, t0, dur)
    if p <= 0: return
    e = ease_out(p); blit(frame, lay, a=e, dx=-int((1 - e) * slide), dy=int((1 - e) * rise))

def card(x, y, w, h, fill=WHITE, outline=LINE, r=18, shadow=True, accent=None, pad=26):
    """White Fiori-style card with soft shadow; optional left accent bar. Returns L (position includes padding)."""
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 5, pad + w, pad + h + 5), r, fill=(20, 50, 90, 46))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
    s = SS(w + 2 * pad, h + 2 * pad); s.rr((pad, pad, pad + w, pad + h), r, fill=fill, outline=outline, width=2)
    if accent: s.rr((pad + 14, pad, pad + w - 14, pad + 8), 4, fill=accent)
    im.alpha_composite(s.done()); return L(im, x - pad, y - pad)

def chip(x, y, text, size=26, fg=WHITE, bg=BLUE, bold=True, padx=18, pady=8, outline=None, r=None, mono=False):
    w = int(tw(text, size, bold, mono)) + 2 * padx; h = int(size * 1.35) + 2 * pady
    s = SS(w + 4, h + 4); s.rr((2, 2, 2 + w, 2 + h), r if r is not None else h // 2, fill=bg, outline=outline, width=2)
    s.text((2 + w / 2, 2 + h / 2 + 1), text, size, fg, bold=bold, mono=mono, anchor="mm"); return L(s.done(), x - 2, y - 2)

def text_layer(x, y, lines, size, fill=TEXT, bold=False, mono=False, gap=1.32, anchor_center=False, width=None):
    if isinstance(lines, str): lines = [lines]
    w = width or int(max(tw(l, size, bold, mono) for l in lines)) + 8; h = int(len(lines) * size * gap) + 8
    s = SS(w, h)
    for i, l in enumerate(lines):
        if anchor_center: s.text((w / 2, 2 + i * size * gap), l, size, fill, bold, mono, anchor="ma")
        else: s.text((2, 2 + i * size * gap), l, size, fill, bold, mono)
    return L(s.done(), x - (w // 2 if anchor_center else 0), y)

@lru_cache(32)
def _img(name):
    for ext in (".png", ".jpg"):
        p = os.path.join(ASSETS, name + ext)
        if os.path.exists(p): return Image.open(p).convert("RGB")
    raise FileNotFoundError(name)

def shot(name, w, h=None, crop=None, r=12, border=True, bg=WHITE):
    """A real screenshot, fitted (contain) into w x h (or width-only), rounded, thin border. Returns (L, scale, (ox, oy))."""
    im = _img(name)
    if crop: im = im.crop(crop)
    sc = w / im.width if h is None else min(w / im.width, h / im.height)
    nw, nh = int(im.width * sc), int(im.height * sc)
    im = im.resize((nw, nh), Image.LANCZOS); bw, bh = (w, h) if h else (nw, nh)
    base = Image.new("RGB", (bw, bh), bg); ox, oy = (bw - nw) // 2, (bh - nh) // 2; base.paste(im, (ox, oy))
    m = Image.new("L", (bw * 2, bh * 2), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw * 2 - 1, bh * 2 - 1), r * 2, fill=255); m = m.resize((bw, bh), Image.LANCZOS)
    out = Image.new("RGBA", (bw, bh)); out.paste(base, (0, 0)); out.putalpha(m)
    if border:
        s = SS(bw, bh); s.rr((1, 1, bw - 1, bh - 1), r, outline=LINE, width=2); out.alpha_composite(s.done())
    return out, sc, (ox, oy)

def arrow_layer(pts, color, width=4, dash=None, head=14):
    """Polyline with arrow head at the end. Returns (L, total_length)."""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; pad = head + width + 4
    x0, y0 = min(xs) - pad, min(ys) - pad; w, h = max(xs) - x0 + pad, max(ys) - y0 + pad
    loc = [(p[0] - x0, p[1] - y0) for p in pts]; s = SS(w, h)
    a, b = loc[-2], loc[-1]; ang = math.atan2(b[1] - a[1], b[0] - a[0]); ux, uy = math.cos(ang), math.sin(ang)
    base = (b[0] - ux * head * 0.9, b[1] - uy * head * 0.9); line_pts = loc[:-1] + [base]
    s.line(line_pts, color, width, dash=dash)
    s.poly([b, (b[0] - ux * head - uy * head * 0.5, b[1] - uy * head + ux * head * 0.5), (b[0] - ux * head + uy * head * 0.5, b[1] - uy * head - ux * head * 0.5)], color)
    return L(s.done(), x0, y0), sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts, pts[1:]))

def path_point(pts, dist):
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if dist <= seg: f = dist / (seg or 1); return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        dist -= seg
    return pts[-1]

def reveal_clip(lay, pts, frac):
    """Clip rect (in layer coords) that reveals an orthogonal polyline's layer progressively along its path (approx. by bbox growth)."""
    total = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts, pts[1:])); d = total * frac
    pt = path_point(pts, d); x0, y0 = lay.x, lay.y
    xs = [p[0] for p in pts[:1]] + [pt[0]]; ys = [p[1] for p in pts[:1]] + [pt[1]]
    # include all fully-passed vertices
    acc = 0.0; cover = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if acc + seg <= d: cover.append(b)
        acc += seg
    cover.append(pt); xs = [p[0] for p in cover]; ys = [p[1] for p in cover]; m = 24
    return (max(0, int(min(xs) - m - x0)), max(0, int(min(ys) - m - y0)), min(lay.w, int(max(xs) + m - x0)), min(lay.h, int(max(ys) + m - y0)))

_dot = {}
def dot_layer(color, r=7):
    k = (color, r)
    if k not in _dot:
        s = SS(r * 4, r * 4); s.ellipse((r * 0.4, r * 0.4, r * 3.6, r * 3.6), fill=(*color, 60)); s.ellipse((r, r, r * 3, r * 3), fill=color, outline=WHITE, width=2); _dot[k] = s.done()
    return _dot[k]

def paste_dot(frame, pos, color, r=7):
    d = dot_layer(color, r); frame.paste(d, (int(pos[0] - d.width / 2), int(pos[1] - d.height / 2)), d)
