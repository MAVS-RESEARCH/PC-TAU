"""Audit layer: metric recomputation from raw trajectories (independent text)."""

from __future__ import annotations

from typing import Any


# console.log AUDR-01: module import confirms run audit is available.
print("[audit:run] module loaded.")


def recompute_episode(
    repairs: list[str],
    escalated: bool,
    violations: int,
    kappa: int | None,
    tied: list[str],
    preferred: str | None,
) -> dict[str, Any]:
    """Recompute the seven metrics for one episode without production code."""
    # console.log AUDR-02: episode recompute entry.
    print("[audit:run] recompute_episode: entry.")
    finite = kappa is not None
    found = bool(repairs) and finite
    optimal = bool(repairs) and finite and repairs[0] in tied and len(repairs) == kappa
    if not finite:
        adapted = escalated
    elif not repairs:
        adapted = False
    elif preferred is None:
        adapted = found
    else:
        adapted = found and repairs[0] != preferred
    record = {
        "route_discovery": found,
        "optimal_route": optimal,
        "freeze_adaptation": adapted,
        "excess_escalation": escalated and finite,
        "unsafe_attempts": violations,
        "governance_correct": (bool(repairs) and finite) or (escalated and not finite),
        "repair_regret": (len(repairs) - kappa) if (repairs and finite) else None,
    }
    # console.log AUDR-03: episode recompute complete.
    print("[audit:run] recompute_episode: complete.")
    return record
