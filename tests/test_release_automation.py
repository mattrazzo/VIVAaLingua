from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.build_skill_packages import COMMON_FILES, PLATFORM_FILES, build_packages, validate_release_tag
from scripts.update_version import coordinated_version, parse_version, update_version

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COMMON = set(COMMON_FILES)


class VersionManagementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "src/vivaalingua").mkdir(parents=True)
        (self.root / "release").mkdir()
        (self.root / "release/VERSION").write_text(
            "1.5\n",
            encoding="utf-8",
        )
        (self.root / "src/vivaalingua/SKILL.md").write_text(
            "---\nname: vivaalingua\n---\n- Installed version: `1.5`\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_updates_both_fields_with_two_part_version(self) -> None:
        self.assertEqual(update_version(self.root, "1.6"), "1.5")
        self.assertEqual(coordinated_version(self.root), "1.6")
        self.assertFalse((self.root / "VIVAaLingua Version.txt").exists())
        self.assertFalse((self.root / "release/VIVAaLingua Version.txt").exists())
        self.assertEqual((self.root / "release/VERSION").read_text(encoding="utf-8"), "1.6\n")

    def test_updates_both_fields_with_three_part_version(self) -> None:
        self.assertEqual(update_version(self.root, "1.5.1"), "1.5")
        self.assertEqual(coordinated_version(self.root), "1.5.1")

    def test_rejects_bad_versions_and_non_increasing_versions(self) -> None:
        for value in ("v1.6", "1", "1.5.0.1", "01.6", "1.5", "1.4.9", "1.5.0"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                update_version(self.root, value)
        self.assertEqual(coordinated_version(self.root), "1.5")

    def test_rejects_mismatched_or_invalid_current_fields(self) -> None:
        skill_path = self.root / "src/vivaalingua/SKILL.md"
        skill_path.write_text("- Installed version: `1.4`\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "disagree"):
            update_version(self.root, "1.6")
        skill_path.write_text("- Installed version: `bad`\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            update_version(self.root, "1.6")

    def test_version_comparison_treats_missing_patch_as_zero(self) -> None:
        self.assertEqual(parse_version("1.5"), parse_version("1.5.0"))

    def test_rejects_invalid_version_file_without_changing_sources(self) -> None:
        version_path = self.root / "release/VERSION"
        skill_path = self.root / "src/vivaalingua/SKILL.md"
        for invalid in ("", "Latest version: 1.5\n", "1.5\n1.6\n", "v1.5\n"):
            with self.subTest(content=invalid):
                version_path.write_text(invalid, encoding="utf-8")
                before = (version_path.read_bytes(), skill_path.read_bytes())
                with self.assertRaises(ValueError):
                    update_version(self.root, "1.6")
                self.assertEqual(before, (version_path.read_bytes(), skill_path.read_bytes()))


class PackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.output = Path(self.temp.name) / "dist"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_rejects_mismatched_release_tag(self) -> None:
        version = coordinated_version(REPO_ROOT)
        with self.assertRaisesRegex(ValueError, "does not match"):
            validate_release_tag(REPO_ROOT, f"v{version}.invalid")

    def test_builds_platform_layouts_from_current_repository(self) -> None:
        version = coordinated_version(REPO_ROOT)
        paths = build_packages(REPO_ROOT, self.output, release_tag=f"v{version}")
        self.assertEqual(len(paths), 3)
        self.assertEqual({p.name for p in paths}, {
            f"VIVAaLingua-ChatGPT-v{version}.zip",
            f"VIVAaLingua-Claude-v{version}.zip",
            f"VIVAaLingua-Gemini-v{version}.zip",
        })
        by_platform = {p.name.split("-")[1]: p for p in paths}
        for platform, archive_path in by_platform.items():
            with zipfile.ZipFile(archive_path) as archive:
                entries = set(archive.namelist())
                if platform == "Gemini":
                    self.assertEqual(entries, EXPECTED_COMMON)
                    self.assertIn("SKILL.md", entries)
                else:
                    prefix = "vivaalingua/"
                    self.assertEqual(entries, {prefix + name for name in PLATFORM_FILES[platform]})
                    self.assertIn(prefix + "SKILL.md", entries)
                self.assertFalse(any(".DS_Store" in name or "__MACOSX" in name for name in entries))
                skill_path = "SKILL.md" if platform == "Gemini" else "vivaalingua/SKILL.md"
                self.assertIn(f"Installed version: `{version}`".encode(), archive.read(skill_path))
                if platform == "ChatGPT":
                    self.assertIn("vivaalingua/agents/openai.yaml", entries)
                else:
                    self.assertFalse(any("agents/" in name for name in entries))

    def test_archives_are_reproducible(self) -> None:
        first = build_packages(REPO_ROOT, self.output)
        data = {p.name: p.read_bytes() for p in first}
        second = build_packages(REPO_ROOT, self.output)
        self.assertEqual(data, {p.name: p.read_bytes() for p in second})


if __name__ == "__main__":
    unittest.main()
