from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft7Validator

from rod_skill.config import RodConfig
from rod_skill.manifest import ManifestError, load_manifest, validate_manifest


MANIFEST_PATHS = [
    Path("skill.json"),
    Path("skills/rod-architecture/skill.json"),
    Path("skills/rod-goal-loop/skill.json"),
]


def test_load_repository_manifest() -> None:
    manifest = load_manifest(Path("skill.json"))

    assert manifest["id"] == "rod"
    assert manifest["version"] == "0.8.0"
    assert manifest["entrypoint"] == {"type": "markdown", "path": "SKILL.md"}
    assert manifest["runtime"]["requires_network"] is False
    assert manifest["security"]["secrets_required"] == []
    assert "select_rod_subskill" in manifest["capabilities"]
    assert "run_ratchet_goal_loop" in manifest["capabilities"]


def test_load_all_skill_manifests() -> None:
    for path in MANIFEST_PATHS:
        manifest = load_manifest(path)
        entrypoint = manifest["entrypoint"]

        assert manifest["version"] == "0.8.0"
        assert entrypoint["type"] == "markdown"
        assert entrypoint["path"].endswith("SKILL.md")
        assert Path(entrypoint["path"]).is_file()
        assert manifest["runtime"]["requires_network"] is False
        assert manifest["security"]["secrets_required"] == []


def test_first_class_skill_ids() -> None:
    architecture = load_manifest(Path("skills/rod-architecture/skill.json"))
    goal_loop = load_manifest(Path("skills/rod-goal-loop/skill.json"))

    assert architecture["id"] == "rod-architecture"
    assert "apply_ratchet_oriented_architecture" in architecture["capabilities"]
    assert "run_ratchet_goal_loop" not in architecture["capabilities"]

    assert goal_loop["id"] == "rod-goal-loop"
    assert "run_ratchet_goal_loop" in goal_loop["capabilities"]
    assert goal_loop["configuration"]["max_iterations"] == "5"


def test_validate_manifest_rejects_missing_required_field() -> None:
    with pytest.raises(ManifestError, match="description"):
        validate_manifest(
            {
                "manifest_version": "1.0.0",
                "id": "rod",
                "name": "ROD",
                "version": "0.8.0",
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


def test_manifests_match_portable_json_schema() -> None:
    schema = json.loads(Path("schemas/skill.schema.json").read_text(encoding="utf-8"))
    Draft7Validator.check_schema(schema)
    validator = Draft7Validator(schema)

    for path in MANIFEST_PATHS:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.path))

        assert errors == []
