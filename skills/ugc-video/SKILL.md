---
name: ugc-video
description: Make a UGC-style short video ad (Instagram Reels, TikTok, Shorts) with an AI avatar talking over real screen recordings of a product. Writes the script and hook variants, the avatar character and prompts for the video tool (OpenArt and similar), checks the generated clips, joins them into one fast cut, removes the background so the avatar stands at the bottom-left over the screens, renders 1080x1920 with HyperFrames, and writes the posting notes. Use when the user wants a UGC video, an AI avatar or AI presenter ad, a talking-head over screen recording, or a script for one, or brings avatar clips to edit.
license: MIT
metadata:
  version: "0.1.0"
  author: Lior Pesoa
argument-hint: "[script|avatar|edit|post] [clip paths...]"
---

# UGC video

A person talks to camera in the corner while the real product plays behind them: the format that reads as a creator's tip, not an ad. The person is an AI avatar; everything on screen is real.

Read this file fully, then load each reference when its step starts.

## Arguments

- A stage to start at: `script`, `avatar`, `edit` or `post`. Without one, pick up where the project is (see §Resume).
- Clip paths: the user's generated avatar clips. Passing them means "start at `edit`".

## Hard rules

1. **Honest by construction.** The avatar never claims to use the product or to have results, never tells invented anecdotes, and says no numbers that aren't real and on screen. Disclose the AI presenter when posting. Details: `references/script.md` §Honesty rules.
2. **Real screens only.** Recordings from a real phone. Blur every real third-party business, person and logo before editing. No stock footage.
3. **The project's rules win.** Before writing anything, look for the project's brand, social or Instagram rules (e.g. `docs/brand/*.md`, `PRODUCT.md`, `DESIGN.md`, `CLAUDE.md` copy rules) and follow them over the defaults here.
4. **Check every clip by transcript,** not by ear. Avatar models insert, drop and blur words.
5. **Ask before spending money** (paid voice tools, voice actors, plan upgrades) and before posting or boosting anything.
6. **No em dashes** in anything a person reads: script, captions, posting notes.

## Requirements

ffmpeg and ffprobe, `whisper-cli` (whisper.cpp) with an English model (`npx hyperframes transcribe` downloads one to `~/.cache`), Node 18+ for `npx hyperframes`, Python 3 (standard library only). The avatar clips come from the user's own video tool account.

## Steps

### 1. Brief (no files yet)
Find out, from the project files first and the user second: the product and its one outcome, the audience (one trade or buyer per video), the platform, the screen recordings that exist (paths, what each shows), and the brand tokens and fonts. If there are no recordings, stop and ask for them: the script is built around what the screens can show.

### 2. Script → `references/script.md`
Write 4 lines (one per avatar clip) and 3 hooks of different types. Map every line to the recording that plays behind it. Give the user plain, copy-pasteable lines. If they reuse a story from an earlier video, change the angle (e.g. a screen-story reel → a "do this right now" dare).

### 3. Avatar → `references/avatar.md`
Give the user, ready to paste: the character's background story, one prompt per clip, the settings, and a voice plan. Tell them to test clips 1 and 2 at low resolution and compare the voices before making the rest.

### 4. Check the clips
```
python3 scripts/clip-report.py clip1.mp4 clip2.mp4 clip3.mp4 clip4.mp4 --lines lines.txt --out <work dir>
```
`lines.txt` holds the expected line per clip. Read the report: extra or missing words, unclear words, speech time vs clip time, and the framing sheet (`framing.png`, clip 1 first). Tell the user what's wrong in plain words and whether to regenerate or cut it. Most problems are fixed in the edit: extra words cut, pauses removed, framing cropped.

### 5. Edit → `references/composition.md`
1. New project folder (e.g. `videos/<name>/` with `assets/`, `fonts/`, `src/` for the raw clips), a `.gitignore` for `*.mp4`, `*.webm`, `renders/`, `.hyperframes/`, and the fonts copied in.
2. Edit the draft `cuts.json` (drop bad segments, crop wider clips), then `python3 scripts/build-avatar.py cuts.json`.
3. `npx hyperframes transcribe assets/avatar.mp4` for word timings.
4. `npx hyperframes remove-background assets/avatar.mp4 -o assets/avatar-cutout.webm --quality best`.
5. Copy `templates/index.html`, set the brand tokens, beats, pans, labels and end card from the timings.
6. Lint, snapshot every beat, look at each frame, fix, then render: `npx hyperframes render -o renders/<name>.mp4` (no captions by default).
7. Verify: transcribe the render and match it to the script and beats; check loudness.

Show the user progress in short lines between steps; a render they can watch beats a description.

### 6. Post → `references/posting.md`
Write the posting notes file next to the render: captions plan and timed lines, hook headline, post caption, AI disclosure, alt text note, music, cover, ad link. Render a captioned version only if the user asks.

## Resume

| Found | Start at |
|---|---|
| Nothing for this video | 1. Brief |
| Script agreed, no clips | 3. Avatar (re-send the prompts) |
| Clips in hand, no project | 4. Check the clips |
| `cuts.json` or `assets/avatar.mp4` | 5. Edit, at the first missing output |
| A render | 6. Post, or the user's change |

## Done means

- The render plays the script word for word, each line over its screen, nothing important under the avatar or in a safe zone.
- The posting notes file exists and every line in it follows the project's copy rules.
- Raw clips, renders and the cutout stay out of git.
