---
name: ROD Goal Loop
description: >-
  Use the ROD Goal Loop for user-defined repair, optimization, verification, and improvement
  tasks. The agent must iterate through observable, reversible patches until the Goal Contract
  is satisfied, blocked, unsafe, or out of budget.
---

# ROD Goal Loop — Ratchet-Oriented Goal Execution

## Purpose

Use this skill when the user gives a repair, optimization, improvement, quality, performance,
test-fixing, RAG-improvement, prompt-improvement, workflow-improvement, or "make this pass"
instruction.

The goal is not to make one attempt.
The goal is to iterate safely until the user's completion standard is satisfied or a clear stop
condition is reached.

Core principle:

AI may propose. Fitness must prove. Policy must permit. Release must be reversible. Baseline only
moves forward.

## When to Use

Use for:

- bug fixes
- failing tests
- regression repair
- optimization tasks
- performance improvement
- prompt or AI behavior improvement
- RAG/KAG retrieval improvement
- workflow improvement
- quality improvement
- user instructions such as "keep going until it works", "fix all failures", "make tests pass", or
  "optimize until the metric improves"

Do not use this skill for initial architecture design unless the user has also given a measurable
completion target.
For new systems or structural design, use ROD Architecture.

## Goal Contract

Before starting a long or multi-step task, define or infer a Goal Contract.

A Goal Contract includes:

- Outcome: what must be true when the task is complete
- Verification: tests, evals, commands, artifacts, benchmarks, or review checks that prove
  completion
- Constraints: what must not regress or be changed
- Boundaries: files, modules, tools, environments, data, and permissions that may be used
- Iteration policy: how to choose the next best action after each failed check
- Stop conditions: when to stop because the goal is complete, blocked, unsafe, or out of budget

If the user does not provide a completion standard, infer the smallest reasonable one from the task
and state it briefly before working.

## ROD Goal Loop

Use this loop:

1. Observe
   Inspect the current baseline, relevant files, tests, configs, prompts, workflows, logs, evals,
   and failure output.

2. Diagnose
   Identify the most likely failure cause or improvement bottleneck.
   Classify the affected surface and risk.

3. Plan
   Choose the smallest reversible patch that could move the system closer to the Goal.

4. Patch
   Implement one focused change.
   Keep the change explainable and reversible.

5. Verify
   Run the defined tests, evals, checks, builds, benchmarks, or manual verification steps.

6. Compare
   Compare results against the baseline and the Goal Contract.
   Identify improvement, regression, or no meaningful change.

7. Decide
   - If the Goal is satisfied, stop and report completion evidence.
   - If the patch improved progress but the Goal is not satisfied, continue with the next smallest
     patch.
   - If the patch failed or regressed protected behavior, revert or adjust before continuing.
   - If no defensible path remains, stop and report the blocker, attempted paths, evidence, and what
     input would unlock progress.

## Loop Requirements

Do not loop blindly.

Each iteration must produce at least one of:

- a code, config, prompt, workflow, policy, test, eval, or documentation patch
- new evidence from a test, eval, benchmark, trace, or review
- a justified decision to stop

Do not continue if:

- the next step would modify Stable Core without required review
- verification cannot be run and no acceptable fallback exists
- the task requires credentials, production access, or external approval not available
- repeated iterations are not improving evidence
- the user-defined budget, iteration limit, or safety boundary is reached
- the next step would require unsafe, destructive, or irreversible actions

## ROD Safety Rules

Even inside a Goal Loop:

- Protect Stable Core.
- Prefer small reversible patches.
- Add regression tests for bugs.
- Do not weaken tests to make the goal pass.
- Do not bypass policy, permission, release, or security gates.
- Do not log secrets or sensitive data.
- Do not optimize one target metric while silently damaging protected metrics.
- Do not expand scope without a reason tied to the Goal Contract.

## Patch Shape

Meaningful iterations should be understandable as:

```yaml
patch:
  target_surface:
  target_id:
  current_version:
  proposed_version:
  problem:
  hypothesis:
  change_summary:
  risk_level:
  tests_added:
  fitness_checks:
  rollback_plan:
```

## Output Requirements

Use this format:

```text
ROD Goal Loop Summary:
- Goal:
- Final decision:
- Changed:
- Surface:
- Risk:
- Iterations:
- Verification:
- Completion evidence:
- Rollback:
- Remaining gaps:
```

Final decision must be one of:

- complete
- blocked
- needs_review
- reverted
- unsafe
- budget_reached

Keep the summary short and concrete.
Do not write long process commentary unless the user asked for it.

## Anti-Patterns

Avoid:

- looping without a measurable completion standard
- continuing after repeated verification failures without a new hypothesis
- treating activity as progress
- expanding scope during a Goal Loop without reason
- skipping rollback after a failed patch
- declaring completion without evidence
- weakening tests, policies, or safety checks to pass
- modifying production state as part of local repair work
- making large rewrites before protecting the baseline

## Default Behavior

When uncertain:

- Prefer evidence over assumption.
- Prefer one focused patch per iteration.
- Prefer rollback over accumulated broken state.
- Prefer adding a failing test before fixing a bug.
- Prefer completing the user's Goal over broad cleanup.
- Prefer stopping with a clear blocker over blind iteration.
