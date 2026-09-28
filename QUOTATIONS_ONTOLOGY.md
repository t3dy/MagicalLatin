# MagicalLatin Quotations Ontology

## Purpose

This document explains how the quotations database is organized and how to query it effectively. It answers: "If I want to know X, how do I find it?"

## Core Entities & Relationships

### Primary Tables

```
texts
├─ Magical work or scholarly analysis
├─ Examples: "Corpus Hermeticum", "Grimoires — A History of Magic Books"
└─ Linked to: quotations (as source), figures (as author)

figures
├─ Person: magician, author, scholar
├─ Examples: "Hermes Trismegistus", "Owen Davies"
└─ Linked to: texts (as author)

quotations
├─ Actual Latin passage + metadata
├─ Examples: "Quod est superius...", "Ignis, Aer, Aqua, Terra..."
└─ Linked to: texts (source + cited in), figures (scholar), concepts

concepts
├─ Magical doctrine, practice, tradition
├─ Examples: "Hermetic Correspondence", "Spirit Binding"
└─ Linked to: quotations, texts

quotation_commentary
├─ Scholarly analysis: linguistic, magical, historical
├─ Examples: grammar notes, magical significance, interpretations
└─ Linked to: quotations
```

### Foreign Key Links

```
quotations.source_text_slug → texts.slug
"Which original work is this quotation from?"

quotations.referenced_in_slug → texts.slug
"Which scholarly work discusses this quotation?"

quotations.scholar_name ← figures.name
"Who analyzes this quotation?"

quotation_commentary.quotation_id → quotations.id
"What has been said about this quotation?"
```

## Query Patterns

### Find Quotations BY TRADITION

**Question:** "Show me all quotations from Hermetic sources"

```sql
SELECT q.latin_text, q.translation, q.scholar_name, t.title
FROM quotations q
JOIN texts t ON q.source_text_slug = t.slug
WHERE t.tradition = 'Hermeticism'
ORDER BY q.scholar_name;
```

**Result:** All Hermetic quotations with scholar attribution

**Problem with current ontology:** 
- Tradition is on texts table (origin source)
- But quotations.source_text_slug may not have tradition filled in
- **Fix needed:** Ensure all source texts have tradition field populated

### Find Quotations DISCUSSED BY A SCHOLAR

**Question:** "What quotations does Owen Davies analyze?"

```sql
SELECT q.latin_text, q.source_work_title, q.page_reference
FROM quotations q
WHERE q.scholar_name = 'Owen Davies'
ORDER BY q.source_work_title, q.page_reference;
```

**Result:** All quotations Davies cites, organized by source

**Current state:** Works if scholar_name is filled ✓

### Find Quotations FROM A SPECIFIC WORK

**Question:** "What quotations from the Emerald Tablet?"

```sql
SELECT q.latin_text, q.translation, q.scholar_name, q.scholar_commentary
FROM quotations q
WHERE q.source_work_title LIKE '%Emerald Tablet%'
ORDER BY q.scholar_name;
```

**Result:** All quotations from that work, with analyses

**Problem:** source_work_title is text field (not normalized)  
**Fix needed:** Add source_work_id foreign key to texts table for exact matching

### Find Quotations EXPLAINING A CONCEPT

**Question:** "Which quotations explain the Hermetic Principle of Correspondence?"

```sql
-- CURRENT: No direct link from quotations to concepts
-- We need: concept_tags in quotations or concept_quotations join table

-- Workaround: Search commentary
SELECT q.id, q.latin_text, q.source_author,
       qc.commentary_text
FROM quotations q
JOIN quotation_commentary qc ON q.id = qc.quotation_id
WHERE qc.commentary_text LIKE '%correspondence%'
   OR q.magical_significance LIKE '%correspondence%'
ORDER BY q.scholar_name;
```

**Result:** Quotations relating to correspondence

**Problem:** Loose text matching, not semantic  
**Fix needed:** Add concepts join table for explicit concept-quotation links

### Find INCOMPLETE QUOTATIONS

**Question:** "Which quotations need linguistic commentary?"

```sql
SELECT q.id, q.latin_text, q.scholar_name, COUNT(qc.id) as comment_count
FROM quotations q
LEFT JOIN quotation_commentary qc ON q.id = qc.quotation_id
GROUP BY q.id
HAVING comment_count < 2
   OR q.linguistic_notes IS NULL
ORDER BY q.review_status;
```

**Result:** Quotations missing complete analysis

**Current state:** Depends on proper field population ✓

### Find BY REVIEW STATUS

**Question:** "Which quotations are ready to publish?"

```sql
SELECT q.id, q.latin_text, q.review_status, q.confidence
FROM quotations q
WHERE q.review_status = 'VERIFIED'
   AND q.confidence = 'HIGH'
ORDER BY q.created_at DESC;
```

**Result:** Production-ready quotations

**Current state:** Works ✓

## Data Quality Issues & Fixes

### Issue 1: Source Text Normalization

**Problem:** 
- Source works referenced multiple ways: "Emerald Tablet", "Tabula Smaragdina", "Emerald Table"
- Makes querying by source unreliable

**Current columns:**
- `source_work_title` (text field, no validation)
- `source_text_slug` (should link to texts table)

**Fix:** 
Add `source_text_id` foreign key:
```sql
ALTER TABLE quotations ADD COLUMN source_text_id INTEGER REFERENCES texts(id);
-- Then: UPDATE quotations SET source_text_id = 
--       (SELECT id FROM texts WHERE slug = quotations.source_text_slug)
```

**This enables:**
```sql
-- Reliable query: all quotations from texts in "Hermetic" tradition
SELECT q.latin_text, t.title, t.tradition
FROM quotations q
JOIN texts t ON q.source_text_id = t.id
WHERE t.tradition = 'Hermeticism';
```

### Issue 2: Concept Linking

**Problem:** 
- Quotations aren't linked to concepts
- Can't ask "which quotations are about Correspondence?"

**Current:** Tags are JSON array (unqueried)

**Fix:** Create concept_quotations join table:
```sql
CREATE TABLE concept_quotations (
    id INTEGER PRIMARY KEY,
    concept_id INTEGER REFERENCES concepts(id),
    quotation_id INTEGER REFERENCES quotations(id),
    relevance TEXT CHECK (relevance IN ('primary', 'secondary', 'tertiary'))
);
```

**This enables:**
```sql
-- Find all quotations explaining a concept
SELECT q.latin_text, q.scholar_name, cq.relevance
FROM quotations q
JOIN concept_quotations cq ON q.id = cq.quotation_id
JOIN concepts c ON cq.concept_id = c.id
WHERE c.slug = 'hermetic-correspondence'
ORDER BY cq.relevance;
```

### Issue 3: Completeness Tracking

**Problem:** 
- No way to know which quotations are "done" vs. still need work
- No workflow status beyond review_status

**Current fields:**
- `review_status`: DRAFT / REVIEWED / VERIFIED
- `confidence`: HIGH / MEDIUM / LOW

**Missing:** Completion checklist per quotation
- [ ] Latin text verified against source PDF
- [ ] Translation provided & checked
- [ ] Source attribution complete (author + work)
- [ ] Scholar name & work documented
- [ ] Page reference included
- [ ] Linguistic commentary written
- [ ] Magical significance documented
- [ ] Source page created on portal

**Fix:** Add completeness tracking:
```sql
ALTER TABLE quotations ADD COLUMN completion_status TEXT DEFAULT 'INCOMPLETE';
-- Values: INCOMPLETE, IN_PROGRESS, COMPLETE, PUBLISHED
```

### Issue 4: Scholar Attribution Normalization

**Problem:**
- Scholar names stored as plain text (no linking)
- "Owen Davies", "Davies, Owen", "O. Davies" might be stored differently

**Fix:** Create scholar_quotations join table:
```sql
CREATE TABLE scholar_quotations (
    id INTEGER PRIMARY KEY,
    quotation_id INTEGER REFERENCES quotations(id),
    figure_id INTEGER REFERENCES figures(id),
    discussion_type TEXT CHECK (discussion_type IN ('cited', 'analyzed', 'critiqued')),
    work_title TEXT,  -- The scholar's work discussing this
    page_reference TEXT
);
```

**This enables:**
```sql
-- Find all quotations discussed by a scholar
SELECT q.latin_text, f.name, sq.work_title, sq.page_reference
FROM quotations q
JOIN scholar_quotations sq ON q.id = sq.quotation_id
JOIN figures f ON sq.figure_id = f.id
WHERE f.slug = 'owen-davies'
ORDER BY sq.work_title;
```

## Proposed Ontology Improvements

### Schema v3 Additions

**New tables:**
- `concept_quotations` — Map quotations to magical concepts
- `scholar_quotations` — Track scholar discussions of quotations
- `quotation_status_log` — Audit trail of status changes

**Enhanced columns:**
- `quotations.source_text_id` (FK to texts, for validation)
- `quotations.completion_status` (INCOMPLETE / IN_PROGRESS / COMPLETE / PUBLISHED)
- `quotations.source_verified` (boolean, Latin verified against PDF)
- `texts.summary` (what this work contains, for discovery)

**New lookup table:**
- `quotation_types` (primary_source, commentary, verse, formula, etc.)

### Query Optimization

**Indexes to add:**
```sql
CREATE INDEX idx_quotations_concept ON concept_quotations(concept_id);
CREATE INDEX idx_quotations_scholar ON scholar_quotations(figure_id);
CREATE INDEX idx_quotations_status ON quotations(completion_status);
CREATE INDEX idx_quotations_tradition ON texts(tradition);
```

**These enable:**
- Fast lookup: "all quotations about concept X"
- Fast lookup: "all quotations by scholar Y"
- Fast lookup: "all incomplete quotations"
- Fast lookup: "all quotations from tradition Z"

## Current Data Coverage

### By Tradition (texts table, should match quotations)
- Hermeticism: 54 texts → ? quotations (0 currently)
- Grimoire: 5 texts → 1 quotation (Goetia binding)
- Alchemy: 54 texts → 1 quotation (elements)
- Kabbalah: 16 texts → 1 quotation (anima mundi/world soul)
- Renaissance: 34 texts → 1 quotation (correspondence)
- Others: 258 texts → ? quotations (0 currently)

**Gap:** Only 4 hand-curated quotations. 100 candidates awaiting enrichment.

### By Scholar (figures table, should match quotations)
- Owen Davies: ? quotations (1 currently: Emerald Tablet)
- Copenhaver: 0 quotations
- Clucas: 0 quotations
- Wolfson: 0 quotations
- Others: ? quotations

**Gap:** No scholar-based queries work yet.

### By Concept (concepts table, should link to quotations)
- 18 concepts defined (traditions)
- 0 concept-quotation links
- Can't answer "what quotations explain X concept?"

**Gap:** No semantic queries possible yet.

## For Next Agent: Handoff Questions

When extracting quotations, ensure you can answer:

1. **"Which original work is this quotation from?"**
   - Must link to existing texts.slug
   - Must verify tradition matches
   - Example: "Corpus Hermeticum" → corpus-hermeticum

2. **"Which scholar discusses this quotation?"**
   - Must be in figures table
   - Must have work title (book/article)
   - Must have page reference
   - Example: Owen Davies in "Grimoires" p. 42

3. **"What concepts does this quotation relate to?"**
   - Must list matching concepts.slug values
   - Should tag primary vs secondary relevance
   - Example: ["hermetic-correspondence", "sympathy-magic"]

4. **"Is this quotation complete?"**
   - Latin text verified? ✓
   - Translation provided? ✓
   - Source attributed? ✓
   - Commentary written? ✓
   - Can mark as COMPLETE when all done

5. **"What does this quotation teach?"**
   - Linguistic notes: grammar, vocabulary, style
   - Magical significance: practice implications
   - Scholarly interpretation: academic context
   - Interconnections: related concepts/quotations

---

## Implementation Roadmap

**Phase 1 (Now):** 
- Document current schema gaps
- Create normalization script for existing 4 quotations
- Set template for what "complete" looks like

**Phase 2 (Next):**
- Add concept_quotations join table
- Link 4 exemplar quotations to relevant concepts
- Test queries for discoverability

**Phase 3 (Scaling):**
- Add scholar_quotations join table
- Normalize scholar names (Davies, Copenhaver, etc.)
- Populate with 50+ extracted quotations

**Phase 4 (Production):**
- Add completion_status workflow
- Audit all quotations for data quality
- Build query interface on portal

---

**Status:** Ontology documented. Schema improvements identified. Ready for next agent to understand data requirements.
