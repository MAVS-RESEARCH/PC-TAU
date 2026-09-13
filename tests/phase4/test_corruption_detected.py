"""P4 test: all 8 corruption families fail closed."""

import json
from pathlib import Path

import yaml


# console.log P4T03-01: test module import confirms corruption check is active.
print("[test:p4-corrupt] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_corruption_detected():
    """Every family passed with all injections detected."""
    # console.log P4T03-02: corruption test entry.
    print("[test:p4-corrupt] test_corruption_detected: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    families = [
        json.loads(line)
        for line in open(
            REPO_ROOT / "results" / cfg["run_id"] / "audit" / "corruption_results.jsonl",
            encoding="utf-8",
        )
    ]
    assert len(families) == 8
    assert all(f["passed"] for f in families)
    assert sum(len(f["checks"]) for f in families) >= 16
    # console.log P4T03-03: corruption families verified.
    print("[test:p4-corrupt] test_corruption_detected: passed.")
