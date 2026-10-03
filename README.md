# MagicalLatin

A comprehensive platform for studying magical texts in Latin, combining an interactive gamified reader with a scholarly knowledge portal.

**🌐 Live Links:**
- **Gamified Reader:** https://t3dy.github.io/MagicalLatin/
- **Knowledge Portal:** https://t3dy.github.io/MagicalLatin/portal/ (texts, authors, concepts, quotations)

## Features

### 1. Gamified Latin Reader (`index.html`)
- **Filterable passage grid** by era, tradition, difficulty
- **Word-click vocabulary tracking** with multiple scaffold modes
- **Passage modals** with Latin text, English gloss, vocabulary, source notes
- **XP/level system**: read (+10), translate (+25), ritual (+50), vocabulary (+3)
- **Flashcard quiz** over all looked-up words
- **Alchemy Lab** with substances and alchemical operations
- **Ritual walkthroughs** with step-by-step guidance
- **Codex/stats modal** with achievements and progress

### 2. Knowledge Portal (`/portal`)
A scholarly reference portal indexing 445 magical texts from your research library, including:
- **421 indexed magical texts** from Western esoteric traditions
- **125 author biographies** (magicians, scholars, philosophers)
- **18 tradition concepts** (Hermeticism, Kabbalah, Alchemy, Tarot, etc.)
- **Text pages** with metadata, author info, tradition classification
- **Author pages** with bibliography of their works
- **Concept pages** mapping traditions across texts

## Architecture

```
MagicalLatin/
├── index.html              # Main gamified reader
├── app.js                  # Core game logic
├── style.css               # Styling (medieval dark-gold theme)
├── dictionary.js           # Word lookup fallback
├── data/
│   ├── passages.json       # 101 Latin passages (gamified reader)
│   ├── rituals.json        # Ritual walkthroughs
│   ├── alchemy.json        # Alchemy lab substances
│   └── sources_raw.json    # Extracted PDF metadata (445 sources)
├── portal/
│   ├── scripts/
│   │   ├── init_db.py      # Create SQLite schema
│   │   ├── seed_from_json.py   # Populate database
│   │   └── build_site.py   # Generate static HTML
│   ├── portal.db           # SQLite knowledge base
│   ├── portal.css          # Portal styling
│   └── [generated pages]   # Built HTML pages
└── docs/                   # Generated static site (GitHub Pages)
```

## Portal Architecture (Knowledge Portal)

Follows the **framework_knowledge_portal** pattern from IslamicateOccultPortal and MorignyPortal:

- **Database**: SQLite with normalized schema
  - `texts` — magical documents/PDFs
  - `figures` — authors and scholars
  - `concepts` — doctrines, practices, traditions
  - `bibliography` — scholarly references
  - `scholarly_refs` — citation links
  - Provenance fields: `source_method`, `review_status`, `confidence`

- **Pipeline** (all idempotent):
  1. `extract_sources.py` — Extract PDF metadata from E:\pdf folders
  2. `init_db.py` — Create schema
  3. `seed_from_json.py` — Populate database from extracted metadata
  4. `build_site.py` — Generate static HTML

- **Output**: Static HTML deployed to GitHub Pages from `/docs` directory

## Sources Indexed

The portal indexes 445 magical texts from these collections:

| Collection | Count | Traditions |
|---|---|---|
| Alchemy | 54 | Alchemical philosophy, laboratory operations |
| Hermetic | 54 | Hermeticism, Corpus Hermeticum |
| Western Esotericism | 53 | General esotericism, occult philosophy |
| Rosicrucian | 44 | Rosicrucianism, mystical orders |
| Tarot | 42 | Tarot divination, card symbolism |
| Renaissance Magic | 34 | Renaissance magicians, Neoplatonism |
| Neoplatonism | 28 | Plotinus, Porphyry, mystical philosophy |
| Gnosticism | 24 | Gnosticism, early Christian mysticism |
| Crowley | 22 | Aleister Crowley, Thelema |
| Magic | 22 | General magic theory |
| Kabbalah | 16 | Jewish Kabbalah, mystical Judaism |
| Lull | 11 | Ramon Lull, ars combinatoria |
| Stephen Clucas | 10 | Scholarly essays on esotericism |
| Western Esotericism (Studies) | 13 | Scholarly analysis |
| Grimoire | 5 | Grimoire tradition, demon binding |
| Albertus Magnus | 5 | Medieval magic, natural philosophy |
| Others | 22 | Voynich, Bohme, Apuleius, specific authors |

**Total: 445 sources across 21+ traditions**

## Gamified Features in Action

### Example 1: Vocabulary Learning
```
Passage: Hermetic Principle of Correspondence
Latin: "Quod est superius, est sicut quod inferius"

Click "quod" → tooltip shows:
  Definition: "that which" (relative pronoun)
  Grammar: Accusative neuter singular
  Context: Introduces a comparative clause
  Related: qualis, quantus (other interrogative/relative words)

XP Earned: +3 for learning the word
Vocabulary Strength: "quod" now at 75% mastery
```

### Example 2: Ritual Progress
```
Ritual: "Invocation of the Divine Name"
Steps Completed: 3/7
  ✓ Purification (read passage, +10 XP)
  ✓ Centering (translated passage, +25 XP)
  ✓ Vowel-work (completed flashcard, +3 XP)
  
Next: Invocation (read next passage)
Total Progress: 45% → Next level at 100%
Current Level: 5 "Initiate" → Level 6 "Adept"
```

### Example 3: Alchemy Lab
```
Available Substances: 23
  • Mercury (Philosophical) - volatility, intellect
  • Sulfur (Calcinatio) - red, transformative
  • Salt (Coagulation) - crystalline, foundation

Operations:
  • Dissolution: Mercury + Text Fragment = Insight
  • Fermentation: Two concepts + Time = New understanding
  • Distillation: Purify understanding of a concept

Recent Experiment: 
  "Dissolution of the Hermetic Principle"
  Result: Gained fluency in Correspondence Magic (+50 XP)
```

### Example 4: Knowledge Portal
```
Search: "Emerald Tablet"
Results:
  • Hermes Trismegistus - Author Page
  • Owen Davies - Scholar discussing it
  • "Quod est superius..." - Quotation with commentary
  • Hermetic Correspondence - Related concept
  
Each result links to full scholarly analysis, linguistic notes, 
magical significance, and bibliographic sources.
```

## Stack

- **Reader**: Vanilla HTML/CSS/JS, no build system
- **Portal**: SQLite + Python static generator
- **Hosting**: GitHub Pages (static site)
- **Dev Server**: Python HTTP (port 5180 for reader, port 5181 for portal)

## Usage

### Run the Gamified Reader
```bash
# Option 1: Python built-in server
cd C:\Dev\MagicalLatin
python -m http.server 5180

# Option 2: Use launch config in Claude Code
# .claude/launch.json has "magical-latin" config
```

Then open: http://localhost:5180

### Rebuild the Knowledge Portal
```bash
cd C:\Dev\MagicalLatin

# 1. Extract PDF metadata (if you add new sources to E:\pdf)
python extract_sources.py

# 2. Initialize database (one-time)
python portal/scripts/init_db.py

# 3. Seed database from metadata
python portal/scripts/seed_from_json.py

# 4. Build static site
python portal/scripts/build_site.py
```

Output goes to `docs/` — can be deployed to GitHub Pages.

## Development

### Coverage Requirement
Every concept in `C:\Dev\medievalmagicdb` must be represented by at least one passage in the gamified reader.

### Adding Passages
1. Write to `data/passages.json` following `STYLEGUIDE.md` schema
2. Validate: `python -c "import json; json.load(open('data/passages.json'))"`
3. Normalize tradition names to underscore_case

### Adding Portal Content
1. Edit `portal/scripts/seed_from_json.py` to adjust traditions/authors
2. Re-run the pipeline to regenerate
3. Commit `docs/` directory to deploy

## Scholarly Sources

The portal's authority is grounded in:
- Primary texts from E:\pdf (445 sources indexed)
- Coverage includes medieval to modern magical philosophy
- Traditions: Hermeticism, Kabbalah, Alchemy, Grimoire, Tarot, Rosicrucianism, Western Esotericism

See `/portal/docs/` for the generated portal and scholarly index.

## Status

- ✅ Reader: All features implemented
- ✅ Portal: Schema, seeding, site generator complete
- ✅ Sources: 445 texts indexed from research library
- ✅ Deployed: https://github.com/t3dy/MagicalLatin

## Next Steps

- [ ] Enrich author biographies from source PDFs
- [ ] Add essay pages synthesizing concepts across texts
- [ ] Implement full-text search in portal
- [ ] Link passages to portal texts
- [ ] Add image gallery of manuscript pages
- [ ] Create concept dependency graphs

## Related Projects

- `C:\Dev\medievalmagicdb` — medieval magic concepts database (coverage source)
- `C:\Dev\wiki\project_magicallatin.md` — wiki entry
- `E:\pdf\*` — Source PDF collection (445 texts indexed)
