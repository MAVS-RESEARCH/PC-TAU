"""P3 test: bootstrap intervals are over tasks with sane ordering."""

import sys
from pathlib import Path


# console.log P3T09-01: test module import confirms bootstrap check is active.
print("[test:p3-bootstrap] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_bootstrap_over_tasks():
    """Mean lies in [lo, hi]; task resampling is deterministic by seed."""
    # console.log P3T09-02: bootstrap test entry.
    print("[test:p3-bootstrap] test_bootstrap_over_tasks: entry.")
    from pc_tau.metrics import bootstrap_mean_ci

    values = [1.0, 1.0, 1.0, 0.0]
    interval = bootstrap_mean_ci(values, seed=0, resamples=200)
    # console.log P3T09-03: interval computed.
    print("[test:p3-bootstrap] mean=%.3f lo=%.3f hi=%.3f." % (interval["mean"], interval["lo"], interval["hi"]))
    assert interval["lo"] <= interval["mean"] <= interval["hi"]
    repeat = bootstrap_mean_ci(values, seed=0, resamples=200)
    assert repeat == interval
    empty = bootstrap_mean_ci([], seed=0)
    assert empty == {"mean": 0.0, "lo": 0.0, "hi": 0.0}
    # console.log P3T09-04: bootstrap verified.
    print("[test:p3-bootstrap] test_bootstrap_over_tasks: passed.")
