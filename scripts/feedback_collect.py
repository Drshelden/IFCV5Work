"""
feedback_collect.py
-------------------
Collects raw comments from sources listed in a batch config JSON.
Outputs one normalized JSON file per source to <batch_dir>/sources/.

Usage:
    python feedback_collect.py <batch.json> [--github-token TOKEN]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent

# ── Dependency bootstrap ───────────────────────────────────────────────────────
def ensure_pkg(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"[collect] Installing {pkg}...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg, "--break-system-packages", "-q"],
            check=True,
        )

ensure_pkg("requests")
ensure_pkg("docx")   # python-docx imports as 'docx'

import requests  # noqa: E402


# ── GitHub helpers ─────────────────────────────────────────────────────────────

def github_headers(token: str | None) -> dict:
    hdrs = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    else:
        print("[collect] WARNING: No GITHUB_TOKEN set — unauthenticated requests (rate-limited to 60/hr).")
    return hdrs


def fetch_github_issue(repo: str, number: int, token: str | None) -> dict:
    """Fetch issue body + all comments; return normalized dict."""
    hdrs = github_headers(token)
    base_url = f"https://api.github.com/repos/{repo}/issues/{number}"

    resp = requests.get(base_url, headers=hdrs, timeout=30)
    resp.raise_for_status()
    issue = resp.json()

    # Collect all comment pages
    comments = []
    comments_url = f"{base_url}/comments"
    while comments_url:
        cr = requests.get(comments_url, headers=hdrs, params={"per_page": 100}, timeout=30)
        cr.raise_for_status()
        comments.extend(cr.json())
        comments_url = cr.links.get("next", {}).get("url")

    # Build participant list (unique, ordered)
    participants = [issue["user"]["login"]]
    for c in comments:
        login = c["user"]["login"]
        if login not in participants:
            participants.append(login)

    # Concatenate body + comments
    parts = [f"# {issue['title']}\n\n{issue.get('body') or ''}"]
    for c in comments:
        ts = c["created_at"][:10]
        parts.append(f"\n---\n**{c['user']['login']}** ({ts}):\n\n{c.get('body') or ''}")
    raw_text = "\n".join(parts)

    return {
        "id": f"github-issue-{number}",
        "source_type": "github_issue",
        "url": issue["html_url"],
        "title": issue["title"],
        "author": issue["user"]["login"],
        "date": issue["created_at"][:10],
        "participants": participants,
        "raw_text": raw_text,
    }


GRAPHQL_DISCUSSION_QUERY = """
query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    discussion(number: $number) {
      title
      url
      createdAt
      author { login }
      body
      comments(first: 100) {
        nodes {
          author { login }
          createdAt
          body
          replies(first: 50) {
            nodes {
              author { login }
              createdAt
              body
            }
          }
        }
      }
    }
  }
}
"""


def fetch_github_discussion(repo: str, number: int, token: str | None) -> dict:
    """Fetch discussion body + comments via GraphQL; return normalized dict."""
    hdrs = github_headers(token)
    hdrs["Content-Type"] = "application/json"

    owner, name = repo.split("/", 1)
    payload = {
        "query": GRAPHQL_DISCUSSION_QUERY,
        "variables": {"owner": owner, "name": name, "number": number},
    }
    resp = requests.post(
        "https://api.github.com/graphql",
        headers=hdrs,
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")

    disc = data["data"]["repository"]["discussion"]

    participants = []
    def add_participant(login):
        if login and login not in participants:
            participants.append(login)

    add_participant(disc["author"]["login"] if disc.get("author") else None)

    parts = [f"# {disc['title']}\n\n{disc.get('body') or ''}"]
    for c in disc["comments"]["nodes"]:
        login = c["author"]["login"] if c.get("author") else "unknown"
        add_participant(login)
        ts = c["createdAt"][:10]
        parts.append(f"\n---\n**{login}** ({ts}):\n\n{c.get('body') or ''}")
        for reply in c.get("replies", {}).get("nodes", []):
            rlogin = reply["author"]["login"] if reply.get("author") else "unknown"
            add_participant(rlogin)
            rts = reply["createdAt"][:10]
            parts.append(f"\n  > **{rlogin}** ({rts}): {reply.get('body') or ''}")

    return {
        "id": f"github-discussion-{number}",
        "source_type": "github_discussion",
        "url": disc["url"],
        "title": disc["title"],
        "author": disc["author"]["login"] if disc.get("author") else "unknown",
        "date": disc["createdAt"][:10],
        "participants": participants,
        "raw_text": "\n".join(parts),
    }


def fetch_local_file(src_cfg: dict) -> dict:
    """Read a local .md, .txt, or .docx file; return normalized dict."""
    raw_path = src_cfg["path"]
    p = Path(raw_path)
    if not p.is_absolute():
        p = WORK_DIR / raw_path
    p = p.resolve()

    if not p.exists():
        raise FileNotFoundError(f"Local file not found: {p}")

    suffix = p.suffix.lower()
    if suffix == ".docx":
        from docx import Document
        doc = Document(str(p))
        raw_text = "\n\n".join(para.text for para in doc.paragraphs if para.text.strip())
    else:
        raw_text = p.read_text(encoding="utf-8", errors="replace")

    return {
        "id": src_cfg["id"],
        "source_type": "local_file",
        "url": str(p),
        "title": src_cfg.get("title", p.name),
        "author": src_cfg.get("author", "unknown"),
        "date": src_cfg.get("date", datetime.now(timezone.utc).date().isoformat()),
        "participants": [src_cfg.get("author", "unknown")],
        "raw_text": raw_text,
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Collect feedback sources for an IFC5 RFC batch.")
    parser.add_argument("batch_json", help="Path to batch.json")
    parser.add_argument("--github-token", help="GitHub API token (overrides GITHUB_TOKEN env var)")
    args = parser.parse_args()

    batch_path = Path(args.batch_json).resolve()
    if not batch_path.exists():
        print(f"[collect] ERROR: batch.json not found: {batch_path}")
        sys.exit(1)

    cfg = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_dir = batch_path.parent
    sources_dir = batch_dir / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)

    token = args.github_token or os.environ.get("GITHUB_TOKEN")

    print(f"[collect] Batch: {cfg['batch_id']}  |  {len(cfg['sources'])} source(s)")

    success = 0
    for src in cfg["sources"]:
        src_id = src["id"]
        out_path = sources_dir / f"{src_id}.json"
        print(f"[collect]   → {src_id} ({src['type']}) ...", end=" ", flush=True)
        try:
            if src["type"] == "github_issue":
                data = fetch_github_issue(src["repo"], src["number"], token)
            elif src["type"] == "github_discussion":
                data = fetch_github_discussion(src["repo"], src["number"], token)
            elif src["type"] == "local_file":
                data = fetch_local_file(src)
            else:
                print(f"SKIP (unknown type '{src['type']}')")
                continue

            out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"OK  → {out_path.relative_to(WORK_DIR)}")
            success += 1
        except Exception as exc:
            print(f"ERROR: {exc}")

    print(f"[collect] Done: {success}/{len(cfg['sources'])} sources collected.")


if __name__ == "__main__":
    main()
