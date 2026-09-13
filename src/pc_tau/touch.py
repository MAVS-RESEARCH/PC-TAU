"""Phase-2 mechanical touch derivation (derived, never authored)."""

from __future__ import annotations

from typing import Any


# console.log TCH-01: module import confirms touch derivation is available.
print("[phase2:touch] module loaded: mechanical touch derivation ready.")


def canonical_classes(classes: list[list[str]]) -> list[list[str]]:
    """Canonicalize an equivalence family for stable comparison."""
    # console.log TCH-02: canonicalization entry.
    print("[phase2:touch] canonical_classes: entry classes=%d." % len(classes))
    result = sorted([sorted(c) for c in classes])
    # console.log TCH-03: canonicalization complete.
    print("[phase2:touch] canonical_classes: complete.")
    return result


def derive_touch(
    pre_h: list[str],
    pre_p: list[list[str]],
    pre_l: list[str],
    post_h: list[str],
    post_p: list[list[str]],
    post_l: list[str],
    repair_meta: dict[str, Any] | None = None,
) -> set[str]:
    """Derive the resource set from successor semantics.

    E iff admitted history changes. R iff the P_R equivalence changes.
    A iff Lambda changes. Any manual label field raises. Operational
    violations raise: R reading external, E altering mapping, A adding
    a world fact.
    """
    # console.log TCH-04: derive_touch entry.
    print("[phase2:touch] derive_touch: entry.")
    meta = repair_meta or {}
    if "resource_label" in meta or "touch" in meta:
        # console.log TCH-05: manual label rejected.
        print("[phase2:touch] derive_touch: manual label rejected.")
        raise ValueError("manual resource labels are forbidden")
    touch: set[str] = set()
    if sorted(pre_h) != sorted(post_h):
        touch.add("E")
    if canonical_classes(pre_p) != canonical_classes(post_p):
        touch.add("R")
    if sorted(pre_l) != sorted(post_l):
        touch.add("A")
    name = str(meta.get("repair", ""))
    flag_e = set(touch) == {"E"}
    flag_r = set(touch) == {"R"}
    flag_a = set(touch) == {"A"}
    if flag_r and (meta.get("reads_external") or meta.get("reads_unadmitted")):
        # console.log TCH-06: R firewall violation rejected.
        print("[phase2:touch] derive_touch: R firewall violation.")
        raise ValueError("%s: R repair must not read external state" % name)
    if flag_e and meta.get("alters_mapping"):
        # console.log TCH-07: E firewall violation rejected.
        print("[phase2:touch] derive_touch: E firewall violation.")
        raise ValueError("%s: E repair must not alter mapping" % name)
    if flag_a and meta.get("adds_fact"):
        # console.log TCH-08: A firewall violation rejected.
        print("[phase2:touch] derive_touch: A firewall violation.")
        raise ValueError("%s: A repair must not add world fact" % name)
    # console.log TCH-09: derive_touch complete.
    print("[phase2:touch] derive_touch: complete touch=%s." % sorted(touch))
    return touch
