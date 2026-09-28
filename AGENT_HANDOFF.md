# Agent Handoff: Quotations System

## For the Next Researcher/Agent

This document tells you everything you need to know to continue the quotations work. Read this first.

## Current State (2026-09-28)

### What's Done ✅

**Database:**
- Schema created (quotations + commentary tables, with provenance tracking)
- 4 hand-curated exemplar quotations seeded and verified
- Database initialized and ready to scale

**Portal:**
- 569 pages generated (texts, authors, concepts, quotations)
- Quotations/index.html displays card grid
- Individual quotation detail pages live
- Navigation includes Quotations tab on all pages

**Infrastructure:**
- Extraction pipeline built (extraction + seeding + generation scripts, all idempotent)
- 100 quotation candidates extracted from PDFs
- 4 high-confidence candidates identified for verification

**Documentation:**
- RESEARCH_PIPELINE.md — How to find and access materials
- QUOTATIONS_ONTOLOGY.md — How data is organized and how to query it
- EXTRACTION_MANIFEST.md — Progress tracking across all folders
- QUOTATION_TEMPLATE.md — What complete quotations look like
- This document — Agent handoff instructions

### What Remains ⏳

**Immediate (Next 4 weeks, Phase 2 goal):**
- Enrich 100 extracted candidates with full metadata
- Move top 30 high-confidence candidates to complete/reviewed status
- Target: 50 total quotations (4 + 46 from candidates)
- Workload: ~1-2 quotations per working day per researcher

**Medium term (Weeks 5-12, Phase 3):**
- Systematically extract from Priority 1 folders (40 PDFs)
- Target: 50 → 200 quotations across all traditions
- Workload: Parallel with Phase 2, systematic folder-by-folder extraction

**Long term (Phase 4+):**
- Implement ontology improvements (concept linking, scholar normalization)
- Build query interface on portal
- Image gallery of manuscript pages

---

## What You Need to Know Right Now

### The Three Critical Files

**1. `data/quotation_candidates.json`** (100 items)
- Automatically extracted candidates awaiting enrichment
- Quality: 4 high-confidence, 96 medium-confidence
- Your job: Verify these, add missing metadata, move to quotations_seed.json

**2. `data/quotations_seed.json`** (4 + your additions)
- Source of truth for quotations database
- Currently 4 exemplars, will grow as you complete candidates
- Format: JSON array, must be valid
- Rules: Edit this file, run seed_quotations.py, then build_site_final.py

**3. `data/quotations_manual.json`** (template)
- For manually-typed quotations you discover while reading
- If you find quotations not in candidates, add them here
- Template structure provided, follow QUOTATION_TEMPLATE.md

### The Pipeline (How It Works)

```
1. Find quotation in PDF
   ↓
2. Fill in all fields (see QUOTATION_TEMPLATE.md)
   ↓
3. Add to data/quotations_seed.json or quotations_manual.json
   ↓
4. python portal/scripts/seed_quotations.py
   (validates, inserts into database)
   ↓
5. python portal/scripts/build_site_final.py
   (generates portal pages)
   ↓
6. git add docs/ data/quotations*.json && git commit && git push
```

**All scripts are idempotent** — safe to re-run after editing files.

### Database Location & Access

**Database file:** `portal/portal.db` (SQLite)

**Quick checks:**
```bash
# Count quotations
sqlite3 portal/portal.db "SELECT COUNT(*) FROM quotations"

# See all quotations
sqlite3 portal/portal.db "SELECT id, latin_text, scholar_name, review_status FROM quotations"

# Find specific quotation
sqlite3 portal/portal.db "SELECT * FROM quotations WHERE latin_text LIKE '%superius%'"
```

**Full schema:** See QUOTATIONS_ONTOLOGY.md

---

## Your Job: Three Phases

### Phase 1: Candidate Verification (Week 1-2)

**Goal:** Move top 10-15 candidates to COMPLETE status

**Steps:**
1. Open `data/quotation_candidates.json`
2. For top HIGH-confidence candidates:
   - Verify Latin text against original PDF
   - Find source work (author + title)
   - Find scholar discussing it (name + publication)
   - Get exact page reference
3. Copy verified candidates to `data/quotations_seed.json`
4. Fill in all fields (see QUOTATION_TEMPLATE.md checklist)
5. Run seeding and portal generation
6. Commit to GitHub

**Quality gate:** Before moving to quotations_seed.json, every field must be filled

**How to verify a candidate:**
```
1. Take the latin_text from candidate
2. Search PDFs for that exact phrase
3. Note the source (which book, page, author)
4. Note which scholar discusses it
5. Compare with PDF to ensure exact match
```

### Phase 2: Systematic Extraction (Week 3-4)

**Goal:** Extract from Priority 1 folders (40 PDFs) for additional 20-30 quotations

**Priority 1 folders (do first):**
- Grimoire/ (5 PDFs)
- Sample of hermetic/ (10 PDFs)
- Sample of renaissance magic/ (10 PDFs)
- Sample of alchemy/ (10 PDFs)
- Brian Copenhaver folder (3-5 PDFs)

**Process:**
1. Open high-priority PDF
2. Read for quotations (look for: italicized text, "quote" marks, Latin phrases, indented passages)
3. For each quotation found:
   - Note exact Latin (screenshot if needed)
   - Find who said it (source author)
   - Note which scholar discusses it
   - Get page references
   - Record in EXTRACTION_MANIFEST.md
4. After reading file, add quotations to quotations_seed.json
5. Run seeding + portal generation
6. Commit changes

**Tracking:** Update EXTRACTION_MANIFEST.md for each folder as you complete it

### Phase 3: Enrichment (Week 5+)

**Goal:** For each quotation, write linguistic & magical analysis

**For each quotation, add:**
1. `linguistic_notes` — Grammar, vocabulary, style analysis (2-4 sentences)
2. `magical_significance` — Why practitioners care (3-5 sentences)
3. `scholar_commentary` — Academic interpretation (3-5 sentences)

**See QUOTATION_TEMPLATE.md for examples of each.**

**Quality bar:** Commentary should be substantial enough that someone unfamiliar with the quotation understands its importance.

---

## Resources & How to Use Them

### QUOTATION_TEMPLATE.md
- Read this first
- Shows what a complete quotation looks like
- Field-by-field breakdown with examples
- Validation checklist before marking complete
- Common mistakes & how to fix them

### RESEARCH_PIPELINE.md
- Where to find materials (which PDFs contain what?)
- How to prioritize reading
- What types of sources we have
- Folder organization by tradition
- How to do guided reading vs. full-text search

### QUOTATIONS_ONTOLOGY.md
- How the database is organized
- Query examples (find by tradition, scholar, concept, etc.)
- Known issues in current schema
- What the next agent should fix
- Understanding relationships between tables

### EXTRACTION_MANIFEST.md
- Track what's been done
- See what remains
- Progress toward Phase 2 goal (50 quotations)
- Weekly/monthly update template
- Handoff template for next agent

---

## Critical Rules

1. **Always verify Latin against original PDF**
   - Candidates are extracted automatically; verify before finalizing
   - Take screenshot if needed
   - Never guess or paraphrase

2. **Every quotation needs source attribution**
   - Author of original work
   - Title of original work
   - Scholar discussing it
   - Page reference

3. **Quotations are only COMPLETE when all fields filled**
   - Use QUOTATION_TEMPLATE.md checklist
   - Don't move to quotations_seed.json until ready

4. **Always update EXTRACTION_MANIFEST.md**
   - Track progress daily
   - Update folder status as you work
   - Help next agent see what's done

5. **Test before committing**
   - After editing quotations_seed.json, run seeding script
   - Check for errors: `sqlite3 portal/portal.db "SELECT COUNT(*) FROM quotations"`
   - Generate portal: `python portal/scripts/build_site_final.py`
   - Only commit if all scripts succeed

6. **Follow the pipeline order**
   - Verify candidates BEFORE extracting new ones
   - Complete data entry BEFORE seeding
   - Seed database BEFORE generating portal
   - Generate portal BEFORE committing

---

## Unresolved Questions (For You to Answer)

These are design questions the previous agent left open. Consider them as you work:

1. **Should we convert high-priority PDFs to markdown?**
   - Current: Search PDFs directly (slow, hard to verify)
   - Alternative: Extract text → markdown → easy search & linking
   - Candidates: Owen Davies, Copenhaver, Secret, Clucas, Wolfson
   - Decision: ROI worth it? Would it speed up quotation extraction?

2. **Should source pages have overview summaries?**
   - Current: Quotation detail pages show just that quotation
   - Alternative: Source page ("Corpus Hermeticum") shows all its quotations
   - Question: Do we have/should we write source summaries (what each work contains)?
   - See: RESEARCH_PIPELINE.md, "Source summaries" section

3. **Should we link quotations to magical concepts?**
   - Current: Quotations tagged with strings
   - Alternative: Create concept_quotations join table for semantic queries
   - Question: When should we do this? Phase 2 or Phase 3?
   - See: QUOTATIONS_ONTOLOGY.md, "Issue 2: Concept Linking"

4. **How much commentary is "complete"?**
   - Current: 3 commentary fields (linguistic, magical, scholarly)
   - Question: Should we require all 3? Or 1 minimum to ship?
   - Decision impacts Phase 2 timeline (50 quotations by Oct 31)

---

## Success Metrics

**Phase 2 success = 50 quotations by Oct 31:**
- 4 exemplars (already done) ✓
- 46 from candidates & extraction

**Each quotation complete when:**
- All fields filled per QUOTATION_TEMPLATE.md checklist
- Latin verified against original PDF
- Source attribution complete (author + work + scholar + page)
- Linguistic notes written (2-4 sentences)
- Magical significance documented (3-5 sentences)
- Scholar commentary included (3-5 sentences)
- review_status = DRAFT (ready for next phase review)
- confidence = HIGH or MEDIUM (not LOW)

**Portal success when:**
- quotations/index.html shows all quotations as cards
- Each quotation/\{slug\}/index.html displays with full commentary
- All 569 pages generated without errors
- Navigation includes Quotations tab on all pages

---

## If You Get Stuck

### Common Problem: Candidates missing source information

**Problem:** 100 candidates have only latin_text, need source attribution

**Solution:** 
1. Take the Latin text
2. Search E:\pdf/ for that exact phrase
3. Note which PDF it came from
4. Search that PDF for scholar's commentary around it
5. Note author of original work, title, scholar name, page

**Tool:** Use RESEARCH_PIPELINE.md to understand folder structure

### Common Problem: Source text not in database

**Problem:** You want to link quotation to "Corpus Hermeticum" but can't find texts.slug

**Solution:**
1. Check if text exists: `sqlite3 portal/portal.db "SELECT slug FROM texts WHERE title LIKE '%Hermet%'"`
2. If not found, you need to add it to database
3. Get text info (author, title, tradition, publication_year)
4. Add to data/sources_raw.json OR manually insert to texts table
5. Then link quotation to it

**See:** QUOTATIONS_ONTOLOGY.md, "Issue 1: Source Text Normalization"

### Common Problem: JSON syntax errors

**Problem:** Run seeding script and get JSON error

**Solution:**
1. Validate JSON: `python -c "import json; json.load(open('data/quotations_seed.json'))"`
2. If error, check for:
   - Missing quotes around strings
   - Trailing commas in arrays
   - Unescaped quotes in text (use \" for quotes inside strings)
3. Use JSON validator online if unsure

---

## Commit Message Template

When you commit quotations work, use this format:

```
Add X quotations to database: [brief description]

- Quotations added: N (candidates verified and enriched)
- Quotations from extraction: M (new systematic extraction)
- Quotations complete/reviewed: K

Status:
- Total quotations: 4 + N + M (running total toward 50)
- Phase 2 progress: X% (toward Oct 31 goal)
- Blockers: [if any]

Testing:
- [✓] Database seeding successful
- [✓] Portal generation successful  
- [✓] All quotation pages render
- [✓] Navigation updated

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

## Next Agent: You're Ready

You have:
- ✓ 4 exemplar quotations (template to follow)
- ✓ 100 candidate quotations (ready for enrichment)
- ✓ Complete documentation (TEMPLATE, PIPELINE, ONTOLOGY, MANIFEST)
- ✓ Database schema (ready to scale)
- ✓ Portal infrastructure (ready to generate pages)
- ✓ GitHub repository (ready to commit)

Everything is set up. The hard part (infrastructure) is done. Now it's systematic enrichment and extraction.

**You can achieve 50 quotations by Oct 31. Here's how:**
1. Week 1-2: Verify & complete 10-15 candidates
2. Week 3-4: Extract 20-30 new from Priority 1 folders
3. Ongoing: Write commentary on all

Timeline is tight but achievable at ~1-2 quotations per working day.

Questions? See the four documentation files above.

Ready to go.

---

**Prepared by:** Claude Haiku 4.5  
**Date:** 2026-09-28  
**Status:** System ready for handoff
