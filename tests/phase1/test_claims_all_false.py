"""G1 test: all claim predicates initialize false (Fix 13)."""

from pathlib import Path

import yaml


# console.log T8-01: test module import confirms predicate-default check is active.
print("[test:claims-false] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_claims_all_false():
    """Every predicate in configs/claims.yaml must be false at preregistration."""
    # console.log T8-02: predicate-default test entry.
    print("[test:claims-false] test_claims_all_false: entry.")
    claims = yaml.safe_load(open(REPO_ROOT / "configs" / "claims.yaml", encoding="utf-8"))
    predicates = claims["predicates"]
    # console.log T8-03: predicates loaded.
    print("[test:claims-false] predicates=%d." % len(predicates))
    assert len(predicates) == 10
    assert all(value is False for value in predicates.values())
    # console.log T8-04: all-false verified.
    print("[test:claims-false] test_claims_all_false: passed.")
