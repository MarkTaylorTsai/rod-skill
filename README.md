# ROD Skills — Ratchet-Oriented Development

[繁體中文](README.zh-TW.md)

ROD (Ratchet-Oriented Development) helps AI agents make software changes in a way that is
observable, testable, reversible, and safe to improve over time. This repository now provides two
first-class skills: one for architecture and one for goal-driven repair or optimization.

Core principle: **AI may propose. Fitness must prove. Policy must permit. Release must be reversible.
Baseline only moves forward.**

## Skills Included

This repository includes two related ROD skills:

1. **ROD Architecture**
   Use when creating new systems or making structural changes. It helps agents design Stable Core
   boundaries, Evolvable Surfaces, fitness checks, observability, rollback paths, and promotion gates.

2. **ROD Goal Loop**
   Use when the user gives a repair, optimization, quality, performance, or "make this pass" target.
   It defines a Goal Contract and loops through Observe, Diagnose, Plan, Patch, Verify, Compare, and
   Decide until the goal is complete or a stop condition is reached.

The root `SKILL.md` and `skill.json` are kept as a backward-compatible default alias for
ROD Architecture.

## Core Features

- Adds Ratchet-Oriented Architecture guidance for designing new systems with protected Stable Core
  boundaries and versioned Evolvable Surfaces.
- Adds a Goal Contract loop for measurable repair, optimization, and verification tasks.
- Helps AI agents separate Stable Core from Evolvable Surfaces.
- Turns meaningful changes into small, observable, testable, and reversible patches.
- Requires behavior-changing prompts, workflows, RAG/KAG settings, policies, configs, and AI outputs
  to have fitness checks.
- Encourages bug fixes to become regression tests.
- Provides a manifest validation CLI for checking integrations before use.

## Directory Structure

```text
rod-skill/
├── .github/
│   └── workflows/
│       └── ci.yml
├── config/
│   └── rod.defaults.json
├── docs/
│   ├── integration.md
│   └── integration.zh-TW.md
├── skills/
│   ├── rod-architecture/
│   │   ├── SKILL.md
│   │   └── skill.json
│   └── rod-goal-loop/
│       ├── SKILL.md
│       └── skill.json
├── src/
│   └── rod_skill/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       └── manifest.py
├── tests/
│   ├── test_env_substitution.py
│   └── test_manifest.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── README.zh-TW.md
├── SKILL.md
├── pyproject.toml
└── skill.json
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/MarkTaylorTsai/rod-skill.git
cd rod-skill
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the package

For normal use:

```bash
pip install -e .
```

For development and tests:

```bash
pip install -e '.[dev]'
pytest -q
```

### 4. Validate the manifests

```bash
rod-skill validate skill.json
rod-skill validate skills/rod-architecture/skill.json
rod-skill validate skills/rod-goal-loop/skill.json
```

Or:

```bash
python -m rod_skill.cli validate skill.json
python -m rod_skill.cli validate skills/rod-architecture/skill.json
python -m rod_skill.cli validate skills/rod-goal-loop/skill.json
```

## Security Notice: Environment Variables and Sensitive Credentials

Do not hardcode API keys, tokens, private keys, passwords, production endpoints, internal paths, or
any sensitive information in `skill.json`, `SKILL.md`, source code, or README files.

Recommended practice:

1. Store sensitive values in a local `.env` file or in your deployment platform's Secrets /
   Environment Variables.
2. Add `.env` to `.gitignore` and never commit it.
3. Commit only `.env.example` to document required variables without real values.
4. Use `${ENV_VAR}` or `${ENV_VAR:-default}` in manifests or external config so the integration layer
   can substitute values at runtime.

Example:

```bash
cp .env.example .env
# Edit .env, but do not commit it.
```

On Linux / macOS:

```bash
set -a
source .env
set +a
```

This project does not require any API key by default. If your own agent platform adds external APIs,
model providers, private databases, or private services, always load credentials from environment
variables or a secret manager. Never hardcode them.

## Usage Examples

### Example 1: ROD Architecture for structural design

**Input**

```text
Design a new AI support system that can evolve prompts, retrieval settings, and workflow rules safely.
```

**Expected ROD Architecture Summary**

```text
ROD Architecture Summary:
- Changed: Proposed initial ROD-friendly project structure and registries.
- Stable Core protected: Auth, tenant boundaries, secrets, audit logs, and promotion paths.
- Evolvable Surfaces: Prompts, retrieval config, workflow rules, evals, and feature flags.
- Fitness: Unit tests, retrieval evals, workflow scenario tests, and citation checks.
- Observability: Trace IDs, structured workflow events, retrieval metrics, and eval reports.
- Rollback: Versioned configs and prompt/workflow registry rollback.
- Remaining gaps: Production release approval policy still needs owner review.
```

### Example 2: ROD Architecture for RAG configuration design

**Input**

```text
Plan how legal QA top_k, reranking, and citation policy should be configurable and testable.
```

**Expected ROD Architecture Summary**

```text
ROD Architecture Summary:
- Changed: Designed retrieval settings as versioned Evolvable Surfaces.
- Stable Core protected: Jurisdiction filters, citation policy gates, and audit logs.
- Evolvable Surfaces: top_k, reranker model, rerank_top_n, freshness boost, and authority boost.
- Fitness: Recall@K, citation support, jurisdiction match, latency, and unsupported claim rate.
- Observability: retrieval_performed, citation_gate_failed, and eval_case_created events.
- Rollback: Restore previous retrieval config version.
- Remaining gaps: More jurisdiction-specific golden cases are needed.
```

### Example 3: ROD Goal Loop for test repair

**Input**

```text
Fix the failing test suite and keep iterating until tests pass or you find a blocker.
```

**Expected ROD Goal Loop Summary**

```text
ROD Goal Loop Summary:
- Goal: Test suite passes without weakening tests.
- Final decision: complete
- Changed:
- Surface:
- Risk:
- Iterations:
- Verification:
- Completion evidence:
- Rollback:
- Remaining gaps:
```

### Example 4: Render a resolved manifest

**Input**

```bash
rod-skill render skills/rod-architecture/skill.json
```

**Output**

```json
{
  "id": "rod-architecture",
  "name": "ROD Architecture",
  "version": "0.2.0",
  "entrypoint": {
    "type": "markdown",
    "path": "skills/rod-architecture/SKILL.md"
  }
}
```

The actual output includes the complete manifest. If the manifest contains values such as
`${ROD_SKILL_MODE:-standard}`, the helper resolves them using the current environment or the provided
default value.

## Integration

Choose the manifest that matches the task:

- Use root `skill.json` for backward-compatible ROD Architecture behavior.
- Use `skills/rod-architecture/skill.json` for new systems, architecture design, structural changes,
  and refactor planning.
- Use `skills/rod-goal-loop/skill.json` for measurable repair, optimization, quality, performance,
  prompt, RAG/KAG, workflow, or test-fixing goals.

Keep environment variable substitution in the integration layer. Do not put secrets directly in any
manifest.

See [`docs/integration.md`](docs/integration.md) for more details.

## Development

Run tests:

```bash
pytest -q
```

Validate the manifests:

```bash
rod-skill validate skill.json
rod-skill validate skills/rod-architecture/skill.json
rod-skill validate skills/rod-goal-loop/skill.json
```

## License

MIT License. See [`LICENSE`](LICENSE).
