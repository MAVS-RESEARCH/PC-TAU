"""LLM1 independent claims audit: separate predicate logic and language rebuild."""

from __future__ import annotations

from typing import Any


# console.log LCA-01: module import confirms claims audit is available.
print("[llm1-audit:claims] module loaded.")

EXPECTED = {
    "actual_learned_agent_evidence": "Actual trained models were evaluated through provider-verified live inference under the sealed PC-TAU resource interventions.",
    "real_inference_complete": "All 5,436 scheduled episodes are accounted for with genuine provider responses.",
    "paired_resource_intervention_measured": "Paired freeze interventions were measured with task, model, repeat and bundle held fixed.",
    "freeze_sensitive_behavior_observed": "Removal of the R-touching optimal repair altered learned-agent behavior under finite fallback.",
    "finite_fallback_discovery_observed": "Learned agents discovered the finite fallback route under the R freeze.",
    "imperfect_adaptation_observed": "Learned agents adapted imperfectly: excess cost or escalation relative to the exact oracle.",
    "cross_model_replication_observed": "The primary freeze effect replicated across independently evaluated model families.",
    "cross_model_heterogeneity_observed": "Model families differed in freeze response.",
    "unsafe_behavior_observed": "Open-state submit attempts were observed and blocked with zero unauthorized executions.",
    "protocol_compatibility_established": "All roster models executed the common semantic protocol without incompatibility.",
}


def verify(ledger: dict[str, Any]) -> tuple[bool, list[str]]:
    """Verify booleans, evidence pointers for flips, and known sentences."""
    # console.log LCA-02: verification entry.
    print("[llm1-audit:claims] verify: entry.")
    problems: list[str] = []
    for name, value in ledger.get("predicates", {}).items():
        if not isinstance(value, bool):
            problems.append("%s not boolean" % name)
        if value is True and name not in EXPECTED:
            problems.append("%s true without known sentence" % name)
        if value is True and name not in ledger.get("evidence", {}):
            problems.append("%s true without evidence pointer" % name)
    # console.log LCA-03: verification complete.
    print("[llm1-audit:claims] verify: problems=%d." % len(problems))
    return (not problems, problems)


def expected_text(ledger: dict[str, Any]) -> str:
    """Rebuild expected claim text from true predicates (separate text)."""
    # console.log LCA-04: rebuild entry.
    print("[llm1-audit:claims] expected_text: entry.")
    lines = ["# LLM1 sealed claims (evidence-derived predicates)", ""]
    for name, sentence in EXPECTED.items():
        if ledger["predicates"].get(name) is True:
            lines.append("- %s" % sentence)
            lines.append("  Evidence: %s" % ledger["evidence"].get(name, "ledger"))
    text = "\n".join(lines) + "\n"
    # console.log LCA-05: rebuild complete.
    print("[llm1-audit:claims] expected_text: complete.")
    return text
