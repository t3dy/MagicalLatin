# Phase 2 Workflow: Quotation Enrichment & Extraction

**Status:** PHASE 2 INITIATED 2026-10-04
**Goal:** 50 total quotations by Oct 31 (need 46 more)
**Pace:** ~1.7 quotations/day to reach deadline

## Current Pipeline

### 1. Verification Agent (Running)
- **Task:** Verify 4 HIGH-confidence candidates + extract 10-15 Priority 1 quotations
- **Output:** `data/quotations_phase2_batch1.json` (complete quotation entries)
- **Timeline:** TBD (complex PDF research)

### 2. Integration (When Agent Returns)
When the agent completes and produces `data/quotations_phase2_batch1.json`:

```bash
# 1. Merge new quotations into seed
python scripts/merge_quotations.py \
  --source data/quotations_phase2_batch1.json \
  --target data/quotations_seed.json

# 2. Validate JSON
python -c "import json; json.load(open('data/quotations_seed.json')); print('✓ Valid')"

# 3. Seed database
python portal/scripts/seed_quotations.py

# 4. Verify database
sqlite3 portal/portal.db "SELECT COUNT(*) FROM quotations;"

# 5. Rebuild portal
python portal/scripts/build_site_final.py

# 6. Commit & push
git add data/quotations_seed.json docs/
git commit -m "Phase 2 Batch 1: Add verified quotations (+N)"
git push
```

### 3. Parallel Extraction (While Agent Works)
If verification takes time, start parallel extraction from:
- **Priority 1A:** Grimoire (Sourceworks continued)
- **Priority 1B:** Hermetic (Copenhaver continued)
- **Priority 1C:** Kabbalah (Cohen Sheʿur Qomah - 18 candidates already extracted)

## Batch Schedule

To reach 50 by Oct 31, target this intake:
- **Batch 1** (due ~Oct 10): 14-19 quotations (4 verified HIGH + 10-15 new)
- **Batch 2** (due ~Oct 17): 15-20 quotations (systematic extraction)
- **Batch 3** (due ~Oct 24): 10-15 quotations (final push)

## Success Criteria

Each quotation in batch is COMPLETE when:
- [ ] Latin text verified against PDF
- [ ] Translation checked for accuracy
- [ ] Source author & work identified
- [ ] Scholar name identified
- [ ] Page reference located
- [ ] All 3 commentary sections filled (2-4 sentences each)
- [ ] All 15 fields present per QUOTATION_TEMPLATE.md
- [ ] JSON validates
- [ ] Database seeds without error
- [ ] Portal pages generate

## Reference Commands

```bash
# Count current quotations
sqlite3 portal/portal.db "SELECT COUNT(*) FROM quotations;"

# Check schema
sqlite3 portal/portal.db ".schema quotations"

# List all quotation slugs
sqlite3 portal/portal.db "SELECT slug FROM quotations ORDER BY slug;"

# Find by tradition
sqlite3 portal/portal.db "SELECT COUNT(*) FROM quotations WHERE tags LIKE '%hermetic%';"
```

## Blocking Issues

None currently. All infrastructure ready:
- ✅ Database schema with quotations tables
- ✅ Seeding scripts (seed_quotations.py)
- ✅ Portal generation (build_site_final.py)
- ✅ Landing page + card grid working
- ✅ Detail pages rendering
- ✅ GitHub Pages live

## Notes

- Agent is working on comprehensive verification to avoid rework
- Raw candidates are in quotation_candidates.json (100 items)
- HIGH-confidence (4) are priority; MEDIUM (96) are secondary
- Rich source material available: Copenhaver (30 candidates), Cohen (18), Crowley (15), etc.
- Top quotation sources by candidate count:
  - Copenhaver Hermetica: 30
  - Cohen Sheʿur Qomah: 18
  - Crowley Magic: 15
  - Skinner/Rankine Goetia: 11
  - McIntosh Rosicrucian: 9

---

**Next check-in:** When Phase 2 Batch 1 lands (expect agent completion notification)
