#!/usr/bin/env python3
"""Validate and update the coordinated VIVAaLingua version fields."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:\.(0|[1-9][0-9]*))?$")
VERSION_FILE = Path("release/VERSION")
SKILL_FILE = Path("src/vivaalingua/SKILL.md")


def parse_version(value: str) -> tuple[int, int, int]:
    if not VERSION_RE.fullmatch(value):
        raise ValueError(f"Invalid version {value!r}. Use MAJOR.MINOR or MAJOR.MINOR.PATCH without a leading v.")
    parts = tuple(int(part) for part in value.split("."))
    return parts + (0,) * (3 - len(parts))


def coordinated_version(root: Path) -> str:
    file_version = (root / VERSION_FILE).read_text(encoding="utf-8").strip()
    skill_text = (root / SKILL_FILE).read_text(encoding="utf-8")
    skill_matches = re.findall(r"(?m)^- Installed version: `([^`]+)`[ \t]*$", skill_text)
    if len(skill_matches) != 1:
        raise ValueError("Expected exactly one Installed version field in SKILL.md.")
    skill_version = skill_matches[0]
    parse_version(file_version)
    parse_version(skill_version)
    if file_version != skill_version:
        raise ValueError(f"Version sources disagree: version file is {file_version}, SKILL.md is {skill_version}.")
    return file_version


def update_version(root: Path, new_version: str) -> str:
    new_order = parse_version(new_version)
    current = coordinated_version(root)
    if new_order <= parse_version(current):
        raise ValueError(f"New version {new_version} must be greater than current version {current}.")
    version_path = root / VERSION_FILE
    skill_path = root / SKILL_FILE
    skill_text = skill_path.read_text(encoding="utf-8")
    skill_text, skill_count = re.subn(r"(?m)^- Installed version: `[^`]+`[ \t]*$", f"- Installed version: `{new_version}`", skill_text)
    if skill_count != 1:
        raise ValueError("Could not safely replace exactly one Installed version field in SKILL.md.")
    version_path.write_text(new_version + "\n", encoding="utf-8")
    skill_path.write_text(skill_text, encoding="utf-8")
    return current


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Next MAJOR.MINOR or MAJOR.MINOR.PATCH version")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        old = update_version(args.root.resolve(), args.version)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Updated coordinated version fields: {old} -> {args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
