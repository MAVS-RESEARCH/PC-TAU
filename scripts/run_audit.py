"""Phase-4 independent rebuild orchestrator with module-boundary guard."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical
from pc_tau_audit import contract_audit, planner_audit, run_audit, source_audit, touch_audit


# console.log RUA-01: script entry confirms rebuild pipeline start.
print("[phase4:run-audit] entry: parsing arguments.")


BANNED = {"semantics", "touch", "freeze", "planner", "metrics", "claims"}


def enforce_boundary() -> None:
    """Fail if a banned production module is already imported."""
    # console.log RUA-02: boundary enforcement entry.
    print("[phase4:run-audit] enforce_boundary: entry.")
    violators = sorted(name for name in sys.modules if name in {"pc_tau." + leaf for leaf in BANNED})
    if violators:
        raise SystemExit("audit boundary violated by %s" % violators)
    # console.log RUA-03: boundary holds.
    print("[phase4:run-audit] enforce_boundary: holds.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log RUA-04: argparse configuration entry.
    print("[phase4:run-audit] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Rebuild from frozen evidence.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log RUA-05: arguments parsed.
    print("[phase4:run-audit] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log RUA-06: manifest update entry.
    print("[phase4:run-audit] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log RUA-07: manifest update complete.
    print("[phase4:run-audit] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Rebuild all six layers and compare against sealed outputs."""
    # console.log RUA-08: main entry.
    print("[phase4:run-audit] main: entry.")
    enforce_boundary()
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log RUA-09: experiment config loaded.
    print("[phase4:run-audit] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    contract_dir = repo_root / "results" / run_id / "contract"
    audit_dir = repo_root / "results" / run_id / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    layers: dict[str, bool] = {}

    upstream = source_audit.rehash_source(repo_root / cfg["upstream"]["dir"])
    manifest = json.loads((repo_root / "external_source" / "source_manifest.json").read_text(encoding="utf-8"))
    layers["source"] = upstream["commit_sha"] == manifest["commit_sha"] and upstream["tree_hash"] == manifest["tree_hash"]
    independent_source = {"run_id": run_id, **upstream}
    (audit_dir / "independent_source.json").write_text(canonical_dumps(independent_source) + "\n", encoding="utf-8")
    # console.log RUA-10: source layer rebuilt.
    print("[phase4:run-audit] main: source equal=%s." % layers["source"])

    contracts = [json.loads(line) for line in open(contract_dir / "task_contracts.jsonl", encoding="utf-8")]
    rebuilt_contracts: list[dict] = []
    family_ok = True
    disagreements: dict[str, list[str]] = {}
    with open(contract_dir / "extraction_records.jsonl", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            if rec["verdict"] == "disagree":
                disagreements.setdefault(rec["task_id"], []).append(rec["kind"])
    for contract in contracts:
        rebuilt = contract_audit.rebuild_contract(contract["task_id"], contract["domain"], contract["provenance"])
        rebuilt_contracts.append(rebuilt)
        for key in ["U_H", "H", "P_R", "Lambda", "omega", "Q", "Succ", "Terminal", "A_Pi", "initial_cert"]:
            if rebuilt[key] != contract[key]:
                family_ok = False
        status = contract_audit.rebuild_family(contract["task_id"], disagreements.get(contract["task_id"], []), bool(contract["provenance"]))
        sealed_status = next(f for f in map(json.loads, open(contract_dir / "contract_families.jsonl", encoding="utf-8")) if f["task_id"] == contract["task_id"])["status"]
        if status != sealed_status:
            family_ok = False
    layers["contract"] = family_ok
    (audit_dir / "independent_contracts.jsonl").write_text(
        "".join(canonical_dumps(c) + "\n" for c in rebuilt_contracts), encoding="utf-8"
    )
    # console.log RUA-11: contract layer rebuilt.
    print("[phase4:run-audit] main: contract equal=%s." % layers["contract"])

    touch_rows: list[dict] = []
    sealed_touch = pd.read_parquet(contract_dir / "touch_records.parquet")
    touch_ok = True
    edges = [("OPEN", "qR_fast", "CLOSED_R"), ("OPEN", "qE_slow", "S1"), ("S1", "qA_close", "CLOSED_A")]
    for contract in contracts:
        snap = touch_audit.snapshots(contract["domain"])
        for pre, rep, post in edges:
            got = touch_audit.recompute(
                snap[pre]["H"], snap[pre]["P_R"], snap[pre]["Lambda"],
                snap[post]["H"], snap[post]["P_R"], snap[post]["Lambda"],
            )
            sealed = set(sealed_touch[(sealed_touch["task_id"] == contract["task_id"]) & (sealed_touch["repair"] == rep)].iloc[0]["touch"])
            if got != sealed:
                touch_ok = False
            touch_rows.append({"task_id": contract["task_id"], "repair": rep, "touch": sorted(got)})
    layers["touch"] = touch_ok
    pd.DataFrame(touch_rows).to_parquet(audit_dir / "independent_touch.parquet", index=False)
    # console.log RUA-12: touch layer rebuilt.
    print("[phase4:run-audit] main: touch equal=%s." % layers["touch"])

    exact = pd.read_parquet(repo_root / "results" / run_id / "exact" / "freeze_results.parquet")
    masks = {"F000": set(), "F100": {"E"}, "F010": {"R"}, "F001": {"A"}, "F110": {"E", "R"}, "F101": {"E", "A"}, "F011": {"R", "A"}, "F111": {"E", "R", "A"}}
    touches_by_task: dict[str, dict[str, set[str]]] = {}
    for _, row in sealed_touch.iterrows():
        touches_by_task.setdefault(row["task_id"], {})[row["repair"]] = set(row["touch"])
    by_id = {c["task_id"]: c for c in contracts}
    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    agreement_rows: list[dict] = []
    planner_ok = True
    indep_rows: list[dict] = []
    for task_id in sorted(population["task_ids"]):
        contract = by_id[task_id]
        for cell, frozen in masks.items():
            masked = {s: [e for e in edges if set(touches_by_task[task_id].get(e["repair"], set())).isdisjoint(frozen)] for s, edges in contract["Succ"].items()}
            indep = planner_audit.solve_deepening(masked, "OPEN", contract["Terminal"])
            sealed = exact[(exact["task_id"] == task_id) & (exact["freeze"] == cell)].iloc[0]
            sealed_finite = sealed["kappa"] != "INF"
            match = (indep["closed"] == bool(sealed_finite)) and (
                (not indep["closed"]) or (indep["kappa"] == int(sealed["kappa"]) and sorted(indep["optimal_first"]) == sorted(sealed["tied_optimal_initial_repairs"]))
            )
            if not match:
                planner_ok = False
            agreement_rows.append({"task_id": task_id, "freeze": cell, "match": bool(match)})
            indep_rows.append({"task_id": task_id, "freeze": cell, "kappa": ("INF" if indep["kappa"] is None else str(indep["kappa"])), "tied": indep["optimal_first"]})
    layers["planner"] = planner_ok
    (audit_dir / "planner_agreement.json").write_text(
        canonical_dumps({"run_id": run_id, "rows": agreement_rows, "agreement": float(sum(r["match"] for r in agreement_rows) / len(agreement_rows))}) + "\n",
        encoding="utf-8",
    )
    pd.DataFrame(indep_rows).to_parquet(audit_dir / "independent_exact_results.parquet", index=False)
    # console.log RUA-13: planner layer compared.
    print("[phase4:run-audit] main: planner agreement=%s." % layers["planner"])

    metrics = pd.read_parquet(repo_root / "results" / run_id / "agents" / "metrics.parquet")
    trajs = [json.loads(line) for line in open(repo_root / "results" / run_id / "agents" / "trajectories.jsonl", encoding="utf-8")]
    sig = pd.read_parquet(repo_root / "results" / run_id / "exact" / "k_pi_signatures.parquet")
    kappa_of = {(r["task_id"], r["freeze"]): (None if r["kappa"] == "INF" else int(r["kappa"])) for _, r in exact.iterrows()}
    tied_of = {(r["task_id"], r["freeze"]): list(r["tied_optimal_initial_repairs"]) for _, r in exact.iterrows()}
    preferred = {"family-a": None, "family-b": "qR_fast", "family-c": "qE_slow"}
    recomputed: list[dict] = []
    run_ok = True
    for traj in trajs:
        key = (traj["task_id"], traj["condition"])
        rec = run_audit.recompute_episode(
            traj["repairs_attempted"], traj["escalated"], traj["violations"],
            kappa_of[key], tied_of[key], preferred[traj["model"]],
        )
        rec.update({"task_id": traj["task_id"], "model": traj["model"], "condition": traj["condition"], "repeat": traj["repeat"]})
        recomputed.append(rec)
    for rec in recomputed:
        sealed = metrics[(metrics["task_id"] == rec["task_id"]) & (metrics["model"] == rec["model"]) & (metrics["condition"] == rec["condition"]) & (metrics["repeat"] == rec["repeat"])].iloc[0]
        for field in ["route_discovery", "optimal_route", "freeze_adaptation", "excess_escalation", "governance_correct"]:
            if bool(sealed[field]) != rec[field]:
                run_ok = False
        sealed_regret = sealed["repair_regret"]
        sealed_none = sealed_regret is None or (isinstance(sealed_regret, float) and sealed_regret != sealed_regret)
        if sealed_none != (rec["repair_regret"] is None) or (not sealed_none and float(sealed_regret) != rec["repair_regret"]):
            run_ok = False
    layers["run"] = run_ok
    pd.DataFrame(recomputed).to_parquet(audit_dir / "independent_agent_metrics.parquet", index=False)
    # console.log RUA-14: run layer rebuilt.
    print("[phase4:run-audit] main: run equal=%s." % layers["run"])

    audit_report = {"run_id": run_id, "layers": layers, "all_equal": all(layers.values())}
    (audit_dir / "audit.json").write_text(canonical_dumps(audit_report) + "\n", encoding="utf-8")
    # console.log RUA-15: audit report written.
    print("[phase4:run-audit] main: all_equal=%s." % audit_report["all_equal"])
    for rel, obj in [
        ("results/%s/audit/independent_source.json" % run_id, independent_source),
        ("results/%s/audit/independent_contracts.jsonl" % run_id, rebuilt_contracts),
        ("results/%s/audit/independent_touch.parquet" % run_id, touch_rows),
        ("results/%s/audit/independent_exact_results.parquet" % run_id, indep_rows),
        ("results/%s/audit/independent_agent_metrics.parquet" % run_id, recomputed),
        ("results/%s/audit/planner_agreement.json" % run_id, {"agreement": audit_report["all_equal"]}),
        ("results/%s/audit/audit.json" % run_id, audit_report),
    ]:
        update_manifest(repo_root, run_id, rel, obj)
    # console.log RUA-16: rebuild pipeline complete.
    print("[phase4:run-audit] main: complete run-id=%s." % run_id)
    return 0 if audit_report["all_equal"] else 4


if __name__ == "__main__":
    # console.log RUA-17: script invoked as main.
    print("[phase4:run-audit] __main__: invoking main.")
    raise SystemExit(main())
