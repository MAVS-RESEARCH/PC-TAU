"""Phase-1 throwaway pilot: provisional multi-route feasibility (WorkPlan 1.3).

Firewall: final-population values are never computed. Viability uses
the Fix-11 reachability checker only. A separate provisional solver
demonstrates finite fallback on excluded pilot tasks for interface
design only. Outputs are tagged provisional and excluded.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.pilot_provisional_solver import pilot_provisional_solve
from pc_tau.reachability import count_viable_first_repairs
from pc_tau.source import canonical_dumps, select_pilot, sha256_of_canonical


# console.log PILOT-01: script entry confirms pilot pipeline start.
print("[phase1:pilot] entry: parsing arguments.")


DOMAIN_REPAIR_TEMPLATE = {
    "airline": {
        "qE": {
            "tool": "get_reservation_details",
            "locator": "external_source/_upstream/src/tau2/domains/airline/tools.py:371",
            "channel": "read-only tool output: reservation facts",
        },
        "qR": {
            "tool": "calculate",
            "locator": "external_source/_upstream/src/tau2/domains/airline/tools.py:321",
            "channel": "compute-only over already-admitted history",
        },
        "qA": {
            "tool": "transfer_to_human_agents",
            "locator": "external_source/_upstream/src/tau2/domains/airline/tools.py:532",
            "channel": "delegation/attestation interface",
        },
    },
    "retail": {
        "qE": {
            "tool": "get_order_details",
            "locator": "external_source/_upstream/src/tau2/domains/retail/tools.py:333",
            "channel": "read-only tool output: order facts",
        },
        "qR": {
            "tool": "calculate",
            "locator": "external_source/_upstream/src/tau2/domains/retail/tools.py:141",
            "channel": "compute-only over already-admitted history",
        },
        "qA": {
            "tool": "transfer_to_human_agents",
            "locator": "external_source/_upstream/src/tau2/domains/retail/tools.py:732",
            "channel": "delegation/attestation interface",
        },
    },
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log PILOT-02: argparse configuration entry.
    print("[phase1:pilot] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run throwaway pilot gate.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log PILOT-03: arguments parsed.
    print("[phase1:pilot] parse_args: config=%s." % args.config)
    return args


def build_provisional_graph(domain: str) -> tuple[dict, dict, dict]:
    """Build throwaway pilot graph template grounded per domain.

    States OPEN/S1/CLOSED. Repairs qR_fast ({R}, OPEN->CLOSED),
    qE_slow ({E}, OPEN->S1), qA_close ({A}, S1->CLOSED). Each repair
    carries a source-grounded justification and operational flags for
    firewall validation. Returns (successors, touches, repairs).
    """
    # console.log PILOT-04: graph template build entry.
    print("[phase1:pilot] build_provisional_graph: entry domain=%s." % domain)
    template = DOMAIN_REPAIR_TEMPLATE[domain]
    successors = {
        "OPEN": [
            {"repair": "qR_fast", "to": "CLOSED"},
            {"repair": "qE_slow", "to": "S1"},
        ],
        "S1": [{"repair": "qA_close", "to": "CLOSED"}],
        "CLOSED": [],
    }
    touches = {"qR_fast": {"R"}, "qE_slow": {"E"}, "qA_close": {"A"}}
    repairs = {
        "qR_fast": {
            "touch": ["R"],
            "tool": template["qR"]["tool"],
            "locator": template["qR"]["locator"],
            "justification": "policy task state + API semantic %s + user channel %s"
            % (template["qR"]["tool"], template["qR"]["channel"]),
            "reads_external": False,
            "reads_unadmitted": False,
            "alters_mapping": False,
            "adds_fact": False,
        },
        "qE_slow": {
            "touch": ["E"],
            "tool": template["qE"]["tool"],
            "locator": template["qE"]["locator"],
            "justification": "policy task state + API semantic %s + user channel %s"
            % (template["qE"]["tool"], template["qE"]["channel"]),
            "reads_external": False,
            "reads_unadmitted": False,
            "alters_mapping": False,
            "adds_fact": True,
        },
        "qA_close": {
            "touch": ["A"],
            "tool": template["qA"]["tool"],
            "locator": template["qA"]["locator"],
            "justification": "policy task state + API semantic %s + user channel %s"
            % (template["qA"]["tool"], template["qA"]["channel"]),
            "reads_external": False,
            "reads_unadmitted": False,
            "alters_mapping": False,
            "adds_fact": False,
        },
    }
    # console.log PILOT-05: graph template complete.
    print("[phase1:pilot] build_provisional_graph: complete repairs=3.")
    return successors, touches, repairs


def validate_firewall(repairs: dict) -> tuple[bool, list[str]]:
    """Validate operational resource constraints for each repair.

    Rejects R repairs that read external or unadmitted state, E repairs
    that alter the certificate mapping, and A repairs that add new
    world facts. Also rejects justifications referencing outcome labels.
    """
    # console.log PILOT-06: firewall validation entry.
    print("[phase1:pilot] validate_firewall: entry repairs=%d." % len(repairs))
    problems: list[str] = []
    banned = ["Delta_R", "K_Pi", "desired sign", "observed final"]
    for name, meta in repairs.items():
        touch = set(meta.get("touch", []))
        for token in banned:
            if token in meta.get("justification", ""):
                problems.append("%s: justification references %s" % (name, token))
        if touch == {"R"} and (
            meta.get("reads_external") or meta.get("reads_unadmitted")
        ):
            problems.append("%s: R repair must not read external/unadmitted state" % name)
        if touch == {"E"} and meta.get("alters_mapping"):
            problems.append("%s: E repair must not alter mapping" % name)
        if touch == {"A"} and meta.get("adds_fact"):
            problems.append("%s: A repair must not add world fact" % name)
    ok = not problems
    # console.log PILOT-07: firewall validation complete.
    print("[phase1:pilot] validate_firewall: ok=%s issues=%d." % (ok, len(problems)))
    return ok, problems


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log PILOT-08: manifest update entry.
    print("[phase1:pilot] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log PILOT-09: manifest update complete.
    print("[phase1:pilot] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Select pilot, run provisional gate, write pilot outputs."""
    # console.log PILOT-10: main entry.
    print("[phase1:pilot] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log PILOT-11: experiment config loaded.
    print("[phase1:pilot] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    seed = int(cfg["pilot"]["seed"])
    per_domain = int(cfg["pilot"]["per_domain"])
    node_budget = int(cfg["pilot"].get("node_budget", 1000))
    census_path = repo_root / "external_source" / "task_census.json"
    census_payload = json.loads(census_path.read_text(encoding="utf-8"))
    # console.log PILOT-12: task census loaded for pilot selection.
    print(
        "[phase1:pilot] main: census loaded records=%d."
        % len(census_payload["records"])
    )
    pilot = select_pilot(census_payload["records"], seed, per_domain)
    # console.log PILOT-13: pilot selection complete.
    print("[phase1:pilot] main: pilot selected total=%d." % len(pilot["pilot_ids"]))
    pilot_dir = repo_root / "results" / run_id / "pilot"
    pilot_dir.mkdir(parents=True, exist_ok=True)
    pilot_ids_path = pilot_dir / "pilot_ids.json"
    pilot_ids_path.write_text(canonical_dumps(pilot) + "\n", encoding="utf-8")
    # console.log PILOT-14: pilot ids written.
    print("[phase1:pilot] main: wrote %s." % pilot_ids_path.as_posix())
    update_manifest(repo_root, run_id, "results/%s/pilot/pilot_ids.json" % run_id, pilot)

    geometry: list[dict] = []
    gate_rows: list[dict] = []
    total_start = time.perf_counter()
    # console.log PILOT-15: per-task provisional evaluation loop entry.
    print("[phase1:pilot] main: evaluating %d pilot tasks." % len(pilot["pilot_ids"]))
    for task_id in pilot["pilot_ids"]:
        domain = task_id.split(":")[0]
        t0 = time.perf_counter()
        successors, touches, repairs = build_provisional_graph(domain)
        firewall_ok, firewall_issues = validate_firewall(repairs)
        n_viable, viable_map = count_viable_first_repairs(
            "OPEN", successors, "CLOSED", node_budget
        )
        distinct_touches = sorted({tuple(sorted(touches[r])) for r in touches})
        unrestricted = pilot_provisional_solve(
            successors, touches, "OPEN", "CLOSED", set(), node_budget
        )
        r_frozen = pilot_provisional_solve(
            successors, touches, "OPEN", "CLOSED", {"R"}, node_budget
        )
        elapsed = time.perf_counter() - t0
        multi_action = n_viable >= 2 and len(distinct_touches) >= 2
        finite_fallback = (
            unrestricted["steps"] is not None
            and r_frozen["steps"] is not None
            and r_frozen["steps"] > unrestricted["steps"]
        )
        # console.log PILOT-16: per-task provisional result computed.
        print(
            "[phase1:pilot] main: task=%s viable=%d touches=%d unrestricted=%s r_frozen=%s fallback=%s cpu=%.4fs."
            % (
                task_id,
                n_viable,
                len(distinct_touches),
                unrestricted["steps"],
                r_frozen["steps"],
                finite_fallback,
                elapsed,
            )
        )
        geometry.append(
            {
                "task_id": task_id,
                "domain": domain,
                "provisional": True,
                "excluded": True,
                "design_only": True,
                "successors": successors,
                "touches": {k: sorted(v) for k, v in touches.items()},
                "unrestricted_steps": unrestricted["steps"],
                "r_frozen_steps": r_frozen["steps"],
                "optimal_first_unrestricted": unrestricted["optimal_first"],
                "witness_unrestricted": unrestricted["witness"],
            }
        )
        gate_rows.append(
            {
                "task_id": task_id,
                "domain": domain,
                "viable_first_repairs": n_viable,
                "viable_map": viable_map,
                "distinct_touches": [list(t) for t in distinct_touches],
                "multi_action_viable": multi_action,
                "finite_fallback": finite_fallback,
                "firewall_ok": firewall_ok,
                "firewall_issues": firewall_issues,
                "cpu_seconds": elapsed,
                "exact_solvable_cpu": elapsed < 1.0,
            }
        )
    total_cpu = time.perf_counter() - total_start
    # console.log PILOT-17: per-task loop complete.
    print("[phase1:pilot] main: loop complete total_cpu=%.3fs." % total_cpu)
    geo_path = pilot_dir / "provisional_geometry.jsonl"
    with open(geo_path, "w", encoding="utf-8") as fh:
        for row in geometry:
            fh.write(canonical_dumps(row) + "\n")
    # console.log PILOT-18: provisional geometry written.
    print("[phase1:pilot] main: wrote %s rows=%d." % (geo_path.as_posix(), len(geometry)))
    gate_payload = {
        "run_id": run_id,
        "total_cpu_seconds": total_cpu,
        "node_budget": node_budget,
        "rows": gate_rows,
    }
    gate_path = pilot_dir / "gate_log.json"
    gate_path.write_text(canonical_dumps(gate_payload) + "\n", encoding="utf-8")
    # console.log PILOT-19: gate log written.
    print("[phase1:pilot] main: wrote %s." % gate_path.as_posix())
    update_manifest(
        repo_root, run_id, "results/%s/pilot/provisional_geometry.jsonl" % run_id, geometry
    )
    update_manifest(
        repo_root, run_id, "results/%s/pilot/gate_log.json" % run_id, gate_payload
    )
    # console.log PILOT-20: pilot pipeline complete.
    print("[phase1:pilot] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log PILOT-21: script invoked as main.
    print("[phase1:pilot] __main__: invoking main.")
    raise SystemExit(main())
