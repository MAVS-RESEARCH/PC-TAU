"""Phase-3 eight-cell freeze lattice with same-instance manifests."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from pc_tau.planner import INF, solve


# console.log FRZ-01: module import confirms freeze lattice is available.
print("[phase3:freeze] module loaded: eight-cell lattice ready.")


CELLS = ["F000", "F100", "F010", "F001", "F110", "F101", "F011", "F111"]

MASKS: dict[str, set[str]] = {
    "F000": set(),
    "F100": {"E"},
    "F010": {"R"},
    "F001": {"A"},
    "F110": {"E", "R"},
    "F101": {"E", "A"},
    "F011": {"R", "A"},
    "F111": {"E", "R", "A"},
}


def canonical(obj: Any) -> str:
    """Canonical JSON encoding for stable hashing."""
    # console.log FRZ-02: canonical encoding entry.
    print("[phase3:freeze] canonical: serializing object.")
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    # console.log FRZ-03: canonical encoding complete.
    print("[phase3:freeze] canonical: complete length=%d." % len(text))
    return text


def apply_mask(
    successors: dict[str, list[dict[str, Any]]],
    touches: dict[str, set[str]],
    frozen: set[str],
) -> dict[str, list[dict[str, Any]]]:
    """Retain a repair iff its touch set is disjoint from the frozen set.

    Composite touches are atomic: any overlap removes the repair unless
    the source exposes an independent subaction, which the template
    source does not.
    """
    # console.log FRZ-04: mask application entry.
    print("[phase3:freeze] apply_mask: entry frozen=%s." % sorted(frozen))
    masked: dict[str, list[dict[str, Any]]] = {}
    for state, edges in successors.items():
        masked[state] = [
            e for e in edges if set(touches.get(e.get("repair", ""), set())).isdisjoint(frozen)
        ]
    # console.log FRZ-05: mask application complete.
    print("[phase3:freeze] apply_mask: retained=%d." % sum(len(v) for v in masked.values()))
    return masked


def classify(kappa: Any, kappa_r: Any) -> str:
    """Classify the R relation for one task."""
    # console.log FRZ-06: classification entry.
    print("[phase3:freeze] classify: entry.")
    if isinstance(kappa, int) and isinstance(kappa_r, int):
        result = "ZERO" if kappa_r == kappa else "FINITE_POSITIVE"
    elif isinstance(kappa, int) and kappa_r is INF:
        result = "STRUCTURAL"
    else:
        result = "UNDERIDENTIFIED"
    # console.log FRZ-07: classification complete.
    print("[phase3:freeze] classify: result=%s." % result)
    return result


def lattice(
    task_id: str,
    successors: dict[str, list[dict[str, Any]]],
    touches: dict[str, set[str]],
    initial: str,
    terminal: str,
) -> dict[str, Any]:
    """Evaluate all eight cells with same-instance manifests.

    The base instance is hashed once; each masked view is hashed. Only
    the forbidden-resource mask differs within the group.
    """
    # console.log FRZ-08: lattice entry.
    print("[phase3:freeze] lattice: entry task=%s." % task_id)
    base_hash = hashlib.sha256(
        canonical({"successors": successors, "initial": initial, "terminal": terminal}).encode(
            "utf-8"
        )
    ).hexdigest()
    cells: dict[str, Any] = {}
    for cell in CELLS:
        masked = apply_mask(successors, touches, MASKS[cell])
        view_hash = hashlib.sha256(canonical(masked).encode("utf-8")).hexdigest()
        solved = solve(masked, initial, terminal)
        cells[cell] = {
            "kappa": ("INF" if solved["kappa"] is INF else solved["kappa"]),
            "tied_optimal_initial_repairs": solved["tied_optimal_initial_repairs"],
            "branch_cost": ("INF" if solved["branch_cost"] is INF else solved["branch_cost"]),
            "terminal_status": solved["terminal_status"],
            "certificate": solved["certificate"],
            "mask": sorted(MASKS[cell]),
            "view_hash": view_hash,
        }
    # console.log FRZ-09: all cells evaluated.
    print("[phase3:freeze] lattice: evaluated 8 cells task=%s." % task_id)
    k0 = cells["F000"]["kappa"]
    kr = cells["F010"]["kappa"]
    ke = cells["F100"]["kappa"]
    r_class = classify(
        None if k0 == "INF" else k0,
        INF if kr == "INF" else kr,
    )
    if isinstance(k0, int) and isinstance(kr, int):
        delta_r: Any = kr - k0
        fallback_premium_r: Any = kr - k0
    else:
        delta_r = None
        fallback_premium_r = None
    finite = lambda v: isinstance(v, int)
    interactions = {
        "er_complementary": bool(finite(k0) and ke == "INF" and kr == "INF"),
        "r_zero": bool(finite(k0) and finite(kr) and kr == k0),
        "r_finite_substitution": bool(finite(k0) and finite(kr) and kr > k0),
        "r_structural": bool(finite(k0) and kr == "INF"),
    }
    # console.log FRZ-10: R classification complete.
    print("[phase3:freeze] lattice: task=%s class=%s." % (task_id, r_class))
    return {
        "task_id": task_id,
        "base_hash": base_hash,
        "cells": cells,
        "delta_r": delta_r,
        "r_class": r_class,
        "fallback_premium_r": fallback_premium_r,
        "route_diversity": len(touches),
        "interactions": interactions,
    }
