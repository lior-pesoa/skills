# Composition and layout

Canvas 1080x1920. Numbers below are for Instagram Reels; TikTok and Shorts have similar bottom and right overlays, so the same layout works.

## Safe zones

| Zone | Covered by | Rule |
|---|---|---|
| Top 250px | Platform header, plus any native headline the user adds | No important text. Labels sit at y=270. |
| Bottom 420px | Caption, username, audio line | No text. The avatar's face stays above it; shoulders may sit under it. |
| Right ~120px from y=1000 to 1700 | Like, comment, share buttons | Captions end by x=960. |

## Layers (bottom to top)

1. **Screen recordings**, full-bleed (`#screen` > `#pan` > one `<video>` per beat). Real screens only, recorded on a real phone; blur every real third-party business, person and logo before editing.
2. **Source labels** (`.tag`), top-left at y=270: the app or site on screen ("ChatGPT app", "yourproduct.com"). They make the footage read as real, not a mockup.
3. **End card** (`#end`), behind the avatar. Its content stays between y=270 and about y=880.
4. **Avatar** (`#cam`), cut out, at left -50px, bottom 0, 560x996. The face lands around y=1100 to 1350.
5. **Captions** (`#caps`), left 540, width 420, bottom 440. Off by default; see below.

## Beats

- Get word timings from the joined avatar track (`npx hyperframes transcribe assets/avatar.mp4`), then cut the screen at the first word of each line or idea.
- Each beat is one `<video>` with `data-start`, `data-duration`, `data-media-start`, and `data-playback-rate` when a recording is longer than its beat.
- **Pan** (`#pan` y) so the key content (the typed query, the answer, the result) sits between y=300 and y=900. Look at each recording's frames first (`ffmpeg -ss <t> -i x.mp4 -frames:v 1`).
- A lifted screen leaves a strip at the bottom. Set `#screen` background to that recording's color at the same time as the pan.
- A 3% scale punch on each cut keeps it moving. No other effects.

## Avatar track

1. `scripts/clip-report.py` on the clips: transcript per speech segment, extra words, framing sheet, draft `cuts.json`.
2. Edit `cuts.json`: drop segments with wrong words, add `crop` to wider clips, keep `speed` at 1.10 to 1.15.
3. `scripts/build-avatar.py cuts.json`: writes the joined track and its voice-only `.m4a`, loudness at -16 LUFS so music can sit under it.
4. Cut out the background: `npx hyperframes remove-background assets/avatar.mp4 -o assets/avatar-cutout.webm --quality best`. It runs locally (about 9 frames a second on Apple silicon). The cutout has no sound, so the voice plays from the separate `<audio>`.
5. Edges wobble a little and hair edges soften at 480p. That is the normal green-screen creator look; leave it.

The boxed alternative (no cutout): a rounded box at left 40, top 940, 380x560, `object-fit: cover; object-position: 50% 30%`, with a border and hard shadow. Use it when the cutout looks wrong (busy background, hands in frame).

## Captions

- Default: **no burned-in captions.** Most users add text in the platform's own editor (Instagram Edits auto captions), which the platform can read; burned-in pixels it can't.
- If the user wants burned captions: `scripts/caption-groups.py assets/transcript.json` prints the arrays for the template; render with `--variables '{"captions":true}'`. Each word turns the accent color as it is spoken.
- Either way, put the timed lines in the posting notes.

## Verify before handing over

- `npx hyperframes lint` (the "nested structure" warning on the end card is fine).
- `npx hyperframes snapshot --at <one time per beat> --no-end` and look at every frame: nothing important under the avatar, labels, captions or safe zones.
- Render, then transcribe the render's audio and compare it to the script: the right words on the right screens.
- Check loudness (`ffmpeg -i out.mp4 -af volumedetect -f null -`): mean around -19 dB, max under -1 dB.
