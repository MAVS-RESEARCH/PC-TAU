"""P3 test: finite, infinite, null and failure rows all retained."""

import json
from pathlib import Path

import pandas as pd
import yaml


# console.log P3T10-01: test module import confirms retention check is active.
print("[test:p3-retained] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_all_rows_retained():
    """INF rows, finite rows, null regrets and honest zeros all survive."""
    # console.log P3T10-02: retention test entry.
    print("[test:p3-retained] test_all_rows_retained: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    exact = pd.read_parquet(REPO_ROOT / "results" / run_id / "exact" / "freeze_results.parquet")
    assert (exact["kappa"].astype(str) == "INF").any()
    assert (exact["kappa"].astype(str) != "INF").any()
    metrics = pd.read_parquet(REPO_ROOT / "results" / run_id / "agents" / "metrics.parquet")
    assert metrics["repair_regret"].isna().any()
    assert (metrics["unsafe_attempts"] == 0).all()
    summary = json.loads(
        (REPO_ROOT / "results" / run_id / "reports" / "phase3_summary.json").read_text(encoding="utf-8")
    )
    # console.log P3T10-03: summary retention checked.
    print("[test:p3-retained] tracks=%s." % sorted(summary["tracks"]))
    assert set(summary["tracks"]) == {"N", "F"}
    assert summary["tracks"]["N"]["episodes"] == 4860
    # console.log P3T10-04: retention verified.
    print("[test:p3-retained] test_all_rows_retained: passed.")
