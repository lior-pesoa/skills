# Changelog

## cv-interview 0.1.0 · 2026-11-17

First release. Tested against a simulated candidate with planted traps (numbers only in a deck, a manager's summary that overstated her part, leadership and customer work missing from her CV), with and without the skill.

- Workflow: set up, gather before asking, draft early, interview in numbered batches, map lines to the reader, edit in their voice, deliver, practise.
- Never fills a gap with a guess; records someone else wrote are confirmed before use; every line must survive five minutes of questions.
- Hidden roles asked as their own batch, including customer-facing work, which a nearby question missed in testing.
- Internal numbers offered as options (exact with source, rounded, unmeasured, left out) instead of a yes/no, and results too vague to check are cut.
- Four outputs: sourced interview notes, an editable CV, .docx and PDF, and an interview practice list with concept checks and what a good answer covers.

## migrate-to-fable-5-2 0.1.0 · 2026-11-12

First release. Written from Anthropic's guide [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2), as it read on 12 November 2026. Not yet run on a real migration.

- Workflow: ask what the repo can't answer, list every place instructions reach the model, calibrate effort, audit what was carried over, fix observed behaviors, report.
- Nine kinds of leftover from earlier models, each with search terms, why it misbehaves on Fable 5.2 and what to do.
- Eight observed behaviors mapped to fixes, with Anthropic's suggested prompt texts quoted, their measured effect, their token cost and when to leave them out.
- Removal before addition, one fix per observed behavior, and prompt changes shipped to new conversations only.

## delegate 0.1.0 · 2026-10-26

First release. The working mode I use for most implementation work.

- Role split: the main agent plans, writes hard logic and reviews; a strong model writes taste-sensitive code, a fast model writes grunt work.
- Delegates by the shape of the work, not its size: clean interfaces, parallel packages and mechanical work go out; coupled changes, debugging and iterative UI work stay inline.
- Spec template with enumerated edge cases and acceptance criteria, diff review against the spec, fix rounds to the same agent with a two-round cap and escalation.

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
