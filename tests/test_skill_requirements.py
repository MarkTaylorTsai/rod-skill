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
        "Metric Quality Requirements",
        "Correctness and verification metrics",
        "Behavior invariant metrics",
        "Deterministic scenario metrics",
        "Interface and integration contract metrics",
        "Scope, dependency, and artifact guardrails",
        "Safety, security, privacy, and policy metrics",
        "Performance, reliability, and resource metrics",
        "Observability and rollback metrics",
        "Minimum expectation: use at least five applicable metric categories for a new project",
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
        assert "Metric gates must protect behavior, contracts, scope, safety, and rollback evidence" in text


def test_goal_loop_rejects_baseline_only_rollback_for_project_patches() -> None:
    text = GOAL_LOOP.read_text(encoding="utf-8")

    assert "A baseline-only rollback is not enough for code or configuration patches." in text
    assert "restores only the baseline artifact" in text
    assert "only when the patch itself changes only the baseline artifact" in text


def test_goal_loop_rejects_coarse_test_count_only_metrics() -> None:
    text = GOAL_LOOP.read_text(encoding="utf-8")

    assert "Do not rely" in text
    assert "test count" in text
    assert "pass count" in text
    assert "single smoke check" in text
    assert "defining metrics that only count tests" in text
    assert "behavior invariants" in text
    assert "deterministic scenarios" in text
    assert "rollback coverage" in text
