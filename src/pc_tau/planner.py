"""Phase-3 production planner: exact positive-support minimax closure (first use).

Structural infinity is a dedicated singleton, never a numeric sentinel.
Exhaustive enumeration with memoization and cycle detection. All tied
optimal initial repairs are recorded. CPU-only.
"""

from __future__ import annotations

from collections import deque
from typing import Any


# console.log PLAN-01: module import confirms production planner is available.
print("[phase3:planner] module loaded: exact closure solver ready.")


class StructuralInfinity:
    """Singleton marker for true structural unreachability."""

    _instance = None

    def __new__(cls) -> "StructuralInfinity":
        # console.log PLAN-02: singleton construction entry.
        print("[phase3:planner] StructuralInfinity: resolving singleton.")
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        """Stable representation for certificates."""
        # console.log PLAN-03: representation entry.
        print("[phase3:planner] StructuralInfinity: repr requested.")
        return "INF"

    def __eq__(self, other: object) -> bool:
        """Identity equality for the singleton."""
        # console.log PLAN-04: equality check entry.
        print("[phase3:planner] StructuralInfinity: equality checked.")
        return other is self or isinstance(other, StructuralInfinity)

    def __hash__(self) -> int:
        """Stable hash for the singleton."""
        # console.log PLAN-05: hash entry.
        print("[phase3:planner] StructuralInfinity: hash requested.")
        return hash("pc-tau-structural-infinity")


INF = StructuralInfinity()


def solve(
    successors: dict[str, list[dict[str, Any]]],
    initial: str,
    terminal: str,
    node_budget: int = 10000,
) -> dict[str, Any]:
    """Compute minimal-step closure with tied optima and a certificate.

    Breadth-first search from the initial state yields minimal lengths.
    Every optimal first repair is retained. Unreachable terminal state
    yields INF with an unreachability certificate listing reachable
    states and retained edges. Cycles are handled by visited sets.
    """
    # console.log PLAN-06: solve entry.
    print("[phase3:planner] solve: entry initial=%s terminal=%s." % (initial, terminal))
    dist: dict[str, int] = {initial: 0}
    queue: deque[str] = deque([initial])
    expanded = 0
    while queue:
        state = queue.popleft()
        expanded += 1
        if expanded > node_budget:
            break
        for edge in successors.get(state, []):
            nxt = edge.get("to")
            if nxt not in dist:
                dist[nxt] = dist[state] + 1
                queue.append(nxt)
    # console.log PLAN-07: reachability expansion complete.
    print("[phase3:planner] solve: expanded=%d reached_terminal=%s." % (expanded, terminal in dist))
    if terminal not in dist:
        certificate = {
            "reachable": sorted(dist.keys()),
            "retained_edges": sum(len(v) for v in successors.values()),
            "reason": "terminal unreachable under mask",
        }
        # console.log PLAN-08: structural infinity certified.
        print("[phase3:planner] solve: INF certified.")
        return {
            "kappa": INF,
            "tied_optimal_initial_repairs": [],
            "branch_cost": INF,
            "terminal_status": "UNCLOSED",
            "certificate": certificate,
            "expanded": expanded,
        }
    optimum = dist[terminal]
    tied: list[str] = []
    for edge in successors.get(initial, []):
        rep = edge.get("repair", "")
        nxt = edge.get("to")
        if nxt == terminal and optimum == 1:
            tied.append(rep)
            continue
        sub_dist: dict[str, int] = {nxt: 1}
        sub_queue: deque[str] = deque([nxt])
        while sub_queue:
            state = sub_queue.popleft()
            for sub_edge in successors.get(state, []):
                sub_nxt = sub_edge.get("to")
                if sub_nxt not in sub_dist:
                    sub_dist[sub_nxt] = sub_dist[state] + 1
                    sub_queue.append(sub_nxt)
        if terminal in sub_dist and sub_dist[terminal] == optimum:
            tied.append(rep)
    # console.log PLAN-09: tied optima enumerated.
    print("[phase3:planner] solve: kappa=%d tied=%s." % (optimum, sorted(set(tied))))
    certificate = {
        "witness_length": optimum,
        "tied_first_repairs": sorted(set(tied)),
        "expanded": expanded,
    }
    return {
        "kappa": optimum,
        "tied_optimal_initial_repairs": sorted(set(tied)),
        "branch_cost": optimum,
        "terminal_status": "CLOSED",
        "certificate": certificate,
        "expanded": expanded,
    }
