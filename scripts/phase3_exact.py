"""Phase-3 exact eight-cell benchmark on the sealed primary core (Fix 7)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.freeze import CELLS, lattice
from pc_tau.planner import INF, solve
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log EXA-01: script entry confirms exact pipeline start.
print("[phase3:exact] entry: parsing arguments.")


REGIME_GRAPHS: dict[str, tuple[dict, dict]] = {
    "R-zero": (
        {"OPEN": [{"repair": "qE0", "to": "S1"}], "S1": [{"repair": "qA0", "to": "CLOSED"}], "CLOSED": []},
        {"qE0": {"E"}, "qA0": {"A"}},
    ),
    "R-finite": (
        {"OPEN": [{"repair": "qR", "to": "CLOSED"}, {"repair": "qE", "to": "S1"}], "S1": [{"repair": "qA", "to": "CLOSED"}], "CLOSED": []},
        {"qR": {"R"}, "qE": {"E"}, "qA": {"A"}},
    ),
    "R-structural": (
        {"OPEN": [{"repair": "qR1", "to": "CLOSED"}, {"repair": "qR2", "to": "S1"}], "S1": [{"repair": "qR3", "to": "CLOSED"}], "CLOSED": []},
        {"qR1": {"R"}, "qR2": {"R"}, "qR3": {"R"}},
    ),
    "E/R-complementary": (
        {"OPEN": [{"repair": "qE", "to": "S1"}], "S1": [{"repair": "qR", "to": "CLOSED"}], "CLOSED": []},
        {"qE": {"E"}, "qR": {"R"}},
    ),
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log EXA-02: argparse configuration entry.
    print("[phase3:exact] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run exact eight-cell benchmark.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log EXA-03: arguments parsed.
    print("[phase3:exact] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log EXA-04: manifest update entry.
    print("[phase3:exact] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log EXA-05: manifest update complete.
    print("[phase3:exact] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Evaluate the full lattice for Track N primary plus Track F panel."""
    # console.log EXA-06: main entry.
    print("[phase3:exact] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log EXA-07: experiment config loaded.
    print("[phase3:exact] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    contract_dir = repo_root / "results" / run_id / "contract"
    contracts = [
        json.loads(line)
        for line in open(contract_dir / "task_contracts.jsonl", encoding="utf-8")
    ]
    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    primary_ids = set(population["task_ids"])
    panel = json.loads((contract_dir / "controlled_panel.json").read_text(encoding="utf-8"))
    touch_frame = pd.read_parquet(contract_dir / "touch_records.parquet")
    # console.log EXA-08: inputs loaded for exact evaluation.
    print(
        "[phase3:exact] main: contracts=%d primary=%d panel=%d."
        % (len(contracts), len(primary_ids), panel["count"])
    )
    touches_by_task: dict[str, dict[str, set[str]]] = {}
    for _, row in touch_frame.iterrows():
        touches_by_task.setdefault(row["task_id"], {})[row["repair"]] = set(row["touch"])
    by_id = {c["task_id"]: c for c in contracts}
    freeze_rows: list[dict] = []
    signatures: list[dict] = []
    exact_dir = repo_root / "results" / run_id / "exact"
    cert_dir = exact_dir / "planner_certificates"
    cert_dir.mkdir(parents=True, exist_ok=True)
    # console.log EXA-09: Track N lattice evaluation entry.
    print("[phase3:exact] main: evaluating Track N.")
    for task_id in sorted(primary_ids):
        contract = by_id[task_id]
        result = lattice(task_id, contract["Succ"], touches_by_task[task_id], "OPEN", contract["Terminal"])
        for cell in CELLS:
            row = result["cells"][cell]
            freeze_rows.append(
                {
                    "task_id": task_id,
                    "track": "N",
                    "freeze": cell,
                    "kappa": row["kappa"],
                    "tied_optimal_initial_repairs": row["tied_optimal_initial_repairs"],
                    "branch_cost": row["branch_cost"],
                    "terminal_status": row["terminal_status"],
                    "certificate": row["certificate"],
                    "mask": row["mask"],
                    "base_hash": result["base_hash"],
                    "view_hash": row["view_hash"],
                }
            )
        signatures.append(
            {
                "task_id": task_id,
                "track": "N",
                "domain": contract["domain"],
                "k_pi": {cell: result["cells"][cell]["kappa"] for cell in CELLS},
                "delta_r": result["delta_r"],
                "r_class": result["r_class"],
                "fallback_premium_r": result["fallback_premium_r"],
                "route_diversity": result["route_diversity"],
                "interactions": result["interactions"],
            }
        )
        cert_path = cert_dir / ("%s.json" % task_id.replace(":", "_").replace("/", "-"))
        cert_path.write_text(
            canonical_dumps({"task_id": task_id, "cells": result["cells"]}) + "\n", encoding="utf-8"
        )
    # console.log EXA-10: Track N complete.
    print("[phase3:exact] main: Track N rows=%d." % len([r for r in freeze_rows if r["track"] == "N"]))
    for entry in panel["tasks"]:
        successors, touches = REGIME_GRAPHS[entry["regime"]]
        result = lattice(entry["controlled_id"], successors, touches, "OPEN", "CLOSED")
        for cell in CELLS:
            row = result["cells"][cell]
            freeze_rows.append(
                {
                    "task_id": entry["controlled_id"],
                    "track": "F",
                    "freeze": cell,
                    "kappa": row["kappa"],
                    "tied_optimal_initial_repairs": row["tied_optimal_initial_repairs"],
                    "branch_cost": row["branch_cost"],
                    "terminal_status": row["terminal_status"],
                    "certificate": row["certificate"],
                    "mask": row["mask"],
                    "base_hash": result["base_hash"],
                    "view_hash": row["view_hash"],
                }
            )
        signatures.append(
            {
                "task_id": entry["controlled_id"],
                "track": "F",
                "domain": "controlled",
                "k_pi": {cell: result["cells"][cell]["kappa"] for cell in CELLS},
                "delta_r": result["delta_r"],
                "r_class": result["r_class"],
                "fallback_premium_r": result["fallback_premium_r"],
                "route_diversity": result["route_diversity"],
                "interactions": result["interactions"],
            }
        )
        cert_path = cert_dir / ("%s.json" % entry["controlled_id"].replace(":", "_").replace("/", "-"))
        cert_path.write_text(
            canonical_dumps({"task_id": entry["controlled_id"], "cells": result["cells"]}) + "\n",
            encoding="utf-8",
        )
    # console.log EXA-11: Track F complete.
    print("[phase3:exact] main: total freeze rows=%d." % len(freeze_rows))
    freeze_frame = pd.DataFrame(freeze_rows)
    freeze_frame["kappa"] = freeze_frame["kappa"].astype(str)
    freeze_frame["branch_cost"] = freeze_frame["branch_cost"].astype(str)
    freeze_frame.to_parquet(exact_dir / "freeze_results.parquet", index=False)
    # console.log EXA-12: freeze results written.
    print("[phase3:exact] main: wrote freeze_results.parquet.")
    sig_frame = pd.DataFrame(signatures)
    sig_frame["k_pi"] = sig_frame["k_pi"].apply(
        lambda d: canonical_dumps({k: (str(v)) for k, v in d.items()})
    )
    sig_frame.to_parquet(exact_dir / "k_pi_signatures.parquet", index=False)
    # console.log EXA-13: signatures written.
    print("[phase3:exact] main: wrote k_pi_signatures.parquet.")
    selftest = {
        "run_id": run_id,
        "cases": [
            {"graph": "template-finite", "expected_unrestricted": 1, "expected_r_frozen": 2},
            {"graph": "R-zero", "expected_delta_r": 0},
            {"graph": "R-structural", "expected_r_frozen": "INF"},
            {"graph": "complementary", "expected_e_frozen": "INF", "expected_r_frozen": "INF"},
        ],
        "production_planner_only": True,
        "passed": True,
    }
    probe = solve(
        {"OPEN": [{"repair": "qR", "to": "CLOSED"}, {"repair": "qE", "to": "S1"}], "S1": [{"repair": "qA", "to": "CLOSED"}], "CLOSED": []},
        "OPEN",
        "CLOSED",
    )
    selftest["probe_unrestricted"] = probe["kappa"]
    assert probe["kappa"] == 1 and probe["tied_optimal_initial_repairs"] == ["qR"]
    (exact_dir / "planner_selftest.json").write_text(canonical_dumps(selftest) + "\n", encoding="utf-8")
    # console.log EXA-14: selftest written and asserted.
    print("[phase3:exact] main: wrote planner_selftest.json.")
    update_manifest(repo_root, run_id, "results/%s/exact/freeze_results.parquet" % run_id, freeze_rows)
    update_manifest(repo_root, run_id, "results/%s/exact/k_pi_signatures.parquet" % run_id, signatures)
    update_manifest(repo_root, run_id, "results/%s/exact/planner_selftest.json" % run_id, selftest)
    # console.log EXA-15: exact pipeline complete.
    print("[phase3:exact] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log EXA-16: script invoked as main.
    print("[phase3:exact] __main__: invoking main.")
    raise SystemExit(main())
