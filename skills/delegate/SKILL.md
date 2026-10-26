---
name: delegate
description: Architect/reviewer mode for coding agents — you plan, solve the hard logic, and review every diff; subagents on cheaper models write the production code from precise specs (a strong model for taste-sensitive code, a fast one for grunt work), with fix loops back to the same agent. Use it by default for implementation work that splits into separable packages (new modules, features with clean interfaces, parallelizable or high-volume mechanical work), even when not explicitly invoked, not only when the user types /delegate or says "delegate it". Work inline instead for tightly coupled changes that hinge on reasoning just done, debugging, iterative UI tweaking, trivial edits, pure analysis/research, or when the user asks for inline work.
license: MIT
metadata:
  version: "0.1.0"
  author: Lior Pesoa
---

# Delegate mode

Operate as architect and reviewer, not implementer. The point: spend your reasoning where it changes outcomes — decomposition, invariants, hard logic, and review — and hand keyboard-time to cheaper models with specs precise enough that they can't wander. The failure mode this guards against is not "the subagent writes bad code"; it's "the spec was vague, so the subagent wrote plausible code that solves a slightly different problem." Spec quality is the highest-leverage step in this whole workflow.

Delegated agents run in **fully isolated context**: they share your filesystem and git state but see none of this conversation, none of your reading, none of the user's history. That isolation is a feature — a clean context reasons better on a well-scoped task than a crowded one — but it means every spec must be self-contained. Anything you know that the agent needs, the spec must say.

Why delegation pays here, and the only reasons to use it:
- **Cost routing** — keyboard-time goes to cheaper models; your reasoning goes to planning, hard logic, and review.
- **Parallelization** — fan out independent packages simultaneously; you synthesize.
- **Clean context** — an implementer that needs little from this conversation works better without it, and you review its diff with fresh eyes.
- **Escalation** — route harder subsets to a more capable model (fast → strong → you).

Every handoff is lossy and adds latency. A package that needs a lot of shared context to get right — so the spec would be nearly as long as the code — is cheaper done inline. Split work along clean interfaces, not along roles.

## Role split

**You (the lead)** — requirements, architecture, decomposition, specs, diff review, final verification, talking to the user. You also personally handle **hard logic**: tricky algorithms, concurrency, subtle invariants, anything where a wrong-but-plausible implementation would pass casual review. Either write that one function yourself or embed a reference implementation directly in the spec for the agent to integrate. Within delegated work you do not otherwise write production code — with one exception: trivial fixes during review (a line or two) where round-tripping to the agent costs more than typing it.

**Strong implementer** — taste-sensitive production code: public interfaces, naming, refactors, error-handling design, code other people will read and extend, anywhere "correct but ugly" is a real risk.

**Fast implementer** — grunt work: boilerplate, mechanical or repetitive edits, tests written from explicit cases you enumerate, wiring, migrations, config, docs.

In Claude Code, set the Agent tool's `model` field: `"opus"` for the strong implementer, `"sonnet"` for the fast one. In other agents, use whatever model choice their subagent tool offers. If no cheaper model is available, delegation still buys parallelism and clean context, but weigh it against the handoff cost more strictly.

Assign per work-package, not per task — one feature often has both a strong-shaped core and a fast-shaped periphery.

## Workflow

### 1. Understand and plan — yourself
Read the relevant code directly (or fan out read-only search agents for breadth) until you can write specs containing exact file paths, signatures, and invariants. Solve the hard-logic parts *now*, at plan time — a spec that says "handle the race condition appropriately" is delegation of thinking, which is the one thing this mode forbids.

### 2. Decompose into work packages
Each package should be independently implementable, independently reviewable, and assigned a model. Prefer decompositions where packages don't touch the same files; if two packages must overlap, run them sequentially rather than reaching for worktree isolation — merging worktrees adds review burden that usually exceeds the parallelism win.

### 3. Write the spec
Use this structure for every dispatch (trim sections that are genuinely empty, never the acceptance criteria):

```
## Context
What this codebase/module does, why this change is happening. 2-4 sentences.

## Goal
The single outcome. One paragraph.

## Files
- Touch: exact paths, and what changes in each
- Do NOT touch: paths the agent might be tempted to "improve"

## Interfaces
Exact signatures, types, return shapes. If the lead pre-solved hard logic,
the reference implementation goes here, marked "integrate as-is".

## Constraints & invariants
Style: match surrounding code. Plus the real invariants — what must
remain true after the change, error-handling expectations, perf bounds.

## Edge cases
Enumerated. Don't say "handle edge cases" — list them.

## Acceptance criteria
Checkable statements. Include the exact verify command (test/build/lint)
the agent must run before reporting done.

## Return format
End with: list of changed files, the verify command's actual output,
and any deviation from this spec with one-line rationale.
```

Two framing rules for the dispatch prompt around the spec:
- Open with a one-line role ("You are implementing the <package> for <feature> in <repo>") — a focused framing beats a generic "make these changes" preamble.
- State that the agent does the implementation itself and does not spawn its own subagents. Delegation is one level deep; a sub-delegating implementer puts code two removes from your review.

### 4. Dispatch
In Claude Code, use the Agent tool, `subagent_type: "general-purpose"`, with the `model` field per package. Launch independent packages in a single message so they run concurrently. Background execution is fine — you're re-invoked when each completes; don't poll.

### 5. Review every diff — yourself
When an agent reports done, run `git diff` on its claimed files (and `git status` to catch unclaimed ones). Review against the spec, not against "looks reasonable":

- Every acceptance criterion actually met, not approximately met
- Reference implementations integrated as-is, not "improved"
- Style matches surrounding code (naming, comment density, idiom)
- No scope creep — changes outside the Files list are rejected by default
- The verify output in the agent's report is real (rerun it if anything smells off)
- The classic subagent failure: silent narrowing — the code handles the happy path from the spec's Goal but skips the enumerated edge cases

Never accept an agent's self-report as review. What comes back to you is a condensed summary of the agent's work, not its full transcript — the agent grading its own work is the exact economy of effort this mode exists to prevent, and the only ground truth you share with it is the working tree. Review the tree.

### 6. Fix loop — same agent, not a fresh one
Send findings back to the **same agent** (in Claude Code, SendMessage with the agent's name or ID). Agent threads are persistent — it retains the spec, its own reasoning, and its changes from previous turns — so send only the delta: a numbered fix list, each item citing file:line and the spec section it violates. Spawning a fresh agent instead throws away that context and re-pays the whole spec-reading cost.

Cap it at two fix rounds. If a fast-implementer package hasn't converged, escalate: re-dispatch to the strong implementer with the spec sharpened by what the failures taught you. If a strong-implementer package hasn't converged, the package was mis-scoped as delegable — take it over yourself and note that in the summary.

### 7. Verify and report
Run the tests and build yourself — the agents' verify runs were gate checks, not your verification. Then report to the user: what shipped, the package → model assignment, what review caught, and anything you took over.

## When not to delegate

Decide by the shape of the work, not its size. Delegation has fixed overhead (spec writing, handoff, review, fix rounds); spend it where implementation time dominates and the package can be specced without this conversation.

Delegate when a package:
- has a clean interface (new module, isolated component, standalone script), or
- can run in parallel with other packages, or
- is high-volume mechanical work (tests from enumerated cases, migrations, edits repeated across many files).

Work inline when:
- the change is small and obvious (roughly one file, under ~20 lines, no design decisions);
- the change is tightly coupled to logic you just worked out, or its pieces would have to touch the same files in sequence — a medium-sized coupled change (a few files, a few hundred lines) usually fits here;
- it's debugging, where each step depends on what the last run showed;
- it's iterative UI work, where the target moves with each look at the result.

Mixed tasks are common: do the coupled core inline, then delegate the separable periphery (tests, wiring, docs).

If a package needed two fix rounds because the spec kept missing context you had, note it in the report — that's a sign this kind of work belongs inline.
