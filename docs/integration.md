# ROD Skills Integration Guide

[繁體中文](integration.zh-TW.md)

This document explains how to integrate the ROD skills into an AI Agent runtime that supports
Manifest / Skill loading.

## Skills and Entry Points

This repository includes three manifest entry points:

- `skill.json`: backward-compatible default alias for ROD Architecture.
- `skills/rod-architecture/skill.json`: first-class ROD Architecture skill.
- `skills/rod-goal-loop/skill.json`: first-class ROD Goal Loop skill.

The root alias exists so older integrations that only load `skill.json` continue to receive
architecture/development guidance. It is not a separate third skill.

## Skill Selection Rules

Use ROD Architecture when:

- creating a new system
- making structural changes
- designing evolvable surfaces
- defining Stable Core boundaries
- planning prompts, workflows, RAG/KAG, policies, or release gates

Use ROD Goal Loop when:

- fixing bugs
- making failing tests pass
- optimizing performance or quality
- improving prompts, RAG/KAG, workflows, policies, or eval metrics
- the user gives a measurable completion target

Do not use ROD Goal Loop for open-ended architecture design unless there is a measurable
Goal Contract.

## Basic Integration Flow

1. Choose the manifest that matches the task.
2. Read the selected `skill.json`.
3. Validate required fields: `id`, `name`, `version`, `description`, `entrypoint`, and `security`.
4. Resolve manifest environment variable placeholders, such as `${ROD_SKILL_MODE:-standard}`.
5. Read the `SKILL.md` file referenced by `entrypoint.path`.
6. Inject that `SKILL.md` into the agent as a skill, development mode, or system workflow guideline.

## Environment Variable Strategy

ROD Skills do not require API keys by default. If your integration layer needs external models,
vector databases, private services, or other sensitive resources, use environment variables or your
platform's Secret Manager.

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
rod-skill validate skills/rod-architecture/skill.json
rod-skill validate skills/rod-goal-loop/skill.json
```

Render manifests after environment variable substitution:

```bash
rod-skill render skill.json
rod-skill render skills/rod-architecture/skill.json
rod-skill render skills/rod-goal-loop/skill.json
```

## Output Formats

ROD Architecture should produce:

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

ROD Goal Loop should produce:

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

The Goal Loop final decision must be one of `complete`, `blocked`, `needs_review`, `reverted`,
`unsafe`, or `budget_reached`.
