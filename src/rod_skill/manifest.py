"""Manifest loading and validation utilities.

This module keeps configuration safe by supporting environment variable
placeholders instead of hardcoded sensitive values. Supported syntax:

- ${NAME}: require NAME to exist in the environment.
- ${NAME:-default}: use default when NAME is absent.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
from typing import Any


_ENV_PATTERN = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)(?::-(.*?))?\}")
_REQUIRED_TOP_LEVEL_FIELDS = {
    "manifest_version",
    "id",
    "name",
    "version",
    "description",
    "entrypoint",
    "security",
}


class ManifestError(ValueError):
    """Raised when a skill manifest cannot be loaded or validated."""


def _substitute_env(value: str) -> str:
    """Replace ${ENV_VAR} and ${ENV_VAR:-default} placeholders in a string."""

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        default = match.group(2)
        env_value = os.getenv(name)

        if env_value is not None:
            return env_value
        if default is not None:
            return default
        raise ManifestError(f"Missing required environment variable: {name}")

    return _ENV_PATTERN.sub(replace, value)


def render_manifest(value: Any) -> Any:
    """Recursively render environment placeholders in manifest data."""

    if isinstance(value, str):
        return _substitute_env(value)
    if isinstance(value, list):
        return [render_manifest(item) for item in value]
    if isinstance(value, dict):
        return {key: render_manifest(item) for key, item in value.items()}
    return value


def load_manifest(path: str | Path = "skill.json", *, render_env: bool = True) -> dict[str, Any]:
    """Load a manifest JSON file and optionally render env placeholders."""

    manifest_path = Path(path)
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"Manifest not found: {manifest_path}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"Manifest is not valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ManifestError("Manifest root must be a JSON object")

    rendered = render_manifest(data) if render_env else data
    validate_manifest(rendered)
    return rendered


def validate_manifest(manifest: dict[str, Any]) -> None:
    """Validate the minimum required manifest shape.

    This is intentionally conservative and platform-neutral. Host platforms may
    enforce additional schema rules.
    """

    missing = sorted(_REQUIRED_TOP_LEVEL_FIELDS - manifest.keys())
    if missing:
        raise ManifestError("Missing required manifest fields: " + ", ".join(missing))

    entrypoint = manifest.get("entrypoint")
    if not isinstance(entrypoint, dict):
        raise ManifestError("entrypoint must be an object")
    if entrypoint.get("type") != "markdown":
        raise ManifestError("entrypoint.type must be 'markdown'")
    if not entrypoint.get("path"):
        raise ManifestError("entrypoint.path is required")

    security = manifest.get("security")
    if not isinstance(security, dict):
        raise ManifestError("security must be an object")
    if "secret_handling_policy" not in security:
        raise ManifestError("security.secret_handling_policy is required")

    runtime = manifest.get("runtime", {})
    if runtime and not isinstance(runtime, dict):
        raise ManifestError("runtime must be an object when provided")

    files = manifest.get("files", [])
    if files and not isinstance(files, list):
        raise ManifestError("files must be a list when provided")
