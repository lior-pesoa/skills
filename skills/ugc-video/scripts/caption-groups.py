#!/usr/bin/env python3
"""Turn a word-level transcript into caption phrases.

Input: a HyperFrames transcript.json (a list of {"text", "start", "end"}) from
`npx hyperframes transcribe`. Phrases break after punctuation, at 4 words, or before a
pause of 0.35s or more.
Prints (1) the W and GROUPS arrays for the composition template, and (2) a timed
list to paste into the posting notes for typing captions by hand.

Usage: caption-groups.py assets/transcript.json [--fix "type=type:" ...]
--fix replaces text inside a single word; join or split words by editing transcript.json.
"""
import argparse, json, re

ap = argparse.ArgumentParser()
ap.add_argument("transcript")
ap.add_argument("--fix", action="append", default=[], help="word replacement, old=new")
a = ap.parse_args()
words = json.load(open(a.transcript))
words = words if isinstance(words, list) else words["words"]
fixes = dict(x.split("=", 1) for x in a.fix)
W = []
for w in words:
    t = w["text"].strip()
    for old, new in fixes.items():
        t = t.replace(old, new)
    W.append([round(w["start"], 2), round(w["end"], 2), t])

groups, cur = [], []
for i, (s, e, t) in enumerate(W):
    cur.append(i)
    nxt = W[i + 1][0] if i + 1 < len(W) else None
    if re.search(r"[.,!?:;]$", t) or len(cur) == 4 or (nxt is not None and nxt - e >= 0.35):
        groups.append(cur[0]); cur = []
if cur:
    groups.append(cur[0])

print("// Paste into the composition script.")
print("const W = [" + ",".join(f'[{s},{json.dumps(t)}]' for s, e, t in W) + "];")
print("const GROUPS = " + json.dumps(groups) + ";")
print(f"const CAP_END = {round(W[-1][1] + 0.1, 2)};\n")

print("Timed lines for posting notes:")
sentence, start = [], None
for i, (s, e, t) in enumerate(W):
    if start is None:
        start = s
    sentence.append(t)
    if re.search(r"[.!?]$", t) or len(sentence) >= 7 or i == len(W) - 1:
        m, sec = divmod(start, 60)
        print(f"{int(m)}:{sec:04.1f}  {' '.join(sentence)}")
        sentence, start = [], None
