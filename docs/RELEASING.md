# Releasing VIVAaLingua skills

The repository version is managed in two places: `release/VERSION` and the Installed version field in `src/vivaalingua/SKILL.md`. The automation checks that they agree before packaging. `release/VERSION` contains only the version number on one line, such as `1.5.1`, followed by a newline. It has no heading, `v` prefix, or download URL.

The raw source URL is https://raw.githubusercontent.com/mattrazzo/VIVAaLingua/main/release/VERSION. Consumers must read the entire trimmed response as the version number rather than searching for a `Latest version:` label. This URL tracks the version on `main`, which may be ahead of the latest published release. A check intended to report published updates should use the latest GitHub Release metadata instead.

## Prepare the next version

1. Open the repository’s **Actions** tab and select **Prepare version bump**.
2. Select **Run workflow**, keep the `main` branch selected, enter the next version (`1.6` or `1.5.1` are valid examples), and run it.
3. Review the pull request opened or updated by the workflow. Merge it only after confirming both version fields changed together.

The version must be greater than the current version. Two-part and three-part numeric versions are supported. A `v` prefix, leading zeroes, malformed values, and non-increasing versions fail before a pull request is created. The workflow uses one shared concurrency group so two version bump runs cannot edit the same PR at once.

## Publish and package the release

After merging the version pull request:

1. In **Releases**, choose **Draft a new release**.
2. Create a tag exactly matching the merged version, with a `v` prefix, such as `v1.6`. Choose the commit on `main` that contains the merged version change as the tag target.
3. Publish the release. Do not publish a tag-only release or create the release before merging the version PR.
4. The **Package published skill release** workflow checks that the tag, version file, and `SKILL.md` all agree. It then builds and attaches the ChatGPT, Claude, and Gemini ZIP files.

The files are built in `dist/` and uploaded as release assets. They are ignored by Git and are not committed to the repository. Package paths are based on the known-good archives in `release/`: ChatGPT and Claude have a `vivaalingua/` wrapper, Gemini has `SKILL.md` at the ZIP root, and only ChatGPT includes `agents/openai.yaml`. All four references are included, matching the existing packages. System metadata such as `.DS_Store` and `__MACOSX` is excluded.

## Permanent Download Links

Every successful release build uploads six assets: one versioned ZIP and one identical copy with a stable filename for each platform. The release steps above stay the same.

Use these permanent URLs for website download buttons:

- ChatGPT: https://github.com/mattrazzo/VIVAaLingua/releases/latest/download/VIVAaLingua-ChatGPT.zip
- Claude: https://github.com/mattrazzo/VIVAaLingua/releases/latest/download/VIVAaLingua-Claude.zip
- Gemini: https://github.com/mattrazzo/VIVAaLingua/releases/latest/download/VIVAaLingua-Gemini.zip

GitHub redirects each URL to the matching asset in the latest release. Keep the stable filenames unchanged across releases. Versioned filenames remain available for downloads pinned to a particular release.

Merge this workflow update before creating the next release tag. These links become usable after a release containing this workflow finishes packaging, or after identical stable-name copies are added to the current release once. Existing releases do not gain assets when this PR is merged, and rerunning an older release workflow uses its older workflow revision.

Before switching the website from Google Drive, confirm that all three permanent URLs download ZIPs. On later releases, wait for **Package published skill release** to succeed before announcing downloads. There can be a short interval between publication and attachment of the assets.

The website links are updated separately in Sites. No Google Drive copy is needed for future releases using these links.

## Required repository setting

For the version workflow to open or update a pull request with the built-in `GITHUB_TOKEN`, enable **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**. The workflow grants only `contents: write` and `pull-requests: write`. GitHub’s workflow dispatch policy must also allow manual dispatch. The setting is at [Settings → Actions → General](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository). If the repository or organization disables Actions, restricts dispatch events, or overrides token permissions, an administrator must adjust that policy.

## Checks and limitations

The workflows validate versions and packaging structure. They also reject release tags whose commit is not reachable from `main`. Current workflow actions use `actions/checkout@v7`, `actions/setup-python@v7`, `peter-evans/create-pull-request@v8`, and `softprops/action-gh-release@v3`. Static ZIP checks cannot confirm that every import surface accepts the packages or that the skill behaves correctly in ChatGPT, Claude, or Gemini. The existing archives establish the project’s current package conventions; platform import behavior can still vary by account, product surface, and current platform policy.
