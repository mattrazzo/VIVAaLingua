# Releasing VIVAaLingua Skills

Use the **Release VIVAaLingua** workflow after your finished edits reach `main`. Entering a version and starting the workflow authorizes publication of that version. A normal push saves your changes without starting a product release.

## Edit and Release Through GitHub Desktop

1. Select the VIVAaLingua repository and the `main` branch. Click **Fetch origin**, then **Pull origin** if offered.
2. Open the file in your editor, make your changes, and save it. Leave the version numbers for the release workflow to update.
3. In GitHub Desktop, review **Changes**, enter a commit summary, and click **Commit to main**.
4. Click **Push origin**. If you prefer to work on a branch, publish the branch and merge its PR into `main` first.
5. Open the [Release VIVAaLingua workflow page](https://github.com/mattrazzo/VIVAaLingua/actions/workflows/release.yml) in your browser.
6. Above the previous runs, click **Run workflow**. Select `main`, enter the next version without `v`, and click the green **Run workflow** button.
7. Open the new run. When it succeeds, return to GitHub Desktop, click **Fetch origin**, and then **Pull origin**. The three latest ZIPs are now in `dist/latest/` inside your local repository folder.

Before your next local edit, fetch and pull `main` again. The workflow creates a version commit and a ZIP update commit on GitHub, which your local copy needs.

## Edit and Release Through GitHub’s Website

1. Open the repository on `main`, open a file, and click its pencil icon.
2. Make the change, preview it, and click **Commit changes**. Commit directly to `main`, or create a branch and merge its PR first.
3. Open **Actions → Release VIVAaLingua → Run workflow**. Keep `main` selected, enter the next version without `v`, and click the green **Run workflow** button.
4. Check that the run succeeds and the release contains all six ZIP assets.

The workflow replaces **Prepare version bump** and **Package published skill release**. You no longer merge a generated version PR, create a release tag, or fill out a separate release form. README and documentation edits are published by committing them to `main`. Run a release when you want updated skill packages.

## What the Workflow Does

The workflow runs the automated tests, validates the requested version, updates `release/VERSION` and the installed version in `src/vivaalingua/SKILL.md`, and builds the three platform packages. It adds identical copies under stable filenames, then commits and pushes only the two version files to `main`.

It creates a draft release targeting that version commit, uploads all six ZIPs, verifies their names, sizes, upload status, and SHA-256 digests when GitHub supplies them, then publishes the release and marks it as latest. Automatic release notes describe changes since the previous release. After publication is verified, it copies the three stable ZIPs into `dist/latest/`, commits them to `main`, and pushes that commit. Those files are byte-for-byte copies of the published assets. Normal builds elsewhere in `dist/` remain ignored. Each release replaces the same three filenames, while Git retains prior copies in its history.

The version must increase and use two or three numeric components, such as `1.6` or `1.5.3`. Leading zeroes, a `v` prefix, existing tags, and mismatched version sources are rejected. One concurrency group prevents overlapping release runs. A concurrent push to `main` causes the version push to fail without overwriting the other change.

## If a Run Fails

A failed build publishes nothing. If an upload fails, its release remains a draft, the previous release stays latest, and `dist/latest/` keeps the previous published ZIPs. If publication succeeds but the final ZIP commit or push fails, the new release is already public. Re-run the same job to verify its published assets and finish updating `dist/latest/`. A rejected push does not overwrite concurrent edits to `main`.

Open the failed run and choose **Re-run all jobs** to retry with the original version input. The same Actions run can resume its own version commit and unfinished draft. It checks an already completed release and finishes any missing `dist/latest/` update without replacing published assets. Starting a new workflow with the same version is rejected.

The same run can also resume after an automation or documentation fix is merged into `main`. It finds its original version commit and requires the skill sources, `release/VERSION`, and package builder to match that commit. The release still targets the original version commit. If those package inputs have changed, the workflow stops for inspection. It also stops if an existing draft or tag points to a different commit.

## Permanent Downloads and Version Data

Website buttons can use:

- ChatGPT: https://github.com/mattrazzo/VIVAaLingua/releases/latest/download/VIVAaLingua-ChatGPT.zip
- Claude: https://github.com/mattrazzo/VIVAaLingua/releases/latest/download/VIVAaLingua-Claude.zip
- Gemini: https://github.com/mattrazzo/VIVAaLingua/releases/latest/download/VIVAaLingua-Gemini.zip

Each release also keeps versioned filenames. The stable URLs become usable after a release containing those files succeeds. The website is updated separately in Sites.

`release/VERSION` contains only a number and a newline. Its raw URL is https://raw.githubusercontent.com/mattrazzo/VIVAaLingua/main/release/VERSION. It tracks `main` and can advance before publication. For the latest published version, read `tag_name` from https://api.github.com/repos/mattrazzo/VIVAaLingua/releases/latest and remove the leading `v`.

## Permissions and Validation

The workflow needs GitHub Actions enabled and `contents: write` for its built-in token. Repository rules must allow its version and ZIP commits to reach `main`. It does not create PRs or require the Actions setting for creating and approving PRs.

The tests exercise real Git commits and pushes to temporary repositories, real ZIP builds, and simulated GitHub releases. They cover interrupted uploads, retries, invalid versions, conflicting tags, asset checks, and concurrent source changes. Passing these checks does not establish platform import acceptance, teaching accuracy, or audio accent.
