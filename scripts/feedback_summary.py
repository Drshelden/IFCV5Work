"""
feedback_summary.py
-------------------
Generates the final summary report for an IFC5 RFC feedback batch.
Assembles all prior stage outputs into a single document and copies it
to the repo directory.

Usage:
    python feedback_summary.py <batch.json>
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent
REPO_DIR   = WORK_DIR.parent / "repo"

GITHUB_REPO = "Drshelden/IFCV5Work"


# ── Git SHA ────────────────────────────────────────────────────────────────────

def get_git_sha(repo_dir: Path) -> tuple[str, str]:
    """Return (full_sha, sha7). Falls back gracefully if git unavailable."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            sha = result.stdout.strip()
            return sha, sha[:7]
    except Exception:
        pass
    return "unknown", "unknown"


# ── Source table ───────────────────────────────────────────────────────────────

def build_sources_table(cfg: dict, sources_dir: Path) -> str:
    rows = ["| # | Source | Author | Date | Type |", "|---|--------|--------|------|------|"]
    for i, src in enumerate(cfg.get("sources", []), 1):
        src_id = src["id"]
        src_file = sources_dir / f"{src_id}.json"
        if src_file.exists():
            data = json.loads(src_file.read_text(encoding="utf-8"))
            author = data.get("author", "?")
            date = data.get("date", "?")
            url = data.get("url", "")
            title = data.get("title", src_id)
            # For local files, use a relative link to the source file
            if src["type"] == "local_file" or not url:
                url = f"sources/{src_id}.json"
            link = f"[{title}]({url})"
        else:
            author = src.get("author", "?")
            date = src.get("date", "?")
            link = src_id + " *(not collected)*"
        rows.append(f"| {i} | {link} | {author} | {date} | {src['type']} |")
    return "\n".join(rows)


# ── Validation inline ──────────────────────────────────────────────────────────

def validation_inline(batch_dir: Path) -> str:
    report = batch_dir / "validation-report.md"
    if not report.exists():
        return "*Validation not run.*"
    text = report.read_text(encoding="utf-8")
    # Count pass/warn/fail
    passes = text.count("✅ PASS")
    warns = text.count("⚠️ WARN")
    fails = text.count("❌ FAIL")
    line = f"**{passes} PASS / {warns} WARN / {fails} FAIL**  →  [Full validation report](validation-report.md)"
    return line


# ── Themes inline ──────────────────────────────────────────────────────────────

def themes_inline(batch_dir: Path) -> str:
    summary = batch_dir / "comment-summary.md"
    if not summary.exists():
        return "*Comment synthesis not run.*"
    text = summary.read_text(encoding="utf-8")
    # Extract just the theme blocks
    # Strip header (everything before first ## Theme)
    idx = text.find("## Theme")
    if idx == -1:
        return text[text.find("---")+3:].strip() if "---" in text else text
    return text[idx:]


# ── Impact map inline ──────────────────────────────────────────────────────────

def impact_map_inline(batch_dir: Path) -> str:
    report = batch_dir / "rfc-impact-report.md"
    if not report.exists():
        return "*Impact analysis not run.*"
    text = report.read_text(encoding="utf-8")
    # Extract just the impact map table
    m = re.search(r'## Impact Map\n([\s\S]+?)(?=\n## |\Z)', text)
    if m:
        return m.group(1).strip()
    return text


# ── Proposed changes table ─────────────────────────────────────────────────────

def proposed_changes_table(batch_dir: Path) -> str:
    updates_dir = batch_dir / "proposed-updates"
    if not updates_dir.exists():
        return "*No proposed updates.*"
    files = sorted(updates_dir.glob("*.md"))
    if not files:
        return "*No proposed updates.*"
    rows = ["| Document | # Changes | Proposed Updates |", "|----------|-----------|-----------------|"]
    for f in files:
        # Skip placeholder files (< 300 bytes = auto-generated empty stubs)
        if f.stat().st_size < 300:
            continue
        text = f.read_text(encoding="utf-8")
        n = len(re.findall(r'^## Change \d+', text, re.MULTILINE))
        # Use a clean display name: strip trailing -updates suffix if present
        slug = f.stem.replace("-updates", "")
        if n > 0:
            rows.append(f"| {slug} | {n} | [View](proposed-updates/{f.name}) |")
    if len(rows) == 2:
        return "*No proposed updates.*"
    return "\n".join(rows)


# ── Action items ───────────────────────────────────────────────────────────────

def extract_action_items(batch_dir: Path) -> str:
    """Extract the summary of actions table from comment-summary.md."""
    summary = batch_dir / "comment-summary.md"
    if not summary.exists():
        return "1. Review collected feedback\n2. Run feedback cycle scripts\n3. Schedule next review"
    text = summary.read_text(encoding="utf-8")
    # Look for the "Summary of actions" markdown table
    table_match = re.search(
        r'(\| #.*?\n(?:\|[-| ]+\|\n)(?:\|.*\n)+)',
        text, re.DOTALL
    )
    if table_match:
        return table_match.group(1).strip()
    # Fallback: extract numbered list items
    items = []
    in_next_steps = False
    for line in text.splitlines():
        if "next steps" in line.lower() or "actions" in line.lower():
            in_next_steps = True
        if in_next_steps and re.match(r'\d+\.', line.strip()) and len(line.strip()) > 15:
            items.append(f"- {line.strip()}")
    if not items:
        items = ["- Review themes and approve proposed changes", "- Schedule next committee meeting"]
    return "\n".join(items[:15])


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate final IFC5 RFC feedback summary.")
    parser.add_argument("batch_json", help="Path to batch.json")
    args = parser.parse_args()

    batch_path = Path(args.batch_json).resolve()
    if not batch_path.exists():
        print(f"[summary] ERROR: batch.json not found: {batch_path}")
        sys.exit(1)

    cfg = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_dir = batch_path.parent
    batch_id = cfg["batch_id"]
    sources_dir = batch_dir / "sources"

    now = datetime.now(timezone.utc)
    now_str = now.strftime("%Y-%m-%d %H:%M UTC")
    next_cycle = (now + timedelta(days=14)).strftime("%Y-%m-%d")

    sha, sha7 = get_git_sha(REPO_DIR)
    repo_link = f"[{GITHUB_REPO} @ {sha7}](https://github.com/{GITHUB_REPO}/tree/{sha})"

    print(f"[summary] Batch: {batch_id}  |  Repo SHA: {sha7}")

    # Build report sections
    sources_table  = build_sources_table(cfg, sources_dir)
    validation_str = validation_inline(batch_dir)
    themes_str     = themes_inline(batch_dir)
    impact_str     = impact_map_inline(batch_dir)
    changes_table  = proposed_changes_table(batch_dir)
    action_items   = extract_action_items(batch_dir)

    report = f"""\
# IFC5 RFC Update Summary — {batch_id}
**Generated:** {now_str}
**Repository:** {repo_link}
**Next review cycle:** {next_cycle}
**Batch directory:** `04 Committee Feedback/{batch_id}/`

---

## 1. Sources Reviewed

{sources_table}

---

## 2. Validation Results

{validation_str}

---

## 3. Comment Themes

{themes_str}

---

## 4. RFC Impact Map

{impact_str}

---

## 5. Proposed Document Changes

{changes_table}

---

## 6. Open Action Items

{action_items}

---

## 7. Next Steps

- Review and approve proposed changes above
- Update Decision Register with any resolved items
- Next feedback cycle: {next_cycle}
- Run reference examples against schema before next committee meeting
"""

    out_filename = f"IFC5-RFC-Update-Summary-{batch_id}.md"
    out_path = batch_dir / out_filename
    out_path.write_text(report, encoding="utf-8")
    print(f"[summary] Summary written → {out_path.relative_to(WORK_DIR)}")

    # Copy to repo
    repo_feedback_dir = REPO_DIR / "04 Committee Feedback" / batch_id
    repo_feedback_dir.mkdir(parents=True, exist_ok=True)
    repo_out = repo_feedback_dir / out_filename
    shutil.copy2(str(out_path), str(repo_out))
    print(f"[summary] Copied to repo → {repo_out.relative_to(REPO_DIR.parent)}")


if __name__ == "__main__":
    main()
