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
        "Gate Enforcement Requirements",
        "Recording metrics is not enough",
        "Every protected metric must have an explicit gate rule",
        "rollback coverage gate",
        "rollback drill gate",
        "Do not mark a ratchet gate as accepted when the evaluation status is `error`",
        "Standard Tooling Entry Points",
        "Required standard entry points for new projects",
        "`ratchet` can only be run indirectly through `evaluate`",
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
        assert "Required gates must block acceptance" in text
        assert "standard test/check/evaluate/baseline/snapshot/ratchet/rollback entry points" in text


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


def test_goal_loop_requires_required_gates_to_block_acceptance() -> None:
    text = GOAL_LOOP.read_text(encoding="utf-8")

    assert "Recording metrics is not enough." in text
    assert "required gate fails" in text
    assert "required metrics" in text
    assert "recorded as false" in text
    assert "rollback coverage" in text
    assert "rollback drill" in text
    assert "recording a failed required metric but still marking the ratchet gate as accepted" in text


def test_goal_loop_requires_standard_entry_points_for_new_projects() -> None:
    text = GOAL_LOOP.read_text(encoding="utf-8")

    assert "Standard Tooling Entry Points" in text
    for command in ["test", "check", "evaluate", "baseline", "snapshot", "ratchet", "rollback"]:
        assert f"`{command}`" in text
    assert "must not replace the standard names" in text
    assert "Do not declare a new project complete" in text
    assert "non-standard command" in text
