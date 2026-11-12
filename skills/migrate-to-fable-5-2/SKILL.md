---
name: migrate-to-fable-5-2
description: Migrate prompts, agents, and harnesses to Claude Fable 5.2 or Claude Mythos 5.2, following Anthropic's prompting guide for the model. Audits system prompts, skills, agent files, CLAUDE.md, memory and notes, tool descriptions, and harness code for instructions written for earlier models (Fable 5.1, Opus 5.5, and older), recalibrates effort, and fixes the behaviors that show up after switching - turns that stop early, unneeded approval requests, silent long turns, too many subagents, duplicated code, dense final reports, and refusals. Use this whenever someone is moving to claude-fable-5-2 or claude-mythos-5-2, asks whether their prompts or agent setup are ready for Fable 5.2, or reports that an agent behaves differently, costs more, or got worse after upgrading, even if they never say "migrate". For API code changes (model IDs, breaking parameters), pair it with /claude-api migrate.
---

# Migrate prompts and harnesses to Claude Fable 5.2

This skill walks a project through the behavior side of a move to Claude Fable 5.2: the effort level, the prompt text, and the harness patterns that change how the model acts. Everything here also applies to Claude Mythos 5.2, which is the same model for verified organizations.

The guidance comes from Anthropic's page [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2), captured on 2026-11-12. If you can fetch web pages and something here looks out of date or incomplete, read the live page and prefer it.

## What this skill covers, and what it leaves to others

It covers the things that do not raise an error when they are wrong: an effort level tuned on another model, a system prompt line that no longer works, a memory file full of old cautions, a harness that looks silent. These show up only as cost, latency, or worse results.

It does not cover the API changes that return a 400. Those belong to the [migration guide](https://platform.claude.com/docs/en/models/fable-5-2/migration-guide). If the project calls the Messages API directly, handle them first or alongside this work. When the `claude-api` skill is installed, `/claude-api migrate this project to claude-fable-5-2` does that job. The main items, so you can tell the user what to expect:

- The model ID is `claude-fable-5-2` (on Amazon Bedrock, `global.anthropic.claude-fable-5-2` or `us.anthropic.claude-fable-5-2`).
- The prefix check on thinking blocks is enforced for every account, so code that edits `system`, `tools`, or earlier messages between requests can now fail.
- `computer_20251124` returns a 400 outside Amazon Bedrock. Use `computer_toolset_20260801`.
- A Fable 5.2 executor accepts only a Fable 5.2 or Mythos 5.2 advisor.
- Thinking tokens count toward `max_tokens`, so a small `max_tokens` can end a response before any text.
- Coming from Claude Opus 5.5: 30-day data retention is required, the default effort is `high` where Opus 5.5 used `medium`, and prices and rate limits differ.

## Four ideas that shape the whole migration

**Remove before you add.** Fable 5.2 follows instructions closely. Text written to push an earlier model harder, or to hold it back, now overshoots. Most of the gain in a migration comes from deleting or narrowing old instructions, so do the audit before you add anything.

**Add a fix only for a behavior someone observed.** Every piece of text the guide offers has a measured cost: the finishing text raised output tokens by about 30 percent, the ownership sentence by 70 to 80 percent, the progress-update text by about 20 percent. Adding all of them up front makes the agent slower and more expensive, and hides which change did what. Add one fix per observed behavior, then measure.

**Change instructions in new conversations only.** Because of the prefix check, a stored conversation resumed with a new system prompt or tool description can return a 400. If instructions must change partway through a conversation, put them in the newest turn, or append a mid-conversation system message where the platform supports it. Say this in your report so that nobody deploys the new prompt to live sessions.

**Keep the confirmation step for risky actions.** Several fixes make the model ask less often. That is the goal for routine work, and it makes the user's own confirmation step for destructive or irreversible actions more important. Do not remove such a step as part of this cleanup.

## Workflow

### Step 1: Learn the situation

Look before you ask. The repository usually tells you where the prompts live, which model ID the code names today, what effort it sets, and whether there are evals. Read enough to answer what you can.

Then ask the user for what only they know. If a structured question tool is available (`AskUserQuestion` in Claude Code), use it and put the questions in one round. Otherwise ask in plain text. Skip any question the request or the repository already answered.

| Question | Why it changes the work |
|---|---|
| Which model are you moving from? | Prompts tuned for Claude Opus 5.5 carry different leftovers from prompts tuned for Claude Fable 5.1, and an unset `effort` meant `medium` on Opus 5.5. |
| Which files or directories are in scope? | Prompt text hides in many places. Editing outside the agreed scope surprises people. |
| Is a person watching the agent work, or does it run unattended? | Progress updates matter for interactive use and cost tokens for nothing on unattended runs. |
| Have you run it on Fable 5.2 yet? If so, what did you see? | The fixes in Step 5 are chosen by observed behavior. Offer the symptom list from `references/behavior-fixes.md` as choices, and allow more than one. |
| For coding agents: should the model restructure code it touches, or change as little as possible? | This decides whether the ownership sentence helps or harms. |
| Do you have evals or recorded sessions to measure against? | Without them you can propose changes, but nobody can confirm an effort level or a fix. |
| Should I apply the edits, or report and propose a diff? | Removing someone's instructions is their call. Default to proposing when they have not said. |

Ask follow-up questions later when a finding needs a decision, for example whether the reason behind an old caution still holds. One clear question beats a wrong guess, and a short batch beats a stream of interruptions.

If the user works through a product that manages the harness for them (Claude Code, claude.ai, Claude Managed Agents), the request-level items (effort parameter, `thinking.display`, reminders, history edits) are the product's job. Focus on the files they do control: instruction files, skills, agent definitions, memory, and notes.

### Step 2: Take inventory

List every place that carries instructions into the model's context. People forget most of these, so search for them:

- System prompts, in prompt files and in string literals in the code.
- Instruction files such as `CLAUDE.md` and `AGENTS.md`, rule files, skills, slash commands, and agent or subagent definitions.
- Memory files, notes, and scratchpads that agents read back, including ones the model wrote.
- Tool definitions and their descriptions, above all the tool that starts subagents.
- Harness code: where requests are built (`effort`, `thinking`, `max_tokens`), anything that rewrites `system`, `tools`, or earlier messages, text injected into prompts at run time (budgets, reminders, automatic "continue" messages), and approval rules.

Keep the list. It becomes the scope line of your report.

### Step 3: Calibrate effort

Effort sets how much the model thinks, how many tool calls it makes, how long a turn takes, and how many tokens it uses. Levels rank the same way across models, but the amount of thinking at each level differs, so a setting tuned on another model does not carry over.

1. Set `effort` to `high` explicitly. It is the default for Fable 5.2 on the Claude API, and stating it removes the surprise for anyone coming from a model with a different default.
2. Run the user's evals at `medium` and `xhigh` as well, and move down to `medium` wherever the results hold. Most of the capability gain arrives at `high`. Above `high`, gains are uneven and depend on the task.
3. If there are no evals, say so in the report and list the sweep as open work. Do not present an effort level as tuned when nothing measured it.

| Level | Suits |
|---|---|
| `low` | Quick back-and-forth, well-specified tasks, high-volume work such as fast subagents. Fable 5.2 at `low` scored close to Fable 5.1 at higher effort on coding evaluations. |
| `medium` | Interactive coding, chat, everyday knowledge work. |
| `high` | Hard coding, research, agentic work, long unattended runs. Turns take noticeably longer than at `medium`. |
| `xhigh` | The hardest long-running coding and agentic work, where a gain was measured. A slight score gain for many more tokens. |
| `max` | Measuring the ceiling, or open-ended problems such as mathematics and scientific discovery, where time and tokens do not matter. |

Things about effort that are easy to miss:

- At `high` and above the model thinks before almost every reply, even a greeting. If simple requests are slow or costly, lower the effort for those turns. A prompt line such as "answer directly" does not stop thinking at `medium` and above.
- Effort has little effect on reply length. Use prompt text to change length and tone.
- Agentic work at `low` or `medium` is more likely to stop early. For that combination, add the finishing text from `references/behavior-fixes.md` (section A).
- A workflow can mix levels, for example planning at `medium` and raising effort for the long unattended part. Per-message effort (beta header `mid-conversation-output-config-2026-07-01`) changes the level inside a conversation and keeps the prompt cache. Where it is not available, a new top-level `effort` value works and starts the cache over.

### Step 4: Audit what the project carries over

Read `references/carried-over-instructions.md` and check every item from your inventory against it. It lists each kind of leftover, how to find it, why it misbehaves on Fable 5.2, and what to do. The kinds are: standing instructions to delegate, a token budget shown to the model, harness code that edits earlier turns, the "treat that answer as done" lines, instructions to think less, hard style rules for writing, cautions that have built up in memory and notes, instructions to write reasoning into the response, and approval rules that are too broad.

Record each finding with its file and line, the text, why it is a problem now, and what you propose. Some findings are clear removals. Others depend on whether an old reason still holds, and only the user knows that. Ask about those rather than deleting on a guess.

### Step 5: Match observed behaviors to fixes

Read `references/behavior-fixes.md`. For each behavior the user has observed on Fable 5.2, it gives the fix, the exact text Anthropic suggests, the measured effect, the token cost, and the cases where the fix should be left out.

If the user has not run on Fable 5.2 yet, do not add fixes on speculation. Finish Steps 3 and 4, then give them the observation checklist: run the longest agentic tasks and note where the model stops early, asks for approvals it does not need, goes quiet, delegates more than the task needs, or adds to existing code where restructuring was wanted. They can come back with what they saw.

Treat the suggested texts as starting points. Adapt them to the product and its readers, and keep the meaning.

### Step 6: Apply the changes

Apply what the user approved, one change at a time where measurement is possible, so that each effect and its token cost can be seen on its own. When editing:

- Rewrite an absolute rule with its scope and its reason, because the model treats "never" as absolute. "Ask for approval before deleting files" keeps the user in control. "Never delete files" blocks the action entirely.
- Tell the model which routine steps need no approval by naming them. "Act more freely" is too vague to change anything.
- Leave the user's confirmation step for risky or irreversible actions in place.

### Step 7: Report

Write the report for a reader who has not seen your tool calls or the files you opened. Put the main points first and use plain, full sentences. Use this structure:

```markdown
# Fable 5.2 migration report: <project>

## Summary
<Three to five sentences: what was reviewed, the most important changes, what still needs measuring.>

## Scope
<Files and directories reviewed, the model migrated from, and how the agent is used.>

## Effort
<Current setting, recommended setting, and whether an eval sweep confirmed it.>

## Instructions removed or rewritten
| Location | Text | Why it is a problem on Fable 5.2 | Change (applied or proposed) |

## Text added for observed behaviors
<For each: the behavior, the text, where it went, the expected effect, the expected token cost.>

## Left unchanged, and why
<Findings that need the user's decision, and fixes not added because the behavior was not observed.>

## What to measure next
<The effort sweep, the observation checklist, and one measurement per added fix.>

## Rollout notes
<Deploy prompt and tool-description changes to new conversations only. List any API changes still open from the migration guide.>
```
