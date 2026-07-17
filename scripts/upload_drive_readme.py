"""
upload_drive_readme.py
----------------------
Creates or updates a README Google Doc at the root of the IFC5 Drive folder.
Content is defined inline as markdown, converted to .docx via Pandoc, and
uploaded as a Google Doc.

Usage:
    python upload_drive_readme.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR     = Path(__file__).resolve().parent
OAUTH_FILE     = SCRIPT_DIR / "oauth_client_secret.json"
TOKEN_FILE     = SCRIPT_DIR / "oauth_token.json"
INDEX_FILE     = SCRIPT_DIR / "drive_index.json"
ROOT_FOLDER_ID   = "1U9J-6hAr5pM_Q28JChDcistHsAHgi33y"
EXISTING_DOC_ID  = "1voB1u9RWjZ_u2XLjjl9GTpD_Z0SqyiJDHP5kYjd2dt4"  # existing Drive README
DOC_NAME         = "README"
INDEX_KEY        = "README.md"

SCOPES   = ["https://www.googleapis.com/auth/drive"]
GDOC_MIME = "application/vnd.google-apps.document"
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

README_CONTENT = """\
# IFC5 Architecture Initiative

**[📝 Google Drive version (this document)](https://docs.google.com/document/d/1voB1u9RWjZ_u2XLjjl9GTpD_Z0SqyiJDHP5kYjd2dt4/edit)** · [📄 GitHub version](https://github.com/Drshelden/IFCV5Work/blob/master/README.md)

This is the working home for the IFC5 Architecture Initiative — a structured effort to develop the architectural foundations of IFC5 through transparent, consensus-based decision-making. Everything lives in two mirrored locations: a [GitHub repository](https://github.com/Drshelden/IFCV5Work) and a [Google Drive folder](https://drive.google.com/drive/folders/1U9J-6hAr5pM_Q28JChDcistHsAHgi33y). Both are kept in sync. Use whichever you are most comfortable with.

---

## Quick Links

| Resource | GitHub | Google Drive |
|---|---|---|
| README (this document) | GitHub | Google Doc |
| Process Guide | GitHub MD | Google Doc |
| RFC Index | GitHub MD | Google Doc |
| Decision Register | CSV | — |
| RFC Priority Survey | — | Take the survey: https://forms.gle/vgu13dUKTpaqWEaE9 |
| All Discussions | View / Start new: https://github.com/Drshelden/IFCV5Work/discussions | — |
| Individual RFC Forms | Links in each RFC header | forms/ folder in this Drive |

Full URLs:
- README Google Doc: https://docs.google.com/document/d/1voB1u9RWjZ_u2XLjjl9GTpD_Z0SqyiJDHP5kYjd2dt4/edit
- README GitHub: https://github.com/Drshelden/IFCV5Work/blob/master/README.md
- Process Guide Google Doc: https://docs.google.com/document/d/1SA5Sg1RbKZT3z3vmYykf6P_DSly2pNG3ac9cET4RTCI/edit
- Process Guide GitHub: https://github.com/Drshelden/IFCV5Work/blob/master/00%20Architecture%20Overview/IFC5_Process_Guide.md
- RFC Index Google Doc: https://docs.google.com/document/d/1L4wD92OdDVGm5cvcPiAGYWQBF9pDHbHXni6ohOS5rKE/edit
- RFC Index GitHub: https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md
- Decision Register: https://github.com/Drshelden/IFCV5Work/blob/master/01%20Decision%20Register/IFC5_Decision_Register.csv
- GitHub repository root: https://github.com/Drshelden/IFCV5Work
- Google Drive folder root: https://drive.google.com/drive/folders/1U9J-6hAr5pM_Q28JChDcistHsAHgi33y

---

## Folder Structure

Both the GitHub repository and Google Drive folder share the same structure:

```
/
├── 00 Architecture Overview/    ← Process Guide, roadmap, meeting notes
├── 01 Decision Register/        ← Master spreadsheet: all 38 RFCs, status, tier, owner
├── 02 RFCs/                     ← One document per RFC  ← START HERE
├── 03 Reference Examples/       ← IFC-SPF / IFCX / ECS comparison examples
├── 04 Committee Feedback/       ← Comment logs and ballot responses
├── 05 Normative Specification/  ← Populated after decisions reach Accepted status
├── 06 Prototype Implementations/← Links to prototype repositories
└── forms/                       ← RFC feedback forms + Priority Survey (Drive only)
```

---

## The RFC Folder — Where the Work Happens

The 02 RFCs/ folder contains 38 structured documents, one per architectural decision. Each RFC covers:

- Problem Statement — what is ambiguous or missing in IFC5
- Background — relevant history and prior art
- IFC4.x Convention — how this is handled today
- Proposed Approaches — at least two alternatives
- Tradeoffs — comparison across expressiveness, compatibility, tooling complexity
- Recommendation — the author's current best thinking (not a committee decision)
- Open Questions — numbered questions reviewers should focus on

Every RFC exists in both places:

| | GitHub | Google Drive |
|---|---|---|
| Format | Markdown (.md) | Google Doc |
| Best for | Reading, version history, pull requests | Commenting, suggesting edits |
| Feedback | GitHub Discussions (tagged by RFC ID) | Google Docs comments + RFC form |

Each RFC's header and footer contains direct links to its counterpart, its discussion thread, and its individual feedback form.

---

## How to Give Feedback

### Fill out the RFC's Google Form

Every RFC has an individual feedback form linked in its header and footer. This is the most structured way to provide input — it captures your rating of each proposed approach, answers to the open questions, and general comments. Forms are linked from both the GitHub MD and the Google Doc version of each RFC.

### GitHub Discussions (GitHub side)

GitHub Discussions are the open-ended conversation space for each RFC.

- View all discussions: https://github.com/Drshelden/IFCV5Work/discussions
- Start a new discussion: https://github.com/Drshelden/IFCV5Work/discussions/new

Use the RFC's category (Tier 1-4) and add its label (e.g. IFC5-007) so it is indexed correctly. Each RFC's header/footer also has a pre-filled "New discussion" link that sets the category, label, and template automatically.

When writing a discussion, start your comment with a classification label (see below) so the RFC author can triage responses efficiently.

### Google Docs Comments (Google Drive side)

Open any RFC Google Doc from the 02 RFCs/ folder. To leave a comment:

1. Select the relevant text
2. Press Ctrl+Alt+M (Windows) or Cmd+Option+M (Mac), or click the comment icon in the toolbar
3. Begin your comment with a classification label (see below)

To suggest edits rather than just commenting, switch to Suggesting mode using the pencil icon in the top-right corner. Your changes appear as tracked edits that the RFC author can accept or reject — the original text is preserved. Start with comments before editing text directly.

### Comment Classification

In all feedback channels, begin each comment with one of these labels:

| Label | Use when |
|---|---|
| Editorial | Grammar or clarity — no technical impact |
| Technical Defect | Error of fact or logic in the RFC |
| Semantic Concern | The proposal may not mean what the author intends |
| Compatibility Concern | Conflicts with IFC4.x usage or existing tooling |
| Alternative Proposal | You have a different approach not covered in the RFC |
| Evidence | You have data, examples, prototypes, or prior art relevant to the decision |
| Blocking Objection | The RFC cannot be accepted as written — reserve for genuine blockers |
| General Support | You support the recommendation |

---

## What to Include in First-Round Feedback

The first round of review is deliberately open. In addition to comments on the existing content, first-round feedback may include:

- New questions — numbered additions to the Open Questions section (e.g. "Q5. Should...")
- New proposed approaches — alternatives not currently in the RFC
- Scope challenges — a proposal to remove this RFC, merge it with another, or split it into two
- Dependencies — identifying that this RFC cannot be resolved before another one is

There is no requirement to resolve these in the first round. The goal is to surface the full landscape of concerns before the RFC author revises.

---

## Review Sequence

The initiative will work through RFCs in roughly this sequence:

1. Priority Survey — committee rates all 38 RFCs to identify which to focus on first
2. Open Review — selected RFCs published for first-round feedback (forms, discussions, doc comments)
3. RFC Revision — author incorporates feedback, updates proposed approaches and open questions
4. Second Round — focused review of changes; unresolved objections documented
5. Prototype (if required) — working prototype built before consensus is reached
6. Committee Review — formal ballot
7. Decision recorded — outcome documented in RFC and Decision Register

---

## Take the Priority Survey

Before diving into individual RFCs, please fill out the RFC Priority Survey:
https://forms.gle/vgu13dUKTpaqWEaE9

Rate all 38 RFCs on a 1-3 scale (1 = top priority, max 3 selections). This directly determines which RFCs enter Open Review first.

---

## Guiding Principles

1. Decisions before specification. Write the architecture first; the spec follows from consensus.
2. One RFC per decision. Bundling makes consensus harder and traceability impossible.
3. Alternatives required. Every RFC must document at least two alternatives, including the IFC4.x convention.
4. Evidence over opinion. Arguments grounded in examples, prototypes, or prior art carry more weight.
5. Prototypes gate acceptance. RFCs marked with a prototype flag require a working prototype before advancing to Committee Review.
6. Structured feedback. Use the comment classification — it prevents important objections from getting buried.

---

IFC5 Architecture Initiative - July 2026
GitHub: https://github.com/Drshelden/IFCV5Work
Google Drive: https://drive.google.com/drive/folders/1U9J-6hAr5pM_Q28JChDcistHsAHgi33y
"""

def resolve_pandoc():
    for candidate in ("pandoc", "pandoc.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    for p in [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe",
        Path("C:/Program Files/Pandoc/pandoc.exe"),
    ]:
        if p.exists():
            return str(p)
    return None


def get_drive_service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception:
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def md_to_docx_bytes(md_text, pandoc_bin):
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
        f.write(md_text)
        md_path = f.name
    tmp_docx = md_path.replace(".md", ".docx")
    try:
        result = subprocess.run(
            [pandoc_bin, md_path, "-o", tmp_docx, "--from", "markdown", "--to", "docx"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Pandoc error: {result.stderr}")
        with open(tmp_docx, "rb") as f:
            return f.read()
    finally:
        for p in [md_path, tmp_docx]:
            if os.path.exists(p):
                os.unlink(p)


def main():
    pandoc = resolve_pandoc()
    if not pandoc:
        print("ERROR: pandoc not found.")
        sys.exit(1)

    print("Converting markdown to docx...")
    docx_bytes = md_to_docx_bytes(README_CONTENT, pandoc)

    print("Connecting to Drive...")
    svc = get_drive_service()
    from googleapiclient.http import MediaInMemoryUpload

    index = json.loads(INDEX_FILE.read_text(encoding="utf-8")) if INDEX_FILE.exists() else {}

    # Always update the known existing doc
    file_id = index.get(INDEX_KEY, EXISTING_DOC_ID)
    print(f"  Updating doc ({file_id})...")
    media = MediaInMemoryUpload(docx_bytes, mimetype=DOCX_MIME, resumable=False)
    svc.files().update(fileId=file_id, media_body=media, supportsAllDrives=True).execute()
    index[INDEX_KEY] = file_id
    INDEX_FILE.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"  [UPDATE] {DOC_NAME}")

    print(f"\n✓ Done.")
    print(f"  https://docs.google.com/document/d/{file_id}/edit")


if __name__ == "__main__":
    sys.exit(main())
