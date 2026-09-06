"""P2 test: refactoring class frozen before any freeze (Fix 4)."""

import json
from pathlib import Path

import yaml


# console.log P2T12-01: test module import confirms policy check is active.
print("[test:p2-refactor-frozen] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_refactor_policy_frozen():
    """Three policy files exist, frozen, hashed; Phase-3 code cannot exist yet."""
    # console.log P2T12-02: policy test entry.
    print("[test:p2-refactor-frozen] test_refactor_policy_frozen: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    contract_dir = REPO_ROOT / "results" / run_id / "contract"
    manifest = json.loads(
        (REPO_ROOT / "results" / run_id / "phase_manifest.json").read_text(encoding="utf-8")
    )
    for name in ["semantic_boundary_policy.json", "admissible_refactorings.json", "contract_family_rules.json"]:
        payload = json.loads((contract_dir / name).read_text(encoding="utf-8"))
        assert payload.get("frozen") is True
        assert "results/%s/contract/%s" % (run_id, name) in manifest
    # console.log P2T12-03: policies frozen and manifested.
    print("[test:p2-refactor-frozen] policies sealed.")
    assert not list((REPO_ROOT / "scripts").glob("phase3_*.py"))
    assert not (REPO_ROOT / "src" / "pc_tau" / "planner.py").exists()
    # console.log P2T12-04: Phase-3 absence verified.
    print("[test:p2-refactor-frozen] test_refactor_policy_frozen: passed.")
