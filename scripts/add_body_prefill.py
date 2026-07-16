"""
add_body_prefill.py
-------------------
Adds a &body= parameter to all "Start a new discussion" URLs in RFC files
and the index, so the form opens with a structured markdown template.

Safe to re-run — replaces existing &body= if present.
"""

import sys
import urllib.parse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent
RFC_DIR    = WORK_DIR / "02 RFCs"

BODY_TEMPLATE = """\
**Comment type:** Editorial | Technical Defect | Semantic Concern | Compatibility Concern | Alternative Proposal | Evidence | Blocking Objection | General Support

*(delete all but one)*

---

**Feedback:**

<!-- Be specific — reference section numbers or quote RFC text where relevant -->

---

**Supporting evidence or examples:**

<!-- Optional: links, code, schema examples, prior art -->

---

**Questions for the working group:**

<!-- Optional: number each question Q1, Q2, ... -->
"""

ENCODED_BODY = urllib.parse.quote(BODY_TEMPLATE, safe="")

def fix_url(url: str) -> str:
    # Strip any existing &body= parameter
    if "&body=" in url:
        url = url[:url.index("&body=")]
    return url + "&body=" + ENCODED_BODY

def fix_file(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    if "/discussions/new?" not in content:
        return "SKIP"

    lines = content.split("\n")
    new_lines = []
    changed = False
    for line in lines:
        if "/discussions/new?" in line:
            # Find and fix each URL in the line
            import re
            def replacer(m):
                return fix_url(m.group(0))
            new_line = re.sub(
                r'https://github\.com/[^)"\s]+/discussions/new\?[^)"\s]+',
                replacer,
                line
            )
            if new_line != line:
                changed = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if not changed:
        return "SKIP"

    path.write_text("\n".join(new_lines), encoding="utf-8")
    return "PATCH"


def main():
    targets = sorted(RFC_DIR.glob("*.md"))
    for path in targets:
        result = fix_file(path)
        print(f"  [{result}] {path.name}")
    print("\n✓ Done.")

if __name__ == "__main__":
    sys.exit(main())
