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

    def api(self, suffix: str, missing_ok: bool = False, *, method: str = "GET",
            payload: dict | None = None, input_file: Path | None = None,
            empty_ok: bool = False) -> dict | None:
        endpoint = suffix if suffix == "graphql" or suffix.startswith("https://uploads.github.com/") else f"repos/{self.repository}/{suffix}"
        args = ["gh", "api", endpoint, "--method", method, "-H", "Cache-Control: no-cache"]
        options = {"capture_output": True, "text": True}
        if payload is not None:
            args += ["--input", "-"]
            options["input"] = json.dumps(payload)
        if input_file is not None:
            args += ["--input", str(input_file), "-H", "Content-Type: application/zip"]
        result = subprocess.run(args, **options)
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            data = None
        if result.returncode:
            if missing_ok and isinstance(data, dict) and str(data.get("status")) == "404":
                return None
            raise RuntimeError(f"GitHub request failed: {result.stderr.strip() or result.stdout.strip()}")
        if empty_ok and not result.stdout.strip():
            return None
        if not isinstance(data, dict) or not data or data.get("errors"):
            raise RuntimeError(f"GitHub returned an unexpected response: {result.stdout.strip()}")
        return data

    def release(self, tag: str) -> dict | None:
        published = self.api(f"releases/tags/{tag}", missing_ok=True)
        if published is not None:
            return published
        # Match GitHub CLI's draft lookup: GraphQL resolves a pending tag to an
        # ID even when the REST published-tag endpoint does not expose it.
        owner, name = self.repository.split("/")
        result = self.api("graphql", method="POST", payload={
            "query": "query($owner:String!,$name:String!,$tag:String!){repository(owner:$owner,name:$name){release(tagName:$tag){databaseId}}}",
            "variables": {"owner": owner, "name": name, "tag": tag},
        })
        try:
            repository = result["data"]["repository"]
            if repository is None:
                raise ValueError("Repository is inaccessible during draft lookup.")
            release = repository["release"]
            if release is None:
                return None
            release_id = release["databaseId"]
        except (KeyError, TypeError) as exc:
            raise RuntimeError("GitHub returned an invalid draft lookup response.") from exc
        return self.api(f"releases/{release_id}")

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

    def create_draft(self, tag: str, commit: str) -> dict:
        return self.api("releases", method="POST", payload={
            "tag_name": tag, "target_commitish": commit,
            "name": f"VIVAaLingua {tag}", "generate_release_notes": True, "draft": True,
        })

    def upload(self, release: dict, paths: list[Path]) -> dict:
        if not release.get("draft"):
            raise ValueError("Uploads require an unpublished draft.")
        release_id = release["id"]
        assets = {asset["name"]: asset for asset in release.get("assets", [])}
        for path in paths:
            previous = assets.get(path.name)
            if previous is not None:
                self.api(f"releases/assets/{previous['id']}", method="DELETE", empty_ok=True)
            # These controlled package filenames need no URL escaping.
            endpoint = f"https://uploads.github.com/repos/{self.repository}/releases/{release_id}/assets?name={path.name}"
            assets[path.name] = self.api(endpoint, method="POST", input_file=path)
        return {**release, "assets": list(assets.values())}

    def publish(self, release: dict) -> dict:
        if not release.get("draft"):
            raise ValueError("Publication requires an unpublished draft.")
        return self.api(f"releases/{release['id']}", method="PATCH", payload={
            "draft": False, "make_latest": "true",
        })


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


def commit_latest_packages(root: Path, aliases: list[Path], version: str) -> None:
    """Track the verified published ZIPs so a normal pull retrieves them."""
    latest = root / "dist/latest"
    latest.mkdir(parents=True, exist_ok=True)
    relative_paths = []
    for source in aliases:
        destination = latest / source.name
        shutil.copyfile(source, destination)
        relative_paths.append(str(destination.relative_to(root)))
    command(["git", "add", "--", *relative_paths], root)
    if not command(["git", "diff", "--cached", "--name-only", "--", *relative_paths], root):
        return
    command(["git", "config", "user.name", "github-actions[bot]"], root)
    command(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], root)
    command(["git", "commit", "-m", f"Update latest skill ZIPs to v{version}"], root)
    # A failed push leaves the published release intact. A fresh retry verifies
    # its assets again and finishes this commit without republishing the release.
    command(["git", "push", "origin", "HEAD:refs/heads/main"], root)


def find_run_commit(root: Path, marker: str) -> str | None:
    candidates = command([
        "git", "log", "--format=%H", "--fixed-strings",
        f"--grep={marker.splitlines()[-1]}", "HEAD",
    ], root).splitlines()
    for commit in candidates:
        if command(["git", "log", "-1", "--format=%B", commit], root) != marker:
            continue
        # Permit an automation fix to be merged before resuming, while keeping
        # the release's original package inputs and target commit unchanged.
        changed = command([
            "git", "diff", "--name-only", commit, "HEAD", "--",
            str(VERSION_FILE), "src/vivaalingua", "scripts/build_skill_packages.py",
        ], root)
        if changed:
            raise ValueError("Package sources changed since this run's version commit; inspect the unfinished release before recovery.")
        return commit
    return None


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
    retry_commit = find_run_commit(root, marker) if current == version else None
    retry = retry_commit is not None
    if not retry and parse_version(version) <= parse_version(current):
        raise ValueError(f"Version {version} must be greater than {current}; only the same Actions run may resume its release commit.")
    commit = retry_commit or commit

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
        commit_latest_packages(root, aliases, version)
        return existing["html_url"]
    pending = existing if existing is not None else github.create_draft(tag, commit)
    if (pending is None or not pending.get("draft") or pending.get("target_commitish") != commit
            or pending.get("tag_name") != tag or not isinstance(pending.get("id"), int)):
        raise ValueError("Asset uploads require this run's unpublished draft.")
    draft = github.upload(pending, paths)
    if (draft is None or not draft.get("draft") or draft.get("target_commitish") != commit
            or draft.get("id") != pending["id"] or draft.get("tag_name") != tag):
        raise ValueError("Expected an unpublished draft targeting the release commit.")
    verify_assets(draft, paths)
    published = github.publish(draft)
    if published is None or published.get("draft") or published.get("prerelease"):
        raise ValueError("Release publication did not complete.")
    if published.get("id") != draft["id"] or published.get("tag_name") != tag:
        raise ValueError("Published release tag does not match the requested version.")
    if github.tag_commit(tag) != commit:
        raise ValueError("Published tag does not match the release commit.")
    verify_assets(published, paths)
    commit_latest_packages(root, aliases, version)
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
            stream.write(f"Published [VIVAaLingua {args.version}]({url}) with all six ZIP assets and the three current ZIPs committed in `dist/latest/`.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
