from __future__ import annotations

import copy
import hashlib
import json
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
            "id": 7, "tag_name": tag, "draft": True, "prerelease": False, "target_commitish": commit,
            "assets": [], "html_url": f"https://example.test/releases/{tag}",
        }
        return copy.deepcopy(self.data)

    def upload(self, release, paths):
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
        return copy.deepcopy(self.data)

    def publish(self, release):
        assert self.data["draft"]
        assert len(self.data["assets"]) == 6, "All ZIPs must exist before publication"
        self.events.append("publish")
        self.data["draft"] = False
        self.tags[release["tag_name"]] = self.data["target_commitish"]
        return copy.deepcopy(self.data)


class DraftApiClient(GitHub):
    """Model draft recovery through GraphQL and a REST lookup by ID."""

    def __init__(self, backend):
        super().__init__("mattrazzo/VIVAaLingua")
        self.backend = backend
        self.tag = None

    def api(self, suffix, missing_ok=False, **kwargs):
        data = self.backend.release(self.tag)
        if suffix.startswith("releases/tags/"):
            return data if data and not data["draft"] and suffix.endswith(self.tag) else None
        if suffix == "graphql":
            return {"data": {"repository": {"release": {"databaseId": 7} if data else None}}}
        if suffix == "releases/7":
            return data
        raise AssertionError(f"Unexpected request: {suffix}")

    def tag_commit(self, tag):
        return self.backend.tag_commit(tag)

    def create_draft(self, tag, commit):
        result = self.backend.create_draft(tag, commit)
        self.tag = tag
        return result

    def upload(self, release, paths):
        return self.backend.upload(release, paths)

    def publish(self, release):
        return self.backend.publish(release)


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
        (self.root / ".gitignore").write_text((SOURCE / ".gitignore").read_text() + "__pycache__/\n")
        (self.root / "dist/latest").mkdir(parents=True)
        for platform in ("ChatGPT", "Claude", "Gemini"):
            (self.root / "dist/latest" / f"VIVAaLingua-{platform}.zip").write_bytes(b"previous published ZIP")
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
        self.assertEqual(self.github.tags["v1.6"], command(["git", "rev-parse", "HEAD^"], self.root))
        self.assertEqual(command(["git", "rev-parse", "refs/heads/main"], self.origin), head)
        changed = set(command(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"], self.root).splitlines())
        self.assertEqual(changed, {f"dist/latest/VIVAaLingua-{p}.zip" for p in ("ChatGPT", "Claude", "Gemini")})
        version_changes = set(command(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD^"], self.root).splitlines())
        self.assertEqual(version_changes, {"release/VERSION", "src/vivaalingua/SKILL.md"})
        for platform in ("ChatGPT", "Claude", "Gemini"):
            stable = self.root / "dist" / f"VIVAaLingua-{platform}.zip"
            versioned = self.root / "dist" / f"VIVAaLingua-{platform}-v1.6.zip"
            self.assertEqual(stable.read_bytes(), versioned.read_bytes())
            self.assertEqual((self.root / "dist/latest" / stable.name).read_bytes(), stable.read_bytes())
        self.assertEqual(command(["git", "status", "--porcelain", "--untracked-files=no"], self.root), "")

    def test_latest_stays_on_previous_release_until_publication_succeeds(self):
        self.github.fail_upload = True
        with self.assertRaises(RuntimeError):
            self.run_release()
        latest = self.root / "dist/latest/VIVAaLingua-ChatGPT.zip"
        self.assertEqual(latest.read_bytes(), b"previous published ZIP")
        original_publish = self.github.publish

        def publish(release):
            self.assertEqual(latest.read_bytes(), b"previous published ZIP")
            return original_publish(release)

        self.github.publish = publish
        self.run_release()
        self.assertEqual(latest.read_bytes(), (self.root / "dist/VIVAaLingua-ChatGPT.zip").read_bytes())

    def test_failed_latest_push_can_resume_without_republishing(self):
        real_command = command
        pushes = 0

        def fail_second_push(args, root=None):
            nonlocal pushes
            if args[:2] == ["git", "push"]:
                pushes += 1
                if pushes == 2:
                    raise RuntimeError("git push failed: interrupted mirror push")
            return real_command(args, root)

        with patch("scripts.release_skill.command", side_effect=fail_second_push):
            with self.assertRaisesRegex(RuntimeError, "interrupted mirror push"):
                self.run_release()
        self.assertFalse(self.github.data["draft"])
        events = self.github.events.copy()
        # A workflow rerun checks out current main, excluding the failed local commit.
        command(["git", "reset", "--hard", "origin/main"], self.root)
        self.run_release()
        self.assertEqual(self.github.events, events)
        self.assertEqual(command(["git", "rev-parse", "HEAD"], self.root),
                         command(["git", "rev-parse", "refs/heads/main"], self.origin))
        self.assertEqual((self.root / "dist/latest/VIVAaLingua-Claude.zip").read_bytes(),
                         (self.root / "dist/VIVAaLingua-Claude.zip").read_bytes())
        head = command(["git", "rev-parse", "HEAD"], self.root)
        self.run_release()
        self.assertEqual(command(["git", "rev-parse", "HEAD"], self.root), head)

    def test_created_draft_does_not_need_to_be_rediscovered(self):
        original_create = self.github.create_draft

        def create(tag, commit):
            original_create(tag, commit)
            return copy.deepcopy(self.github.data)

        def lookup(tag):
            if self.github.data is not None:
                raise AssertionError("New draft is not visible through discovery")
            return None

        self.github.create_draft = create
        self.github.release = lookup
        self.run_release()
        self.assertEqual(self.github.events, ["draft", "upload", "publish"])

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
        self.assertEqual(command(["git", "rev-parse", "HEAD^"], self.root), head)
        self.assertEqual(self.github.events.count("draft"), 1)
        self.assertEqual(self.github.events.count("publish"), 1)

    def test_failure_after_push_before_draft_creation_can_resume(self):
        self.github.fail_create = True
        with self.assertRaisesRegex(RuntimeError, "Interrupted draft"):
            self.run_release()
        head = command(["git", "rev-parse", "HEAD"], self.root)
        self.run_release()
        self.assertEqual(command(["git", "rev-parse", "HEAD^"], self.root), head)

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

        def omit_asset(release, paths):
            original_upload(release, paths)
            self.github.data["assets"].pop()
            return copy.deepcopy(self.github.data)

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

    def test_changed_skill_sources_block_resume_of_an_interrupted_release(self):
        self.github.fail_upload = True
        with self.assertRaises(RuntimeError):
            self.run_release()
        (self.root / "src/vivaalingua/later.txt").write_text("A later edit\n")
        command(["git", "add", "src/vivaalingua/later.txt"], self.root)
        command(["git", "commit", "-m", "Later edit"], self.root)
        command(["git", "push", "origin", "main"], self.root)
        with self.assertRaisesRegex(ValueError, "Package sources changed"):
            self.run_release()
        self.assertTrue(self.github.data["draft"])

    def test_automation_fix_can_resume_original_run_and_target_commit(self):
        backend = self.github
        self.github = DraftApiClient(backend)
        backend.fail_upload = True
        with self.assertRaisesRegex(RuntimeError, "Interrupted upload"):
            self.run_release()
        release_commit = command(["git", "rev-parse", "HEAD"], self.root)
        (self.root / "scripts").mkdir()
        (self.root / "scripts/release_skill.py").write_text("# Automation fix\n")
        command(["git", "add", "scripts/release_skill.py"], self.root)
        command(["git", "commit", "-m", "Fix draft lookup"], self.root)
        command(["git", "push", "origin", "main"], self.root)
        fixed_head = command(["git", "rev-parse", "HEAD"], self.root)
        self.run_release()
        self.assertEqual(backend.tags["v1.6"], release_commit)
        self.assertEqual(command(["git", "rev-parse", "HEAD^"], self.root), fixed_head)
        self.assertEqual(backend.events.count("draft"), 1)
        with self.assertRaisesRegex(ValueError, "same Actions run"):
            self.run_release(run_id="456")


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
    def test_create_upload_publish_use_response_id_and_binary_file(self):
        github = GitHub("mattrazzo/VIVAaLingua")
        draft = {"id": 17, "tag_name": "v1.6", "target_commitish": "abc", "draft": True, "assets": []}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "VIVAaLingua-Claude.zip"
            path.write_bytes(b"ZIP binary payload")
            asset = {"id": 23, "name": path.name, "state": "uploaded", "size": path.stat().st_size}
            published = {**draft, "draft": False, "assets": [asset]}
            responses = [subprocess.CompletedProcess([], 0, stdout=json.dumps(data), stderr="")
                         for data in (draft, asset, published)]
            with patch("scripts.release_skill.subprocess.run", side_effect=responses) as run:
                pending = github.create_draft("v1.6", "abc")
                uploaded = github.upload(pending, [path])
                self.assertEqual(github.publish(uploaded), published)
            calls = run.call_args_list
            self.assertEqual(len(calls), 3)
            create, upload, publish = [call.args[0] for call in calls]
            self.assertEqual(create[2], "repos/mattrazzo/VIVAaLingua/releases")
            self.assertEqual(json.loads(calls[0].kwargs["input"]), {
                "tag_name": "v1.6", "target_commitish": "abc", "name": "VIVAaLingua v1.6",
                "generate_release_notes": True, "draft": True,
            })
            self.assertEqual(upload[2], "https://uploads.github.com/repos/mattrazzo/VIVAaLingua/releases/17/assets?name=" + path.name)
            self.assertEqual(upload[upload.index("--input") + 1], str(path))
            self.assertIn("Content-Type: application/zip", upload)
            self.assertEqual(publish[2], "repos/mattrazzo/VIVAaLingua/releases/17")
            self.assertEqual(publish[publish.index("--method") + 1], "PATCH")
            self.assertEqual(json.loads(calls[2].kwargs["input"]), {"draft": False, "make_latest": "true"})

    def test_partial_draft_replaces_asset_by_id_before_binary_upload(self):
        github = GitHub("mattrazzo/VIVAaLingua")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "VIVAaLingua-Claude.zip"
            path.write_bytes(b"new ZIP")
            asset = {"id": 24, "name": path.name, "state": "uploaded", "size": 7}
            draft = {"id": 17, "draft": True, "assets": [{"id": 23, "name": path.name}]}
            responses = [subprocess.CompletedProcess([], 0, stdout="", stderr=""),
                         subprocess.CompletedProcess([], 0, stdout=json.dumps(asset), stderr="")]
            with patch("scripts.release_skill.subprocess.run", side_effect=responses) as run:
                updated = github.upload(draft, [path])
            self.assertEqual(updated["assets"], [asset])
            delete = run.call_args_list[0].args[0]
            self.assertEqual(delete[2], "repos/mattrazzo/VIVAaLingua/releases/assets/23")
            self.assertEqual(delete[delete.index("--method") + 1], "DELETE")

    def test_published_assets_cannot_be_mutated(self):
        github = GitHub("mattrazzo/VIVAaLingua")
        with patch("scripts.release_skill.subprocess.run") as run:
            with self.assertRaises(ValueError):
                github.upload({"id": 17, "draft": False}, [])
            with self.assertRaises(ValueError):
                github.publish({"id": 17, "draft": False})
            run.assert_not_called()

    def test_only_explicit_not_found_is_treated_as_absent(self):
        github = GitHub("mattrazzo/VIVAaLingua")
        for status in ("404", "403", "500"):
            result = subprocess.CompletedProcess([], 1, stdout='{"status":"' + status + '"}', stderr="request failed")
            with self.subTest(status=status), patch("scripts.release_skill.subprocess.run", return_value=result):
                if status == "404":
                    self.assertIsNone(github.api("releases/tags/v1.6", missing_ok=True))
                else:
                    with self.assertRaises(RuntimeError):
                        github.api("releases/tags/v1.6", missing_ok=True)

    def test_finds_draft_when_published_tag_endpoint_returns_404(self):
        draft = {"id": 7, "tag_name": "v1.6", "draft": True, "target_commitish": "abc", "assets": []}
        responses = [
            subprocess.CompletedProcess([], 1, stdout='{"status":"404"}', stderr="Not Found"),
            subprocess.CompletedProcess([], 0, stdout=json.dumps({"data":{"repository":{"release":{"databaseId":7}}}}), stderr=""),
            subprocess.CompletedProcess([], 0, stdout=json.dumps(draft), stderr=""),
        ]
        with patch("scripts.release_skill.subprocess.run", side_effect=responses) as run:
            self.assertEqual(GitHub("mattrazzo/VIVAaLingua").release("v1.6"), draft)
            self.assertTrue(run.call_args_list[-1].args[0][2].endswith("releases/7"))

    def test_graphql_errors_are_not_treated_as_absent(self):
        responses = [
            subprocess.CompletedProcess([], 1, stdout='{"status":"404"}', stderr="Not Found"),
            subprocess.CompletedProcess([], 0, stdout='{"errors":[{"message":"Forbidden"}]}', stderr=""),
        ]
        with patch("scripts.release_skill.subprocess.run", side_effect=responses):
            with self.assertRaises(RuntimeError):
                GitHub("mattrazzo/VIVAaLingua").release("v1.6")

    def test_absent_release_returns_none_after_graphql_null(self):
        responses = [
            subprocess.CompletedProcess([], 1, stdout='{"status":"404"}', stderr="Not Found"),
            subprocess.CompletedProcess([], 0, stdout=json.dumps({"data":{"repository":{"release":None}}}), stderr=""),
        ]
        with patch("scripts.release_skill.subprocess.run", side_effect=responses):
            self.assertIsNone(GitHub("mattrazzo/VIVAaLingua").release("v1.6"))

    def test_published_release_does_not_need_draft_lookup(self):
        published = {"id": 7, "tag_name": "v1.6", "draft": False}
        result = subprocess.CompletedProcess([], 0, stdout=json.dumps(published), stderr="")
        with patch("scripts.release_skill.subprocess.run", return_value=result) as run:
            self.assertEqual(GitHub("mattrazzo/VIVAaLingua").release("v1.6"), published)
            self.assertEqual(run.call_count, 1)

    def test_draft_lookup_permission_error_is_not_treated_as_absent(self):
        responses = [
            subprocess.CompletedProcess([], 1, stdout='{"status":"404"}', stderr="Not Found"),
            subprocess.CompletedProcess([], 1, stdout='{"status":"403"}', stderr="Forbidden"),
        ]
        with patch("scripts.release_skill.subprocess.run", side_effect=responses):
            with self.assertRaisesRegex(RuntimeError, "Forbidden"):
                GitHub("mattrazzo/VIVAaLingua").release("v1.6")


if __name__ == "__main__":
    unittest.main()
