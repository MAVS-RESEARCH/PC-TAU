"""LLM1 L3 tests: reconstructed metrics integrity and gate readiness."""

import json
from pathlib import Path

import pandas as pd


# console.log L3T-01: test module import confirms L3 checks are active.
print("[test:llm1-l3] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW = REPO_ROOT / "llm1" / "raw"


def test_metrics_join():
    """Metrics rows join trajectories one-to-one with nulls retained."""
    # console.log L3T-02: join test entry.
    print("[test:llm1-l3] test_metrics_join: entry.")
    metrics = pd.read_parquet(REPO_ROOT / "llm1" / "metrics.parquet")
    trajectories = pd.read_parquet(REPO_ROOT / "llm1" / "trajectories.parquet")
    assert len(metrics) == len(trajectories) == 5436
    assert metrics["repair_regret"].isna().any()
    assert (metrics["unsafe_attempts"] >= 0).all()
    assert metrics["unsafe_attempts"].sum() == 262
    assert (metrics["unsafe_attempts"] > 0).sum() == 211
    assert not ((trajectories["effect"]) & (trajectories["steps"].isna())).any()
    # console.log L3T-03: join verified.
    print("[test:llm1-l3] test_metrics_join: passed.")


def test_stratification():
    """Tracks, models and freezes reported separately, never collapsed."""
    # console.log L3T-04: stratification test entry.
    print("[test:llm1-l3] test_stratification: entry.")
    metrics = pd.read_parquet(REPO_ROOT / "llm1" / "metrics.parquet")
    assert set(metrics["track"]) == {"N", "F"}
    assert len(metrics["model"].unique()) == 3
    assert set(metrics["condition"]) == {"F000", "F100", "F010", "F001"}
    paired = pd.read_parquet(REPO_ROOT / "llm1" / "paired_runs.parquet")
    assert len(paired) == 5436
    # console.log L3T-05: stratification verified.
    print("[test:llm1-l3] test_stratification: passed.")


def test_cost_reconciles():
    """Ledger sums equal the cost report within rounding."""
    # console.log L3T-06: cost test entry.
    print("[test:llm1-l3] test_cost_reconciles: entry.")
    rows = [json.loads(line) for line in open(RAW / "cost_ledger.jsonl", encoding="utf-8")]
    calibration = sum(r["reported_cost"] for r in rows if r.get("kind") == "calibration")
    scientific = sum(r["reported_cost"] for r in rows if r.get("kind") == "scientific")
    assert abs(calibration - 0.014074) < 1e-6
    assert abs((calibration + scientific) - 1.070047) < 1e-4
    assert calibration + scientific <= 20.00
    # console.log L3T-07: cost reconciled.
    print("[test:llm1-l3] test_cost_reconciles: passed.")
