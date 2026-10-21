# Anti-slop: design tells

last_reviewed: 2026-10-21
re-check by: 2027-04

## How to use this

Slop is lost specifics: the real fact about this product replaced by the most common default. The fix is specifics, not synonyms or a different default. A tell is a flag, not a verdict. The brief, PRODUCT.md or DESIGN.md can earn any of them, so never flag what the brief asks for. Judge the density of tells across a screen, not single hits. Write "reads generic", never "AI-made". First test for any screen: could an unrelated product use this unchanged? If yes, flag it even when no listed tell matches.

Evidence labels: "widely cited (N)" is N independent sources. Impeccable (IMP, CF) counts as one lineage; Anthropic (FD, ANT) as one. Source keys: PRG, 925, KR, IMP, CF, FD, ANT, SD, CH, REM, HN are the research notes' abbreviations.

## Layout

### `identical-icon-card-grid`
- Looks like: three or four equal cards, each icon + short heading + one sentence.
- Why it reads generic: structure ignores content; every feature gets the same weight.
- Test: swap the card text with another product's. Does the grid still work with no layout change?
- Instead: size and place each feature by importance; show the feature itself (UI, output), not an icon for it.
- Evidence: widely cited (7) — PRG, 925, KR, IMP/CF, FD, SD, CH

### `centered-hero-cta`
- Looks like: centered headline, one-line subhead, two buttons, nothing that shows the product.
- Why it reads generic: the hero is a template slot, not the most characteristic thing in the subject's world.
- Test: cover the logo. Does the hero say what the product does or who it is for?
- Instead: lead with the real product, output or artifact; one primary action.
- Evidence: widely cited (4)

### `hero-metric-block`
- Looks like: a big number with a small label ("10x faster", "99.9%") under the hero.
- Why it reads generic: the number is decoration; no source, denominator or context.
- Test: can you find what the number measures, for whom, and from where?
- Instead: a real, sourced figure in context, or no figure.
- Evidence: widely cited (3)

### `fake-sequence-numbers`
- Looks like: "01 / 02 / 03" or "Step 1, 2, 3" labels on content that has no order.
- Why it reads generic: numbering borrows the look of process without a process.
- Test: would reordering the items change the meaning? If not, the numbers are decoration.
- Instead: number only real sequences; otherwise drop the labels.
- Evidence: widely cited (3)

### `nested-cards`
- Looks like: a card inside a card inside a section, each with its own border and radius.
- Why it reads generic: containers used for every grouping instead of spacing and alignment.
- Test: remove the inner borders. Is grouping still clear?
- Instead: one level of container; group with space and type.
- Evidence: single source — IMP lineage

### `template-rhythm`
- Looks like: hero, three features, CTA band, footer, in that order.
- Why it reads generic: the page follows the common sequence, not the story of this product.
- Test: could you reorder the sections of a competitor's page into this one with no edits?
- Instead: order sections by what this buyer needs to decide.
- Evidence: single source — practitioner

## Type

### `default-sans`
- Looks like: Inter, Roboto or Geist at default weights with no typographic decision visible.
- Why it reads generic: the most common font in the training data, chosen by omission.
- Test: is there a second typeface, a weight contrast or a size scale that was clearly chosen?
- Instead: a font tied to the product's character, with defined roles (display, body, data).
- Evidence: widely cited (6+)

### `second-wave-fonts`
- Looks like: Space Grotesk, Instrument Serif or Geist used as the "non-default" choice.
- Why it reads generic: avoiding Inter moved the default; ANT saw output converge on Space Grotesk after Inter was banned.
- Test: is the font here because of the brand, or because it is the usual alternative?
- Instead: pick from the subject's world (signage, print, interface heritage) and say why.
- Evidence: widely cited (2) — ANT, 925

### `accent-word-headline`
- Looks like: one word in the headline in italic, serif or gradient color.
- Why it reads generic: a stock device to fake emphasis.
- Test: remove the styling. Does the headline lose meaning, or only decoration?
- Instead: a headline whose words carry the emphasis.
- Evidence: widely cited (3)

### `eyebrow-label`
- Looks like: small ALL-CAPS tracked label above every section heading.
- Why it reads generic: repeated on every section it labels nothing.
- Test: count eyebrows per page. Does each add information the heading lacks?
- Instead: use one only where it adds a category the reader needs. Note the brief may call for it.
- Evidence: widely cited (5)

### `costume-mono`
- Looks like: monospace for labels and badges on a product that is not technical.
- Why it reads generic: "developer" styling as a costume.
- Test: is there code, data or IDs in that text? If not, the mono is decoration.
- Instead: mono for actual code, IDs and tabular data.
- Evidence: widely cited (2) — plus HN

### `flat-hierarchy`
- Looks like: weights 400 vs 600 only, sizes close together.
- Why it reads generic: hierarchy is timid, so everything is medium importance.
- Test: squint. Can you tell the first, second, third read?
- Instead: bigger jumps (ANT: 100/200 vs 800/900) and clear size steps.
- Evidence: widely cited (2) — ANT, IMP

## Color and surface

### `purple-indigo-gradient`
- Looks like: indigo-to-violet gradients on hero, buttons or backgrounds.
- Why it reads generic: Tailwind indigo-500 is a library default; KR calls it "VibeCode Purple" (gradients on 28% of sites sampled).
- Test: is the purple in the brand? If not, why is it there?
- Instead: a palette derived from the product or its subject.
- Evidence: widely cited (8+) — KR, PRG, IMP and others

### `gradient-text`
- Looks like: headline or number filled with a gradient.
- Why it reads generic: emphasis by effect; also lowers contrast.
- Test: does the text still read at solid color, and is contrast fine at its lightest stop?
- Instead: solid color; emphasis through size and weight.
- Evidence: widely cited (2)

### `glow-dark-mode`
- Looks like: dark background, neon glow on cards, buttons or borders.
- Why it reads generic: KR measured 20.3% of sampled sites as always-dark; the glow is the default dark look.
- Test: remove the glows. Does any hierarchy depend on them?
- Instead: dark surfaces with defined elevation steps and restrained accents.
- Evidence: widely cited (3+) — KR

### `decorative-glass`
- Looks like: frosted, blurred translucent panels with no content behind them.
- Why it reads generic: blur used as style, not to show layering.
- Test: what is behind the glass? If nothing meaningful, it is decoration.
- Instead: solid surfaces, or blur only over real content.
- Evidence: widely cited (4)

### `side-stripe-border`
- Looks like: card or callout with a thick colored left border.
- Why it reads generic: IMP calls it the most recognizable tell; it marks "important" without a reason.
- Test: delete the stripe. Does the card lose any meaning?
- Instead: state the type of callout in the content or use a real icon and label.
- Evidence: widely cited (5) — IMP

### `uniform-soft-shadow-radius`
- Looks like: every element with the same large radius and soft shadow.
- Why it reads generic: one default applied everywhere removes depth cues.
- Test: list radii and shadows used. Is there more than one, with a rule?
- Instead: a small radius and shadow scale tied to element role.
- Evidence: widely cited (4)

### `tasteful-ai-cream`
- Looks like: cream background (#F4F1EA), serif headings, terracotta accent (#D97757).
- Why it reads generic: the second-generation default that replaced purple; the "tasteful AI" look.
- Test: could this palette sit on an unrelated product unchanged?
- Instead: a palette from the product's own materials.
- Evidence: widely cited (3) — second-gen tell

### `broadsheet-costume`
- Looks like: newspaper masthead rules, dateline, columns on a product that is not publishing.
- Why it reads generic: editorial styling as a costume.
- Test: is there editorial content that needs these devices?
- Instead: use print devices only for real editorial content.
- Evidence: single source

### `fake-black`
- Looks like: #0B0B0B (near-black) backgrounds with no tinted neutrals.
- Why it reads generic: the default dark; no relation to the palette.
- Test: do the neutrals carry a hue from the brand?
- Instead: tint the neutral scale toward the brand hue.
- Evidence: single source

### `unthemed-browser-chrome`
- Looks like: default text selection, caret, scrollbar, focus ring; proportional digits in tables.
- Why it reads generic: details left at browser defaults show no one finished the surface.
- Test: select text, tab through, scroll, check number columns. Any default left?
- Instead: themed selection, caret, scrollbar and focus; tabular numbers for data.
- Evidence: single source — checkable in DOM

## Icons and imagery

### `emoji-icons`
- Looks like: emoji as feature or bullet icons.
- Why it reads generic: stands in for an icon system; renders differently per platform.
- Test: would a designer have chosen these glyphs for this brand?
- Instead: one consistent icon set, or real imagery.
- Evidence: widely cited (4)

### `generic-line-icons`
- Looks like: thin stock line icons (lightning, shield, rocket) for abstract benefits.
- Why it reads generic: the icon names a cliché, not the feature.
- Test: does the icon depict something specific to the feature?
- Instead: show the feature, or omit the icon.
- Evidence: single source

### `placeholder-illustration`
- Looks like: abstract blobs, grid or dot backgrounds, 3D shapes unrelated to the product.
- Why it reads generic: fills space with no information.
- Test: what does the image tell the user? If nothing, flag it.
- Instead: product screenshots, real photos, diagrams of the actual mechanism.
- Evidence: single source — plus REM

### `sparkline-as-content`
- Looks like: tiny charts or fake dashboards with no axes, data or labels.
- Why it reads generic: shows "data" without any.
- Test: can you read a value, unit and time range?
- Instead: a real chart with labels, or no chart.
- Evidence: widely cited (2)

## Components

### `stock-shadcn`
- Looks like: unmodified shadcn/Tailwind components in default theme.
- Why it reads generic: KR found 23.5% of Show HN sites; the shadcn changelog admits "the defaults were a little too good".
- Test: any token or component changed from the default?
- Instead: change tokens first (radius, color, type), then component shape.
- Evidence: widely cited (3) — KR, shadcn changelog

### `missing-states`
- Looks like: only the happy path shown; no empty, loading, error, disabled or hover/focus states.
- Why it reads generic: generated from static examples; states were never designed.
- Test: trigger empty, error and loading. Does each exist and fit the system?
- Instead: design each state with a real message and next action.
- Evidence: widely cited (3) — PRG, SD

## Motion

### `scattered-entrances`
- Looks like: fade-up on every element, hover-lift on every card.
- Why it reads generic: motion applied everywhere says nothing is important.
- Test: count animated elements. Is there one orchestrated moment or twenty?
- Instead: one orchestrated page load (ANT); motion only where it explains change.
- Evidence: widely cited (2) — ANT

### `bounce-pulse-marquee`
- Looks like: bouncing arrows, pulsing badges, scrolling logo marquees.
- Why it reads generic: attention-grabbing loops with no function.
- Test: what does the motion communicate? Does it stop?
- Instead: motion tied to state change; respect reduced-motion.
- Evidence: single source

## Content

### `weightless-copy`
- Looks like: "Build faster. Ship smarter." Two short parallel claims.
- Why it reads generic: any product could print it.
- Test: could an unrelated product use this unchanged?
- Instead: name the object, the user and the outcome. See anti-slop-copy.md.
- Evidence: widely cited (3)

### `chrome-punctuation`
- Looks like: "A · B · C" strings, arrows on buttons, em dashes in labels.
- Why it reads generic: punctuation as decoration.
- Test: remove the marks. Is anything lost?
- Instead: plain labels; an arrow only where direction matters.
- Evidence: single source — plus IMP

## Second-generation tells

Bans move the tic. After Inter was banned, output converged on Space Grotesk. After purple was banned, it moved to cream, serif and terracotta. Tells also date: purple and glass peaked around 2022, cream and Instrument Serif are current. So do not accept a swap as a fix. Ask whether the new choice came from the product.

## Pitfalls

- Bans create a new monoculture (Space Grotesk, cream look). Rewrite toward specifics, not toward the next default.
- Do not ban what the brief asks for. The brief wins (FD). An absolute eyebrow ban contradicts a rule that lets the brief earn it (CF).
- No single tell proves anything (KR). Many conventions predate LLMs (REM).
- Over-correcting into weird has no documented evidence; treat as inference.
- Vague rules cannot be checked (ROP, CH). Every flag needs a test a reviewer can run.
- Not verified in the research: Wathan tweet text, New Yorker "Claudian sameness", Hallmark 57 gates, NN/g or v0 guidance.

## Sources

- https://claude.com/blog/improving-frontend-design-through-skills
- https://www.adriankrebs.ch/blog/design-slop/
- https://impeccable.style/anti-patterns
- https://www.mintlify.com/pbakaus/impeccable/concepts/anti-patterns
- https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website
- https://www.925studios.co/blog/ai-slop-design-tells
- https://robotsonpayroll.substack.com/p/how-to-avoid-that-vibe-coded-look
- https://www.superdesign.dev/blog/why-ai-design-looks-generic
- https://ui.shadcn.com/docs/changelog/2025-12-shadcn-create
- https://github.com/Vinayak-Shukla-03/anti-ai-slop
- https://docs.lovable.dev/prompting/prompting-one
- https://docs.lovable.dev/features/design-guidance
- https://chaseai.io/blog/claude-code-frontend-design-skills
- https://www.remio.ai/post/hacker-news-finds-the-ai-aesthetic-and-the-real-conflict-is-authorship
- https://arxiv.org/abs/2510.01171
- https://www.microsoft.com/en-us/research/?p=1171164
- https://arxiv.org/abs/2607.22928
- https://northeasttimes.com/2026/07/31/ai-design-tools-are-making-every-website-look-the-same/
- https://www.designsystemscollective.com/is-anyone-else-tired-of-every-tailwind-shadcn-app-looking-the-same-69c545e73114
- https://github.com/Laith0003/ux-skill/wiki/Anti-AI-slop-ban-list
