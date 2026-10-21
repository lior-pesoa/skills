#!/usr/bin/env python3
"""Join avatar clips into one track: keep the listed speech segments, crop clips to
match the first clip's framing, speed up, and normalize loudness.

Usage: build-avatar.py cuts.json
cuts.json:
  {"speed": 1.12, "width": 480, "height": 854, "out": "assets/avatar.mp4",
   "clips": [{"src": "src/clip1.mp4", "segments": [[0.33, 2.6], ...], "crop": null},
             {"src": "src/clip2.mp4", "segments": [...], "crop": "369:656:55:0"}]}
crop is an ffmpeg crop (w:h:x:y in source pixels) applied before scaling back to
width x height; use it to zoom a wider clip in to match clip 1.
Also writes <out>.m4a (the voice alone) next to the video.
"""
import json, os, subprocess, sys

cfg = json.load(open(sys.argv[1]))
W, H, speed, out = cfg["width"], cfg["height"], cfg.get("speed", 1.0), cfg["out"]
f, labels, n = [], "", 0
for c, clip in enumerate(cfg["clips"]):
    segs = clip["segments"]
    crop = f"crop={clip['crop']}," if clip.get("crop") else ""
    f.append(f"[{c}:v]{crop}scale={W}:{H},setsar=1,fps=24,split={len(segs)}" + "".join(f"[c{c}v{i}]" for i in range(len(segs))))
    f.append(f"[{c}:a]aresample=48000,asplit={len(segs)}" + "".join(f"[c{c}a{i}]" for i in range(len(segs))))
    for i, (s, e) in enumerate(segs):
        f.append(f"[c{c}v{i}]trim={s}:{e},setpts=PTS-STARTPTS[s{c}v{i}]")
        # Tiny fades stop clicks at each cut.
        f.append(f"[c{c}a{i}]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={max(0, e - s - 0.02):.3f}:d=0.02[s{c}a{i}]")
        labels += f"[s{c}v{i}][s{c}a{i}]"
        n += 1
f.append(f"{labels}concat=n={n}:v=1:a=1[cv][ca]")
f.append(f"[cv]setpts=PTS/{speed},fps=24[v]")
f.append(f"[ca]atempo={speed},loudnorm=I=-16:TP=-1.5:LRA=7[a]")

os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
cmd = ["ffmpeg", "-v", "error", "-y"]
for clip in cfg["clips"]:
    cmd += ["-i", clip["src"]]
cmd += ["-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "16",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out]
subprocess.run(cmd, check=True)
voice = os.path.splitext(out)[0] + "-voice.m4a"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vn", "-c:a", "copy", voice], check=True)
dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                     capture_output=True, text=True).stdout.strip()
print(f"Wrote {out} ({float(dur):.2f}s) and {voice}")
