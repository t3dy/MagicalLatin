#!/usr/bin/env python3
"""
Seed MagicalLatin portal database from JSON sources.
Converts extracted PDF metadata into database entries.
"""

import json
import sqlite3
from pathlib import Path
import re

DB_PATH = Path(__file__).parent.parent / 'portal.db'
SOURCES_FILE = Path(__file__).parent.parent.parent / 'data' / 'sources_raw.json'

# Mapping of PDF folders to traditions
FOLDER_TO_TRADITION = {
    'magic': 'Western Magic',
    'Grimoire': 'Grimoire Tradition',
    'hermetic': 'Hermeticism',
    'Kabbalah': 'Kabbalah',
    'kabbalah': 'Kabbalah',
    'Kabbalah and Hermeticism': 'Hermetic Kabbalah',
    'magic squares': 'Magic Squares',
    'neoplatonism': 'Neoplatonism',
    'renaissance magic': 'Renaissance Magic',
    'Rosicrucian': 'Rosicrucianism',
    'Tarot': 'Tarot',
    'Western Esotericism and Occult': 'Western Esotericism',
    'western esotericism religious studies': 'Western Esotericism',
    'esoteric': 'Esoteric Studies',
    'esoteric studies': 'Esoteric Studies',
    'gnosticism': 'Gnosticism',
    'art of memory': 'Art of Memory',
    'alchemy': 'Alchemy',
    'Astrology and Prophecy': 'Astrology',
    'bohme': 'Jacob Böhme',
    'crowley': 'Crowleyanism',
    'Lull': 'Ramon Lull',
    'Voynich Studies': 'Voynich Manuscript',
    'albertus magnus': 'Albertus Magnus',
    'Apuleis': 'Apuleius',
    'Brian Copenhaver': 'Renaissance Magic',
    'David Lapoujade': 'Continental Philosophy',
    'Eugenio Garin': 'Renaissance Magic',
    'FM Van Helmont': 'Van Helmont Family',
    'Francois Secret': 'Renaissance Occultism',
    'Stephen Clucas': 'Western Esotericism',
}

def slugify(text):
    """Convert text to slug format."""
    if not text:
        return None
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')[:80]
    return slug

def extract_author_from_filename(filename):
    """Try to extract author name from filename."""
    # Remove .pdf
    name = filename.replace('.pdf', '')

    # Try various patterns
    patterns = [
        r'^([^-]+)\s*-\s*',  # "Author - Title"
        r'^([^(]+)\s*\(',     # "Author (Title)"
    ]

    for pattern in patterns:
        match = re.match(pattern, name)
        if match:
            author = match.group(1).strip()
            if author and len(author) < 100:
                return author

    return None

def seed_texts(conn, sources):
    """Seed texts table from extracted sources."""
    c = conn.cursor()
    count = 0

    print(f"Seeding {len(sources)} texts...")

    for source in sources:
        # Extract data
        title = source.get('title', 'Unknown')
        author = source.get('author')
        if not author:
            author = extract_author_from_filename(source.get('filename', ''))

        folder = source.get('folder', 'unknown')
        tradition = FOLDER_TO_TRADITION.get(folder, 'Western Esotericism')
        slug = slugify(title)

        if not slug:
            continue

        # Check for duplicates
        c.execute('SELECT id FROM texts WHERE slug = ?', (slug,))
        if c.fetchone():
            continue

        try:
            c.execute('''
                INSERT INTO texts
                (slug, title, authors, tradition, text_type, folder, pdf_path, summary,
                 source_method, review_status, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                slug,
                title,
                author or '',
                tradition,
                'primary',
                folder,
                source.get('path', ''),
                title[:200],  # Use title as summary initially
                'SEED_DATA',
                'DRAFT',
                'MEDIUM'
            ))
            count += 1
        except sqlite3.IntegrityError:
            continue

    conn.commit()
    print(f"  ✓ Inserted {count} texts")
    return count

def seed_figures(conn, sources):
    """Extract and seed unique authors as figures."""
    c = conn.cursor()
    authors_seen = set()
    count = 0

    print(f"Extracting unique authors...")

    for source in sources:
        author = source.get('author')
        if not author:
            author = extract_author_from_filename(source.get('filename', ''))

        if author and author not in authors_seen and len(author) < 100:
            authors_seen.add(author)
            slug = slugify(author)

            if not slug:
                continue

            # Check for duplicates
            c.execute('SELECT id FROM figures WHERE slug = ?', (slug,))
            if c.fetchone():
                continue

            try:
                c.execute('''
                    INSERT INTO figures
                    (slug, name, summary, source_method, review_status, confidence)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    slug,
                    author,
                    author,  # Use name as summary initially
                    'SEED_DATA',
                    'DRAFT',
                    'MEDIUM'
                ))
                count += 1
            except sqlite3.IntegrityError:
                continue

    conn.commit()
    print(f"  ✓ Inserted {count} author figures")
    return count

def seed_folder_concepts(conn, sources):
    """Create concepts from the main traditions/folders."""
    c = conn.cursor()
    traditions_seen = set()
    count = 0

    print(f"Creating tradition concepts...")

    for source in sources:
        folder = source.get('folder')
        tradition = FOLDER_TO_TRADITION.get(folder)

        if tradition and tradition not in traditions_seen:
            traditions_seen.add(tradition)
            slug = slugify(tradition)

            if not slug:
                continue

            c.execute('SELECT id FROM concepts WHERE slug = ?', (slug,))
            if c.fetchone():
                continue

            try:
                c.execute('''
                    INSERT INTO concepts
                    (slug, name, concept_type, tradition, summary, source_method, review_status, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    slug,
                    tradition,
                    'doctrine',
                    tradition,
                    f"Tradition and texts related to {tradition}",
                    'SEED_DATA',
                    'DRAFT',
                    'MEDIUM'
                ))
                count += 1
            except sqlite3.IntegrityError:
                continue

    conn.commit()
    print(f"  ✓ Inserted {count} tradition concepts")
    return count

def main():
    """Load sources and seed database."""

    if not SOURCES_FILE.exists():
        print(f"ERROR: {SOURCES_FILE} not found")
        print(f"Run extract_sources.py first")
        return

    print(f"Loading sources from {SOURCES_FILE}...")
    with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
        sources = json.load(f)

    print(f"Loaded {len(sources)} sources\n")

    # Connect to database
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found")
        print(f"Run init_db.py first")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')

    try:
        # Seed in order of dependencies
        count_concepts = seed_folder_concepts(conn, sources)
        count_figures = seed_figures(conn, sources)
        count_texts = seed_texts(conn, sources)

        print(f"\n{'='*60}")
        print(f"Seeding complete!")
        print(f"  Concepts: {count_concepts}")
        print(f"  Figures: {count_figures}")
        print(f"  Texts: {count_texts}")
        print(f"{'='*60}")

    finally:
        conn.close()

if __name__ == '__main__':
    main()
