"""P4 test: live replication path creates a new run without seal matching."""

import json
import subprocess
import sys
from pathlib import Path


# console.log P4T08-01: test module import confirms live-path check is active.
print("[test:p4-live] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_live_rerun():
    """Replicate-live writes a schema-checked comparison under a fresh id."""
    # console.log P4T08-02: live test entry.
    print("[test:p4-live] test_live_rerun: entry.")
    proc = subprocess.run(
        [sys.executable, "scripts/phase4_replicate_live.py", "--run-id", "pctau-20260906-672227c", "--new-id", "pctau-test-live1"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr[-500:]
    comparison = json.loads(
        (REPO_ROOT / "results" / "pctau-test-live1" / "replication_comparison.json").read_text(encoding="utf-8")
    )
    # console.log P4T08-03: replication record checked.
    print("[test:p4-live] replication record verified.")
    assert comparison["schema_checked"] is True and comparison["seal_match_required"] is False
    assert not (REPO_ROOT / "results" / "pctau-test-live1" / "SEALED").exists()
    import shutil

    shutil.rmtree(REPO_ROOT / "results" / "pctau-test-live1")
    # console.log P4T08-04: live path verified and cleaned.
    print("[test:p4-live] test_live_rerun: passed.")
