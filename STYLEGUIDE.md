# Magical Latin: Style Guide for Passage and Card Entries

This guide governs every entry in `data/passages.json`. Read it before adding, editing, or reviewing any passage. The content standard draws on the medievalmagicdb EmeraldTablet discipline (see `C:\Dev\medievalmagicdb\STYLEGUIDE.md`) adapted for a reader-facing educational application rather than a scholarly portal.

---

## The Two Entry Types

### Full Passages
2–5 sentences of Latin with complete vocabulary, English gloss, source notes, and bibliography. These are the primary educational content. Currently ~101 in the corpus.

### Short Entries (one or two sentences)
A single representative Latin sentence or a two-sentence excerpt, with vocabulary (2–3 words), a brief gloss, and source notes. Designed for breadth: covering more texts, authors, and concepts with lighter editorial overhead. Target: 200+ in the corpus. Short entries follow the same JSON schema but have `"entry_type": "short"` and shorter `source_notes` (2–4 sentences only).

---

## JSON Schema

Every passage object must have all of these fields. No field may be omitted; use `null` only for `ritual_id`.

```json
{
  "id": "author-shorttitle-keyword",
  "entry_type": "full",
  "title": "Latin Title — Latin Subtitle",
  "title_english": "English Title — English Subtitle",
  "source": "Full Source Title",
  "author": "Author Name (attrib. if pseudepigraphic)",
  "date": "c. YYYY CE  |  YYYY–YYYY  |  c. Xth century",
  "era": "ancient | medieval | renaissance",
  "tradition": "tradition_underscore",
  "category": "category_slug",
  "difficulty": 1,
  "representative_sentence": "Single best Latin sentence for the card preview.",
  "latin_text": "2–5 sentences for full entries; 1–2 for short entries.",
  "english_gloss": "Close English translation of the latin_text.",
  "vocabulary": [
    {"word": "form as it appears", "lemma": "dictionary form", "definition": "word — magical/scholarly significance in context"}
  ],
  "has_ritual": false,
  "ritual_id": null,
  "tags": ["Author surname", "short title", "topic", "era/place"],
  "source_notes": "1–3 paragraphs for full; 2–4 sentences for short. Scholarly context.",
  "bibliography": "Author, Firstname. Title. Place: Publisher, Year. // Second source."
}
```

### Field-by-Field Rules

**`id`** — kebab-case, globally unique. Format: `author-shorttitle-keyword`. Examples: `agrippa-dop-i1`, `picatrix-i2`, `defixio-aquae-sulis`. Never include years in the id. Never use spaces.

**`entry_type`** — `"full"` or `"short"`. Short entries have 1–2 vocabulary items and 2–4 sentence source_notes. If omitted, treated as `"full"`.

**`title`** — Latin source title, em-dash, descriptive Latin subtitle. Do not translate here. Example: `Asclepius — De Deo et Mundo`.

**`title_english`** — English title, em-dash, English descriptive subtitle. Example: `Asclepius — On God and World`.

**`source`** — Full formal name of the source text, as a scholar would cite it. Include book/chapter if relevant: `De Occulta Philosophia Libri Tres, Liber I, Caput xiv`.

**`author`** — Attributed author as commonly cited in scholarship. Add `(attrib.)` for pseudepigrapha: `Anonymous (attrib. Aristotle; trans. Gerard of Cremona)`. Use `Anonymous` if no attribution exists.

**`date`** — Use `c.` for approximate dates. Use CE/BCE for ancient texts where ambiguity exists. Prefer ranges for texts with uncertain composition: `c. 1250–1300`. For Arabic-to-Latin translations, give both: `Arabic c. 10th c.; Latin trans. c. 1187`.

**`era`** — One of three values only:
- `ancient` — Classical antiquity through Late Antiquity (up to c. 700 CE)
- `medieval` — Early to late Middle Ages (c. 700–1450)
- `renaissance` — Renaissance and early modern (c. 1450–1700)

**`tradition`** — Must use underscore_case. Current normalized values:
- `natural_magic` — operative use of hidden natural properties
- `hermetic` — Hermetic philosophy, Corpus Hermeticum, prisca theologia tradition
- `neoplatonic` — Neoplatonic/theurgical philosophy (Plotinus, Iamblichus, Proclus, Ficino)
- `angelic_magic` — invocation of angels, revealed knowledge, Ars Notoria tradition
- `astrological` — astral causation, image magic, lunar mansions, talismans
- `alchemy` — transmutational and spiritual alchemy
- `solomonic` — grimoires invoking Solomonic authority, Clavicula tradition
- `folk_magic` — popular/vernacular charms, incantations, healing magic
- `demonology` — classification and combat of demons, witch theory
- `kabbalistic` — Christian and Jewish Kabbalah, divine names
- `necromancy` — communication with the dead, underworld descent
- `divination` — sortilege, geomancy, chiromancy, hydromancy, astrology as practice
- `classification` — encyclopedic classification of magic types
New traditions may be added but must be underscore_case and logged in this guide.

**`category`** — More granular than tradition. Free-form slug, lowercase. Examples: `ritual_magic`, `natural_philosophy`, `alchemy`, `healing_magic`, `pastoral_care`, `theurgy`, `witchcraft`, `exorcism`, `divination`, `curse_magic`, `spirit_lore`.

**`difficulty`** — Integer 1–5. Displayed as ✦ symbols on cards.
- `1` ✦ — Simple, post-classical Latin; short formulaic sentences; basic vocabulary
- `2` ✦✦ — Standard medieval Latin; accessible syntax; subject matter manageable
- `3` ✦✦✦ — Technical Latin; specialized magical/alchemical/philosophical vocabulary
- `4` ✦✦✦✦ — Dense scholastic or Neoplatonic Latin; complex syntax; substantial vocabulary load
- `5` ✦✦✦✦✦ — Highly technical, archaic, deliberately obscure, or polyglot (Greek/Hebrew/Arabic terms); expert level

**`representative_sentence`** — The single best sentence to represent the passage on a card. Must be: complete and grammatical, representative of the passage's topic and voice, striking enough to invite clicking. Not a summary — a real sentence from the source or closely based on it.

**`latin_text`** — For full entries: 2–5 sentences. For short entries: 1–2 sentences. This may be a verbatim quotation from the critical edition, a composite of multiple sentences from the same source, or (for untranslated texts) a carefully composed Latin passage representative of the source's content and period style. Never invent content not in the source. Note in `source_notes` if the text is a composite or representative reconstruction.

**`english_gloss`** — A close, working translation of `latin_text`, prioritizing accuracy over style. Not a literary translation — a crib. Every sentence in `latin_text` must have a corresponding sentence in `english_gloss`.

**`vocabulary`** — Array of 3–5 items for full entries, 2–3 for short entries. Each item:
- `word`: the form as it appears in `latin_text` (not necessarily lemma form)
- `lemma`: standard dictionary form (nominative singular for nouns; infinitive for verbs)
- `definition`: word in English, em-dash, then a short explanation of its specific magical, philosophical, or scholarly significance in this context. Not a bare dictionary gloss. Example: `"definition": "sympathia — the hidden affinity linking different levels of reality; the operative basis of talismanic magic"`

**`has_ritual`** — `true` only if a corresponding entry exists in `data/rituals.json`.

**`ritual_id`** — The matching id string in `data/rituals.json`, or `null`.

**`tags`** — Array of 4–8 strings. Always include: author surname, source short title, primary topic, era/place. Tags drive search. Use standard capitalizations: `"Agrippa"`, not `"agrippa"`.

**`source_notes`** — For full entries: 2–4 sentences of scholarly context. Must include: what the source is, when it was written, why it matters for the history of magic, and one or two scholarly anchors (names, debates). For short entries: 2–4 sentences only.

Do not write source_notes in promotional or mystical register. Write as a critical historian. Mark actor terms versus analyst terms. Identify evidentiary status of claims.

**`bibliography`** — Critical edition or standard scholarly translation, in full bibliographic form. Format: `Author, Firstname. Title. Place: Publisher, Year.` Two sources separated by ` // `. Do not use URLs as substitutes for bibliographic data. If no critical edition exists, cite the best available scholarly discussion of the text. If uncertain, a web-research agent should be spawned to verify.

---

## Coverage Requirements

The passage corpus must represent every concept in the medievalmagicdb concepts taxonomy. The canonical list is maintained in `C:\Dev\medievalmagicdb\scripts\seed_comprehensive_coverage.py` and related batch files. Current concepts requiring coverage:

**Must have at least one passage:**
Amulets, Angelic Invocation, Ars Notoria, Astral Image Magic, Astrological Influence, Celestial Influence, Characters and Seals, Charms, Chiromancy, Clerical Underworld, Condemned Arts, Confession / Pastoral Care, Demonology, Demonic Pact, Divination, Exorcism, Experimental Science, Familiar Spirit, Geomancy, Grimoire, Grimoire Corpus, Hydromancy, Learned Magic, Licit and Illicit Knowledge, Magical Alphabets, Maleficium, Mathematical Arts, Natural Powers, Necromancy, Nigromantia, Notae, Occult Properties, Planetary Spirits, Prohibited Arts, Pseudepigraphy, Ritual Diagrams, Ritual Purity, Secret Names, Secret of Secrets, Solomonic Magic, Sortilege, Scholastic Classification of Magic, Superstitio, Suffumigation, Talismans, University Condemnation, Voces Magicae, Witchcraft

When adding new passages, cross-reference this list and `data/passages.json` tags before selecting topics.

---

## The Timeline Obligation

The corpus must represent the complete intellectual history of Latin magical writing from Classical antiquity through the early modern period. Anchor texts that must be present:

**Ancient (to c. 700 CE):** Virgil's witchcraft (Eclogues, Aeneid VI), Horace's Canidia, Lucan's Erictho, Ovid's Medea, Pliny on magic, Apuleius (Apologia + Metamorphoses III), Cicero on divination, Curse tablets (defixiones), Marcellus Empiricus, Augustine (City of God X), Plotinus (Enneads IV.4), Iamblichus (De Mysteriis), Proclus (De Sacrificio), Pseudo-Dionysius (Divine Names), Porphyry (Letter to Anebo), Firmicus Maternus, Macrobius, Hermetica (Tabula Smaragdina, Asclepius), Martin of Braga.

**Medieval (c. 700–1450):** Isidore (Etymologiae VIII), Hugh of St Victor (Didascalicon), Al-Kindi (De Radiis), Picatrix, Speculum Astronomiae, Ars Notoria, Liber Juratus (Sworn Book), Liber Razielis, Liber Lunae, Clavicula Salomonis, Heptameron, John of Salisbury (Policraticus), Roger Bacon (Opus Majus + De Secretis), Albertus Magnus, Thomas Aquinas, William of Auvergne, Liber de Causis, Michael Scot, Arnald of Villanova (Rosarium), Geber (Summa Perfectionis), Burchard of Worms (Decretum X), Sortes Sanctorum, Tempier Condemnations (1277), Munich Manual, John of Morigny (Liber Florum), Secretum Secretorum, Ramon Lull, Hildegard (Physica), Geomancy, Nider (Formicarius).

**Renaissance (c. 1450–1700):** Ficino (De Vita, De Amore), Pico (Oratio, Conclusiones), Reuchlin (De Arte Cabalistica, De Verbo Mirifico), Giorgio (De Harmonia Mundi), Agrippa (De Occulta Philosophia I–III, De Incertitudine), Paracelsus (Philosophia Sagax, Liber de Nymphis), Trithemius (Steganographia, Antipalus), Dee (Propaedeumata, Monas, Spirit Diaries), Bruno (De Umbris, De Magia, De Vinculis), Della Porta (Magia Naturalis), Cardano (De Subtilitate), Campanella (De Sensu Rerum), Malleus Maleficarum, Weyer (De Praestigiis), Nider (Formicarius), Ripley (Medulla), Khunrath (Amphitheatrum), Maier (Atalanta Fugiens), Kircher (Oedipus Aegyptiacus, Mundus Subterraneus), Fludd (Utriusque Cosmi), Arbatel, Indagine (Chiromantia), Ars Almadel.

---

## Short Entry Standard (200+ Corpus)

Short entries extend coverage to texts that matter historically but do not require a full passage. They follow the full schema but with reduced content:

- `entry_type`: `"short"`
- `latin_text`: 1–2 sentences maximum
- `vocabulary`: 2–3 items
- `source_notes`: 2–4 sentences only (what it is, when, why it matters)
- `bibliography`: same standard as full entries

Good candidates for short entries:
- Individual spells or recipes from larger collections (Lacnunga, Medicina de Quadrupedibus)
- Condemnation canons from councils (Elvira, Laodicea, Vannes, Toledo)
- Single famous sentences from well-known authors (Seneca on magic, Tacitus on magi)
- Brief technical definitions from encyclopedists (Vincent of Beauvais, Bartholomaeus Anglicus)
- Individual Psalm texts with magical use history
- Single aphorisms from astrological or alchemical collections
- Glossary entries from legal texts defining magical offenses

---

## Bibliography Protocol

### Format

```
Author, Firstname. Title in Italics Form. Place: Publisher, Year.
```

For articles:
```
Author, Firstname. "Article Title." Journal Name Vol (Year): Pages.
```

Multiple references separated by ` // `.

### Verification

If uncertain about a critical edition, spawn a web-research agent with the specific query. Prefer:
1. A modern critical edition with Latin text (e.g., CCSL, CCCM, Teubner, Les Belles Lettres, Loeb)
2. A peer-reviewed scholarly translation with introduction (e.g., Cambridge, Penn State, Brill, MRTS)
3. A significant scholarly monograph that edits or deeply analyses the text

Never use URLs as bibliography entries. A URL may appear in source_notes parenthetically only if it points to a stable institutional resource (JSTOR doi, manuscript catalogue entry).

### Key Reference Series to Check

- **Corpus Christianorum Series Latina (CCSL)** — patristic and early medieval Latin
- **Corpus Christianorum Continuatio Mediaevalis (CCCM)** — medieval Latin continuation
- **Corpus Medicorum Latinorum (CML)** — medical texts
- **Loeb Classical Library** — Greek and Latin with facing translation
- **Les Belles Lettres (Budé)** — French critical editions of classical texts
- **Medieval & Renaissance Texts & Studies (MRTS/ACMRS)** — Binghamton/Tempe
- **Pontifical Institute of Mediaeval Studies (PIMS)** — Toronto
- **Brill** — Arabic-Latin transmission, scholastic philosophy
- **Penn State University Press** — grimoire studies, magic history
- **SISMEL / Edizioni del Galluzzo** — Italian series for medieval learned magic

---

## Prohibited Practices

Do not write entries in an operational, instructional, or how-to register. Describe ritual content historically; do not convert it into practical guidance.

Do not write promotional prose ("powerful ritual," "real magic," "ancient secrets") outside of quotation or source analysis.

Do not treat manuscript attributions as certain authorship without noting pseudepigraphy, compilation, or textual instability.

Do not assign difficulty 1 or 2 to highly technical philosophical texts, or difficulty 4–5 to simple formulaic texts.

Do not omit the `bibliography` field or use placeholder text in it. If the edition is unknown, say what type of resource is needed and flag for follow-up.

Do not invent Latin text. If no verbatim source is quotable, compose a closely representative passage in appropriate period style and note in `source_notes` that it is a representative reconstruction. Never claim invented text is a direct quotation.

---

## Scholarly Voice

Write source_notes as a critical historian of ideas. Standard scholarly anchors for this corpus:

- **Richard Kieckhefer** — clerical underworld, learned magic, *Forbidden Rites*, *Magic in the Middle Ages*
- **Claire Fanger** — angelic magic, visionary practice, *Invoking Angels*, John of Morigny
- **Frank Klaassen** — manuscript transmission, *Transformations of Magic*, Elizabethan magic
- **Sophie Page** — codicology, *Magic in the Cloister*, monastic contexts
- **Michael D. Bailey** — demonology, religion/superstition, Nider, *Battling Demons*
- **Frances A. Yates** — Hermetic tradition, Bruno, memory, Rosicrucians
- **D.P. Walker** — spiritual magic, Ficino, *Spiritual and Demonic Magic*
- **Brian P. Copenhaver** — Hermetica, Renaissance magic, *Magic in Western Culture*
- **William R. Newman** — alchemy, Geber, *The Summa Perfectionis*
- **William Eamon** — secrets, natural magic, Della Porta
- **Deborah Harkness** — John Dee, Elizabethan science
- **Paola Zambelli** — Speculum Astronomiae, Albertus, astrology
- **Charles Burnett** — Arabic-Latin transmission, astrology, Picatrix
- **Dan Attrell / David Porreca** — Picatrix modern translation

Cite names and works, not vague "scholars say." State disagreements where they exist.
