"""Phase-4 claim verification: evidence flips plus generated-language check."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.claims import evaluate_evidence, fresh_ledger, generate_claims
from pc_tau.source import canonical_dumps, sha256_of_canonical
from pc_tau_audit.claims_audit import expected_claims_text, verify_ledger


# console.log VCL-01: script entry confirms claim pipeline start.
print("[phase4:verify-claims] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log VCL-02: argparse configuration entry.
    print("[phase4:verify-claims] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Verify evidence-derived claims.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log VCL-03: arguments parsed.
    print("[phase4:verify-claims] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log VCL-04: manifest update entry.
    print("[phase4:verify-claims] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log VCL-05: manifest update complete.
    print("[phase4:verify-claims] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Evaluate evidence, flip predicates, generate and verify CLAIMS.md."""
    # console.log VCL-06: main entry.
    print("[phase4:verify-claims] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log VCL-07: experiment config loaded.
    print("[phase4:verify-claims] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    sig = pd.read_parquet(repo_root / "results" / run_id / "exact" / "k_pi_signatures.parquet")
    refactor_rows = [
        json.loads(line)
        for line in open(repo_root / "results" / run_id / "audit" / "refactor_results.jsonl", encoding="utf-8")
    ]
    primary = sig[sig["track"] == "N"]
    panel = sig[sig["track"] == "F"]
    # console.log VCL-08: evidence assembled for predicates.
    print("[phase4:verify-claims] main: primary=%d panel=%d." % (len(primary), len(panel)))
    evidence = {
        "constructed_finite_cases": int(((primary["r_class"] == "FINITE_POSITIVE")).sum()),
        "finite_substitution_constructed_authorized": "exact/k_pi_signatures.parquet track=N r_class=FINITE_POSITIVE count>0",
        "controlled_regimes_reproduced": bool(
            set(panel[panel["task_id"].str.startswith("controlled:R-zero")]["r_class"]) == {"ZERO"}
            and set(panel[panel["task_id"].str.startswith("controlled:R-finite")]["r_class"]) == {"FINITE_POSITIVE"}
            and (panel["r_class"] == "STRUCTURAL").sum() == 16
        ),
        "controlled_regime_authorized": "exact/k_pi_signatures.parquet track=F per-regime classes ZEROx8 FINITEx8 STRUCTURALx16",
        "refactoring_checks_agree": bool(refactor_rows and refactor_rows[0].get("passed")),
        "typing_invariance_authorized": "audit/refactor_results.jsonl passed with frozen-only class",
        "learned_model_inference_present": False,
        "learned_pointer": "audit_prephase4/phase3_model_evidence_verdict.json LM-C",
    }
    ledger = fresh_ledger()
    ledger["predicates"] = evaluate_evidence(evidence)
    ledger["evidence"] = evidence
    # console.log VCL-09: predicates flipped on evidence.
    print(
        "[phase4:verify-claims] main: true=%s."
        % sorted(k for k, v in ledger["predicates"].items() if v)
    )
    ok, problems = verify_ledger(ledger)
    if not ok:
        raise SystemExit("claim ledger invalid: %s" % problems)
    text = generate_claims(ledger)
    assert text == expected_claims_text(ledger)
    # console.log VCL-10: independent language rebuild agrees.
    print("[phase4:verify-claims] main: language rebuild agrees.")
    reports_dir = repo_root / "results" / run_id / "reports"
    (reports_dir / "CLAIMS.md").write_text(text, encoding="utf-8")
    (reports_dir / "claim_ledger.json").write_text(canonical_dumps(ledger) + "\n", encoding="utf-8")
    # console.log VCL-11: ledger and CLAIMS.md written.
    print("[phase4:verify-claims] main: wrote ledger and CLAIMS.md.")
    update_manifest(repo_root, run_id, "results/%s/reports/claim_ledger.json" % run_id, ledger)
    update_manifest(repo_root, run_id, "results/%s/reports/CLAIMS.md" % run_id, {"text": text})
    # console.log VCL-12: claim pipeline complete.
    print("[phase4:verify-claims] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log VCL-13: script invoked as main.
    print("[phase4:verify-claims] __main__: invoking main.")
    raise SystemExit(main())
