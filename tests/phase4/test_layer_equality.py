"""P4 test: independent layers equal sealed outputs with full agreement."""

import json
from pathlib import Path

import yaml


# console.log P4T02-01: test module import confirms equality check is active.
print("[test:p4-layers] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_layer_equality():
    """audit.json all_equal with 100 percent planner agreement and sidecar exactness."""
    # console.log P4T02-02: equality test entry.
    print("[test:p4-layers] test_layer_equality: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    audit = json.loads((REPO_ROOT / "results" / run_id / "audit" / "audit.json").read_text(encoding="utf-8"))
    assert audit["all_equal"] is True
    assert set(audit["layers"]) == {"source", "contract", "touch", "planner", "run"}
    agreement = json.loads((REPO_ROOT / "results" / run_id / "audit" / "planner_agreement.json").read_text(encoding="utf-8"))
    assert abs(agreement["agreement"] - 1.0) < 1e-12
    # console.log P4T02-03: equality verified.
    print("[test:p4-layers] test_layer_equality: passed.")
