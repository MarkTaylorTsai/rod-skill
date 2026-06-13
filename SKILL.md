---
name: ROD
description: >-
  Root entry point for the ROD skill pack. Select ROD Architecture for structural design or
  ROD Goal Loop for measurable repair, optimization, and verification tasks.
---

# ROD — Ratchet-Oriented Development Skill Pack

This root `SKILL.md` is the umbrella entry point for ROD. Use it to select the appropriate
specialized skill, then apply that skill's more specific instructions.

## Skill Selection

Use `skills/rod-architecture/SKILL.md` when creating a new system, making structural changes,
designing AI-enabled software, or refactoring architecture.

Use `skills/rod-goal-loop/SKILL.md` when the user gives a measurable repair, optimization,
verification, quality, performance, or "keep going until this passes" target.

When the task is structural and not an explicit persistent loop, default to ROD Architecture.

## Purpose

Use this root skill to keep AI-assisted software changes observable, testable, reversible, and safe
to improve over time.

ROD Architecture means designing software so future AI-generated changes can be made as small,
observable, testable, reversible patches.

Core principle:

AI may propose. Fitness must prove. Policy must permit. Release must be reversible. Baseline only
moves forward.

## When to Use

Use for:

- new project setup
- architecture design
- structural refactoring
- AI system design
- RAG/KAG system design
- workflow system design
- policy, permission, or release gate design
- prompt/config/workflow registry design
- observability and eval harness design

For persistent repair, optimization, or "keep going until verified" tasks, switch to ROD Goal
Loop instead of treating the architecture path as an optimization loop.

## Architecture Pattern Requirement

Design the system with two explicit layers:

1. Stable Core
   Protect security boundaries, identity, authentication, authorization, permissions, data
   integrity, transactions, tenant boundaries, secrets, audit logs, destructive operations,
   production promotion
   paths, and legal/safety guardrails.
   AI may suggest changes to Stable Core, but those changes require stricter tests, policy checks,
   rollback or recovery planning, and human review.

2. Evolvable Surfaces
   Expose changeable behavior as versioned, observable, testable, and reversible surfaces.
   Examples include prompts, configs, workflows, policies, retrieval settings, reranking rules,
   routing rules, document templates, UI copy, feature flags, evals, tests, and
   non-critical business rules.

For every Evolvable Surface, prefer:

- a clear owner
- a version or baseline
- a file, registry, schema, or declarative definition
- a fitness check
- a rollback or recovery method
- observability signals
- a promotion gate appropriate to risk

Do not hide evolvable behavior inside scattered imperative code unless there is a clear reason.
The default architecture should make future AI-generated patches smaller, safer, easier to evaluate,
and easier to roll back.

For optimization or measurable improvement work, switch to ROD Goal Loop and establish a baseline,
comparison rule, rollback point, rollback coverage, and detailed protected metric set before accepting
behavior changes.

## Non-Negotiable Rules

- Separate Stable Core from Evolvable Surfaces.
- Prefer declarative, versioned surfaces.
- Every evolvable surface needs a fitness check.
- Every meaningful patch must be reversible.
- Baseline gates are required for non-trivial improvement loops.
- Rollback coverage must include the files or artifacts a patch may modify.
- Metric gates must protect behavior, contracts, scope, safety, and rollback evidence, not only test counts.
- Failed cases should be able to become regression tests.
- AI must not bypass gates.
- Do not expose secrets or sensitive data.
- Do not optimize one metric while silently damaging protected metrics.

## Development Pattern

1. Understand project context.
2. Identify baseline.
3. Classify surface and risk.
4. Protect Stable Core.
5. Design Evolvable Surfaces.
6. Define fitness.
7. Add observability.
8. Gate promotion.
9. Document rollback.

## New Project Pattern

For new projects, establish the smallest useful ROD-friendly structure.

Minimum:

- source layout
- test command
- config convention
- logging or observability convention
- rollback-friendly change process
- documented Stable Core
- documented Evolvable Surfaces

For AI projects, also prefer:

- prompt or model config registry
- golden eval dataset
- eval runner
- trace IDs
- citation or grounding policy when retrieval is used
- safety/refusal tests
- protected metric list

## Recommended ROD Artifacts

When useful, use:

```text
/rod
  ratchet.yaml
  ledger.md
  patches/
  fitness/
  evals/
```

These artifacts support Ratchet-Oriented Architecture by making evolvable surfaces, gates,
baselines, and promotion history explicit.

## Output Requirements

Use this format:

```text
ROD Architecture Summary:
- Changed:
- Stable Core protected:
- Evolvable Surfaces:
- Fitness:
- Observability:
- Rollback:
- Remaining gaps:
```

Keep the summary short and concrete.

## Anti-Patterns

Avoid:

- hardcoding prompts, workflows, rules, or thresholds without versioning
- making AI behavior changes without evals
- adding automation without auditability
- changing permissions without allow/deny tests
- introducing irreversible migrations casually
- letting AI directly mutate production state
- treating "looks better" as proof
- hiding behavior in scattered conditionals
- making large rewrites without baseline tests
- logging secrets or sensitive payloads

## Default Behavior

When uncertain:

- Prefer patch over mutation.
- Prefer config over hardcoding.
- Prefer versioned surfaces over hidden behavior.
- Prefer test over assumption.
- Prefer rollback over one-way change.
- Prefer explicit policy over implicit permission logic.
- Prefer observable behavior over silent behavior.
- Prefer small reversible changes over large rewrites.
- Prefer existing project conventions over new parallel systems.
