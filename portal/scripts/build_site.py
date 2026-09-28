#!/usr/bin/env python3
"""
Build static HTML site for MagicalLatin knowledge portal.
Generates pages from database and outputs to docs/ directory.
"""

import sqlite3
from pathlib import Path
import json
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / 'portal.db'
OUTPUT_DIR = Path(__file__).parent.parent.parent / 'docs'

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — MagicalLatin Knowledge Portal</title>
    <link rel="stylesheet" href="/MagicalLatin/portal.css">
</head>
<body>
    <nav class="header">
        <div class="nav-container">
            <h1><a href="/MagicalLatin/">MagicalLatin</a></h1>
            <ul>
                <li><a href="/MagicalLatin/">Home</a></li>
                <li><a href="/MagicalLatin/texts/">Texts</a></li>
                <li><a href="/MagicalLatin/authors/">Authors</a></li>
                <li><a href="/MagicalLatin/concepts/">Concepts</a></li>
                <li><a href="/MagicalLatin/search.html">Search</a></li>
            </ul>
        </div>
    </nav>

    <main>
        {content}
    </main>

    <footer>
        <p>MagicalLatin Knowledge Portal • Generated {generated_date}</p>
    </footer>
</body>
</html>
'''

CSS_TEMPLATE = '''
:root {
    --color-dark: #1a1a1a;
    --color-gold: #d4af37;
    --color-text: #e8e8e8;
    --color-border: #333;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Georgia', serif;
    background: var(--color-dark);
    color: var(--color-text);
    line-height: 1.6;
}

.header {
    background: var(--color-dark);
    border-bottom: 2px solid var(--color-gold);
    padding: 2rem 0;
    margin-bottom: 2rem;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-container h1 {
    font-size: 1.8rem;
    color: var(--color-gold);
}

.nav-container a {
    color: var(--color-gold);
    text-decoration: none;
}

.nav-container a:hover {
    text-decoration: underline;
}

.nav-container ul {
    display: flex;
    list-style: none;
    gap: 2rem;
}

main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

h1 {
    color: var(--color-gold);
    margin-bottom: 1rem;
    font-size: 2rem;
}

h2 {
    color: var(--color-gold);
    margin: 1.5rem 0 0.5rem 0;
    font-size: 1.4rem;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.card {
    border: 1px solid var(--color-border);
    padding: 1.5rem;
    background: rgba(212, 175, 55, 0.02);
    transition: all 0.3s;
}

.card:hover {
    border-color: var(--color-gold);
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.1);
}

.card h3 {
    color: var(--color-gold);
    margin-bottom: 0.5rem;
}

.card a {
    color: var(--color-gold);
    text-decoration: none;
}

.card a:hover {
    text-decoration: underline;
}

.meta {
    font-size: 0.9rem;
    color: #aaa;
    margin-top: 1rem;
}

footer {
    text-align: center;
    padding: 2rem;
    border-top: 1px solid var(--color-border);
    margin-top: 4rem;
    color: #888;
}
'''

def ensure_output_dir():
    """Create output directory structure."""
    (OUTPUT_DIR / 'texts').mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'authors').mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'concepts').mkdir(parents=True, exist_ok=True)

def write_html(path, content):
    """Write HTML file with template wrapper."""
    path.parent.mkdir(parents=True, exist_ok=True)

    # Extract title from content or use path
    title = path.stem.replace('-', ' ').title()

    html = HTML_TEMPLATE.format(
        title=title,
        content=content,
        generated_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

def build_index_page(conn):
    """Build main index page."""
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM texts')
    text_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM figures')
    author_count = c.fetchone()[0]

    c.execute('SELECT COUNT(*) FROM concepts')
    concept_count = c.fetchone()[0]

    content = f'''
        <h1>MagicalLatin Knowledge Portal</h1>

        <p>A comprehensive knowledge base of magical texts, authors, and concepts from Western esoteric traditions.</p>

        <div class="grid">
            <div class="card">
                <h3><a href="texts/">Texts</a></h3>
                <p>{text_count} magical documents and primary sources</p>
                <p class="meta">Grimoires, alchemical treatises, Kabbalistic works, and more</p>
            </div>

            <div class="card">
                <h3><a href="authors/">Authors</a></h3>
                <p>{author_count} scholarly and primary source authors</p>
                <p class="meta">Occult philosophers, medieval magicians, Renaissance scholars</p>
            </div>

            <div class="card">
                <h3><a href="concepts/">Concepts</a></h3>
                <p>{concept_count} doctrines and traditions</p>
                <p class="meta">Hermeticism, Kabbalah, Alchemy, Tarot, and more</p>
            </div>
        </div>

        <h2>Traditions Covered</h2>
        <ul style="margin-left: 2rem; margin-bottom: 2rem;">
            <li>Hermeticism & Hermetic Magic</li>
            <li>Kabbalah & Jewish Mysticism</li>
            <li>Alchemy & Alchemical Philosophy</li>
            <li>Grimoire Tradition & Ceremonial Magic</li>
            <li>Renaissance Magic & Neoplatonism</li>
            <li>Western Esotericism & Occult Philosophy</li>
            <li>Tarot & Divination</li>
            <li>Rosicrucianism & Mystical Orders</li>
        </ul>
    '''

    write_html(OUTPUT_DIR / 'index.html', content)
    print(f"  ✓ index.html")

def build_texts_index(conn):
    """Build texts listing page."""
    c = conn.cursor()

    c.execute('SELECT slug, title, authors, publication_year, tradition FROM texts ORDER BY title')
    texts = c.fetchall()

    # Group by tradition
    by_tradition = {}
    for slug, title, authors, year, tradition in texts:
        if tradition not in by_tradition:
            by_tradition[tradition] = []
        by_tradition[tradition].append((slug, title, authors, year))

    content = '<h1>Magical Texts</h1>\n<p>Primary and secondary sources on magic in Latin and European traditions.</p>\n'

    for tradition in sorted(by_tradition.keys()):
        items = by_tradition[tradition]
        content += f'\n<h2>{tradition}</h2>\n<div class="grid">\n'

        for slug, title, authors, year in sorted(items, key=lambda x: x[1]):
            author_str = f' — {authors}' if authors else ''
            year_str = f' ({year})' if year else ''
            content += f'''
    <div class="card">
        <h3><a href="/MagicalLatin/texts/{slug}/">{title}</a></h3>
        <p class="meta">{author_str}{year_str}</p>
    </div>
'''

        content += '</div>\n'

    write_html(OUTPUT_DIR / 'texts' / 'index.html', content)
    print(f"  ✓ texts/index.html")

    # Build individual text pages
    for slug, title, authors, year, tradition in texts:
        text_content = f'''
        <h1>{title}</h1>
        <div class="meta">
            <p><strong>Tradition:</strong> {tradition}</p>
            {f'<p><strong>Author:</strong> {authors}</p>' if authors else ''}
            {f'<p><strong>Year:</strong> {year}</p>' if year else ''}
        </div>

        <h2>Entry</h2>
        <p>This is a primary or secondary source in the {tradition} tradition.</p>
        '''

        write_html(OUTPUT_DIR / 'texts' / slug / 'index.html', text_content)

    print(f"  ✓ {len(texts)} text pages")

def build_authors_index(conn):
    """Build authors listing page."""
    c = conn.cursor()

    c.execute('SELECT slug, name FROM figures ORDER BY name')
    authors = c.fetchall()

    content = '<h1>Authors & Scholars</h1>\n<p>Magical philosophers, occultists, and scholars in the Western esoteric tradition.</p>\n'
    content += '<div class="grid">\n'

    for slug, name in authors:
        content += f'''
    <div class="card">
        <h3><a href="/MagicalLatin/authors/{slug}/">{name}</a></h3>
    </div>
'''

    content += '</div>\n'

    write_html(OUTPUT_DIR / 'authors' / 'index.html', content)
    print(f"  ✓ authors/index.html")

    # Build individual author pages
    for slug, name in authors:
        # Get texts by this author
        c.execute('SELECT slug, title, publication_year FROM texts WHERE authors LIKE ? ORDER BY publication_year', (f'%{name}%',))
        texts_by_author = c.fetchall()

        author_content = f'<h1>{name}</h1>\n'

        if texts_by_author:
            author_content += '<h2>Works</h2>\n<ul>\n'
            for text_slug, text_title, year in texts_by_author:
                year_str = f' ({year})' if year else ''
                author_content += f'    <li><a href="/MagicalLatin/texts/{text_slug}/">{text_title}</a>{year_str}</li>\n'
            author_content += '</ul>\n'

        write_html(OUTPUT_DIR / 'authors' / slug / 'index.html', author_content)

    print(f"  ✓ {len(authors)} author pages")

def build_concepts_index(conn):
    """Build concepts listing page."""
    c = conn.cursor()

    c.execute('SELECT slug, name, tradition FROM concepts ORDER BY tradition, name')
    concepts = c.fetchall()

    # Group by tradition
    by_tradition = {}
    for slug, name, tradition in concepts:
        if tradition not in by_tradition:
            by_tradition[tradition] = []
        by_tradition[tradition].append((slug, name))

    content = '<h1>Magical Concepts & Traditions</h1>\n<p>Key doctrines, practices, and traditions in Western magic.</p>\n'

    for tradition in sorted(by_tradition.keys()):
        items = by_tradition[tradition]
        content += f'\n<h2>{tradition}</h2>\n<div class="grid">\n'

        for slug, name in sorted(items, key=lambda x: x[1]):
            content += f'''
    <div class="card">
        <h3><a href="/MagicalLatin/concepts/{slug}/">{name}</a></h3>
    </div>
'''

        content += '</div>\n'

    write_html(OUTPUT_DIR / 'concepts' / 'index.html', content)
    print(f"  ✓ concepts/index.html")

    # Build individual concept pages
    for slug, name, tradition in concepts:
        concept_content = f'''
        <h1>{name}</h1>
        <p><strong>Tradition:</strong> {tradition}</p>

        <h2>Description</h2>
        <p>This concept is central to the {tradition} tradition within Western esotericism.</p>
        '''

        write_html(OUTPUT_DIR / 'concepts' / slug / 'index.html', concept_content)

    print(f"  ✓ {len(concepts)} concept pages")

def build_search_page():
    """Build search page."""
    search_content = '''
        <h1>Search</h1>
        <div id="search-box">
            <input type="text" id="search-input" placeholder="Search texts, authors, concepts...">
            <div id="search-results"></div>
        </div>

        <script src="/MagicalLatin/search.js"></script>
    '''

    write_html(OUTPUT_DIR / 'search.html', search_content)
    print(f"  ✓ search.html")

def write_css():
    """Write CSS stylesheet."""
    with open(OUTPUT_DIR / 'portal.css', 'w', encoding='utf-8') as f:
        f.write(CSS_TEMPLATE)
    print(f"  ✓ portal.css")

def main():
    """Build the entire static site."""

    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found")
        print(f"Run init_db.py and seed_from_json.py first")
        return

    print(f"Building MagicalLatin knowledge portal...")
    print(f"Output directory: {OUTPUT_DIR}\n")

    ensure_output_dir()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        print("Generating pages:")
        build_index_page(conn)
        build_texts_index(conn)
        build_authors_index(conn)
        build_concepts_index(conn)
        build_search_page()
        write_css()

        print(f"\n{'='*60}")
        print(f"✓ Portal built successfully!")
        print(f"  Output: {OUTPUT_DIR}")
        print(f"  Next: push to GitHub Pages")
        print(f"{'='*60}")

    finally:
        conn.close()

if __name__ == '__main__':
    main()
