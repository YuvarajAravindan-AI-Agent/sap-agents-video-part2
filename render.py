"""Render all scenes of part 2 in parallel, build the audio track, mux. Run on contabo-tally (has ffmpeg):  python render.py [crf]"""
import os, sys, subprocess, shutil, wave, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, HERE)
import video, content
from lib import W, H, FPS
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
CRF = sys.argv[1] if len(sys.argv) > 1 else "17"
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)

def render_scene(i):
    T = video.scene(i)[1]; n = int(round(T * FPS)); out = os.path.join(PARTS, f"s{i:02d}.mp4"); t0 = time.time()
    p = subprocess.Popen([FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", CRF, "-pix_fmt", "yuv420p", "-g", str(FPS * 2), "-an", out], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(video.full_frame(i, k / FPS).tobytes())
    p.stdin.close(); p.wait(); return i, n, round(time.time() - t0, 1)

def build_audio(path):
    rate = None; chunks = []
    for i, sc in enumerate(content.SCENES):
        with wave.open(os.path.join(HERE, "audio", sc["id"] + ".wav")) as w:
            rate = rate or w.getframerate(); assert w.getnchannels() == 1 and w.getsampwidth() == 2; pcm = w.readframes(w.getnframes())
        T = video.scene(i)[1]; total = int(round(T * FPS)) / FPS; lead = int(video.LEAD * rate) * 2
        pad = max(0, int(total * rate) * 2 - lead - len(pcm)); chunks.append(b"\0" * lead + pcm + b"\0" * pad)
    with wave.open(path, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(b"".join(chunks))

if __name__ == "__main__":
    n = len(content.SCENES); t0 = time.time()
    only = [int(x) for x in sys.argv[2:]] or list(range(n))
    with Pool(4) as pool:
        for i, frames, sec in pool.imap_unordered(render_scene, only): print(f"scene {i:02d} {content.SCENES[i]['id']:<12} {frames} frames in {sec}s", flush=True)
    lst = os.path.join(PARTS, "list.txt"); open(lst, "w").write("".join(f"file 's{i:02d}.mp4'\n" for i in range(n)))
    silent = os.path.join(HERE, "silent.mp4"); subprocess.check_call([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
    wav = os.path.join(HERE, "narration.wav"); build_audio(wav)
    final = os.path.join(HERE, "sap-agents-part2.mp4")
    subprocess.check_call([FFMPEG, "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", final])
    sz = os.path.getsize(final); dur = float(subprocess.check_output([FFMPEG, "-i", final], stderr=subprocess.STDOUT, text=False).decode().split("Duration: ")[1].split(",")[0].split(":")[2]) if False else 0
    print("DONE", final, round(sz / 1e6, 2), "MB", round(time.time() - t0), "s")
