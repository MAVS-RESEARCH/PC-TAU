"""Fix-1 provisional pilot-only closure solver (throwaway, never scientific).

Namespace is intentionally isolated as pilot_provisional_*. No module
outside Phase-1 pilot code may import this file. Results are tagged
provisional and excluded, confined to results/<run_id>/pilot/.
"""

from __future__ import annotations

from collections import deque
from typing import Any


# console.log PROV-01: provisional solver module loaded (pilot-only).
print("[phase1:pilot-provisional] module loaded: throwaway closure solver ready.")


def pilot_provisional_solve(
    successors: dict[str, list[dict[str, Any]]],
    touches: dict[str, set[str]],
    initial: str,
    terminal: str,
    frozen: set[str],
    node_budget: int = 1000,
) -> dict[str, Any]:
    """Minimal-step closure under a frozen-resource mask (unit step weight).

    A repair is retained iff its derived contact set is disjoint from
    the frozen set. Returns minimal steps (None for unreachable),
    optimal first repairs, and a witness path. Unreachable is
    structural, represented as None rather than a numeric sentinel.
    """
    # console.log PROV-02: provisional solve entry.
    print(
        "[phase1:pilot-provisional] solve: entry frozen=%s initial=%s."
        % (sorted(frozen), initial)
    )
    allowed: dict[str, list[dict[str, Any]]] = {}
    for state, edges in successors.items():
        kept = [
            e
            for e in edges
            if set(touches.get(e.get("repair", ""), set())).isdisjoint(frozen)
        ]
        allowed[state] = kept
    # console.log PROV-03: freeze mask applied to repair set.
    print("[phase1:pilot-provisional] solve: mask applied, states=%d." % len(allowed))
    queue: deque[tuple[str, list[str]]] = deque([(initial, [])])
    seen: dict[str, int] = {initial: 0}
    best: list[str] | None = None
    expanded = 0
    while queue:
        state, path = queue.popleft()
        expanded += 1
        if expanded > node_budget:
            break
        for edge in allowed.get(state, []):
            nxt = edge.get("to")
            npath = path + [edge.get("repair", "")]
            if nxt == terminal:
                if best is None or len(npath) < len(best):
                    best = npath
                continue
            if nxt not in seen or len(npath) < seen[nxt]:
                seen[nxt] = len(npath)
                queue.append((nxt, npath))
    # console.log PROV-04: provisional search complete.
    print(
        "[phase1:pilot-provisional] solve: complete expanded=%d found=%s."
        % (expanded, best is not None)
    )
    if best is None:
        return {
            "steps": None,
            "optimal_first": [],
            "witness": None,
            "expanded": expanded,
        }
    first_options = sorted({e.get("repair", "") for e in allowed.get(initial, [])})
    optimal_first: list[str] = []
    for rep in first_options:
        queue2: deque[tuple[str, list[str]]] = deque()
        for e in allowed.get(initial, []):
            if e.get("repair") == rep:
                queue2.append((e.get("to"), [rep]))
        found = False
        seen2: set[str] = set()
        while queue2:
            st, pth = queue2.popleft()
            if st == terminal and len(pth) == len(best):
                found = True
                break
            if len(pth) >= len(best):
                continue
            for e in allowed.get(st, []):
                queue2.append((e.get("to"), pth + [e.get("repair", "")]))
        if found:
            optimal_first.append(rep)
    # console.log PROV-05: optimal first repairs enumerated.
    print(
        "[phase1:pilot-provisional] solve: optimal_first=%s steps=%d."
        % (",".join(sorted(optimal_first)), len(best))
    )
    return {
        "steps": len(best),
        "optimal_first": sorted(optimal_first),
        "witness": best,
        "expanded": expanded,
    }
