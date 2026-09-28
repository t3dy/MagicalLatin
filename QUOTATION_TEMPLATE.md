# Quotation Entry Template

## What a Complete Quotation Looks Like

This document shows the exact format and fields needed for a production-ready quotation entry.

## Full Example: Complete Quotation

```json
{
  "slug": "quod-superius-inferius",
  "latin_text": "Quod est superius, est sicut quod inferius; et quod est inferius, est sicut quod est superius, ad perpetranda miracula rei unius.",
  "translation": "That which is above is like that which is below; and that which is below is like that which is above, to accomplish the miracles of the one thing.",
  "source_author": "Hermes Trismegistus",
  "source_work_title": "Emerald Tablet (Tabula Smaragdina)",
  "source_text_slug": "grimoires-a-history-of-magic-books-2009-libgen-li",
  "referenced_in_slug": "grimoires-a-history-of-magic-books-2009-libgen-li",
  "scholar_name": "Owen Davies",
  "quotation_context": "Foundation principle of correspondence in magical philosophy, cited as central to European grimoire tradition",
  "page_reference": "General reference in grimoire discussion",
  "linguistic_notes": "Latin translation of Arabic original (Balinas/Hermes Trismegistus). The bidirectional structure (superius/inferius) reflects the principle of correspondence. Medieval translation uses classical constructions. 'Miracles' (miracula) connects magical operations to divine action.",
  "magical_significance": "Most fundamental principle in Western magic. Establishes theoretical basis for sympathetic magic and correspondential operations. If all creation is interconnected (macrocosm/microcosm), then working with any part affects the whole. Justifies construction of talismans, sigils, and ritual correspondences aligned with celestial/elemental forces.",
  "scholar_commentary": "Davies demonstrates how this principle enabled European mages to construct complex systems of correspondence linking celestial bodies, metals, stones, plants, and spiritual entities. The principle remains central to modern magical practice. Represents the synthesis of Platonic philosophy with mystical theology in magical tradition.",
  "tags": ["emerald-tablet", "correspondence", "hermetic-principle", "sympathetic-magic", "grimoire-tradition"],
  "source_method": "MANUAL_EXTRACTION",
  "review_status": "DRAFT",
  "confidence": "HIGH"
}
```

## Field Breakdown

### Identification

**`slug`** (REQUIRED, unique)
- URL-friendly identifier
- Format: `lowercase-with-hyphens`
- Source: First 50 chars of latin_text, slugified
- Example: `quod-superius-inferius` (from "Quod est superius...")
- Uniqueness: Must not duplicate existing slugs
- Check: `sqlite3 portal.db "SELECT slug FROM quotations WHERE slug = 'X'"`

### The Quotation Itself

**`latin_text`** (REQUIRED, exact from source)
- The actual Latin passage
- Must be verifiable against original PDF
- Length: 20-500 characters (typical: 80-200)
- Format: Plain text, preserve original spelling/punctuation
- ❌ DO NOT paraphrase or modernize
- ❌ DO NOT include surrounding words unless part of quotation
- ✓ DO verify you can find this exact text in the source PDF

**`translation`** (RECOMMENDED, good English)
- English translation of Latin text
- Preserve original sense; translation guides understanding
- NOT an interpretation (that goes in commentary)
- Length: roughly same as Latin (may vary by language structure)
- Format: Idiomatic English that sounds natural
- ✓ DO: "That which is above is like that which is below"
- ❌ DON'T: "The thing-which-is above is-similar-to thing-below" (wooden)
- Verification: Does someone unfamiliar with Latin understand the meaning?

### Source Attribution

**`source_author`** (REQUIRED)
- Author of the original work being quoted
- Format: "Firstname Lastname" or "Ancient Author (Latin Name)"
- Examples: "Hermes Trismegistus", "Paracelsus", "Marsilio Ficino"
- Historical: Use common English form (not native language spelling)
- Pseudonymous: "Author Unknown" if truly unknown; link to actual author if known
- Check: Must match existing figures table or be creatable

**`source_work_title`** (REQUIRED)
- Title of the work containing this quotation
- Format: As commonly cited in scholarship
- Examples: "Corpus Hermeticum", "Emerald Tablet", "Picatrix", "Three Books of Occult Philosophy"
- Include: Edition info only if significantly different versions (e.g., "Zohar, Mantua edition")
- Translation: Original language title if work translated (explain in linguistic_notes)
- Check: Does this work exist in texts table? If not, note where found

**`source_text_slug`** (REQUIRED, must validate)
- Must reference existing texts.slug
- If work not in database: Add to texts table first
- Check query: `sqlite3 portal.db "SELECT slug FROM texts WHERE title LIKE '%Corpus%Hermeticum%'"`
- If no match: You need to find/add this text first

**`referenced_in_slug`** (REQUIRED, must validate)
- The scholarly work that discusses this quotation
- Must be texts.slug of the scholar's analysis
- Example: "grimoires-a-history-of-magic-books-2009-libgen-li" (Owen Davies' work)
- Check: `sqlite3 portal.db "SELECT slug, title FROM texts WHERE authors LIKE '%Davies%'"`

### Scholarly Attribution

**`scholar_name`** (REQUIRED)
- Name of scholar who discusses/cites this quotation
- Format: "Firstname Lastname"
- Examples: "Owen Davies", "Brian Copenhaver", "François Secret"
- Must match figures table (or be creatable)
- Can be modern scholar OR ancient author if quoting their interpretation

**`quotation_context`** (REQUIRED, 1-2 sentences)
- Where does this quotation appear in the source work?
- What is its role in the text?
- Examples:
  - "Opening invocation in Hermetic cosmology establishing divine principle"
  - "Principle of correspondence in magical philosophy, foundational to grimoire tradition"
  - "Explanation of how celestial forces influence terrestrial operations"
- Purpose: Reader should understand why this quotation matters without reading the whole source

**`page_reference`** (REQUIRED)
- Where in the source work is this found?
- Format: "p. XX", "pp. XX-YY", "Tract I", "Chapter 3, Section 2", "Folio 42r"
- Example: "p. 42" or "Tract III, Tractate 7"
- Verification: You can point someone to exactly where this appears
- Check: Is this information in the PDF you're citing?

### Analysis & Commentary

**`linguistic_notes`** (REQUIRED, 2-4 sentences)
- Technical language analysis
- Grammar: cases, tenses, constructions, unusual syntax
- Vocabulary: rare terms, technical terminology, wordplay
- Style: rhetoric, devices, translation choices
- Context: language variants (classical vs. medieval Latin?)
- Examples:
  - "Medieval Latin translation. The term 'daemon' (Greek daimon) refers to spirit/intelligence, not necessarily evil. Conditional construction 'ut compareas' establishes magician's imperative authority."
  - "Classical Latin with perfect symmetry (superius/inferius structure). The bidirectional formulation reflects philosophical correspondence. 'Miracula' connects magical operations to divine action."

**`magical_significance`** (REQUIRED, 3-5 sentences)
- Why does this matter to magical theory & practice?
- What principle does it establish or exemplify?
- How did/do practitioners use this concept?
- What does it enable or justify magically?
- Examples:
  - "Foundation of correspondence magic. Establishes that microcosm mirrors macrocosm, so working with any part (herb, stone, sigil) affects the whole. Justifies talismanic magic, sympathetic operations, astrological correspondence."
  - "Most fundamental principle in Western magic. Provides theoretical basis for understanding how words and symbols connect to reality. Enables magical operations to access and influence cosmic principles."

**`scholar_commentary`** (REQUIRED, 3-5 sentences)
- How does the scholar interpret this quotation?
- What does it mean historically/philosophically?
- What does it reveal about magical tradition?
- How does it fit the scholar's argument?
- Examples:
  - "Davies demonstrates how this principle enabled mages to construct complex correspondence systems linking celestial bodies, metals, stones, and entities. Shows European grimoire tradition integrated philosophical frameworks with practical operations."
  - "Copenhaver argues this represents synthesis of Platonic philosophy with mystical theology. The logos doctrine provided Renaissance mages framework for understanding how symbols affect reality through connection to divine principle."

### Metadata & Status

**`tags`** (RECOMMENDED, JSON array)
- Keywords for discovery
- Format: ["tag1", "tag2", "tag3"]
- Use: Tradition, concept, practice type
- Examples: ["emerald-tablet", "correspondence", "hermetic-principle", "sympathetic-magic"]
- Do NOT over-tag (3-8 tags is ideal)

**`source_method`** (REQUIRED)
- How was this quotation entered?
- Values: "MANUAL_EXTRACTION" (human found it), "EXTRACTED" (automated)
- Set to MANUAL_EXTRACTION if you're typing this entry

**`review_status`** (REQUIRED)
- Set to "DRAFT" when first entered
- Later updated to "REVIEWED" after fact-checking
- Finally "VERIFIED" after multiple-source confirmation
- Start: Always "DRAFT"

**`confidence`** (REQUIRED)
- How confident are you in this entry?
- Values: "HIGH" (verified against PDF), "MEDIUM" (likely correct), "LOW" (candidate, needs work)
- Start: "MEDIUM" unless you've verified it yourself
- Set to "HIGH" only after checking original PDF

## Validation Checklist

Before marking a quotation COMPLETE, verify:

- [ ] `latin_text` — Found exact text in source PDF (take screenshot if needed)
- [ ] `translation` — Makes sense in English, preserves Latin meaning
- [ ] `source_author` — Matches historical records, correct spelling
- [ ] `source_work_title` — Work exists, title is accurate
- [ ] `source_text_slug` — MUST reference existing texts.slug
- [ ] `referenced_in_slug` — MUST reference scholar's work in texts table
- [ ] `scholar_name` — Scholar correctly identified, can be found in figures table
- [ ] `quotation_context` — Reader understands why this quotation matters
- [ ] `page_reference` — Can point someone to exact location
- [ ] `linguistic_notes` — Covers grammar, vocabulary, style, translation issues
- [ ] `magical_significance` — Explains what principle this demonstrates
- [ ] `scholar_commentary` — Reflects actual scholarly interpretation
- [ ] `tags` — 3-8 relevant keywords, no duplicates
- [ ] `source_method` — Set correctly (MANUAL_EXTRACTION for hand-entry)
- [ ] `review_status` — Set to DRAFT for new entries
- [ ] `confidence` — HIGH/MEDIUM/LOW appropriately set

## Common Mistakes & How to Fix Them

### ❌ Mistake: Slug collision
```json
"slug": "correspondence"  // Too generic, may duplicate
```
**Fix:** Use more specific text
```json
"slug": "quod-superius-correspondence"  // Unique, identifies specific quotation
```

### ❌ Mistake: Paraphrased Latin
```json
"latin_text": "That which is above is similar to that which is below"  // This is translation, not Latin!
```
**Fix:** Use exact Latin
```json
"latin_text": "Quod est superius, est sicut quod inferius..."
```

### ❌ Mistake: Missing source verification
```json
"source_text_slug": "corpus-hermeticum"  // You haven't checked if this exists in texts table
```
**Fix:** Verify first
```bash
sqlite3 portal.db "SELECT slug FROM texts WHERE slug LIKE '%hermet%'" 
# If no result, need to find correct slug or add text to database first
```

### ❌ Mistake: Vague commentary
```json
"magical_significance": "This is important to magic"  // Why? How?
```
**Fix:** Be specific
```json
"magical_significance": "Establishes correspondence between levels of reality, enabling sympathetic magic where operations on microcosm affect macrocosm. Practitioners use this to construct talismans attuned to specific celestial/elemental forces."
```

### ❌ Mistake: No translation
```json
"translation": null  // Reader can't understand the Latin
```
**Fix:** Provide translation (unless it's a proper noun or extremely simple)
```json
"translation": "That which is above is like that which is below..."
```

## Real Examples in Database

See `data/quotations_seed.json` for 4 complete exemplars showing:
1. Hermetic principle ("Quod est superius...")
2. Goetia binding ("Conjuro te, daemon...")
3. Alchemy ("Ignis, Aer, Aqua, Terra...")
4. World soul ("Universus hic mundus...")

## For Writers: How to Write Each Section

### Writing `linguistic_notes`
1. Identify the language (Classical Latin? Medieval? Translation from Arabic?)
2. Note any unusual grammar (cases, tenses, constructions)
3. Explain key terms (unusual vocabulary, technical language)
4. Mention rhetorical devices (parallelism, symmetry, etc.)
5. Say why the language choices matter

**Example:**
"Medieval Latin translation from Arabic original. The paired structure (superius/inferius) mirrors the principle being explained. Classical Latin constructions create authoritative tone. 'Miracula' (miracles) intentionally links magical operations to divine action through word choice."

### Writing `magical_significance`
1. What principle does this exemplify?
2. How would a practitioner use this understanding?
3. What does it enable or justify?
4. Why would someone memorize or invoke this?
5. Connect to broader magical worldview

**Example:**
"Foundation of sympathetic magic. Establishes that working on one level of reality (making a talisman, speaking a word of power) can influence other levels (celestial spheres, material effects). Allows practitioners to construct operations linking earth, planets, and spirits through understood correspondences."

### Writing `scholar_commentary`
1. What does the scholar say this means?
2. How does it fit historical context?
3. What does it reveal about the tradition?
4. Does it resolve a debate or clarify something?
5. Why did the scholar highlight this quotation?

**Example:**
"Copenhaver shows how Hermetic philosophy provided Renaissance mages theoretical justification for magical operations. The logos doctrine meant that words, symbols, and correspondences could genuinely affect reality because they connected to divine principle. This allowed mages to integrate magic into Christian theology."

---

**Status:** Template created. Use this format for all new quotations. 4 exemplars follow this structure exactly.
