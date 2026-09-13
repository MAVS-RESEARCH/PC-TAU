"""Audit layer: independent touch recomputation from successor semantics."""

from __future__ import annotations

from typing import Any


# console.log AUDT2-01: module import confirms touch audit is available.
print("[audit:touch] module loaded.")


def canonical(classes: list[list[str]]) -> list[list[str]]:
    """Canonicalize an equivalence family (independent text)."""
    # console.log AUDT2-02: canonicalization entry.
    print("[audit:touch] canonical: entry.")
    result = sorted([sorted(group) for group in classes])
    # console.log AUDT2-03: canonicalization complete.
    print("[audit:touch] canonical: complete.")
    return result


def recompute(
    pre_h: list[str],
    pre_p: list[list[str]],
    pre_l: list[str],
    post_h: list[str],
    post_p: list[list[str]],
    post_l: list[str],
) -> set[str]:
    """Recompute the resource set from snapshot differences."""
    # console.log AUDT2-04: recompute entry.
    print("[audit:touch] recompute: entry.")
    touched: set[str] = set()
    if sorted(pre_h) != sorted(post_h):
        touched.add("E")
    if canonical(pre_p) != canonical(post_p):
        touched.add("R")
    if sorted(pre_l) != sorted(post_l):
        touched.add("A")
    # console.log AUDT2-05: recompute complete.
    print("[audit:touch] recompute: touch=%s." % sorted(touched))
    return touched


def snapshots(domain: str) -> dict[str, dict[str, Any]]:
    """Rebuild per-state governance snapshots (independent text)."""
    # console.log AUDT2-06: snapshot rebuild entry.
    print("[audit:touch] snapshots: entry domain=%s." % domain)
    base = [["h0_open"], ["h1_mid"], ["h2_closed"]]
    exposed = [["h0_open", "h1_mid"], ["h2_closed"]]
    authority = sorted(["source:tool:%s" % domain, "source:user"])
    result = {
        "OPEN": {"H": [], "P_R": base, "Lambda": authority},
        "S1": {"H": ["fact_E:%s" % domain], "P_R": base, "Lambda": authority},
        "CLOSED_R": {"H": [], "P_R": exposed, "Lambda": authority},
        "CLOSED_A": {
            "H": ["fact_E:%s" % domain],
            "P_R": base,
            "Lambda": sorted(authority + ["interface:approval"]),
        },
    }
    # console.log AUDT2-07: snapshot rebuild complete.
    print("[audit:touch] snapshots: complete.")
    return result
