#!/usr/bin/env python3
"""Build and publish one release from main, with retries scoped to its Actions run."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

try:
    from .build_skill_packages import build_packages
    from .update_version import SKILL_FILE, VERSION_FILE, coordinated_version, parse_version, update_version
except ImportError:
    from build_skill_packages import build_packages
    from update_version import SKILL_FILE, VERSION_FILE, coordinated_version, parse_version, update_version


def command(args: list[str], root: Path | None = None) -> str:
    result = subprocess.run(args, cwd=root, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"{args[0]} {args[1]} failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


class GitHub:
    def __init__(self, repository: str):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("Expected an owner/repository name.")
        self.repository = repository

    def api(self, suffix: str, missing_ok: bool = False) -> dict | None:
        result = subprocess.run(
            ["gh", "api", f"repos/{self.repository}/{suffix}"], capture_output=True, text=True
        )
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            data = {}
        if result.returncode:
            if missing_ok and str(data.get("status")) == "404":
                return None
            raise RuntimeError(f"GitHub request failed: {result.stderr.strip() or result.stdout.strip()}")
        if not isinstance(data, dict) or not data:
            raise RuntimeError("GitHub returned an unexpected response.")
        return data

    def release(self, tag: str) -> dict | None:
        return self.api(f"releases/tags/{tag}", missing_ok=True)

    def tag_commit(self, tag: str) -> str | None:
        ref = self.api(f"git/ref/tags/{tag}", missing_ok=True)
        if ref is None:
            return None
        target = ref["object"]
        for _ in range(10):
            if target["type"] == "commit":
                return target["sha"]
            if target["type"] != "tag":
                break
            target = self.api(f"git/tags/{target['sha']}")["object"]
        raise ValueError("The release tag does not resolve to a commit.")

    def create_draft(self, tag: str, commit: str) -> None:
        command([
            "gh", "release", "create", tag, "--repo", self.repository,
            "--target", commit, "--title", f"VIVAaLingua {tag}", "--generate-notes", "--draft",
        ])

    def upload(self, tag: str, paths: list[Path]) -> None:
        command([
            "gh", "release", "upload", tag, "--repo", self.repository,
            "--clobber", *[str(path) for path in paths],
        ])

    def publish(self, tag: str) -> None:
        command(["gh", "release", "edit", tag, "--repo", self.repository, "--draft=false", "--latest"])


def verify_assets(release: dict, paths: list[Path]) -> None:
    assets = {asset["name"]: asset for asset in release.get("assets", [])}
    for path in paths:
        asset = assets.get(path.name)
        if asset is None or asset.get("state") != "uploaded" or asset.get("size") != path.stat().st_size:
            raise ValueError(f"Release asset is missing or incomplete: {path.name}")
        digest = asset.get("digest")
        expected = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if digest and digest != expected:
            raise ValueError(f"Release asset digest does not match: {path.name}")


def release_skill(root: Path, version: str, run_id: str, github: GitHub) -> str:
    parse_version(version)
    if not run_id.isdigit():
        raise ValueError("An Actions run ID is required for retry tracking.")
    if command(["git", "branch", "--show-current"], root) != "main":
        raise ValueError("Release only from main.")
    command(["git", "diff", "--quiet"], root)
    command(["git", "diff", "--cached", "--quiet"], root)
    commit = command(["git", "rev-parse", "HEAD"], root)
    if commit != command(["git", "rev-parse", "origin/main"], root):
        raise ValueError("The checkout must match origin/main before releasing.")

    current = coordinated_version(root)
    marker = f"Release VIVAaLingua {version}\n\nGitHub-Actions-Run: {run_id}"
    retry = current == version and command(["git", "log", "-1", "--format=%B"], root) == marker
    if not retry and parse_version(version) <= parse_version(current):
        raise ValueError(f"Version {version} must be greater than {current}; only the same Actions run may resume its release commit.")

    tag = f"v{version}"
    existing = github.release(tag)
    tagged_commit = github.tag_commit(tag)
    if not retry and (existing is not None or tagged_commit is not None):
        raise ValueError(f"Tag or release {tag} already exists; choose an unused version.")
    if retry and tagged_commit is not None and tagged_commit != commit:
        raise ValueError("The existing tag points to a different commit.")
    if retry and existing is not None and existing.get("draft") and existing.get("target_commitish") != commit:
        raise ValueError("The existing draft targets a different commit.")

    if not retry:
        update_version(root, version)
    paths = build_packages(root, root / "dist", release_tag=tag)
    aliases = []
    for path in paths:
        alias = path.with_name(path.name.removesuffix(f"-{tag}.zip") + ".zip")
        shutil.copyfile(path, alias)
        aliases.append(alias)
    paths += aliases

    if not retry:
        changed = set(command(["git", "diff", "--name-only"], root).splitlines())
        if changed != {str(VERSION_FILE), str(SKILL_FILE)}:
            raise ValueError("Expected only the two coordinated version files to change.")
        command(["git", "config", "user.name", "github-actions[bot]"], root)
        command(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], root)
        command(["git", "add", "--", str(VERSION_FILE), str(SKILL_FILE)], root)
        command(["git", "commit", "-m", marker], root)
        commit = command(["git", "rev-parse", "HEAD"], root)
        # A normal push rejects concurrent changes to main instead of overwriting them.
        command(["git", "push", "origin", "HEAD:refs/heads/main"], root)

    if existing is not None and not existing.get("draft"):
        if tagged_commit != commit:
            raise ValueError("The published release does not match this run's commit.")
        verify_assets(existing, paths)
        return existing["html_url"]
    if existing is None:
        github.create_draft(tag, commit)
    pending = github.release(tag)
    if pending is None or not pending.get("draft") or pending.get("target_commitish") != commit:
        raise ValueError("Asset uploads require this run's unpublished draft.")
    github.upload(tag, paths)
    draft = github.release(tag)
    if draft is None or not draft.get("draft") or draft.get("target_commitish") != commit:
        raise ValueError("Expected an unpublished draft targeting the release commit.")
    verify_assets(draft, paths)
    github.publish(tag)
    published = github.release(tag)
    if published is None or published.get("draft") or published.get("prerelease"):
        raise ValueError("Release publication did not complete.")
    if github.tag_commit(tag) != commit:
        raise ValueError("Published tag does not match the release commit.")
    verify_assets(published, paths)
    return published["html_url"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Next MAJOR.MINOR or MAJOR.MINOR.PATCH without v")
    args = parser.parse_args()
    try:
        github = GitHub(os.environ.get("GITHUB_REPOSITORY", ""))
        url = release_skill(Path(__file__).resolve().parents[1], args.version, os.environ.get("GITHUB_RUN_ID", ""), github)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    print(f"Release ready: {url}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as stream:
            stream.write(f"Published [VIVAaLingua {args.version}]({url}) with all six ZIP assets.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
