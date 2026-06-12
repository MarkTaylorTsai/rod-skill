# Manifest Contract

This document describes the portable `skill.json` contract used by this repository. It is intentionally
platform-neutral. A host skill registry or agent platform may require additional fields or stricter
validation.

## Required fields

- `manifest_version`: Manifest contract version used by this package.
- `id`: Stable machine-readable skill identifier.
- `name`: Human-readable skill name.
- `version`: Skill package version.
- `description`: Clear summary of when and why to use the skill.
- `entrypoint`: Object describing the instruction entrypoint.
- `entrypoint.type`: Must be `markdown`.
- `entrypoint.path`: Path to the Markdown instruction file, usually `SKILL.md`.
- `security`: Object describing secret and data-handling expectations.
- `security.secret_handling_policy`: Required text explaining how secrets must be handled.

## Recommended fields

- `display_name`: Review-friendly display name.
- `license`: License identifier.
- `language`: Primary instruction language.
- `tags`: Search and categorization tags.
- `runtime`: Runtime needs, including shell, network, and filesystem-write requirements.
- `configuration`: Non-secret defaults and environment-variable placeholders.
- `capabilities`: Machine-readable behaviors the skill provides.
- `files`: Files that belong to the skill package, including required entrypoints.
- `compatibility`: Known agent runtime assumptions.
- `source`: Repository, homepage, and issue tracker links.

## File requirements

The `entrypoint.path` value must point to an existing Markdown file. Any file listed under `files`
with `required: true` must also exist in the repository.

## Security expectations

Manifests and examples must not contain real secrets, tokens, private keys, production credentials,
private endpoints, or sensitive payloads. Use environment-variable placeholders such as
`${ENV_VAR}` or `${ENV_VAR:-default}` instead.

## Schema

The repository includes `schemas/skill.schema.json` as a portable JSON Schema for this contract.
It documents the expected shape used by this package, but platform-specific registries may enforce
their own official schema.
