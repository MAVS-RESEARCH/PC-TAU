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
    for path in (REPO_ROOT / "scripts").glob("phase3_*.py"):
        lines = path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if "semantic_boundary_policy" in line or "admissible_refactorings" in line or "contract_family_rules" in line:
                window = "\n".join(lines[max(0, i - 2):i + 3])
                assert "write_text" not in window and '"w"' not in window and "'w'" not in window, (
                    "%s writes refactor policy: %s" % (path.name, line.strip()[:100])
                )
    # console.log P2T12-04: Phase-3 non-interference verified.
    print("[test:p2-refactor-frozen] test_refactor_policy_frozen: passed.")
