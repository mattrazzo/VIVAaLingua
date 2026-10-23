#!/usr/bin/env python3
"""Build reproducible, platform-specific VIVAaLingua skill ZIP files."""
from __future__ import annotations

import argparse
import stat
import zipfile
from pathlib import Path

try:
    from .update_version import coordinated_version, parse_version
except ImportError:  # Running as a standalone workflow script.
    from update_version import coordinated_version, parse_version

SKILL_ROOT = Path("src/vivaalingua")
COMMON_FILES = (
    "SKILL.md",
    "references/coaching-reference.md",
    "references/pronunciation-reference.md",
    "references/help-reference.md",
    "references/regression-tests.md",
    "assets/icon.svg",
)
PLATFORM_FILES = {
    "ChatGPT": COMMON_FILES + ("agents/openai.yaml",),
    "Claude": COMMON_FILES,
    "Gemini": COMMON_FILES,
}


def validate_release_tag(root: Path, tag: str) -> str:
    version = coordinated_version(root)
    if tag != f"v{version}":
        raise ValueError(f"Release tag {tag!r} does not match coordinated version v{version}.")
    return version


def _zip_entry(archive: zipfile.ZipFile, archive_name: str, source: Path) -> None:
    info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (stat.S_IFREG | 0o644) << 16
    archive.writestr(info, source.read_bytes())


def build_packages(root: Path, output_dir: Path, release_tag: str | None = None) -> list[Path]:
    version = coordinated_version(root)
    if release_tag is not None:
        validate_release_tag(root, release_tag)
    source_root = root / SKILL_ROOT
    output_dir.mkdir(parents=True, exist_ok=True)
    built: list[Path] = []
    for platform, files in PLATFORM_FILES.items():
        destination = output_dir / f"VIVAaLingua-{platform}-v{version}.zip"
        with zipfile.ZipFile(destination, "w") as archive:
            for relative in sorted(files):
                source = source_root / relative
                if not source.is_file():
                    raise FileNotFoundError(f"Required package source is missing: {source}")
                if platform == "Gemini":
                    archive_name = relative
                else:
                    archive_name = f"vivaalingua/{relative}"
                _zip_entry(archive, archive_name, source)
        built.append(destination)
    return built


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help=argparse.SUPPRESS)
    parser.add_argument("--output-dir", type=Path, default=None, help="Output folder (default: ROOT/dist)")
    parser.add_argument("--release-tag", help="Also require this tag to equal v plus both installed version fields")
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = (args.output_dir or root / "dist").resolve()
    try:
        files = build_packages(root, output_dir, args.release_tag)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    for path in files:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
