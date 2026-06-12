"""Runtime configuration helpers for local ROD Skill tooling.

The skill itself does not require secrets. This module intentionally reads
configuration from environment variables so integrators do not hardcode keys,
tokens, credentials, or machine-specific paths in source files.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


_VALID_MODES = {"lightweight", "standard", "strict"}


@dataclass(frozen=True)
class RodConfig:
    """Configuration loaded from environment variables."""

    mode: str = "standard"
    log_level: str = "INFO"
    defaults_path: Path = Path("config/rod.defaults.json")

    @classmethod
    def from_env(cls) -> "RodConfig":
        """Load configuration from the current process environment.

        Supported variables:
        - ROD_SKILL_MODE: lightweight, standard, or strict.
        - ROD_SKILL_LOG_LEVEL: log level string used by helper tools.
        - ROD_SKILL_DEFAULTS_PATH: path to external defaults JSON.
        """

        mode = os.getenv("ROD_SKILL_MODE", cls.mode).strip().lower()
        if mode not in _VALID_MODES:
            raise ValueError(
                "ROD_SKILL_MODE must be one of: " + ", ".join(sorted(_VALID_MODES))
            )

        log_level = os.getenv("ROD_SKILL_LOG_LEVEL", cls.log_level).strip().upper()
        defaults_path = Path(
            os.getenv("ROD_SKILL_DEFAULTS_PATH", str(cls.defaults_path))
        ).expanduser()

        return cls(mode=mode, log_level=log_level, defaults_path=defaults_path)
