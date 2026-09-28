#!/usr/bin/env python3
"""
Initialize MagicalLatin knowledge portal database.
Creates SQLite schema following framework_knowledge_portal pattern.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'portal.db'

def init_db():
    """Create database schema with all tables."""

    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    c = conn.cursor()

    # Schema version for migrations
    c.execute('''
        CREATE TABLE IF NOT EXISTS schema_version (
            id INTEGER PRIMARY KEY,
            version INTEGER NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Core entity tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS figures (
            id INTEGER PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            birth_year INTEGER,
            death_year INTEGER,
            era TEXT,
            tradition TEXT,
            summary TEXT NOT NULL,
            full_description TEXT,
            biography_notes TEXT,
            tags TEXT,
            source_method TEXT DEFAULT 'SEED_DATA',
            review_status TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
            confidence TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            authors TEXT,
            publication_year INTEGER,
            original_language TEXT DEFAULT 'Latin',
            tradition TEXT,
            text_type TEXT CHECK(text_type IN ('primary','secondary','commentary','translation')),
            folder TEXT,
            pdf_path TEXT,
            summary TEXT NOT NULL,
            full_description TEXT,
            key_concepts TEXT,
            tags TEXT,
            source_method TEXT DEFAULT 'SEED_DATA',
            review_status TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
            confidence TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS concepts (
            id INTEGER PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            tradition TEXT,
            concept_type TEXT CHECK(concept_type IN ('doctrine','practice','term','ritual','entity')),
            summary TEXT NOT NULL,
            full_description TEXT,
            etymology TEXT,
            related_concepts TEXT,
            tags TEXT,
            source_method TEXT DEFAULT 'SEED_DATA',
            review_status TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
            confidence TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS bibliography (
            id INTEGER PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            author TEXT,
            title TEXT NOT NULL,
            year INTEGER,
            place TEXT,
            publisher TEXT,
            edition TEXT,
            url TEXT,
            doi TEXT,
            summary TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS scholarly_refs (
            id INTEGER PRIMARY KEY,
            entity_type TEXT NOT NULL CHECK(entity_type IN ('figure','text','concept')),
            entity_slug TEXT NOT NULL,
            bibliography_slug TEXT NOT NULL,
            page_or_locus TEXT,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(bibliography_slug) REFERENCES bibliography(slug)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS essays (
            id INTEGER PRIMARY KEY,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            subject_area TEXT,
            body TEXT NOT NULL,
            related_entities TEXT,
            tags TEXT,
            source_method TEXT DEFAULT 'SEED_DATA',
            review_status TEXT DEFAULT 'DRAFT',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Relationships between entities
    c.execute('''
        CREATE TABLE IF NOT EXISTS text_authors (
            id INTEGER PRIMARY KEY,
            text_slug TEXT NOT NULL,
            figure_slug TEXT NOT NULL,
            role TEXT DEFAULT 'author',
            FOREIGN KEY(text_slug) REFERENCES texts(slug),
            FOREIGN KEY(figure_slug) REFERENCES figures(slug)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS text_concepts (
            id INTEGER PRIMARY KEY,
            text_slug TEXT NOT NULL,
            concept_slug TEXT NOT NULL,
            relevance TEXT DEFAULT 'primary',
            FOREIGN KEY(text_slug) REFERENCES texts(slug),
            FOREIGN KEY(concept_slug) REFERENCES concepts(slug)
        )
    ''')

    # Create indexes
    c.execute('CREATE INDEX IF NOT EXISTS idx_figures_tradition ON figures(tradition)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_texts_tradition ON texts(tradition)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_texts_year ON texts(publication_year)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_concepts_tradition ON concepts(tradition)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_scholarly_entity ON scholarly_refs(entity_type, entity_slug)')

    # Record schema version
    c.execute('INSERT OR REPLACE INTO schema_version (id, version) VALUES (1, 1)')

    conn.commit()
    conn.close()

    print(f"✓ Database initialized: {DB_PATH}")
    print(f"  Tables created: figures, texts, concepts, bibliography, essays, etc.")
    print(f"  Indexes created for efficient querying")

if __name__ == '__main__':
    init_db()
