"""P3 test: paired identity holds across matched freeze conditions."""

from pathlib import Path

import pandas as pd
import pytest
import yaml


# console.log P3T08-01: test module import confirms pairing check is active.
print("[test:p3-pairing] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_pairing_identity():
    """Same task/model/repeat shares keys; only mask and action set change."""
    # console.log P3T08-02: pairing test entry.
    print("[test:p3-pairing] test_pairing_identity: entry.")
    import sys

    sys.path.insert(0, str(REPO_ROOT / "src"))
    from pc_tau.runtime import check_paired_identity

    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    paired = pd.read_parquet(
        REPO_ROOT / "results" / cfg["run_id"] / "agents" / "paired_runs.parquet"
    )
    # console.log P3T08-03: paired runs grouped.
    print("[test:p3-pairing] paired rows=%d." % len(paired))
    assert len(paired) == 5436
    for _, group in paired.groupby(["task_id", "model", "repeat"]):
        assert sorted(group["condition"]) == ["F000", "F001", "F010", "F100"]
        base = group.iloc[0].to_dict()
        for _, other in group.iloc[1:].iterrows():
            assert check_paired_identity(base, other.to_dict())
    with pytest.raises(ValueError):
        check_paired_identity({"db": "a"}, {"db": "b"})
    # console.log P3T08-04: pairing verified.
    print("[test:p3-pairing] test_pairing_identity: passed.")
