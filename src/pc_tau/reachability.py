"""Fix-11 unrestricted closure-reachability checker.

Determines whether a repair begins at least one finite legal closure
path on the unrestricted graph. The checker uses only graph topology
(states, repairs, successors, terminal marker). It has no notion of
resource masks, numerical weights, comparative gaps or signatures,
and it is never replaced by the optimizing solver used later.
"""

from __future__ import annotations

from collections import deque
from typing import Any


# console.log REACH-01: module import confirms checker is available.
print("[phase1:reachability] module loaded: unrestricted viability checker ready.")


def viable(
    repair: str,
    initial: str,
    successors: dict[str, list[dict[str, Any]]],
    terminal: str,
    node_budget: int = 1000,
) -> tuple[bool, int | None]:
    """Return (is_viable, witness_length) for a first repair.

    A repair is viable when a finite legal path beginning with it
    reaches the terminal state. Breadth-first search over the
    unrestricted graph is used. Witness length counts edges.
    """
    # console.log REACH-02: viable entry for repair.
    print("[phase1:reachability] viable: entry repair=%s initial=%s." % (repair, initial))
    first_steps = [e for e in successors.get(initial, []) if e.get("repair") == repair]
    if not first_steps:
        # console.log REACH-03: repair not offered at initial state.
        print("[phase1:reachability] viable: repair not offered at initial state.")
        return False, None
    best: int | None = None
    for first in first_steps:
        start = first.get("to")
        if start == terminal:
            # console.log REACH-04: direct closure found.
            print("[phase1:reachability] viable: direct closure path length=1.")
            return True, 1
        queue: deque[tuple[str, int]] = deque([(start, 1)])
        seen: set[str] = {start}
        expanded = 0
        while queue:
            state, length = queue.popleft()
            expanded += 1
            if expanded > node_budget:
                break
            for edge in successors.get(state, []):
                nxt = edge.get("to")
                if nxt == terminal:
                    total = length + 1
                    if best is None or total < best:
                        best = total
                    continue
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, length + 1))
        # console.log REACH-05: first-step search branch complete.
        print("[phase1:reachability] viable: branch searched expanded=%d." % expanded)
    if best is None:
        # console.log REACH-06: no finite closure path found.
        print("[phase1:reachability] viable: no finite closure path found.")
        return False, None
    # console.log REACH-07: viable with witness length.
    print("[phase1:reachability] viable: viable witness_length=%d." % best)
    return True, best


def count_viable_first_repairs(
    initial: str,
    successors: dict[str, list[dict[str, Any]]],
    terminal: str,
    node_budget: int = 1000,
) -> tuple[int, dict[str, int]]:
    """Count distinct first repairs that are viable, with witness lengths."""
    # console.log REACH-08: count entry.
    print("[phase1:reachability] count_viable_first_repairs: entry initial=%s." % initial)
    repairs = sorted({e.get("repair", "") for e in successors.get(initial, [])})
    viable_map: dict[str, int] = {}
    for rep in repairs:
        ok, length = viable(rep, initial, successors, terminal, node_budget)
        if ok and length is not None:
            viable_map[rep] = length
    # console.log REACH-09: count complete.
    print(
        "[phase1:reachability] count_viable_first_repairs: complete viable=%d/%d."
        % (len(viable_map), len(repairs))
    )
    return len(viable_map), viable_map
