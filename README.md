# ROD Skill — Ratchet-Oriented Development

[繁體中文](README.zh-TW.md)

ROD (Ratchet-Oriented Development) is a development skill for AI Agent / Skill / Manifest systems. It helps new and existing projects make software changes in a way that is verifiable, reversible, observable, and safe to improve over time.

Core principle: **AI may propose. Fitness must prove. Policy must permit. Release must be reversible. Baseline only moves forward.**

This repository packages the ROD Skill as an open-source project that can be downloaded, validated, and integrated into agent runtimes. It includes:

- `SKILL.md`: the full skill instructions and operating rules.
- `skill.json`: a standardized manifest for agent platforms and integrators.
- `src/rod_skill/`: helper utilities for manifest loading, environment variable substitution, and basic validation.
- `tests/`: tests for manifest validation and environment variable substitution.
- `config/`: default configuration examples.

## Core Features

- Helps AI agents separate **Stable Core** from **Evolvable Surfaces**.
- Turns meaningful changes into small, observable, testable, and reversible patches.
- Uses Strict Mode for high-risk areas such as auth, permissions, secrets, data deletion, migrations, and release gates.
- Requires behavior-changing prompts, workflows, RAG/KAG settings, policies, configs, and AI outputs to have fitness checks.
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

### 4. Validate the manifest

```bash
rod-skill validate skill.json
```

Or:

```bash
python -m rod_skill.cli validate skill.json
```

## Security Notice: Environment Variables and Sensitive Credentials

Do not hardcode API keys, tokens, private keys, passwords, production endpoints, internal paths, or any sensitive information in `skill.json`, `SKILL.md`, source code, or README files.

Recommended practice:

1. Store sensitive values in a local `.env` file or in your deployment platform's Secrets / Environment Variables.
2. Add `.env` to `.gitignore` and never commit it.
3. Commit only `.env.example` to document required variables without real values.
4. Use `${ENV_VAR}` or `${ENV_VAR:-default}` in manifests or external config so the integration layer can substitute values at runtime.

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

This project does not require any API key by default. If your own agent platform adds external APIs, model providers, private databases, or private services, always load credentials from environment variables or a secret manager. Never hardcode them.

## Usage Examples

### Example 1: Fix behavior-changing authentication logic

**Input**

```text
Fix the login flow bug where an unauthenticated user can sometimes access the dashboard.
```

**Expected ROD Skill Output Summary**

```text
ROD Summary:
- Changed: Fixed the dashboard route guard so unauthenticated users are redirected to login.
- Surface: permission / code
- Risk: high
- Fitness: Added allow/deny tests to verify authenticated users can enter and unauthenticated users cannot.
- Rollback: Revert the route guard patch and the added tests.
- Remaining gaps: Audit event coverage has not been added yet and can be handled in a follow-up patch.
```

### Example 2: Adjust RAG retrieval settings

**Input**

```text
Change legal QA top_k from 5 to 10 and check whether answers become more complete.
```

**Expected ROD Skill Output Summary**

```text
ROD Summary:
- Changed: Updated rag_config.legal_qa.top_k from 5 to 10.
- Surface: rag_config
- Risk: medium
- Fitness: Ran retrieval evals for Recall@K, citation support, latency, and unsupported claim rate.
- Rollback: Restore top_k to 5.
- Remaining gaps: More jurisdiction-specific golden cases are needed.
```

### Example 3: Render the resolved manifest

**Input**

```bash
rod-skill render skill.json
```

**Output**

```json
{
  "id": "rod",
  "name": "ROD",
  "version": "0.1.0",
  "entrypoint": {
    "type": "markdown",
    "path": "SKILL.md"
  }
}
```

The actual output includes the complete manifest. If the manifest contains values such as `${ROD_SKILL_MODE:-standard}`, the helper resolves them using the current environment or the provided default value.

## Integration

1. Copy `skill.json` and `SKILL.md` into the skills directory used by your agent platform.
2. Let the agent runtime read `entrypoint.path` from `skill.json`.
3. Inject the content of `SKILL.md` as a system skill, development workflow, or operating guideline.
4. Keep environment variable substitution in the integration layer. Do not put secrets directly in the manifest.

See [`docs/integration.md`](docs/integration.md) for more details.

## Development

Run tests:

```bash
pytest -q
```

Validate the manifest:

```bash
rod-skill validate skill.json
```

## License

MIT License. See [`LICENSE`](LICENSE).
