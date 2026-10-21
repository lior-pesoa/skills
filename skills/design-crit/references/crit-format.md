# crit.json format

The lead writes one `crit.json` per run. `scripts/render.py` turns it into `crit.html`. The next run reads it to score old notes.

Run folder: `<project>/.design-crit/<slug>/<YYYY-MM-DD-HHMM>/` holding `crit.json`, `shots/*.png`, `crit.html`. With no local project, use `<scratchpad>/.design-crit/<slug>/<YYYY-MM-DD-HHMM>/`.

Slug: the route or screen name for a project (`home`, `onboarding`), or the hostname without www for an external URL (`findnewpath.com` → `findnewpath`).

```jsonc
{
  "version": 1,
  "target": "my-portfolio · / (homepage)",   // what was reviewed, human-readable
  "slug": "home",                               // stable across runs of the same target
  "title": "Homepage crit",                     // optional page name (2-4 words, no colon explainer); shown as the page heading when present
  "date": "2026-10-21",
  "effort": "medium",                           // low | medium | high | max
  "surface": "persuade",                        // persuade | operate | read | experience
  "brief": "One paragraph: what the screen is for, who uses it, the one job, the committed direction.",
  "brief_source": "PRODUCT.md, DESIGN.md",      // or "inferred"
  "method": "lead + visual + a11y + copy, director pass",
  "degraded": null,                             // or a string: "single context: no subagents"
  "coverage": {
    "captured": ["390 light", "390 dark", "1440 light", "1440 dark", "keyboard pass"],
    "not_captured": ["hover states", "error state"]
  },
  "direction": null,                            // one sentence only when something is fundamentally off
  "screens": [
    {
      "id": "home-390-light",
      "label": "Home · 390 · light",
      "image": "shots/home-390-light.png",       // relative to crit.json
      "width": 1170, "height": 7200,              // natural pixel size of the image
      "scale": 3                                    // optional: image pixels per CSS px / pt (device pixel ratio)
    }
  ],
  "working": [
    { "title": "Short claim", "why": "Why it works, so nobody 'fixes' it.", "screen": "home-1440-light",
      "region": { "x": 0, "y": 0, "w": 2880, "h": 1600 } }   // region optional
  ],
  "notes": [
    {
      "id": 1,
      "tier": "must",                           // must | should | polish
      "title": "One-line claim",
      "screen": "home-390-light",
      "region": { "x": 96, "y": 1840, "w": 980, "h": 420 },  // image pixels, same space as width/height
      "what": "What is wrong, concretely.",
      "principle": {
        "rule_id": "contrast-text",
        "name": "Text contrast (WCAG 2.2 SC 1.4.3)",
        "source": "W3C WCAG 2.2",
        "url": "https://www.w3.org/TR/WCAG22/#contrast-minimum",
        "evidence": "rule"                       // S | M | W | rule | heuristic. rule = standards, platform rules, the project's own system; heuristic = established practitioner heuristics (Nielsen, Gestalt, Laws of UX)
      },
      "effect": "What the user experiences.",
      "fix": "Minimal, specific change with values.",
      "specialist": "a11y",                     // visual | a11y | copy | interaction | pattern | platform
      "verdict": "confirmed",                   // confirmed | plausible
      "measured": "3.1:1 (#8A8F98 on #FFFFFF)",  // optional: the number behind the note
      "after_image": null                        // optional: shots/... after --fix
    }
  ],
  "questions": [
    { "q": "Question tied to note 2", "note": 2, "options": ["Option A", "Option B"] }
  ],
  "previous": null                               // or { "date": "...", "fixed": [1,3], "partial": [2], "open": [4] }
}
```

Rules
- `notes` are ordered must → should → polish, most severe first within a tier.
- Every note has a `principle` with a real `url`. No principle, no note.
- `region` is required on notes; renderer clamps it to the image.
- Any screenshot a note relies on must be a screen in `shots/` listed in `screens[]`. A scratch crop or focus shot used as evidence is saved into `shots/` first.
- `region` points at the most telling instance, not a whole section; a whole-section note uses the section's first screenful.
- `screens[].image` paths must exist; renderer reports missing files instead of failing.
