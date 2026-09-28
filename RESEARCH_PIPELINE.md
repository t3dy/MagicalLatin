# MagicalLatin Research Pipeline

## Overview

The quotations database depends on three research phases:
1. **Sourcing** — Finding scholarly materials that cite magical texts
2. **Extraction** — Locating and capturing quotations with context
3. **Enrichment** — Adding linguistic and magical analysis

This document maps how to access materials, prioritize reading, and track progress.

## Phase 1: Sourcing — Where Are the Materials?

### Primary Source: E:\pdf Structure

**445 magical texts organized by tradition and scholarly analysis:**

```
E:\pdf/
├── magic/ (22) ← General magic theory & practice
├── Grimoire/ (5) ← Grimoire tradition & ceremonial magic
├── hermetic/ (54) ← Hermeticism & Hermetic philosophy
├── Kabbalah/ (16) ← Jewish mysticism & Kabbalah
├── renaissance magic/ (34) ← Renaissance mages & Neoplatonism
├── alchemy/ (54) ← Alchemical texts & theory
├── Rosicrucian/ (44) ← Rosicrucian manifestos & tradition
├── Tarot/ (42) ← Tarot & divination
├── neoplatonism/ (28) ← Neoplatonic philosophy
├── gnosticism/ (24) ← Gnostic texts & thought
├── Western Esotericism and Occult/ (13) ← Scholarly overviews
├── western esotericism religious studies/ (53) ← Academic studies
├── crowley/ (22) ← Aleister Crowley & Thelema
├── [Other scholarly/author folders] → 54 more PDFs
└── ... (445 total)
```

### Two Types of Sources

**Type A: Primary Texts (Original Magical Works)**
- Corpus Hermeticum, Emerald Tablet
- Picatrix, Key of Solomon, Dr. Rudd's Goetia
- Paracelsus, Agrippa, Pico

**Location:** Usually cited *within* scholarly works or in primary text folders  
**How to find:** Search inside PDFs for Latin passages, repeated references  
**Extraction priority:** These are the SOURCES of quotations ✓

**Type B: Scholarly Works (Commentary & Analysis)**
- Owen Davies: "Grimoires — A History of Magic Books"
- Brian Copenhaver: essays on Hermeticism
- Francois Secret: Renaissance Kabbalah studies
- Elliot Wolfson: Kabbalistic hermeneutics
- Stephen Clucas: Western esotericism

**Location:** Authors have dedicated folders; most PDFs are scholarly analysis  
**How to find:** Folders named after scholars (Brian Copenhaver, Stephen Clucas, etc.)  
**Extraction priority:** These contain DISCUSSIONS OF quotations ✓

### Finding Materials for Specific Traditions

#### Hermetic Tradition (54 PDFs)
**Priority sources:**
- Copenhaver editions of Hermes Trismegistus
- Works on Corpus Hermeticum interpretation
- Ficino translations & commentary

**Location:** E:\pdf/hermetic/, E:\pdf/renaissance magic/, E:\pdf/Brian Copenhaver/  
**Expected quotations:** 15-25 (Emerald Tablet, divine principles, correspondence)

#### Grimoire Tradition (5 PDFs)
**Priority sources:**
- Sourceworks of Ceremonial Magic (Skinner & Rankine)
- Dr. Rudd's Goetia analysis
- Key of Solomon editions

**Location:** E:\pdf/Grimoire/, E:\pdf/magic/  
**Expected quotations:** 10-15 (spirit binding, divine authority, angel invocations)

#### Kabbalistic Tradition (16 PDFs)
**Priority sources:**
- Zohar commentaries
- Elliot Wolfson on Abulafia
- François Secret on Renaissance Kabbalah

**Location:** E:\pdf/Kabbalah/, E:\pdf/Francois Secret/  
**Expected quotations:** 10-15 (Sefirot, emanation, theurgic operations)

#### Alchemical Tradition (54 PDFs)
**Priority sources:**
- Paracelsus & alchemical philosophy
- Jabir ibn Hayyan (Geber)
- Elemental theory & transmutation

**Location:** E:\pdf/alchemy/, E:\pdf/Early Modern History/  
**Expected quotations:** 15-25 (elements, transmutation, animal soul)

#### Renaissance Magic (34 PDFs)
**Priority sources:**
- Ficino, Pico, Agrippa
- Neoplatonic synthesis with magic
- Correspondence & celestial influence

**Location:** E:\pdf/renaissance magic/, E:\pdf/Brian Copenhaver/, E:\pdf/neoplatonism/  
**Expected quotations:** 15-25 (macrocosm/microcosm, world soul, divine intellect)

### How to Locate a Specific Work

**Finding if we have a source:**
```bash
# Check if PDF exists in our collection
ls E:\pdf/**/*Corpus*Hermeticum* 2>/dev/null
ls E:\pdf/**/Picatrix* 2>/dev/null
ls E:\pdf/**/Zohar* 2>/dev/null

# Search by author
ls E:\pdf/Copenhaver/
ls E:\pdf/Stephen\ Clucas/
```

**If not found locally:**
- Check availability through academic databases
- Note it in EXTRACTION_MANIFEST.md as "SOURCED_EXTERNALLY"
- Link to where it was found

## Phase 2: Extraction — How to Find Quotations

### Strategy A: Guided Reading by Folder

**Best for:** Systematic coverage, understanding context  
**Time per folder:** 1-3 hours depending on length  
**Output:** 3-8 quotations per folder

**Process:**
1. Open folder with related PDFs (e.g., E:\pdf/hermetic/)
2. Skim titles to find scholarly commentaries
3. Read focusing on:
   - Direct quotations (in quotes, italicized, indented)
   - Latin phrases and their translations
   - Scholarly analysis of specific passages
4. For each quotation found, note:
   - Exact Latin text
   - Source work (author & title)
   - Which scholar discusses it
   - Page reference
   - Why scholar thinks it matters

**Tracking:** Use extraction checklist in EXTRACTION_MANIFEST.md

### Strategy B: Full-Text Search

**Best for:** Finding specific concepts or sources  
**Time per search:** 15-30 minutes  
**Output:** 1-5 quotations per search

**Process:**
```bash
# Search all PDFs for a word/phrase
grep -r "virtutes caelorum" E:\pdf/*.pdf
grep -r "anima mundi" E:\pdf/*.pdf
grep -r "Emerald Tablet" E:\pdf/*.pdf
```

**Then:** Examine context around each match

### Strategy C: Automatic Extraction

**Best for:** Initial candidate generation  
**Time:** Already done (100 candidates extracted)  
**Next step:** Manual verification & enrichment

**Current state:** `data/quotation_candidates.json` has 100 candidates  
**Quality:** 4 high-confidence, 96 need verification

## Phase 3: Material Formats

### PDF Source Materials
- **Location:** E:\pdf/ (445 files, 445 GB total)
- **Format:** Native PDFs (often scanned books)
- **Searchability:** Variable (older scans less searchable)
- **Best tool:** Adobe Reader Find, or convert to searchable text

### Markdown Conversions
**Status:** NOT YET CREATED  
**Question:** Should we convert high-priority PDFs to markdown for easier extraction?

**Candidates for markdown conversion:**
- Owen Davies: "Grimoires" (high citation count)
- Brian Copenhaver essays (foundational Hermetic scholarship)
- Francois Secret works (Renaissance Kabbalah)
- Stephen Clucas articles (Western esotericism overview)

**Conversion method:**
```bash
# Extract text from PDF
pdftotext source.pdf source.txt

# Convert to markdown with:
# - Preserve italics/emphasis
# - Keep section structure
# - Note page numbers
```

**Decision needed:** Worth doing for top 10-15 sources?

### Database Records (Current)

**Available in portal.db:**
- 421 texts indexed (extracted from filenames)
- 125 authors extracted
- 18 tradition concepts
- 4 hand-curated quotations

**Missing:**
- Source summaries (what each text contains)
- Reading order/priority
- Conversion status (is it searchable text or image scans?)
- Extraction progress tracker

## Phase 4: Prioritization Framework

### Research Questions Ranked by Value

**Tier 1: Highest ROI** (foundational principles, often quoted)
1. Hermetic Principle of Correspondence ("As above, so below")
2. Elemental Theory (Fire, Air, Water, Earth composition)
3. World Soul / Anima Mundi (universal animation)
4. Spirit Binding Formulas (Goetia methodology)
5. Kabbalah Emanation (Sefirot & divine descent)

**Tier 2: High Value** (important traditions, frequently cited)
6. Celestial Magic (planetary hours, stellar influence)
7. Sympathetic Correspondences (stones, herbs, animals)
8. Talismanic Magic (construction & consecration)
9. Theurgic Operations (working with higher powers)
10. Alchemical Transmutation (spiritual & material change)

**Tier 3: Substantive** (specific practices, period-specific)
11. Goetia Spirit Hierarchies & ranks
12. Rosicrucian Symbolism & allegory
13. Tarot Correspondences & meanings
14. Kabbalistic Letter Mysticism
15. Neoplatonic Emanation & return

**Tier 4: Context** (history, philosophy, background)
16. Renaissance Magic Synthesis (Ficino, Pico)
17. Islamic Influence (Picatrix, al-Ghazali)
18. Christian Theology & Magic (reconciling systems)

### Folder Priority for Extraction

**Priority 1 (40 PDFs expected → 30-40 quotations):**
- E:\pdf/Grimoire/ (foundational ceremonial magic)
- E:\pdf/hermetic/ (sample of 54, prioritize Copenhaver)
- E:\pdf/renaissance magic/ (synthesis texts)

**Priority 2 (40 PDFs → 20-30 quotations):**
- E:\pdf/alchemy/ (sample of 54)
- E:\pdf/Kabbalah/ (mystical tradition)
- E:\pdf/Rosicrucian/ (order & symbolism)

**Priority 3 (remaining):**
- All other folders as time permits

## Tracking & Progress

### EXTRACTION_MANIFEST.md

**Required:** One file documenting:
- Which folders have been scanned
- How many quotations from each
- Status of each candidate
- What remains to extract

**Format:**
```yaml
extraction_status:
  grimoire:
    status: IN_PROGRESS
    pdfs_scanned: 3/5
    quotations_found: 4
    candidates_extracted: 8
    next: Continue with remaining 2 PDFs
  
  hermetic:
    status: NOT_STARTED
    pdfs_scanned: 0/54
    quotations_found: 0
    candidates_extracted: 0
    priority: HIGH
    expected: 15-25 quotations
```

### Query Aid: What Questions Should the Database Answer?

After extraction, the database should answer:

**By tradition:**
- "Show me all quotations about Hermetic correspondence"
- "Which quotations from grimoire tradition?"
- "What do we have on Kabbalah?"

**By source:**
- "What quotations from the Emerald Tablet?"
- "Which passages does Owen Davies cite?"
- "What does Agrippa say about celestial magic?"

**By scholar:**
- "Which quotations does Copenhaver discuss?"
- "All quotations analyzed by Clucas"
- "Quotations in Francois Secret's work"

**By concept:**
- "All quotations explaining correspondence"
- "Quotations about elemental magic"
- "Passages on world soul"

**By completeness:**
- "Which quotations need commentary?"
- "Which are still DRAFT status?"
- "Which need source page written?"

---

## Implementation Checklist

- [ ] EXTRACTION_MANIFEST.md created and updated weekly
- [ ] Priority 1 folders (40 PDFs) scanned for quotations
- [ ] 100 candidates evaluated and categorized
- [ ] Top 30 candidates converted to full quotation entries
- [ ] Source summaries written for 421 texts
- [ ] Reading order documented by tradition
- [ ] High-value sources (Copenhaver, Davies, etc.) prioritized
- [ ] Markdown conversions done for top 10 sources (optional, evaluate ROI)
- [ ] Agent handoff instructions documented
- [ ] Next researcher briefed on priorities & progress

---

**Status:** Research pipeline documented. Ready for systematic extraction. Recommend starting with Priority 1 folders for highest ROI.
