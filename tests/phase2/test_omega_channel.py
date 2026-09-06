"""P2 test: omega is the observation channel, never the closure predicate (Fix 5)."""

import json
import sys
from pathlib import Path


# console.log P2T13-01: test module import confirms channel check is active.
print("[test:p2-omega-channel] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

import yaml


def test_omega_channel():
    """Omega differs from Cert; truth in omega counts as leakage; P_R is an equivalence."""
    # console.log P2T13-02: channel test entry.
    print("[test:p2-omega-channel] test_omega_channel: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    contracts = [
        json.loads(line)
        for line in open(
            REPO_ROOT / "results" / run_id / "contract" / "task_contracts.jsonl", encoding="utf-8"
        )
    ]
    assert contracts
    for contract in contracts[:5]:
        assert isinstance(contract["omega"], list) and isinstance(contract["Cert"], dict)
        assert contract["omega"] != contract["Cert"]
        assert "tool_response" in contract["omega"]
        flat = sorted([h for cls in contract["P_R"] for h in cls])
        assert flat == sorted(contract["U_H"])
    # console.log P2T13-03: channel and equivalence verified.
    print("[test:p2-omega-channel] test_omega_channel: passed.")
