#!/usr/bin/env python3
"""
Build static HTML site for MagicalLatin knowledge portal with quotations.
Extended version that includes quotation cards, detail pages, and search.
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

# Enhanced CSS with quotation-specific styles
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
    flex-wrap: wrap;
    gap: 2rem;
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
    gap: 1.5rem;
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
    background: rgba(201, 169, 97, 0.03);
}

.quotation-card .latin-text {
    font-style: italic;
    color: var(--color-latin);
    font-size: 0.95rem;
    margin: 1rem 0;
    line-height: 1.8;
    padding: 0.5rem 0 0.5rem 1rem;
    border-left: 2px solid var(--color-latin);
}

.quotation-card .translation {
    color: #aaa;
    font-size: 0.9rem;
    margin: 0.5rem 0;
    font-style: italic;
}

.quotation-card .meta {
    display: flex;
    gap: 1rem;
    font-size: 0.85rem;
    color: #888;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.quotation-card .meta span {
    display: flex;
    gap: 0.5rem;
}

.meta {
    font-size: 0.9rem;
    color: #aaa;
    margin-top: 1rem;
}

.commentary {
    background: var(--color-commentary);
    padding: 1rem;
    margin: 1rem 0;
    border-left: 2px solid var(--color-gold);
    font-size: 0.95rem;
    line-height: 1.7;
}

.commentary .type {
    color: var(--color-gold);
    font-weight: bold;
    font-size: 0.85rem;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.commentary .scholar {
    color: var(--color-latin);
    font-style: italic;
    margin-top: 0.5rem;
    font-size: 0.85rem;
}

.tabs {
    display: flex;
    gap: 1rem;
    margin: 2rem 0;
    border-bottom: 1px solid var(--color-border);
    flex-wrap: wrap;
}

.tabs button {
    background: none;
    border: none;
    color: #888;
    cursor: pointer;
    padding: 1rem;
    border-bottom: 2px solid transparent;
    transition: all 0.3s;
}

.tabs button.active {
    color: var(--color-gold);
    border-bottom-color: var(--color-gold);
}

.tabs button:hover {
    color: var(--color-gold);
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

def build_quotations_index(conn):
    """Build quotations listing page with card grid."""
    c = conn.cursor()

    c.execute('''
        SELECT q.slug, q.latin_text, q.translation, q.scholar_name, q.source_work_title, q.source_text_slug
        FROM quotations q
        ORDER BY q.scholar_name, q.source_text_slug
    ''')
    quotations = c.fetchall()

    content = '<h1>Latin Quotations from Magical Texts</h1>\n'
    content += '<p>A collection of significant Latin passages from magical texts, cited and analyzed by scholars.</p>\n'
    content += f'<p class="meta">Total: {len(quotations)} quotations</p>\n'

    if quotations:
        content += '<div class="grid">\n'

        for slug, latin_text, translation, scholar, work_title, source_slug in quotations:
            latin_short = latin_text[:80] + '...' if len(latin_text) > 80 else latin_text

            content += f'''
    <div class="card quotation-card">
        <div class="latin-text">{latin_short}</div>
        {f'<div class="translation">"{translation[:100]}..."</div>' if translation else ''}
        <div class="meta">
            <span><strong>Scholar:</strong> {scholar or 'Unknown'}</span>
            <span><strong>Source:</strong> {work_title or source_slug}</span>
        </div>
        <p style="margin-top: 1rem;"><a href="/MagicalLatin/quotations/{slug}/">View Full Quotation</a></p>
    </div>
'''

        content += '</div>\n'
    else:
        content += '<p>No quotations yet. Create data/quotations_seed.json to add them.</p>\n'

    write_html(OUTPUT_DIR / 'quotations' / 'index.html', content)
    print(f"  ✓ quotations/index.html")

    # Build individual quotation pages
    for slug, latin_text, translation, scholar, work_title, source_slug in quotations:
        # Get commentary
        c.execute('''
            SELECT commentary_type, commentary_text, scholar_name, significance_level
            FROM quotation_commentary
            WHERE quotation_id = (SELECT id FROM quotations WHERE slug = ?)
            ORDER BY commentary_type
        ''', (slug,))
        commentaries = c.fetchall()

        # Get source text info
        c.execute('''
            SELECT title, authors, publication_year FROM texts WHERE slug = ?
        ''', (source_slug,))
        source_row = c.fetchone()
        source_title = source_row[0] if source_row else 'Unknown Source'

        quotation_content = f'''
        <h1>Quotation</h1>

        <div class="quotation-card">
            <div class="latin-text">{latin_text}</div>
            {f'<div class="translation">Translation: "{translation}"</div>' if translation else ''}
        </div>

        <h2>Source Information</h2>
        <div class="meta">
            <p><strong>Original Text:</strong> <a href="/MagicalLatin/texts/{source_slug}/">{source_title}</a></p>
            <p><strong>Cited by:</strong> {scholar or 'Unknown Scholar'}</p>
            {f'<p><strong>Work:</strong> {work_title}</p>' if work_title else ''}
        </div>

        <h2>Scholarly Commentary</h2>
'''

        if commentaries:
            for comm_type, comm_text, comm_scholar, significance in commentaries:
                comm_type_label = comm_type.title() if comm_type else 'General'
                quotation_content += f'''
        <div class="commentary">
            <div class="type">{comm_type_label}</div>
            <div>{comm_text}</div>
            {f'<div class="scholar">— {comm_scholar}</div>' if comm_scholar else ''}
        </div>
'''
        else:
            quotation_content += '<p>No commentary available yet.</p>\n'

        write_html(OUTPUT_DIR / 'quotations' / slug / 'index.html', quotation_content)

    print(f"  ✓ {len(quotations)} quotation pages")
    return len(quotations)

def build_source_detail_pages(conn):
    """Build detail pages for sources with all their quotations."""
    c = conn.cursor()

    c.execute('''
        SELECT DISTINCT source_text_slug FROM quotations
    ''')
    source_slugs = [row[0] for row in c.fetchall() if row[0]]

    count = 0
    for source_slug in source_slugs:
        # Get source info
        c.execute('SELECT title, authors FROM texts WHERE slug = ?', (source_slug,))
        source_row = c.fetchone()
        if not source_row:
            continue

        source_title = source_row[0]
        source_authors = source_row[1]

        # Get all quotations from this source
        c.execute('''
            SELECT slug, latin_text, translation, scholar_name
            FROM quotations
            WHERE source_text_slug = ?
            ORDER BY scholar_name
        ''', (source_slug,))
        quotations = c.fetchall()

        content = f'<h1>{source_title}</h1>\n'
        if source_authors:
            content += f'<p class="meta"><strong>Author:</strong> {source_authors}</p>\n'

        content += f'<p>This source contains {len(quotations)} quoted passages in the scholarly literature.</p>\n'

        if quotations:
            content += '<h2>Quotations</h2>\n'
            content += '<div class="grid">\n'

            for q_slug, latin_text, translation, scholar in quotations:
                latin_short = latin_text[:80] + '...' if len(latin_text) > 80 else latin_text
                content += f'''
    <div class="card quotation-card">
        <div class="latin-text">{latin_short}</div>
        {f'<div class="translation">"{translation[:80]}..."</div>' if translation else ''}
        <div class="meta">
            <span><strong>Scholar:</strong> {scholar or 'Unknown'}</span>
        </div>
        <p style="margin-top: 1rem;"><a href="/MagicalLatin/quotations/{q_slug}/">View Full</a></p>
    </div>
'''

            content += '</div>\n'

        write_html(OUTPUT_DIR / 'sources' / source_slug / 'index.html', content)
        count += 1

    print(f"  ✓ {count} source detail pages")
    return count

def write_css():
    """Write enhanced CSS stylesheet."""
    with open(OUTPUT_DIR / 'portal.css', 'w', encoding='utf-8') as f:
        f.write(CSS_TEMPLATE)
    print(f"  ✓ portal.css (enhanced with quotation styles)")

def main():
    """Build the portal with quotations."""

    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found")
        return

    print(f"Building MagicalLatin portal with quotations...")
    print(f"Output directory: {OUTPUT_DIR}\n")

    ensure_output_dir()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        print("Generating quotation pages:")
        q_count = build_quotations_index(conn)
        s_count = build_source_detail_pages(conn)
        write_css()

        print(f"\n{'='*60}")
        print(f"✓ Portal with quotations built successfully!")
        print(f"  Quotations: {q_count}")
        print(f"  Source detail pages: {s_count}")
        print(f"  Output: {OUTPUT_DIR}")
        print(f"{'='*60}")

    finally:
        conn.close()

if __name__ == '__main__':
    main()
