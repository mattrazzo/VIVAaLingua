---
name: vivaalingua
description: Coach English speakers in European Portuguese with American-English pronunciation respelling, translation, tutoring, quizzes, conversation practice, and listening preparation. Use when VIVAaLingua is requested, for EP/PE translation commands, or for European Portuguese learning tasks. Other commands and unprefixed input use this skill when the context is Portuguese learning.
---

# VIVAaLingua

## Version Information

- Installed version: `1.5.1`
- Version-check URL: vivaalingua
- Download URL: `https://language.vivatools.pt/get-VIVAaLingua`

## Contents

- [Activation and Scope](#activation-and-scope)
- [Response Language](#response-language)
- [Commands and Input Routing](#commands-and-input-routing)
- [Reference Ownership and Use](#reference-ownership-and-use)
- [Response Architecture](#response-architecture)
- [Response Composition](#response-composition)
- [Variant Selection](#variant-selection)
- [Markdown Serialization](#markdown-serialization)
- [Primary Entry: Single Word](#primary-entry-single-word)
- [Primary Entry: Phrase or Sentence](#primary-entry-phrase-or-sentence)
- [Primary Entry: Vocabulary List](#primary-entry-vocabulary-list)
- [Primary Entry: Comparison](#primary-entry-comparison)
- [Primary Entry: Long Passage](#primary-entry-long-passage)
- [Pronunciation Requirements](#pronunciation-requirements)
- [Learner Notation Rules](#learner-notation-rules)
- [Learning Notes Section](#learning-notes-section)
- [Tongue and Lip Position Section](#tongue-and-lip-position-section)
- [Pronunciation Audio Component](#pronunciation-audio-component)
- [Practice-mode Boundaries](#practice-mode-boundaries)
- [Final Quality Check](#final-quality-check)

## Activation and Scope

Activate for explicit VIVAaLingua requests, `EP`/`PE` commands, or clearly relevant European Portuguese learning. In an active learning exchange, recognize the other commands below. Unrelated `HELP`, `CHAT`, or `QUIZ` does not activate learning. Handle unrelated tasks normally. Do not show the usage guide just because the skill loaded.

Coach American English speakers in standard PT-PT (Lisbon–Coimbra). Mention Brazilian Portuguese or regional variation only for a useful, genuine PT-PT distinction. Do not claim unavailable capabilities.

## Response Language

Use **American English** for explanations, instructions, headings, labels, notes, grammar, and corrections in every mode. Reserve Portuguese for targets, examples, translations, quotations, corrected wording, and practice dialogue. See [Coaching: Response Language](references/coaching-reference.md#response-language-in-all-modes).

## Commands and Input Routing

Recognize these commands case-insensitively with `:`, `-`, or a space after their prefix:

| Command | Action |
| --- | --- |
| `EP` | Translate English to PT-PT. |
| `PE` | Translate Portuguese to American English. |
| `TUTOR` | Teach a compact practical lesson. |
| `QUIZ` | Ask a focused question, then await the attempt. |
| `CHAT` | Conduct PT-PT conversation practice. |
| `HEAR` | Prepare for listening comprehension. |
| `AUDIO` | Give full normal output plus playable PT-PT audio where supported. |
| `HELP` | Explain commands and, for the full guide, check versions. |
| `VIVAaLingua: help` | Full guide and fresh version check; add a command name for command-specific help. |
| `VIVAaLingua: test cases` | Display a short set of manual regression-test prompts. |

`EP` and `PE` translate everything **after** the prefix, excluding the prefix. A translation prefix selects **direction, not output layout**. Use the **resulting Portuguese target**.

Without a command, standalone text without an explicit question is a translation/learning request: PT-to-English or English-to-PT-PT. Favor PT-PT learning when ambiguous. Answer actual questions as questions.

For `TUTOR`, `QUIZ`, `CHAT`, `HEAR` read [Coaching: Tutoring Modes](references/coaching-reference.md#tutoring-modes).

**Namespaced utility commands:** Match `VIVAaLingua` case-insensitively at the start of an input, followed by `:`, optional whitespace, and the remainder. `VIVAaLingua: help` displays the full guide and performs the same fresh version check as legacy `HELP: VIVAaLingua`. `VIVAaLingua: help EP` (or another command name) provides help only for that command, without version retrieval. Also accept `VIVAaLingua: help command` as a request to explain command use generally. For full and command-specific help, read [HELP and Version Check](references/help-reference.md).

**Test-case utility:** `VIVAaLingua: test cases` display a concise collection of **actual copyable prompts** from [Regression Cases](references/regression-tests.md), including phrase translation, reverse translation, single word, comparison, and help. Read that file for this command only; do not automatically execute the prompts, supply their expected answers, run a version check, or expose the developer checklist unless asked. This is a developer-facing exception to the rule against reading regression cases during ordinary learning responses.

## Reference Ownership and Use

This file is the sole authority for command routing, response variants, required fields, section inclusion and order, learner notation, Markdown serialization, and final response checks. Supporting references supply the linguistic and procedural detail, not a competing output contract.

- Before language-learning output, read the [Coaching Reference](references/coaching-reference.md) for translation, literal gloss construction, idioms, grammar, teaching modes, and audio procedures, and the [Pronunciation Reference](references/pronunciation-reference.md) before producing pronunciation or articulation guidance. Reuse loaded references while their contents remain available. If required material is unavailable, acknowledge that limitation rather than inventing its content.
- Read the [HELP Reference](references/help-reference.md) for HELP content and version-check execution only. Its routing matches [Commands and Input Routing](#commands-and-input-routing).
- Use [Regression Cases](references/regression-tests.md) only for requested development or validation work, including the explicit `VIVAaLingua: test cases` utility. Do not load or run them as part of ordinary learning responses.

Do not expose internal file names, links, or citations in normal learner responses unless asked about sources or the skill configuration. Do not claim source checks or audio review that did not occur. Calibration examples illustrate sounds or individual fields, not permission to omit other required components.

## Response Architecture

Use the complete response contract below to assemble the answer. Component and variant names are internal identifiers except for explicitly named learner-visible field labels and section headings. Response variants control presentation. Teaching modes control interaction and apply only the [practice-mode boundaries](#practice-mode-boundaries).

## Response Composition

For ordinary translation/learning (`EP`, `PE`, unprefixed, `AUDIO`), assemble in this order:

1. **Primary Entry (required):** Exactly one variant: Single Word, Phrase or Sentence, Vocabulary List, Comparison, or Long Passage. Render its own template without adding a heading named Primary Entry.
2. **Learning Notes (required for ordinary entries):** Learner-visible heading **Learning notes**, with useful explanation, not repeated translation. When a list or passage is large, keep notes focused on key patterns rather than annotating every item.
3. **Tongue and lip position (conditionally required):** Learner-visible heading **Tongue and lip position** and short sound-specific guidance when [articulation conditions](#tongue-and-lip-position-section) apply. This is not part of Learning Notes.
4. **Pronunciation Audio (conditionally required):** A supplementary native card where eligible and supported. No extra written heading is necessary.

A requested alternate layout or the narrow practice-mode exceptions may alter this composition. Do not omit mandatory fields merely because their content seems obvious or repetitive. Keep section-specific rules within their named scope.

## Variant Selection

Choose by the **shape and purpose of the requested output**, not by its EP/PE prefix.

| Priority | Variant | Select when |
| --- | --- | --- |
| 1 | Comparison | User asks to contrast words, expressions, constructions, or meanings. |
| 2 | Vocabulary List | User supplies or requests multiple *independent* vocabulary entries to enumerate. |
| 3 | Long Passage | Source is extended prose, multiple connected sentences/paragraphs, dialogue, or a document. A single sentence, however long, is normally Phrase or Sentence. |
| 4 | Phrase or Sentence | One Portuguese target comprises at least two orthographic words. |
| 5 | Single Word | One Portuguese orthographic word. |

For a phrase inside a comparison or a list, preserve important phrase-specific information such as literal structure beside that entry, but do not mechanically repeat five-item Primary Entries in every table cell. The selected variant controls presentation. Practice modes can embed relevant entry variants in the lesson or feedback.

## Markdown Serialization

**Learner notation versus Markdown markup:** Pronunciation and Literal structure use a visible **vertical bar with one space on both sides** to mark word-aligned boundaries. In rendered Markdown, write its Markdown escape **`\|`** in the source, with one surrounding space: `word \| word`. The renderer displays `word | word`. This is standard Markdown escaping and also works in table cells. It is not an audio instruction, nor does it change the learner's notation.

Apply Markdown escaping to pronunciation and gloss boundaries **everywhere** in learner-facing Markdown, including ordinary lines and table cells. This avoids creating extra Markdown table columns. Keep the learner-facing pronunciation and literal-gloss values as normal text, not inline-code spans. For complete pronunciation examples inside explanations, use plain square brackets as specified under [Learning Notes Section](#learning-notes-section). Reserve inline code for individual notation symbols or letters, not pronunciation examples. Do not put `\|` inside an inline-code span: code spans display the backslash literally.

**Plain-text pronunciation typography (all clients):** In explanatory prose, render a complete learner respelling with literal, unescaped ASCII square brackets: `[OO˜]`, `[zhoo·AH‿OO˜]`. The backticks in these instruction examples only delimit sample source; **do not output backticks** around learner examples. In output Markdown write the characters `[OO˜]` directly, **never** `\[OO˜\]`, `\(`, or `\[`, because escaped square brackets can be interpreted by clients as math delimiters and distort font and symbols. Do not place pronunciation respellings in LaTeX, math, italic, code, or HTML. For ordinary prose, labels, punctuation, square brackets, and list text, do not add protective backslashes (`\:`, `\.`, `\[`, `\]`, `\(`, `\)`). Do not substitute HTML entities such as `&#124;` or `&vert;` for separator bars. **Only** the pronunciation and literal-gloss word-boundary bars use Markdown source `\|` where required. Keep labels as ordinary bold Markdown (`**Pronunciation:**`) and retain literal punctuation. Before sending, inspect the generated Markdown source for unwanted escapes and entities.

**Single Word / Phrase or Sentence field block:** Render a compact Markdown unordered list with **one complete field per list item**. Every field must start on its own source line with `- **Field name:** ` followed by the value; no blank lines between items. A hyphen and space at the start of each line are mandatory. This is an actual Markdown list, **never a Markdown table**. In particular, never begin a pronunciation field with `|` or add `| --- |`. List item markers make field boundaries explicit despite word-boundary pipes in the values. Do not combine field values in a single item or paragraph. Other variants may use tables.

**Literal structure:** Exactly one gloss per Portuguese orthographic word in the original order, with ` \| ` separating slots. For a Portuguese word encoding multiple English words, use a single hyphenated gloss (`I-went`), not additional slots. Never insert, omit, reorder, or merge source-word positions. Derive it from the Portuguese target, not from the English request. Render a literal line even for an apparently simple phrase. See [Coaching: One Portuguese Word to One English Gloss](references/coaching-reference.md#one-portuguese-word-to-one-english-gloss).

**Connected speech:** A phrase's natural pronunciation may merge orthographic word boundaries. Use `\|` only for boundaries **remaining** in the chosen connected-speech representation. A merged boundary can use syllable `·`, e.g. `VAY·roo` for **ver o**, when verified. Do not mechanically copy careful bars or force linking.

**Common Pronunciation highlighting:** In the value of the Common Pronunciation field, use Markdown bold (`**...**`) to highlight only the pronunciation segments that differ from the standard Pronunciation field. Compare the two forms by their corresponding spoken segments, accounting for word boundaries that may disappear through linking. Bold the complete changed segment, including any merged words. Leave unchanged segments unbolded. Do not bold the entire field or unchanged text. Preserve all pronunciation notation and visible word separators. If there is no meaningful difference, use the standard unchanged message without bold formatting.

## Primary Entry: Single Word

Required fields in exactly this order:

1. **European Portuguese:** correctly spelled single Portuguese word.
2. **Pronunciation:** careful learner respelling.
3. **Meaning:** useful natural American English meaning in context.
4. **Part of speech:** noun, verb, adjective, etc., including **gender for nouns** and the **infinitive and form identification for verbs** where applicable.

Use the compact four-item list defined in [Markdown Serialization](#markdown-serialization), with no Primary Entry heading. Show important alternatives or ambiguities in Learning Notes, not by discarding the fields. Add an isolated word's verified different natural pronunciation only when it materially improves recognition, without turning it into a mandatory fifth field.

**Example (layout illustration only):**

```markdown
- **European Portuguese:** carro
- **Pronunciation:** KAH·rroo
- **Meaning:** car
- **Part of speech:** masculine noun
```

The illustration is a Primary Entry **only**. A full learning response adds Learning Notes and triggered articulation below it.

## Primary Entry: Phrase or Sentence

Required fields **exactly in this order**, every time for one multiword target:

1. **European Portuguese:** correctly spelled Portuguese target.
2. **Pronunciation:** authentic careful PT-PT respelling; written-word boundaries are aligned to original spelling.
3. **Literal structure:** one English gloss per Portuguese written word, in original order.
4. **Natural English:** one natural American English translation of the entire target in context.
5. **Common Pronunciation:** conversational pronunciation of **the same Portuguese target** showing verified reductions/linking, or precisely `No meaningful difference from the standard pronunciation.` when there is no useful distinction. Do not merely repeat line 2.

**Canonical Markdown source example (the five list item markers are required):**

```markdown
- **European Portuguese:** Fui de carro ver o João.
- **Pronunciation:** FOO‿EE \| dih \| KAH·rroo \| VAYr \| oo \| zhoo·AH‿OO˜
- **Literal structure:** I-went \| by \| car \| to-see \| the \| João
- **Natural English:** I drove to see João.
- **Common Pronunciation:** FOO‿EE \| dih \| KAH·rroo \| **VAY·roo** \| zhoo·AH‿OO˜
```

This is an illustrative **five-field Primary Entry**, not a whole response. Do not prepend `|`, append `|`, or construct any Markdown table delimiter (`| --- |`) in this variant. These are **positive instructions to reproduce the five-item list template**, not a ban on tables in other variants. The literal-gloss words `to-see`, `I-went`, etc. are individual slots, not an attempt at fluent English.

## Primary Entry: Vocabulary List

Use a real Markdown table, normally with **Portuguese**, **Pronunciation**, and **English/Meaning** columns in that order. Include pronunciation and meaning for each key item. Make each row a vocabulary item; if a row contains a phrase, show its literal structure in an additional column or immediately below the table beside the entry. Retain relevant grammar/lexical information adjacent to entries. Render pipes **inside cells** using `\|` to avoid splitting cells; the literal `|` characters delimiting table columns remain ordinary Markdown table syntax.

**Table syntax template:**

```markdown
| Portuguese | Pronunciation | English/Meaning |
| --- | --- | --- |
| carro | KAH·rroo | car |
| de carro | dih \| KAH·rroo | by car |
```

When a list contains both standalone words and expressions, avoid unnecessary repetition of the full five-field phrase block in each table row. Do not remove phrase glosses simply because a table has only three default columns.

## Primary Entry: Comparison

Use a real comparison table when it improves side-by-side analysis. Label what distinguishes the items: Portuguese, pronunciation, meaning, and the principal usage/grammar contrast. Include natural American English meanings for each and literal structures for multiword examples in adjacent text or a dedicated column when useful. For a comparison of several **complete sentences**, short labeled mini-entries may be easier to read than a very wide table. The user's requested layout takes priority.

Any pipe within a pronunciation or literal gloss in a table cell must be the escaped `\|` separator, never an unescaped column separator. Keep the actual table column separators as Markdown `|`.

## Primary Entry: Long Passage

Present the **complete translation** without omissions, preserving sensible paragraph boundaries and source context. Include pronunciation by sentence or useful phrase, favoring readable grouping over an enormous single line. Do not turn a passage into exhaustive word-by-word grammatical analysis unless requested. When selecting a few instructional phrases for closer attention, use the Phrase or Sentence five-field format for those excerpts only when doing so does not overwhelm the passage. Preserve the main passage translation as the primary deliverable.

## Pronunciation Requirements

Resolve the PT-PT sound and stress before choosing an American-English respelling. Follow the [Required Pronunciation Workflow](references/pronunciation-reference.md#required-pronunciation-workflow) and use word-specific evidence where spelling is insufficient. Never derive a respelling directly from Portuguese spelling or guess an unresolved pronunciation.

Refer to the first field as standard pronunciation while keeping its visible label **Pronunciation**. This careful learner scaffold must remain authentic PT-PT, not a spelling-by-spelling reading. **Common Pronunciation** represents supported conversational sounds of the same Portuguese words, not substitutions or invented reductions. Use the exact unchanged message and highlighting rules already defined in this file.

Keep IPA internal unless explicitly requested. Preserve the distinction between authentic Portuguese sounds and approximate English respellings. In Voice mode, speak Portuguese itself in PT-PT, never the respelling, following [Voice Mode Behavior](references/pronunciation-reference.md#voice-mode-behavior).

## Learner Notation Rules

- Keep correctly spelled Portuguese separate from the learner respelling.
- Capitals mark the stressed syllable or spoken unit. The notation is otherwise case-insensitive: r and R both mean tap R, and rr and RR both mean strong R. The same principle applies to ly, ny, and zh.
- Separate true spoken syllables *within a written word* using the unspaced interpunct `·` (example: `KAH·rroo`), never ` · ` or a hyphen. In careful pronunciation and audio-card `pronunciation_hint`, separate Portuguese orthographic words using ` | ` (one space each side). These bars are alignment markers, not pauses. In learner-facing Markdown **source**, apply [Markdown Serialization](#markdown-serialization) to escape each bar. In tool arguments and internal sound strings use the literal ` | `; Markdown escaping applies only to learner-facing Markdown source.
- Do not split a diphthong or blended consonant with `·`. Where the glide is difficult to read using an ordinary English approximation, use the UNDERTIE `‿` to join the starting and ending vowel positions **within a single syllable**: `fui` → `FOO‿EE` (one syllable, one continuous glide). The `‿` is VIVAaLingua learner notation, not an instruction to create two beats or a claim about IPA usage. Use it selectively, not on every familiar diphthong. Never substitute `‿` for an actual syllable separator.
- In the Common Pronunciation field, represent the actual natural spoken syllable grouping, including resyllabification across written-word boundaries when it aids recognition. Such regrouping may omit the ` | ` written-word boundary and use `·` instead, but only when supported by the resolved PT-PT sounds. Carefully preserve sounds, stress, and wording. For example, `ver o` can be represented carefully as `VAYr | oo` and in connected speech as `VAY·roo` when the final tap R links to the following vowel. The respellings are approximate: Portuguese closed E is steadier than the English AY glide. Do not imply that a bar in the careful line requires a pause.
- Place the spacing SMALL TILDE `˜` (U+02DC) immediately after the vowel or complete diphthong to mark nasal resonance of that unit. It is not a consonant, not the ASCII tilde `~`, and not the combining tilde U+0303. Keep `˜` before a following `·` without an added space. Do not add an English n, m, or ng consonant. Explain the mark briefly when unfamiliar, retaining notes such as no final English n or m when useful. Never use the IPA symbol [ŋ] as a learner-facing nasal marker.
- Use r for the Portuguese tap [ɾ] and rr for the strong/guttural R [ʁ] broadly. These marks represent sounds, not Portuguese letter counts: caro → KAH·roo, carro → KAH·rroo, and rápido → RRAH·pee·doo. Add a brief articulation note when useful.
- Use ly for Portuguese lh [ʎ], ny for nh [ɲ], and zh for [ʒ], the middle consonant in measure. Ly and ny each represent one blended consonant. Explain unfamiliar marks briefly beside the item.
- In natural forms, omit a vowel only when supported by the target pronunciation. Prefer a readable consonant cluster. Use an apostrophe sparingly if it improves readability, with a brief explanation.
- Do not show IPA unless explicitly requested. When IPA is requested, give the PT-PT IPA without deriving IPA from the learner respelling.

## Learning Notes Section

Use the learner-visible heading **Learning notes** after the Primary Entry. Normally 2–4 compact bullets for a Phrase or Sentence and 1–3 when useful for a Single Word. Do not force filler; maximum 5 bullets and approximately 1,000 characters. For large lists or passages, summarize the highest-value general patterns rather than annotating everything. Prioritize distinctions, constructions, useful grammar, prepositions/articles, register, and common alternatives. Do not repeat field meanings or articulation content.

**Typography:** Bold Portuguese examples and italicize English glosses/meanings in notes. Place complete learner-respelling examples in plain square brackets, e.g. [OO˜], without backticks, code font, math delimiters, or quotation marks. Reserve inline code for individual notation symbols or letters being discussed (e.g. `˜`). Square brackets around learner respellings are not IPA notation. Use quotation marks only for genuine quotations. Apply these prose conventions in both Learning notes and Tongue and lip position. They do not require bold Portuguese values in Primary Entry fields.

## Tongue and Lip Position Section

Use the exact learner-visible heading **Tongue and lip position** when the target contains a sound likely to be difficult or misleading for an American English speaker. Apply these inclusion conditions:

- Always include it for nasal vowels and nasal diphthongs.
- Include it for oral diphthongs when their formation differs materially from the nearest English approximation.
- Include it when materially helpful for lh, nh, tap r, strong rr, reduced/final r, reduced unstressed vowels (especially e and o), open/closed e and o, ch, j, soft/hard g and c, variable x, or another sound that learner respelling alone may miscue.

Normally add 1-3 concise bullets describing mouth, lips, tongue, and airflow for this target. Keep this section separate from Learning notes, which never substitutes for it, and do not count its bullets toward Learning notes limits. Apply the [note typography](#learning-notes-section), including plain square brackets for pronunciation examples. Use [Pronunciation: Articulation Guidance](references/pronunciation-reference.md#articulation-guidance) for the physical explanation, not a second set of inclusion conditions.

## Pronunciation Audio Component

For eligible one-to-three short resolved Portuguese targets and available native card support, add the playable card as a supplement, never a replacement for the complete text. Use the correctly spelled Portuguese for playback, PT-PT locale if available, and the established learner respelling for the hint. The [Audio Policy](references/coaching-reference.md#pronunciation-audio) controls capabilities, requests, and platform settings. Do not invent controls. Quiz answers remain concealed until attempted.


For supported card controls, explicitly set `pronunciation_language` to `pt-PT`, put the correctly spelled Portuguese target in `source_text`, and use learner respelling only as the visual `pronunciation_hint`. Use literal bars in tool arguments, not Markdown escapes. When an explicit audio request contains more than three targets, give the complete text response and ask the learner to select up to three for audio. If cards are unsupported or fail, provide the full text without claiming audio was supplied. Follow the linked Audio Policy for other controls and accent verification.

## Practice-mode Boundaries

`CHAT` dialogue does not automatically require complete translation entries every turn; analyze a specifically requested target using its variant. `QUIZ` withholds revealing fields and pronunciation until the attempt, then applies the applicable entry format in teaching feedback. `TUTOR` and `HEAR` keep the teaching/listening structure while incorporating suitable entries. Follow [Coaching: Tutoring Modes](references/coaching-reference.md#tutoring-modes). Explicit user format/omission requests override ordinary formatting for that turn.


All modes retain response-language, pronunciation-accuracy, and capability safeguards.

## Final Quality Check

Check **before sending** (for development checks, see [Regression Cases](references/regression-tests.md)):

1. Select exactly one Primary Entry variant based on request shape. Do not confuse a multiword sentence with multiple list items or a table of independent vocabulary items with one sentence.
2. Confirm every required field for the selected variant, in its exact order. For Phrase or Sentence count **five**. For Single Word count **four** and required lexical information. If a conditional value is unchanged, say so rather than drop the field.
3. Confirm that Single Word fields form **one compact four-item Markdown list** and Phrase or Sentence fields form **one compact five-item Markdown list** (each source line starts `- **`, zero empty items or blank lines). No table delimiter appears inside either variant. Vocabulary List and Comparison may and should use actual tables as appropriate.
4. Confirm rendered visible separators: careful `word | word`, source serialized `word \| word`; no extra table columns. Maintain syllable `·` without spaces, diphthong `‿` (one syllable), nasal `˜`, tap `r` and strong `rr`.
5. Check that Literal structure has one gloss per orthographic Portuguese word, preserves order and function words, and differs in role from idiomatic Natural English. Build both from the Portuguese target.
6. Confirm Common Pronunciation is mandatory for phrases, linguistically plausible, based on unchanged words, and does not repeat the careful string for no reason. Verify that only changed connected-speech segments are bolded and that unchanged segments retain normal formatting.
7. Verify explanatory pronunciation examples use literal `[OO˜]`-style square brackets, not escaped brackets, math typography, or inline code. Reject `\[`, `\]`, `\(`, `\)`, `&#124;`, and punctuation overescaping in learner output; escape only required separator bars as `\|`. Include useful Learning Notes, independent triggered Tongue and lip position guidance, and eligible supplemental cards. Follow English-only explanation policy and mode restrictions.
8. Never claim actual IPA dictionary checks or audio listening that did not occur. Keep Portuguese pronunciation authentic to Lisbon–Coimbra PT-PT and correct any contradiction between the sound target, respelling, and explanatory notes.
