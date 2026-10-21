#!/usr/bin/env python3
"""Report on generated avatar clips before editing.

For each clip: duration, size, the speech segments (from silence detection), what was
actually said in each segment (whisper.cpp), and words that differ from the line it
was supposed to say. Writes a draft cuts.json for build-avatar.py and a framing sheet
(one frame per clip, side by side) so zoom differences are easy to spot.

Usage:
  clip-report.py clip1.mp4 clip2.mp4 ... [--lines lines.txt] [--out work/]
  lines.txt: one expected line per clip, in the same order (optional).
Env: WHISPER_MODEL=/path/to/ggml-*.bin (otherwise the newest of medium.en/small.en/base.en
     found under ~/.cache is used). Needs ffmpeg, ffprobe and whisper-cli on PATH.
"""
import argparse, difflib, glob, json, os, re, subprocess, sys, tempfile

PAD = 0.06        # seconds kept before and after each speech segment
MERGE_GAP = 0.15  # pauses shorter than this stay in
NOISE = "-40dB"
MIN_SILENCE = 0.25


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def find_model():
    if os.environ.get("WHISPER_MODEL"):
        return os.environ["WHISPER_MODEL"]
    for name in ("medium.en", "small.en", "base.en"):
        hits = glob.glob(os.path.expanduser(f"~/.cache/**/ggml-{name}.bin"), recursive=True)
        if hits:
            return hits[0]
    sys.exit("No whisper model found. Set WHISPER_MODEL or run `npx hyperframes transcribe` once to download one.")


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height:format=duration", "-of", "json", path]).stdout
    d = json.loads(out)
    s = d["streams"][0]
    return float(d["format"]["duration"]), s["width"], s["height"]


def speech_segments(path, duration):
    err = run(["ffmpeg", "-i", path, "-vn", "-af", f"silencedetect=n={NOISE}:d={MIN_SILENCE}", "-f", "null", "-"]).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    silences = list(zip(starts, ends + [duration] * (len(starts) - len(ends))))
    segs, t = [], 0.0
    for s, e in silences:
        if s - t > 0.05:
            segs.append([max(0, t - PAD), min(duration, s + PAD)])
        t = e
    if duration - t > 0.05:
        segs.append([max(0, t - PAD), duration])
    merged = []
    for s in segs:
        if merged and s[0] - merged[-1][1] < MERGE_GAP:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    # Drop slivers (a breath or a click at the very end).
    return [[round(a, 2), round(b, 2)] for a, b in merged if b - a >= 0.25]


def transcribe(model, path, start=None, end=None):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav = f.name
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if start is not None:
        cmd += ["-ss", str(start), "-to", str(end)]
    run(cmd + ["-i", path, "-ar", "16000", "-ac", "1", wav])
    text = run(["whisper-cli", "-m", model, "-f", wav, "-nt", "-np"]).stdout
    os.unlink(wav)
    return " ".join(text.split())


def words(s):
    return re.findall(r"[a-z0-9']+", s.lower().replace("chat gpt", "chatgpt"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--lines")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    lines = open(a.lines).read().strip().splitlines() if a.lines else []
    model = find_model()
    report, cuts, frames = [], [], []

    for i, clip in enumerate(a.clips):
        dur, w, h = probe(clip)
        segs = speech_segments(clip, dur)
        full = transcribe(model, clip)
        seg_text = [transcribe(model, clip, s, e) for s, e in segs]
        speech = sum(e - s for s, e in segs)
        item = {"clip": clip, "duration": round(dur, 2), "size": f"{w}x{h}", "speech_seconds": round(speech, 2),
                "transcript": full, "segments": [{"range": s, "said": t} for s, t in zip(segs, seg_text)]}
        if i < len(lines):
            exp, got = words(lines[i]), words(full)
            sm = difflib.SequenceMatcher(a=exp, b=got)
            item["expected"] = lines[i]
            item["extra_words"] = [" ".join(got[j1:j2]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op in ("insert", "replace")]
            item["missing_words"] = [" ".join(exp[i1:i2]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op in ("delete", "replace")]
        report.append(item)
        cuts.append({"src": clip, "segments": segs, "crop": None})
        fr = os.path.join(a.out, f"frame-{i + 1}.png")
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(min(1.0, dur / 2)), "-i", clip, "-frames:v", "1", "-vf", "scale=300:-2", fr])
        frames.append(fr)

        print(f"\n== clip {i + 1}: {clip}  {dur:.2f}s  {w}x{h}  speech {speech:.2f}s")
        print(f"   heard: {full}")
        for s, t in zip(segs, seg_text):
            print(f"   {s[0]:6.2f}-{s[1]:6.2f}  {t}")
        if item.get("extra_words"):
            print(f"   EXTRA WORDS (cut or regenerate): {item['extra_words']}")
        if item.get("missing_words"):
            print(f"   MISSING WORDS: {item['missing_words']}")

    sheet = os.path.join(a.out, "framing.png")
    inputs = sum((["-i", f] for f in frames), [])
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", f"hstack={len(frames)}" if len(frames) > 1 else "null", sheet])
    json.dump(report, open(os.path.join(a.out, "clip-report.json"), "w"), indent=2)
    first = report[0]["size"].split("x")
    json.dump({"speed": 1.12, "width": int(first[0]), "height": int(first[1]), "out": "assets/avatar.mp4", "clips": cuts},
              open(os.path.join(a.out, "cuts.json"), "w"), indent=2)
    print(f"\nWrote {a.out}/clip-report.json, {a.out}/cuts.json (draft) and {sheet} (framing, clip 1 first).")


if __name__ == "__main__":
    main()
