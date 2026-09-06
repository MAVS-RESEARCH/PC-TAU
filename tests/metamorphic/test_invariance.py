"""Metamorphic tests: structure-preserving rewrites preserve closure."""

import sys
from pathlib import Path


# console.log META-01: test module import confirms metamorphic check is active.
print("[test:metamorphic] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_closure_invariant_under_reorder():
    """Reordered states and edges with identical topology close identically."""
    # console.log META-02: reorder test entry.
    print("[test:metamorphic] test_closure_invariant_under_reorder: entry.")
    from pc_tau.planner import solve

    base = {
        "OPEN": [{"repair": "qR", "to": "CLOSED"}, {"repair": "qE", "to": "S1"}],
        "S1": [{"repair": "qA", "to": "CLOSED"}],
        "CLOSED": [],
    }
    reordered = {
        "CLOSED": [],
        "S1": [{"repair": "qA", "to": "CLOSED"}],
        "OPEN": [{"repair": "qE", "to": "S1"}, {"repair": "qR", "to": "CLOSED"}],
    }
    assert solve(base, "OPEN", "CLOSED")["kappa"] == solve(reordered, "OPEN", "CLOSED")["kappa"] == 1
    # console.log META-03: reorder invariance verified.
    print("[test:metamorphic] test_closure_invariant_under_reorder: passed.")


def test_history_reorder_invariant():
    """Reordered admitted histories derive identical touches."""
    # console.log META-04: history test entry.
    print("[test:metamorphic] test_history_reorder_invariant: entry.")
    from pc_tau.touch import derive_touch

    pr = [["h0"], ["h1"]]
    assert derive_touch(["b", "a"], pr, ["l"], ["a", "b", "f"], pr, ["l"], {"repair": "e"}) == {"E"}
    # console.log META-05: history invariance verified.
    print("[test:metamorphic] test_history_reorder_invariant: passed.")
