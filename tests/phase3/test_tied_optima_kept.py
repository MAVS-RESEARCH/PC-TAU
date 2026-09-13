"""P3 test: all tied optimal initial repairs are recorded."""

import sys
from pathlib import Path


# console.log P3T02-01: test module import confirms tie check is active.
print("[test:p3-tied] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_tied_optima_kept():
    """Two one-step closers both appear; omission would fail."""
    # console.log P3T02-02: tie test entry.
    print("[test:p3-tied] test_tied_optima_kept: entry.")
    from pc_tau.planner import solve

    graph = {
        "OPEN": [{"repair": "qa", "to": "CLOSED"}, {"repair": "qb", "to": "CLOSED"}],
        "CLOSED": [],
    }
    result = solve(graph, "OPEN", "CLOSED")
    # console.log P3T02-03: tied graph solved.
    print("[test:p3-tied] kappa=%s tied=%s." % (result["kappa"], result["tied_optimal_initial_repairs"]))
    assert result["kappa"] == 1
    assert sorted(result["tied_optimal_initial_repairs"]) == ["qa", "qb"]
    # console.log P3T02-04: tied optima verified.
    print("[test:p3-tied] test_tied_optima_kept: passed.")
