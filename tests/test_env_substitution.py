from __future__ import annotations

import pytest

from rod_skill.manifest import ManifestError, render_manifest


def test_render_manifest_uses_default_for_missing_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ROD_SKILL_MODE", raising=False)

    rendered = render_manifest({"mode": "${ROD_SKILL_MODE:-standard}"})

    assert rendered == {"mode": "standard"}


def test_render_manifest_uses_environment_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ROD_SKILL_MODE", "strict")

    rendered = render_manifest({"mode": "${ROD_SKILL_MODE:-standard}"})

    assert rendered == {"mode": "strict"}


def test_render_manifest_requires_missing_env_without_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PRIVATE_API_KEY", raising=False)

    with pytest.raises(ManifestError, match="PRIVATE_API_KEY"):
        render_manifest({"api_key": "${PRIVATE_API_KEY}"})
