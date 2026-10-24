from __future__ import annotations

import copy
import hashlib
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.release_skill import GitHub, command, release_skill

SOURCE = Path(__file__).resolve().parents[1]


class FakeGitHub:
    def __init__(self):
        self.data = None
        self.tags = {}
        self.events = []
        self.fail_create = False
        self.fail_upload = False
        self.corrupt_digest = False

    def release(self, tag):
        return copy.deepcopy(self.data)

    def tag_commit(self, tag):
        return self.tags.get(tag)

    def create_draft(self, tag, commit):
        if self.fail_create:
            self.fail_create = False
            raise RuntimeError("Interrupted draft creation")
        self.events.append("draft")
        self.data = {
            "draft": True, "prerelease": False, "target_commitish": commit,
            "assets": [], "html_url": f"https://example.test/releases/{tag}",
        }

    def upload(self, tag, paths):
        assert self.data["draft"], "Published assets must never be overwritten"
        self.events.append("upload")
        assets = {asset["name"]: asset for asset in self.data["assets"]}
        for path in paths:
            assets[path.name] = {
                "name": path.name, "state": "uploaded", "size": path.stat().st_size,
                "digest": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            self.data["assets"] = list(assets.values())
            if self.fail_upload:
                self.fail_upload = False
                raise RuntimeError("Interrupted upload")
        if self.corrupt_digest:
            self.data["assets"][0]["digest"] = "sha256:incorrect"

    def publish(self, tag):
        assert self.data["draft"]
        assert len(self.data["assets"]) == 6, "All ZIPs must exist before publication"
        self.events.append("publish")
        self.data["draft"] = False
        self.tags[tag] = self.data["target_commitish"]


class SingleReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.parent = Path(self.temp.name)
        self.root = self.parent / "checkout"
        self.root.mkdir()
        self.origin = self.parent / "origin.git"
        command(["git", "init", "--bare", "--initial-branch=main", str(self.origin)])
        command(["git", "init", "--initial-branch=main"], self.root)
        command(["git", "config", "user.name", "Fixture"], self.root)
        command(["git", "config", "user.email", "fixture@example.test"], self.root)
        shutil.copytree(SOURCE / "src", self.root / "src")
        skill = self.root / "src/vivaalingua/SKILL.md"
        skill.write_text(re.sub(r"Installed version: `[^`]+`", "Installed version: `1.5`", skill.read_text()))
        (self.root / "release").mkdir()
        (self.root / "release/VERSION").write_text("1.5\n")
        (self.root / ".gitignore").write_text("/dist/\n__pycache__/\n")
        command(["git", "add", "."], self.root)
        command(["git", "commit", "-m", "Initial content"], self.root)
        command(["git", "remote", "add", "origin", str(self.origin)], self.root)
        command(["git", "push", "-u", "origin", "main"], self.root)
        self.head = command(["git", "rev-parse", "HEAD"], self.root)
        self.github = FakeGitHub()

    def tearDown(self):
        self.temp.cleanup()

    def run_release(self, version="1.6", run_id="123"):
        return release_skill(self.root, version, run_id, self.github)

    def test_one_trigger_pushes_version_and_publishes_all_six_assets(self):
        url = self.run_release()
        self.assertEqual(url, "https://example.test/releases/v1.6")
        self.assertEqual(self.github.events, ["draft", "upload", "publish"])
        self.assertEqual((self.root / "release/VERSION").read_text(), "1.6\n")
        head = command(["git", "rev-parse", "HEAD"], self.root)
        self.assertEqual(self.github.tags["v1.6"], head)
        self.assertEqual(command(["git", "rev-parse", "refs/heads/main"], self.origin), head)
        changed = set(command(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"], self.root).splitlines())
        self.assertEqual(changed, {"release/VERSION", "src/vivaalingua/SKILL.md"})
        for platform in ("ChatGPT", "Claude", "Gemini"):
            stable = self.root / "dist" / f"VIVAaLingua-{platform}.zip"
            versioned = self.root / "dist" / f"VIVAaLingua-{platform}-v1.6.zip"
            self.assertEqual(stable.read_bytes(), versioned.read_bytes())

    def test_three_part_version_is_supported(self):
        self.run_release("1.5.1")
        self.assertEqual((self.root / "release/VERSION").read_text(), "1.5.1\n")
        self.assertIn("v1.5.1", self.github.tags)

    def test_invalid_or_non_increasing_versions_do_not_write_or_publish(self):
        for version in ("v1.6", "1.5", "1.4", "1.5.0", "1.6;echo injected"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                self.run_release(version)
        self.assertEqual((self.root / "release/VERSION").read_text(), "1.5\n")
        self.assertEqual(self.github.events, [])
        self.assertEqual(command(["git", "rev-parse", "HEAD"], self.root), self.head)

    def test_existing_tag_is_rejected_before_version_changes(self):
        self.github.tags["v1.6"] = self.head
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.run_release()
        self.assertEqual((self.root / "release/VERSION").read_text(), "1.5\n")

    def test_interrupted_upload_resumes_without_another_commit(self):
        self.github.fail_upload = True
        with self.assertRaisesRegex(RuntimeError, "Interrupted upload"):
            self.run_release()
        self.assertTrue(self.github.data["draft"])
        head = command(["git", "rev-parse", "HEAD"], self.root)
        self.run_release()
        self.assertEqual(command(["git", "rev-parse", "HEAD"], self.root), head)
        self.assertEqual(self.github.events.count("draft"), 1)
        self.assertEqual(self.github.events.count("publish"), 1)

    def test_failure_after_push_before_draft_creation_can_resume(self):
        self.github.fail_create = True
        with self.assertRaisesRegex(RuntimeError, "Interrupted draft"):
            self.run_release()
        head = command(["git", "rev-parse", "HEAD"], self.root)
        self.run_release()
        self.assertEqual(command(["git", "rev-parse", "HEAD"], self.root), head)

    def test_completed_run_retry_verifies_without_replacing_assets(self):
        self.run_release()
        events = self.github.events.copy()
        self.run_release()
        self.assertEqual(self.github.events, events)
        with self.assertRaisesRegex(ValueError, "same Actions run"):
            self.run_release(run_id="456")

    def test_draft_target_mismatch_cannot_be_overwritten(self):
        self.github.fail_upload = True
        with self.assertRaises(RuntimeError):
            self.run_release()
        self.github.data["target_commitish"] = self.head
        events = self.github.events.copy()
        with self.assertRaisesRegex(ValueError, "different commit"):
            self.run_release()
        self.assertEqual(self.github.events, events)

    def test_bad_asset_digest_keeps_release_unpublished(self):
        self.github.corrupt_digest = True
        with self.assertRaisesRegex(ValueError, "digest"):
            self.run_release()
        self.assertTrue(self.github.data["draft"])
        self.assertNotIn("publish", self.github.events)

    def test_missing_uploaded_asset_keeps_release_unpublished(self):
        original_upload = self.github.upload

        def omit_asset(tag, paths):
            original_upload(tag, paths)
            self.github.data["assets"].pop()

        self.github.upload = omit_asset
        with self.assertRaisesRegex(ValueError, "missing or incomplete"):
            self.run_release()
        self.assertTrue(self.github.data["draft"])
        self.assertNotIn("publish", self.github.events)

    def test_build_failure_does_not_push_or_create_release(self):
        (self.root / "src/vivaalingua/assets/icon.svg").unlink()
        command(["git", "add", "-u"], self.root)
        command(["git", "commit", "-m", "Missing source fixture"], self.root)
        command(["git", "push", "origin", "main"], self.root)
        head = command(["git", "rev-parse", "HEAD"], self.root)
        with self.assertRaises(FileNotFoundError):
            self.run_release()
        self.assertEqual(command(["git", "rev-parse", "refs/heads/main"], self.origin), head)
        self.assertEqual(self.github.events, [])

    def test_new_main_commit_blocks_resume_of_an_interrupted_release(self):
        self.github.fail_upload = True
        with self.assertRaises(RuntimeError):
            self.run_release()
        (self.root / "later.txt").write_text("A later edit\n")
        command(["git", "add", "later.txt"], self.root)
        command(["git", "commit", "-m", "Later edit"], self.root)
        command(["git", "push", "origin", "main"], self.root)
        with self.assertRaisesRegex(ValueError, "same Actions run"):
            self.run_release()
        self.assertTrue(self.github.data["draft"])


    def test_concurrent_main_push_is_rejected_without_overwriting_it(self):
        other = self.parent / "other-checkout"
        command(["git", "clone", str(self.origin), str(other)])
        command(["git", "config", "user.name", "Another edit"], other)
        command(["git", "config", "user.email", "another@example.test"], other)
        original_release = self.github.release

        def advance_main(tag):
            (other / "new-edit.txt").write_text("A concurrent change\n")
            command(["git", "add", "new-edit.txt"], other)
            command(["git", "commit", "-m", "Concurrent edit"], other)
            command(["git", "push", "origin", "main"], other)
            return original_release(tag)

        self.github.release = advance_main
        with self.assertRaisesRegex(RuntimeError, "git push failed"):
            self.run_release()
        self.assertEqual(
            command(["git", "rev-parse", "refs/heads/main"], self.origin),
            command(["git", "rev-parse", "HEAD"], other),
        )
        self.assertEqual(self.github.events, [])


class GitHubResponseTests(unittest.TestCase):
    def test_only_explicit_not_found_is_treated_as_absent(self):
        github = GitHub("mattrazzo/VIVAaLingua")
        for status in ("404", "403", "500"):
            result = subprocess.CompletedProcess([], 1, stdout='{"status":"' + status + '"}', stderr="request failed")
            with self.subTest(status=status), patch("scripts.release_skill.subprocess.run", return_value=result):
                if status == "404":
                    self.assertIsNone(github.release("v1.6"))
                else:
                    with self.assertRaises(RuntimeError):
                        github.release("v1.6")


if __name__ == "__main__":
    unittest.main()
