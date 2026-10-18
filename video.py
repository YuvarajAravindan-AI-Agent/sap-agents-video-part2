"""Driver: timeline from narration durations, per-scene frames with a vertical wipe between scenes, previews."""
import json, os, sys
from PIL import Image, ImageDraw
from lib import *
import content, scenes

HERE = os.path.dirname(os.path.abspath(__file__))
DUR = json.load(open(os.path.join(HERE, "durations.json")))
LEAD, TAIL, TRANS = 0.35, 0.7, 0.55


def timeline(sc):
    sp = [s[1] for s in sc["sentences"]]; tot = sum(len(x) for x in sp); a = DUR[sc["id"]]; cum = 0; st = []
    for x in sp: st.append(LEAD + a * cum / tot); cum += len(x)
    return LEAD + a + TAIL, st, [s[0] for s in sc["sentences"]]

_cache = {}
def scene(i):
    if i not in _cache:
        sc = content.SCENES[i]; T, st, sents = timeline(sc); _cache[i] = (scenes.BUILD[sc["id"]](T, st, sents), T, st)
    return _cache[i]

def frame_at(i, t):
    draw, T, st = scene(i); f = Image.new("RGB", (W, H), WHITE); draw(f, min(t, T)); return f

_last = {}
def last_frame(i):
    if i not in _last: _last[i] = frame_at(i, scene(i)[1])
    return _last[i]

def full_frame(i, t):
    """Vertical wipe: the new scene rises from the bottom over the previous scene's last frame, with a teal edge."""
    cur = frame_at(i, t)
    if i == 0:
        return cur if t >= 0.5 else Image.blend(Image.new("RGB", (W, H), WHITE), cur, ease_out(t / 0.5))
    if t >= TRANS: return cur
    e = ease_io(t / TRANS); y = int(H * (1 - e)); out = last_frame(i - 1).copy()
    out.paste(cur.crop((0, y, W, H)), (0, y)); ImageDraw.Draw(out).rectangle((0, max(0, y - 3), W, y + 3), fill=ACC)
    return out

def preview(i, times, out):
    os.makedirs(out, exist_ok=True)
    for t in times: full_frame(i, t).save(f"{out}/s{i:02d}_{t:05.1f}.png")

if __name__ == "__main__":
    i = int(sys.argv[1]); T = scene(i)[1]; ts = [float(x) for x in sys.argv[2:]] or [T * 0.97]
    preview(i, ts, os.path.join(HERE, "preview")); print("scene", i, content.SCENES[i]["id"], "T=%.1f" % T, "st", [round(x, 1) for x in scene(i)[2]])
