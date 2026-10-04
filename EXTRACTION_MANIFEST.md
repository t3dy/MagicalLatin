# Quotations Extraction Manifest

## Purpose

Track extraction progress across all 445 PDF sources. Answers: "What's been done? What remains? How much progress toward our goal?"

## Current Status (2026-10-04)

```
OVERALL: 4/50 quotations (Phase 2 goal)
         4/200 quotations (Phase 3 goal)

Quotations Seeded:        4 (hand-curated exemplars)
Candidates Extracted:    100 (HIGH: 4, MEDIUM: 96)
Quotations Complete:      0
Phase 2 In Progress:      YES (verification agent running)

Phase 2 Target: 46 additional quotations by Oct 31 (27 days remaining)
Current pace: Need ~1.7 per day to reach 50 by deadline
```

## Extraction by Tradition

### HERMETIC (54 PDFs, Goal: 15-25 quotations)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| hermetic/ | NOT_STARTED | 54 | 0 | — | Highest priority: Corpus Hermeticum references |
| Brian Copenhaver/ | NOT_STARTED | 3-5 | 0 | — | Key Hermetic scholar |
| David Lapoujade/ | NOT_STARTED | 1-2 | 0 | — | Hermes & Neoplatonism |

**Exemplars queued:** "Quod est superius..." (Emerald Tablet, via Davies)

**Next action:** Sample 5 Copenhaver essays, extract Hermetic principles

---

### ALCHEMY (54 PDFs, Goal: 15-25 quotations)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| alchemy/ | NOT_STARTED | 54 | 0 | — | Paracelsus, elemental theory |
| FM Van Helmont/ | NOT_STARTED | 2-3 | 0 | — | Transmutation philosophy |

**Exemplars queued:** "Ignis, Aer, Aqua, Terra..." (elemental composition)

**Next action:** Prioritize Van Helmont works, transmutation texts

---

### GRIMOIRE & CEREMONIAL MAGIC (5 PDFs, Goal: 10-15 quotations)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| Grimoire/ | EXTRACTION_IN_PROGRESS | 5 | 1 | 15+ | High-quality candidates extracted |
| magic/ | PARTIAL | 22 | 0 | 85+ | Candidates extracted, need review |

**Exemplars queued:** "Conjuro te, daemon..." (Dr. Rudd's Goetia)

**Extraction notes:**
- Sourceworks of Ceremonial Magic: Rich quotations on spirit binding
- Multiple candidates from Goetia hierarchies & angel invocations
- Candidates quality: MEDIUM (need context verification)

**Next action:** Verify high-confidence candidates, move 10 to complete status

---

### KABBALAH & JEWISH MYSTICISM (16 PDFs, Goal: 10-15 quotations)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| Kabbalah/ (both variants) | NOT_STARTED | 16 | 1 | — | Sefirot, emanation, letters |
| Francois Secret/ | NOT_STARTED | 2-3 | 0 | — | Renaissance Kabbalist synthesis |
| Eugenio Garin/ | NOT_STARTED | 1-2 | 0 | — | Renaissance Magic & Kabbalah |

**Exemplars queued:** "Universus hic mundus..." (world soul, relates to Kabbalistic emanation)

**Next action:** Start with Francois Secret, extract Kabbalistic principles

---

### ROSICRUCIAN (44 PDFs, Goal: 8-12 quotations)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| Rosicrucian/ | NOT_STARTED | 44 | 0 | — | Symbolism, orders, philosophy |

**Next action:** Sample 5 texts on Rosicrucian principles & symbolism

---

### TAROT & DIVINATION (42 PDFs, Goal: 5-10 quotations)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| Tarot/ | NOT_STARTED | 42 | 0 | — | Correspondences, interpretation |

**Next action:** Sample texts on tarot symbolism & divinatory practice

---

### NEOPLATONISM & PHILOSOPHY (28 PDFs, Goal: 5-10 quotations)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| neoplatonism/ | NOT_STARTED | 28 | 0 | — | Plotinus, Porphyry, emanation |
| Stephen Clucas/ | NOT_STARTED | 10 | 0 | — | Western esotericism overview |

**Next action:** Stephen Clucas synthesis articles

---

### GNOSTICISM (24 PDFs, Goal: 3-5 quotations)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| gnosticism/ | NOT_STARTED | 24 | 0 | — | Cosmology, divine knowledge |

**Next action:** Sample for magical principles

---

### RENAISSANCE MAGIC (34 PDFs, Goal: 10-15 quotations)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| renaissance magic/ | NOT_STARTED | 34 | 0 | — | Ficino, Pico, Agrippa synthesis |
| Brian Copenhaver/ | NOT_STARTED | 3-5 | 0 | — | Overlaps with Hermetic |

**Next action:** Copenhaver on Renaissance magic theory

---

### OTHER TRADITIONS (54 PDFs combined)

| Folder | Status | PDFs | Q Found | Candidates | Notes |
|--------|--------|------|---------|------------|-------|
| Western Esotericism/ | NOT_STARTED | 66 | 0 | — | Broad overview & scholarship |
| crowley/ | NOT_STARTED | 22 | 0 | — | Modern magical theory |
| Others | NOT_STARTED | ~32 | 0 | — | Author-specific, misc |

---

## Extracted Candidates Status

**Source:** `data/quotation_candidates.json` (100 total)

| Confidence | Count | Status | Next Action |
|------------|-------|--------|------------|
| HIGH | 4 | Review for errors | Move 4 to complete if verified |
| MEDIUM | 96 | Verify context | 30 to complete by Phase 2 |
| LOW | — | Not included | — |

**Candidate evaluation criteria:**
- ✓ Is it actual Latin (not English)?
- ✓ Is it intelligible without surrounding context?
- ✓ Is it quotable length (20-200 words)?
- ✓ Can we find source attribution?
- ✓ Is there scholarly discussion?

**High-confidence candidates requiring verification:**
1. Iron & Mars correspondence (from Skinner & Rankine)
2. Goetia hierarchy description (from Skinner & Rankine)
3. [2 more from Grimoire folder]

---

## Quotation Completeness Tracking

### What "Complete" Means

A quotation is COMPLETE when all of these are filled:

| Field | Required? | Status | Example |
|-------|-----------|--------|---------|
| latin_text | ✓ | — | "Quod est superius..." |
| translation | ✓ | — | "That which is above..." |
| source_author | ✓ | 4/4 | "Hermes Trismegistus" |
| source_work_title | ✓ | 4/4 | "Emerald Tablet" |
| source_text_slug | ✓ | 2/4 | Must link to texts table |
| referenced_in_slug | ✓ | 1/4 | Scholar's work |
| scholar_name | ✓ | 4/4 | "Owen Davies" |
| page_reference | ✓ | 3/4 | "p. 42" or "Tract I" |
| linguistic_notes | ✓ | 4/4 | Grammar & vocabulary |
| magical_significance | ✓ | 4/4 | Why practitioners care |
| scholar_commentary | ✓ | 4/4 | Academic interpretation |
| review_status | ✓ | 4/4 → DRAFT | DRAFT/REVIEWED/VERIFIED |

**Current 4 exemplars:** All fields populated, review_status = DRAFT (ready for review)

**Candidates (100):** Mostly latin_text only, need all other fields filled

---

## Workflow: From Candidate to Complete

```
CANDIDATE (in quotation_candidates.json)
    ↓
    [RESEARCH PHASE]
    - Find source work (author + title)
    - Find scholar discussing it
    - Get page references
    - Write commentary
    ↓
DRAFTED (in quotations_seed.json, review_status=DRAFT)
    ↓
    [REVIEW PHASE]
    - Verify Latin against PDF
    - Check scholar attribution
    - Validate commentary quality
    ↓
REVIEWED (in database, review_status=REVIEWED)
    ↓
    [VERIFICATION PHASE]
    - Cross-check against multiple sources
    - Ensure commentary accuracy
    - Portal page generation
    ↓
VERIFIED & PUBLISHED (on portal, review_status=VERIFIED)
```

---

## Phase 2 Checklist (Goal: 50 quotations)

**By tradition, 10 quotations each:**

- [ ] Hermetic (10): Correspondence, divine principle, emanation
- [ ] Alchemy (10): Elements, transmutation, philosophical mercury
- [ ] Grimoire (10): Spirit binding, divine authority, hierarchies
- [ ] Kabbalah (10): Sefirot, emanation, divine names
- [ ] Renaissance (10): Macrocosm/microcosm, world soul, celestial magic

**Required by date:** 2026-10-31 (4 weeks)

**Workload:** ~1 quotation per working day per researcher

---

## Data Quality Checkpoints

### Verify All Quotations Have:

```bash
# Check each quotation in database
SELECT id, latin_text, source_author, scholar_name, 
       CASE WHEN linguistic_notes IS NULL THEN '❌' ELSE '✓' END as linguistics,
       CASE WHEN magical_significance IS NULL THEN '❌' ELSE '✓' END as magical,
       review_status
FROM quotations
ORDER BY review_status, id;
```

**Target:** All rows have ✓ on all columns before publishing

### Verify Source Links:

```bash
# Check quotation source_text_slug matches texts table
SELECT q.id, q.source_text_slug, 
       CASE WHEN t.slug IS NULL THEN '❌ NOT_FOUND' ELSE '✓' END as link_status
FROM quotations q
LEFT JOIN texts t ON q.source_text_slug = t.slug;
```

**Target:** No ❌ rows (all source_text_slug values must exist in texts table)

---

## Progress Updates

### Weekly Review

Every Friday, update this section:

```
## 2026-09-28 (Week 1)
- Extraction completed: 100 candidates
- Quotations completed: 4 exemplars
- Progress: 4/50 (8%) toward Phase 2
- Blockers: Candidates need context enrichment
- Next week: Verify top 10 high-confidence candidates
```

### Monthly Report

End of each month:

```
## September 2026
- Total extracted: 104 (100 candidates + 4 exemplars)
- Total complete: 4 (8%)
- Traditions covered: 5/8
- Estimated completion date: Actual vs. Projected
```

---

## For Next Agent: Handoff Template

When you take over, update this section:

```yaml
HANDOFF - [DATE] - [YOUR_NAME]:
  inherited:
    - 4 exemplar quotations (seeded)
    - 100 candidate quotations (extracted)
    - Database schema (v2, with improvements noted in QUOTATIONS_ONTOLOGY.md)
  
  current_focus: Enriching candidates to move to DRAFTED status
  
  blockers:
    - Need source attribution for 100 candidates
    - Need scholar names linked
    - Need context commentary for each
  
  next_priorities:
    - Start with HIGH confidence candidates (4 identified)
    - Then MEDIUM confidence ones (96 identified)
    - Then extract from Priority 1 folders
  
  estimated_timeline: 50 quotations by 2026-10-31
  
  questions?: See RESEARCH_PIPELINE.md, QUOTATIONS_ONTOLOGY.md, QUOTATION_TEMPLATE.md
```

---

**Status:** Manifest created. 4 exemplars seeded. 100 candidates waiting for enrichment. Ready for systematic scaling.
