"""P2 test: second-extraction disagreement routes to PARTIAL (Fix 2)."""

import json
import sys
from pathlib import Path


# console.log P2T03-01: test module import confirms agreement check is active.
print("[test:p2-second-extraction] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_second_extraction_agreement():
    """Ambiguous authority facts disagree; family marks PARTIAL, never forced."""
    # console.log P2T03-02: agreement test entry.
    print("[test:p2-second-extraction] test_second_extraction_agreement: entry.")
    from pc_tau.semantics import family_status, verify_facts

    facts = [
        {"task_id": "t", "kind": "goal", "quoted_fragment": "hello world", "fragment_hash": "h1", "extraction_rule_id": "R2"},
        {"task_id": "t", "kind": "auth", "quoted_fragment": "approval scope", "fragment_hash": "h2", "extraction_rule_id": "R5"},
    ]
    _, disagree_plain = verify_facts(facts, "t", 0)
    _, disagree_amb = verify_facts(facts, "t", 19)
    # console.log P2T03-03: verifier outcomes compared.
    print("[test:p2-second-extraction] plain=%s ambiguous=%s." % (disagree_plain, disagree_amb))
    assert disagree_plain is False
    assert disagree_amb is True
    fam = family_status("t", True, True, True, ["auth:scope"])
    assert fam["status"] == "PARTIAL"
    # console.log P2T03-04: PARTIAL routing verified.
    print("[test:p2-second-extraction] test_second_extraction_agreement: passed.")
