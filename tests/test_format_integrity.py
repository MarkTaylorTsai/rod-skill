from __future__ import annotations

import ast
import json
from pathlib import Path
import subprocess
import tomllib
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
SKILL_FILES = [
    ROOT / "SKILL.md",
    ROOT / "skills/rod-architecture/SKILL.md",
    ROOT / "skills/rod-goal-loop/SKILL.md",
]
MARKDOWN_FILES = [
    ROOT / "README.md",
    ROOT / "README.zh-TW.md",
    ROOT / "docs/integration.md",
    ROOT / "docs/integration.zh-TW.md",
    *SKILL_FILES,
]
JSON_FILES = [
    ROOT / "skill.json",
    ROOT / "skills/rod-architecture/skill.json",
    ROOT / "skills/rod-goal-loop/skill.json",
    ROOT / "config/rod.defaults.json",
]
PYTHON_FILES = [
    *sorted((ROOT / "src/rod_skill").glob("*.py")),
    *sorted((ROOT / "tests").glob("*.py")),
]
BIDI_OR_HIDDEN_CODEPOINTS = {
    0x200B,
    0x200C,
    0x200D,
    0x202A,
    0x202B,
    0x202C,
    0x202D,
    0x202E,
    0x2066,
    0x2067,
    0x2068,
    0x2069,
    0xFEFF,
}


def _tracked_text_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    paths = []
    for name in output.splitlines():
        path = ROOT / name
        if path.suffix.lower() in {".md", ".json", ".py", ".toml", ".yml", ".yaml", ".txt"}:
            paths.append(path)
        elif path.name in {".gitignore", ".env.example", ".gitattributes"}:
            paths.append(path)
    return paths


def test_skill_front_matter_is_multiline_yaml() -> None:
    for path in SKILL_FILES:
        lines = path.read_text(encoding="utf-8").splitlines()

        assert lines[0] == "---", path
        assert lines[1].startswith("name: "), path
        assert lines[2] == "description: >-", path
        assert lines[3].startswith("  "), path
        assert "---" in lines[4:8], path


def test_json_files_are_valid_pretty_json() -> None:
    for path in JSON_FILES:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
        pretty = json.dumps(data, ensure_ascii=False, indent=2) + "\n"

        assert raw == pretty, path


def test_toml_and_python_files_parse() -> None:
    with (ROOT / "pyproject.toml").open("rb") as file:
        tomllib.load(file)

    for path in PYTHON_FILES:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_no_hidden_or_bidirectional_unicode_characters() -> None:
    findings = []
    for path in _tracked_text_files():
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            for column, char in enumerate(line, 1):
                codepoint = ord(char)
                if codepoint in BIDI_OR_HIDDEN_CODEPOINTS or unicodedata.category(char) == "Cf":
                    name = unicodedata.name(char, "UNKNOWN")
                    findings.append(f"{path.relative_to(ROOT)}:{line_no}:{column}:U+{codepoint:04X}:{name}")

    assert findings == []


def test_markdown_and_python_are_not_single_line_blobs() -> None:
    for path in [*MARKDOWN_FILES, *PYTHON_FILES, ROOT / "pyproject.toml"]:
        lines = path.read_text(encoding="utf-8").splitlines()
        non_empty_lines = [line for line in lines if line.strip()]

        assert len(non_empty_lines) >= 5, path
        assert all(len(line) <= 120 for line in lines), path
