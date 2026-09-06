"""Phase-4 predicate claim locks: all start false, flip only on evidence.

Authorization B is enforced here: learned-agent predicates cannot flip
without valid trained-model inference, which this run does not contain.
The generator emits sentences only for true predicates, so paraphrase
cannot bypass the locks.
"""

from __future__ import annotations

from typing import Any


# console.log CLM-01: module import confirms claim locks are available.
print("[phase4:claims] module loaded: predicate locks ready.")


SCIENTIFIC_PREDICATES = [
    "multiroute_existence_authorized",
    "finite_substitution_natural_authorized",
    "finite_substitution_constructed_authorized",
    "imperfect_adaptation_authorized",
    "learned_agent_evidence_authorized",
    "controlled_regime_authorized",
    "typing_invariance_authorized",
]

PERMANENT_NONCLAIMS = [
    "prevalence_claim_authorized",
    "superiority_claim_authorized",
    "deployment_safety_claim_authorized",
    "natural_frequency_from_track_f",
    "planner_expressiveness_claim_authorized",
]

ALL_PREDICATES = SCIENTIFIC_PREDICATES + PERMANENT_NONCLAIMS

SENTENCES = {
    "finite_substitution_constructed_authorized": "Finite resource substitution occurs in the sealed constructed contracts (finite positive fallback premium under a resource freeze).",
    "controlled_regime_authorized": "The controlled panel reproduces the predicted zero, finite, structural and complementarity mechanisms (balanced by design).",
    "typing_invariance_authorized": "Resource typing is invariant under the frozen harmless-refactoring class for retained tasks.",
}


def fresh_ledger() -> dict[str, Any]:
    """Initialize every predicate to false with empty evidence."""
    # console.log CLM-02: ledger initialization entry.
    print("[phase4:claims] fresh_ledger: entry.")
    ledger = {
        "predicates": {name: False for name in ALL_PREDICATES},
        "evidence": {},
    }
    # console.log CLM-03: ledger initialized all-false.
    print("[phase4:claims] fresh_ledger: predicates=%d all false." % len(ALL_PREDICATES))
    return ledger


def evaluate_evidence(evidence: dict[str, Any]) -> dict[str, bool]:
    """Flip a scientific predicate only when its evidence predicate succeeds.

    Permanent nonclaims stay false unconditionally. Learned-agent
    predicates require valid trained-model inference evidence, which is
    absent, so they remain false with any probe-only pattern.
    """
    # console.log CLM-04: evidence evaluation entry.
    print("[phase4:claims] evaluate_evidence: entry.")
    result = {name: False for name in ALL_PREDICATES}
    if evidence.get("constructed_finite_cases", 0) > 0:
        result["finite_substitution_constructed_authorized"] = True
    if evidence.get("controlled_regimes_reproduced") is True:
        result["controlled_regime_authorized"] = True
    if evidence.get("refactoring_checks_agree") is True:
        result["typing_invariance_authorized"] = True
    # console.log CLM-05: evidence evaluation complete.
    print(
        "[phase4:claims] evaluate_evidence: true=%s."
        % sorted(k for k, v in result.items() if v)
    )
    return result


def generate_claims(ledger: dict[str, Any]) -> str:
    """Generate CLAIMS.md exclusively from true predicates."""
    # console.log CLM-06: generation entry.
    print("[phase4:claims] generate_claims: entry.")
    lines = ["# Sealed claims (evidence-derived predicates)", ""]
    for name in SCIENTIFIC_PREDICATES + PERMANENT_NONCLAIMS:
        if ledger["predicates"].get(name) is True and name in SENTENCES:
            lines.append("- %s" % SENTENCES[name])
            lines.append("  Evidence: %s" % ledger["evidence"].get(name, "ledger"))
    if len(lines) == 2:
        lines.append("No scientific predicates flipped on the sealed evidence.")
    text = "\n".join(lines) + "\n"
    # console.log CLM-07: generation complete.
    print("[phase4:claims] generate_claims: sentences=%d." % (len(lines) - 2))
    return text
