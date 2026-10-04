#!/usr/bin/env python3
"""
Merge new quotations from agent/extraction into quotations_seed.json

Usage:
    python merge_quotations.py --source data/quotations_phase2_batch1.json --target data/quotations_seed.json
"""

import json
import argparse
import sys
from pathlib import Path


def load_json(path):
    """Load JSON file with UTF-8 encoding"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, path):
    """Save JSON file with UTF-8 encoding"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved {len(data)} quotations to {path}")


def merge_quotations(source_path, target_path):
    """
    Merge source quotations into target, avoiding duplicates by slug.

    Args:
        source_path: Path to new quotations (from agent/extraction)
        target_path: Path to existing quotations_seed.json

    Returns:
        Merged list of quotations
    """

    # Load both files
    print(f"Loading source: {source_path}")
    new_quots = load_json(source_path)
    print(f"  Found {len(new_quots)} new quotations")

    print(f"Loading target: {target_path}")
    existing_quots = load_json(target_path)
    print(f"  Found {len(existing_quots)} existing quotations")

    # Build slug map for existing
    existing_slugs = {q.get('slug'): q for q in existing_quots}

    # Merge, preferring new over old (in case of re-enrichment)
    merged = list(existing_quots)
    added = 0
    updated = 0

    for new_q in new_quots:
        slug = new_q.get('slug')
        if slug in existing_slugs:
            # Update existing
            idx = next(i for i, q in enumerate(merged) if q.get('slug') == slug)
            merged[idx] = new_q
            updated += 1
            print(f"  ↻ Updated: {slug}")
        else:
            # Add new
            merged.append(new_q)
            added += 1
            print(f"  + Added: {slug}")

    print(f"\nMerge summary:")
    print(f"  Added: {added}")
    print(f"  Updated: {updated}")
    print(f"  Total: {len(merged)}")

    # Validate all quotations have required fields
    required_fields = [
        'slug', 'latin_text', 'translation',
        'source_author', 'source_work_title', 'source_text_slug', 'referenced_in_slug',
        'scholar_name', 'quotation_context', 'page_reference',
        'linguistic_notes', 'magical_significance', 'scholar_commentary',
        'tags', 'source_method', 'review_status', 'confidence'
    ]

    invalid = []
    for q in merged:
        missing = [f for f in required_fields if f not in q or not q[f]]
        if missing:
            invalid.append((q.get('slug', 'UNKNOWN'), missing))

    if invalid:
        print(f"\n⚠ Validation warnings:")
        for slug, missing in invalid:
            print(f"  {slug}: missing {missing}")
    else:
        print(f"\n✓ All quotations valid (all required fields present)")

    return merged


def main():
    parser = argparse.ArgumentParser(description='Merge quotations into seed file')
    parser.add_argument('--source', required=True, help='Source quotations file (new/enriched)')
    parser.add_argument('--target', required=True, help='Target quotations_seed.json')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be merged without writing')

    args = parser.parse_args()

    source_path = Path(args.source)
    target_path = Path(args.target)

    if not source_path.exists():
        print(f"ERROR: Source file not found: {source_path}")
        sys.exit(1)

    if not target_path.exists():
        print(f"ERROR: Target file not found: {target_path}")
        sys.exit(1)

    # Merge
    merged = merge_quotations(source_path, target_path)

    if not args.dry_run:
        # Save merged result
        save_json(merged, target_path)
        print(f"\n✓ Merge complete. Run:")
        print(f"  python portal/scripts/seed_quotations.py")
        print(f"  python portal/scripts/build_site_final.py")
        print(f"  git add data/quotations_seed.json docs/")
        print(f"  git commit -m 'Phase 2 Batch: Add verified quotations'")
    else:
        print(f"\n[DRY RUN] No changes written. Remove --dry-run to save.")


if __name__ == '__main__':
    main()
