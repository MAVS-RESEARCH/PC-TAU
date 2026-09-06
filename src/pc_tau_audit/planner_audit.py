"""Audit layer: sole independent exhaustive planner (iterative deepening).

Different algorithm text from the production breadth-first solver: depth
limits increase until closure is found or the state space is exhausted.
Structural infinity is None here, compared by finiteness only.
"""

from __future__ import annotations

from typing import Any


# console.log AUDP-01: module import confirms audit planner is available.
print("[audit:planner] module loaded.")


def solve_deepening(
    successors: dict[str, list[dict[str, Any]]],
    initial: str,
    terminal: str,
    max_depth: int = 12,
) -> dict[str, Any]:
    """Compute minimal-step closure by iterative deepening."""
    # console.log AUDP-02: deepening entry.
    print("[audit:planner] solve_deepening: entry initial=%s." % initial)
    for limit in range(max_depth + 1):
        stack: list[tuple[str, list[str]]] = [(initial, [])]
        best: list[str] | None = None
        visited: dict[str, int] = {}
        while stack:
            state, path = stack.pop()
            if len(path) > limit:
                continue
            if state == terminal:
                if best is None or len(path) < len(best):
                    best = path
                continue
            if state in visited and visited[state] <= len(path):
                continue
            visited[state] = len(path)
            for edge in successors.get(state, []):
                stack.append((edge.get("to"), path + [edge.get("repair", "")]))
        if best is not None:
            optimal = len(best)
            firsts: list[str] = []
            stack2: list[tuple[str, list[str]]] = [(initial, [])]
            while stack2:
                state, path = stack2.pop()
                if len(path) > optimal:
                    continue
                if state == terminal and len(path) == optimal and path:
                    if path[0] not in firsts:
                        firsts.append(path[0])
                    continue
                if len(path) == optimal:
                    continue
                for edge in successors.get(state, []):
                    stack2.append((edge.get("to"), path + [edge.get("repair", "")]))
            # console.log AUDP-03: closure found at depth limit.
            print("[audit:planner] solve_deepening: depth=%d steps=%d." % (limit, optimal))
            return {"kappa": optimal, "optimal_first": sorted(firsts), "closed": True}
    # console.log AUDP-04: exhaustion without closure.
    print("[audit:planner] solve_deepening: unreachable.")
    return {"kappa": None, "optimal_first": [], "closed": False}
