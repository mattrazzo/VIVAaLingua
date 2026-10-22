# VIVAaLingua Pronunciation Reference

European Portuguese pronunciation for native American English speakers

Use this guide to resolve PT-PT sounds internally with the International Phonetic Alphabet (IPA), then teach them through readable American-English respellings. These visible forms are approximations chosen for each word or phrase. This internal reference contains IPA for control and review. Do not reproduce that IPA in learner responses unless requested. Use [SKILL.md](../SKILL.md) for layout, required sections, learner notation, and command behavior, and the [Coaching reference](coaching-reference.md) for translation and teaching details.

## Contents

- [Target Variety and Governing Principles](#target-variety-and-governing-principles)
- [Required Pronunciation Workflow](#required-pronunciation-workflow)
- [Learner Notation Rules](#learner-notation-rules)
- [American English Respelling Principles](#american-english-respelling-principles)
- [Vowels and Reduction](#vowels-and-reduction)
- [Diphthongs and High Value Regional Distinctions](#diphthongs-and-high-value-regional-distinctions)
- [Nasality](#nasality)
- [Consonant Selection](#consonant-selection)
- [Stress](#stress)
- [Careful and Natural Speech](#careful-and-natural-speech)
- [Calibration Examples](#calibration-examples)
- [Cabeleireiro Worked Example](#cabeleireiro-worked-example)
- [Output Quality Check](#output-quality-check)
- [Voice Mode Behavior](#voice-mode-behavior)
- [Source Hierarchy and Evidence](#source-hierarchy-and-evidence)

## Target Variety and Governing Principles

Default to contemporary standard European Portuguese centered on the Lisbon-Coimbra standard. This provides one stable teaching target while allowing genuine regional alternatives to be mentioned when they are common and useful. The standard target is descriptive, not a claim that regional varieties are inferior. [1]

Resolve the established Portuguese pronunciation before choosing the visible spelling. Use ordinary American-English respelling for most sounds, supplemented by the small VIVAaLingua notation set below. Preserve visible tap/strong R, nasal, lh, nh, and zh distinctions. Keep finer phonetic detail internal or explain it locally when useful.

Prioritize accurate stress, vowel quality, vowel reduction, nasalization, rhythm, and major consonant contrasts. A learner respelling is necessarily approximate, but it should move an American English speaker toward the Portuguese target without inviting an English reading of Portuguese spelling.

## Required Pronunciation Workflow

1. Identify the exact Portuguese word or phrase and its context.
2. Resolve a broad IPA target internally before considering the visible respelling. Never derive the learner respelling directly from Portuguese spelling. Use word-specific evidence when spelling does not determine pronunciation.
3. Apply predictable contextual processes such as unstressed-vowel reduction, coda s/z voicing, linking, and common weak-vowel deletion.
4. Only after the sound target is resolved, choose familiar English words, syllables, or spelling patterns for the whole spoken unit, then apply the controlled VIVAaLingua marks. A rule in this reference overrides an intuitive English-style reading of Portuguese spelling. Vowel spellings may vary with consonant context. Do not impose fixed one-to-one vowel codes.
5. Write the careful learner respelling. It must remain authentic PT-PT without sounding out every written letter.
6. Determine whether a supported common realization materially improves recognition. Apply [SKILL.md: Phrase or Sentence](../SKILL.md#primary-entry-phrase-or-sentence) for the required Common Pronunciation field or unchanged message, and [Single Word](../SKILL.md#primary-entry-single-word) for an optional natural form. Do not invent a sound difference to fill a field.
7. If pronunciation remains uncertain, identify the uncertain part. Do not guess.

For lexical fallback, prefer a current PT-PT dictionary with phonetic transcription, then authoritative European Portuguese pronunciation references. Use general spelling rules only where they are reliable. Infopédia is useful for word-specific transcription. Camões IP and phonetic literature are useful for system-level rules. [1]-[6]

## Learner Notation Rules

Apply the complete [Learner Notation Rules in SKILL.md](../SKILL.md#learner-notation-rules), including stress capitals, interpuncts, word bars, UNDERTIE, SMALL TILDE, consonant marks, and the exception for supported common-speech regrouping. Apply its [Markdown Serialization](../SKILL.md#markdown-serialization) only to learner-facing Markdown, not to spoken text or literal tool arguments. The sections below resolve the sounds to which those marks apply.
## American English Respelling Principles

Use the closest readable American-English approximation with the controlled VIVAlanguage marks. Explain an unfamiliar mark in the response so the learner can attempt the word immediately. Articulation notes refine the approximation. These are teaching choices, not dictionary transcriptions.

### Vowels and Whole Syllables

Use familiar patterns such as ee in see, eh in bed, ah in father, oo in food, and oh in go where they fit the surrounding consonants. Closed Portuguese e and o are steadier than English ay and oh. Open o can use aw for Americans who distinguish law from father. If those vowels merge for the learner, explain the rounded open vowel locally.

For reduced vowels, keep [ɐ] distinct from [ɨ] when useful: uh can suggest [ɐ], while brief ih can scaffold [ɨ]. Neither English sound is an exact match. Keep weak syllables light, and do not teach a full English hit vowel as the Portuguese target. Adapt the spelling to the whole syllable instead of imposing ih everywhere.

### Diphthongs

A diphthong moves between vowel positions within one syllable. For [ɐj], familiar eye, lie, rye, or sigh patterns give a readable starting point. Thus lei can use LIE, rei RRYE with strong rr, and seis SIGHSH. The Portuguese start is more central than American eye. Preserve that distinction internally. Do not revive UHY or a fixed vowel code. [6]

The oral targets [aj] and [ɐj] may share an eye-like approximation. Explain the more central start when teaching their contrast. For [ej] or [ɛj], choose an ay-like approximation and explain openness only when useful. For [oj] and [ɔj], use an oy-like pattern and a local vowel note if the distinction matters.

For [aw], choose an ow pattern that reads like now, not snow. For [ew] and [ɛw], a whole English-like sequence such as sayoo or eh·oo may misleadingly add a syllable. Where needed, use `‿` to connect vowel positions within a single syllable and explain the movement. For [iw], explain a single-syllable ee-to-oo glide. For [uj], explain a single-syllable oo-to-ee glide, using `FOO‿EE` for verified `fui`. Verify the actual Portuguese diphthong before choosing a spelling. Do not mechanically insert the marker into established intuitive respellings such as `OY` or `EYE`.

Written ou commonly has a steady oh-like vowel in the default target. Preserve regional diphthongs internally when relevant. Do not force every written vowel pair into a diphthong. [7]

### Nasal Sounds

Use a readable vowel approximation followed by `˜` for nasality. For nasal [ĩ], [ẽ], [ɐ̃], [õ], and [ũ], begin near ee, steady ay, uh, steady oh, and oo respectively. These are starting points, not fixed vowel spellings. For example, sim can use SEE˜ and bom BOH˜. Include the required Tongue and lip position guidance.

For mãe, MY˜ is a readable first attempt. Bem can use BYE˜, não NOW˜, and põe POY˜. Keep nasality through the whole glide. The `˜` marks nasal resonance in the vowel or diphthong, without an added English n, m, or ng consonant.

### Consonants English Does Not Match

Keep Portuguese R contrasts visible: caro → KAH·roo has a tap, and carro → KAH·rroo has strong R. Use ly for lh [ʎ] and ny for nh [ɲ], each one blended consonant. The middle sounds of million and canyon offer starting approximations. Blend without adding a syllable or inserting a separator between the letters.

Use zh for [ʒ], the middle consonant in English measure. Sh is familiar English spelling. Keep hard g unambiguous. Retain ordinary l for dark final l, with a local articulation note when useful. Do not create special visible notation for dark l or natural b/d/g weakening by default.

### Articulation Guidance

Follow [SKILL.md: Tongue and Lip Position Section](../SKILL.md#tongue-and-lip-position-section) for all inclusion triggers, the heading, placement, length, and typography.

Describe only what matters to the target: tongue position or movement, lip shape or rounding, jaw opening when relevant, airflow or nasalization, and transitions between sounds. Contrast a likely American-English error when useful. Keep the guidance concise and target-specific.

## Vowels and Reduction

European Portuguese has a richer stressed-vowel system than English learners often expect, and a much smaller unstressed system. In the standard pattern, unstressed mid front vowels reduce toward [ɨ], unstressed mid back vowels reduce toward [u], and unstressed [a] raises toward [ɐ]. High [i] and [u] generally remain high. [2][3][4]

| Stressed source | Typical unstressed result | Teaching guidance |
| --- | --- | --- |
| [e] or [ɛ] | [ɨ] | A brief ih can scaffold [ɨ]. Keep it weak. |
| [o] or [ɔ] | [u] | Choose a readable syllable. Keep the unstressed vowel brief. |
| [a] | [ɐ] | Uh can scaffold [ɐ]. Keep it light. |
| [i] | [i] | Choose a readable syllable. Keep the unstressed vowel brief. |
| [u] | [u] | Choose a readable syllable. Keep the unstressed vowel brief. |

Do not apply reduction mechanically. Lexical exceptions, syllable structure, morphology, and regional speech can block or alter the usual pattern. The internal IPA target must come before the learner respelling.

Final unstressed e is commonly a very weak [ɨ] and can disappear in conversational speech. Some dictionaries use [ə] for this sound. Current EP phonetic literature often uses [ɨ], and older [ə] transcriptions need not imply a different sound target. [3]

Initial unstressed e before s plus consonant often surfaces as [i] or is absent, as in estar. Treat forms such as [iʃˈtar] and [ʃˈtar] as normal standard possibilities without forcing an English-like initial vowel. [5]

Stressed unaccented e and o are lexical. Do not infer open versus closed quality from spelling alone when the word is not already known.

## Diphthongs and High Value Regional Distinctions

Written ei is not reliably English AY. In the standard/Lisbon-oriented target, many ei sequences use [ɐj]. For example, seis is [sɐjʃ], and Ciberdúvidas describes standard ei as approximately a central âi sound. Regional [ej] and monophthongal [e] also occur and are valid where established. [5][6]

Written ou is commonly monophthongal [o] in the Lisbon-Coimbra standard, while [ow] and [ɐw] remain valid regional realizations, especially farther north. Do not pronounce ou as an English-style diphthong by default merely because two vowels are written. [7]

Do not assume every adjacent vowel pair is a diphthong. Resolve the word first. Keep genuine diphthongs within one spoken syllable in the learner respelling.

## Nasality

In Portuguese spelling, a tilde signals nasality. Orthographic m or n closing a syllable commonly indicates a nasal vowel rather than a separate final English m or n. When m or n marks nasality, never carry that letter into the learner respelling as an English consonant. Do not apply that rule when m or n begins the next syllable. [1][2]

Final em and ens in standard PT-PT commonly pattern with the nasal diphthong [ɐ̃j̃]. Written ão commonly gives [ɐ̃w̃]. Written õe gives [õj̃]. Use word-specific evidence for exceptions.

Muito has the verified target [ˈmũj̃tu]. A readable starting approximation is MOY˜·too, with a nasal first diphthong. Explain: start with rounded oo lips and glide toward ee in one syllable, without a final n. English boy starts too open. Use a spoken PT-PT model when available. Do not revive MWEEN or an unexplained MOOY code. [8]

## Consonant Selection

### Core Spelling Patterns

- c is k before a, o, u and s before e, i. ç is s.
- ch is sh. j is zh.
- g is hard g before a, o, u and zh before e, i, subject to gu spelling patterns.
- h is silent outside digraphs.
- ss is s.
- Use ly for lh [ʎ] and ny for nh [ɲ]. Each is one blended consonant. Add the articulation guidance above when useful.
- Standard PT-PT t and d do not become the Brazilian-style ch/j sounds before i.

### R and Rr

Initial r and intervocalic rr take strong R. A back-of-mouth realization is common in Lisbon-oriented speech, while tongue-tip trills also occur. Single r between vowels and in clusters such as pr, br, and tr normally takes a tap. Final r can weaken. In the respelling, use rr for the strong sound and r for the tap, regardless of Portuguese spelling or stress capitals. Add gesture guidance when useful.

### S and Z at the End of a Syllable

| Context | Target |
| --- | --- |
| Initial s or ss | s |
| Single s between vowels | z |
| z beginning a syllable | z |
| Syllable-final s/z before pause or voiceless consonant | sh |
| Syllable-final s/z before voiced consonant | zh |
| Word-final s/z linked to a following vowel | z |

Coda means the end of a syllable. Apply these sound rules across word boundaries. A pause blocks linking.

### Qu Gu and X

QU and GU require lexical control because the written u may be silent or pronounced. X may represent sh, z, ks, or s. Initial x and x after en or a diphthong often use sh, but this is not a complete rule. Use word-specific pronunciation for uncertain x, GU, and QU words.

### Natural Stop Weakening

Voiced stops b, d, and g can be noticeably softened between vowels in natural PT-PT. Treat this primarily as a listening-recognition feature. Do not create a separate learner respelling unless the distinction is being taught.

## Stress

| Word pattern | Working stress rule |
| --- | --- |
| Acute or circumflex accent | Stress the accented syllable. |
| Common unaccented endings a, e, o, with or without s | Usually stress the next-to-last syllable. |
| Unaccented am, em, ens endings | Usually next-to-last stress in multisyllable words. |
| Unaccented i, u, is, us, l, r, z, x | Usually final stress. |
| Final falling diphthong | Normally final stress unless an accent marks otherwise. |
| Third-to-last stress | Normally identified by a written acute or circumflex. |

These are working defaults, not a substitute for lexical knowledge. Check exceptions, compounds, and verb forms. A tilde marks nasality and does not by itself assign stress. A grave accent does not independently assign stress.

## Careful and Natural Speech

Standard pronunciation (the learner-facing Pronunciation field, called careful pronunciation in phonetic description) is a learner scaffold that preserves the correct PT-PT sound categories and stress. It may retain a weak vowel that native speech often reduces further, but it must not restore full vowels because they appear in spelling.

Natural pronunciation may show common deletion of weak [ɨ], initial-vowel loss, linking, and s/z assimilation. Apply [SKILL.md](../SKILL.md#primary-entry-phrase-or-sentence) for the field requirement and exact unchanged message, and its [Single Word variant](../SKILL.md#primary-entry-single-word) for optional natural forms. Do not delete weak vowels mechanically, invent extreme compression, or substitute different Portuguese words. A careful-line bar does not prohibit linking.

| Context | Careful respelling | Natural respelling / point |
| --- | --- | --- |
| está | eesh·TAH | SHTAH - initial vowel can disappear. |
| dois before a pause | DOYSH | Same. |
| dois gatos | DOYZH \| GAH·toosh | Final s voices before g. |
| dois copos | DOYSH \| KOH·poosh | Final s stays voiceless before k. |
| os amigos | ooz \| uh·MEE·goosh | Final s links as z before the following vowel. |
| nove | NAW·vih | NAWV is a possible compact natural realization when final [ɨ] is barely audible. |

In HEAR mode, emphasize connected-speech forms that make familiar words difficult to recognize, while keeping the careful form available as an anchor.

## Calibration Examples

These examples illustrate teaching choices, not mandatory sound-to-spelling rules. Keep the IPA column internal. Natural forms are possibilities, not required replacements. Revise vowel approximations when evidence or learner feedback supports a clearer reading, while retaining the controlled VIVAaLingua marks. Apply the required articulation guidance when triggered.

| Portuguese | Internal IPA | Careful respelling | Natural | Teaching point |
| --- | --- | --- | --- | --- |
| olá | [ɔˈla] | aw·LAH |  | Open initial O, final stress. |
| bom | [bõ] | BOH˜ |  | Nasal vowel. No final English n or m. |
| bem | [bɐ̃j̃] | BYE˜ |  | Nasal vowel. No final English n or m. |
| sim | [sĩ] | SEE˜ |  | Nasal vowel. No final English n or m. |
| não | [nɐ̃w̃] | NOW˜ |  | Nasal ão. Start is more central than English now. |
| muito | [ˈmũj̃tu] | MOY˜·too |  | High rounded nasal diphthong. Start with rounded oo lips, glide toward ee. |
| um | [ũ] | OO˜ |  | Nasal vowel. No final English n or m. |
| seis | [sɐjʃ] | SIGHSH |  | Sigh plus sh, one syllable. More central start. |
| nove | [ˈnɔvɨ] | NAW·vih | NAWV | Open stressed O and weak final e. |
| dois | [dojʃ] | DOYSH |  | Final s before pause. |
| três | [tɾeʃ] | TRAYSH |  | Closed stressed E and tap r. |
| sete | [ˈsɛtɨ] | SEH·tih | SEHT | Open stressed E and weak final e. |
| dez | [dɛʃ] | DESH |  | Open E and final z → sh before pause. |
| hoje | [ˈoʒɨ] | OH·zhih | OHZH | Closed O and weak final e. |
| casa | [ˈkazɐ] | KAH·zuh |  | Intervocalic s → z. Final a reduces. |
| onde | [ˈõdɨ] | OH˜·dih |  | Nasal first vowel. The written n marks nasality, not an English n consonant. Final e is weak. |
| banho | [ˈbɐɲu] | BUH·nyoo |  | Central first vowel. Keep ny blended like canyon, without an extra syllable. |
| bilhete | [biˈʎetɨ] | bee·LYAY·tih |  | Blend l and y like million. Keep ay steady and final vowel weak. |
| melhor | [mɨˈʎɔɾ] | mih·LYOR |  | Weak initial e, open O, final tap r. |
| obrigado | [ubɾiˈɣadu] | oo·bree·GAH·doo |  | Natural g may soften. Keep PT-PT vowels. |
| quarto | [ˈkwartu] | KWAR·too |  | Pronounced u in qu and tap r. |
| rápido | [ˈʁapidu] | RRAH·pee·doo |  | Use a strong back-of-mouth R. |
| está | [iʃˈta] | eesh·TAH | SHTAH | Initial vowel may be absent naturally. |
| desculpe | [dɨʃˈkuɫpɨ] | dish·KOOL·pih |  | Reduced vowels. Coda l is dark. |
| estação | [iʃtɐˈsɐ̃w̃] | eesh·tuh·SOW˜ | shtuh·SOW˜ | Initial vowel may delete. SOW rhymes with cow. Nasal final vowel. |
| informação | [ĩfuɾmɐˈsɐ̃w̃] | ee˜·foor·muh·SOW˜ |  | Nasal first and last vowels. SOW rhymes with cow. Tap r. |
| segunda | [sɨˈɡũdɐ] | sih·GOO˜·duh | sGOO˜·duh | Nasal stressed oo, no final n. Keep the first vowel weak. |
| sábado | [ˈsabɐdu] | SAH·buh·doo |  | Middle a reduces to [ɐ]. |
| cinco | [ˈsĩku] | SEE˜·koo |  | Nasal first vowel. No final English n or m. |
| conta | [ˈkõtɐ] | KOH˜·tuh |  | Nasal first vowel. No final English n or m. |
| Bom dia | [bõ ˈdiɐ] | BOH˜ \| DEE·uh |  | Nasal BOH˜. Keep d as d, not English j. |
| Fala inglês | [ˈfalɐ ĩˈɡleʃ] | FAH·luh \| ee˜·GLAYSH |  | Nasal ee˜ at the start of inglês. Final sh before a pause. |
| cedo | [ˈsedu] | SAY·doo |  | Closed stressed E. |
| oito | [ˈojtu] | OY·too |  | Oral oi diphthong. |
| caro | [ˈkaɾu] | KAH·roo |  | Single r is a tap. |
| carro | [ˈkaʁu] | KAH·rroo |  | Use a strong back-of-mouth R. |
| fui | [ˈfuj] | FOO‿EE |  | One-syllable oral diphthong: move from rounded oo toward ee. The UNDERTIE joins vowel positions, not syllables. |
| João | [ʒuˈɐ̃w̃] | zhoo·AH‿OO˜ |  | Two syllables in a careful model. Keep the stressed nasal diphthong together in its final syllable. Exact reduction varies with speech rate. |
| ver | [veɾ] | VAYr |  | Closed E is steadier than English AY. Final R is a tap, not strong rr. |
| ver o | [veɾ u] | VAYr \| oo | VAY·roo | Linking moves final tap R into the following spoken syllable without changing the words. |
| de carro | [dɨ ˈkaʁu] | dih \| KAH·rroo |  | de means by as a transport preposition. Weak vowel quality must not be inferred from spelling alone. |
| da | [dɐ] | duh |  | Contraction de + a. Different lexical and sound target from de. |
| mãe | [mɐ̃j̃] | MY˜ |  | Nasal central diphthong. |
| põe | [põj̃] | POY˜ |  | Nasal O plus y glide. |
| xarope | [ʃɐˈɾɔpɨ] | shuh·RAW·pih |  | x = sh, open stressed O, final weak e. |
| exame | [iˈzɐmɨ] | ee·ZUH·mih |  | x = z, initial e → i, stressed central A. |
| táxi | [ˈtaksi] | TAHK·see |  | x = ks. |
| máximo | [ˈmasimu] | MAH·see·moo |  | x = s. |
| leite | [ˈlɐjtɨ] | LIGHT·ih |  | Light plus a very brief final vowel. Do not stress the ending. |
| feira | [ˈfɐjɾɐ] | FIE·ruh |  | FIE rhymes with pie. Tap the r. |
| ouro | [ˈoɾu] | OH·roo |  | Standard target commonly monophthongizes written ou to [o]. |
| cabeleireiro | [kɐbɨlɐjˈɾɐjɾu] | kuh·buh·lie·RYE·roo |  | Both ei sequences have an eye-like glide. R in RYE and r in roo both mark taps. [9] |

## Cabeleireiro Worked Example

Infopédia transcribes cabeleireiro as kɐbəlɐjˈrɐjru. Its [ə] represents the reduced vowel and its r convention is normalized here to tap [ɾ], giving the internal target [kɐbɨlɐjˈɾɐjɾu]. Both ei sequences retain their glides. [9]

Careful pronunciation: kuh·buh·lie·RYE·roo. Stress RYE, keep the first two syllables light, and tap both r sounds. RYE uses a single tap R even in capitals. Here buh is a word-level scaffold for [ɨ], not a rule equating [ɨ] with [ɐ]. The English eye vowel is an approximation with a lower starting point. Do not remove the first glide through a mechanical unstressed-vowel rule. Add a natural form only when a supported reduction helps the learner.

## Output Quality Check

Before answering, verify:

- Resolve the target variety, lexical evidence, nasality, and phrase context before respelling. If a respelling looks like a direct English reading of Portuguese spelling, recheck the sound target. Example: onde → OH˜·dih, not AWN·dih.
- Independently compare the stressed syllable in the internal IPA target with the syllable in capitals. They must agree. For an acute or circumflex accent, verify that the accented syllable receives stress. Correct any mismatch.
- Confirm `r`/`rr`, `˜`, `‿`, `ly`, `ny`, and `zh` where needed in careful and connected-speech forms. Capitals affect stress only. Nasality adds no English n, m, or ng.
- Match every pronunciation explanation to the resolved sound and learner respelling. Use `r` for a tap and `rr` for strong R. Correct whichever element is erroneous if a note contradicts the target or respelling. Never assume word-final r is guttural.
- Apply the [separator rules](#learner-notation-rules) to all respellings and supported audio hints. Check unspaced interpuncts, carefully aligned word bars, connected-speech regrouping, and `\|` Markdown escaping of bars in learner-facing Markdown, including table cells. Do not put an interpunct inside a diphthong.
- Check that natural speech contains the same Portuguese wording. Apply [SKILL.md: Final Quality Check](../SKILL.md#final-quality-check) for field presence, unchanged-message handling, typography, and supporting sections.
- Read the remaining respelling with American-English instincts, checking weak vowels and whole diphthongs. Explain unfamiliar marks locally and include [articulation guidance](#articulation-guidance) when required.
- Keep repeated words consistent in the same context unless evidence or feedback supports a change.
- Never claim a source check or audio review that did not occur.

## Voice Mode Behavior

In Voice mode, pronounce the Portuguese itself with PT-PT sounds, never the English respelling. Give careful speech first and a natural version second when meaningfully different. Preserve Portuguese stress, reduction, rhythm, linking, and consonants. Do not claim regional precision or audio assessment beyond the available voice capabilities.

## Source Hierarchy and Evidence

Use the sources below as evidence for the phonetic system and calibration. They are not scripts to reproduce. When a current, reliable word-specific transcription conflicts with an older learner respelling, update the learner respelling to match the phonetic target. When reputable sources use different IPA symbols for the same reduced vowel, interpret the phonetic description without treating symbol choice alone as a contradiction.

[1] Camões IP, A Pronúncia do Português Europeu. https://cvc.instituto-camoes.pt/cpp/acessibilidade/capitulo1_2.html Defines the Lisbon-Coimbra region as the standard reference and provides a systematic pronunciation course.

[2] Madalena Cruz-Ferreira, European Portuguese, Journal of the International Phonetic Association. https://doi.org/10.1017/S0025100300005223 Broad IPA description of European Portuguese consonants and vowels.

[3] Shu-hao Shih, Phonetics of European Portuguese stress: A nonce word experiment, JIPA. https://www.cambridge.org/core/journals/journal-of-the-international-phonetic-association/article/phonetics-of-european-portuguese-stress-a-nonce-word-experiment/812DC040F6261A4A4AD14D0FFB76A711 Summarizes the standard unstressed-vowel reduction pattern and discusses [ɨ] versus older [ə] notation.

[4] Ana Maria Martins, Portugal, The Oxford Handbook of the Portuguese Language, 2026. https://academic.oup.com/edited-volume/63048/chapter-abstract/566525577 Current overview including European Portuguese unstressed-vowel reduction.

[5] Infopédia, Dicionário de Português para Estrangeiros and Dicionário da Língua Portuguesa. https://www.infopedia.pt/dicionarios/portugues-estrangeiros Useful word-specific phonetic transcriptions. Calibration checks include muito, seis, nove, bem, mãe, olá, casa, hoje, and others.

[6] Ciberdúvidas, O ditongo ei em Portugal. https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/o-ditongo-ei-em-portugal/35054 Describes standard Portuguese ei approximately as [ɐj] and distinguishes it from [aj].

[7] Ciberdúvidas, A conservação do ditongo ou. https://ciberduvidas.iscte-iul.pt/consultorio/perguntas/a-conservacao-do-ditongo-ou/33036 Describes [o] as the standard Lisbon-Coimbra realization of many written ou sequences, with preserved diphthongs regionally.

[8] Infopédia entry for muito. https://www.infopedia.pt/dicionarios/portugues-estrangeiros/muito Gives the Portugal pronunciation [ˈmũj̃tu].

[9] Infopédia, cabeleireiro. https://www.infopedia.pt/dicionarios/lingua-portuguesa/cabeleireiro Word-specific transcription checked for this revision on 24 September 2026. The respelling is a VIVAaLingua teaching choice.
