#!/usr/bin/env python3
"""
Extract metadata from magic-related PDFs for MagicalLatin knowledge portal.
Uses filename extraction (fast, reliable) rather than PDF metadata parsing.
Outputs to data/sources_raw.json for manual review and seeding.
"""

import json
import os
from pathlib import Path
from collections import defaultdict
import re

MAGIC_FOLDERS = [
    'magic',
    'Grimoire',
    'hermetic',
    'Kabbalah',
    'kabbalah',
    'Kabbalah and Hermeticism',
    'magic squares',
    'neoplatonism',
    'renaissance magic',
    'Rosicrucian',
    'Tarot',
    'Western Esotericism and Occult',
    'western esotericism religious studies',
    'esoteric',
    'esoteric studies',
    'gnosticism',
    'art of memory',
    'alchemy',
    'Astrology and Prophecy',
    'bohme',
    'crowley',
    'Lull',
    'Voynich Studies',
    'albertus magnus',
    'Apuleis',
    'Brian Copenhaver',
    'David Lapoujade',
    'Eugenio Garin',
    'FM Van Helmont',
    'Francois Secret',
    'Stephen Clucas'
]

BASE_PDF_PATH = Path('E:/pdf')
OUTPUT_FILE = Path('data/sources_raw.json')

def extract_filename_metadata(filename):
    """Extract author, title from filename using common patterns."""
    name = filename.replace('.pdf', '').replace('_', ' ').strip()

    author = None
    title = None

    # Pattern 1: "Author - Title"
    if ' - ' in name:
        parts = name.split(' - ', 1)
        author = parts[0].strip()
        title = parts[1].strip()
    # Pattern 2: "Author (Title)"
    elif '(' in name and ')' in name:
        idx_open = name.index('(')
        idx_close = name.rindex(')')
        author = name[:idx_open].strip()
        title = name[idx_open+1:idx_close].strip()
    # Pattern 3: Just use filename as title
    else:
        title = name

    # Clean up
    if author and len(author) > 100:  # Likely not a real author
        author = None
    if not author or author.lower() == 'unknown':
        author = None

    return {'author': author, 'title': title}

def extract_pdf_metadata(filepath):
    """Extract metadata from PDF filename."""
    metadata = {
        'filename': filepath.name,
        'folder': filepath.parent.name,
        'path': str(filepath).replace('\\', '/'),
        'author': None,
        'title': None,
        'slug': None,
    }

    fname_meta = extract_filename_metadata(filepath.name)
    metadata['author'] = fname_meta['author']
    metadata['title'] = fname_meta['title']

    # Create slug from title
    if metadata['title']:
        slug = metadata['title'].lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')[:50]  # Max 50 chars
        metadata['slug'] = slug

    return metadata

def main():
    sources = []
    folder_counts = defaultdict(int)

    print(f"Scanning {len(MAGIC_FOLDERS)} magic-related folders...")
    print(f"Base path: {BASE_PDF_PATH}\n")

    for folder_name in sorted(MAGIC_FOLDERS):
        folder_path = BASE_PDF_PATH / folder_name
        if not folder_path.exists():
            continue

        pdfs = list(folder_path.glob('*.pdf'))
        if not pdfs:
            continue

        folder_counts[folder_name] = len(pdfs)
        print(f"  {folder_name}: {len(pdfs)} PDFs")

        for pdf_path in sorted(pdfs):
            metadata = extract_pdf_metadata(pdf_path)
            sources.append(metadata)

    print(f"\n{'='*70}")
    print(f"Total PDFs extracted: {len(sources)}")
    print(f"Folders processed: {len(folder_counts)}")
    print(f"{'='*70}\n")

    # Create output directory
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sources, f, indent=2, ensure_ascii=False)

    print(f"✓ Metadata exported to: {OUTPUT_FILE}")
    print(f"\nNext steps:")
    print(f"  1. Review {OUTPUT_FILE} to validate author/title extraction")
    print(f"  2. Create portal schema (init_db.py)")
    print(f"  3. Convert to seed.json for database seeding")
    print(f"  4. Build static site generator (build_site.py)")
    print(f"  5. Deploy to GitHub")

if __name__ == '__main__':
    main()
