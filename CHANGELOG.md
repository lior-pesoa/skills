# Changelog

## design-crit 0.2.0 · 2026-10-21

From a cold test run (a fresh agent using only the skill's files) and the first iOS run.

- Capture: `--stitch` for pages that reveal content on scroll, `--at=<y>` for sticky bars, `--settle` and `--step`; burst capture for moving content; iOS steps for a dedicated simulator, Release builds, deep-link prompts and Dynamic Type.
- Measurement: near-identical text and background colors are reported as unknown, not as failures.
- Rules: 58 sourced rules (WCAG 2.5.5, 4.1.3, 2.4.12, 2.4.13 and copy rules added; Apple rules scoped to iOS). Every bias links to its paper, and the search covers biases.
- Process: one output format for every reviewer, the keyboard pass owned by the accessibility reviewer, measured WCAG AA failures beat the brief, clear limits including Polish, and rules for merging notes and replacing citations.
- Crit page: the title is the page heading, code shows as code, wide crops stay readable.

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
