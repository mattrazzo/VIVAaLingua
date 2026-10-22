# VIVAaLingua Regression Cases (Development Only)

This is a test checklist, **not** a learner-facing format or an instruction to reproduce fixed translations. Evaluate **structural compliance and linguistic correctness separately**. Real outputs may vary in explanatory wording across ChatGPT, Claude, and Gemini.

## Format and Rendering Tests

1. **EP: I drove to see João.** Expect Phrase or Sentence Primary Entry with exactly five consecutive labeled list items, followed by Learning notes and triggered Tongue and lip position. Pronunciation must preserve `‿`, `˜`, `·`, and visible ` | ` between careful written words. Check the copied raw Markdown: no `| --- |` alignment row in the five-field block; source bars are written `\|`.
2. **PE: Fui de carro ver o João.** Same variant and field count. Literal-gloss slots must align to six Portuguese words, in order: Fui / de / carro / ver / o / João; each English slot remains one gloss (hyphenated if needed). Do not simply repeat the input English or give only a natural translation.
3. **PE: carro** Expect Single Word, four compact labeled list items including masculine noun, with correct strong rr. No fifth Common Pronunciation field is required. Articulation may be added where useful.
4. **PE: mãe** Expect Single Word with nasal `˜`, no final English n or m in respelling, and mandatory nasal articulation guidance.
5. **EP: eight thirty** Expect appropriate PT-PT target and correct entry variant. Verify final line fields without extra blank paragraphs.
6. **Give a vocabulary table for caro, carro, mãe.** Expect a genuine table with Portuguese / Pronunciation / English/Meaning. Comparison of caro and carro should distinguish the tap R and strong R; real table delimiters are valid in these variants.
7. **Compare passear, caminhar, andar a pé.** Expect Comparison Primary Entry. Multiword `andar a pé` receives accurate pronunciation and helpful literal mapping adjacent to its comparison entry, without a huge repeated five-line layout in each cell.
8. **PE: a sentence of two or more clauses** Expect Phrase or Sentence for one complete sentence, and Long Passage for connected multiple-sentence prose or paragraphs. No omission of supplied content.
9. **HELP: vivaalingua** Expect full command help, installed version 1.4, and live-version reporting based strictly on a fresh retrieval or stated tool limitation. **HELP: EP** explains only EP; bare **HELP** remains invalid under this skill's established policy.
10. **QUIZ: Portuguese demonstratives** Expect one quiz question without prematurely exposing the target translation/pronunciation. Test reveal after an answer.
11. **CHAT: ordering in a tasca** Expect conversational PT-PT turns without full glossary on every turn. Target-specific teaching upon request obeys its variant.
12. **AUDIO: trazer** When a playable PT-PT card is supported, request `pronunciation_language=pt-PT`; card is supplemental to full output. Do not speak English respelling.

## Root-Cause Reproduction: Markdown Pipes

**Bad source (the user's copied failing output, reduced):**

```markdown
| **Pronunciation:** FOO‿EE | dih | KAH·rroo | VAYr | oo | zhoo·AH‿OO˜ |
|--------|--------|--------|--------|--------|--------|
```

This is a six-column Markdown table, and the renderer spreads the columns horizontally. The literal `|` symbols are interpreted as table columns because a following delimiter row declares a table. This **does not** establish that all visible pipes are problematic in normal lines.

**Working source for two field items (excerpt only, not a complete Primary Entry):**

```markdown
- **Pronunciation:** FOO‿EE \| dih \| KAH·rroo \| VAYr \| oo \| zhoo·AH‿OO˜
- **Literal structure:** I-went \| by \| car \| to-see \| the \| João
```

Escapes display as pipes while remaining safe in a list-based field and in a Markdown table cell. Do not put escaped bars inside inline-code spans; the backslash would remain visible.

## Scorecard

**Structure (pass/fail):** correct variant, required field count/order, Markdown rendering, separators, distinct notes/articulation/audio, mode restrictions.

**Linguistics (pass/fail):** correct PT-PT idiom, source-word alignment, natural English, genuine IPA-to-respelling correspondence, stress, diphthong/tilde/R, verified natural linking.

A passing ZIP validation only establishes package syntax and path integrity. It **cannot** prove actual model compliance or audio accent. Manually run these cases in each target platform after installation.

## Batch 1 Presentation Regression

- **EP: I took a cake to João.** Expect five consecutive labeled list items including **Literal structure** and **Common Pronunciation**. No table delimiter row in the entry. When unchanged, Common Pronunciation reads `No meaningful difference from the standard pronunciation.`
- **PE: um** Expect **Learning notes** heading in sentence case, and when a complete pronunciation example appears in an explanatory bullet, show `[OO˜]` as plain text rather than inline code or math. An isolated notation symbol such as `˜` may still use inline code.
- **EP: I drove to see João.** When common speech links **ver o**, bold the changed segment only, e.g. `**VAY·roo**`; retain other separators as visible pipes.

These are manual behavioral tests, not proofs of compliance based on ZIP validation.

- **Five-field serialization failure regression:** For `EP: I took a cake to João.`, inspect raw output. The five fields must each begin with `- **`, including `- **Literal structure:**`; no field may begin with `|`, no table alignment row (`| --- |`) may appear, and Common Pronunciation must not share a line with Natural English.

## Consolidation Verification

The authoritative response rules now reside in [SKILL.md](../SKILL.md#response-architecture). Use this file only for development checks, not during ordinary translation or coaching.

- Confirm that the Single Word canonical example renders four list items and the Phrase or Sentence example renders five. Both require bold labels and one field per item.
- Confirm that vocabulary/comparison tables still render as tables, with escaped pronunciation bars kept inside their intended cells.
- Check that all former Response Contract links resolve to the corresponding SKILL.md headings and that the retired response-contract.md file is absent.
- Check exact no-difference wording, Common Pronunciation highlighting, sentence-case Learning notes, and plain square-bracket respellings in explanatory prose.
- Keep version 1.4, existing command routing, HELP behavior, UI metadata, icon, and linguistic calibration data unchanged. Test model behavior separately from these static checks.

## iOS Pronunciation Typography Regression

- **EP: I took a cake to João.** Run in a fresh iOS Chat Instant conversation and compare with macOS Chat Instant. Expect a five-item list, no table, no omitted Literal structure, and text such as `[OO˜]` and `[zhoo·AH‿OO˜]` displayed in the ordinary prose font in articulation notes. Check the **actual rendered UI** as well as copied source: no math italics or misplaced symbol spacing.
- Reject raw escaped-bracket math delimiters such as `\[OO˜\]` or `\( ... \)`, unnecessary escaped labels/punctuation such as `**Pronunciation\:**` and `\.`, and HTML pipe entities `&#124;` or `&vert;`. Expect visible ` | ` bars in learner output, represented in Markdown source as ` \| `.
- Preserve actual Markdown emphasis around labels and changed Common Pronunciation segments. Never convert complete respelling examples to inline code, math, italics, or HTML while fixing this issue.
- A syntactically valid ZIP cannot validate actual iOS rendering. Record the installed skill version, client, model setting, and screenshot when doing the manual test.

## Namespaced Commands Regression

- **VIVAaLingua: help**: Expect the full guide with the installed version and a fresh version retrieval or accurate unavailable-tool message.
- **VIVAaLingua: help PE**: Expect only command-specific help, with no version retrieval.
- **VIVAaLingua: help command**: Expect a short explanation of command syntax and available commands.
- **VIVAaLingua: test cases**: Expect a short list of prompts quoted accurately from this file (e.g., `EP: I took a cake to João.`, `EP: I drove to see João.`, `PE: Fui de carro ver o João.`, `PE: carro`, `Compare passear, caminhar, andar a pé.`). Do not execute those prompts, expose their expected answers, or run an update check.
- Confirm legacy `HELP: vivaalingua`, `HELP: EP`, and bare `HELP` retain their former behaviors.
