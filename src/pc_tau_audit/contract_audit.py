"""Audit layer: independent contract rebuild from verified source facts."""

from __future__ import annotations

from typing import Any


# console.log AUDC-01: module import confirms contract audit is available.
print("[audit:contract] module loaded.")


def rebuild_histories(domain: str) -> tuple[list[str], dict[str, list[str]]]:
    """Rebuild the history universe and admission map (separate text)."""
    # console.log AUDC-02: history rebuild entry.
    print("[audit:contract] rebuild_histories: entry domain=%s." % domain)
    universe = ["h0_open", "h1_mid", "h2_closed"]
    admitted = {
        "h0_open": [],
        "h1_mid": ["fact_E:%s" % domain],
        "h2_closed": ["fact_E:%s" % domain, "fact_A:%s" % domain],
    }
    # console.log AUDC-03: history rebuild complete.
    print("[audit:contract] rebuild_histories: complete.")
    return universe, admitted


def rebuild_equivalence() -> list[list[str]]:
    """Rebuild the representation equivalence over the universe."""
    # console.log AUDC-04: equivalence rebuild entry.
    print("[audit:contract] rebuild_equivalence: entry.")
    classes = [["h0_open"], ["h1_mid"], ["h2_closed"]]
    # console.log AUDC-05: equivalence rebuild complete.
    print("[audit:contract] rebuild_equivalence: complete.")
    return classes


def rebuild_contract(task_id: str, domain: str, provenance: list[str]) -> dict[str, Any]:
    """Rebuild one contract with Fix-5 types (independent implementation)."""
    # console.log AUDC-06: contract rebuild entry.
    print("[audit:contract] rebuild_contract: entry task=%s." % task_id)
    universe, admitted = rebuild_histories(domain)
    contract = {
        "task_id": task_id,
        "domain": domain,
        "U_H": universe,
        "H": admitted,
        "P_R": rebuild_equivalence(),
        "Lambda": sorted(["interface:approval", "source:tool:%s" % domain, "source:user"]),
        "omega": sorted(["tool_response", "user_message"]),
        "Cert": {"closed_when": "history==h2_closed", "open OTHERWISE": True},
        "Q": ["qR_fast", "qE_slow", "qA_close"],
        "Succ": {
            "OPEN": [{"repair": "qR_fast", "to": "CLOSED"}, {"repair": "qE_slow", "to": "S1"}],
            "S1": [{"repair": "qA_close", "to": "CLOSED"}],
            "CLOSED": [],
        },
        "Terminal": "CLOSED",
        "A_Pi": "close_authorization",
        "initial_cert": "OPEN",
        "provenance": list(provenance),
    }
    # console.log AUDC-07: contract rebuild complete.
    print("[audit:contract] rebuild_contract: complete.")
    return contract


def rebuild_family(task_id: str, disagreements: list[str], has_provenance: bool) -> str:
    """Re-derive family status from verification verdicts."""
    # console.log AUDC-08: family rebuild entry.
    print("[audit:contract] rebuild_family: entry task=%s." % task_id)
    if not has_provenance:
        status = "INVALID"
    elif disagreements:
        status = "PARTIAL"
    else:
        status = "IDENTIFIED"
    # console.log AUDC-09: family rebuild complete.
    print("[audit:contract] rebuild_family: status=%s." % status)
    return status
