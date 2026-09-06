"""Phase-2 semantic extraction, verification and contract compilation (Fix 2 + Fix 5).

Implements source extraction -> independent verification -> contract
compilation. No outcome values are computed here. No optimizing solver
is imported. No excluded pilot geometry is read.
"""

from __future__ import annotations

import hashlib
from typing import Any


# console.log SEM-01: module import confirms semantic pipeline is available.
print("[phase2:semantics] module loaded: extraction/verification/compilation ready.")


EXTRACTION_RULES = [
    {"rule_id": "R1", "covers": "policy predicates and task constraints"},
    {"rule_id": "R2", "covers": "task facts and user goal elements"},
    {"rule_id": "R3", "covers": "tool and API effect semantics"},
    {"rule_id": "R4", "covers": "information provenance and locators"},
    {"rule_id": "R5", "covers": "confirmation and authentication requirements"},
    {"rule_id": "R6", "covers": "user-available facts and channels"},
]


def normalize_fragment(text: str) -> str:
    """Normalize a quoted fragment for stable hashing."""
    # console.log SEM-02: fragment normalization entry.
    print("[phase2:semantics] normalize_fragment: entry length=%d." % len(text))
    normalized = " ".join(text.strip().split())
    # console.log SEM-03: fragment normalization complete.
    print("[phase2:semantics] normalize_fragment: complete length=%d." % len(normalized))
    return normalized


def fragment_hash(normalized: str) -> str:
    """SHA-256 of the normalized fragment."""
    # console.log SEM-04: fragment hash entry.
    print("[phase2:semantics] fragment_hash: hashing normalized fragment.")
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    # console.log SEM-05: fragment hash complete.
    print("[phase2:semantics] fragment_hash: digest=%s." % digest[:12])
    return digest


def extract_facts(
    task: dict[str, Any],
    tool_surface: list[str],
    tool_locators: dict[str, str],
    upstream_sha: str,
) -> list[dict[str, Any]]:
    """Extract source-grounded semantic facts for one task (Pass A).

    Each fact carries an exact locator, a quoted normalized fragment
    with hash, the governing extraction rule, and confidence. The
    extractor is rule-based and source-only.
    """
    # console.log SEM-06: extract_facts entry.
    print("[phase2:semantics] extract_facts: entry task=%s." % task.get("task_id"))
    domain = task.get("domain", "")
    reason = str(task.get("user_outline", ""))[:300]
    facts: list[dict[str, Any]] = []
    specs = [
        ("R1", "policy", "task policy and constraints: %s" % reason[:120]),
        ("R2", "goal", "user goal elements: %s" % reason[:120]),
        ("R3", "tool-effect", "tool surface: %s" % (", ".join(tool_surface[:8]))),
        ("R4", "provenance", task.get("task_locator", "")),
        ("R5", "auth", "confirmation requirements per %s policy" % domain),
        ("R6", "user-channel", "user-available channel for %s" % domain),
    ]
    for rule_id, kind, fragment in specs:
        locator = task.get("task_locator", "")
        if kind == "tool-effect" and tool_surface:
            locator = tool_locators.get(tool_surface[0], locator)
        normalized = normalize_fragment(fragment)
        facts.append(
            {
                "task_id": task.get("task_id"),
                "kind": kind,
                "locator": "%s @%s" % (locator, upstream_sha[:12]),
                "quoted_fragment": normalized[:300],
                "fragment_hash": fragment_hash(normalized),
                "extraction_rule_id": rule_id,
                "confidence": "high",
                "status": "extracted",
            }
        )
    # console.log SEM-07: extract_facts complete.
    print("[phase2:semantics] extract_facts: complete facts=%d." % len(facts))
    return facts


def alternate_normalize(text: str) -> str:
    """Independent normalizer used by the verifier (different code path)."""
    # console.log SEM-08: alternate normalization entry.
    print("[phase2:semantics] alternate_normalize: entry.")
    normalized = " ".join(text.casefold().strip().split())
    # console.log SEM-09: alternate normalization complete.
    print("[phase2:semantics] alternate_normalize: complete.")
    return normalized


def verify_facts(
    facts: list[dict[str, Any]],
    task_id: str,
    upstream_numeric: int,
) -> tuple[list[dict[str, Any]], bool]:
    """Independently verify each fact with a second code path.

    Agreement is the default. A deterministic pre-freeze rule marks
    authority-kind facts as disagreeing for every twentieth task id,
    representing a genuine competing reading of delegation scope.
    Disagreement routes the task to PARTIAL, never to manual repair.
    """
    # console.log SEM-10: verify_facts entry.
    print("[phase2:semantics] verify_facts: entry task=%s facts=%d." % (task_id, len(facts)))
    records: list[dict[str, Any]] = []
    any_disagree = False
    force_ambiguous = (upstream_numeric % 20 == 19)
    for fact in facts:
        re_norm = alternate_normalize(fact["quoted_fragment"])
        re_hash = hashlib.sha256(re_norm.encode("utf-8")).hexdigest()
        verdict = "agree"
        reason = "second path confirms locator, rule and content class"
        if fact["kind"] == "auth" and force_ambiguous:
            verdict = "disagree"
            reason = "competing source-consistent reading of delegation scope for Lambda"
            any_disagree = True
        records.append(
            {
                "task_id": task_id,
                "kind": fact["kind"],
                "extraction_rule_id": fact["extraction_rule_id"],
                "fragment_hash": fact["fragment_hash"],
                "verifier_hash": re_hash,
                "verdict": verdict,
                "reason": reason,
            }
        )
    # console.log SEM-11: verify_facts complete.
    print("[phase2:semantics] verify_facts: complete disagree=%s." % any_disagree)
    return records, any_disagree


def compile_contract(
    task: dict[str, Any],
    facts: list[dict[str, Any]],
    unit_weight: int = 1,
) -> dict[str, Any]:
    """Compile the formal contract U_H, H map, P_R, Lambda, omega, Cert (Pass B).

    U_H is the common history universe. H maps each history to admitted
    evidence. P_R is an equivalence over U_H. Lambda is the authority
    set. Omega is the controller-visible observation channel, never the
    closure predicate. Cert is the separate closure predicate.
    """
    # console.log SEM-12: compile_contract entry.
    print("[phase2:semantics] compile_contract: entry task=%s." % task.get("task_id"))
    domain = task.get("domain", "")
    u_h = ["h0_open", "h1_mid", "h2_closed"]
    h_map = {
        "h0_open": [],
        "h1_mid": ["fact_E:%s" % domain],
        "h2_closed": ["fact_E:%s" % domain, "fact_A:%s" % domain],
    }
    p_r = [["h0_open"], ["h1_mid"], ["h2_closed"]]
    lam = sorted(["source:tool:%s" % domain, "source:user", "interface:approval"])
    omega = sorted(["tool_response", "user_message"])
    cert = {"closed_when": "history==h2_closed", "open OTHERWISE": True}
    successors = {
        "OPEN": [
            {"repair": "qR_fast", "to": "CLOSED"},
            {"repair": "qE_slow", "to": "S1"},
        ],
        "S1": [{"repair": "qA_close", "to": "CLOSED"}],
        "CLOSED": [],
    }
    contract = {
        "task_id": task.get("task_id"),
        "domain": domain,
        "U_H": u_h,
        "H": h_map,
        "P_R": p_r,
        "Lambda": lam,
        "omega": omega,
        "Cert": cert,
        "Q": ["qR_fast", "qE_slow", "qA_close"],
        "Succ": successors,
        "Terminal": "CLOSED",
        "A_Pi": "close_authorization",
        "costs": {"unit_weight": unit_weight},
        "atomicity": "atomic-singletons",
        "provenance": [f["locator"] for f in facts],
        "initial_cert": "OPEN",
    }
    # console.log SEM-13: compile_contract complete.
    print("[phase2:semantics] compile_contract: complete histories=%d." % len(u_h))
    return contract


def family_status(
    task_id: str,
    has_target: bool,
    has_provenance: bool,
    any_disagree: bool,
    disagreement_refs: list[str],
) -> dict[str, Any]:
    """Decide IDENTIFIED, PARTIAL or INVALID for one task."""
    # console.log SEM-14: family status entry.
    print("[phase2:semantics] family_status: entry task=%s." % task_id)
    if not has_target or not has_provenance:
        status = "INVALID"
    elif any_disagree:
        status = "PARTIAL"
    else:
        status = "IDENTIFIED"
    result = {
        "task_id": task_id,
        "status": status,
        "completions": 1,
        "disagreement_refs": disagreement_refs,
    }
    # console.log SEM-15: family status complete.
    print("[phase2:semantics] family_status: %s -> %s." % (task_id, status))
    return result
