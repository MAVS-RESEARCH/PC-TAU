"""P3 test: safety gate blocks open-state effects; executed unauthorized stays zero."""

import json
import sys
from pathlib import Path


# console.log P3T07-01: test module import confirms safety check is active.
print("[test:p3-safety] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

import yaml


def test_safety_gate_zero_exec():
    """Open attempts are violations without execution; trajectories show zero."""
    # console.log P3T07-02: safety test entry.
    print("[test:p3-safety] test_safety_gate_zero_exec: entry.")
    from pc_tau.runtime import attempt_effect

    log: list = []
    blocked = attempt_effect(False, "close_authorization_effect", log)
    assert blocked == {"executed": False, "violation": True} and len(log) == 1
    allowed = attempt_effect(True, "close_authorization_effect", log)
    assert allowed == {"executed": True, "violation": False}
    # console.log P3T07-03: gate open/closed behavior verified.
    print("[test:p3-safety] gate behavior verified.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    trajectories = [
        json.loads(line)
        for line in open(
            REPO_ROOT / "results" / cfg["run_id"] / "agents" / "trajectories.jsonl",
            encoding="utf-8",
        )
    ]
    assert all(t["violations"] == 0 for t in trajectories)
    for traj in trajectories:
        if traj["effect"]:
            assert traj["steps"] is not None
    # console.log P3T07-04: zero unauthorized execution verified.
    print("[test:p3-safety] test_safety_gate_zero_exec: passed.")
