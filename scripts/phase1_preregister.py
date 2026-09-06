"""Phase-1 preregistration gate: verify G1 and seal PREREGISTERED or STOP."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical, sha256_of_file


# console.log REG-01: script entry confirms gate pipeline start.
print("[phase1:preregister] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log REG-02: argparse configuration entry.
    print("[phase1:preregister] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Evaluate Phase-1 gate G1.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--check-gate", default=None)
    args = parser.parse_args()
    # console.log REG-03: arguments parsed.
    print("[phase1:preregister] parse_args: check-gate=%s." % args.check_gate)
    return args


def _imports_forbidden(path: Path, banned: list[str]) -> list[str]:
    """Return banned top-level imports found via AST in a file."""
    # console.log REG-04: import scan entry for file.
    print("[phase1:preregister] _imports_forbidden: scanning %s." % path.name)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in banned:
                    found.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in banned:
                found.append(node.module)
            if (node.module or "").startswith("pc_tau."):
                leaf = (node.module or "").split(".")[-1]
                if leaf in banned:
                    found.append(node.module or "")
    # console.log REG-05: import scan complete.
    print("[phase1:preregister] _imports_forbidden: %s hits=%d." % (path.name, len(found)))
    return found


def evaluate_gate(repo_root: Path, run_id: str, cfg: dict) -> dict:
    """Evaluate every G1 condition and return the gate payload."""
    # console.log REG-06: gate evaluation entry.
    print("[phase1:preregister] evaluate_gate: entry run-id=%s." % run_id)
    reasons: list[str] = []
    checks: dict[str, bool] = {}

    manifest_path = repo_root / "external_source" / "source_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    upstream_dir = repo_root / cfg["upstream"]["dir"]
    actual_head = __import__("subprocess").run(
        ["git", "-C", str(upstream_dir), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    checks["source_immutable"] = actual_head == manifest["commit_sha"]
    # console.log REG-07: source immutability checked.
    print("[phase1:preregister] evaluate_gate: source_immutable=%s." % checks["source_immutable"])
    if not checks["source_immutable"]:
        reasons.append("source HEAD does not match manifest")

    pilot_payload = json.loads(
        (repo_root / "results" / run_id / "pilot" / "pilot_ids.json").read_text(
            encoding="utf-8"
        )
    )
    gate_payload = json.loads(
        (repo_root / "results" / run_id / "pilot" / "gate_log.json").read_text(
            encoding="utf-8"
        )
    )
    rows = gate_payload["rows"]
    viable_rows = [r for r in rows if r["multi_action_viable"]]
    by_domain: dict[str, int] = {}
    for r in viable_rows:
        by_domain[r["domain"]] = by_domain.get(r["domain"], 0) + 1
    fallback_rows = [r for r in rows if r["finite_fallback"]]
    firewall_ok = all(r["firewall_ok"] for r in rows)
    cpu_ok = all(r["exact_solvable_cpu"] for r in rows) and gate_payload[
        "total_cpu_seconds"
    ] < 60.0
    checks["pilot_yield"] = len(viable_rows) >= 8
    checks["pilot_multidomain"] = all(by_domain.get(d, 0) >= 2 for d in ["airline", "retail"])
    checks["pilot_finite_fallback"] = len(fallback_rows) >= 1
    checks["pilot_firewall"] = firewall_ok
    checks["pilot_cpu"] = cpu_ok
    # console.log REG-08: pilot gate conditions evaluated.
    print(
        "[phase1:preregister] evaluate_gate: viable=%d fallback=%d domains=%s."
        % (len(viable_rows), len(fallback_rows), by_domain)
    )
    if not checks["pilot_yield"]:
        reasons.append("fewer than 8/24 viable-route pilot tasks")
    if not checks["pilot_multidomain"]:
        reasons.append("fewer than 2 viable-route tasks per domain")
    if not checks["pilot_finite_fallback"]:
        reasons.append("no provisional finite fallback case")
    if not checks["pilot_firewall"]:
        reasons.append("operational firewall validation failed")
    if not checks["pilot_cpu"]:
        reasons.append("CPU budget exceeded")

    required_configs = [
        "configs/experiment.yaml",
        "configs/costs.yaml",
        "configs/models.yaml",
        "configs/freezes.yaml",
        "configs/claims.yaml",
    ]
    checks["configs_sealed"] = all((repo_root / p).exists() for p in required_configs)
    # console.log REG-09: config presence checked.
    print("[phase1:preregister] evaluate_gate: configs_sealed=%s." % checks["configs_sealed"])
    if not checks["configs_sealed"]:
        reasons.append("one or more phase configs missing")
    checks["single_freeze_file"] = (repo_root / "configs" / "freezes.yaml").exists() and not (
        repo_root / "configs" / "freeze_lattice.yaml"
    ).exists()
    if not checks["single_freeze_file"]:
        reasons.append("freeze file rule violated (need exactly configs/freezes.yaml)")
    # console.log REG-10: freeze file rule checked.
    print(
        "[phase1:preregister] evaluate_gate: single_freeze_file=%s."
        % checks["single_freeze_file"]
    )

    required_prereg = [
        "preregistration/eligibility_rule.json",
        "preregistration/model_protocol.json",
        "preregistration/user_response_protocol.json",
        "preregistration/nonclaims.json",
    ]
    checks["prereg_sealed"] = all((repo_root / p).exists() for p in required_prereg)
    if not checks["prereg_sealed"]:
        reasons.append("preregistration files missing")
    # console.log REG-11: preregistration presence checked.
    print("[phase1:preregister] evaluate_gate: prereg_sealed=%s." % checks["prereg_sealed"])

    eligibility_payload = json.loads(
        (repo_root / "preregistration" / "eligibility_rule.json").read_text(
            encoding="utf-8"
        )
    )
    required_text = json.dumps(eligibility_payload.get("required", []))
    forbidden_text = json.dumps(eligibility_payload.get("forbidden", []))
    checks["eligibility_blind"] = all(
        token not in required_text for token in ["Delta_R", "K_Pi"]
    ) and all(token in forbidden_text for token in ["Delta_R", "K_Pi"])
    if not checks["eligibility_blind"]:
        reasons.append("eligibility rule uses outcome values or fails to forbid them")
    # console.log REG-12: eligibility blindness checked.
    print(
        "[phase1:preregister] evaluate_gate: eligibility_blind=%s."
        % checks["eligibility_blind"]
    )
    for rel in [
        "src/pc_tau/source.py",
        "src/pc_tau/reachability.py",
        "scripts/phase1_pilot.py",
    ]:
        hits = _imports_forbidden(repo_root / rel, ["freeze", "planner", "metrics"])
        key = "imports_clean:" + Path(rel).name
        checks[key] = len(hits) == 0
        if hits:
            reasons.append("%s imports forbidden modules %s" % (rel, hits))

    forbidden_found: list[str] = []
    results_root = repo_root / "results" / run_id
    for path in sorted(results_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        if rel.startswith("results/%s/pilot/" % run_id):
            continue
        if rel.endswith(("phase_manifest.json", "phase1_preregistration.json")):
            continue
        name = path.name.lower()
        if "k_pi" in name or "freeze_result" in name or "trajector" in name:
            forbidden_found.append(rel)
    checks["no_final_values"] = len(forbidden_found) == 0
    if forbidden_found:
        reasons.append("final-population values present: %s" % forbidden_found[:3])
    # console.log REG-13: final-value filesystem scan complete.
    print(
        "[phase1:preregister] evaluate_gate: no_final_values=%s." % checks["no_final_values"]
    )

    manifest_path_run = results_root / "phase_manifest.json"
    checks["manifest_complete"] = manifest_path_run.exists()
    if checks["manifest_complete"]:
        manifest_run = json.loads(manifest_path_run.read_text(encoding="utf-8"))
        for key in [
            "external_source/source_manifest.json",
            "external_source/task_census.json",
        ]:
            if key not in manifest_run:
                checks["manifest_complete"] = False
                reasons.append("manifest missing %s" % key)
    else:
        reasons.append("run manifest missing")
    # console.log REG-14: manifest completeness checked.
    print(
        "[phase1:preregister] evaluate_gate: manifest_complete=%s."
        % checks["manifest_complete"]
    )

    status = "PREREGISTERED" if all(checks.values()) and not reasons else "STOP"
    # console.log REG-15: gate verdict determined.
    print("[phase1:preregister] evaluate_gate: verdict=%s." % status)
    config_hashes = {}
    for rel in [
        "configs/experiment.yaml",
        "configs/costs.yaml",
        "configs/models.yaml",
        "configs/freezes.yaml",
        "configs/claims.yaml",
        "preregistration/eligibility_rule.json",
        "preregistration/model_protocol.json",
        "preregistration/user_response_protocol.json",
        "preregistration/nonclaims.json",
    ]:
        config_hashes[rel] = sha256_of_file(repo_root / rel)
    # console.log REG-15b: config hashes recorded for gate evidence.
    print("[phase1:preregister] evaluate_gate: recorded %d config hashes." % len(config_hashes))
    return {
        "run_id": run_id,
        "status": status,
        "checks": checks,
        "reasons": reasons,
        "pilot_viable": len(viable_rows),
        "pilot_fallback": len(fallback_rows),
        "by_domain": by_domain,
        "source_commit": manifest["commit_sha"],
        "source_tree": manifest["tree_hash"],
        "config_hashes": config_hashes,
    }


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log REG-16: manifest update entry.
    print("[phase1:preregister] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log REG-17: manifest update complete.
    print("[phase1:preregister] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Run gate evaluation and write preregistration report."""
    # console.log REG-18: main entry.
    print("[phase1:preregister] main: entry.")
    args = parse_args()
    if args.check_gate is not None and args.check_gate != "g1":
        raise SystemExit("unknown gate %s (expected g1)" % args.check_gate)
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log REG-19: experiment config loaded.
    print("[phase1:preregister] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    payload = evaluate_gate(repo_root, run_id, cfg)
    # console.log REG-20: gate payload assembled.
    print("[phase1:preregister] main: verdict=%s." % payload["status"])
    out_path = repo_root / "results" / run_id / "reports" / "phase1_preregistration.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(canonical_dumps(payload) + "\n", encoding="utf-8")
    # console.log REG-21: preregistration report written.
    print("[phase1:preregister] main: wrote %s." % out_path.as_posix())
    update_manifest(
        repo_root, run_id, "results/%s/reports/phase1_preregistration.json" % run_id, payload
    )
    # console.log REG-22: preregister pipeline complete.
    print("[phase1:preregister] main: complete run-id=%s." % run_id)
    return 0 if payload["status"] == "PREREGISTERED" else 2


if __name__ == "__main__":
    # console.log REG-23: script invoked as main.
    print("[phase1:preregister] __main__: invoking main.")
    raise SystemExit(main())
