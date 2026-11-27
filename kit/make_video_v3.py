"""Video vertical 1080x1920 v3 (27-nov: ~32 s para leer con calma).
Uso: python3 make_video_v3.py OUTDIR DAY OUTFILE.mp4 FONT "HOOK" [seed]
"""
import sys, os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT, DAY, OUTFILE, FONT, HOOK = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
SEED = int(sys.argv[6]) if len(sys.argv) > 6 else DAY
CRF = os.environ.get("CRF", "26")  # ~2,4 MB por video de 31,7 s
W, H, FPS = 1080, 1920, 30
DUR = [3.2, 4.0, 4.5, 4.5, 4.0, 4.5, 3.5, 3.5]  # 27-nov: ~32 s para leer con calma (antes 17 s, no se alcanzaba a leer)
TOTAL = sum(DUR)
tmp = os.path.join(OUT, f"vtmp{DAY}")
os.makedirs(tmp, exist_ok=True)

def font(size, weight=900):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight, 100])
    return f

def hook_band(canvas, bg):
    d = ImageDraw.Draw(canvas)
    dark = bg == (18, 18, 18)
    fg = (255, 91, 31) if dark else (18, 18, 18)
    s = 84
    while s > 40 and d.textlength(HOOK, font=font(s)) > W - 120:
        s -= 4
    f = font(s)
    tw = d.textlength(HOOK, font=f)
    d.text(((W - tw) / 2, 285 - 60 - s), HOOK, font=f, fill=fg)

frames = []
n = 0
prev = None
for i in range(8):
    im = Image.open(os.path.join(OUT, f"dia{DAY:02d}-{i+1:02d}.png")).convert("RGB")
    bg = im.getpixel((20, 20))
    nf = int(DUR[i] * FPS)
    for k in range(nf):
        t = k / max(nf - 1, 1)
        if i == 0 and k < 12:
            z = 1.10 - 0.10 * (k / 11)
        else:
            z = 1.0 + 0.03 * t
        sw, sh = int(1080 * z), int(1350 * z)
        s = im.resize((sw, sh), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), bg)
        canvas.paste(s, ((W - sw) // 2, (H - sh) // 2 + 60))
        hook_band(canvas, bg)
        d = ImageDraw.Draw(canvas)
        done = (sum(DUR[:i]) + DUR[i] * t) / TOTAL
        col = (18, 18, 18) if bg != (18, 18, 18) else (242, 238, 230)
        d.rectangle((0, 0, int(W * done), 10), fill=col)
        if i > 0 and k < 5 and prev is not None:
            canvas = Image.blend(prev, canvas, k / 5)
        canvas.save(os.path.join(tmp, f"f{n:05d}.jpg"), quality=90)
        prev = canvas
        n += 1

sr = 44100
rng = np.random.default_rng(SEED)
bpm = [92, 96, 100, 88][SEED % 4]
beat = 60 / bpm
t = np.arange(int(TOTAL * sr)) / sr
audio = np.zeros_like(t)
roots = [[220, 261.63, 196, 246.94], [196, 233.08, 174.61, 220], [246.94, 293.66, 220, 261.63], [174.61, 207.65, 155.56, 196]][SEED % 4]
bar = beat * 4
for b in range(int(TOTAL / bar) + 1):
    f0 = roots[b % 4]
    start, end = int(b * bar * sr), int(min((b + 1) * bar, TOTAL) * sr)
    if start >= len(t): break
    tt = t[start:end] - t[start]
    env = np.minimum(1, tt / 0.05) * np.exp(-tt / (bar * 0.9))
    for mult, amp in [(1, 0.08), (1.5, 0.05), (2, 0.04), (0.5, 0.06)]:
        audio[start:end] += amp * env * np.sin(2 * np.pi * f0 * mult * tt + 0.3 * np.sin(2 * np.pi * 0.5 * tt))
for k in range(int(TOTAL / beat) + 1):
    s = int(k * beat * sr)
    if s >= len(t): break
    seg = t[s:s + int(0.25 * sr)] - t[s]
    audio[s:s + len(seg)] += 0.5 * np.exp(-seg * 18) * np.sin(2 * np.pi * (55 + 60 * np.exp(-seg * 30)) * seg)
    for h in (0, 0.5):
        hs = int((k + h) * beat * sr)
        if hs >= len(t): break
        hseg = t[hs:hs + int(0.06 * sr)] - t[hs]
        audio[hs:hs + len(hseg)] += rng.standard_normal(len(hseg)) * np.exp(-hseg * 80) * (0.12 if h == 0 else 0.07)
    if k % 2 == 1:
        sseg = t[s:s + int(0.12 * sr)] - t[s]
        audio[s:s + len(sseg)] += 0.18 * rng.standard_normal(len(sseg)) * np.exp(-sseg * 35)
fade = np.ones_like(audio); nf = int(1.5 * sr); fade[-nf:] = np.linspace(1, 0, nf)
audio = audio * fade
audio = 0.85 * audio / np.max(np.abs(audio))
wav = os.path.join(tmp, "music.wav")
with wave.open(wav, "w") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes((audio * 32767).astype(np.int16).tobytes())

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.jpg"),
    "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-crf", CRF, "-r", str(FPS),
    "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", OUTFILE], check=True)
print(OUTFILE, round(TOTAL, 1), "s", bpm, "bpm")
