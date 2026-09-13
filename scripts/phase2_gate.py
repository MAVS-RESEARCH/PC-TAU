"""Phase-2 gate G2: verify CONTRACT_SEALED or STOP (Fix 12 sole success state)."""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log GATE2-01: script entry confirms gate pipeline start.
print("[phase2:gate] entry: parsing arguments.")


PHASE2_OUTPUTS = [
    "results/{run}/contract/semantic_facts.jsonl",
    "results/{run}/contract/extraction_records.jsonl",
    "results/{run}/contract/extraction_protocol.json",
    "results/{run}/contract/task_contracts.jsonl",
    "results/{run}/contract/contract_families.jsonl",
    "results/{run}/contract/repair_actions.jsonl",
    "results/{run}/contract/touch_records.parquet",
    "results/{run}/contract/route_classification.parquet",
    "results/{run}/contract/natural_population.json",
    "results/{run}/contract/partial_tasks.jsonl",
    "results/{run}/contract/controlled_panel.json",
    "results/{run}/contract/semantic_boundary_policy.json",
    "results/{run}/contract/admissible_refactorings.json",
    "results/{run}/contract/contract_family_rules.json",
    "results/{run}/contract/failure_cards.jsonl",
]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log GATE2-02: argparse configuration entry.
    print("[phase2:gate] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Evaluate Phase-2 gate G2.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--check-gate", default=None)
    args = parser.parse_args()
    # console.log GATE2-03: arguments parsed.
    print("[phase2:gate] parse_args: check-gate=%s." % args.check_gate)
    return args


def _imports(path: Path, banned: list[str]) -> list[str]:
    """AST import scan for banned module roots and pc_tau leaves."""
    # console.log GATE2-04: import scan entry.
    print("[phase2:gate] _imports: scanning %s." % path.name)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in banned:
                    found.append(alias.name)
                if alias.name.startswith("pc_tau."):
                    leaf = alias.name.split(".")[-1]
                    if leaf in banned:
                        found.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in banned:
                found.append(node.module)
            if (node.module or "").startswith("pc_tau."):
                leaf = (node.module or "").split(".")[-1]
                if leaf in banned:
                    found.append(node.module or "")
    # console.log GATE2-05: import scan complete.
    print("[phase2:gate] _imports: %s hits=%d." % (path.name, len(found)))
    return found


def evaluate_gate(repo_root: Path, run_id: str) -> dict:
    """Evaluate every G2 condition."""
    # console.log GATE2-06: gate evaluation entry.
    print("[phase2:gate] evaluate_gate: entry run-id=%s." % run_id)
    reasons: list[str] = []
    checks: dict[str, bool] = {}
    contract_dir = repo_root / "results" / run_id / "contract"

    contracts = [
        json.loads(line)
        for line in open(contract_dir / "task_contracts.jsonl", encoding="utf-8")
    ]
    families = [
        json.loads(line)
        for line in open(contract_dir / "contract_families.jsonl", encoding="utf-8")
    ]
    repairs = [
        json.loads(line)
        for line in open(contract_dir / "repair_actions.jsonl", encoding="utf-8")
    ]
    # console.log GATE2-07: contract artifacts loaded.
    print(
        "[phase2:gate] evaluate_gate: contracts=%d families=%d repairs=%d."
        % (len(contracts), len(families), len(repairs))
    )
    checks["provenance_complete"] = all(r.get("locator") and r.get("justification") for r in repairs)
    if not checks["provenance_complete"]:
        reasons.append("missing provenance for retained repairs")
    checks["no_manual_touch"] = all(
        "resource_label" not in r and "touch" not in r for r in repairs
    )
    if not checks["no_manual_touch"]:
        reasons.append("manual touch labels present")
    # console.log GATE2-08: provenance and manual-touch checked.
    print(
        "[phase2:gate] evaluate_gate: provenance=%s no_manual=%s."
        % (checks["provenance_complete"], checks["no_manual_touch"])
    )
    types_ok = True
    for contract in contracts:
        if not isinstance(contract.get("U_H"), list):
            types_ok = False
        if not isinstance(contract.get("H"), dict):
            types_ok = False
        if not isinstance(contract.get("P_R"), list):
            types_ok = False
        if not isinstance(contract.get("Lambda"), list):
            types_ok = False
        if not isinstance(contract.get("omega"), list):
            types_ok = False
        if "Cert" not in contract:
            types_ok = False
        if contract.get("omega") == contract.get("Cert"):
            types_ok = False
    checks["types_valid"] = types_ok
    if not types_ok:
        reasons.append("formal contract types invalid")
    # console.log GATE2-09: formal types checked.
    print("[phase2:gate] evaluate_gate: types_valid=%s." % types_ok)

    banned = ["freeze", "planner", "metrics"]
    for rel in [
        "src/pc_tau/semantics.py",
        "src/pc_tau/repairs.py",
        "src/pc_tau/touch.py",
        "scripts/phase2_extract.py",
        "scripts/phase2_verify.py",
        "scripts/phase2_compile.py",
        "scripts/phase2_touch.py",
        "scripts/phase2_eligibility.py",
    ]:
        hits = _imports(repo_root / rel, banned)
        key = "imports_clean:" + Path(rel).name
        checks[key] = len(hits) == 0
        if hits:
            reasons.append("%s imports forbidden %s" % (rel, hits))
    checks["planner_absent"] = not (repo_root / "src" / "pc_tau" / "planner.py").exists()
    checks["freeze_absent"] = not (repo_root / "src" / "pc_tau" / "freeze.py").exists()
    if not checks["planner_absent"]:
        reasons.append("production planner present before Phase 3")
    if not checks["freeze_absent"]:
        reasons.append("freeze module present before Phase 3")
    # console.log GATE2-10: planner isolation checked.
    print("[phase2:gate] evaluate_gate: planner_absent=%s." % checks["planner_absent"])
    for rel in [
        "src/pc_tau/semantics.py",
        "src/pc_tau/repairs.py",
        "src/pc_tau/touch.py",
    ]:
        text = (repo_root / rel).read_text(encoding="utf-8")
        key = "provisional_invisible:" + Path(rel).name
        checks[key] = "provisional_geometry" not in text and "pilot_provisional" not in text
        if not checks[key]:
            reasons.append("%s reads provisional geometry" % rel)

    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    partials = [
        json.loads(line)
        for line in open(contract_dir / "partial_tasks.jsonl", encoding="utf-8")
        if line.strip()
    ]
    failures = [
        json.loads(line)
        for line in open(contract_dir / "failure_cards.jsonl", encoding="utf-8")
        if line.strip()
    ]
    checks["primary_count"] = population["count"] >= 40
    checks["primary_domains"] = len(population.get("by_domain", {})) >= 2
    if not checks["primary_count"]:
        reasons.append("IDENTIFIED primary core <40")
    if not checks["primary_domains"]:
        reasons.append("primary core spans fewer than 2 domains")
    # console.log GATE2-11: primary population checked.
    print(
        "[phase2:gate] evaluate_gate: primary=%d domains=%s partial=%d."
        % (population["count"], population.get("by_domain"), len(partials))
    )
    panel = json.loads((contract_dir / "controlled_panel.json").read_text(encoding="utf-8"))
    checks["panel_separate"] = (
        panel["count"] == 32
        and panel["per_regime"] == 8
        and panel["balanced_by_design"] is True
        and panel["estimates_natural_frequency"] is False
    )
    if not checks["panel_separate"]:
        reasons.append("controlled panel malformed")
    for name in [
        "semantic_boundary_policy.json",
        "admissible_refactorings.json",
        "contract_family_rules.json",
    ]:
        payload = json.loads((contract_dir / name).read_text(encoding="utf-8"))
        key = "refactor_frozen:" + name
        checks[key] = payload.get("frozen") is True
        if not checks[key]:
            reasons.append("%s not frozen" % name)
    # console.log GATE2-12: panel and refactor policies checked.
    print("[phase2:gate] evaluate_gate: panel=%s refactor sealed." % checks["panel_separate"])

    manifest = json.loads(
        (repo_root / "results" / run_id / "phase_manifest.json").read_text(encoding="utf-8")
    )
    checks["manifest_complete"] = all(
        ("results/%s/contract/%s" % (run_id, Path(p).name) in manifest)
        or (p.replace("{run}", run_id) in manifest)
        for p in PHASE2_OUTPUTS
    )
    if not checks["manifest_complete"]:
        reasons.append("manifest missing Phase-2 outputs")
    forbidden_found: list[str] = []
    for path in sorted((repo_root / "results" / run_id).rglob("*")):
        if not path.is_file():
            continue
        name = path.name.lower()
        if "freeze_result" in name or "trajector" in name or "k_pi" in name:
            forbidden_found.append(path.relative_to(repo_root).as_posix())
    checks["no_final_values"] = len(forbidden_found) == 0
    if forbidden_found:
        reasons.append("final values present: %s" % forbidden_found[:3])
    # console.log GATE2-13: manifest and final-value scan complete.
    print(
        "[phase2:gate] evaluate_gate: manifest=%s no_final=%s."
        % (checks["manifest_complete"], checks["no_final_values"])
    )
    status = "CONTRACT_SEALED" if all(checks.values()) and not reasons else "STOP"
    # console.log GATE2-14: gate verdict determined.
    print("[phase2:gate] evaluate_gate: verdict=%s." % status)
    counts: dict[str, int] = {}
    for family in families:
        counts[family["status"]] = counts.get(family["status"], 0) + 1
    return {
        "run_id": run_id,
        "status": status,
        "checks": checks,
        "reasons": reasons,
        "counts": counts,
        "primary": population["count"],
        "partial": len(partials),
        "phase3_authorized_on_primary": status == "CONTRACT_SEALED",
    }


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log GATE2-15: manifest update entry.
    print("[phase2:gate] update_manifest: entry %s." % rel_path)
    from pc_tau.source import canonical_dumps, sha256_of_canonical

    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log GATE2-16: manifest update complete.
    print("[phase2:gate] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Run gate evaluation and write the seal marker on success."""
    # console.log GATE2-17: main entry.
    print("[phase2:gate] main: entry.")
    parser = argparse.ArgumentParser(description="Evaluate Phase-2 gate G2.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--check-gate", default=None)
    args = parser.parse_args()
    if args.check_gate is not None and args.check_gate != "g2":
        raise SystemExit("unknown gate %s (expected g2)" % args.check_gate)
    # console.log GATE2-18: arguments parsed.
    print("[phase2:gate] main: check-gate=g2.")
    import yaml

    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log GATE2-19: experiment config loaded.
    print("[phase2:gate] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    payload = evaluate_gate(repo_root, run_id)
    # console.log GATE2-20: gate payload assembled.
    print("[phase2:gate] main: verdict=%s." % payload["status"])
    if payload["status"] == "CONTRACT_SEALED":
        marker = {
            "run_id": run_id,
            "status": "CONTRACT_SEALED",
            "counts": payload["counts"],
            "primary": payload["primary"],
            "partial": payload["partial"],
        }
        marker_path = repo_root / "results" / run_id / "contract" / "CONTRACT_SEALED"
        marker_path.write_text(canonical_dumps(marker) + "\n", encoding="utf-8")
        # console.log GATE2-21: seal marker written.
        print("[phase2:gate] main: wrote %s." % marker_path.as_posix())
        update_manifest(
            repo_root, run_id, "results/%s/contract/CONTRACT_SEALED" % run_id, marker
        )
    # console.log GATE2-22: gate pipeline complete.
    print("[phase2:gate] main: complete run-id=%s." % run_id)
    return 0 if payload["status"] == "CONTRACT_SEALED" else 2


if __name__ == "__main__":
    # console.log GATE2-23: script invoked as main.
    print("[phase2:gate] __main__: invoking main.")
    raise SystemExit(main())
