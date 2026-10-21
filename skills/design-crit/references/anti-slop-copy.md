# Anti-slop: copy tells

last_reviewed: 2026-10-21
re-check by: 2027-04

## How to use this

Slop is lost specifics: the real fact replaced by the most common default. The fix is specifics, not synonyms. A tell is a flag, not a verdict. The brief, PRODUCT.md or DESIGN.md can earn any of them, so never flag what the brief asks for. Judge density, not single hits (thresholds below). Write "reads generic", never "AI-written": detectors and humans are unreliable, and non-native writers get falsely flagged. First test for any text: could an unrelated product use this unchanged?

Protect human voice. First person, direct address, anecdotes and real enthusiasm are human signals. Do not strip them.

Check Claude's current tics first: "less like X and more like Y", "rather than merely", "matters because", "It's not X, it's Y" / "not just X but Y". Lists go stale and 65% of tells are model-specific, so keep this list short and versioned.

Evidence labels: widely cited (3+ independent), single source, inference. Source keys: Wiki (Wikipedia: Signs of AI writing), Graphite, Kobak, Reinhart, WaPo, NN/g, Mailchimp.

## Vocabulary

### `ai-vocab-density`
- Looks like: delve, underscore, showcase, pivotal, crucial, tapestry, testament, vibrant, intricate, foster, enhance, landscape, align with. Wiki mid-2026 adds: matters, leverage, multifaceted, quietly, steady, dependable.
- Why it reads generic: instruction-tuned models over-use these words; the excess is style words (Kobak: "delves" ~28x; Reinhart: "tapestry" in 23% of GPT-4o outputs, over 100x human).
- Test: count distinct terms from the list per short block. One hit is not a flag.
- Instead: name the thing. Bad: "A vibrant tapestry of features" → better: "Six export formats, including PDF and CSV".
- Evidence: widely cited (3+) — Kobak, Reinhart, Wiki

### `saas-hype-verbs`
- Looks like: unlock, supercharge, empower, elevate, seamless, unleash, game-changer, transform.
- Why it reads generic: claims an effect without naming the work done.
- Test: replace the verb with what the product does. Does the sentence get more concrete?
- Instead: Bad: "Supercharge your productivity" → better: "Organizes your tasks, saving you hours each week".
- Evidence: widely cited — vendor-blog grade as an AI tell specifically

### `puffery-significance`
- Looks like: stands as a testament, plays a pivotal role, nestled in the heart of, rich heritage, evolving landscape.
- Why it reads generic: asserts importance instead of showing it.
- Test: delete the phrase. Is any fact lost?
- Instead: Bad: "Plays a pivotal role in onboarding" → better: "Sends the first invoice template on day one".
- Evidence: widely cited — Wiki and others

### `stiff-synonyms`
- Looks like: utilize, facilitate, leverage where use or help fits.
- Why it reads generic: longer words for the same meaning.
- Test: swap in the short word. Same meaning?
- Instead: Bad: "Utilize filters" → better: "Use filters".
- Evidence: widely cited

### `elegant-variation`
- Looks like: the same thing called "project", "workspace", "board" across screens.
- Why it reads generic: cycling synonyms for literary effect. In UI it confuses users.
- Test: list names for each object. More than one per object is a flag.
- Instead: one term per thing, everywhere. Contested for non-native writers, so flag softly.
- Evidence: single source, contested

## Structure

### `negative-parallelism`
- Looks like: "It's not X, it's Y"; "not just X but Y"; "less like X and more like Y"; "rather than merely"; "matters because".
- Why it reads generic: corrective framing against an argument nobody made. Graphite 2026: Claude Opus 5 uses "less like X and more like Y" 105x, "rather than merely" 160x, "matters because" 132x the human rate. WaPo: "not just X, but Y" in 6% of ChatGPT chats, Jul 2025.
- Test: who said X? If no one did, the contrast is filler.
- Instead: Bad: "It's not a to-do app, it's a calm place to work" → better: "Plan your week in one list. Nothing syncs until you say so."
- Evidence: widely cited — Graphite, WaPo. Current Claude tic.

### `rule-of-three`
- Looks like: triads of adjectives or benefits, "fast, simple, and secure".
- Why it reads generic: a sign only when the items are superficial or interchangeable.
- Test: more than one triad per block, or could the adjectives swap places?
- Instead: Bad: "Fast, simple, secure" → better: "Loads in under a second" (only if true and measured).
- Evidence: widely cited

### `participle-tail`
- Looks like: a sentence ending ", highlighting…", ", ensuring…", ", reflecting…".
- Why it reads generic: adds a vague claim of significance. Reinhart: 2 to 5x human.
- Test: cut the tail. Does the sentence lose a fact?
- Instead: Bad: "Syncs hourly, ensuring your data stays current" → better: "Syncs hourly".
- Evidence: widely cited — Reinhart

### `copula-avoidance`
- Looks like: "serves as", "stands as", "boasts" instead of is or has.
- Why it reads generic: grander verb, same fact.
- Test: replace with is/has. Same meaning?
- Instead: Bad: "The dashboard serves as a hub" → better: "The dashboard shows all open orders".
- Evidence: single source, strong

### `didactic-hedge`
- Looks like: "it's important to note", "worth noting", "may vary".
- Why it reads generic: announces importance instead of stating the point.
- Test: delete the phrase. Is the sentence still true and clear?
- Instead: Bad: "It's important to note that exports take time" → better: "Exports take about 2 minutes".
- Evidence: widely cited

### `summary-closer`
- Looks like: "In summary", "Overall", a paragraph restating the above.
- Why it reads generic: repeats instead of ending.
- Test: does the last paragraph add anything the page did not say?
- Instead: end on the next action.
- Evidence: single source

### `generic-opener`
- Looks like: "In today's fast-paced world…".
- Why it reads generic: says nothing about this subject.
- Test: delete the first sentence. Is anything lost?
- Instead: start with the first fact the reader needs.
- Evidence: blog-grade

### `uniform-rhythm`
- Looks like: sentences of similar length; longer words (5.2 to 5.7 characters vs 4.9 human, per Graphite).
- Why it reads generic: no variation in cadence.
- Test: read aloud. Is there a short sentence anywhere?
- Instead: mix short and long; prefer the short word.
- Evidence: single source — Graphite

## Punctuation and format

### `em-dash-density`
- Looks like: several em dashes per paragraph or per UI string; spaced "WORD — fragment" labels.
- Why it reads generic: ChatGPT went from under 10% to over 50% of replies by mid-2025 (WaPo). Now suppressed: GPT-6 at ~1/8 the human rate, Claude Opus 5 near human (Graphite 2026).
- Test: never flag one dash. Flag more than 1 per UI string or more than ~2 per 100 words.
- Instead: rewrite the sentence; do not just swap for a colon, which is its own sign.
- Evidence: contested

### `title-case-headings`
- Looks like: Every Word Capitalized In Headings.
- Why it reads generic: not inherently AI; a house-style issue.
- Test: does the house style say sentence case?
- Instead: enforce sentence case as a house rule.
- Evidence: widely cited, not inherently AI

### `bold-inline-headers`
- Looks like: bold lead-ins on every bullet; bold scattered through paragraphs.
- Why it reads generic: structure imposed on prose.
- Test: if you remove the bold, does anything get harder to scan?
- Instead: bold only for the one thing the reader must not miss.
- Evidence: single source

### `emoji-bullets`
- Looks like: emoji at the start of lines or bullets.
- Why it reads generic: WaPo found emoji in 70% of ChatGPT messages; the check mark emoji 11x.
- Test: line-start emoji in a non-playful product.
- Instead: plain bullets or real icons.
- Evidence: widely cited — WaPo

### `template-chrome`
- Looks like: ALL-CAPS eyebrow, "A · B · C" strings, "→" on buttons.
- Why it reads generic: decorative punctuation and labels.
- Test: remove them. Is anything lost?
- Instead: plain verb+object labels.
- Evidence: single source — FD

### `placeholder-leak`
- Looks like: [Your Name], 2025-XX-XX, lorem text.
- Why it reads generic: template left unfilled.
- Test: grep for brackets and XX patterns. Any hit is a flag.
- Instead: fill with real content or remove.
- Evidence: single source, unambiguous

## Tone

### `sycophancy-chat-residue`
- Looks like: "Great question!", "Certainly!", "I hope this helps".
- Why it reads generic: chat-assistant residue pasted into product copy (Sharma, ICLR 2024).
- Test: grep. Does a person say this to a user of a tool?
- Instead: Bad: "Great question! Here's how…" → better: start with the answer.
- Evidence: widely cited — Sharma 2024

### `preamble`
- Looks like: "Here is…", "Based on…" before the content.
- Why it reads generic: announces instead of delivering.
- Test: delete the first line. Is anything lost?
- Instead: Bad: "Here is a summary of your usage" → better: "Usage this month".
- Evidence: single source — Anthropic

### `exclamation-inflation`
- Looks like: "!" on many strings; any in error messages.
- Why it reads generic: Mailchimp allows at most one and none in errors. Note humans use "!" over 100x more than current models (Graphite), so scarcity is not the tell here.
- Test: count "!" per screen; any in an error?
- Instead: save it for real good news.
- Evidence: single source

## Content

### `vague-attribution`
- Looks like: "experts say", "industry leaders trust us".
- Why it reads generic: authority with no source.
- Test: can you name the expert or customer?
- Instead: Bad: "Industry leaders trust us" → better: "Used by 40 clinics in Ohio" (only if true and cited).
- Evidence: widely cited

### `invented-stats`
- Looks like: a number with no source, date or denominator.
- Why it reads generic: false specificity.
- Test: is there a citation or a way to check it? Never accept an uncited number.
- Instead: cite source and denominator, or remove.
- Evidence: strong as a rule (findnewpath CLAUDE.md:9)

### `regression-to-generic`
- Looks like: a specific fact replaced by a generic positive claim.
- Why it reads generic: the core mechanism of slop.
- Test: compare to the source material. Which fact disappeared?
- Instead: Bad: "A seamless experience" → better: the actual change (one-click refunds).
- Evidence: widely cited — Wiki

### `filler-sections`
- Looks like: "Challenges and Future Outlook"; a line under a heading that repeats the heading.
- Why it reads generic: sections exist because a template has them.
- Test: delete the section. Does the page lose information?
- Instead: keep only sections with content.
- Evidence: single source

## UI copy

### `cta-generic`
- Looks like: Submit, Get started, OK.
- Why it reads generic: any product could use it.
- Test: does the button say what happens?
- Instead: Bad: "Submit" → better: "Send invoice".
- Evidence: craft rule

### `error-vague-or-cute`
- Looks like: "Oops! Something went wrong".
- Why it reads generic: says nothing of cause or fix.
- Test: does it say what failed, why, and what to do?
- Instead: Bad: "Oops! Something went wrong" → better: "Couldn't save. You're offline. Your edits are kept; we'll retry when you reconnect."
- Evidence: craft rule — NN/g 2023

### `empty-state-mood`
- Looks like: "Nothing here yet ✨".
- Why it reads generic: mood instead of help.
- Test: does it say why it is empty and what to do next?
- Instead: Bad: "Nothing here yet ✨" → better: "No invoices yet. Create your first invoice."
- Evidence: craft rule

### `onboarding-hype`
- Looks like: "Welcome to the future of X".
- Why it reads generic: promise before first task.
- Test: does it name the first task and its payoff?
- Instead: Bad: "Welcome to the future of billing" → better: "Add a client to send your first invoice".
- Evidence: craft rule

### `loading-fake`
- Looks like: "Working magic…".
- Why it reads generic: hides the real operation.
- Test: does it name the real operation and give honest timing?
- Instead: Bad: "Working magic…" → better: "Importing 2,140 rows. About 30 seconds."
- Evidence: craft rule

## Greps

Case-insensitive. A hit starts a check; it is not a finding.

- `\[Your |XXXX|\d{4}-XX|lorem ipsum` (placeholders)
- `great question|certainly!|i hope this helps|here is|based on` (chat residue, preamble)
- `less like .* and more like|rather than merely|matters because|not just .* but|it's not .*, it's|it is not .*, it is` (corrective framing)
- `it's important to note|it is important to note|worth noting|may vary` (hedges)
- `delve|underscore|showcase|pivotal|crucial|tapestry|testament|vibrant|intricate|foster|enhance|landscape|align with|leverage|multifaceted` (vocabulary)
- `unlock|supercharge|empower|elevate|seamless|unleash|game-changer|transform` (hype verbs)
- `utilize|facilitate` (stiff synonyms)
- `^\s*[-*]?\s*\p{Emoji}` (line-start emoji)
- Title case: headings where most words are capitalized
- Numbers with no source nearby (uncited stats)
- `—` count per string and per 100 words

## Density thresholds

Our inference, calibrated to Graphite's bar that a tell is meaningful at 2x the human rate. Not tested values.

- 2 or more distinct AI-vocab terms in one short block
- More than 1 triad per section
- Em dash: more than 2 per 100 words, or more than 1 per UI string
- Corrective framing: more than 1 per page

## Pitfalls

- Bans shift tics: em-dash bans produce colons. Graphite: GPT total tells rose 48% while known ones fell. Antislop (ICLR 2026): naive banning breaks about 2,000 patterns and DPO suppression hurts quality. Rewrite toward specifics, not synonyms.
- Detector and human error: Liang 2023 flagged 61.22% of TOEFL essays; human detection is near chance. Say "reads generic".
- Over-sanding: keep first person, direct address, anecdotes, real enthusiasm.
- Lists go stale: re-check every 6 to 12 months.

## Sources

- https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11874169/
- https://arxiv.org/abs/2508.01930
- https://graphite.io/five-percent/research/ai-tells
- https://www.bostonglobe.com/2025/11/13/business/chatgpt-writing-style-clues/
- https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html
- https://www.economist.com/culture/2026/07/30/how-to-spot-ai-writing
- https://www.optimizely.com/field-notes/articles/in-defense-of-the-em-dash-and-everything-else-on-this-ai-tell-trial
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- https://arxiv.org/abs/2510.01171
- https://arxiv.org/abs/2310.13548
- https://arxiv.org/abs/2510.15061
- https://arxiv.org/pdf/2304.02819
- https://arxiv.org/abs/2409.01754
- https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/
- https://styleguide.mailchimp.com/voice-and-tone/
- https://www.nngroup.com/articles/error-message-guidelines/
- https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/
- https://microcopyexamples.substack.com/p/avoid-landing-page-words
