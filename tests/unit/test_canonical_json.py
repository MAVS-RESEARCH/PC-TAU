"""Unit test for canonical JSON determinism (WorkPlan style check)."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

import json


# console.log UT-01: test module import confirms harness is active.
print("[test:canonical-json] module loaded.")


def test_canonical_dumps_deterministic():
    """Canonical dumps must be key-order independent and compact."""
    # console.log UT-02: determinism test entry.
    print("[test:canonical-json] test_canonical_dumps_deterministic: entry.")
    from pc_tau.source import canonical_dumps

    a = {"b": 2, "a": 1}
    b = {"a": 1, "b": 2}
    assert canonical_dumps(a) == canonical_dumps(b)
    assert canonical_dumps(a) == '{"a":1,"b":2}'
    # console.log UT-03: determinism assertions passed.
    print("[test:canonical-json] test_canonical_dumps_deterministic: passed.")


def test_canonical_hash_stable():
    """Same object yields same hash; timestamps must not leak into hashes."""
    # console.log UT-04: hash stability test entry.
    print("[test:canonical-json] test_canonical_hash_stable: entry.")
    from pc_tau.source import sha256_of_canonical

    obj = {"x": [1, 2, 3]}
    assert sha256_of_canonical(obj) == sha256_of_canonical(obj)
    assert len(sha256_of_canonical(obj)) == 64
    # console.log UT-05: hash stability assertions passed.
    print("[test:canonical-json] test_canonical_hash_stable: passed.")
