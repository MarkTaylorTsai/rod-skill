# ROD Skill Integration Guide

[繁體中文](integration.zh-TW.md)

This document explains how to integrate the ROD Skill into an AI Agent runtime that supports Manifest / Skill loading.

## Basic Integration Flow

1. Read `skill.json`.
2. Validate the required fields: `id`, `name`, `version`, `description`, `entrypoint`, and `security`.
3. Resolve manifest environment variable placeholders, such as `${ROD_SKILL_MODE:-standard}`.
4. Read the `SKILL.md` file referenced by `entrypoint.path`.
5. Inject `SKILL.md` into the agent as a skill, development mode, or system workflow guideline.
6. Enable ROD when a task may affect behavior, quality, security, data, workflows, RAG/KAG, policy, or release behavior.

## Environment Variable Strategy

ROD Skill itself does not require an API key. If your integration layer needs external models, vector databases, private services, or other sensitive resources, use environment variables or your platform's Secret Manager.

Do not commit:

- `.env`
- API keys
- access tokens
- private keys
- production credentials
- raw sensitive payloads

Recommended files to commit:

- `.env.example`
- config schemas
- redacted sample configs
- defaults that contain no sensitive values

## Manifest Validation

After installing the helper, run:

```bash
rod-skill validate skill.json
```

Render the manifest after environment variable substitution:

```bash
rod-skill render skill.json
```

## Agent Usage Recommendations

Use ROD Standard Mode or Strict Mode for tasks such as:

- feature work, bug fixes, or refactors
- prompt, workflow, policy, RAG/KAG, or config changes
- auth, permission, secrets, migrations, or production release gates
- AI output quality, safety, grounding, or citation behavior changes

Use Lightweight Mode for typo fixes, formatting, comments, or documentation-only edits.

## Output Format

When completing a ROD-guided task, the agent should output:

```text
ROD Summary:
- Changed:
- Surface:
- Risk:
- Fitness:
- Rollback:
- Remaining gaps:
```

This helps users quickly understand what changed, where the risk is, how the work was verified, and how it can be rolled back.
