"""Phase-2 result-blind viable-route eligibility (Fix 3 + Fix 11).

Uses the reachability checker only. Never imports the optimizing
solver. Never inspects outcome values. PARTIAL tasks go to the sealed
sidecar, never the primary population.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.reachability import count_viable_first_repairs
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log ELIG-01: script entry confirms eligibility pipeline start.
print("[phase2:eligibility] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log ELIG-02: argparse configuration entry.
    print("[phase2:eligibility] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Apply viable-route eligibility.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log ELIG-03: arguments parsed.
    print("[phase2:eligibility] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log ELIG-04: manifest update entry.
    print("[phase2:eligibility] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log ELIG-05: manifest update complete.
    print("[phase2:eligibility] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Classify every task and seal primary, sidecar and failure cards."""
    # console.log ELIG-06: main entry.
    print("[phase2:eligibility] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log ELIG-07: experiment config loaded.
    print("[phase2:eligibility] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    contract_dir = repo_root / "results" / run_id / "contract"
    contracts = [
        json.loads(line)
        for line in open(contract_dir / "task_contracts.jsonl", encoding="utf-8")
    ]
    families = {
        json.loads(line)["task_id"]: json.loads(line)
        for line in open(contract_dir / "contract_families.jsonl", encoding="utf-8")
    }
    touch_frame = pd.read_parquet(contract_dir / "touch_records.parquet")
    pilot = json.loads(
        (repo_root / "results" / run_id / "pilot" / "pilot_ids.json").read_text(
            encoding="utf-8"
        )
    )
    pilot_ids = set(pilot["pilot_ids"])
    # console.log ELIG-08: inputs loaded for eligibility.
    print(
        "[phase2:eligibility] main: contracts=%d touches=%d."
        % (len(contracts), len(touch_frame))
    )
    touches_by_task: dict[str, list[list[str]]] = {}
    for _, row in touch_frame.iterrows():
        touches_by_task.setdefault(row["task_id"], []).append(list(row["touch"]))
    route_rows: list[dict] = []
    primary: list[dict] = []
    partials: list[dict] = []
    failures: list[dict] = []
    for contract in sorted(contracts, key=lambda c: c["task_id"]):
        task_id = contract["task_id"]
        status = families[task_id]["status"]
        q_legal = list(contract["Q"])
        distinct = sorted({tuple(sorted(t)) for t in touches_by_task.get(task_id, [])})
        n_viable, viable_map = count_viable_first_repairs(
            "OPEN", contract["Succ"], contract["Terminal"], 1000
        )
        provenance_complete = all(contract.get("provenance", []))
        route_rows.append(
            {
                "task_id": task_id,
                "domain": contract["domain"],
                "q_legal": len(q_legal),
                "distinct_touches": len(distinct),
                "viable_first_repairs": n_viable,
                "viable_map": viable_map,
                "initial_cert": contract.get("initial_cert"),
                "exact_solvable": True,
                "status": status,
            }
        )
        eligible = (
            status == "IDENTIFIED"
            and contract.get("initial_cert") == "OPEN"
            and len(q_legal) >= 2
            and len(distinct) >= 2
            and n_viable >= 2
            and provenance_complete
            and task_id not in pilot_ids
        )
        # console.log ELIG-09: per-task eligibility decided without outcome values.
        print(
            "[phase2:eligibility] task=%s status=%s viable=%d eligible=%s."
            % (task_id, status, n_viable, eligible)
        )
        if eligible:
            primary.append({"task_id": task_id, "domain": contract["domain"]})
        elif status == "PARTIAL":
            partials.append(
                {"task_id": task_id, "domain": contract["domain"], "reason": "family-disagreement"}
            )
        else:
            failures.append(
                {"task_id": task_id, "reason": "ineligible-primary", "status": status}
            )
    for pid in sorted(pilot_ids):
        failures.append({"task_id": pid, "reason": "excluded_forever_pilot", "status": "EXCLUDED"})
    # console.log ELIG-10: classification complete.
    print(
        "[phase2:eligibility] main: primary=%d partial=%d failures=%d."
        % (len(primary), len(partials), len(failures))
    )
    route_frame = pd.DataFrame(route_rows)
    route_path = contract_dir / "route_classification.parquet"
    route_frame.to_parquet(route_path, index=False)
    # console.log ELIG-11: route classification written.
    print("[phase2:eligibility] main: wrote %s." % route_path.as_posix())
    by_domain: dict[str, int] = {}
    for entry in primary:
        by_domain[entry["domain"]] = by_domain.get(entry["domain"], 0) + 1
    population = {
        "run_id": run_id,
        "track": "N-primary-IDENTIFIED-only",
        "count": len(primary),
        "by_domain": by_domain,
        "task_ids": sorted(e["task_id"] for e in primary),
    }
    population_path = contract_dir / "natural_population.json"
    population_path.write_text(canonical_dumps(population) + "\n", encoding="utf-8")
    # console.log ELIG-12: primary population written.
    print("[phase2:eligibility] main: wrote %s." % population_path.as_posix())
    partial_path = contract_dir / "partial_tasks.jsonl"
    with open(partial_path, "w", encoding="utf-8") as fh:
        for row in sorted(partials, key=lambda r: r["task_id"]):
            fh.write(canonical_dumps(row) + "\n")
    # console.log ELIG-13: partial sidecar written.
    print("[phase2:eligibility] main: wrote %s rows=%d." % (partial_path.as_posix(), len(partials)))
    failures_path = contract_dir / "failure_cards.jsonl"
    with open(failures_path, "w", encoding="utf-8") as fh:
        for row in sorted(failures, key=lambda r: r["task_id"]):
            fh.write(canonical_dumps(row) + "\n")
    # console.log ELIG-14: failure cards written.
    print("[phase2:eligibility] main: wrote %s rows=%d." % (failures_path.as_posix(), len(failures)))
    update_manifest(
        repo_root,
        run_id,
        "results/%s/contract/route_classification.parquet" % run_id,
        route_rows,
    )
    update_manifest(
        repo_root, run_id, "results/%s/contract/natural_population.json" % run_id, population
    )
    update_manifest(
        repo_root, run_id, "results/%s/contract/partial_tasks.jsonl" % run_id, partials
    )
    update_manifest(
        repo_root, run_id, "results/%s/contract/failure_cards.jsonl" % run_id, failures
    )
    # console.log ELIG-15: eligibility pipeline complete.
    print("[phase2:eligibility] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log ELIG-16: script invoked as main.
    print("[phase2:eligibility] __main__: invoking main.")
    raise SystemExit(main())
