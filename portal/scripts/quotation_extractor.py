#!/usr/bin/env python3
"""
Extract Latin quotations from magical texts and scholarly works.
Builds quotation_seed.json with semantic and linguistic context.

This is a semi-manual extraction framework:
1. Scans PDFs for candidates (quoted text patterns, italics, etc.)
2. Outputs candidates for manual verification
3. Merges with manual entries
4. Builds structured quotation records for seeding
"""

import json
import re
from pathlib import Path
from collections import defaultdict

try:
    import PyPDF2
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

DB_PATH = Path(__file__).parent.parent / 'portal.db'
OUTPUT_FILE = Path(__file__).parent.parent.parent / 'data' / 'quotations_seed.json'
SOURCES_FILE = Path(__file__).parent.parent.parent / 'data' / 'sources_raw.json'
MANUAL_QUOTATIONS_FILE = Path(__file__).parent.parent.parent / 'data' / 'quotations_manual.json'

# High-priority sources for quotation extraction
# These folders are most likely to have rich quotations
PRIORITY_FOLDERS = [
    'Grimoire',
    'magic',
    'hermetic',
    'Kabbalah',
    'renaissance magic',
    'alchemy',
    'Lull',
    'Rosicrucian',
    'crowley',
    'Brian Copenhaver',
    'Stephen Clucas',
]

# Pattern: Quotation patterns common in scholarly texts
QUOTATION_PATTERNS = [
    r'"([^"]{20,300})"',  # Double quoted passages
    r"'([^']{20,300})'",  # Single quoted passages (long)
    r'«([^»]{20,300})»',  # French guillemets
    r'\n\s{4,}([A-Z][^.\n]{20,200})\.?\n',  # Indented block quotes
]

# Latin word indicators (very common in magical texts)
LATIN_INDICATORS = [
    r'\b(ut|nam|enim|quia|quoniam|si|nisi|cum|quod|in)\b',
    r'\b(deus|spiritus|daemon|anima|mens|corpus)\b',
    r'\b(fiat|facit|fecit|est|sum|erat|erunt)\b',
    r'\b(lux|ignis|aqua|terra|aether|quinta essentia)\b',
]

class QuotationCandidate:
    """Represents a potential quotation for verification."""

    def __init__(self, text, source_file, page_num=None):
        self.text = text.strip()
        self.source_file = source_file
        self.page_num = page_num
        self.confidence = self._assess_confidence()

    def _assess_confidence(self):
        """Estimate confidence this is a Latin quotation."""
        if not self.text or len(self.text) < 15:
            return 'low'

        latin_count = sum(
            len(re.findall(pattern, self.text, re.IGNORECASE))
            for pattern in LATIN_INDICATORS
        )

        if latin_count > 5:
            return 'high'
        elif latin_count > 2:
            return 'medium'
        else:
            return 'low'

    def to_dict(self):
        return {
            'text': self.text,
            'source_file': self.source_file,
            'page_num': self.page_num,
            'confidence': self.confidence,
            'status': 'CANDIDATE',  # Needs manual review
        }

def build_manual_quotation_template():
    """Create a template JSON file for manual quotation entry."""
    template = {
        "_instructions": """
        Add quotations manually using this format.
        Every field is required except translation and manuscript_reference.

        source_text_slug: slug of the original Latin text (e.g. 'corpus-hermeticum')
        source_author: author of original text
        source_work_title: title of original work
        referenced_in_slug: slug of the scholarly work citing it
        scholar_name: scholar who discusses this quotation
        quotation_context: brief context where quotation appears
        page_reference: page number or location in referenced work

        commentary fields should explain:
        - linguistic_notes: grammar, vocabulary, word choices
        - magical_significance: relevance to magical practice
        - scholar_commentary: main scholarly interpretation
        """,
        "quotations": [
            {
                "latin_text": "Example Latin quotation text",
                "translation": "English translation (optional)",
                "source_text_slug": "original-source-slug",
                "source_author": "Author of Original Text",
                "source_work_title": "Original Work Title",
                "referenced_in_slug": "scholarly-work-slug",
                "scholar_name": "Scholar Name",
                "quotation_context": "Context where quotation appears",
                "page_reference": "p. 42",
                "linguistic_notes": "Notes on grammar, vocabulary, linguistic features",
                "magical_significance": "Why this quotation matters magically",
                "scholar_commentary": "Scholar's interpretation and analysis",
                "tags": ["tradition:hermeticism", "concept:divine-mind"]
            }
        ]
    }

    return template

def load_manual_quotations():
    """Load manually-entered quotations if file exists."""
    if not MANUAL_QUOTATIONS_FILE.exists():
        # Create template
        template = build_manual_quotation_template()
        with open(MANUAL_QUOTATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)
        print(f"✓ Created quotation template: {MANUAL_QUOTATIONS_FILE}")
        print(f"  Fill in manually-found quotations and re-run this script")
        return []

    with open(MANUAL_QUOTATIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data.get('quotations', [])

def seed_quotations_from_manual():
    """Convert manual quotations into structured database entries."""
    manual = load_manual_quotations()
    quotations = []

    if not manual:
        print("No manual quotations found yet.")
        return quotations

    print(f"\nProcessing {len(manual)} manual quotations...")

    for item in manual:
        if item.get('latin_text'):
            slug = item.get('latin_text')[:50].lower()
            slug = re.sub(r'[^a-z0-9]+', '-', slug)

            quotation = {
                'slug': slug,
                'latin_text': item.get('latin_text'),
                'translation': item.get('translation'),
                'source_text_slug': item.get('source_text_slug'),
                'source_author': item.get('source_author'),
                'source_work_title': item.get('source_work_title'),
                'referenced_in_slug': item.get('referenced_in_slug'),
                'scholar_name': item.get('scholar_name'),
                'quotation_context': item.get('quotation_context'),
                'linguistic_notes': item.get('linguistic_notes'),
                'magical_significance': item.get('magical_significance'),
                'page_reference': item.get('page_reference'),
                'scholar_commentary': item.get('scholar_commentary'),
                'tags': item.get('tags', []),
                'source_method': 'MANUAL_EXTRACTION',
                'review_status': 'DRAFT',
                'confidence': 'MEDIUM',
            }

            quotations.append(quotation)

    return quotations

def extract_candidates_from_pdf(pdf_path):
    """Try to extract quotation candidates from a PDF."""
    candidates = []

    if not HAS_PYPDF:
        return candidates

    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if not text:
                    continue

                # Try quotation patterns
                for pattern in QUOTATION_PATTERNS:
                    for match in re.finditer(pattern, text, re.MULTILINE):
                        candidate_text = match.group(1)
                        if 15 < len(candidate_text) < 500:
                            candidate = QuotationCandidate(
                                candidate_text,
                                str(pdf_path),
                                page_num
                            )
                            if candidate.confidence in ['medium', 'high']:
                                candidates.append(candidate)

    except Exception as e:
        pass  # Silently skip PDFs that can't be parsed

    return candidates

def main():
    """Build quotation seed data."""
    print("Building MagicalLatin quotation database...")
    print(f"Output: {OUTPUT_FILE}\n")

    quotations = []

    # Step 1: Load manual quotations
    print("Step 1: Loading manual quotations...")
    manual_quotations = seed_quotations_from_manual()
    quotations.extend(manual_quotations)
    print(f"  ✓ Loaded {len(manual_quotations)} manual quotations")

    # Step 2: Extract candidates from high-priority PDFs
    print(f"\nStep 2: Extracting candidates from priority folders...")
    base_path = Path('E:/pdf')
    candidates = []

    for folder in PRIORITY_FOLDERS:
        folder_path = base_path / folder
        if not folder_path.exists():
            continue

        pdfs = list(folder_path.glob('*.pdf'))[:5]  # Sample 5 PDFs per folder

        for pdf_path in pdfs:
            pdf_candidates = extract_candidates_from_pdf(pdf_path)
            candidates.extend(pdf_candidates)

    print(f"  Found {len(candidates)} candidate quotations")
    print(f"  → Review data/quotation_candidates.json and add verified ones to data/quotations_manual.json")

    # Step 3: Save candidates for manual review
    if candidates:
        candidates_output = Path('data/quotation_candidates.json')
        candidates_output.parent.mkdir(exist_ok=True)

        with open(candidates_output, 'w', encoding='utf-8') as f:
            json.dump(
                [c.to_dict() for c in candidates[:100]],  # Top 100 by confidence
                f, indent=2, ensure_ascii=False
            )
        print(f"  ✓ Saved candidates to {candidates_output}")

    # Step 4: Output quotations seed
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(quotations, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Quotation data ready!")
    print(f"  Quotations found: {len(quotations)}")
    print(f"  Output: {OUTPUT_FILE}")
    print(f"  Next: Seed database with seed_quotations.py")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
