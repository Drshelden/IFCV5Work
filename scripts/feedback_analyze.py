"""
feedback_analyze.py
-------------------
Analyzes RFC impact. Reads RFC markdown files, matches themes to sections,
and generates proposed updates using the Anthropic API.

Usage:
    python feedback_analyze.py <batch.json>
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent

MODEL = "claude-haiku-4-5-20251001"

# ── Dependency bootstrap ───────────────────────────────────────────────────────
def ensure_pkg(pkg, import_as=None):
    try:
        __import__(import_as or pkg)
    except ImportError:
        print(f"[analyze] Installing {pkg}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--break-system-packages", "-q"],
            check=True,
        )

ensure_pkg("anthropic")


# ── Section parser ─────────────────────────────────────────────────────────────

def make_anchor(title: str) -> str:
    """Convert a heading title to a GitHub markdown anchor."""
    anchor = title.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)   # remove non-alphanumeric except hyphens/spaces
    anchor = re.sub(r'\s+', '-', anchor.strip())
    anchor = re.sub(r'-+', '-', anchor)
    return anchor


def parse_sections(md_text: str) -> list:
    """
    Parse markdown headings into a list of section dicts:
      {"level": 2, "title": "...", "anchor": "...", "content": "..."}
    """
    sections = []
    current = None
    content_lines = []

    for line in md_text.splitlines():
        m = re.match(r'^(#{1,6})\s+(.+)', line)
        if m:
            if current is not None:
                current["content"] = "\n".join(content_lines).strip()
                sections.append(current)
            level = len(m.group(1))
            title = m.group(2).strip()
            current = {"level": level, "title": title, "anchor": make_anchor(title), "content": ""}
            content_lines = []
        else:
            if current is not None:
                content_lines.append(line)

    if current is not None:
        current["content"] = "\n".join(content_lines).strip()
        sections.append(current)

    return sections


def github_link(repo: str, branch: str, filepath_in_repo: str, anchor: str) -> str:
    """Build a GitHub deep-link to a specific section of a file."""
    encoded = urllib.parse.quote(filepath_in_repo)
    return f"https://github.com/{repo}/blob/{branch}/{encoded}#{anchor}"


# ── RFC loader ─────────────────────────────────────────────────────────────────

def load_rfcs(rfc_dir: Path) -> list:
    """Load all RFC markdown files; return list of dicts with path, slug, sections."""
    rfcs = []
    pattern = re.compile(r'RFC-IFC5-\d+', re.IGNORECASE)
    for md_file in sorted(rfc_dir.glob("RFC-IFC5-*.md")):
        text = md_file.read_text(encoding="utf-8", errors="replace")
        sections = parse_sections(text)
        title = sections[0]["title"] if sections else md_file.stem
        slug = md_file.stem
        rfcs.append({
            "path": md_file,
            "slug": slug,
            "title": title,
            "sections": sections,
            "text": text,
        })
    return rfcs


# ── Theme loader ───────────────────────────────────────────────────────────────

def load_themes(batch_dir: Path) -> list:
    """Parse themes from comment-summary.md."""
    summary_path = batch_dir / "comment-summary.md"
    if not summary_path.exists():
        return []

    text = summary_path.read_text(encoding="utf-8")
    themes = []
    # Each theme block starts with "## Theme N: ..."
    blocks = re.split(r'\n(?=## Theme \d+)', text)
    for block in blocks:
        m = re.match(r'## Theme \d+: (.+)', block)
        if not m:
            continue
        theme = {"title": m.group(1).strip(), "raw": block}
        for field in ["Type", "Severity", "Sources", "RFC impact", "Summary"]:
            fm = re.search(rf'\*\*{re.escape(field)}:\*\*\s*(.+)', block)
            if fm:
                theme[field.lower().replace(" ", "_")] = fm.group(1).strip()
        themes.append(theme)
    return themes


# ── API-based impact mapping ───────────────────────────────────────────────────

IMPACT_SYSTEM = """\
You are a technical analyst for the IFC5 standards committee.
Given a list of feedback themes and RFC section summaries, produce:
1. An impact map table row for each (theme, RFC section) pair that is relevant.
   Format: | RFC slug | Section title | Change type | Theme title | GitHub link |
   Change types: "Modify content" | "Add to open questions" | "Add approach" | "Correct error"
2. For each affected RFC, a concise proposed change block:
   ## Change N: [Short title]
   **Section:** [section title]
   **Type:** [change type]
   **Rationale:** [1-2 sentences]
   **Proposed text:** [the actual proposed addition or modification]

Output ONLY the table rows (starting with |) and change blocks (starting with ## Change).
Separate the table section from the changes section with exactly: ---CHANGES---
"""

def call_api_for_impact(themes: list, rfcs: list, repo: str, branch: str) -> dict:
    """Use API to map themes to RFC sections; return {rfc_slug: [change_blocks]}."""
    import anthropic  # noqa: E402

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {}

    client = anthropic.Anthropic(api_key=api_key)

    # Build a compact representation of RFCs (first 3 sections only to fit context)
    rfc_summaries = []
    for rfc in rfcs:
        section_titles = [f"  - {s['title']}" for s in rfc["sections"][:10]]
        rfc_summaries.append(
            f"**{rfc['slug']}** — {rfc['title']}\n" + "\n".join(section_titles)
        )

    themes_text = "\n\n".join(
        f"Theme: {t['title']}\nType: {t.get('type','?')}\nSeverity: {t.get('severity','?')}\n"
        f"RFC impact: {t.get('rfc_impact','?')}\nSummary: {t.get('summary','?')}"
        for t in themes
    )

    user_msg = (
        "THEMES:\n\n" + themes_text +
        "\n\n---\n\nRFC SECTIONS:\n\n" + "\n\n".join(rfc_summaries)
    )

    print(f"[analyze] Calling {MODEL} for impact mapping ...")
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=IMPACT_SYSTEM,
            messages=[{"role": "user", "content": user_msg}],
        )
        raw = resp.content[0].text
    except Exception as exc:
        print(f"[analyze] API call failed: {exc}")
        return {}

    # Split on ---CHANGES---
    parts = raw.split("---CHANGES---", 1)
    table_rows = []
    changes_text = parts[1].strip() if len(parts) > 1 else ""

    for line in parts[0].splitlines():
        line = line.strip()
        if line.startswith("|") and not line.startswith("| RFC") and "---" not in line:
            table_rows.append(line)

    # Group changes by RFC slug
    changes_by_rfc: dict[str, list] = {}
    # Detect RFC slugs mentioned in change blocks
    for rfc in rfcs:
        slug = rfc["slug"]
        # Extract change blocks that mention this slug
        slug_pattern = re.compile(re.escape(slug), re.IGNORECASE)
        rfc_changes = []
        for block in re.split(r'\n(?=## Change \d+)', changes_text):
            if slug_pattern.search(block):
                rfc_changes.append(block.strip())
        if rfc_changes:
            changes_by_rfc[slug] = rfc_changes

    return {"table_rows": table_rows, "changes_by_rfc": changes_by_rfc}


# ── Proposed-update file writer ────────────────────────────────────────────────

def write_proposed_update(rfc: dict, changes: list, batch_id: str, updates_dir: Path):
    """Write a proposed-updates/<slug>.md file for one RFC."""
    slug = rfc["slug"]
    title = rfc["title"]

    lines = [
        f"# Proposed Updates: {title}",
        f"**Batch:** {batch_id}",
        "",
    ]
    for i, change in enumerate(changes, 1):
        # Ensure each block has a Change N header
        if not change.strip().startswith("## Change"):
            change = f"## Change {i}: Proposed update\n\n{change}"
        lines.append(change)
        lines.append("")

    out_path = updates_dir / f"{slug}.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ── Placeholder fallback ───────────────────────────────────────────────────────

def write_placeholder_update(rfc: dict, themes: list, batch_id: str, updates_dir: Path):
    """Write a placeholder proposed-updates file when no API key is available."""
    slug = rfc["slug"]
    lines = [
        f"# Proposed Updates: {rfc['title']}",
        f"**Batch:** {batch_id}",
        "",
        "> ⚠️ Manual review needed — ANTHROPIC_API_KEY not set, so automated analysis was skipped.",
        "",
        "## Relevant themes (to review manually)",
        "",
    ]
    for t in themes:
        rfc_impact = t.get("rfc_impact", "")
        # Check if this RFC slug appears in the theme's RFC impact field
        if rfc_impact and (slug.split("-")[2] in rfc_impact or "General" in rfc_impact or "TBD" in rfc_impact):
            lines += [
                f"### {t['title']}",
                f"**Type:** {t.get('type','?')}  **Severity:** {t.get('severity','?')}",
                f"**Summary:** {t.get('summary','')}",
                "",
            ]
    out_path = updates_dir / f"{slug}.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Analyze RFC impact and generate proposed updates.")
    parser.add_argument("batch_json", help="Path to batch.json")
    args = parser.parse_args()

    batch_path = Path(args.batch_json).resolve()
    if not batch_path.exists():
        print(f"[analyze] ERROR: batch.json not found: {batch_path}")
        sys.exit(1)

    cfg = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_dir = batch_path.parent
    batch_id = cfg["batch_id"]
    repo = cfg.get("repo_slug", "Drshelden/IFCV5Work")
    branch = cfg.get("repo_branch", "master")

    rfc_dir = WORK_DIR / cfg.get("rfc_dir", "02 RFCs")
    updates_dir = batch_dir / "proposed-updates"
    updates_dir.mkdir(parents=True, exist_ok=True)

    # Load RFCs and themes
    rfcs = load_rfcs(rfc_dir)
    themes = load_themes(batch_dir)
    print(f"[analyze] Batch: {batch_id}  |  {len(rfcs)} RFCs  |  {len(themes)} themes")

    if not rfcs:
        print("[analyze] WARNING: No RFC files found.")
        sys.exit(0)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    # ── Impact mapping ─────────────────────────────────────────────────────────
    table_rows = []
    changes_by_rfc: dict[str, list] = {}

    if api_key and themes:
        result = call_api_for_impact(themes, rfcs, repo, branch)
        table_rows = result.get("table_rows", [])
        changes_by_rfc = result.get("changes_by_rfc", {})
    elif not api_key:
        print("[analyze] WARNING: ANTHROPIC_API_KEY not set — producing placeholder outputs.")

    # ── Write proposed-update files ────────────────────────────────────────────
    update_links = []
    written_slugs = set()

    for rfc in rfcs:
        slug = rfc["slug"]
        if slug in changes_by_rfc and changes_by_rfc[slug]:
            out_path = write_proposed_update(rfc, changes_by_rfc[slug], batch_id, updates_dir)
            update_links.append((rfc["title"], out_path.name, len(changes_by_rfc[slug])))
            written_slugs.add(slug)
            print(f"[analyze]   Proposed updates → proposed-updates/{out_path.name}")
        elif not api_key and themes:
            # Write placeholder for RFCs referenced in themes
            referenced = any(
                slug.split("-")[2] in t.get("rfc_impact", "") or
                rfc["title"] in t.get("rfc_impact", "")
                for t in themes
            )
            if referenced:
                out_path = write_placeholder_update(rfc, themes, batch_id, updates_dir)
                update_links.append((rfc["title"], out_path.name, 0))
                written_slugs.add(slug)

    # ── Impact report ──────────────────────────────────────────────────────────
    lines = [
        f"# RFC Impact Report — Batch {batch_id}",
        f"**Generated:** {now}",
        "",
        "## Impact Map",
        "",
        "| Document | Section | Change Type | Theme | Link |",
        "|----------|---------|-------------|-------|------|",
    ]

    if table_rows:
        lines.extend(table_rows)
    else:
        # Build a minimal table from themes
        for t in themes:
            rfc_ref = t.get("rfc_impact", "TBD")
            lines.append(
                f"| {rfc_ref} | (see proposed-updates) | TBD | {t['title']} | — |"
            )

    lines += [
        "",
        "## Proposed Updates",
        "",
    ]

    for title, fname, n_changes in update_links:
        n_str = f"{n_changes} change(s)" if n_changes else "placeholder (manual review)"
        lines.append(f"- [{title} updates](proposed-updates/{fname}) — {n_str}")

    if not update_links:
        lines.append("*No proposed updates generated.*")

    report_path = batch_dir / "rfc-impact-report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[analyze] Impact report written → {report_path.relative_to(WORK_DIR)}")


if __name__ == "__main__":
    main()
