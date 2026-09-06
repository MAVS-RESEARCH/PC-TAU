"""P2 test: viable routes beat dead buttons via the checker (Fix 3)."""

import sys
from pathlib import Path


# console.log P2T10-01: test module import confirms route check is active.
print("[test:p2-viable-routes] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_viable_routes():
    """Two-route graph passes; single-closer plus dead button fails."""
    # console.log P2T10-02: route test entry.
    print("[test:p2-viable-routes] test_viable_routes: entry.")
    from pc_tau.reachability import count_viable_first_repairs

    two_route = {
        "OPEN": [{"repair": "qR", "to": "CLOSED"}, {"repair": "qE", "to": "S1"}],
        "S1": [{"repair": "qA", "to": "CLOSED"}],
        "CLOSED": [],
    }
    dead_button = {
        "OPEN": [{"repair": "q1", "to": "CLOSED"}, {"repair": "q2", "to": "DEAD"}],
        "DEAD": [],
        "CLOSED": [],
    }
    n_two, _ = count_viable_first_repairs("OPEN", two_route, "CLOSED")
    n_dead, _ = count_viable_first_repairs("OPEN", dead_button, "CLOSED")
    # console.log P2T10-03: route counts compared.
    print("[test:p2-viable-routes] two=%d dead=%d." % (n_two, n_dead))
    assert n_two >= 2
    assert n_dead == 1
    # console.log P2T10-04: viable-route rule verified.
    print("[test:p2-viable-routes] test_viable_routes: passed.")
