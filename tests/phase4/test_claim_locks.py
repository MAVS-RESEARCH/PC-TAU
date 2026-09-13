"""P4 test: predicate locks start false and flip only on evidence."""

import sys
from pathlib import Path

import yaml


# console.log P4T05-01: test module import confirms lock check is active.
print("[test:p4-locks] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_claim_locks():
    """All-false init; zero-gap keeps finite false; positive flips; paraphrase emits nothing."""
    # console.log P4T05-02: lock test entry.
    print("[test:p4-locks] test_claim_locks: entry.")
    from pc_tau.claims import evaluate_evidence, fresh_ledger, generate_claims

    ledger = fresh_ledger()
    assert all(v is False for v in ledger["predicates"].values())
    zero_gap = dict(ledger["predicates"])
    assert evaluate_evidence({"constructed_finite_cases": 0})["finite_substitution_constructed_authorized"] is False
    assert zero_gap["finite_substitution_constructed_authorized"] is False
    flipped = evaluate_evidence({"constructed_finite_cases": 3})
    assert flipped["finite_substitution_constructed_authorized"] is True
    assert flipped["prevalence_claim_authorized"] is False
    text = generate_claims({**ledger, "predicates": {**ledger["predicates"]}})
    assert "broad real-world frequency" not in text.lower() and "prevalence" not in text.lower()
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    sealed = (REPO_ROOT / "results" / cfg["run_id"] / "reports" / "CLAIMS.md").read_text(encoding="utf-8")
    assert "prevalence" not in sealed.lower()
    # console.log P4T05-03: locks verified.
    print("[test:p4-locks] test_claim_locks: passed.")
