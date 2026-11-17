# Output formats

## 1. Interview notes

The record the CV is built from. Another writer, or another agent, should be able to build the CV from this file alone.

```markdown
# Interview notes: <Name>
Target role: <role> · Market: <country> · Date: <YYYY-MM-DD>
Sources read: <list, e.g. "old CV (2023), LinkedIn PDF, 'Q3 review' deck">

## <Company> · <Title> · <years>

| Fact | Their words | Source | Confirmed |
|---|---|---|---|
| Grew the support team from 2 to 9 | "it was me and one other, nine when I left" | chat | yes |
| Cut first-reply time from 2 days to 4 hours | – | "H1 review" deck, slide 6 | yes, may be shared |
| Ran the onboarding for new hires | "every new hire went through me for a year" | chat | yes |

Open: <questions they skipped or couldn't answer>
Cut: <things they asked to remove, and why, so nobody adds them back>

## Voice
Words they changed and prefer, e.g. "talked about" (not "presented"), "re-orgs" (not "reorganizations").

## Confidential
Facts they asked to keep off the CV, or to share only with their OK.
```

`Confirmed` is `yes` only when the person said so in this conversation. Facts read from documents start as `no`.

## 2. CV, editable

Plain Markdown or a docs connector, with this order: name and contact line, headline, summary, highlights (optional), experience, training and projects, education, skills. Use standard headings ("Experience", "Education", "Skills"). Dates as years.

```markdown
# <Name>
<City> · <email> · <phone> · <linkedin or site>

## <Target headline>

<Summary, 2–4 lines, no "I".>

## Experience

**<Title>**, <Company> · <YYYY>–<YYYY>
<One line on what the company does, if it isn't well known.>
- <Verb> <what> <for whom or at what scale> <result, if given>
- ...

## Skills
<Concrete tools and methods, written the way they use them.>
```

## 3. CV, file to send

A text-based PDF and a .docx, from the same content.

- If a docx or PDF skill is installed (`docx`, `pdf`), use it and give it the design rules from `cv-rules.md`.
- Otherwise, with `pandoc`: `pandoc cv.md -o cv.docx`, then open the .docx in Word, Pages or Google Docs and export to PDF, or `pandoc cv.md -o cv.pdf --pdf-engine=weasyprint` with a small CSS file (single column, 10.5–11 pt body, 15–20 mm margins, black on white).
- Check the result: text is selectable, nothing sits in a header or footer, it fits in two pages, page one stands on its own.

Name files `<Firstname>-<Lastname>-CV.pdf` and `.docx`.

## 4. Interview practice list

```markdown
# Interview practice: <Name>

## <CV line, quoted>

**Concept checks**
- What is <term>?
  A good answer covers: <2–3 points, from general knowledge, at the level their CV implies>

**Walk me through it**
- <Question about the claim>
  A good answer covers: <their facts from the notes: what, how, their part, the result>
  Missing: <facts the notes don't have; ask them before the interview>

⚠ <Flag if they couldn't answer this well: reword or cut the line.>
```

Order the list as the CV is ordered. Put the five questions they're most likely to get at the top: "Tell me about yourself", "Why are you leaving / why this move?", and the three strongest claims on page one.
