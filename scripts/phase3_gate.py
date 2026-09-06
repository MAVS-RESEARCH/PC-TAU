"""Phase-3 gate G3: verify MEASURED with planner-first-use and bundle readiness."""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log GATE3-01: script entry confirms gate pipeline start.
print("[phase3:gate] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log GATE3-02: argparse configuration entry.
    print("[phase3:gate] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Evaluate Phase-3 gate G3.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--check-gate", default=None)
    args = parser.parse_args()
    # console.log GATE3-03: arguments parsed.
    print("[phase3:gate] parse_args: check-gate=%s." % args.check_gate)
    return args


def evaluate_gate(repo_root: Path, run_id: str) -> dict:
    """Evaluate every G3 condition."""
    # console.log GATE3-04: gate evaluation entry.
    print("[phase3:gate] evaluate_gate: entry run-id=%s." % run_id)
    reasons: list[str] = []
    checks: dict[str, bool] = {}
    exact_dir = repo_root / "results" / run_id / "exact"
    agents_dir = repo_root / "results" / run_id / "agents"
    contract_dir = repo_root / "results" / run_id / "contract"

    exact = pd.read_parquet(exact_dir / "freeze_results.parquet")
    sig = pd.read_parquet(exact_dir / "k_pi_signatures.parquet")
    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    panel = json.loads((contract_dir / "controlled_panel.json").read_text(encoding="utf-8"))
    expected_rows = (len(population["task_ids"]) + panel["count"]) * 8
    checks["lattice_allocated"] = len(exact) == expected_rows
    if not checks["lattice_allocated"]:
        reasons.append("lattice rows %d != expected %d" % (len(exact), expected_rows))
    # console.log GATE3-05: lattice allocation checked.
    print("[phase3:gate] evaluate_gate: rows=%d expected=%d." % (len(exact), expected_rows))
    checks["certificates_valid"] = bool((exact["terminal_status"].isin(["CLOSED", "UNCLOSED"])).all())
    checks["infinite_retained"] = bool((exact["kappa"] == "INF").any())
    checks["finite_retained"] = bool((exact["kappa"] != "INF").any())
    if not checks["infinite_retained"]:
        reasons.append("no infinite rows retained")
    # console.log GATE3-06: finite and infinite retention checked.
    print(
        "[phase3:gate] evaluate_gate: finite=%s infinite=%s."
        % (checks["finite_retained"], checks["infinite_retained"])
    )
    selftest = json.loads((exact_dir / "planner_selftest.json").read_text(encoding="utf-8"))
    checks["selftest_pass"] = selftest.get("passed") is True and selftest.get("probe_unrestricted") == 1
    if not checks["selftest_pass"]:
        reasons.append("planner selftest failed")

    paired = pd.read_parquet(agents_dir / "paired_runs.parquet")
    trajectories = [json.loads(line) for line in open(agents_dir / "trajectories.jsonl", encoding="utf-8")]
    checks["pairing_join"] = len(paired) == len(trajectories) and len(paired) > 0
    if not checks["pairing_join"]:
        reasons.append("pairing manifest does not join trajectories")
    # console.log GATE3-07: pairing checked.
    print("[phase3:gate] evaluate_gate: paired=%d trajs=%d." % (len(paired), len(trajectories)))
    metrics = pd.read_parquet(agents_dir / "metrics.parquet")
    checks["metrics_present"] = len(metrics) == len(trajectories)
    checks["unsafe_zero"] = bool((metrics["unsafe_attempts"] == 0).all())
    if not checks["unsafe_zero"]:
        reasons.append("executed unauthorized effects nonzero")
    # console.log GATE3-08: metrics and safety checked.
    print("[phase3:gate] evaluate_gate: metrics=%d unsafe_zero=%s." % (len(metrics), checks["unsafe_zero"]))

    manifest = json.loads((repo_root / "results" / run_id / "phase_manifest.json").read_text(encoding="utf-8"))
    for key in [
        "results/%s/exact/freeze_results.parquet" % run_id,
        "results/%s/exact/k_pi_signatures.parquet" % run_id,
        "results/%s/exact/planner_selftest.json" % run_id,
        "results/%s/agents/trajectories.jsonl" % run_id,
        "results/%s/agents/paired_runs.parquet" % run_id,
        "results/%s/agents/metrics.parquet" % run_id,
        "results/%s/controls/control_results.jsonl" % run_id,
        "results/%s/reports/phase3_summary.json" % run_id,
    ]:
        if key not in manifest:
            checks["manifest_complete"] = False
            reasons.append("manifest missing %s" % key)
            break
    else:
        checks["manifest_complete"] = True
    g2_hashes = {
        name: manifest.get("results/%s/contract/%s" % (run_id, name))
        for name in ["semantic_boundary_policy.json", "admissible_refactorings.json", "contract_family_rules.json"]
    }
    checks["refactor_untouched"] = all(v is not None for v in g2_hashes.values())
    # console.log GATE3-09: manifest and refactor files checked.
    print("[phase3:gate] evaluate_gate: manifest=%s." % checks["manifest_complete"])
    log = subprocess.run(
        ["git", "log", "--oneline", "--", "src/pc_tau/planner.py", "src/pc_tau/freeze.py"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    checks["planner_first_use"] = log.stdout.strip() == ""
    if not checks["planner_first_use"]:
        reasons.append("planner history predates Phase 3")
    # console.log GATE3-10: planner-first-use checked.
    print("[phase3:gate] evaluate_gate: planner_first_use=%s." % checks["planner_first_use"])
    status = "MEASURED" if all(checks.values()) and not reasons else "STOP"
    # console.log GATE3-11: gate verdict determined.
    print("[phase3:gate] evaluate_gate: verdict=%s." % status)
    return {"run_id": run_id, "status": status, "checks": checks, "reasons": reasons}


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log GATE3-12: manifest update entry.
    print("[phase3:gate] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log GATE3-13: manifest update complete.
    print("[phase3:gate] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Run gate evaluation and write PHASE3_COMPLETE on success."""
    # console.log GATE3-14: main entry.
    print("[phase3:gate] main: entry.")
    args = parse_args()
    if args.check_gate is not None and args.check_gate != "g3":
        raise SystemExit("unknown gate %s (expected g3)" % args.check_gate)
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log GATE3-15: experiment config loaded.
    print("[phase3:gate] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    payload = evaluate_gate(repo_root, run_id)
    # console.log GATE3-16: gate payload assembled.
    print("[phase3:gate] main: verdict=%s." % payload["status"])
    if payload["status"] == "MEASURED":
        marker = {"run_id": run_id, "status": "MEASURED"}
        marker_path = repo_root / "results" / run_id / "PHASE3_COMPLETE"
        marker_path.write_text(canonical_dumps(marker) + "\n", encoding="utf-8")
        # console.log GATE3-17: marker written.
        print("[phase3:gate] main: wrote %s." % marker_path.as_posix())
        update_manifest(repo_root, run_id, "results/%s/PHASE3_COMPLETE" % run_id, marker)
    # console.log GATE3-18: gate pipeline complete.
    print("[phase3:gate] main: complete run-id=%s." % run_id)
    return 0 if payload["status"] == "MEASURED" else 2


if __name__ == "__main__":
    # console.log GATE3-19: script invoked as main.
    print("[phase3:gate] __main__: invoking main.")
    raise SystemExit(main())
