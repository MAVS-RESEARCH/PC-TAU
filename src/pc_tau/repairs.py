"""Phase-2 source-grounded legal repair extraction (no manual labels)."""

from __future__ import annotations

from typing import Any


# console.log REP-01: module import confirms repair extraction is available.
print("[phase2:repairs] module loaded: legal repair extraction ready.")


REPAIR_JUSTIFICATIONS = {
    "qR_fast": "compute-only over already-admitted history; no external query",
    "qE_slow": "read-only acquisition of an admitted fact via task tool",
    "qA_close": "delegation change without adding a new world fact",
}


def legal_repairs(
    contract: dict[str, Any],
    tool_locators: dict[str, str],
) -> list[dict[str, Any]]:
    """Extract legal repairs with preconditions, successors and justifications.

    Atomicity is preserved: each repair is an atomic singleton. No
    composite is split unless the source exposes a subaction, which the
    template source does not. Each repair exists for a source reason
    independent of any outcome value.
    """
    # console.log REP-02: legal_repairs entry.
    print(
        "[phase2:repairs] legal_repairs: entry task=%s." % contract.get("task_id")
    )
    domain = contract.get("domain", "")
    successors: dict[str, list[dict[str, Any]]] = contract.get("Succ", {})
    repairs: list[dict[str, Any]] = []
    preconditions = {"qR_fast": "OPEN", "qE_slow": "OPEN", "qA_close": "S1"}
    for name in contract.get("Q", []):
        targets = [e["to"] for e in successors.get(preconditions[name], []) if e["repair"] == name]
        repairs.append(
            {
                "task_id": contract.get("task_id"),
                "repair": name,
                "precondition": preconditions[name],
                "successors": targets,
                "justification": "%s; tool %s; domain %s"
                % (REPAIR_JUSTIFICATIONS[name], tool_locators.get(name, domain), domain),
                "locator": tool_locators.get(name, contract.get("domain", "")),
                "atomic": True,
                "reads_external": False,
                "reads_unadmitted": False,
                "alters_mapping": False,
                "adds_fact": (name == "qE_slow"),
            }
        )
    # console.log REP-03: legal_repairs complete.
    print("[phase2:repairs] legal_repairs: complete repairs=%d." % len(repairs))
    return repairs
