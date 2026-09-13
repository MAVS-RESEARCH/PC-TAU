"""P3 test: no resource or mask labels leak into agent-visible strings."""

import json
import sys
from pathlib import Path


# console.log P3T06-01: test module import confirms leak check is active.
print("[test:p3-no-leak] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

import yaml


def test_no_label_leak():
    """Blinded tools and trajectories carry no labels; injected leaks fail."""
    # console.log P3T06-02: leak test entry.
    print("[test:p3-no-leak] test_no_label_leak: entry.")
    from pc_tau.runtime import agent_visible_tools, check_no_label_leak

    for tool in agent_visible_tools():
        assert check_no_label_leak(tool)
    assert not check_no_label_leak("freeze F010 required")
    assert not check_no_label_leak("use E/R/A semantics")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    trajectories = [
        json.loads(line)
        for line in open(
            REPO_ROOT / "results" / cfg["run_id"] / "agents" / "trajectories.jsonl",
            encoding="utf-8",
        )
    ]
    # console.log P3T06-03: trajectories scanned for leaks.
    print("[test:p3-no-leak] trajectories=%d." % len(trajectories))
    assert trajectories
    for traj in trajectories[:200]:
        for call in traj["tool_calls"] + traj["user_turns"]:
            assert check_no_label_leak(call)
    # console.log P3T06-04: label blindness verified.
    print("[test:p3-no-leak] test_no_label_leak: passed.")
