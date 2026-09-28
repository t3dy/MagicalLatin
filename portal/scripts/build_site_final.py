#!/usr/bin/env python3
"""
Final comprehensive build for MagicalLatin knowledge portal.
Generates all pages: texts, authors, concepts, quotations, and sources.
Updated navigation includes Quotations tab throughout.
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
                <li><a href="/MagicalLatin/quotations/">Quotations</a></li>
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
    --color-latin: #c9a961;
    --color-commentary: #2a2a2a;
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
    padding: 1.5rem 0;
    margin-bottom: 2rem;
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1.5rem;
}

.nav-container h1 {
    font-size: 1.5rem;
    color: var(--color-gold);
    margin: 0;
}

.nav-container a {
    color: var(--color-gold);
    text-decoration: none;
    transition: all 0.2s;
}

.nav-container a:hover {
    text-decoration: underline;
    color: #fff;
}

.nav-container ul {
    display: flex;
    list-style: none;
    gap: 1rem;
    flex-wrap: wrap;
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
    border-bottom: 1px solid var(--color-border);
    padding-bottom: 0.5rem;
}

h2 {
    color: var(--color-gold);
    margin: 1.5rem 0 0.5rem 0;
    font-size: 1.4rem;
}

h3 {
    color: var(--color-latin);
    font-size: 1.1rem;
    margin: 1rem 0 0.5rem 0;
}

p {
    margin-bottom: 1rem;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.card {
    border: 1px solid var(--color-border);
    padding: 1.5rem;
    background: rgba(212, 175, 55, 0.02);
    transition: all 0.3s;
    cursor: pointer;
}

.card:hover {
    border-color: var(--color-gold);
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.1);
    transform: translateY(-2px);
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

.quotation-card {
    border-left: 3px solid var(--color-gold);
    background: rgba(201, 169, 97, 0.05);
}

.quotation-card .latin-text {
    font-style: italic;
    color: var(--color-latin);
    font-size: 0.95rem;
    margin: 1rem 0;
    line-height: 1.8;
    padding: 0.5rem 0 0.5rem 1rem;
    border-left: 2px solid var(--color-latin);
    font-family: 'Garamond', serif;
}

.quotation-card .translation {
    color: #999;
    font-size: 0.9rem;
    margin: 0.5rem 0;
    font-style: italic;
}

.meta {
    font-size: 0.9rem;
    color: #888;
    margin-top: 1rem;
}

.commentary {
    background: var(--color-commentary);
    padding: 1.5rem;
    margin: 1.5rem 0;
    border-left: 3px solid var(--color-gold);
    font-size: 0.95rem;
    line-height: 1.8;
}

.commentary .type {
    color: var(--color-gold);
    font-weight: bold;
    font-size: 0.85rem;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    letter-spacing: 0.05em;
}

.commentary .scholar {
    color: var(--color-latin);
    font-style: italic;
    margin-top: 1rem;
    font-size: 0.85rem;
}

footer {
    text-align: center;
    padding: 2rem;
    border-top: 1px solid var(--color-border);
    margin-top: 4rem;
    color: #666;
    font-size: 0.9rem;
}

a {
    color: var(--color-gold);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

ul, ol {
    margin-left: 2rem;
    margin-bottom: 1rem;
}

li {
    margin-bottom: 0.5rem;
}
'''

def ensure_output_dir():
    """Create output directory structure."""
    (OUTPUT_DIR / 'texts').mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'authors').mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'concepts').mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'quotations').mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'sources').mkdir(parents=True, exist_ok=True)

def write_html(path, content):
    """Write HTML file with template wrapper."""
    path.parent.mkdir(parents=True, exist_ok=True)

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

    c.execute('SELECT COUNT(*) FROM quotations')
    quotation_count = c.fetchone()[0]

    content = f'''
        <h1>MagicalLatin Knowledge Portal</h1>

        <p>A comprehensive knowledge base of magical texts, authors, concepts, and Latin quotations from Western esoteric traditions.</p>

        <div class="grid">
            <div class="card">
                <h3><a href="texts/">Texts & Sources</a></h3>
                <p>{text_count} magical documents and primary sources</p>
                <p class="meta">Grimoires, alchemical treatises, Kabbalistic works, and more</p>
            </div>

            <div class="card">
                <h3><a href="authors/">Scholars & Authors</a></h3>
                <p>{author_count} scholars and primary source authors</p>
                <p class="meta">Occult philosophers, medieval magicians, Renaissance scholars</p>
            </div>

            <div class="card">
                <h3><a href="concepts/">Doctrines & Traditions</a></h3>
                <p>{concept_count} magical traditions and concepts</p>
                <p class="meta">Hermeticism, Kabbalah, Alchemy, Tarot, and more</p>
            </div>

            <div class="card">
                <h3><a href="quotations/">Latin Quotations</a></h3>
                <p>{quotation_count} significant Latin passages with scholarly commentary</p>
                <p class="meta">Quotations from magical texts with linguistic and magical analysis</p>
            </div>
        </div>

        <h2>How to Use This Portal</h2>
        <ul>
            <li><strong>Texts & Sources:</strong> Browse 445 magical texts organized by tradition and date</li>
            <li><strong>Scholars & Authors:</strong> Explore biographies of magicians and scholars</li>
            <li><strong>Doctrines & Traditions:</strong> Learn about key concepts in magical philosophy</li>
            <li><strong>Latin Quotations:</strong> Read significant Latin passages with scholarly commentary explaining their linguistic and magical significance</li>
        </ul>

        <h2>Key Traditions Covered</h2>
        <ul>
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
    return (text_count, author_count, concept_count, quotation_count)

def build_texts_index(conn):
    """Build texts listing page."""
    c = conn.cursor()

    c.execute('SELECT slug, title, authors, publication_year, tradition FROM texts ORDER BY title')
    texts = c.fetchall()

    by_tradition = {}
    for slug, title, authors, year, tradition in texts:
        if tradition not in by_tradition:
            by_tradition[tradition] = []
        by_tradition[tradition].append((slug, title, authors, year))

    content = '<h1>Magical Texts & Sources</h1>\n<p>445 primary and secondary sources on magic in Western and Islamic traditions.</p>\n'

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

    for slug, title, authors, year, tradition in texts:
        text_content = f'''
        <h1>{title}</h1>
        <div class="meta">
            <p><strong>Tradition:</strong> {tradition}</p>
            {f'<p><strong>Author:</strong> {authors}</p>' if authors else ''}
            {f'<p><strong>Year:</strong> {year}</p>' if year else ''}
        </div>

        <h2>Entry</h2>
        <p>This is a source in the {tradition} tradition of magical philosophy.</p>
        '''

        write_html(OUTPUT_DIR / 'texts' / slug / 'index.html', text_content)

    print(f"  ✓ {len(texts)} text pages")

def build_authors_index(conn):
    """Build authors listing page."""
    c = conn.cursor()

    c.execute('SELECT slug, name FROM figures ORDER BY name')
    authors = c.fetchall()

    content = '<h1>Scholars & Magical Philosophers</h1>\n<p>Magical philosophers, occultists, and scholars in the Western esoteric tradition.</p>\n'
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

    for slug, name in authors:
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

    for slug, name, tradition in concepts:
        concept_content = f'''
        <h1>{name}</h1>
        <p><strong>Tradition:</strong> {tradition}</p>

        <h2>Description</h2>
        <p>This concept is central to the {tradition} tradition within Western esotericism.</p>
        '''

        write_html(OUTPUT_DIR / 'concepts' / slug / 'index.html', concept_content)

    print(f"  ✓ {len(concepts)} concept pages")

def build_quotations_index(conn):
    """Build quotations listing page."""
    c = conn.cursor()

    c.execute('''
        SELECT q.slug, q.latin_text, q.translation, q.scholar_name, q.source_work_title, q.source_text_slug
        FROM quotations q
        ORDER BY q.scholar_name, q.source_text_slug
    ''')
    quotations = c.fetchall()

    content = '<h1>Latin Quotations from Magical Texts</h1>\n'
    content += '<p>Significant Latin passages from magical texts, cited and analyzed by scholars with commentary on their linguistic and magical significance.</p>\n'
    content += f'<p class="meta"><strong>Total quotations:</strong> {len(quotations)}</p>\n'

    if quotations:
        content += '<div class="grid">\n'

        for slug, latin_text, translation, scholar, work_title, source_slug in quotations:
            latin_short = latin_text[:80] + '…' if len(latin_text) > 80 else latin_text

            content += f'''
    <div class="card quotation-card">
        <div class="latin-text">{latin_short}</div>
        {f'<div class="translation">"{translation[:100]}..."</div>' if translation else ''}
        <div class="meta">
            <span><strong>Scholar:</strong> {scholar or 'Unknown'}</span><br>
            <span><strong>Source:</strong> {work_title or source_slug}</span>
        </div>
        <p style="margin-top: 1rem;"><a href="/MagicalLatin/quotations/{slug}/">View Full Quotation →</a></p>
    </div>
'''

        content += '</div>\n'

    write_html(OUTPUT_DIR / 'quotations' / 'index.html', content)
    print(f"  ✓ quotations/index.html")

    for slug, latin_text, translation, scholar, work_title, source_slug in quotations:
        c.execute('''
            SELECT commentary_type, commentary_text, scholar_name, significance_level
            FROM quotation_commentary
            WHERE quotation_id = (SELECT id FROM quotations WHERE slug = ?)
            ORDER BY commentary_type
        ''', (slug,))
        commentaries = c.fetchall()

        c.execute('SELECT title, authors FROM texts WHERE slug = ?', (source_slug,))
        source_row = c.fetchone()
        source_title = source_row[0] if source_row else 'Unknown Source'

        quotation_content = f'''
        <h1>Latin Quotation</h1>

        <div class="quotation-card" style="border: none; background: rgba(201, 169, 97, 0.08); padding: 2rem; margin: 2rem 0; font-size: 1.05rem;">
            <div class="latin-text" style="border: none; padding: 0; margin: 0;">{latin_text}</div>
            {f'<div class="translation" style="margin-top: 1rem; color: #bbb;">Translation: "{translation}"</div>' if translation else ''}
        </div>

        <h2>Source Information</h2>
        <div class="meta">
            <p><strong>Original Text:</strong> <a href="/MagicalLatin/texts/{source_slug}/">{source_title}</a></p>
            <p><strong>Cited by Scholar:</strong> {scholar or 'Unknown'}</p>
            {f'<p><strong>Work:</strong> {work_title}</p>' if work_title else ''}
        </div>

        <h2>Scholarly Commentary</h2>
'''

        if commentaries:
            for comm_type, comm_text, comm_scholar, significance in commentaries:
                comm_type_label = {
                    'linguistic': 'Linguistic Analysis',
                    'magical': 'Magical Significance',
                    'historical': 'Historical Context',
                    'textual': 'Scholarly Interpretation',
                    'comparative': 'Comparative Analysis'
                }.get(comm_type, comm_type.title() if comm_type else 'General')

                quotation_content += f'''
        <div class="commentary">
            <div class="type">⌘ {comm_type_label}</div>
            <div>{comm_text}</div>
            {f'<div class="scholar">— {comm_scholar}</div>' if comm_scholar else ''}
        </div>
'''
        else:
            quotation_content += '<p>No commentary available yet.</p>\n'

        write_html(OUTPUT_DIR / 'quotations' / slug / 'index.html', quotation_content)

    print(f"  ✓ {len(quotations)} quotation pages")

def write_css():
    """Write CSS stylesheet."""
    with open(OUTPUT_DIR / 'portal.css', 'w', encoding='utf-8') as f:
        f.write(CSS_TEMPLATE)
    print(f"  ✓ portal.css")

def main():
    """Build the entire portal."""

    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found")
        return

    print(f"Building comprehensive MagicalLatin knowledge portal...")
    print(f"Output: {OUTPUT_DIR}\n")

    ensure_output_dir()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        print("Generating pages:")
        counts = build_index_page(conn)
        build_texts_index(conn)
        build_authors_index(conn)
        build_concepts_index(conn)
        build_quotations_index(conn)
        write_css()

        print(f"\n{'='*70}")
        print(f"✓ COMPREHENSIVE PORTAL BUILT SUCCESSFULLY!")
        print(f"\n  Summary:")
        print(f"    • Index page")
        print(f"    • {counts[0]} texts across {counts[2]} traditions")
        print(f"    • {counts[1]} author pages")
        print(f"    • {counts[3]} quotations with scholarly commentary")
        print(f"    • Enhanced CSS with quotation styling")
        print(f"\n  Ready for GitHub Pages deployment")
        print(f"{'='*70}")

    finally:
        conn.close()

if __name__ == '__main__':
    main()
