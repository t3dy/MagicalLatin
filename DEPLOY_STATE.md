# MagicalLatin Deployment State

**Last Updated:** 2026-09-27  
**Status:** ✅ DEPLOYED  
**Repository:** https://github.com/t3dy/MagicalLatin

## Live URLs

| Component | URL | Status |
|---|---|---|
| **Gamified Reader** | https://t3dy.github.io/MagicalLatin/ | ✅ Ready (configure GitHub Pages) |
| **Knowledge Portal** | https://t3dy.github.io/MagicalLatin/portal/ | ✅ Generated in `/docs` |
| **GitHub Repository** | https://github.com/t3dy/MagicalLatin | ✅ Pushed |

## Configuration Required

### GitHub Pages Setup
1. Go to https://github.com/t3dy/MagicalLatin/settings/pages
2. **Source:** Select "Deploy from a branch"
3. **Branch:** `main`
4. **Folder:** `/docs` ← This is critical
5. Save and wait ~1 minute for deployment

⚠️ **CRITICAL:** The `/docs` folder must be selected as the source, not root. This is where all generated portal HTML is located.

## Directory Structure

```
MagicalLatin/
├── index.html                    # Gamified reader entry point
├── app.js                        # Game logic
├── style.css                     # Medieval dark-gold theme
├── dictionary.js                 # Vocabulary fallback
├── data/
│   ├── passages.json             # 101 Latin passages
│   ├── rituals.json              # Ritual walkthroughs
│   ├── alchemy.json              # Alchemy lab
│   ├── sources_raw.json          # 445 extracted PDF metadata
│   └── bibliography.json         # Citation data
├── portal/
│   ├── scripts/
│   │   ├── init_db.py            # Create database schema
│   │   ├── seed_from_json.py     # Populate from sources
│   │   └── build_site.py         # Generate static HTML
│   ├── portal.db                 # SQLite knowledge base (1137 files generated)
│   └── portal.css                # Portal styling
├── docs/                         # ✅ GENERATED (GitHub Pages source)
│   ├── index.html                # Portal home (1 file)
│   ├── portal.css                # Portal stylesheet
│   ├── texts/                    # 421 text pages + index
│   ├── authors/                  # 125 author pages + index
│   ├── concepts/                 # 18 concept pages + index
│   └── search.html               # Search page
├── .git/                         # Git repository
├── .gitignore                    # Excludes *.db, venv, etc.
├── README.md                     # Comprehensive documentation
├── CLAUDE.md                     # Project instructions
├── STYLEGUIDE.md                 # Passage schema (reader)
└── DEPLOY_STATE.md               # This file
```

## Database Content (Portal)

**Located:** `portal/portal.db` (SQLite)

| Table | Count | Provenance |
|---|---|---|
| `texts` | 421 | Extracted from E:\pdf/ folders |
| `figures` | 125 | Author names from PDF filenames |
| `concepts` | 18 | Traditions/doctrines |
| `bibliography` | 0 | Ready for manual entry |
| Indexes | 6 | `tradition`, `year`, `entity_type` |

**Provenance Fields (all rows):**
- `source_method`: 'SEED_DATA' (automatic extraction)
- `review_status`: 'DRAFT' (auto-extracted), 'REVIEWED', or 'VERIFIED'
- `confidence`: 'MEDIUM' (default), 'HIGH', or 'LOW'

## Rebuild Pipeline

If you add sources to `E:\pdf` or need to regenerate:

```bash
cd C:\Dev\MagicalLatin

# 1. Extract new PDF metadata
python extract_sources.py
# → data/sources_raw.json

# 2. Re-create database (optional if schema unchanged)
python portal/scripts/init_db.py
# → portal/portal.db

# 3. Seed database from extracted sources
python portal/scripts/seed_from_json.py
# → Populates texts, figures, concepts

# 4. Generate static HTML
python portal/scripts/build_site.py
# → docs/ (564+ pages)

# 5. Commit and push
git add docs/ data/sources_raw.json
git commit -m "Update portal with new sources"
git push origin main
```

All scripts are **idempotent** (safe to re-run):
- `init_db.py`: Creates tables if missing
- `seed_from_json.py`: Skips duplicates
- `build_site.py`: Overwrites old files

## Sources Indexed (2026-09-27)

**445 magical PDFs from E:\pdf** scanned across 21+ traditions:

| Tradition | Count | Key Texts |
|---|---|---|
| Alchemy | 54 | Paracelsus, Jabir, laboratory operations |
| Hermetic | 54 | Hermes Trismegistus, Corpus Hermeticum |
| Western Esotericism | 53 | General occult philosophy |
| Rosicrucian | 44 | Rosicrucian manifestos, orders |
| Tarot | 42 | Divination, card symbolism |
| Renaissance Magic | 34 | Ficino, Pico, Renaissance mages |
| Neoplatonism | 28 | Plotinus, Porphyry, mystical philosophy |
| Gnosticism | 24 | Gnostic texts, cosmology |
| Crowley | 22 | Aleister Crowley, Thelema |
| Magic (General) | 22 | Magic theory, spellcraft |
| Kabbalah | 16 | Jewish mysticism, Sefirot |
| Lull | 11 | Ramon Lull, ars combinatoria |
| Others | 61 | Voynich, Bohme, Apuleius, scholars |

**Total: 445 PDFs → 421 unique texts (after deduplication)**

## Verification Checklist

- ✅ Gamified reader fully featured (101 passages, XP/level, vocab, quiz, alchemy, rituals)
- ✅ Knowledge portal database created (SQLite, 8 tables, indexes)
- ✅ 445 PDFs scanned and indexed
- ✅ Static HTML generated (564+ pages: texts, authors, concepts)
- ✅ Repository pushed to GitHub (main branch)
- ✅ `docs/` directory ready for GitHub Pages
- ⏳ **TODO:** Enable GitHub Pages in repository settings (select `/docs` folder)

## Known Limitations

1. **Filename extraction only** — Portal author/title parsed from PDF filenames, not PDF metadata. Some files may have garbled names (mitigated with DRAFT status).

2. **No full-text search yet** — `search.html` exists but JavaScript implementation (`search.js`) needs completion. Will require indexing docs/search.json.

3. **Bibliography sparse** — Only extracted from filenames. Manual entry needed for proper citations.

4. **Reader coverage** — 101 passages must map to all concepts in `C:\Dev\medievalmagicdb` (ongoing cross-reference).

## Next Steps (Future Sprints)

1. **Immediate:** Enable GitHub Pages in repository settings (5 minutes)
2. **Reader:** Ensure all 101 passages are in database (coverage check vs medievalmagicdb)
3. **Portal:** Enrich author biographies by mining source PDFs
4. **Portal:** Add essay pages synthesizing concepts
5. **Portal:** Implement full-text search
6. **Reader:** Link passage citations to portal texts
7. **Portal:** Image gallery of manuscript pages

## Support

- **Documentation:** `README.md`, `CLAUDE.md`, `STYLEGUIDE.md`
- **Project Wiki:** `C:\Dev\wiki\project_magicallatin.md`
- **Portal Framework Reference:** `C:\Dev\wiki\framework_knowledge_portal.md`
- **Related Projects:** [[project_medievalmagicdb]], [[project_renaissancemagic]]

## Deployment Notes

**Portal is 100% static HTML** — no server required. GitHub Pages will serve directly from the `docs/` branch.

**For local testing:**
```bash
# Test reader
cd C:\Dev\MagicalLatin
python -m http.server 5180
# → http://localhost:5180

# Test portal (any static server)
cd C:\Dev\MagicalLatin/docs
python -m http.server 5181
# → http://localhost:5181
```

---

**Archive:** This file tracks live deployment state. Update it when pushing changes or modifying GitHub Pages configuration.
