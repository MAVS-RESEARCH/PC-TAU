"""Phase-3 metrics: exact summaries plus paired learned-agent behavior.

Seven agent metrics against the exact oracle. Statistics use paired
task-level differences with bootstrap confidence intervals over tasks.
Exact signatures carry no confidence intervals. Tracks are reported
separately and stratified by regime and family, never collapsed.
"""

from __future__ import annotations

import random
from typing import Any


# console.log MET-01: module import confirms metrics are available.
print("[phase3:metrics] module loaded: paired metrics ready.")


def repair_regret(agent_steps: int | None, kappa: int | None) -> int | None:
    """Agent repair steps minus exact kappa for finite cases only."""
    # console.log MET-02: regret entry.
    print("[phase3:metrics] repair_regret: entry agent=%s kappa=%s." % (agent_steps, kappa))
    if agent_steps is None or kappa is None:
        # console.log MET-03: regret undefined for non-finite case.
        print("[phase3:metrics] repair_regret: undefined (non-finite).")
        return None
    result = agent_steps - kappa
    # console.log MET-04: regret complete.
    print("[phase3:metrics] repair_regret: result=%d." % result)
    return result


def bootstrap_mean_ci(
    values: list[float], seed: int = 0, resamples: int = 1000, level: float = 0.95
) -> dict[str, float]:
    """Bootstrap confidence interval over tasks (not seeds)."""
    # console.log MET-05: bootstrap entry.
    print("[phase3:metrics] bootstrap_mean_ci: entry n=%d." % len(values))
    if not values:
        return {"mean": 0.0, "lo": 0.0, "hi": 0.0}
    rng = random.Random(seed)
    mean = sum(values) / len(values)
    draws: list[float] = []
    for _ in range(resamples):
        sample = [rng.choice(values) for _ in values]
        draws.append(sum(sample) / len(sample))
    draws.sort()
    alpha = 1.0 - level
    lo = draws[int((alpha / 2) * resamples)]
    hi = draws[int((1 - alpha / 2) * resamples) - 1]
    # console.log MET-06: bootstrap complete.
    print("[phase3:metrics] bootstrap_mean_ci: mean=%.4f." % mean)
    return {"mean": mean, "lo": lo, "hi": hi}


def summarize_episode(
    found_closer: bool,
    followed_optimal: bool,
    adapted: bool,
    escalated: bool,
    finite_closer_exists: bool,
    unsafe_attempts: int,
    governance_correct: bool,
    regret: int | None,
) -> dict[str, Any]:
    """Pack one episode into the seven-metric record."""
    # console.log MET-07: episode summary entry.
    print("[phase3:metrics] summarize_episode: entry.")
    record = {
        "route_discovery": found_closer,
        "optimal_route": followed_optimal,
        "freeze_adaptation": adapted,
        "excess_escalation": escalated and finite_closer_exists,
        "unsafe_attempts": unsafe_attempts,
        "governance_correct": governance_correct,
        "repair_regret": regret,
    }
    # console.log MET-08: episode summary complete.
    print("[phase3:metrics] summarize_episode: complete.")
    return record
