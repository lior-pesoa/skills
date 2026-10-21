# UX biases for UI and copy

last_reviewed: 2026-10-21

## How to use this

Cite as `bias-id (evidence; Author Year)`, for example: "default-effect (S; Jachimowicz 2019): annual preselected but no 'Recommended' label. Add the label or drop the preselection." Never write "this triggers FOMO".

Evidence grades: S = strong, M = mixed, W = weak or contested. (U) after a year means the figure or date is from memory and unverified. W items may only be suggested as "worth testing" (an A/B test), never stated as fact. lawsofux and growth.design do not grade evidence; treat them as candidate lists.

Ego depletion and decision fatigue are excluded. Never cite them (Hagger 2016, 23-lab replication, d=0.04).

Ethics test for every use: does it help the user decide, or decide for them? Misuse is a dark pattern and is Must fix.

For tools and B2B products, lean on cognitive load, defaults, progress and endings, and avoid urgency and scarcity. This is judgment, not tested evidence: most studies use consumer samples, and expert buyers weaken overload and decoy effects.

## Biases

### `framing-effect` — S
- Source: https://doi.org/10.1126/science.7455683
- What: the same facts choose differently depending on how they are put.
- In UI: "Data saver" instead of "Lower quality".
- In copy: Bad: "Churn fell from 85% to 80%" → better: "Retention rose from 15% to 20%" (same facts; pick the frame the user cares about, never one that hides the number).
- Fair use / misuse: a frame that is accurate and relevant to the user / a frame that hides the real number.
- Cite: Tversky & Kahneman 1981; Many Labs 2014 replicated it at about half the size.

### `anchoring` — S
- Source: https://doi.org/10.1126/science.185.4157.1124
- What: a first number shifts later judgments.
- In UI: annual price next to monthly price.
- In copy: Bad: "$29/mo" → better: "$29/mo (vs $49 billed monthly)".
- Fair use / misuse: anchor against a real alternative / an inflated "was" price.
- Cite: Tversky & Kahneman 1974; 2024 meta-analysis g≈0.83 across 2,601 effects.

### `precise-anchor` — M to S
- Source: https://doi.org/10.1111/j.1467-9280.2008.02057.x
- What: a precise number reads as better grounded than a round one.
- In UI: a stat line with source and sample size.
- In copy: Bad: "Saves hours" → better: "Saves 3.5 hrs/week (median, 2,140 teams)".
- Fair use / misuse: real, sourced figures / false precision.
- Cite: Janiszewski & Uy 2008.

### `loss-aversion` — S/M
- Source: https://www.aeaweb.org/doi/10.1257/jel.20221698
- What: losses weigh more than equal gains.
- In UI: Gmail storage warning.
- In copy: "You'll lose 3 saved drafts" (only for real, specific, user-owned losses).
- Fair use / misuse: warn about a real loss / confirmshaming.
- Cite: JEL 2024 meta-analysis λ≈1.96; Walasek 2018 ≈1.31; Gal & Rucker 2018 (U) disputes the effect.

### `default-effect` — S, heterogeneous
- Source: https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html
- What: people stay with the preselected option.
- In UI: recommended or privacy-safe option preselected.
- In copy: "Recommended for most teams", with a one-click opt-out.
- Fair use / misuse: a default that is best for most, labeled / preselection such as a pre-ticked add-on (see EU DSA Art. 25).
- Cite: Johnson & Goldstein 2003 (measured registered consent, not donations); Jachimowicz 2019 meta-analysis d=0.68, 58 studies.

### `decoy-effect` — M
- Source: https://doi.org/10.1086/208899
- What: a worse middle option makes another look better.
- In UI: a middle tier that makes the top tier look worth it.
- In copy: describe each tier by who it fits.
- Fair use / misuse: tiers that are real and distinct / a fake option built to steer.
- Cite: Huber 1982; Frederick 2014: mostly vanishes with realistic stimuli.

### `choice-overload` — W/M
- Source: https://edoc.unibas.ch/20586
- What: too many options may reduce choice or satisfaction.
- In UI: highlight one plan; add filters.
- In copy: "Most teams start with Team."
- Fair use / misuse: curate and filter / hide options the user needs.
- Cite: Iyengar & Lepper 2000; Scheibehenne 2010 meta-analysis mean ≈0; Chernev 2015 moderators. Never cite the jam study alone. Suggest "worth testing" only.

### `hicks-law` — S, simple stimulus-response only
- Source: https://doi.org/10.1080/17470215208416600
- What: choice time grows with the number of options.
- In UI: shorter menus, grouped actions. Rough guide only.
- In copy: fewer, clearer labels.
- Fair use / misuse: trim by task relevance / hide key options.
- Cite: Hick 1952 (U).

### `social-proof` — M
- Source: https://doi.org/10.1086/586910
- What: people follow what others do.
- In UI: "Most popular" tag.
- In copy: Bad: "Loved by thousands" → better: "4,812 teams switched last quarter".
- Fair use / misuse: real, recent, named reference group / fake counts; normalizing bad behavior.
- Cite: Goldstein 2008; Bohner & Schlüter 2014 null result; boomerang effect, Schultz 2007.

### `scarcity-urgency` — M
- Source: https://arxiv.org/abs/1907.07032v2
- What: limited supply or time raises perceived value.
- In UI: real stock count or real deadline.
- In copy: "Offer ends 31 Oct" only if it does.
- Fair use / misuse: live data / fake timers and low-stock claims.
- Cite: Worchel 1975 (U); Mathur 2019 found them across 11K sites. Avoid in tools and B2B (judgment).

### `goal-gradient` — S (field)
- Source: https://business.columbia.edu/sites/default/files-efs/pubfiles/1200/goalgradient.pdf
- What: effort rises as the goal gets closer.
- In UI: progress bar on setup.
- In copy: "2 of 5 done, 3 min left".
- Fair use / misuse: honest progress / progress that stalls or resets.
- Cite: Kivetz, Urminsky & Zheng 2006.

### `endowed-progress` — S/M
- Source: https://doi.org/10.1086/500480
- What: a head start raises completion.
- In UI: checklist begins with "Account created" checked.
- In copy: "1 of 4 done: account created".
- Fair use / misuse: pre-filled step is real / a fake completed step.
- Cite: Nunes & Drèze 2006 (U for figures).

### `zeigarnik-ovsiankina` — W (for memory)
- Source: https://doi.org/10.1057/s41599-025-05000-w
- What: unfinished tasks pull people back.
- In UI: "Resume draft".
- In copy: "Pick up where you left off".
- Fair use / misuse: resume real work / nag.
- Cite: Ghibellini & Meier 2025 meta-analysis: no memory advantage. The resumption urge is robust, so cite Ovsiankina, not Zeigarnik.

### `peak-end-rule` — S
- Source: https://doi.org/10.1111/j.1467-9280.1993.tb00589.x
- What: experiences are judged by the peak and the end.
- In UI: satisfying success state; calm cancellation.
- In copy: end errors and cancellations with the next step and a plain goodbye.
- Fair use / misuse: improve real endings / mask a bad experience.
- Cite: Kahneman 1993 (U); Alaybek 2022 r=.58.

### `serial-position` — S (list recall)
- Source: https://doi.org/10.1037/h0045106
- What: first and last items are remembered best.
- In UI: key nav at the ends.
- In copy: lead with the benefit; end with the CTA.
- Fair use / misuse: place by importance / bury the opt-out in the middle.
- Cite: Murdock 1962 (U). Weaker for UI scanning.

### `von-restorff` — S (memory)
- Source: https://lawsofux.com/von-restorff-effect/
- What: the distinct item stands out.
- In UI: one accent-colored primary CTA.
- In copy: make the main action the only emphasized one.
- Fair use / misuse: one clear primary / making the decline look disabled (visual interference).
- Cite: von Restorff 1933 (U).

### `labor-illusion` — M to S
- Source: https://doi.org/10.1287/mnsc.1110.1376
- What: visible effort raises perceived value.
- In UI: "Checking 412 flights…".
- In copy: name the real work and count.
- Fair use / misuse: real operations shown / fake delays.
- Cite: Buell & Norton 2011; Buell 2017 field study.

### `ikea-effect` — S/M
- Source: https://doi.org/10.1016/j.jcps.2011.08.002
- What: people value what they helped build.
- In UI: co-built setup, customizable template.
- In copy: "Make it yours" after real choices.
- Fair use / misuse: only if the user completes it / forced assembly.
- Cite: Norton 2012; Sarstedt 2017.

### `commitment-consistency` — M
- Source: https://doi.org/10.1146/annurev.psych.55.090902.142015
- What: small commitments lead to larger ones.
- In UI: a micro-commitment before signup.
- In copy: "Tell us your goal" before the form.
- Fair use / misuse: optional, useful step / forced action.
- Cite: Cialdini (U).

### `reciprocity` — M
- Source: https://doi.org/10.1146/annurev.psych.55.090902.142015
- What: value given first invites a return.
- In UI: useful content before the email ask.
- In copy: give the template, then ask.
- Fair use / misuse: a real gift / a trap gift that locks the user in.
- Cite: Cialdini (U).

### `reactance` — M
- Source: https://academic.oup.com/jla/article/13/1/43/6180579
- What: pressure triggers resistance.
- In UI: soft upsells, no blocking.
- In copy: Bad: "You must upgrade now" → better: "Upgrade when you need X".
- Fair use / misuse: give the choice back / backlash from forced messaging.
- Cite: Brehm (U); Luguri & Strahilevitz 2021 on backlash.

### `aesthetic-usability` — M
- Source: https://lawsofux.com/aesthetic-usability-effect/
- What: attractive interfaces are judged easier to use.
- In UI: polish on first-use screens.
- In copy: consistent tone.
- Fair use / misuse: polish that matches function / polish that hides poor usability.
- Cite: lawsofux (no evidence grade).

### `cognitive-load` — S (as principle)
- Source: https://doi.org/10.1207/s15516709cog1202_4
- What: working memory is limited; chunk and cut.
- In UI: group fields, one decision per step.
- In copy: short lines, one job per element.
- Fair use / misuse: reduce load / hide needed information.
- Cite: Miller 7±2 is misapplied to UI; do not use it as a rule for menu size.

### `jakobs-law` — S (as heuristic)
- Source: https://lawsofux.com/jakobs-law/
- What: users expect your product to work like others they know.
- In UI: standard patterns for nav, forms, checkout.
- In copy: use the user's vocabulary.
- Fair use / misuse: follow conventions / break them with no gain.
- Cite: heuristic, not an experimental effect.

### `ego-depletion-decision-fatigue` — W, DO NOT CITE
- Source: https://doi.org/10.1177/1745691616652873
- What: the idea that willpower or decision quality depletes.
- In UI: none. Do not use as a reason.
- In copy: none.
- Fair use / misuse: not applicable.
- Cite: Hagger 2016, 23-lab replication, d=0.04.

## Review checks

1. Recommended = default, and default good for user?
2. Price anchored to a real alternative; fees before last step?
3. Progress starts with a real done step; steps/time left?
4. Exactly one distinct primary; decline looks like a real button?
5. Neutral decline copy?
6. Urgency/scarcity backed by live data?
7. Social proof specific/current/verifiable?
8. Options few or filterable, one highlighted?
9. Good ending (success/cancel/error)?
10. Cancel as easy as signup?

## Copy framing rules

- Gain frame for prevention and adoption (Gallagher & Updegraff 2012, small effect r≈.08). Use a loss frame only for real, specific, user-owned losses. Never shame.
  - id: `framing-gain-frame`
  - Source: https://doi.org/10.1007/s12160-011-9308-7
- Precise numbers with source and denominator. Use the frame the user cares about, never the one that hides the real number.
  - id: `framing-precise-numbers`
  - Source: https://doi.org/10.1111/j.1467-9280.2008.02057.x
- Defaults: only when best for most. Label "Recommended for…". Opt-out in one click.
  - id: `framing-defaults-labeled`
  - Source: https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html
- Anchor against real alternatives. Show all fees up front (hidden costs: deceptive.design and FTC).
  - id: `framing-anchor-and-fees`
  - Source: https://www.deceptive.design/types
- Social proof: real, recent, named reference group. Never normalize bad behavior.
  - id: `framing-social-proof-real`
  - Source: https://doi.org/10.1086/586910
- Reduce effort: state time and steps ("2 min, 3 questions"). Use exploratory verbs ("Check availability", +17% at Google I/O 2017, U). Start with a real first step done.
  - id: `framing-reduce-effort`
  - Source: https://business.columbia.edu/sites/default/files-efs/pubfiles/1200/goalgradient.pdf

## Pitfalls

- Contested: choice overload, Zeigarnik memory, ego depletion, decoy with realistic stimuli. Average nudge effect is about 0 after publication-bias correction (Maier 2022).
- Persuasion overuse: mild dark patterns doubled signups, aggressive ones about 4x with backlash (Luguri & Strahilevitz 2021). Regulatory risk. See also persuasion knowledge (Friestad & Wright 1994).
- Dark patterns: Gray 2018 (nagging, obstruction, sneaking, interface interference, forced action); deceptive.design lists 18 types; Mathur 2019 found 1,818 instances; EU DSA Art. 25; FTC 2022 report. The click-to-cancel rule was vacated Jul 2025 (8th Cir.), but ROSCA, FTC Act section 5 and state laws still apply.
- B2B and dev tools: evidence is from consumer samples; expert buyers weaken overload and decoy; urgency and scarcity erode trust. Lean on cognitive load, defaults, progress and endings (judgment).
- Johnson & Goldstein measured registered consent, not donations.
- W items: suggest an A/B test or do not cite.

## Sources

- https://lawsofux.com/cognitive-bias/
- https://growth.design/psychology
- https://growth.design/case-studies/framing-effect
- https://www.deceptive.design/types
- https://www.aeaweb.org/doi/10.1257/jel.20221698
- https://ideas.repec.org/a/cup/bpubpo/v3y2019i02p159-186_00.html
- https://marketing.wharton.upenn.edu/wp-content/uploads/2016/10/The-Limits-of-Attraction.pdf
- https://edoc.unibas.ch/20586
- https://business.columbia.edu/sites/default/files-efs/pubfiles/1200/goalgradient.pdf
- https://arxiv.org/abs/1907.07032v2
- https://academic.oup.com/jla/article/13/1/43/6180579
- https://www.lw.com/en/insights/eighth-circuit-vacates-ftc-click-to-cancel-rule
