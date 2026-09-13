"""P4 test: frozen-class refactoring gates (invariance vs PARTIAL flip)."""

import json
from pathlib import Path

import yaml


# console.log P4T04-01: test module import confirms refactor check is active.
print("[test:p4-refactor] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_refactor_gates():
    """Frozen-only class passes; unlisted perturbations refused."""
    # console.log P4T04-02: refactor test entry.
    print("[test:p4-refactor] test_refactor_gates: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    rows = [
        json.loads(line)
        for line in open(
            REPO_ROOT / "results" / cfg["run_id"] / "audit" / "refactor_results.jsonl",
            encoding="utf-8",
        )
    ]
    assert len(rows) == 1 and rows[0]["passed"] is True
    names = {c["name"] for c in rows[0]["checks"]}
    assert {"harmless-rename-invariant", "reorder-invariant", "boundary-change-routes-to-partial", "no-forced-label", "unlisted-perturbation-refused"} <= names
    # console.log P4T04-03: refactor gates verified.
    print("[test:p4-refactor] test_refactor_gates: passed.")
