# Observed behaviors on Claude Fable 5.2 and their fixes

Each section starts from a behavior someone has seen, and gives the fix, the text Anthropic suggests, what it did in Anthropic's testing, what it costs, and when to leave it out. The texts in code blocks are quoted from the prompting guide. Treat them as starting points and adapt them to the product.

Add a fix only for a behavior that was observed, one at a time, and measure its effect and its token cost on the user's own tasks. Put new text into new conversations only (see the prefix check note in `SKILL.md`).

## Contents

- A. A turn ends before the work is done
- B. The agent asks for approvals it does not need, or holds routine work
- C. A coding agent copies existing code, or reports problems and leaves them
- D. Long agentic turns look silent
- E. Sessions start more subagents than the task needs
- F. Final reports and handoffs are hard to follow
- G. Requests return `stop_reason: "refusal"`
- H. Easy requests start slowly or cost too much

## A. A turn ends before the work is done

**Behavior.** On long, multistep tasks the model ends the turn by listing what is left, offering to continue, or stopping at an ordinary obstacle such as a timeout. This happens more often at `low` and `medium` effort.

**Fix.** Add text like this to the system prompt:

```text
# Finishing work
Please avoid stopping while you still owe work the user asked for. Be persistent and do not stop unless needed.

While status notes are welcome, as is clarifying with the user on open decisions, carry on with work that does not depend on the user's answer without unnecessary stops.

If you notice yourself inviting the user to redirect you or offering to wait, instead proceed on the next part of the task. You may meet ordinary obstacles like errors, timeouts, locked files, empty results or failing tools. Diagnose them first, and when they are not real blockers, work through them with the access you have (wait and retry, fix the request, use another tool or source) rather than stopping unnecessarily.

If someone clearly decided something is a hard blocker, such as a file marked not to be touched, access that was intentionally withheld, or a safety guardrail, leave it alone, say plainly what you found, and look for another safe way to finish the task. Stopping before the task is complete is very rarely merited, as in when the task can't move forward without user input, or where the blocker is deliberate and should not be worked past. This does not override the need for confirmation on risky or destructive actions.
```

The text separates ordinary obstacles (errors, timeouts, failing tools), which the model should diagnose and work through, from deliberate blockers (a file marked not to be touched), which it should leave alone and report.

**Measured effect.** On recorded sessions from an agentic coding product replayed at `medium`, about half as many sessions ended with unfinished work that could have been continued. The text removed most endings that ask permission or offer to continue. It did not remove endings that list what remains and then stop.

**Cost.** Output tokens rose by about 30 percent.

**Notes.**

- For agentic work at `low` or `medium` effort, Anthropic recommends this text directly, because early stops are more likely there.
- The model asks less often with this text, so the user needs their own confirmation step for risky or irreversible actions.
- When telling the model to keep going, say exactly what is wanted. "Yes, run the migration on the staging database" works where a bare "continue" does not.

## B. The agent asks for approvals it does not need, or holds routine work

**Behavior.** The agent stops to ask permission for routine steps, or holds back ordinary requests to other agents, colleagues, or teams. This is most common when several agents work together and share memory or notes.

**Fix.** This one is solved by removal. There is no text to add. Work through items 7 and 9 of `carried-over-instructions.md`:

- Remove cautions in memory, notes, and instruction files whose reason no longer holds.
- Name the routine steps that need no approval. "Act more freely" is too vague.
- Remove or narrow stopping conditions such as "stop and review at the first error".
- Rewrite absolute rules with their scope: "ask for approval before deleting files" in place of "never delete files".
- Make approval rules name specific actions. A rule that listed "sending messages to people outside this conversation" among the steps needing approval led the model to hold back about half of its routine requests to colleagues and other teams.
- If the system is already stuck, consider restarting it with its memory and notes trimmed.

**Notes.** Keep the user's confirmation step for risky or irreversible actions.

## C. A coding agent copies existing code, or reports problems and leaves them

**Behavior.** The model adds to the existing structure even when that duplicates code, or it notices a problem, reports it, and does not fix it. Fable 5.2 pays close attention to who owns the code. When the prompt says nothing about ownership, or presents the code base as someone else's, it stays inside the existing structure.

**Fix.** If the user wants the model to improve the structure as it works, say that the code is the model's own:

```text
You are the owner and long-term maintainer of this codebase, and its design is up to you.
```

**Measured effect.** On small coding tasks, the model consolidated duplicated code in under 10 percent of runs without the sentence and in about 75 percent of runs with it.

**Cost.** Output tokens rose by about 70 to 80 percent. The model also made changes nobody had asked for, many of them new tests and documentation, and in some runs it changed how an existing feature behaves.

**When to leave it out.** Leave the sentence out where the user owns the code and wants it changed as little as possible. A rule that limits scope does not cancel the sentence: with "No drive-by refactors, renames or cleanups" earlier in the same prompt, the model still consolidated duplicated code in more than half of runs. So this is a choice between two modes, and the user should make it. Ask before adding it.

**Notes.** A closing pull request summary from Fable 5.2 often left out small changes. Tell the user to review the diff as well as the summary.

## D. Long agentic turns look silent

**Behavior.** The user sees little or nothing during a long run of tool calls, or the model makes its first tool call without saying what it is about to do.

Work through these in order. The first one is a client check and costs nothing.

**1. Check that the client receives the updates.** On Fable 5.2, the updates the model writes between tool calls come back as progress-update `thinking` blocks. Their text is empty at the default `thinking.display` of `"omitted"`, so a client that renders only `text` blocks looks silent. Set `display: "updates"` (beta header `thinking-display-updates-2026-08-18`) for a short summary of each update, or `"summarized"` for the updates along with summarized reasoning. Then render the non-empty `thinking` blocks between tool calls.

**2. Add a reminder in the harness.** This works where the platform supports mid-conversation system messages. Count consecutive tool-calling steps that give the user nothing to read: no `text` block and no `thinking` block with text. Count with `display` set to `"updates"` or `"summarized"`, because at `"omitted"` every thinking block is empty. When several pass in a row, append this reminder after the latest tool results as a turn-scoped system message (`clear_at: "next_user_message"`, beta header `mid-conversation-system-clear-at-2026-08-21`):

```text
The user hasn't heard from you in a while: say in a few words what you're doing, then continue.
```

On multi-turn coding tasks, the reminder roughly halved the longest silent stretch without a noticeable increase in tokens or time. Leave each reminder in `messages` on later requests. Removing or rewording one edits an earlier turn, which invalidates the thinking blocks after it.

**3. Ask for an opening line, updates, and a recap.** Add this to the system prompt:

```text
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own (what you found, what you did, and what's next), so a reader who only sees the last message has the full picture.
```

With this text, the model wrote a message before its first tool call in every run of the coding tasks. Output tokens per task rose by roughly 20 percent. Use it where a person is directly in the loop. For more frequent updates, use it together with the reminder.

**4. If the harness cannot add the reminder.** When the reminder is not possible, or the platform has no mid-conversation system messages, add this sentence to the system prompt:

```text
Every few tool calls, give the user a one-line update on where things stand.
```

This sentence cut most long silent stretches on workflow automation tasks.

**When to leave it out.** Frequent updates matter most in interactive settings. For long-running asynchronous work where nobody is watching, the updates cost tokens and help no one. Even with the reminder and the opening-and-recap text together, expect runs of several tool calls between updates.

## E. Sessions start more subagents than the task needs

**Behavior.** The agent delegates more than the tasks need, and subagents are a large share of token use. At `xhigh` and `max`, Fable 5.2 may also start subagents to review its own work, which Fable 5.1 did not do on the same tasks.

**Fix.** In this order:

1. Review the lines in system prompts, skills, and agent files that tell the model to delegate, and remove the ones that are no longer needed (item 1 of `carried-over-instructions.md`).
2. Check which model the subagents use by default, because that sets what each one costs.
3. Only if the model still starts more subagents than the tasks need, rewrite the subagent tool's description. In the new description:
   - State what a subagent adds to the cost of a session.
   - Say when delegation is worth it and when it is not.
   - Tell the model how to brief a subagent that it starts.

If the model still delegates too much, say more about what a subagent costs in this harness, and test the change.

**Measured effect.** At `high` effort, a longer description focused on cost roughly halved the number of subagents compared with a shorter version.

**When to leave it out.** A new description is most useful in a harness that already invites delegation and where subagents are a large share of token use. If the subagent tool has a plain description and nothing else in the prompts asks for delegation, it is likely not needed. Delegation is also not a fault in itself: early testers had good results with Fable 5.2 as the planner and orchestrator for other models, and delegation speeds up work that runs well in parallel.

**Notes.** A tool description is part of `tools`, so the change belongs in new conversations only.

## F. Final reports and handoffs are hard to follow

**Behavior.** After long agentic work, the final report is dense, uses terms the model made up during the work, or assumes the reader saw the tool calls and files behind it.

**Fix.** First remove the hard style rules that are no longer needed (item 6 of `carried-over-instructions.md`), so that old rules and the new text do not conflict. Then add this text to the system prompt and adjust it to the readers and the product:

```text
# Communicating clearly
Write for an intelligent but low-context reader. The person reading has not seen your tool calls, your reasoning or the files you opened, and may be switching in from other work. Messages should generally be self-contained: the reader should understand what you mean without having to dig for other context. Put the key points in the first few sentences. Practice progressive disclosure in your sentence order, and do not use undefined references and ideas in line 1 that won't make sense until the reader reaches line 12.

Use plain words, and write in clear, understandable full sentences. Do not use a term or abbreviation that you made up during the work. Say what the thing is in a way any reader would understand. Write mostly in the style of ASD-STE100 Simplified Technical English: short sentences, one idea per sentence, active voice, and consistently using the same word for the same thing. Use a paragraph of flowing prose where ideas connect, and keep bullets for lists of separate items. Leave out unnecessary details unless the reader asks and practice concision, but do ensure that your messages have the key context. Aim to make your user-facing text as human-readable and clear as possible.
```

**Measured effect.** On agentic tasks, the text made final reports less dense and reduced the number of semicolons. It also shortened sentences on workflow automation tasks.

**Notes.** Depending on the use case, add instructions about length or ask the model to include specific details. Effort has little effect on reply length, so length is a prompt matter.

## G. Requests return `stop_reason: "refusal"`

**Behavior.** A request is declined. The response has `stop_reason: "refusal"`, and `stop_details.category` names the category:

| Category | Meaning |
|---|---|
| `cyber` | The request could enable cyber harm, such as malware or exploit development. |
| `bio` | The request could enable biological harm, such as dangerous lab methods. |
| `frontier_llm` | The request could assist the development of competing AI models. |
| `reasoning_extraction` | The request asks the model to reproduce its internal reasoning in the response text. |
| `general_harms` | The request falls under another usage-policy area. |
| `null` | The refusal does not map to a named category. |

**Fix.** It depends on the category:

- **`reasoning_extraction`:** find and remove instructions in prompts, skills, or tool descriptions that ask the model to write out its reasoning in the response (item 8 of `carried-over-instructions.md`). To see how the model reasoned, set `display: "summarized"` and read the thinking blocks.
- **`cyber` or `bio` on legitimate work:** benign security and life sciences work can trigger these classifiers. Prompt changes are not the answer here. Point the user to Anthropic's [Cyber Verification Program](https://support.claude.com/en/articles/14604842) or [Life Sciences Verification Program](https://www.anthropic.com/news/life-sciences-verification-program). Claude Mythos 5.2 offers the same capabilities to organizations verified through these programs.
- **Any category:** make sure the code checks `stop_reason` before it reads the content, and handles every category. To retry a declined request on another model, see [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback).

**Notes.** Do not try to reword a prompt to get past a classifier. If the work is legitimate, the verification programs are the route.

## H. Easy requests start slowly or cost too much

**Behavior.** Simple requests, even greetings, take a while or cost more than expected.

**Fix.** This is effort, and prompt text will not fix it. At `high` and above the model thinks before almost every reply. Use a lower effort level for those turns. A line such as "answer directly without deliberating" does not stop thinking at `medium` and above, so remove such lines (item 5 of `carried-over-instructions.md`). See Step 3 of `SKILL.md` for the levels and for changing effort inside a conversation.
