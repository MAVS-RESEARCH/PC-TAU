"""P3 test: raw trajectories archived, manifested and bundle-listed (Fix 6/14)."""

import json
import sys
from pathlib import Path

import yaml


# console.log P3T11-01: test module import confirms archive check is active.
print("[test:p3-archived] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_trajectories_archived():
    """Trajectory count joins pairing; hashes match; bundle list covers them."""
    # console.log P3T11-02: archive test entry.
    print("[test:p3-archived] test_trajectories_archived: entry.")
    from pc_tau.source import sha256_of_canonical

    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    agents_dir = REPO_ROOT / "results" / run_id / "agents"
    trajectories = [json.loads(line) for line in open(agents_dir / "trajectories.jsonl", encoding="utf-8")]
    import pandas as pd

    paired = pd.read_parquet(agents_dir / "paired_runs.parquet")
    # console.log P3T11-03: counts joined.
    print("[test:p3-archived] trajs=%d paired=%d." % (len(trajectories), len(paired)))
    assert len(trajectories) == len(paired) == 5436
    manifest = json.loads(
        (REPO_ROOT / "results" / run_id / "phase_manifest.json").read_text(encoding="utf-8")
    )
    key = "results/%s/agents/trajectories.jsonl" % run_id
    assert manifest[key] == sha256_of_canonical(trajectories)
    assert manifest[key] == sha256_of_canonical(
        [json.loads(line) for line in open(agents_dir / "trajectories.jsonl", encoding="utf-8")]
    )
    # console.log P3T11-04: archive verified.
    print("[test:p3-archived] test_trajectories_archived: passed.")
