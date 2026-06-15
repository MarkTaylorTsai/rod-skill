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
- Baseline: current metric values, expected thresholds, and protected behavior before patching
- Ratchet gate: the comparison rule that decides whether a patch is accepted, rejected, or needs
  review
- Rollback point: git commit, patch backup, full project file snapshot, config version, or other
  reversible state that covers every file or artifact the patch may modify
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
   and failure output. If no baseline exists for an improvement task, create the smallest useful
   baseline before patching.

2. Diagnose
   Identify the most likely failure cause or improvement bottleneck.
   Classify the affected surface and risk.

3. Plan
   Choose the smallest reversible patch that could move the system closer to the Goal. Identify the
   rollback point and the exact comparison rule that will accept or reject the patch.

4. Patch
   Implement one focused change.
   Keep the change explainable and reversible.

5. Verify
   Run the defined tests, evals, checks, builds, benchmarks, or manual verification steps. Capture
   machine-readable results when possible.

6. Compare
   Compare results against the baseline and the Goal Contract. Identify improvement, regression, or
   no meaningful change. Protected metrics must not fall below their threshold or tolerance.

7. Decide
   - If the Goal is satisfied and the ratchet gate passes, stop and report completion evidence.
   - If the patch improved progress, the ratchet gate passes, and the Goal is not satisfied,
     continue with the next smallest patch.
   - If the patch failed or regressed protected behavior, roll back to the rollback point before
     continuing unless the user explicitly asks to keep the broken state for inspection.
   - If no defensible path remains, stop and report the blocker, attempted paths, evidence, and what
     input would unlock progress.


## Baseline and Ratchet Gate Requirements

For repair, optimization, performance, quality, or multi-step improvement tasks, the loop must have a
baseline gate before any non-trivial patch is accepted.

A baseline gate should include:

- baseline command: the command or script that measures the current state
- baseline artifact: a checked-in file, generated report, log, snapshot, or recorded metric set
- protected metrics: values that must not regress, such as test pass count, error count, latency,
  throughput, bundle size, win-rate bounds, safety score, or behavior invariants
- tolerance: explicit allowed drift for noisy metrics, especially timing and benchmark results
- rollback method: git restore, revert commit, patch backup, full project file snapshot, config
  version rollback, or a clearly documented manual rollback path
- rollback coverage: the exact files, directories, configs, generated artifacts, and baseline files
  that can be restored by the rollback method
- promotion rule: when the new result is allowed to replace the baseline

If a task has no existing baseline, create the smallest useful baseline first. Do not claim a Goal
Loop is complete only because checks pass after the patch; compare the result to the baseline and
state whether the ratchet gate accepted it.

If the ratchet gate fails, default to rollback. Keep the failed patch only when rollback is unsafe,
impossible, or the user explicitly asks to inspect the failure.

A baseline-only rollback is not enough for code or configuration patches. If a patch can modify
project files, the rollback point must restore those project files, not only `baseline.json`, reports,
logs, or metric artifacts. A rollback method that restores only the baseline artifact is acceptable
only when the patch itself changes only the baseline artifact.


## Metric Quality Requirements

A ratchet gate must measure more than whether commands exit successfully. For non-trivial work,
define a metric set that is detailed enough to protect the system's actual behavior. Do not rely
only on test count, pass count, pass rate, or a single smoke check.

A strong, portable metric set should include the applicable categories below. If a category is not
applicable, state why in the baseline artifact or summary.

1. Correctness and verification metrics
   Capture tests passed, tests failed, eval cases passed, command status, syntax or type-check status,
   build status, and explicit error counts.

2. Behavior invariant metrics
   Capture domain-neutral invariants that must remain true, such as valid state transitions, resource
   conservation, authorization boundaries, data integrity, id uniqueness, limit enforcement, and
   impossible-state prevention.

3. Deterministic scenario metrics
   Capture at least one representative golden path, edge case, or replayable scenario with fixed
   inputs. Record expected outputs or state summaries, not only that the scenario ran.

4. Interface and integration contract metrics
   Capture public API shape, schema validity, event names, input/output contracts, routing contracts,
   config contract, or artifact presence expected by users or downstream systems.

5. Scope, dependency, and artifact guardrails
   Capture file count, source size, dependency count, lockfile changes, external network or asset
   usage, generated files, and whether changes stayed inside the permitted boundary.

6. Safety, security, privacy, and policy metrics
   Capture secret-scan status, unsafe permission changes, destructive-operation exposure, private data
   handling, access-control invariants, or other protected safety rules relevant to the project.

7. Performance, reliability, and resource metrics
   Capture latency, throughput, memory, bundle size, startup time, benchmark score, retry/error rate,
   or simulation speed when relevant. Noisy metrics require explicit tolerance.

8. Observability and rollback metrics
   Capture baseline artifact path, rollback coverage, rollback drill status, latest report path, and
   promotion status. For new projects or new ratchet tooling, run a rollback drill before declaring
   the gate complete.

Minimum expectation: use at least five applicable metric categories for a new project, and at least
three applicable categories for a small patch. The metric set must include behavior invariants,
deterministic scenarios, rollback coverage, and scope/dependency guardrails unless explicitly
justified.


## Gate Enforcement Requirements

Recording metrics is not enough. Every protected metric must have an explicit gate rule, comparison
operator, expected threshold, actual value, and pass/fail result in the ratchet report. A ratchet
report must not be accepted when any required gate fails, is missing, or cannot be evaluated.

For new projects or new ratchet tooling, these gates are required unless explicitly impossible and
justified:

- evaluation status gate: the evaluation itself must complete successfully
- correctness gate: required tests, evals, checks, or builds must pass
- behavior invariant gate: protected invariants must be true
- deterministic scenario gate: at least one representative fixed-input scenario must match expected
  outputs or state summaries
- interface contract gate: required files, exports, schemas, routes, configs, public contracts, and
  standard tooling entry points must be present and valid
- tooling integrity gate: ratchet tooling files, script targets, evaluator output, snapshot, rollback, and
  baseline promotion behavior must be present, current, executable, and self-consistent
- report consistency gate: accepted/rejected decision, aggregate gate status, failed gate lists, and
  per-gate results must not contradict each other
- scope and dependency gate: changes must stay inside the declared boundary and must not add
  undeclared dependencies, external assets, network calls, or generated artifacts
- safety and policy gate: secrets, sensitive data handling, permissions, destructive operations, and
  policy boundaries must remain clean
- rollback coverage gate: rollback coverage must include every file or artifact the patch may modify
- rollback drill gate: new rollback tooling must be proven with a temporary failure or equivalent
  restore verification before the final report is accepted
- tooling survival gate: after rollback, standard scripts and their target files must still exist and run

Do not mark a ratchet gate as accepted when the evaluation status is `error`, when required metrics
are recorded as false, when rollback coverage or rollback drill is false, when ratchet tooling
integrity fails, or when the ratchet report is internally contradictory. Optional or noisy metrics
may produce warnings, but required gates must block acceptance.


## Standard Tooling Entry Points

For new software projects, ratchet tooling must expose a consistent command surface so humans and
automation can verify the same workflow across domains. Prefer package scripts when the project uses
Node or has a `package.json`; otherwise provide equivalent commands in a `Makefile`, taskfile, or
documented shell scripts.

Required standard entry points for new projects:

- `test`: run deterministic tests or eval cases
- `check`: run syntax, type, lint, smoke, or load checks that are broader than tests alone
- `evaluate`: produce machine-readable metric results without changing the baseline
- `baseline`: create or promote the accepted baseline artifact
- `snapshot`: create a rollback point covering the files and artifacts the next patch may modify
- `ratchet`: compare current evaluation against the baseline, enforce required gates, and rollback on
  required-gate failure when a rollback point exists
- `rollback`: restore the most recent rollback point

The interface contract gate must verify these entry points exist and are runnable. A project may add
extra commands such as `promote`, `drill`, or `report`, but those must not replace the standard names.
If a runtime cannot support these exact script names, the baseline artifact and summary must document
the equivalent command mapping and the ratchet report must mark the mapping as an interface contract.

Do not declare a new project complete if `ratchet` can only be run indirectly through `evaluate` or a
non-standard command. The standard `ratchet` entry point must exist unless explicitly impossible and
justified.




## Ratchet Report Consistency Gate

A ratchet report must be internally consistent. The final accepted/rejected decision must be derived
from required gate results, not written independently.

The report consistency gate must verify:

- `accepted` is true only when every required gate passed
- `accepted` is false when `requiredGatesFailed`, `failed_required`, or equivalent lists are non-empty
- `accepted` is false when `allGatesPassed` or equivalent aggregate is false
- `accepted` is false when evaluation status is error, missing, or unparsable
- `accepted` is false when rollback coverage, rollback drill, tooling integrity, or tooling survival is false
- the final decision, aggregate booleans, failed gate lists, and per-gate results do not contradict each other
- baseline promotion cannot run from a contradictory report

If a report contains both failed required gates and an accepted decision, the report itself is invalid
and the ratchet must reject. Do not repair this by hiding the failed gate; repair the gate or rollback.


## Ratchet Tooling Integrity Gate

Ratchet tooling is Stable Core. A system cannot safely ratchet forward if the gate, baseline, snapshot,
or rollback machinery can disappear, self-corrupt, or be bypassed by a stale script alias.

For new projects and any patch that changes evaluation, rollback, scripts, CI, or tool wiring, add a
required tooling-integrity gate. This gate must verify:

- every standard entry point exists by name
- every standard entry point resolves to an existing file, command, or documented equivalent
- `evaluate` emits machine-readable results and exits non-zero on required-gate failure
- `ratchet` invokes the current evaluation command, enforces required gates, and exits non-zero on rejection
- `snapshot` captures the ratchet tooling files or a known-good restore path for them
- `rollback` restores the ratchet tooling files as well as application files
- `baseline` never promotes an evaluation with required failed gates
- rollback drill proves the tooling still exists and runs after restore
- package scripts, Makefile targets, taskfile targets, or shell entry points do not point to missing files
- snapshots and cleanup logic do not delete the active ratchet tooling directory

The tooling-integrity gate must fail when a script name exists but its target file is missing, when a
script can only run from a stale path, when rollback removes the ratchet tooling, or when a ratchet
report is produced by an older copied evaluator instead of the current evaluator.

For AI systems, tooling-integrity is especially important because evaluation, trace, retrieval,
agent, skill, and loop gates depend on the ratchet toolchain. Do not accept an AI system when the AI
subsystem metrics pass but the ratchet tooling is missing, stale, self-inconsistent, or not covered by
rollback.


## AI System Ratchet Gates

For AI systems, keep all standard gates and add AI-specific protected gates when applicable. The ratchet gate
should prove that AI behavior improved or stayed safe, not merely that code executed. Use deterministic mock
providers for local tests unless live calls are explicitly authorized.

Applicable AI metric categories include:

1. Provider and model contract
   Verify mock provider determinism, real-provider boundary, timeout/retry/fallback behavior, environment-variable-only
   credentials, no key persistence, and no live calls in local gates.

2. Prompt and template quality
   Verify prompt schema, variable validation, missing constraints, output-format hints, unsafe prompt patterns, prompt
   injection resistance, and prompt registry versioning.

3. RAG retrieval quality
   Verify corpus/index integrity, chunk counts, retrieval precision/recall on golden questions, reranking behavior,
   citation coverage, source authorization, unsupported-answer behavior, and retrieval traceability.

4. Graph RAG quality
   Verify entity extraction, relation extraction, graph schema validity, traversal limits, hybrid retrieval fusion,
   graph provenance, and deterministic graph-answer scenarios.

5. Workflow quality
   Verify workflow DAG/state-machine validity, required nodes, transitions, tool-call contracts, idempotency, failure
   paths, retries, and terminal states.

6. Agent and sub-agent safety
   Verify role manifests, spawn limits, recursion/depth limits, budget limits, permission boundaries, handoff contracts,
   merge strategy, and audit trace completeness.

7. Skill creation quality
   Verify skill manifest schema, instruction safety, allowed tool scope, packaging checks, eval fixtures, versioning,
   compatibility, and rollback path for generated skills.

8. Loop control and self-improvement safety
   Verify goal contract, baseline, iteration budget, stop criteria, regression detection, rollback trigger, escalation
   path, and no blind self-modification.

9. Grounding, citation, and answer policy
   Verify citations or provenance when retrieval is used, unsupported-answer refusal, hallucination traps, PII
   redaction, safety policy adherence, and trace IDs.

For a new AI system, at least one required gate should cover each AI subsystem that exists. If the project
contains RAG, graph RAG, workflows, agents, skills, or loops, their contracts must be part of the metric set
and must block acceptance when false. Do not accept an AI system ratchet report when RAG citation coverage,
graph schema validity, workflow terminal-state coverage, sub-agent spawn limits, skill manifest validation, or
loop stop criteria fail.

AI eval datasets should include:

- golden-path cases that should pass
- unsupported or out-of-corpus questions that should refuse or abstain
- adversarial/prompt-injection cases
- privacy/PII cases
- deterministic workflow and agent traces
- regression cases produced by prior failures

Do not store real provider keys in baselines, snapshots, traces, eval results, or docs. Key-like provider
prefixes should be absent from project files unless clearly masked, for example `PROVIDER_API_KEY=***`.


## Loop Requirements

Do not loop blindly.

Each iteration must produce at least one of:

- a code, config, prompt, workflow, policy, test, eval, or documentation patch
- new evidence from a test, eval, benchmark, trace, or review
- a justified decision to stop

Do not continue if:

- the next step would modify Stable Core without required review
- no baseline or rollback point exists for a non-trivial improvement patch
- rollback coverage does not include every project file or artifact that the patch may modify
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
  metric_categories:
  protected_metrics:
  baseline_artifact:
  comparison_result:
  ratchet_gate:
  required_gates:
  standard_entry_points:
  tooling_integrity:
  failed_gates:
  rollback_plan:
  rollback_coverage:
  rollback_trigger:
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
- Baseline:
- Metric categories:
- Protected metrics:
- Verification:
- Comparison:
- Ratchet gate:
- Required gates:
- Standard entry points:
- Tooling integrity:
- Failed gates:
- Completion evidence:
- Rollback:
- Rollback coverage:
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
- accepting a non-trivial patch without a baseline, comparison, and rollback point
- treating a baseline-only backup as rollback coverage for code or config changes
- continuing after repeated verification failures without a new hypothesis
- treating activity as progress
- expanding scope during a Goal Loop without reason
- skipping rollback after a failed patch
- declaring completion without evidence
- declaring completion from post-change checks only, without comparing against baseline
- defining metrics that only count tests without protecting behavior, contracts, scope, and rollback
- recording a failed required metric but still marking the ratchet gate as accepted
- omitting standard entry points such as `ratchet` and relying on a non-standard command instead
- keeping a script alias while deleting or moving its target file
- writing a report that lists failed required gates while also marking the result as accepted
- allowing rollback or snapshot cleanup to delete the active ratchet tooling
- weakening tests, policies, or safety checks to pass
- modifying production state as part of local repair work
- making large rewrites before protecting the baseline

## Default Behavior

When uncertain:

- Prefer evidence over assumption.
- Prefer one focused patch per iteration.
- Prefer rollback over accumulated broken state.
- Prefer creating a small baseline gate before optimizing or improving behavior.
- Prefer full project file snapshots when the project is not yet in git.
- Prefer detailed protected metrics over coarse pass/fail smoke checks.
- Prefer explicit required-gate failures over optimistic acceptance.
- Prefer standard command names over tool-specific aliases.
- Prefer adding a failing test before fixing a bug.
- Prefer completing the user's Goal over broad cleanup.
- Prefer stopping with a clear blocker over blind iteration.
