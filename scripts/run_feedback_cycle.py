"""
run_feedback_cycle.py
---------------------
Orchestrator for the IFC5 RFC committee feedback pipeline.

Runs: collect → validate → synthesize → analyze → summary

Usage:
    python run_feedback_cycle.py <batch_config.json>
        [--github-token TOKEN]
        [--skip-validate]
        [--skip-synthesize]
        [--skip-analyze]
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent

STEPS = [
    ("collect",    "feedback_collect.py"),
    ("validate",   "feedback_validate.py"),
    ("synthesize", "feedback_synthesize.py"),
    ("analyze",    "feedback_analyze.py"),
    ("summary",    "feedback_summary.py"),
]


def run_step(script_name: str, batch_json: str, extra_args: list[str] = None) -> bool:
    """Run a pipeline step script; return True on success."""
    script_path = SCRIPT_DIR / script_name
    cmd = [sys.executable, str(script_path), batch_json] + (extra_args or [])
    print(f"\n{'='*60}")
    print(f"STEP: {script_name}")
    print(f"{'='*60}")
    t0 = time.time()
    result = subprocess.run(cmd)
    elapsed = time.time() - t0
    ok = result.returncode == 0
    status = "OK" if ok else f"FAILED (exit {result.returncode})"
    print(f"[orchestrator] {script_name}: {status}  ({elapsed:.1f}s)")
    return ok


def validate_batch_config(cfg: dict) -> list[str]:
    """Basic validation of batch config; return list of error strings."""
    errors = []
    if "batch_id" not in cfg:
        errors.append("Missing 'batch_id'")
    if "sources" not in cfg or not isinstance(cfg["sources"], list):
        errors.append("Missing or invalid 'sources' list")
    else:
        for i, src in enumerate(cfg["sources"]):
            if "id" not in src:
                errors.append(f"Source[{i}] missing 'id'")
            if "type" not in src:
                errors.append(f"Source[{i}] missing 'type'")
    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Run the IFC5 RFC committee feedback pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("batch_json", help="Path to batch.json")
    parser.add_argument("--github-token", help="GitHub API token (passed to collect step)")
    parser.add_argument("--skip-validate",   action="store_true", help="Skip validation step")
    parser.add_argument("--skip-synthesize", action="store_true", help="Skip synthesis step")
    parser.add_argument("--skip-analyze",    action="store_true", help="Skip analysis step")
    args = parser.parse_args()

    batch_path = Path(args.batch_json).resolve()
    if not batch_path.exists():
        print(f"[orchestrator] ERROR: batch.json not found: {batch_path}")
        sys.exit(1)

    cfg = json.loads(batch_path.read_text(encoding="utf-8"))

    # Validate config
    errors = validate_batch_config(cfg)
    if errors:
        print("[orchestrator] ERROR: Invalid batch config:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    batch_id = cfg["batch_id"]
    print(f"\n{'#'*60}")
    print(f"  IFC5 RFC Feedback Pipeline")
    print(f"  Batch: {batch_id}")
    print(f"  Description: {cfg.get('description', '(none)')}")
    print(f"  Sources: {len(cfg.get('sources', []))}")
    print(f"{'#'*60}")

    # Create batch directory structure
    batch_dir = WORK_DIR / "04 Committee Feedback" / batch_id
    (batch_dir / "sources").mkdir(parents=True, exist_ok=True)
    (batch_dir / "proposed-updates").mkdir(parents=True, exist_ok=True)
    print(f"[orchestrator] Batch directory: {batch_dir.relative_to(WORK_DIR.parent)}")

    # Determine skip flags
    skip_steps = set()
    if args.skip_validate:
        skip_steps.add("validate")
    if args.skip_synthesize:
        skip_steps.add("synthesize")
    if args.skip_analyze:
        skip_steps.add("analyze")

    # Build extra args per step
    extra_args_map: dict[str, list] = {
        "collect": (["--github-token", args.github_token] if args.github_token else []),
    }

    # Run steps
    results: dict[str, str] = {}
    pipeline_ok = True
    t_start = time.time()

    for step_name, script_name in STEPS:
        if step_name in skip_steps:
            print(f"\n[orchestrator] Skipping: {step_name}")
            results[step_name] = "SKIPPED"
            continue

        extra = extra_args_map.get(step_name, [])
        ok = run_step(script_name, str(batch_path), extra)
        results[step_name] = "OK" if ok else "FAILED"
        if not ok:
            pipeline_ok = False
            print(f"[orchestrator] WARNING: {step_name} failed — continuing pipeline.")

    # Final report
    total_time = time.time() - t_start
    summary_filename = f"IFC5-RFC-Update-Summary-{batch_id}.md"
    summary_path = batch_dir / summary_filename

    print(f"\n{'#'*60}")
    print(f"  Pipeline complete ({total_time:.1f}s)")
    print(f"{'#'*60}")
    for step_name, _ in STEPS:
        status = results.get(step_name, "NOT RUN")
        icon = {"OK": "✅", "SKIPPED": "⏭ ", "FAILED": "❌"}.get(status, "❓")
        print(f"  {icon}  {step_name:<15} {status}")

    print()
    if summary_path.exists():
        print(f"  Summary report: {summary_path.relative_to(WORK_DIR.parent)}")
    else:
        print("  Summary report: not generated")

    sys.exit(0 if pipeline_ok else 1)


if __name__ == "__main__":
    main()
