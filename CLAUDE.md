# Claude Code Instructions — MagicalLatin

Gamified Latin reader for magical texts. Pure vanilla HTML/CSS/JS static site, no build system.

## Stack

- `index.html` — single-page app, all modals inline
- `app.js` — all logic: passage rendering, quiz, alchemy lab, XP/level, filters, localStorage
- `style.css` — medieval dark-gold theme, Cinzel + EB Garamond
- `dictionary.js` — word lookup fallback dictionary
- `data/passages.json` — the corpus (101 passages; see STYLEGUIDE.md for schema)
- `data/rituals.json` — step-by-step ritual walkthroughs
- `data/alchemy.json` — alchemy lab substances and operations
- **Dev server**: Python HTTP on port 5180 (`magical-latin` in `.claude/launch.json`)

## State

localStorage key `magicalLatin_v1`. Fields: `xp`, `level`, `wordsLooked` (map), `passagesRead` (set), `passagesTranslated` (set), `ritualsPerformed` (set), `readList` (set), `experimentsCount`.

## Features (all implemented)

- Card grid with era/tradition/difficulty filters, search, read-list filter
- Word-click vocabulary tracking with tooltip (Full/Hover/None/Interlinear scaffold modes)
- Prev/next navigation within current filter state
- Passage modal: Latin text, English gloss, vocab panel, source notes
- XP/level system: read (+10), translate (+25), ritual (+50), flashcard known (+3)
- Flashcard quiz over all looked-up words
- Alchemy Lab (alchemy.json)
- Ritual walkthroughs (rituals.json)
- Codex/stats modal with achievements
- Word coverage progress bar on each card

## Coverage Requirement

Every concept in `C:\Dev\medievalmagicdb` must be represented by at least one passage. The canonical concepts list is the one seeded in `medievalmagicdb/scripts/seed_comprehensive_coverage.py` and related batch scripts. Cross-reference before adding passages to confirm gaps.

## Passage Data

See `STYLEGUIDE.md` for the complete schema, field-by-field spec, traditions taxonomy, difficulty scale, bibliography format, and content requirements.

When adding passages, always:
1. Write to a Python script in the project root (not inline shell), run it, then delete it
2. Validate JSON after: `python -c "import json; data=json.load(open('data/passages.json',encoding='utf-8')); print(len(data), 'passages')"`
3. Normalize traditions to underscore_case (no spaces)

## Bibliography Research

Bibliography entries should cite the critical edition or standard scholarly translation. When uncertain, spawn a web-research agent rather than guessing. Format: `Author, Firstname. Title. Place: Publisher, Year. // Second source if needed.`

## Adding App Features

All UI logic is in `app.js`. Pattern: add HTML to `index.html`, wire event listeners in `setupEventListeners()`, add rendering logic near related features. State always goes through `STATE` object and `saveState()`.
