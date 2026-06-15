---
name: ROD Architecture
description: >-
  Apply Ratchet-Oriented Architecture when creating new systems or making structural software
  changes. Use this skill to separate Stable Core from Evolvable Surfaces and make software
  observable, versioned, testable, reversible, and safe for AI-assisted evolution.
---

# ROD Architecture — Ratchet-Oriented Architecture

## Purpose

Use this skill when creating a new system, making structural changes, designing AI-enabled software,
or refactoring architecture.

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

Do not use this skill as a persistent optimization loop.
For user-defined repair, optimization, or "keep going until verified" tasks, use ROD Goal Loop.

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
- Required gates must block acceptance when protected metrics fail or cannot be evaluated.
- New projects should expose standard test/check/evaluate/baseline/snapshot/ratchet/rollback entry points.
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


## AI System Architecture Pattern

When designing AI systems, keep the general ROD architecture rules and add explicit AI-specific surfaces and
gates. The goal is not to hardcode one AI stack, but to make AI behavior observable, versioned, testable,
reversible, and safe across RAG, graph RAG, agentic workflows, skills, and loops.

Treat these as Stable Core unless intentionally isolated behind a safe evolvable surface:

- identity, tenant, authorization, permission, and tool-execution boundaries
- secret handling and provider credentials
- data-ingestion trust boundaries and document access policy
- retrieval authorization and source visibility rules
- tool allowlists, destructive action guards, and human-approval gates
- sub-agent spawn limits, budget limits, recursion limits, and loop-stop conditions
- audit logs, trace IDs, provenance, citations, and evaluation history
- baseline, snapshot, rollback, and promotion logic
- PII handling, redaction, retention, and privacy policy

Prefer these as Evolvable Surfaces, each with schema, owner, version, evals, traces, and rollback:

- prompts, prompt templates, system messages, and prompt routing rules
- model/provider configuration, temperature, max tokens, retry policy, and fallback policy
- chunking, embedding, retrieval, reranking, and citation policy for RAG
- entity extraction, relation extraction, graph schema, graph traversal, and hybrid retrieval policy
- workflow graphs, node configs, transition rules, tool-call plans, and guardrail policies
- agent role definitions, sub-agent manifests, spawn policy, handoff contracts, and merge policies
- skill manifests, skill instructions, tool contracts, eval fixtures, and packaging checks
- loop goals, iteration budgets, stop criteria, self-critique prompts, and escalation rules
- evaluator rubrics, golden datasets, adversarial datasets, and regression fixtures
- memory policy, summarization policy, context-packing policy, and cache policy

Recommended AI project layout when applicable:

```text
/ai
  providers/          # provider adapters and deterministic mocks
  prompts/            # versioned prompt templates and routing
  retrieval/          # RAG configs, chunking, indexing, reranking
  graph/              # graph schema, extraction rules, traversal configs
  workflows/          # workflow DAGs or state machines
  agents/             # agent roles, sub-agent spawn policy, handoff contracts
  skills/             # generated or project-local skills with manifests and evals
  evals/              # golden/adversarial datasets and scoring rubrics
  traces/             # sample traces or trace schema, not private data
  policies/           # safety, tool, privacy, citation, and escalation policies
/rod
  ratchet.yaml
  fitness/
  snapshots/
```

For AI systems, document these contracts before accepting the architecture:

- provider contract: mock provider, real provider boundary, timeout, retry, fallback, and no-secret rule
- grounding contract: source selection, citation format, unsupported-answer behavior, and retrieval auth
- workflow contract: states, transitions, tool calls, outputs, failure handling, and idempotency
- agent contract: roles, permissions, spawn limits, message schema, termination, and merge strategy
- skill contract: manifest schema, allowed tools, eval fixtures, versioning, and rollback path
- loop contract: goal, baseline, iteration budget, stop rules, regression gates, and escalation

AI system fitness should include deterministic offline evals using mock providers. Live provider calls may be
optional integration checks, but they must not be required for the local ratchet gate unless secrets and
network side effects are explicitly authorized by the user.


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
