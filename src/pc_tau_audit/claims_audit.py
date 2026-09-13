"""Audit layer: predicate ledger and paper-language verification (no keyword lists)."""

from __future__ import annotations

from typing import Any


# console.log AUDCL-01: module import confirms claims audit is available.
print("[audit:claims] module loaded.")


EXPECTED_SENTENCES = {
    "finite_substitution_constructed_authorized": "Finite resource substitution occurs in the sealed constructed contracts (finite positive fallback premium under a resource freeze).",
    "controlled_regime_authorized": "The controlled panel reproduces the predicted zero, finite, structural and complementarity mechanisms (balanced by design).",
    "typing_invariance_authorized": "Resource typing is invariant under the frozen harmless-refactoring class for retained tasks.",
}

PERMANENT = [
    "prevalence_claim_authorized",
    "superiority_claim_authorized",
    "deployment_safety_claim_authorized",
    "natural_frequency_from_track_f",
    "planner_expressiveness_claim_authorized",
]


def verify_ledger(ledger: dict[str, Any]) -> tuple[bool, list[str]]:
    """Verify predicate discipline: booleans, permanent false, evidence-backed flips."""
    # console.log AUDCL-02: ledger verification entry.
    print("[audit:claims] verify_ledger: entry.")
    problems: list[str] = []
    predicates = ledger.get("predicates", {})
    for name in PERMANENT:
        if predicates.get(name) is not False:
            problems.append("%s not permanently false" % name)
    for name, value in predicates.items():
        if not isinstance(value, bool):
            problems.append("%s not boolean" % name)
        if value is True and name not in EXPECTED_SENTENCES:
            problems.append("%s true without known sentence" % name)
        if value is True and name not in ledger.get("evidence", {}):
            problems.append("%s true without evidence pointer" % name)
    # console.log AUDCL-03: ledger verification complete.
    print("[audit:claims] verify_ledger: problems=%d." % len(problems))
    return (not problems, problems)


def expected_claims_text(ledger: dict[str, Any]) -> str:
    """Rebuild the expected CLAIMS.md from true predicates (separate text)."""
    # console.log AUDCL-04: expectation rebuild entry.
    print("[audit:claims] expected_claims_text: entry.")
    lines = ["# Sealed claims (evidence-derived predicates)", ""]
    for name in [
        "multiroute_existence_authorized",
        "finite_substitution_natural_authorized",
        "finite_substitution_constructed_authorized",
        "imperfect_adaptation_authorized",
        "learned_agent_evidence_authorized",
        "controlled_regime_authorized",
        "typing_invariance_authorized",
        "prevalence_claim_authorized",
        "superiority_claim_authorized",
        "deployment_safety_claim_authorized",
        "natural_frequency_from_track_f",
        "planner_expressiveness_claim_authorized",
    ]:
        if ledger["predicates"].get(name) is True and name in EXPECTED_SENTENCES:
            lines.append("- %s" % EXPECTED_SENTENCES[name])
            lines.append("  Evidence: %s" % ledger["evidence"].get(name, "ledger"))
    if len(lines) == 2:
        lines.append("No scientific predicates flipped on the sealed evidence.")
    text = "\n".join(lines) + "\n"
    # console.log AUDCL-05: expectation rebuild complete.
    print("[audit:claims] expected_claims_text: complete.")
    return text
