"""
update-spec-crosslinks.py
--------------------------
After the first `sync_and_push`, run this script to inject the actual Google Docs
URLs back into both spec files' cross-reference lines.

Then re-run sync_and_push to push the updated specs (with live links) to both
GitHub and Google Drive.

Usage:
    cd C:\_LOCAL\Claude\IFCV5
    python work\scripts\update-spec-crosslinks.py
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent
INDEX_FILE = SCRIPT_DIR / "drive_index.json"

SPECS = [
    {
        "relative": r"05 Normative Specification\ifcx-ifcy-specification-0.1.md",
        "filename": "ifcx-ifcy-specification-0.1.md",
        "github_url": f"{GH_BASE}/ifcx-ifcy-specification-0.1.md",
    },
    {
        "relative": r"05 Normative Specification\ifcx-specification-0.1.md",
        "filename": "ifcx-specification-0.1.md",
        "github_url": f"{GH_BASE}/ifcx-specification-0.1.md",
    },
]

def main():
    if not INDEX_FILE.exists():
        print("ERROR: drive_index.json not found — run sync_and_push first.")
        sys.exit(1)

    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))

    updated = 0
    for spec in SPECS:
        file_id = None
        for key, fid in index.items():
            if spec["filename"] in key:
                file_id = fid
                break

        if not file_id:
            print(f"SKIP: {spec[\'filename\']} not found in drive_index.json (not synced yet).")
            continue

        gdocs_url = f"https://docs.google.com/document/d/{file_id}/edit"
        spec_path = WORK_DIR / "05 Normative Specification" / spec["filename"]

        if not spec_path.exists():
            print(f"SKIP: {spec_path} not found.")
            continue

        content = spec_path.read_text(encoding="utf-8")

        old_pat = (r'\*\*Cross-reference:\*\* \[GitHub\]\([^)]+\) · '
                   r'Google Docs \*\(link generated on first `sync_and_push`[^*]*\)\*')
        new_xref = (f'**Cross-reference:** [GitHub]({spec["github_url"]}) · '
                    f'[Google Docs]({gdocs_url})')

        new_content, n = re.subn(old_pat, new_xref, content)
        if n == 0:
            if gdocs_url in content:
                print(f"  {spec[\'filename\']}: already up to date.")
            else:
                print(f"  WARNING: Could not update {spec[\'filename\']}.")
            continue

        spec_path.write_text(new_content, encoding="utf-8")
        print(f"  ✓ Updated cross-reference in {spec[\'filename\']}")
        print(f"    Google Docs: {gdocs_url}")
        updated += 1

    if updated:
        print(f"\nNext step: run sync_and_push.bat to push the updated specs to GitHub and Google Drive.")


if __name__ == "__main__":
    main()
