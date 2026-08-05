"""
feedback_synthesize.py
----------------------
Groups collected source comments into structured themes using the Anthropic API.
Outputs a structured comment-summary.md in the batch directory.

Usage:
    python feedback_synthesize.py <batch.json>
"""

import argparse
import json
import os
import subprocess
import sys
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
        print(f"[synthesize] Installing {pkg}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--break-system-packages", "-q"],
            check=True,
        )

ensure_pkg("anthropic")


# ── Prompt ─────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are an expert technical secretary for the IFC5 standards committee.
Your task is to read raw feedback from multiple sources and identify distinct
recurring themes. For each theme output a structured block in this exact format:

## Theme N: [Short descriptive title]
**Type:** Bug | Clarification | New-Proposal | Disagreement | Evidence
**Severity:** Critical | Major | Minor
**Sources:** [comma-separated source ids]
**RFC impact:** RFC-NNN or "General" or "TBD"
**Summary:** 2-3 sentence description of the theme, what is contested or unclear, and why it matters.
**Action items:**
- ...

Do not add any other prose outside these blocks. Number themes starting at 1.
"""

def build_user_prompt(sources: list[dict]) -> str:
    parts = ["Below are the collected feedback sources. Identify all distinct themes.\n"]
    for src in sources:
        parts.append(f"--- SOURCE: {src['id']} (by {src.get('author','?')}, {src.get('date','?')}) ---")
        parts.append(src.get("raw_text", "")[:6000])  # cap per source to avoid token overflow
        parts.append("")
    return "\n".join(parts)


# ── Raw dump fallback ──────────────────────────────────────────────────────────

def raw_dump(sources: list[dict], batch_id: str) -> str:
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        f"# Comment Summary — Batch {batch_id}",
        f"**Sources:** {len(sources)}",
        f"**Generated:** {now}",
        "",
        "> ⚠️ WARNING: ANTHROPIC_API_KEY not set. Synthesis skipped. Raw source dump below.",
        "",
    ]
    for src in sources:
        lines += [
            f"## Source: {src['id']}",
            f"**Author:** {src.get('author','?')}  **Date:** {src.get('date','?')}",
            f"**URL:** {src.get('url','')}",
            "",
            src.get("raw_text", "")[:3000],
            "",
            "---",
            "",
        ]
    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Synthesize feedback themes via Anthropic API.")
    parser.add_argument("batch_json", help="Path to batch.json")
    args = parser.parse_args()

    batch_path = Path(args.batch_json).resolve()
    if not batch_path.exists():
        print(f"[synthesize] ERROR: batch.json not found: {batch_path}")
        sys.exit(1)

    cfg = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_dir = batch_path.parent
    batch_id = cfg["batch_id"]
    sources_dir = batch_dir / "sources"

    # Load all collected sources
    sources = []
    for src_cfg in cfg.get("sources", []):
        src_file = sources_dir / f"{src_cfg['id']}.json"
        if src_file.exists():
            sources.append(json.loads(src_file.read_text(encoding="utf-8")))
        else:
            print(f"[synthesize] WARNING: source file missing: {src_file.name} — skipping")

    if not sources:
        print("[synthesize] ERROR: No source files found. Run feedback_collect.py first.")
        sys.exit(1)

    print(f"[synthesize] Batch: {batch_id}  |  {len(sources)} source(s) loaded")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    out_path = batch_dir / "comment-summary.md"

    if not api_key:
        print("[synthesize] WARNING: ANTHROPIC_API_KEY not set — writing raw dump.")
        out_path.write_text(raw_dump(sources, batch_id), encoding="utf-8")
        print(f"[synthesize] Raw dump written → {out_path.relative_to(WORK_DIR)}")
        return

    import anthropic  # noqa: E402

    client = anthropic.Anthropic(api_key=api_key)
    user_prompt = build_user_prompt(sources)

    print(f"[synthesize] Calling {MODEL} ...")
    try:
        message = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        themes_text = message.content[0].text
    except Exception as exc:
        print(f"[synthesize] API call failed: {exc}")
        print("[synthesize] Falling back to raw dump.")
        out_path.write_text(raw_dump(sources, batch_id), encoding="utf-8")
        return

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    header = "\n".join([
        f"# Comment Summary — Batch {batch_id}",
        f"**Sources:** {len(sources)}",
        f"**Generated:** {now}",
        f"**Model:** {MODEL}",
        "",
        "---",
        "",
    ])

    out_path.write_text(header + themes_text, encoding="utf-8")
    print(f"[synthesize] Summary written → {out_path.relative_to(WORK_DIR)}")


if __name__ == "__main__":
    main()
