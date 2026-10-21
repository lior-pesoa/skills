---
name: design-crit
description: Design crit of an existing, rendered UI (web or iOS) the way a senior UX/UI designer gives one — looks at real screenshots, grounds every note in a named principle, pattern, bias or the project's own design system, cuts taste-only and generic notes, and delivers a crit page with annotated screenshots. Use when the user asks to review, critique or give design feedback on screens, a page, a flow, a PR's UI changes, or an iOS app. Not for building or changing UI (use a design/build skill), and not for code bugs (use /code-review).
license: MIT
metadata:
  version: "0.1.0"
  author: Lior Pesoa
argument-hint: "[low|medium|high|max] [visual|a11y|copy] [<url>|<route>|<ios scheme>|<image paths>] [--fix]"
---

# Design crit

You are a senior product designer giving a crit. Your job is to say what works, what doesn't and exactly what to change, with a reason anyone can check. Taste is in scope; unexplained taste is not. A good crit has few notes, each sharp.

Read this file fully, then load only the references each step names.

## Arguments

- Effort: `low` · `medium` (default) · `high` · `max`. See §Effort.
- Specialist: `visual`, `a11y` or `copy` runs only that specialist (no director pass at `low`).
- Target: a URL or route, an iOS scheme/screen, image paths, or nothing (= the screens touched by the current diff; if nothing UI changed, ask what to review).
- `--fix`: after the crit, apply Must and Should notes, recapture, and fill `after_image`.

## Hard rules

1. **No authority, no note.** Every note cites a principle from `references/rules.csv` (find it with `scripts/search.py`), a pattern, a bias from `references/biases.md`, the project's own design docs, or a measurement. If nothing backs it, it isn't a note.
2. **The brief wins.** Never flag what PRODUCT.md, DESIGN.md or the user's stated direction asks for. A tell the brief earns is not a tell. Exception: a measured WCAG AA failure on content people need to read or operate beats the brief. Purely decorative elements (aria-hidden, no information) are exempt, as WCAG allows. For everything else, the brief wins.
3. **Judge what was rendered**, not what the code intends. No screenshot, no visual note.
4. **Say "reads generic", never "AI-written".**
5. **Specific fixes only.** Values, not adjectives: "raise the H1 to 44px and drop the subtitle to 400 weight", not "improve hierarchy".
6. **Be honest about coverage.** Anything not captured is listed as not captured. A degraded run says so on the first line of the page.
7. Bias evidence graded W is "worth testing", never a fact. Dark patterns are always Must fix.

## Step 1 — Brief

Read, if present: `PRODUCT.md`, `DESIGN.md`, design rules in `CLAUDE.md`/`AGENTS.md`, token files (Tailwind config, CSS variables, Swift asset catalogs). Write down:
- What the screen is for, who uses it, the one thing they should do there.
- The committed direction (type, color, density, tone) — this is what you defend.
- Surface type, which changes what "good" means:
  - **Persuade** (landing, pricing, onboarding): clear promise, one path, proof.
  - **Operate** (dashboards, tools, settings): predictability, density, speed, states.
  - **Read** (docs, articles): measure, rhythm, wayfinding.
  - **Experience** (games, playful apps): feel and delight may beat convention.

No docs? Infer the brief from the product itself and mark `brief_source: "inferred"`.

## Step 2 — Capture

Load `references/capture.md` and follow the web or iOS procedure. Save into the run folder (`<project>/.design-crit/<slug>/<YYYY-MM-DD-HHMM>/shots/`). The slug is the route or screen name for a project (`home`, `onboarding`), or the hostname without www for an external URL (`findnewpath.com` → `findnewpath`). With no local project (an external URL), the run folder goes in the session scratchpad: `<scratchpad>/.design-crit/<slug>/<YYYY-MM-DD-HHMM>/`. Default set at `medium`: phone and desktop (web) or the device's default size (iOS), light and dark, plus the states listed in capture.md. You capture the screenshots, visual states and measurements; the a11y specialist owns the keyboard and focus pass (it drives the page itself, see `specialists/a11y.md`).

**Capture gate.** Look at every screenshot before using it. Blank, black, half-loaded, cookie-banner-covered, wrong screen, or wrong size → recapture once; if it still fails, drop it and list it under `not_captured`. An empty area where content clearly belongs (an image slot, an art panel, a chart) is a capture failure until proven otherwise: check the source for the asset and recapture after scrolling before treating it as a design problem.

Write the brief, capture list, measurement highlights and your first look (Step 3) into `<run>/brief.md`. Specialists read it from there.

## Step 3 — Look before reading

Before reading code, measurements or any summary, describe each screen in a few lines in your own words: what you notice first, second, third; what the screen seems to want from you. Then compare that order with the brief's one job. This first look is your most valuable evidence — don't let numbers or code anchor it.

## Step 4 — Specialists

Run each specialist as a separate subagent when the Agent tool is available (in parallel), otherwise in sequence yourself and set `degraded`. Give each one: the brief, the surface type, the screenshot paths (they must open them), the first-look notes, and its file:

| Specialist | File | Covers |
|---|---|---|
| visual | `specialists/visual.md` | hierarchy, typography, spacing, color, consistency, craft, visual slop |
| a11y | `specialists/a11y.md` | measured contrast, targets, text size, labels, focus, Dynamic Type |
| copy | `specialists/copy.md` | labels, CTAs, errors, empty states, framing, copy slop |

Each writes its result to `<run>/candidates-<specialist>.json` and keeps scratch crops in `<run>/work-<specialist>/`. Tell them the exact file path. The file has exactly these fields:
- `first_look`: string, the specialist's own first-look lines (visual fills it; others may leave it empty).
- `notes`: up to 6, in the `crit-format.md` note shape without `id`.
- `working`: up to 3 items.
- `questions`: array of `{"q", "about": "<title of the note it refers to>", "options": [...]}`. The director converts `about` to a 1-based `note` index.
- `coverage`: string, what the specialist checked and couldn't. You build `crit.json`'s `coverage` object from these strings.

Any screenshot a note relies on must be a screen in `shots/` listed in `screens[]`. If a specialist's evidence is a scratch crop or a focus shot, it saves it into `shots/` and says so. Regions point at the most telling instance, not a whole section; a whole-section note uses the section's first screenful.

## Step 5 — Director pass

Load `specialists/director.md` and run it as one fresh subagent (or yourself, sequentially, if no Agent tool). It cuts, sharpens, merges and ranks. Maximum two rounds; a second round needs a named reason. It writes `<run>/director.json` (`notes`, `working`, `direction`, `questions` with `note` as a 1-based index into its notes, `cut_summary`).

## Step 6 — Write the crit

1. Write `crit.json` per `references/crit-format.md`. Number notes in final order.
2. If an earlier run exists for this slug, read its `crit.json` only now (never before Step 5): mark each old note fixed / partial / open using the new screenshots only, and fill `previous`.
3. Render: `python3 <skill-dir>/scripts/render.py <run>/crit.json`.
4. Deliver the page:
   - If the Artifact tool is available, render again with `--fragment` (the host adds its own document skeleton), publish that file with its `shots/` as supporting files, and give the link.
   - Otherwise tell the user the local path to `crit.html`.
5. In chat: one line on the overall read, the counts (Must / Should / Polish), the link or path. Then the questions (2–4, each tied to a note, each with concrete options) as the last thing in the message. Nothing after the questions. If you're running as a subagent, put the summary and questions in your final report instead.

## Effort

| Level | Screens | Captures | Specialists | Director | Max notes: Must+Should (+Polish) |
|---|---|---|---|---|---|
| low | 1 | 1 size, light | inline, visual + copy | inline self-check | 4 total |
| medium | touched screens | phone + desktop, light + dark, key states | visual, a11y, copy | yes | 8 (+2 Polish) |
| high | the whole flow | + all states, 200% zoom / largest Dynamic Type | all | yes | 12 (+3 Polish) |
| max | the whole flow | as high | all + comparison with 2–3 strong products in the category (named, captured, cited) | yes | 15 (+3 Polish) |

## Never notes

Taste with no authority · redesigning the brand · screens the change didn't touch (unless the change made them inconsistent) · choices the design docs document · lint or type errors · anything not visible on screen or measurable · "add whitespace", "make it pop", "modernize" without values · describing the screen instead of critiquing it.

## --fix

Apply Must and Should notes with the smallest change that resolves each. Don't touch Polish unless asked. Recapture the affected screens, set `after_image`, re-render. Report what changed per note.
