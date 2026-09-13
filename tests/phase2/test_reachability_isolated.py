"""P2 test: reachability checker isolated and brute-force correct (Fix 11)."""

import sys
from collections import deque
from pathlib import Path


# console.log P2T08-01: test module import confirms isolation check is active.
print("[test:p2-reachability-isolated] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def brute_viable(repair, initial, successors, terminal):
    """Independent brute-force enumerator for cross-checking."""
    # console.log P2T08-02: brute enumerator entry.
    print("[test:p2-reachability-isolated] brute_viable: entry repair=%s." % repair)
    queue = deque()
    for edge in successors.get(initial, []):
        if edge["repair"] == repair:
            queue.append((edge["to"], 1))
    seen = set()
    while queue:
        state, length = queue.popleft()
        if state == terminal:
            return True
        if (state, length) in seen or length > 10:
            continue
        seen.add((state, length))
        for edge in successors.get(state, []):
            queue.append((edge["to"], length + 1))
    return False


def test_reachability_isolated():
    """Checker imports nothing forbidden and matches brute force."""
    # console.log P2T08-03: isolation test entry.
    print("[test:p2-reachability-isolated] test_reachability_isolated: entry.")
    from pc_tau import reachability
    from pc_tau.reachability import count_viable_first_repairs, viable

    text = (REPO_ROOT / "src" / "pc_tau" / "reachability.py").read_text(encoding="utf-8")
    for token in ["freeze", "planner", "metrics", "Delta", "K_Pi"]:
        assert token not in text
    graphs = [
        ({"OPEN": [{"repair": "a", "to": "CLOSED"}], "CLOSED": []}, "OPEN", "CLOSED"),
        (
            {
                "OPEN": [{"repair": "a", "to": "MID"}, {"repair": "b", "to": "CLOSED"}],
                "MID": [{"repair": "c", "to": "CLOSED"}],
                "CLOSED": [],
            },
            "OPEN",
            "CLOSED",
        ),
        (
            {
                "OPEN": [{"repair": "qR", "to": "CLOSED"}, {"repair": "qE", "to": "S1"}],
                "S1": [{"repair": "qA", "to": "CLOSED"}],
                "CLOSED": [],
            },
            "OPEN",
            "CLOSED",
        ),
    ]
    for successors, initial, terminal in graphs:
        for edge in successors.get(initial, []):
            rep = edge["repair"]
            assert viable(rep, initial, successors, terminal)[0] == brute_viable(
                rep, initial, successors, terminal
            )
    n, _ = count_viable_first_repairs(
        "OPEN",
        {"OPEN": [{"repair": "qR", "to": "CLOSED"}, {"repair": "qE", "to": "S1"}], "S1": [{"repair": "qA", "to": "CLOSED"}], "CLOSED": []},
        "CLOSED",
    )
    assert n == 2
    # console.log P2T08-04: isolation and agreement verified.
    print("[test:p2-reachability-isolated] test_reachability_isolated: passed.")
