"""
update-spec-crosslinks.py
--------------------------
After the first `sync_and_push`, run this script to inject the actual Google Docs
URL back into the IFCX-Specification-v3.md cross-reference line.

Then re-run sync_and_push to push the updated spec (with live link) to both
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

SPEC_RELATIVE = r"05 Normative Specification\IFCX-Specification-v3.md"
SPEC_PATH     = WORK_DIR / "05 Normative Specification" / "IFCX-Specification-v3.md"

GITHUB_URL = ("https://github.com/Drshelden/IFCV5Work/blob/master/"
              "05%20Normative%20Specification/IFCX-Specification-v3.md")

def main():
    if not INDEX_FILE.exists():
        print("ERROR: drive_index.json not found — run sync_and_push first.")
        sys.exit(1)

    index = json.loads(INDEX_FILE.read_text(encoding="utf-8"))

    # Find the spec's Drive file ID (key uses backslash on Windows, forward slash on other OS)
    file_id = None
    for key, fid in index.items():
        if "IFCX-Specification-v3" in key and "05 Normative" in key:
            file_id = fid
            break

    if not file_id:
        print("ERROR: IFCX-Specification-v3 not found in drive_index.json.")
        print("       Make sure sync_to_gdrive.py ran successfully first.")
        sys.exit(1)

    gdocs_url = f"https://docs.google.com/document/d/{file_id}/edit"
    print(f"Found Google Docs file ID: {file_id}")
    print(f"Google Docs URL: {gdocs_url}")

    if not SPEC_PATH.exists():
        print(f"ERROR: Spec file not found at {SPEC_PATH}")
        sys.exit(1)

    content = SPEC_PATH.read_text(encoding="utf-8")

    # Replace the placeholder cross-reference with the live link
    old_xref_pat = (r'\*\*Cross-reference:\*\* \[GitHub\]\([^)]+\) · '
                    r'Google Docs \*\(link generated on first `sync_and_push`[^*]*\)\*')
    new_xref = (f'**Cross-reference:** [GitHub]({GITHUB_URL}) · '
                f'[Google Docs]({gdocs_url})')

    new_content, n = re.subn(old_xref_pat, new_xref, content)
    if n == 0:
        # Maybe it was already updated — check if current link matches
        if gdocs_url in content:
            print("Cross-reference already up to date.")
            return
        print("WARNING: Could not find cross-reference pattern to replace.")
        print("         Check IFCX-Specification-v3.md manually.")
        sys.exit(1)

    SPEC_PATH.write_text(new_content, encoding="utf-8")
    print(f"\n✓ Updated cross-reference in {SPEC_PATH.name}")
    print(f"\nNext step: run sync_and_push.bat to push the updated spec to GitHub and Google Drive.")


if __name__ == "__main__":
    main()
