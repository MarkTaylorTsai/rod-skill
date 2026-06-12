from __future__ import annotations

from pathlib import Path

import pytest

from rod_skill.config import RodConfig
from rod_skill.manifest import ManifestError, load_manifest, validate_manifest


def test_load_repository_manifest() -> None:
    manifest = load_manifest(Path("skill.json"))

    assert manifest["id"] == "rod"
    assert manifest["entrypoint"] == {"type": "markdown", "path": "SKILL.md"}
    assert manifest["runtime"]["requires_network"] is False
    assert manifest["security"]["secrets_required"] == []


def test_validate_manifest_rejects_missing_required_field() -> None:
    with pytest.raises(ManifestError, match="description"):
        validate_manifest(
            {
                "manifest_version": "1.0.0",
                "id": "rod",
                "name": "ROD",
                "version": "0.1.0",
                "entrypoint": {"type": "markdown", "path": "SKILL.md"},
                "security": {"secret_handling_policy": "Use env vars."},
            }
        )


def test_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ROD_SKILL_MODE", "strict")
    monkeypatch.setenv("ROD_SKILL_LOG_LEVEL", "debug")
    monkeypatch.setenv("ROD_SKILL_DEFAULTS_PATH", "config/custom.json")

    config = RodConfig.from_env()

    assert config.mode == "strict"
    assert config.log_level == "DEBUG"
    assert str(config.defaults_path) == "config/custom.json"
