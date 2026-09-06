"""P2 test: 100 percent provenance for retained repairs."""

import json
import sys
from pathlib import Path


# console.log P2T01-01: test module import confirms provenance check is active.
print("[test:p2-provenance] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def _run_id():
    """Read run id from experiment config."""
    # console.log P2T01-02: run id resolution entry.
    print("[test:p2-provenance] _run_id: reading experiment config.")
    import yaml

    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    return cfg["run_id"]


def test_provenance_complete():
    """Every repair has locator, justification, fragment hash and rule id."""
    # console.log P2T01-03: provenance test entry.
    print("[test:p2-provenance] test_provenance_complete: entry.")
    run_id = _run_id()
    contract_dir = REPO_ROOT / "results" / run_id / "contract"
    repairs = [json.loads(line) for line in open(contract_dir / "repair_actions.jsonl", encoding="utf-8")]
    facts = [json.loads(line) for line in open(contract_dir / "semantic_facts.jsonl", encoding="utf-8")]
    # console.log P2T01-04: artifacts loaded.
    print("[test:p2-provenance] repairs=%d facts=%d." % (len(repairs), len(facts)))
    assert len(repairs) > 0 and len(facts) > 0
    for repair in repairs:
        assert repair.get("locator") and repair.get("justification")
    for fact in facts:
        assert fact.get("locator") and fact.get("fragment_hash") and fact.get("extraction_rule_id")
    families = [json.loads(line) for line in open(contract_dir / "contract_families.jsonl", encoding="utf-8")]
    contracts = [json.loads(line) for line in open(contract_dir / "task_contracts.jsonl", encoding="utf-8")]
    assert len(families) == len(contracts) > 0
    # console.log P2T01-05: provenance completeness verified.
    print("[test:p2-provenance] test_provenance_complete: passed.")
