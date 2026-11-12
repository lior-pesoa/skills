# Instructions and harness patterns carried over from earlier models

Check every item in the inventory against this list. In Anthropic's testing, these practices raised cost, caused side effects, or stopped having an effect on Claude Fable 5.2.

The search signals are starting points. They find candidates, and you still need to read each hit, because the same idea is worded in many ways. Search case-insensitively across prompt files, instruction files, skills, agent definitions, memory, notes, tool descriptions, and string literals in the harness code.

## Contents

1. Standing instructions to delegate
2. A token budget shown to the model
3. Harness code that edits earlier turns
4. The "treat that answer as done" lines
5. Instructions to think less
6. Hard style rules for writing
7. Cautions that have built up in memory, notes, and rules
8. Instructions to write reasoning into the response
9. Approval rules that are too broad, and bare "continue" messages

## 1. Standing instructions to delegate

**What it looks like.** Lines in system prompts, skills, or agent files that tell the model to use subagents: "always delegate research to a subagent", "use parallel agents liberally", "spawn a reviewer for every change".

**Search signals.** `delegate`, `subagent`, `sub-agent`, `spawn`, `parallel agents`, `use the Task tool`, `use the Agent tool`.

**Why it matters now.** How much Fable 5.2 delegates depends on what the harness and prompts invite. In a product whose prompts invite delegation, it delegates readily, and at `xhigh` and `max` it also starts subagents to review its own work. Subagents can be a large share of what a session costs.

**What to do.** Read these lines before migrating. If the model delegates too much in testing, remove the lines that are no longer needed, and do this before touching the subagent tool's description. Also check which model the subagents use by default. Keep delegation instructions that protect something real, such as parallel work that is measurably faster.

## 2. A token budget shown to the model

**What it looks like.** Harness text that tells the model its token budget for the task and how much is left.

**Search signals.** `token budget`, `tokens remaining`, `tokens left`, `budget:`, `remaining budget`, a countdown injected into prompts or tool results.

**Why it matters now.** The size of the displayed budget changes how much Fable 5.2 spends. On coding tasks at `high` and `xhigh`, removing a large budget lowered cost with equivalent performance.

**What to do.** Test the tasks without the budget text. This finding is about text in the prompt. It is not about the API's task budgets feature (`task_budget` in `output_config`), which the testing did not cover, so leave that alone unless the user asks.

## 3. Harness code that edits earlier turns

**What it looks like.** Code that changes the system prompt, the tool list, or an earlier message between requests: trimming or summarizing old messages in place, rewriting or removing old reminders, a timestamp or other changing value in the system prompt, tools added or removed mid-conversation, an MCP tool list that is not pinned.

**Search signals.** In the code that builds requests: `messages.pop`, `messages.splice`, `messages[i] =`, slicing or filtering the message list, `truncate`, `trim`, `prune`, `summarize`, string formatting inside the system prompt (dates, counters), tool lists built per request.

**Why it matters now.** Fable 5.2 uses preserved thinking, and every thinking block is valid only against the system prompt, tools, and history that came before it. After an edit, the thinking blocks that follow the changed point are invalid. By default the Messages API rejects the request with a 400, and the Message Batches API drops those blocks. Fable 5.2 enforces this for every account, including older accounts that never hit the check on an earlier model.

**What to do.**

- Keep the history append-only. This also keeps the prompt cache hit rate high.
- To shorten the history, use context editing, or compaction that keeps no earlier turns after the summary.
- To change instructions partway through, put them in the newest turn or append a mid-conversation system message.
- As a stopgap, `thinking.block_binding.prefix_mismatch_behavior: "drop_block"` (beta header `thinking-binding-controls-2026-08-01`) makes the Messages API drop the invalid blocks instead of failing. The model then thinks again and uses more output tokens, so measure output tokens before relying on it.

This item overlaps with the API migration. If the `claude-api` skill is installed, its `preserved-thinking-migration` flow finds and measures these edits in an existing harness. Details: [preserved thinking](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking).

## 4. The "treat that answer as done" lines

**What it looks like.** Two sentences that the Claude Opus 5.5 prompting guide offered for chat system prompts. They tell the model to treat an earlier answer as done and to focus its thinking on the new message.

**Search signals.** `as done`, `already answered`, `earlier answer`, `previous answer`, `do not revisit`, `focus your thinking on the new message`, `focus on the latest message`.

**Why it matters now.** At `high` effort these lines reduced Fable 5.2's thinking on follow-up questions, which was their purpose. They also made the model far less likely to point out mistakes in its own earlier answers.

**What to do.** Leave the lines out wherever the user wants the model to keep re-examining earlier answers. Elsewhere, test that the model still points out its own mistakes before keeping them.

## 5. Instructions to think less

**What it looks like.** "Answer directly without deliberating", "do not overthink", "respond immediately", "no need to reason about this".

**Search signals.** `without deliberating`, `answer directly`, `don't think`, `do not think`, `overthink`, `respond immediately`, `no reasoning`, `skip reasoning`.

**Why it matters now.** Fable 5.1 usually followed such a line. On Fable 5.2 it does not stop the model from thinking at `medium` effort and above. A request that relied on the line to fit a small `max_tokens` can now run out of tokens before writing any text.

**What to do.** Remove the lines and lower the effort level for those turns. Where `max_tokens` is small, raise it to leave room for thinking.

## 6. Hard style rules for writing

**What it looks like.** Rigid limits on prose: "one instruction per sentence, in 20 words or fewer", "never use more than three sentences", "no sentence over 15 words", bans on particular punctuation.

**Search signals.** `words or fewer`, `no more than`, `at most`, `maximum of`, `never use`, sentence or word counts near words such as `sentence`, `paragraph`, `response`.

**Why it matters now.** Fable 5.2 follows style rules closely, so a hard limit written to rein in a wordier model can make its prose choppy.

**What to do.** Remove the rules that are no longer needed. Do this before adding the "Communicating clearly" text from `behavior-fixes.md`, or the two will fight each other. Keep rules that reflect a real product constraint, such as a character limit in a user interface.

## 7. Cautions that have built up in memory, notes, and rules

**What it looks like.** Memory files, notes, and instruction files collect cautions over time: "never retry", "always ask before running commands", "stop and review at the first error", "do not touch the config directory". The model may have written some of them itself after one bad session.

**Search signals.** `never`, `always ask`, `do not`, `must not`, `stop and`, `ask before`, `confirm before`, `wait for approval`, `at the first error`. Read memory and notes files in full, because they are usually short and the context around a rule shows whether its reason still holds.

**Why it matters now.** Fable 5.2 follows these instructions closely, and it treats an instruction that contains "never" as absolute. Stacked cautions make it ask for approvals nobody needs and hold routine work. Anthropic saw this mostly when several agents worked together.

**What to do.**

- **Remove notes that are no longer needed.** An old instruction such as "never retry" keeps being followed until someone deletes it.
- **Name the steps that need no approval.** Telling the model to act more freely is too vague. List the routine steps it can take on its own.
- **Check the validation steps.** A condition such as "stop and review at the first error" can block autonomous work. Remove or narrow the stopping conditions that are not needed.
- **Be explicit about exceptions.** Write "ask for approval before deleting files" where the user wants to keep the decision, in place of "never delete files".
- If a system is already stuck, consider restarting it with its memory and notes trimmed.

Whether a caution's reason still holds is often something only the user knows. Ask about the ones you cannot judge from the files. Leave in place the confirmation step for risky or irreversible actions.

## 8. Instructions to write reasoning into the response

**What it looks like.** Prompts, skills, or tool descriptions that ask the model to reproduce its reasoning in the response text: "show your full chain of thought", "output your reasoning in `<thinking>` tags before answering", "include your internal reasoning in the response".

**Search signals.** `chain of thought`, `show your reasoning`, `show your work`, `<thinking>`, `internal reasoning`, `think out loud`, `reasoning in your response`.

**Why it matters now.** Fable 5.2 runs safety classifiers, and one refusal category, `reasoning_extraction`, covers requests that ask the model to reproduce its internal reasoning in the response. Such a request can come back with `stop_reason: "refusal"`.

**What to do.** Remove these instructions. To see how the model reasoned, set `thinking.display` to `"summarized"` and read the thinking blocks. Asking for an explanation of an answer, or for the steps of a solution as part of the answer, is ordinary output and is a different thing from asking for the model's internal reasoning. Use judgment on the borderline cases and flag them for the user.

## 9. Approval rules that are too broad, and bare "continue" messages

**What it looks like.** Two related patterns:

- A system prompt rule that lists broad categories of action as needing approval, such as "sending messages to people outside this conversation".
- Harness code or habits that reply to the model with a bare "continue", "go", or "yes" when it pauses.

**Search signals.** `approval`, `permission`, `confirm`, `before sending`, `outside this conversation`. In the harness: automatic messages whose whole content is `continue`, `go on`, `proceed`, `keep going`.

**Why it matters now.** On simulated tasks with nobody there to approve, the "sending messages to people outside this conversation" rule led the model to hold back about half of its routine requests to colleagues and other teams. And a bare "continue" does not tell the model what was approved.

**What to do.** Rewrite approval rules to name the specific actions the user wants double-checked. When the harness or the user tells the model to keep going, say exactly what is wanted, for example "Yes, run the migration on the staging database".
