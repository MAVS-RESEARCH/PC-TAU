"""P3 test: same-instance discipline holds (only the mask differs)."""

from pathlib import Path

import pandas as pd
import yaml


# console.log P3T05-01: test module import confirms same-instance check is active.
print("[test:p3-same-instance] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_same_instance():
    """Base hash single per task; view hashes differ; masks match the lattice."""
    # console.log P3T05-02: same-instance test entry.
    print("[test:p3-same-instance] test_same_instance: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    exact = pd.read_parquet(
        REPO_ROOT / "results" / cfg["run_id"] / "exact" / "freeze_results.parquet"
    )
    expected_masks = {
        "F000": [], "F100": ["E"], "F010": ["R"], "F001": ["A"],
        "F110": ["E", "R"], "F101": ["E", "A"], "F011": ["R", "A"], "F111": ["E", "R", "A"],
    }
    # console.log P3T05-03: freeze rows grouped per task.
    print("[test:p3-same-instance] rows=%d." % len(exact))
    for task_id, group in exact.groupby("task_id"):
        assert len(group) == 8
        assert group["base_hash"].nunique() == 1
        assert group["view_hash"].nunique() >= 2
        for _, row in group.iterrows():
            assert sorted(row["mask"]) == sorted(expected_masks[row["freeze"]])
    # console.log P3T05-04: same-instance discipline verified.
    print("[test:p3-same-instance] test_same_instance: passed.")
