"""Phase-2 Pass B: contract compilation and family status (Fix 5)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.semantics import compile_contract, family_status
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log CMP-01: script entry confirms compilation pipeline start.
print("[phase2:compile] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log CMP-02: argparse configuration entry.
    print("[phase2:compile] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Compile contracts.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log CMP-03: arguments parsed.
    print("[phase2:compile] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log CMP-04: manifest update entry.
    print("[phase2:compile] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log CMP-05: manifest update complete.
    print("[phase2:compile] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Compile one formal contract per candidate task plus family status."""
    # console.log CMP-06: main entry.
    print("[phase2:compile] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log CMP-07: experiment config loaded.
    print("[phase2:compile] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    contract_dir = repo_root / "results" / run_id / "contract"
    by_task: dict[str, list[dict]] = {}
    with open(contract_dir / "semantic_facts.jsonl", encoding="utf-8") as fh:
        for line in fh:
            fact = json.loads(line)
            by_task.setdefault(fact["task_id"], []).append(fact)
    disagreements: dict[str, list[str]] = {}
    with open(contract_dir / "extraction_records.jsonl", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            if rec["verdict"] == "disagree":
                disagreements.setdefault(rec["task_id"], []).append(
                    "%s:%s" % (rec["kind"], rec["reason"])
                )
    # console.log CMP-08: facts and verification joined per task.
    print("[phase2:compile] main: tasks=%d disagreements=%d." % (len(by_task), len(disagreements)))
    census = json.loads(
        (repo_root / "external_source" / "task_census.json").read_text(encoding="utf-8")
    )
    task_by_id = {r["task_id"]: r for r in census["records"]}
    unit_weight = int(
        yaml.safe_load(open(repo_root / "configs" / "costs.yaml", encoding="utf-8"))[
            "primary"
        ]["unit_intervention_cost"]
    )
    contracts: list[dict] = []
    families: list[dict] = []
    for task_id in sorted(by_task):
        contract = compile_contract(
            task_by_id[task_id], by_task[task_id], unit_weight
        )
        contracts.append(contract)
        refs = disagreements.get(task_id, [])
        families.append(
            family_status(task_id, True, bool(contract["provenance"]), bool(refs), refs)
        )
    # console.log CMP-09: compilation complete.
    print(
        "[phase2:compile] main: contracts=%d families=%d."
        % (len(contracts), len(families))
    )
    contracts_path = contract_dir / "task_contracts.jsonl"
    with open(contracts_path, "w", encoding="utf-8") as fh:
        for contract in contracts:
            fh.write(canonical_dumps(contract) + "\n")
    # console.log CMP-10: contracts written.
    print("[phase2:compile] main: wrote %s." % contracts_path.as_posix())
    families_path = contract_dir / "contract_families.jsonl"
    with open(families_path, "w", encoding="utf-8") as fh:
        for family in families:
            fh.write(canonical_dumps(family) + "\n")
    # console.log CMP-11: families written.
    print("[phase2:compile] main: wrote %s." % families_path.as_posix())
    update_manifest(
        repo_root, run_id, "results/%s/contract/task_contracts.jsonl" % run_id, contracts
    )
    update_manifest(
        repo_root,
        run_id,
        "results/%s/contract/contract_families.jsonl" % run_id,
        families,
    )
    # console.log CMP-12: compilation pipeline complete.
    print("[phase2:compile] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log CMP-13: script invoked as main.
    print("[phase2:compile] __main__: invoking main.")
    raise SystemExit(main())
