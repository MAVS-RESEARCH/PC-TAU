"""P2 test: sealed primary with partial sidecar authorizes Phase 3 (Fix 12)."""

import json
from pathlib import Path

import yaml


# console.log P2T11-01: test module import confirms seal check is active.
print("[test:p2-sealed-with-partials] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_sealed_with_partials():
    """IDENTIFIED core plus sidecar seals; primary alone authorizes Phase 3."""
    # console.log P2T11-02: seal test entry.
    print("[test:p2-sealed-with-partials] test_sealed_with_partials: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    contract_dir = REPO_ROOT / "results" / run_id / "contract"
    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    partials = [line for line in open(contract_dir / "partial_tasks.jsonl", encoding="utf-8") if line.strip()]
    marker = json.loads((contract_dir / "CONTRACT_SEALED").read_text(encoding="utf-8"))
    # console.log P2T11-03: seal artifacts loaded.
    print(
        "[test:p2-sealed-with-partials] primary=%d partial=%d marker=%s."
        % (population["count"], len(partials), marker["status"])
    )
    assert population["count"] >= 40 and len(population["by_domain"]) >= 2
    assert marker["status"] == "CONTRACT_SEALED"
    assert marker["primary"] == population["count"]
    assert not (contract_dir / "PARTIAL").exists()
    assert set(population["task_ids"]).isdisjoint(
        {json.loads(line)["task_id"] for line in partials}
    )
    # console.log P2T11-04: sealed-with-partials verified.
    print("[test:p2-sealed-with-partials] test_sealed_with_partials: passed.")
