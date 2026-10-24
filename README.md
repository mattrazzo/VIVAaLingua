# VIVAaLingua

European Portuguese coaching for English speakers, built for everyday life in Portugal.

VIVAaLingua is a skill for your AI assistant. It combines translation, readable pronunciation, grammar, and practice, with explanations in American English. Its teaching target is contemporary European Portuguese (PT-PT), centered on the Lisbon–Coimbra standard, with regional differences explained when useful.

[Website](https://language.vivatools.pt/) · [How to Use](https://language.vivatools.pt/how-to-use.html) · [Installation Guide](https://language.vivatools.pt/get-vivaalingua.html) · [Latest Release](https://github.com/mattrazzo/VIVAaLingua/releases/latest)

## What You Can Do

- **Translate with context.** Move between English and European Portuguese while preserving meaning, tone, and politeness.
- **Work on pronunciation.** Use familiar American English sound references, stress markers, and guidance for your tongue and lips.
- **Understand everyday speech.** Compare careful pronunciation with common spoken forms, including reduced vowels and connected speech.
- **Learn through short lessons.** Explore grammar, vocabulary, idioms, and usage through practical examples.
- **Test what you know.** Answer focused quiz questions, with answers withheld until you try.
- **Rehearse conversations.** Practice situations such as ordering coffee, making an appointment, or returning a purchase, with corrections suited to your level.
- **Prepare to listen.** Explore what another person might say and how to recognize their reply.

## Get Started

You need a ChatGPT, Claude, or Gemini account with skill uploads available.

1. Open the [latest GitHub Release](https://github.com/mattrazzo/VIVAaLingua/releases/latest) and download the ZIP named for your platform: ChatGPT, Claude, or Gemini.
2. Keep the file zipped and follow the matching steps in the [installation guide](https://language.vivatools.pt/get-vivaalingua.html).
3. Start a new chat, invoke the skill as described in the guide, and ask for help with a word, phrase, or situation.

Commands are optional. You can ask naturally:

```text
Teach me the difference between ser and estar using practical examples.
```

Or use a short command to set the task.

## Commands

| Command | Purpose | Example |
| --- | --- | --- |
| `EP` | English to European Portuguese | `EP: I work at home.` |
| `PE` | Portuguese to American English | `PE: Onde fica a tua casa?` |
| `TUTOR` | A compact lesson | `TUTOR: reflexive verbs` |
| `QUIZ` | Practice one question at a time | `QUIZ: family vocabulary` |
| `CHAT` | Conversation practice | `CHAT: ordering at a café` |
| `HEAR` | Prepare for what you might hear | `HEAR: at the pharmacy` |
| `AUDIO` | Add playable pronunciation audio where supported | `AUDIO: espreguiçadeiras` |

Commands are case-insensitive. A colon, dash, or space can separate the command from the request.

Use `VIVAaLingua: help` for the full guide and version-check status, or `VIVAaLingua: help PE` for help with one command. Full help attempts a fresh update check when live web reading is available. Updates are downloaded and installed manually.

## What a Response Includes

For a phrase or sentence, the standard response brings together:

1. **European Portuguese:** the correctly spelled target.
2. **Pronunciation:** a careful pronunciation guide.
3. **Literal structure:** an English gloss for each Portuguese word, in order.
4. **Natural English:** the meaning in ordinary American English.
5. **Common Pronunciation:** a useful everyday spoken form, or a statement that there is no meaningful difference.

Learning notes explain grammar and usage. Tongue and lip guidance appears when a sound needs it. Single words include meaning and grammatical information, such as noun gender or verb form. Vocabulary lists, comparisons, longer passages, and practice modes use formats suited to the task.

### Reading the Pronunciation

The notation uses English sound approximations with a few extra marks:

- Capitals mark stress.
- `·` separates syllables within a word.
- A vertical bar, ` | `, separates written words in the careful pronunciation.
- `‿` joins vowel positions within one syllable.
- `˜` marks nasal resonance, without adding an English n, m, or ng sound.

English approximations cannot reproduce every Portuguese sound. Use them alongside listening and mouth-position guidance. Playable audio and voice features depend on the host platform, and their availability does not guarantee the accent is correct.

## Repository Structure

```text
src/vivaalingua/
  SKILL.md             Skill instructions and response rules
  references/          Coaching, pronunciation, help, and regression cases
  assets/              Skill icon
  agents/openai.yaml   OpenAI interface metadata
scripts/               Version management and ZIP packaging
tests/                 Automated release and package checks
.github/workflows/     Version PR and release packaging workflows
docs/RELEASING.md      Maintainer release instructions
release/               Previously stored package ZIPs
VIVAaLingua Version.txt
LICENSE.md
```

The [skill instructions](src/vivaalingua/SKILL.md) define command routing and response formats. Edit the source under `src/vivaalingua/`. New builds go into the ignored `dist/` directory and are attached to GitHub Releases without committing generated ZIPs.

## Local Builds and Checks

Use Python 3.13 to match GitHub Actions. The packaging tools use the Python standard library.

From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_skill_packages.py
```

The builder creates one ZIP per platform. ChatGPT and Claude use a `vivaalingua/` wrapper. Gemini puts `SKILL.md` at the ZIP root. Only ChatGPT includes `agents/openai.yaml`.

Automated checks cover version validation, archive contents, and reproducible builds. They do not establish platform import acceptance or teaching accuracy. Use the [manual regression cases](src/vivaalingua/references/regression-tests.md) to assess responses in each platform.

## Preparing a Release

1. Run **Prepare version bump** from the repository’s Actions tab on `main`, entering a higher version such as `1.6` or `1.5.2`.
2. Review and merge the generated PR, which updates `VIVAaLingua Version.txt` and the installed version in `SKILL.md`.
3. Publish a GitHub Release with the matching tag, such as `v1.6`, targeting the merged version commit.
4. **Package published skill release** validates the versions, builds the three ZIPs, and attaches them automatically.

See [Releasing VIVAaLingua Skills](docs/RELEASING.md) for repository settings and the full procedure.

## License

VIVAaLingua is available under the [VIVAaLingua Personal Use License](LICENSE.md). It permits free personal, noncommercial use, modification, and sharing subject to its conditions. Commercial use requires prior written permission from Daniel Mattrazzo.
