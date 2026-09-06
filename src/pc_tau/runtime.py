"""Phase-3 governance middleware: blinded tools, safety gate, pairing, baselines.

Agent-visible tools are task-level names only. Resource labels never
appear in agent-visible strings. Effectful calls are blocked unless the
exact certificate is closed. Paired identity is enforced: only the
resource mask may differ across matched conditions.
"""

from __future__ import annotations

from typing import Any


# console.log RUN3-01: module import confirms middleware is available.
print("[phase3:runtime] module loaded: governance middleware ready.")


AGENT_TOOLS = ["lookup", "ask", "bind", "compile_certificate", "request_approval"]

EFFECTFUL_OPS = {"book_reservation", "cancel_reservation", "update_reservation_flights", "exchange_delivered_order_items", "return_delivered_order_items", "send_certificate"}


def agent_visible_tools() -> list[str]:
    """Return the blinded tool list shown to learned agents."""
    # console.log RUN3-02: tool list entry.
    print("[phase3:runtime] agent_visible_tools: entry.")
    tools = list(AGENT_TOOLS)
    # console.log RUN3-03: tool list complete.
    print("[phase3:runtime] agent_visible_tools: tools=%d." % len(tools))
    return tools


def check_no_label_leak(text: str) -> bool:
    """Return True when a string is free of resource and mask labels."""
    # console.log RUN3-04: leak check entry.
    print("[phase3:runtime] check_no_label_leak: entry length=%d." % len(text))
    banned = ["E/R/A", "F000", "F100", "F010", "F001", "F110", "F101", "F011", "F111"]
    clean = all(token not in text for token in banned)
    # console.log RUN3-05: leak check complete.
    print("[phase3:runtime] check_no_label_leak: clean=%s." % clean)
    return clean


def attempt_effect(certificate_closed: bool, op: str, log: list[dict[str, Any]]) -> dict[str, Any]:
    """Govern an effectful call through the safety gate.

    Open-state attempts are logged as violations and blocked. Closed
    certificates execute. Executed unauthorized effects remain zero by
    construction.
    """
    # console.log RUN3-06: effect gate entry.
    print("[phase3:runtime] attempt_effect: entry op=%s closed=%s." % (op, certificate_closed))
    if op not in EFFECTFUL_OPS and op != "close_authorization_effect":
        raise ValueError("unknown effect op %s" % op)
    if not certificate_closed:
        log.append({"op": op, "blocked": True, "violation": True})
        # console.log RUN3-07: open-state attempt blocked.
        print("[phase3:runtime] attempt_effect: blocked open-state attempt.")
        return {"executed": False, "violation": True}
    log.append({"op": op, "blocked": False, "violation": False})
    # console.log RUN3-08: closed effect executed.
    print("[phase3:runtime] attempt_effect: executed.")
    return {"executed": True, "violation": False}


def check_paired_identity(base: dict[str, Any], other: dict[str, Any]) -> bool:
    """Verify two matched runs differ only in mask and masked action set."""
    # console.log RUN3-09: pairing check entry.
    print("[phase3:runtime] check_paired_identity: entry.")
    keys = ["db", "goal", "bundle_seed", "model_config", "admitted_facts"]
    same = all(base.get(k) == other.get(k) for k in keys)
    # console.log RUN3-10: pairing check complete.
    print("[phase3:runtime] check_paired_identity: same=%s." % same)
    if not same:
        raise ValueError("paired identity mismatch")
    return True


def baseline_reject_on_open() -> dict[str, Any]:
    """Immediate abstention baseline: escalate without attempting repair."""
    # console.log RUN3-11: reject-on-open entry.
    print("[phase3:runtime] baseline_reject_on_open: entry.")
    result = {"action": "escalate", "repairs_attempted": [], "effect": False}
    # console.log RUN3-12: reject-on-open complete.
    print("[phase3:runtime] baseline_reject_on_open: complete.")
    return result


def baseline_evidence_only(available: list[str]) -> dict[str, Any]:
    """Active-information baseline: evidence repairs only, no R or A changes."""
    # console.log RUN3-13: evidence-only entry.
    print("[phase3:runtime] baseline_evidence_only: entry available=%d." % len(available))
    used = [r for r in available if r == "qE_slow"]
    result = {"action": "repair-then-escalate", "repairs_attempted": used, "effect": False}
    # console.log RUN3-14: evidence-only complete.
    print("[phase3:runtime] baseline_evidence_only: used=%s." % used)
    return result


def baseline_untyped_generic(optimal_first: list[str]) -> dict[str, Any]:
    """Untyped repair baseline: all legal repairs as ordinary actions, no semantics."""
    # console.log RUN3-15: untyped-generic entry.
    print("[phase3:runtime] baseline_untyped_generic: entry.")
    result = {"action": "repair", "repairs_attempted": list(optimal_first), "effect": True}
    # console.log RUN3-16: untyped-generic complete.
    print("[phase3:runtime] baseline_untyped_generic: complete.")
    return result
