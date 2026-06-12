from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GOAL_LOOP = ROOT / "skills/rod-goal-loop/SKILL.md"
ROOT_SKILL = ROOT / "SKILL.md"
ARCHITECTURE = ROOT / "skills/rod-architecture/SKILL.md"


def test_goal_loop_requires_baseline_ratchet_and_rollback_gate() -> None:
    text = GOAL_LOOP.read_text(encoding="utf-8")

    required_phrases = [
        "Baseline and Ratchet Gate Requirements",
        "baseline command",
        "protected metrics",
        "tolerance",
        "rollback method",
        "rollback coverage",
        "full project file snapshot",
        "baseline-only rollback is not enough",
        "promotion rule",
        "ratchet gate",
        "comparison_result",
        "rollback_coverage",
        "rollback_trigger",
    ]

    for phrase in required_phrases:
        assert phrase in text


def test_root_and_architecture_route_improvement_work_to_goal_loop_gate() -> None:
    for path in [ROOT_SKILL, ARCHITECTURE]:
        text = path.read_text(encoding="utf-8")

        assert "Baseline gates are required for non-trivial improvement loops." in text
        assert "baseline" in text
        assert "comparison rule" in text
        assert "rollback point" in text
        assert "rollback coverage" in text


def test_goal_loop_rejects_baseline_only_rollback_for_project_patches() -> None:
    text = GOAL_LOOP.read_text(encoding="utf-8")

    assert "A baseline-only rollback is not enough for code or configuration patches." in text
    assert "restores only the baseline artifact" in text
    assert "only when the patch itself changes only the baseline artifact" in text
