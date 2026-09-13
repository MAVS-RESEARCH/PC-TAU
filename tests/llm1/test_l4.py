"""LLM1 L4 tests: audit agreement, corruption, claims, bundle, replay."""

import hashlib
import io
import json
import tarfile
from pathlib import Path

import pandas as pd
import zstandard


# console.log L4T-01: test module import confirms L4 checks are active.
print("[test:llm1-l4] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
LLM1 = REPO_ROOT / "llm1"


def test_audit_agreement():
    """Independent layers all equal with complete provenance."""
    # console.log L4T-02: agreement test entry.
    print("[test:llm1-l4] test_audit_agreement: entry.")
    audit = json.loads((LLM1 / "audit" / "audit.json").read_text(encoding="utf-8"))
    assert audit["all_equal"] is True
    assert set(audit["layers"]) >= {"inheritance", "metrics", "costs", "provenance", "population", "pairing"}
    assert all(audit["layers"].values())
    # console.log L4T-03: agreement verified.
    print("[test:llm1-l4] test_audit_agreement: passed.")


def test_corruption_fail_closed():
    """All 24 corruption families detected."""
    # console.log L4T-04: corruption test entry.
    print("[test:llm1-l4] test_corruption_fail_closed: entry.")
    families = [json.loads(line) for line in open(LLM1 / "audit" / "corruption_results.jsonl", encoding="utf-8")]
    assert len(families) == 24 and all(f["passed"] for f in families)
    # console.log L4T-05: corruption verified.
    print("[test:llm1-l4] test_corruption_fail_closed: passed.")


def test_claims_evidence_only():
    """Ledger flips match evidence; language has no unevidenced sentences."""
    # console.log L4T-06: claims test entry.
    print("[test:llm1-l4] test_claims_evidence_only: entry.")
    import sys

    sys.path.insert(0, str(REPO_ROOT / "src"))
    from llm1_audit.claims_audit import expected_text, verify

    ledger = json.loads((LLM1 / "claim_ledger.json").read_text(encoding="utf-8"))
    ok, problems = verify(ledger)
    assert ok, problems
    text = (LLM1 / "reports" / "LLM1_CLAIMS.md").read_text(encoding="utf-8")
    assert text == expected_text(ledger)
    assert "prevalence" not in text.lower() and "frontier" not in text.lower()
    # console.log L4T-07: claims verified.
    print("[test:llm1-l4] test_claims_evidence_only: passed.")


def test_bundle_clean_and_sealed():
    """Bundle has no secrets; pointer matches; marker sealed with empty reasons."""
    # console.log L4T-08: bundle test entry.
    print("[test:llm1-l4] test_bundle_clean_and_sealed: entry.")
    pointer = json.loads((LLM1 / "release_pointer.json").read_text(encoding="utf-8"))
    asset = LLM1 / pointer["bundle"]
    assert hashlib.sha256(asset.read_bytes()).hexdigest() == pointer["sha256"]
    names = tarfile.open(fileobj=io.BytesIO(zstandard.ZstdDecompressor().decompress(asset.read_bytes())), mode="r").getnames()
    assert not any(".env" in n or "Authorization" in n for n in names)
    marker = json.loads((LLM1 / "LLM1_SEALED").read_text(encoding="utf-8"))
    assert marker["status"] == "LLM1_SEALED" and marker["reasons"] == []
    assert not (LLM1 / "INVALID").exists()
    # console.log L4T-09: bundle and seal verified.
    print("[test:llm1-l4] test_bundle_clean_and_sealed: passed.")


def test_cost_within_cap():
    """Reconciled total stays within the operational cap."""
    # console.log L4T-10: cost test entry.
    print("[test:llm1-l4] test_cost_within_cap: entry.")
    costs = json.loads((LLM1 / "audit" / "independent_costs.json").read_text(encoding="utf-8"))
    assert costs["total"] <= 20.00 and costs["within_cap"] is True
    # console.log L4T-11: cost verified.
    print("[test:llm1-l4] test_cost_within_cap: passed.")
