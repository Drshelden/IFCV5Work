"""
fix_category_slugs.py
---------------------
Replaces incorrect category slugs in all RFC .md files and the RFC index.

Old slugs (guessed):          Correct slugs (from GraphQL):
  tier-1-foundational    →      -tier-1-foundational
  tier-2-core-architecture →    -tier-2-core-architecture
  tier-3-domain-modeling →      -tier-3-domain-modeling
  tier-4-governance      →      -tier-4-governance

Usage:
    python fix_category_slugs.py [--dry-run]
"""

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent
RFC_DIR    = WORK_DIR / "02 RFCs"

SLUG_FIXES = {
    "?category=tier-1-foundational":      "?category=-tier-1-foundational",
    "?category=tier-2-core-architecture": "?category=-tier-2-core-architecture",
    "?category=tier-3-domain-modeling":   "?category=-tier-3-domain-modeling",
    "?category=tier-4-governance":        "?category=-tier-4-governance",
}

def fix_file(path: Path, dry_run: bool) -> str:
    content = path.read_text(encoding="utf-8")
    new_content = content
    for old, new in SLUG_FIXES.items():
        new_content = new_content.replace(old, new)
    if new_content == content:
        return "SKIP"
    if not dry_run:
        path.write_text(new_content, encoding="utf-8")
    return "PATCH"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN ===\n")

    targets = list(RFC_DIR.glob("*.md"))
    for path in sorted(targets):
        result = fix_file(path, dry_run=args.dry_run)
        print(f"  [{result}] {path.name}")

    print("\n✓ Done.")

if __name__ == "__main__":
    sys.exit(main())
