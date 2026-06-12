"""Command line interface for ROD Skill helper tooling."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .config import RodConfig
from .manifest import ManifestError, load_manifest


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rod-skill")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate a skill manifest")
    validate.add_argument("manifest", nargs="?", default="skill.json")

    render = subparsers.add_parser(
        "render", help="render a skill manifest after environment substitution"
    )
    render.add_argument("manifest", nargs="?", default="skill.json")

    config = subparsers.add_parser("config", help="print resolved helper config")
    config.add_argument(
        "--json", action="store_true", help="print configuration as JSON instead of text"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "validate":
            manifest = load_manifest(Path(args.manifest))
            print(
                f"OK: {manifest['id']} {manifest['version']} "
                f"({manifest['entrypoint']['path']})"
            )
            return 0

        if args.command == "render":
            manifest = load_manifest(Path(args.manifest))
            print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
            return 0

        if args.command == "config":
            config = RodConfig.from_env()
            if args.json:
                print(
                    json.dumps(
                        {
                            "mode": config.mode,
                            "log_level": config.log_level,
                            "defaults_path": str(config.defaults_path),
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                )
            else:
                print(f"mode={config.mode}")
                print(f"log_level={config.log_level}")
                print(f"defaults_path={config.defaults_path}")
            return 0

    except (ManifestError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
