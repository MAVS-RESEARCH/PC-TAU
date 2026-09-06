"""P3 test: structural infinity is a singleton, never a numeric sentinel."""

import sys
from pathlib import Path


# console.log P3T01-01: test module import confirms infinity check is active.
print("[test:p3-infinity] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_infinity_structural():
    """INF differs from sentinels; cycles yield certified INF."""
    # console.log P3T01-02: infinity test entry.
    print("[test:p3-infinity] test_infinity_structural: entry.")
    from pc_tau.planner import INF, StructuralInfinity, solve

    assert INF != 10**18 and INF != 999999
    assert StructuralInfinity() is INF
    assert (INF == INF) and hash(INF) == hash(StructuralInfinity())
    cyclic = {"OPEN": [{"repair": "a", "to": "MID"}], "MID": [{"repair": "b", "to": "MID"}], "CLOSED": []}
    result = solve(cyclic, "OPEN", "CLOSED")
    # console.log P3T01-03: cyclic graph solved.
    print("[test:p3-infinity] cyclic terminal=%s." % result["terminal_status"])
    assert result["kappa"] is INF and result["terminal_status"] == "UNCLOSED"
    assert "reachable" in result["certificate"]
    # console.log P3T01-04: structural infinity verified.
    print("[test:p3-infinity] test_infinity_structural: passed.")
