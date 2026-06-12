---
name: ROD
description: Use Ratchet-Oriented Development for meaningful software work in new or existing projects, especially AI systems, RAG/KAG, prompts, workflows, configs, policies, release gates, migrations, refactors, and behavior-changing code. Use lightweight mode for tiny low-risk edits.
---

# ROD — Ratchet-Oriented Development

## Purpose

Use this skill as a development pattern for both new projects and existing projects.

ROD means building and modifying software so the system can safely improve over time without hidden regressions.

Core principle:

AI may propose. Fitness must prove. Policy must permit. Release must be reversible. Baseline only moves forward.

Do not only implement the requested change. Also leave the project in a state where future changes can be made as smaller, more observable, more testable, and more reversible patches.

ROD is not about overengineering. It is about making meaningful changes safe to evaluate, promote, and roll back.

## When to Use

Use ROD for meaningful development work, including:

- new project setup
- feature development
- bug fixes
- refactoring
- AI behavior changes
- prompt changes
- RAG, KAG, retrieval, reranking, or embedding changes
- workflow or routing changes
- policy, permission, security, or release gate changes
- database schema or migration changes
- infra, deployment, observability, or CI changes
- evaluation, benchmark, or test harness changes

Use Lightweight Mode for tiny low-risk changes such as:

- typo fixes
- comments
- formatting
- small UI copy changes
- documentation-only edits
- test name cleanup

Even in Lightweight Mode, keep rollback and verification clear.

## Operating Modes

### Lightweight Mode

Use for small, low-risk edits.

Minimum requirements:

- Identify the changed surface.
- State the risk level.
- Add or run the closest practical check.
- State rollback method.
- Do not create new ROD artifacts unless useful.

### Standard Mode

Use for normal feature work, bug fixes, refactors, config changes, prompts, workflows, evals, RAG/KAG changes, or any behavior-changing patch.

Minimum requirements:

- Identify baseline.
- Classify the changed surface.
- Define fitness checks.
- Implement as a small patch.
- Add or update tests/evals when practical.
- Record rollback method.
- Summarize remaining gaps.

### Strict Mode

Use for high-risk areas.

High-risk areas include:

- authentication
- authorization
- permissions
- data deletion
- secrets
- payments
- production deployment
- database migrations
- legal, medical, financial, or safety-critical outputs
- privacy, PII, confidentiality, or privileged data
- security boundaries
- audit logs
- release gates
- policy enforcement
- live production state

Strict Mode requirements:

- Do not make destructive, irreversible, or production-affecting changes without explicit approval.
- Prefer fail-closed behavior.
- Add allow and deny tests for policy/security changes.
- Add rollback or recovery plan.
- Preserve auditability.
- Do not weaken gates to make tests pass.
- Separate proposal, evaluation, review, and promotion.

## Non-Negotiable Rules

1. Never make opaque changes.
   Every meaningful change must be explainable as a patch against a known baseline.
2. Separate Stable Core from Evolvable Surfaces.
   Stable Core includes:
   - identity
   - authentication
   - authorization
   - permission checks
   - data integrity
   - transactions
   - secrets handling
   - audit logs
   - deletion logic
   - production promotion
   - legal/safety guardrails
   Evolvable Surfaces include:
   - prompts
   - configs
   - workflows
   - routing rules
   - retrieval settings
   - reranking settings
   - chunking policy
   - KAG schemas
   - output schemas
   - UI copy
   - evals
   - tests
   - non-critical business rules
   - feature flags
   - policy thresholds
3. Prefer declarative, versioned surfaces.
   When practical, put changeable behavior into versioned files, registries, schemas, or config objects instead of burying it in hardcoded logic.
4. Every evolvable surface needs a fitness check.
   A surface is not ROD-ready unless there is a way to judge whether a change made it better, worse, unsafe, or merely different.
5. Every meaningful patch must be reversible.
   Do not introduce a meaningful change unless rollback is clear.
6. Failed cases become regression tests.
   When fixing a bug, bad AI behavior, missed retrieval, wrong workflow route, policy failure, or unsafe output, add or update a test/eval that prevents the same failure from silently returning.
7. AI must not bypass gates.
   AI may generate code, configs, prompts, tests, evals, migrations, reports, and patch proposals. Production promotion must go through tests, policy, review, release gates, or approval appropriate to risk.
8. Do not expose secrets or sensitive data.
   Do not read, print, copy, commit, or log secrets, tokens, API keys, private keys, credentials, seed phrases, production data, private user data, or sensitive payloads unless explicitly required, safe, and approved.
9. Do not optimize one metric while silently damaging protected metrics.
   Protected metrics may include correctness, safety, latency, cost, recall, grounding, permission behavior, privacy, and user trust.
10. Do not replace gates with vibes.
   “Looks better” is not proof. Meaningful AI/system behavior changes need tests, evals, traces, or review evidence.

## Development Pattern

Follow this sequence when starting or modifying a system.

### 1. Understand the Project Context

For existing projects, first inspect the project conventions.

Look for:

- README
- AGENTS.md
- CONTRIBUTING
- Makefile
- package scripts
- CI workflows
- test folders
- eval folders
- schema folders
- config folders
- docs or runbooks
- existing release gates
- existing observability or audit conventions

Do not fight existing structure without reason. Extend the project’s current pattern when it is safe and adequate.

For new projects, establish the smallest useful conventions early:

- clear source layout
- test command
- config convention
- logging/observability convention
- rollback-friendly deployment or change process
- documented critical surfaces

### 2. Identify the Baseline

Determine what currently exists before changing it.

Record or infer:

- current behavior
- current files, configs, prompts, workflows, schemas, or routes involved
- current tests or evals
- current known risks
- current version or rollback point
- current owner or gate, if any

If no explicit baseline exists, create the smallest useful baseline.

Examples:

- Add a test that captures current behavior.
- Snapshot current config.
- Record current eval score.
- Document current workflow shape.
- Save current schema version.
- Add a fixture representing the failing case.

### 3. Classify the Surface

Classify the target surface.

Common surface types:

- code
- config
- prompt
- rag_config
- kag_schema
- retrieval_index
- workflow
- router
- policy
- permission
- database_schema
- migration
- infra
- ui
- test
- eval
- documentation
- observability
- release_gate

Classify risk:

- low: safe copy, docs, tests, formatting, small UI, non-behavioral cleanup
- medium: business logic, prompts, retrieval config, workflow, routing, non-critical automation
- high: auth, permissions, data deletion, secrets, production state, migrations, legal/medical/financial outputs, safety, privacy, release gates

Use stricter gates for higher risk.

### 4. Protect the Stable Core

Before changing behavior, ask whether the change touches Stable Core.

If yes:

- prefer small changes
- preserve existing security boundaries
- add explicit allow and deny tests
- avoid broad refactors
- keep audit trails intact
- document failure behavior
- prefer fail-closed over fail-open
- do not weaken validations or gates just to make a feature work

Stable Core should not be made “more flexible” unless there is a clear policy reason and a testable safety boundary.

### 5. Design Evolvable Surfaces

Prefer these transformations when useful:

- hardcoded prompt → prompt file or prompt registry
- hidden threshold → versioned config
- implicit workflow → workflow definition
- scattered permissions → centralized policy or policy-as-code
- unmeasured behavior → metric, log, trace, test, or eval
- one-way migration → reversible migration or recovery plan
- manual-only quality check → automated fitness check
- production-only behavior → testable local/staging path
- untracked AI behavior → eval case and prompt/config version

Do not overengineer.

Use the smallest structure that makes the change observable, testable, reversible, and understandable.

### 6. Define Fitness

Before or while implementing, define how the patch will be judged.

Use relevant fitness checks.

Correctness:

- unit tests
- integration tests
- contract tests
- schema tests
- golden tests
- regression tests

AI quality:

- answer correctness
- citation grounding
- retrieval recall
- context relevance
- hallucination rate
- prompt compliance
- refusal correctness
- eval pass rate
- judge agreement
- unsupported claim rate

RAG/KAG quality:

- Recall@K
- MRR
- NDCG
- source authority ranking
- citation support
- freshness
- jurisdiction match
- graph relation coverage
- retrieval latency
- reranker cost
- degraded-path behavior

Workflow quality:

- workflow completion rate
- blocked step rate
- missing input detection
- manual intervention count
- rework rate
- artifact schema validity
- approval correctness

System quality:

- latency
- P95 latency
- error rate
- cost
- memory usage
- timeout behavior
- retry behavior
- security scan
- permission checks
- audit coverage

Data quality:

- schema validity
- null rate
- duplication
- freshness
- lineage
- retention compliance
- deletion propagation
- PII handling

A patch may pass only when:

- hard constraints pass
- protected metrics do not regress beyond tolerance
- at least one target metric improves, or the requested bug is fixed
- rollback is available
- risk-appropriate review is satisfied

### 7. Implement as a Patch

For meaningful changes, make the implementation understandable in this shape:

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

This does not always need to be a literal file. The final implementation and summary must still be understandable in this form.

Prefer small patches over large rewrites.

If a large rewrite seems necessary, split it into ratchetable steps:

```text
step 1: add tests around current behavior
step 2: extract interface or config
step 3: add new implementation behind flag
step 4: compare old and new behavior
step 5: promote after gate passes
step 6: remove old path only after rollback window
```

### 8. Add or Update Tests

Every meaningful change should include the closest practical test.

Minimum expectations:

- bug fix → regression test
- new feature → behavior test
- prompt change → eval case
- RAG change → retrieval or answer eval
- KAG change → graph consistency or retrieval eval
- workflow change → scenario test
- policy change → allow and deny tests
- permission change → positive and negative authorization tests
- migration change → migration and rollback/recovery check
- infra change → plan, validate, smoke, or health check
- observability change → emitted event/span/log shape test when practical

If no automated test is practical, state the manual verification clearly and explain why automation was not practical.

Do not remove or weaken tests unless the baseline was wrong and the replacement is stricter or more accurate.

### 9. Add Observability

For behavior that may need future improvement, add useful signals.

Prefer structured events such as:

- operation_started
- operation_completed
- operation_failed
- validation_failed
- policy_denied
- retrieval_performed
- retrieval_degraded
- reranker_fallback
- citation_gate_failed
- workflow_step_started
- workflow_step_blocked
- workflow_step_completed
- ai_response_generated
- user_correction_received
- eval_case_created
- patch_evaluated
- patch_promoted
- patch_rejected
- rollback_performed

Logs, metrics, traces, and audit events should help answer:

- What happened?
- Which version, config, prompt, workflow, policy, or model was active?
- Why did it fail?
- Was the failure expected, degraded, or unsafe?
- Which input or case caused it?
- Can this become a future test?
- What rollback point exists?

Do not log secrets, private data, tokens, credentials, raw sensitive payloads, or unnecessary user content.

When sensitive observability is required, prefer:

- redaction
- hashing
- stable IDs
- summary tags
- counts
- metadata
- allowlisted fields
- access-controlled audit storage

### 10. Gate Promotion

Separate implementation from promotion.

A patch can be:

- draft
- evaluated
- rejected
- needs_review
- approved
- promoted
- rolled_back

Promotion rules by risk:

Low risk:

- tests or validation pass
- rollback is clear
- human review optional

Medium risk:

- tests/evals pass
- protected metrics do not regress
- rollback is clear
- human review recommended or required by project policy

High risk:

- tests/evals pass
- security/policy checks pass
- audit behavior is preserved
- rollback or recovery is documented
- human review required
- production promotion must be explicit

Do not directly mutate production state as part of normal development unless the user explicitly requested it and risk is understood.

## New Project Pattern

When starting a new project, establish ROD-friendly structure without overbuilding.

Minimum recommended setup:

```text
/src
/tests
/docs
README.md
```

If the project has meaningful AI behavior, workflows, policies, or configs, also consider:

```text
/evals
/fixtures
/config
/schemas
/rod
```

Only add what is useful.

For a new project, define:

- how to run tests
- where configs live
- where schemas live
- how prompts or AI behavior are versioned, if applicable
- how failures become tests
- what is Stable Core
- what is safe to evolve
- how rollback works

For a new AI project, prefer adding from the start:

- prompt/version registry
- small golden dataset
- eval runner
- trace IDs
- citation/grounding policy, if retrieval is used
- safety and refusal tests
- protected metric list

## Existing Project Pattern

When modifying an existing project:

1. Respect existing conventions.
2. Find current tests/evals before adding new tools.
3. Prefer extending existing gates over inventing parallel gates.
4. Keep patches small.
5. Avoid broad rewrites unless the baseline is protected by tests.
6. Do not move critical files without need.
7. Do not change public contracts silently.
8. Do not change production config directly.
9. Add regression coverage near the failing behavior.
10. Summarize remaining non-ROD-ready areas.

If the project already has CI, evals, release gates, or observability, integrate with them.

If the project lacks them, add the smallest missing piece.

## Recommended ROD Artifacts

When a project has no existing convention and the change is meaningful, use this minimal structure:

```text
/rod
  ratchet.yaml
  ledger.md
  patches/
  fitness/
  evals/
```

Use only what is needed.

### ratchet.yaml

Defines evolvable surfaces and gates.

```yaml
system:
  id:
  owner:
surfaces:
  - id:
    type:
    path:
    risk_level:
    owner:
    versioned: true
    rollback: true
fitness:
  - id:
    surface_id:
    command:
    required: true
release_policy:
  low:
    requires_tests: true
    requires_human_review: false
  medium:
    requires_tests: true
    requires_human_review: true
  high:
    requires_tests: true
    requires_human_review: true
    requires_security_review: true
```

### ledger.md

Append important accepted or rejected changes.

```markdown
## PATCH_ID

- Target:
- Baseline:
- Change:
- Tests:
- Result:
- Rollback:
- Decision:
- Lesson:
```

Do not create ledger noise for tiny low-risk edits.

## AI System Guidance

For AI systems, prefer treating prompts, retrieval settings, workflow definitions, eval datasets, and safety policies as evolvable surfaces.

Useful AI surfaces:

- prompt templates
- model config
- tool routing
- workflow definitions
- output schemas
- retrieval config
- chunking policy
- embedding model
- reranker config
- citation policy
- grounding policy
- refusal policy
- escalation policy
- evaluation datasets
- judge prompts
- safety thresholds

AI changes should usually include:

- version identifier
- eval case or golden example
- before/after comparison
- protected metrics
- failure examples
- rollback path

AI must not silently self-modify production behavior.

## RAG and KAG Guidance

For RAG/KAG systems, classify these as evolvable surfaces:

- collection names
- payload schema
- chunk size
- chunk overlap
- embedding model
- top_k
- score threshold
- hybrid search settings
- dense/sparse weights
- reranker model
- rerank_top_n
- citation policy
- jurisdiction filter
- freshness boost
- authority boost
- KAG entity types
- KAG relation types
- graph traversal depth
- fallback behavior

RAG/KAG patches should include relevant checks such as:

- retrieval recall
- source precision
- citation grounding
- jurisdiction match
- authority freshness
- latency
- cost
- degraded-path behavior
- hallucination or unsupported claim rate

For legal systems, do not promote retrieval changes that improve general relevance while damaging authority correctness, jurisdiction correctness, or citation support.

## Workflow Guidance

For workflow systems, treat workflow definitions as versioned surfaces.

A workflow should ideally define:

- workflow_id
- version
- required inputs
- steps
- roles
- output schema
- write targets
- validation rules
- approval rules
- failure handlers
- degrade policy
- metrics

Workflow patches should include scenario tests.

Examples:

- missing required input should block or ask a clarification
- incomplete evidence should produce a gap report
- draft workflow should mark draft status
- external action should not be claimed unless actually executed
- approval-required step should not be skipped

## Policy and Permission Guidance

For policy, permission, safety, privacy, or compliance changes:

- use Strict Mode
- add allow and deny tests
- keep policy centralized when practical
- preserve audit logs
- prefer explicit policy over hidden conditional logic
- fail closed when uncertain
- do not loosen a policy without documenting why
- do not bypass policy in tests unless testing the bypass guard itself

Policy changes require especially clear rollback.

## Database and Migration Guidance

For database changes:

- identify current schema baseline
- prefer additive migrations when possible
- include rollback or recovery notes
- test migration path when practical
- protect data integrity
- avoid destructive operations without explicit approval
- document backfill behavior
- document compatibility between old and new code
- consider zero-downtime rollout if production-like

High-risk data changes should not be bundled with unrelated refactors.

## Refactoring Guidance

Refactoring must preserve behavior unless explicitly changing behavior.

Before refactoring:

- identify current tests
- add characterization tests if coverage is weak
- keep public contracts stable
- avoid mixing refactor and feature change
- use small steps
- run tests

If behavior changes during refactor, treat it as a separate patch.

## Output Requirements

When completing a ROD-guided development task, include a short summary.

Use this format:

```text
ROD Summary:
- Changed:
- Surface:
- Risk:
- Fitness:
- Rollback:
- Remaining gaps:
```

For Lightweight Mode, keep the summary very short.

For Strict Mode, include any approval, security, migration, or release-gate notes.

Do not write long process commentary unless the user asked for it.

## Anti-Patterns

Avoid these:

- hardcoding prompts, rules, workflows, or thresholds without versioning
- making AI behavior changes without evals
- fixing bugs without regression tests
- adding automation without auditability
- changing permissions without allow and deny tests
- introducing irreversible migrations casually
- letting AI directly mutate production state
- treating “looks better” as proof
- optimizing one metric while silently damaging protected metrics
- weakening tests to pass a patch
- hiding behavior in scattered conditionals
- making large rewrites without baseline tests
- logging secrets or sensitive payloads
- bypassing existing project gates
- changing production config as part of local experimentation
- mixing refactor, feature, migration, and policy change in one patch without need

## ROD Readiness Checklist

A system or feature is ROD-ready when:

- [ ] Important behavior is observable
- [ ] Changeable behavior is identifiable
- [ ] Evolvable surfaces are versioned or versionable
- [ ] Stable Core is protected
- [ ] Tests or evals exist for important behavior
- [ ] Failed cases can become regression tests
- [ ] Rollback or recovery is possible
- [ ] Risk level is known
- [ ] Promotion requires appropriate gates
- [ ] Sensitive data is protected
- [ ] Output contracts are explicit where needed
- [ ] Project conventions are documented

If the checklist is not satisfied, improve the smallest missing part while completing the requested task.

## Default Behavior

When uncertain, choose the safer ROD option:

- Prefer patch over mutation.
- Prefer config over hardcoding.
- Prefer versioned surfaces over hidden behavior.
- Prefer test over assumption.
- Prefer regression case over one-time fix.
- Prefer rollback over one-way change.
- Prefer explicit policy over implicit permission logic.
- Prefer observable behavior over silent behavior.
- Prefer small reversible changes over large rewrites.
- Prefer existing project conventions over new parallel systems.
- Prefer human review for high-risk promotion.
