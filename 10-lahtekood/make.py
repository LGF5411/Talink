"""Render scene.html frame by frame -> mp4. Usage: python3 make.py <name> <w> <h> <cut> [preview t1,t2,...]"""
import sys, pathlib, subprocess, shutil
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).resolve().parent
name, W, H, cut = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
preview = [float(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else None
FPS = 30
total = 6 if cut == "short" else 15
pause_at = 1.5 if cut == "short" else 3.6
OUT = D.parent / "out" / "video"; OUT.mkdir(parents=True, exist_ok=True)
frames = D / f"_frames_{name}"
shutil.rmtree(frames, ignore_errors=True); frames.mkdir()

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": H})
    pg.goto((D / "scene.html").as_uri() + f"?w={W}&h={H}&cut={cut}", wait_until="networkidle")
    pg.evaluate("document.fonts.ready")
    times = preview or [i / FPS for i in range(int(total * FPS))]
    for i, t in enumerate(times):
        pg.evaluate(f"render({t})")
        path = OUT / f"{name}-t{t:.1f}.jpg" if preview else frames / f"f{i:05d}.jpg"
        pg.screenshot(path=str(path), type="jpeg", quality=92)
    b.close()

if preview:
    print("preview frames saved"); sys.exit()
wav = OUT / f"_{name}.wav"
subprocess.run(["python3", str(D / "audio.py"), str(total), str(pause_at), str(wav)], check=True)
mp4 = OUT / f"{name}.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(frames / "f%05d.jpg"), "-i", str(wav),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "-c:a", "aac", "-b:a", "160k", "-shortest", str(mp4)], check=True)
shutil.rmtree(frames); wav.unlink()
print("ok", mp4)
