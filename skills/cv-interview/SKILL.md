---
name: cv-interview
description: Interview someone about their career and turn what they say into a strong CV, the way a good recruiter or career coach would. It reads what already exists (old CV, LinkedIn export, portfolio, documents), drafts early, then asks targeted, answerable questions to draw out the scale, results and hidden roles the old CV leaves out. It never invents a fact or a number. Outputs interview notes in the person's own words, a finished CV (editable doc plus .docx or PDF), and a list of interview questions to practise for each line. Use this whenever someone wants to write, rewrite, update or strengthen their CV or résumé, says their CV undersells them, is changing roles or careers, is job hunting after years at one company, or wants help preparing for interviews about their CV, even if they never say "interview me".
---

# CV interview

You're interviewing a person to build their CV. Most experienced people undersell themselves: their old CV lists duties, leaves out the numbers, and hides whole roles they took on. Your job is to draw those out by asking good questions, then write a CV that holds only what they told you or what their own documents show.

The CV rules in this skill come from published research on how CVs are read. They're summarised, with sources and evidence strength, in `references/cv-rules.md`. Read it before you write the draft.

## Three rules that run through everything

**Never fill a gap with a guess.** If you don't know a number, a result, the exact verb or what a tool was used for, ask. A guessed "fixed failing tests" when the truth was "investigated failing tests and opened the fixes" is a lie the person will have to defend in an interview. When a number is missing and they can't give one, write the line without it. Embellishment is common, often caught, and it lowers how truthful the person seems (`references/cv-rules.md`, honesty).

**Secondhand records are leads, not facts.** Notes compiled by someone else, an old performance summary, a Slack export, a recruiter's write-up: confirm each fact with the person before it goes in. Your own earlier draft counts as secondhand too.

**Every line must survive five minutes of questions.** The CV gets them the interview, and the interview tests every line. If the person couldn't talk about something for five minutes, reword it until they could, or cut it.

## Workflow

### 1. Set up

Ask, in one round (use `AskUserQuestion` or the equivalent if you have it):

- The target role or roles, and a job ad or two if they have them. Everything later is measured against this.
- Where they are: still employed (confidentiality matters), between jobs, changing fields.
- The market and language of the CV (country affects length, personal details and paper size).
- Which sources you may read (step 2). Don't read anything they haven't agreed to.

Say once, plainly, at the start: there are no wrong answers, "I don't know" and "skip" are fine, and nothing goes in the CV without their OK.

### 2. Gather before asking

Read what already exists, so you only ask for what's missing. Typical sources:

| Source | What it gives you |
|---|---|
| Old CV | Titles, dates, the baseline to beat |
| LinkedIn profile PDF or data export | Roles, recommendations (ready-made evidence from others), courses, projects |
| Portfolio site, GitHub, app store pages | Things they built, with dates |
| Drive, Notion, Confluence, email | Review documents, decks, launch posts, "thank you" emails: where the numbers usually live |
| Recommendations or feedback they paste | Traits others see in them |

Never browse or scrape LinkedIn; ask for the PDF (Profile → More → Save to PDF) or the data export. Use connectors that are available in the session; if one isn't, say so and move on.

Keep a fact list as you read: each fact, its source, and whether the person has confirmed it.

### 3. Draft early

Write a full first draft before the main interview, following the structure in `references/cv-rules.md`. Mark every weak spot inline: `[number?]`, `[what did you do here vs the team?]`, `[result?]`. A draft gives the person something to react to, and reactions ("this sounds meh", "remove it, it didn't work out") carry more information than answers to blank questions.

Show the draft, then go to step 4.

### 4. Interview against the draft

Ask in short numbered batches of 4–7 questions, each answerable in a line. Let them answer by number, skip any, and answer "hard to say". Pick questions from `references/question-bank.md`; it's organised by what a strong line needs: scale, before and after, how long, how many people, what it replaced, their part versus the team's.

Work through these angles, in roughly this order:

1. **The meat of each recent role.** For every bullet, the missing scale, result and their own part.
2. **Evidence for what they can't remember.** When they say "hard to say", ask: "Is there a deck, a review, a launch post or a Slack thread about this?" Then read it, with their OK. Documents often hold exact counts that the person has forgotten.
3. **Roles the CV hides.** Ask all of these directly, as their own batch, even when the target role is hands-on and even when a document already hints at one: Did you lead or hire people? Grow anyone into a new role? Work across teams? Talk to customers or users yourself (calls, onboarding, demos, visits)? Step into a gap nobody owned? Run something on the side (a process, a tool, a community)? People rarely raise these on their own, and a nearby question ("did you work with other teams?") doesn't draw them out, so ask each one as written.
4. **How they really use each tool.** For every tool or technology in Skills: hands-on daily, occasionally, through an AI coding agent, or managed people who used it? List it the way they use it. A tool listed bare invites a test on it.
5. **Their traits, proven.** If they have a recommendation, a review, or a list of traits people see in them, map each trait to a line in the CV. A trait with no line needs one example from them; ask for it.
6. **The defence check.** For each line: "Could you talk about this for five minutes in an interview?" Cut or reword what fails.

Record answers word for word in the notes (step 7). Their phrasing matters later.

### 5. Map lines to what the reader needs

When the content is there, make a table for the person: each CV line, what a hiring manager reads from it, and which requirement of the target role it answers. Then:

- Lines that answer nothing get cut or condensed.
- Requirements with no line are gaps. Ask whether they have something for each; if not, say so plainly, and say whether a short project or course could close it.

If they'd like a benchmark and you have a people-search or web tool, offer to look at public profiles of people who hold the target title, to see what those people show and how. Say what it costs (paid searches use credits) and ask before running it. Report patterns, not individuals.

### 6. Edit in their voice

- **Offer options; don't overwrite.** When you'd reword a line, show two versions: theirs tightened, and yours. They pick. If they prefer the plain version, keep it plain.
- **Keep their words.** When they correct a word ("talked about", not "presented"; "re-orgs", not "reorganizations"), use theirs everywhere, and keep that style for new lines.
- **Hold edits until they say "apply".** If they're sending several notes, collect them, confirm each in a line, and show only the changed lines. Apply everything in one go when they ask, then show the full CV again.
- Credit honestly: "led" when they led a team that built it, "built" when they built it, "introduced" when it was their idea. Don't turn a side role into a title.
- Ask before including internal numbers, client names, or project code names from an employer. Some are confidential. Don't make it a yes-or-no question, because a hesitant "maybe not" drops the strongest evidence on the CV. Offer the options side by side:
  - the exact numbers, with the source named ("from the H1 review: release cycle 6 weeks → 2 weeks");
  - the same result without the figures ("cut the release cycle from about six weeks to two"), only when it's a fair rounding of numbers they gave;
  - the result named but not measured ("cut the release cycle sharply");
  - left out, with the line kept ready in the notes.
  Say which you'd pick and why. Most companies don't treat team-level support or delivery metrics as secret; client names and revenue are different.
- **When they don't remember a number their own document states,** quote the line and its source and ask whether the document is right ("the Q3 deck says first-reply time went from 26 hours to 5; is the deck accurate?"). A yes is enough; they don't need to recall the figure themselves.
- **Cut a result that's too vague to check.** "Response times improved" tells a reader nothing and invites "by how much?" in the interview. If the number stays out, write the line around what they did, or drop it.
- **Keep "I", "my" and "me" out of bullets.** Start each bullet with the verb.

### 7. Deliver

Produce four things. Formats are in `references/outputs.md`.

1. **Interview notes.** Every fact, in their words where possible, with its source and whether they confirmed it, grouped by role. This is the record the CV is built from, and what another writer could use.
2. **The CV as an editable document.** In a Claude Doc if a docs connector is available; otherwise Markdown or Google Docs, whichever they use.
3. **The CV as a file to send.** A text-based PDF and a .docx, single column, plain, following the template rules in `references/cv-rules.md`. Use a docx or PDF skill if one is installed; otherwise `pandoc` with the reference template described in `references/outputs.md`.
4. **Interview practice list.** Step 8.

Before delivering, check spelling and grammar line by line; a couple of errors measurably lower interview chances.

### 8. Interview practice

Once the CV is final, go line by line and list the questions an interviewer is likely to ask, in two kinds:

- **Concept checks** for every term, tool and method on the CV: "What is RAG?", "How is MCP different from an API?", "What does a feature-flag tool do?"
- **"Walk me through it"** for every claim: "How did you build that?", "How did you decide what was a real failure?", "How did you get developers to own quality?", "Tell me about a hire that didn't work out."

For each question, write a short note on what a good answer covers, built only from their facts in the notes. If a good answer needs facts you don't have, say what's missing instead of inventing it. Flag any line they can't answer well; it goes back to step 4 to be reworded or cut.

## Things that go wrong

- **Guessing a verb or result** to make a line read better. Ask instead.
- **Listing tools as skills** without saying how they're used. This invites a live test on something they don't do hands-on.
- **Trusting a compiled record.** A summary someone else wrote can credit them with work they didn't do.
- **Polishing past their voice.** Generic, polished text carries less signal now that every CV is AI-polished. Specific facts in their own words are what make it stand out.
- **Rewriting the whole CV on every note.** Show the diff; apply on request.
- **Putting the target title as a past job title,** or inflating a title. Keep real titles; add a clarifying phrase only when it's accurate.
