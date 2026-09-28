#!/usr/bin/env python3
"""
Seed quotations into the MagicalLatin portal database.
Converts quotations_seed.json into database records.
"""

import json
import sqlite3
from pathlib import Path
import re

DB_PATH = Path(__file__).parent.parent / 'portal.db'
QUOTATIONS_FILE = Path(__file__).parent.parent.parent / 'data' / 'quotations_seed.json'

def slugify(text):
    """Convert text to slug."""
    if not text:
        return None
    slug = text.lower()[:100]
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

def seed_quotations(conn, quotations):
    """Seed quotations table."""
    c = conn.cursor()
    count = 0

    for q in quotations:
        # Create slug from Latin text
        slug = slugify(q.get('latin_text'))
        if not slug:
            continue

        # Check for duplicate
        c.execute('SELECT id FROM quotations WHERE slug = ?', (slug,))
        if c.fetchone():
            continue

        try:
            c.execute('''
                INSERT INTO quotations
                (slug, latin_text, translation, source_text_slug, source_author,
                 source_work_title, referenced_in_slug, scholar_name,
                 quotation_context, linguistic_notes, magical_significance,
                 page_reference, scholar_commentary, tags,
                 source_method, review_status, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                slug,
                q.get('latin_text'),
                q.get('translation'),
                q.get('source_text_slug'),
                q.get('source_author'),
                q.get('source_work_title'),
                q.get('referenced_in_slug'),
                q.get('scholar_name'),
                q.get('quotation_context'),
                q.get('linguistic_notes'),
                q.get('magical_significance'),
                q.get('page_reference'),
                q.get('scholar_commentary'),
                json.dumps(q.get('tags', [])),
                q.get('source_method', 'EXTRACTED'),
                q.get('review_status', 'DRAFT'),
                q.get('confidence', 'MEDIUM'),
            ))
            count += 1
        except sqlite3.IntegrityError:
            continue

    conn.commit()
    return count

def seed_quotation_commentary(conn, quotations):
    """Extract and seed commentary entries."""
    c = conn.cursor()
    count = 0

    for q in quotations:
        # Get quotation ID
        slug = slugify(q.get('latin_text'))
        c.execute('SELECT id FROM quotations WHERE slug = ?', (slug,))
        row = c.fetchone()
        if not row:
            continue

        quotation_id = row[0]

        # Add linguistic commentary
        if q.get('linguistic_notes'):
            try:
                c.execute('''
                    INSERT INTO quotation_commentary
                    (quotation_id, scholar_name, commentary_text, commentary_type)
                    VALUES (?, ?, ?, ?)
                ''', (
                    quotation_id,
                    q.get('scholar_name'),
                    q.get('linguistic_notes'),
                    'linguistic'
                ))
                count += 1
            except:
                pass

        # Add magical significance commentary
        if q.get('magical_significance'):
            try:
                c.execute('''
                    INSERT INTO quotation_commentary
                    (quotation_id, scholar_name, commentary_text, commentary_type, significance_level)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    quotation_id,
                    q.get('scholar_name'),
                    q.get('magical_significance'),
                    'magical',
                    'high'
                ))
                count += 1
            except:
                pass

        # Add main scholarly commentary
        if q.get('scholar_commentary'):
            try:
                c.execute('''
                    INSERT INTO quotation_commentary
                    (quotation_id, scholar_name, commentary_text, commentary_type)
                    VALUES (?, ?, ?, ?)
                ''', (
                    quotation_id,
                    q.get('scholar_name'),
                    q.get('scholar_commentary'),
                    'textual'
                ))
                count += 1
            except:
                pass

    conn.commit()
    return count

def main():
    """Load and seed quotations."""

    if not QUOTATIONS_FILE.exists():
        print(f"Note: {QUOTATIONS_FILE} not found")
        print(f"Run quotation_extractor.py first to create quotations_seed.json")
        return

    print(f"Loading quotations from {QUOTATIONS_FILE}...")
    with open(QUOTATIONS_FILE, 'r', encoding='utf-8') as f:
        quotations = json.load(f)

    print(f"Loaded {len(quotations)} quotations\n")

    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')

    try:
        print("Seeding quotations...")
        count_q = seed_quotations(conn, quotations)

        print(f"Seeding quotation commentary...")
        count_c = seed_quotation_commentary(conn, quotations)

        print(f"\n{'='*60}")
        print(f"✓ Quotations seeded!")
        print(f"  Quotations: {count_q}")
        print(f"  Commentary entries: {count_c}")
        print(f"{'='*60}")

    finally:
        conn.close()

if __name__ == '__main__':
    main()
