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


def test_architecture_defines_ai_system_surfaces_and_contracts() -> None:
    text = ARCHITECTURE.read_text(encoding="utf-8")

    required = [
        "AI System Architecture Pattern",
        "RAG",
        "graph RAG",
        "sub-agent spawn limits",
        "skill manifests",
        "workflow contract",
        "agent contract",
        "skill contract",
        "loop contract",
        "deterministic offline evals using mock providers",
    ]
    for phrase in required:
        assert phrase in text


def test_goal_loop_defines_ai_system_ratchet_gates() -> None:
    text = GOAL_LOOP.read_text(encoding="utf-8")

    required = [
        "AI System Ratchet Gates",
        "Provider and model contract",
        "Prompt and template quality",
        "RAG retrieval quality",
        "Graph RAG quality",
        "Workflow quality",
        "Agent and sub-agent safety",
        "Skill creation quality",
        "Loop control and self-improvement safety",
        "Grounding, citation, and answer policy",
        "RAG citation coverage",
        "sub-agent spawn limits",
        "skill manifest validation",
        "loop stop criteria",
        "provider",
        "prefixes",
        "absent",
    ]
    for phrase in required:
        assert phrase in text


def test_goal_loop_requires_ratchet_tooling_integrity_gate() -> None:
    text = GOAL_LOOP.read_text(encoding="utf-8")

    required = [
        "Ratchet Tooling Integrity Gate",
        "Ratchet tooling is Stable Core",
        "every standard entry point resolves to an existing file",
        "evaluate` emits machine-readable results",
        "ratchet` invokes the current evaluation command",
        "snapshot` captures the ratchet tooling files",
        "rollback` restores the ratchet tooling files",
        "baseline` never promotes an evaluation with required failed gates",
        "script name exists but its target file is missing",
        "tooling survival gate",
    ]
    for phrase in required:
        assert phrase in text


def test_root_and_architecture_treat_ratchet_tooling_as_stable_core() -> None:
    for path in [ROOT_SKILL, ARCHITECTURE]:
        text = path.read_text(encoding="utf-8")

        assert "Ratchet tooling is Stable Core" in text
        assert "snapshot" in text
        assert "rollback" in text
        assert "self-checks" in text


def test_goal_loop_requires_ratchet_report_consistency_gate() -> None:
    text = GOAL_LOOP.read_text(encoding="utf-8")

    required = [
        "Ratchet Report Consistency Gate",
        "ratchet report must be internally consistent",
        "accepted` is true only when every required gate passed",
        "accepted` is false when `requiredGatesFailed`",
        "allGatesPassed",
        "failed required gates and an accepted decision",
        "baseline promotion cannot run from a contradictory report",
        "writing a report that lists failed required gates",
    ]
    for phrase in required:
        assert phrase in text


def test_root_and_architecture_require_consistent_ratchet_reports() -> None:
    for path in [ROOT_SKILL, ARCHITECTURE]:
        text = path.read_text(encoding="utf-8")

        assert "Ratchet reports must be internally consistent" in text
        assert "failed required gates cannot coexist with accepted decisions" in text
