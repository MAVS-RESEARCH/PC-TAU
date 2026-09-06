"""Audit tests: artifact completeness, verdict consistency, sealed-run immutability."""

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml


# console.log AUDT-01: test module import confirms audit check is active.
print("[test:audit-prephase4] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

RUN_ID = "pctau-20260906-672227c"
AUDIT_DIR = REPO_ROOT / "results" / RUN_ID / "audit_prephase4"

EXPECTED = [
    "source_grounding_all_tasks.parquet",
    "source_mechanism_clusters.json",
    "repair_provenance_summary.json",
    "partial_origin_audit.json",
    "model_protocol_audit.json",
    "phase3_model_evidence_verdict.json",
    "exact_result_interpretation.json",
    "POST_MEASUREMENT_AUDIT.md",
    "authorization_decision.json",
]


def test_audit_artifacts_complete():
    """All nine required audit artifacts exist with consistent verdicts."""
    # console.log AUDT-02: completeness test entry.
    print("[test:audit-prephase4] test_audit_artifacts_complete: entry.")
    for name in EXPECTED:
        assert (AUDIT_DIR / name).exists(), name
    grounding = pd.read_parquet(AUDIT_DIR / "source_grounding_all_tasks.parquet")
    assert len(grounding) == 135
    assert set(grounding["qE_class"]) == {"A"}
    assert set(grounding["qR_class"]) == {"B"}
    assert set(grounding["overall"]) == {"SG-B-contributing"}
    decision = json.loads((AUDIT_DIR / "authorization_decision.json").read_text(encoding="utf-8"))
    assert decision["source_verdict"] == "SG-B"
    assert decision["authorization"] == "B"
    assert decision["predicate_locks"]["imperfect_adaptation_authorized"] is False
    assert decision["predicate_locks"]["learned_agent_evidence_authorized"] is False
    verdict = json.loads((AUDIT_DIR / "phase3_model_evidence_verdict.json").read_text(encoding="utf-8"))
    assert verdict["verdict"] == "LM-C" and verdict["lm_b_handling_applies"] is True
    interpretation = json.loads((AUDIT_DIR / "exact_result_interpretation.json").read_text(encoding="utf-8"))
    assert interpretation["interpretation"] == "B" and interpretation["n_distinct_semantic_mechanisms"] == 3
    partial = json.loads((AUDIT_DIR / "partial_origin_audit.json").read_text(encoding="utf-8"))
    assert partial["origin_verdict"].startswith("DELIBERATE_HARNESS_INJECTION")
    # console.log AUDT-03: verdicts consistent.
    print("[test:audit-prephase4] test_audit_artifacts_complete: passed.")


def test_audit_report_structure():
    """The report carries all 20 sections plus the claim matrix."""
    # console.log AUDT-04: structure test entry.
    print("[test:audit-prephase4] test_audit_report_structure: entry.")
    text = (AUDIT_DIR / "POST_MEASUREMENT_AUDIT.md").read_text(encoding="utf-8")
    for section in [
        "## 1. Executive verdict", "## 20. Immutable audit trail", "## CLAIM MATRIX",
        "AUTHORIZATION B", "SG-B", "LM-C",
        "construction consistency, not 135 independent discoveries",
    ]:
        assert section in text, section
    # console.log AUDT-05: structure verified.
    print("[test:audit-prephase4] test_audit_report_structure: passed.")


def test_sealed_run_unmutated():
    """No scientific file changed: only new audit paths plus one harness fix."""
    # console.log AUDT-06: immutability test entry.
    print("[test:audit-prephase4] test_sealed_run_unmutated: entry.")
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    allowed_new = (
        "?? results/pctau-20260906-672227c/audit_prephase4/",
        "?? scripts/audit_prephase4.py",
        "?? tests/audit/",
    )
    # console.log AUDT-07: status lines collected.
    print("[test:audit-prephase4] status lines=%d." % len(status))
    assert status, "expected new audit files in status"
    for line in status:
        if line.startswith("??"):
            assert line.startswith(allowed_new), "unexpected new path: %s" % line
        elif line.startswith(" M "):
            assert line.strip() in (
                "M tests/phase3/test_planner_first_use.py",
                "M Path.md",
            ), "sealed mutation: %s" % line
        else:
            raise AssertionError("sealed mutation: %s" % line)
    for prefix in (" M results/", " M configs/", " M preregistration/", " M src/", " M scripts/", " M schemas/"):
        assert not any(l.startswith(prefix) for l in status), prefix
    manifest = json.loads(
        (REPO_ROOT / "results" / RUN_ID / "phase_manifest.json").read_text(encoding="utf-8")
    )
    assert len(manifest) == 31
    # console.log AUDT-08: immutability verified.
    print("[test:audit-prephase4] test_sealed_run_unmutated: passed.")
