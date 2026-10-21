# Changelog

## ugc-video 0.1.0 · 2026-10-21

First release, built from making a real Instagram ad end to end.

- Script rules: hook types to test, honesty rules for AI presenters, slop check.
- Avatar character, prompt template, settings and voice-consistency plan for OpenArt-style tools.
- `clip-report.py`: per-segment transcripts, added or dropped words, pauses, framing sheet, draft cut list.
- `build-avatar.py`: joins clips, cuts pauses, crops to match framing, speeds up, normalizes loudness.
- `caption-groups.py`: caption phrases from word timings.
- HyperFrames template: cut-out avatar at the bottom-left over full-bleed screen recordings, safe zones, labels, end card, optional word captions.

## design-crit 0.1.0 — 2026-10-21

First release.

- Web capture with lazy content loaded, at phone and desktop widths, light and dark; in-page measurement of contrast, targets, names, alt text, text size and overflow.
- iOS capture steps for the Simulator: appearance, Dynamic Type, status bar, accessibility audit.
- Visual, accessibility and copy reviewers, and a director pass that cuts unsourced and generic notes.
- 48 sourced rules with a search script; anti-slop lists for design and copy; 25 cognitive biases graded by evidence.
- Crit page renderer with annotated screenshot crops, light and dark themes.
