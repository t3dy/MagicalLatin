# MagicalLatin Quotations Database Guide

## Overview

The MagicalLatin knowledge portal now includes a comprehensive **quotations database** capturing significant Latin passages from magical texts as cited by scholars, complete with linguistic and magical analysis.

**Current Status:**
- ✅ 4 example quotations seeded with full commentary
- ✅ Portal pages generated (quotations/index.html + detail pages)
- ✅ Extraction framework created (quotation_extractor.py)
- ✅ Seeding pipeline ready (seed_quotations.py)
- ⏳ Ready for scaling: extract from 445 scholarly PDFs

## Database Schema

Three tables hold quotation data with full provenance tracking:

### 1. `quotations` Table
Main quotation records with metadata and commentary:

| Column | Type | Purpose |
|--------|------|---------|
| `id` | INTEGER | Primary key |
| `slug` | TEXT | URL-friendly identifier |
| `latin_text` | TEXT | The actual Latin quotation |
| `translation` | TEXT | English translation (optional) |
| `source_text_slug` | TEXT | Which work the quote is from |
| `source_author` | TEXT | Author of the original work |
| `source_work_title` | TEXT | Title of original work |
| `referenced_in_slug` | TEXT | Which scholarly work cites it |
| `scholar_name` | TEXT | Scholar who discusses it |
| `quotation_context` | TEXT | Where in the work it appears |
| `linguistic_notes` | TEXT | Grammar, vocabulary, style notes |
| `magical_significance` | TEXT | Why this matters magically |
| `page_reference` | TEXT | Page/section in citing work |
| `scholar_commentary` | TEXT | Main scholarly interpretation |
| `tags` | TEXT | JSON array of tags |
| `source_method` | TEXT | How it was entered (MANUAL_EXTRACTION, EXTRACTED) |
| `review_status` | TEXT | DRAFT → REVIEWED → VERIFIED |
| `confidence` | TEXT | HIGH / MEDIUM / LOW |

### 2. `quotation_sources` Table
Links quotations to their original sources:

| Column | Type | Purpose |
|--------|------|---------|
| `quotation_id` | INTEGER | FK to quotations |
| `original_source_slug` | TEXT | Original work slug |
| `page_number` | TEXT | Page in original |
| `section` | TEXT | Section/chapter |
| `manuscript_reference` | TEXT | MS reference if applicable |

### 3. `quotation_commentary` Table
Separate commentary entries allow multiple interpretations per quotation:

| Column | Type | Purpose |
|--------|------|---------|
| `quotation_id` | INTEGER | FK to quotations |
| `scholar_slug` | TEXT | Scholar identifier |
| `scholar_name` | TEXT | Scholar name |
| `commentary_text` | TEXT | The commentary itself |
| `commentary_type` | TEXT | linguistic / magical / historical / textual / comparative |
| `significance_level` | TEXT | high / medium / low |

## How the System Works

### Entry Points

**Three scripts handle the quotation lifecycle:**

1. **`quotation_extractor.py`** — Find candidates
   - Scans E:\pdf folders for quoted text patterns
   - Identifies likely Latin quotations
   - Outputs `quotation_candidates.json` for review
   - Also creates `quotations_manual.json` template

2. **`seed_quotations.py`** — Populate database
   - Reads `data/quotations_seed.json`
   - Validates against existing texts
   - Seeds quotations + commentary tables
   - All idempotent (safe to re-run)

3. **`build_site_final.py`** — Generate HTML
   - Reads database
   - Generates quotations/index.html (card grid)
   - Generates quotations/{slug}/index.html (detail pages)
   - Updates navigation across all pages

### Data Flow

```
E:\pdf folders
    ↓
quotation_extractor.py (scan PDFs)
    ↓
quotation_candidates.json (review & verify)
    ↓ (manual curation)
quotations_manual.json (hand-entered, high-quality)
    ↓ (merge both sources)
data/quotations_seed.json
    ↓
seed_quotations.py (insert into DB)
    ↓
portal/portal.db
    ↓
build_site_final.py (generate HTML)
    ↓
docs/quotations/
```

## Adding Quotations

### Method 1: Manual Entry (Recommended)

Edit `data/quotations_manual.json` following this structure:

```json
{
  "_instructions": "...",
  "quotations": [
    {
      "latin_text": "Quod est superius...",
      "translation": "That which is above...",
      "source_text_slug": "grimoires-a-history-of-magic-books-2009-libgen-li",
      "source_author": "Hermes Trismegistus",
      "source_work_title": "Emerald Tablet",
      "referenced_in_slug": "grimoires-a-history-of-magic-books-2009-libgen-li",
      "scholar_name": "Owen Davies",
      "quotation_context": "Davies cites the Emerald Tablet...",
      "page_reference": "p. 42",
      "linguistic_notes": "Latin translation of Arabic original...",
      "magical_significance": "Foundation principle of correspondence...",
      "scholar_commentary": "Davies shows how this principle...",
      "tags": ["emerald-tablet", "correspondence", "hermetic-principle"]
    }
  ]
}
```

### Method 2: Extraction from PDFs

Use the extraction framework for semi-automated candidate detection:

```bash
# 1. Extract candidates from E:\pdf
python portal/scripts/quotation_extractor.py
# → Creates quotation_candidates.json with high-confidence guesses

# 2. Review candidates
# Open data/quotation_candidates.json
# Copy verified ones into data/quotations_manual.json

# 3. Seed and build
python portal/scripts/seed_quotations.py
python portal/scripts/build_site_final.py

# 4. Commit
git add docs/ data/quotations*.json
git commit -m "Add X quotations: [details]"
git push origin main
```

## Field Guide

### `latin_text` (Required)
The actual Latin quotation. Must be exact and verifiable from source.

**Good examples:**
- "Quod est superius, est sicut quod inferius"
- "Virtutes caelorum in has inferiores res operantur"
- "Omnis illuminatio divina indirecta simul accidit"

### `translation` (Optional but recommended)
English translation. Preserve original sense without interpreting.

### `source_text_slug`
Reference to the original work using the TEXT slug from our database. **Must match existing text!**

```bash
# Find available slugs:
sqlite3 portal/portal.db "SELECT slug, title FROM texts LIMIT 20"
```

### `referenced_in_slug`
The scholarly work that cites this quotation. Should also be in texts table.

### `scholar_name`
Name of the scholar discussing this quotation. Create consistent author references.

### `linguistic_notes`
Technical language analysis:
- Grammar: cases, tenses, constructions
- Vocabulary: unusual or technical terms
- Style: rhetorical devices, word choice
- Manuscript variants if known

**Example:**
```
"Medieval Latin translation. The term 'daemon' (from Greek daimon) 
refers to spirit/intelligence. The conditional 'ut compareas' establishes 
the magician's imperative authority over the spirit."
```

### `magical_significance`
Why this quotation matters to magical theory and practice:
- What principle does it establish?
- How did mages use this concept?
- What does it enable magically?

**Example:**
```
"Foundation of correspondence magic. If macrocosm mirrors microcosm,
then working with herbs, stones, or sigils attuned to celestial forces
can influence broader patterns. This principle justified grimoire magic
and sympathetic operations."
```

### `scholar_commentary`
The scholar's own interpretation:
- What does this quotation mean?
- How does it fit the historical context?
- What does it reveal about magical philosophy?

**Example:**
```
"Davies demonstrates that European grimoire tradition integrated 
Christian theological frameworks with older pagan binding techniques. 
The invocation of angels provides divine sanction, positioning the 
magician as an agent of divine will rather than a transgressor."
```

## Provenance & Review Status

Every quotation carries provenance metadata:

| Status | Meaning | When to Use |
|--------|---------|------------|
| **DRAFT** | Needs review | Auto-extracted, unverified entries |
| **REVIEWED** | Checked by domain expert | Verified against source PDF |
| **VERIFIED** | Cited in scholarship | Confirmed in published scholarship |

| Confidence | Meaning | When to Use |
|------------|---------|------------|
| **HIGH** | Direct quotation, well-sourced | Exact Latin from primary/secondary |
| **MEDIUM** | Likely correct but unverified | Extracted from PDF, sounds right |
| **LOW** | Candidate, needs verification | Automatic extraction, needs review |

## Example Quotations

The database ships with 4 examples covering major traditions:

1. **"Quod est superius..."** (Hermetic Principle)
   - Emerald Tablet
   - Cited by Owen Davies
   - Foundation of correspondence magic

2. **"Conjuro te, daemon..."** (Goetia Binding)
   - Dr. Rudd's Goetia
   - Cited by Skinner & Rankine
   - Spirit binding formula with divine authority

3. **"Ignis, Aer, Aqua, Terra..."** (Alchemy)
   - Alchemical theory
   - Cited by Egil Asprem
   - Elemental composition and transmutation

4. **"Universus hic mundus..."** (World Soul)
   - Neoplatonic cosmology
   - Cited by Elliot R. Wolfson
   - Universal animation and emanation

## Scaling the Quotations Database

### Strategy 1: Systematic PDF Mining
For each major source folder (Grimoire, Hermetic, Alchemy, etc.):

1. Prioritize key texts (scholarly works with lots of citations)
2. Run quotation_extractor.py on that folder
3. Manually verify candidates
4. Categorize by tradition/concept
5. Seed into database

### Strategy 2: Scholarly Reading
As you read through the 445 PDFs:

1. Mark significant quotations
2. Note source + author
3. Capture context and significance
4. Add to quotations_manual.json monthly
5. Re-seed and rebuild portal

### Scaling Targets

| Phase | Goal | Scope |
|-------|------|-------|
| Phase 1 (current) | Proof of concept | 4 foundational quotations |
| Phase 2 | Core quotations | 50 quotations across 8 traditions |
| Phase 3 | Comprehensive | 200+ quotations with full commentary |
| Phase 4 | Exhaustive | 500+ quotations, image gallery of MSS |

## Tips for Quality Quotations

✅ **DO:**
- Verify quotations against original PDFs
- Provide clear source attribution
- Include specific page/section references
- Separate linguistic from magical interpretation
- Use consistent terminology across commentary
- Tag by tradition and concept for discoverability

❌ **DON'T:**
- Paraphrase—use exact Latin only
- Mix multiple quotations in one entry
- Leave translation blank without reason
- Write vague commentary without evidence
- Add unsourced interpretations
- Duplicate quotations across entries

## Troubleshooting

### "Quotations not appearing on website"
1. Check `build_site_final.py` ran: `ls -la docs/quotations/`
2. Verify quotations in database: 
   ```bash
   sqlite3 portal/portal.db "SELECT COUNT(*) FROM quotations"
   ```
3. Check source_text_slug matches:
   ```bash
   sqlite3 portal/portal.db "SELECT source_text_slug FROM quotations"
   # Compare with:
   sqlite3 portal/portal.db "SELECT slug FROM texts"
   ```

### "Can't seed quotations"
1. Verify quotations_seed.json is valid:
   ```bash
   python -c "import json; json.load(open('data/quotations_seed.json'))"
   ```
2. Check database exists:
   ```bash
   ls -la portal/portal.db
   ```
3. Check schema includes quotations table:
   ```bash
   sqlite3 portal/portal.db ".tables"
   ```

### "Navigation missing Quotations tab"
Update `build_site_final.py` navigation template to include:
```html
<li><a href="/MagicalLatin/quotations/">Quotations</a></li>
```

## Next Steps

1. **Start with Manual Entry** — Add 10-20 high-confidence quotations from our current 4 examples
2. **Extract Candidates** — Run extractor on top grimoire/hermetic folders
3. **Build Commentary Library** — Systematically read scholarly texts and note commentary
4. **Expand Coverage** — Target 50 quotations across all 8 major traditions
5. **Image Integration** — Add manuscript page images alongside quotations

## Files Reference

| File | Purpose |
|------|---------|
| `data/quotations_manual.json` | Hand-entered, high-quality quotations |
| `data/quotations_seed.json` | Merged seed file (manual + extracted) |
| `data/quotation_candidates.json` | Extraction candidates awaiting review |
| `portal/scripts/quotation_extractor.py` | PDF scanning & candidate detection |
| `portal/scripts/seed_quotations.py` | Database population |
| `portal/scripts/build_site_final.py` | HTML generation with quotations |
| `docs/quotations/index.html` | Quotations card grid |
| `docs/quotations/{slug}/` | Detail page for each quotation |

---

**Status:** Quotations system is production-ready. 4 examples seeded. Framework ready for scaling to 100+ quotations.
