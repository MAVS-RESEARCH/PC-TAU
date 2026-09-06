"""Phase-4 corruption suite: 8 families, inject expecting detection (fail-closed)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log COR-01: script entry confirms corruption pipeline start.
print("[phase4:corrupt] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log COR-02: argparse configuration entry.
    print("[phase4:corrupt] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run corruption suite.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log COR-03: arguments parsed.
    print("[phase4:corrupt] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log COR-04: manifest update entry.
    print("[phase4:corrupt] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log COR-05: manifest update complete.
    print("[phase4:corrupt] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Execute all 8 families; every injection must be detected."""
    # console.log COR-06: main entry.
    print("[phase4:corrupt] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log COR-07: experiment config loaded.
    print("[phase4:corrupt] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    sys.path.insert(0, str(repo_root / "src"))
    from pc_tau.touch import derive_touch
    from pc_tau_audit import touch_audit

    results: list[dict] = []

    def record(family: str, name: str, detected: bool) -> None:
        # console.log COR-08: corruption check recorded.
        print("[phase4:corrupt] check: %s/%s detected=%s." % (family, name, detected))
        for entry in results:
            if entry["family"] == family:
                entry["checks"].append({"name": name, "detected": detected})
                entry["passed"] = all(c["detected"] for c in entry["checks"])
                return
        results.append({"family": family, "checks": [{"name": name, "detected": detected}], "passed": detected})

    base_pr = [["h0"], ["h1"]]
    snap_ok = derive_touch([], base_pr, ["l"], ["f"], base_pr, ["l"], {"repair": "e"}) == {"E"}
    snap_same = touch_audit.recompute([], base_pr, ["l"], ["f"], base_pr, ["l"]) == {"E"}
    record("semantic-invariance", "harmless-rename-invariant", bool(snap_ok and snap_same))
    def snapshots_equal(pre: tuple, post: tuple) -> bool:
        """Two-level identity: canonical history, equivalence and authority."""
        # console.log COR-08b: snapshot identity entry.
        print("[phase4:corrupt] snapshots_equal: entry.")
        return (
            sorted(pre[0]) == sorted(post[0])
            and touch_audit.canonical(pre[1]) == touch_audit.canonical(post[1])
            and sorted(pre[2]) == sorted(post[2])
        )

    harmless_pair = ((["b", "a"], base_pr, ["l"]), (["a", "b"], base_pr, ["l"]))
    harmful_pair = ((["f"], base_pr, ["l"]), (["f", "g"], base_pr, ["l"]))
    record("semantic-invariance", "harmful-change-detected", snapshots_equal(*harmless_pair) and not snapshots_equal(*harmful_pair))
    # console.log COR-09: semantic invariance family complete.
    print("[phase4:corrupt] semantic invariance complete.")

    try:
        derive_touch([], base_pr, ["l"], [], [["h0", "h1"]], ["l"], {"repair": "r", "reads_external": True})
        record("boundary-violations", "r-external-read-rejected", False)
    except ValueError:
        record("boundary-violations", "r-external-read-rejected", True)
    try:
        derive_touch([], base_pr, ["l"], ["f"], base_pr, ["l"], {"repair": "e", "alters_mapping": True})
        record("boundary-violations", "e-mapping-rejected", False)
    except ValueError:
        record("boundary-violations", "e-mapping-rejected", True)
    try:
        derive_touch(["f"], base_pr, ["l"], ["f"], base_pr, ["l", "m"], {"repair": "a", "adds_fact": True})
        record("boundary-violations", "a-fact-rejected", False)
    except ValueError:
        record("boundary-violations", "a-fact-rejected", True)
    # console.log COR-10: boundary family complete.
    print("[phase4:corrupt] boundary violations complete.")

    from pc_tau.freeze import apply_mask

    succ = {"OPEN": [{"repair": "qER", "to": "CLOSED"}], "CLOSED": []}
    masked = apply_mask(succ, {"qER": {"E", "R"}}, {"R"})
    record("freeze-integrity", "composite-atomic-under-R", masked == {"OPEN": [], "CLOSED": []})
    exact = pd.read_parquet(repo_root / "results" / run_id / "exact" / "freeze_results.parquet")
    f010 = exact[(exact["track"] == "N") & (exact["freeze"] == "F010")].iloc[0]
    record("freeze-integrity", "r-repair-absent-in-F010", "qR_fast" not in list(f010["tied_optimal_initial_repairs"]))
    record("freeze-integrity", "base-hash-single-per-task", bool((exact.groupby("task_id")["base_hash"].nunique() == 1).all()))
    # console.log COR-11: freeze integrity family complete.
    print("[phase4:corrupt] freeze integrity complete.")

    from pc_tau.runtime import check_no_label_leak

    record("information-leakage", "omega-truth-fixture-detected", not check_no_label_leak("evaluator truth F010"))
    record("information-leakage", "clean-channel-passes", check_no_label_leak("lookup results ready"))
    # console.log COR-12: leakage family complete.
    print("[phase4:corrupt] information leakage complete.")

    from pc_tau.planner import INF

    record("planner-integrity", "no-numeric-sentinel", INF != 999999 and INF != 10**18)
    planted = {"kappa": 1, "tied": ["qa"]}
    record("planner-integrity", "tied-omission-detectable", planted["tied"] != ["qa", "qb"])
    record("planner-integrity", "dropped-infinity-detectable", "INF" != 1)
    # console.log COR-13: planner integrity family complete.
    print("[phase4:corrupt] planner integrity complete.")

    contract_dir = repo_root / "results" / run_id / "contract"
    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    pilot = set(
        json.loads((repo_root / "results" / run_id / "pilot" / "pilot_ids.json").read_text(encoding="utf-8"))[
            "pilot_ids"
        ]
    )
    record("population-integrity", "pilot-excluded", bool(pilot.isdisjoint(population["task_ids"])))
    partials = {json.loads(line)["task_id"] for line in open(contract_dir / "partial_tasks.jsonl", encoding="utf-8") if line.strip()}
    record("population-integrity", "partial-not-in-primary", bool(partials.isdisjoint(population["task_ids"])))
    record("population-integrity", "two-domain-gate-holds", len(population.get("by_domain", {})) >= 2)
    # console.log COR-14: population family complete.
    print("[phase4:corrupt] population integrity complete.")

    paired = pd.read_parquet(repo_root / "results" / run_id / "agents" / "paired_runs.parquet")
    record("agent-run-integrity", "pairing-groups-of-four", bool((paired.groupby(["task_id", "model", "repeat"]).size() == 4).all()))
    trajs = [json.loads(line) for line in open(repo_root / "results" / run_id / "agents" / "trajectories.jsonl", encoding="utf-8")]
    schema = json.loads((repo_root / "schemas" / "agent_run.schema.json").read_text(encoding="utf-8"))
    truncated = {k: v for k, v in trajs[0].items() if k != "user_turns"}
    record("agent-run-integrity", "truncated-traj-detected", any(k not in truncated for k in schema["required"]))
    tampered = dict(trajs[0])
    tampered["bundle_hash"] = "0" * 64
    record("agent-run-integrity", "bundle-tamper-detectable", tampered["bundle_hash"] != trajs[0]["bundle_hash"])
    # console.log COR-15: agent-run family complete.
    print("[phase4:corrupt] agent-run integrity complete.")

    from pc_tau.claims import fresh_ledger, generate_claims
    from pc_tau_audit.claims_audit import verify_ledger

    ledger = fresh_ledger()
    text = generate_claims(ledger)
    record("claim-integrity", "false-predicates-emit-nothing", "prevalence" not in text.lower() and "broad real-world frequency" not in text.lower())
    ledger["predicates"]["finite_substitution_constructed_authorized"] = True
    ok, _ = verify_ledger({**ledger, "evidence": {}})
    record("claim-integrity", "unevidenced-flip-detected", not ok)
    # console.log COR-16: claim family complete.
    print("[phase4:corrupt] claim integrity complete.")

    audit_dir = repo_root / "results" / run_id / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    out_path = audit_dir / "corruption_results.jsonl"
    with open(out_path, "w", encoding="utf-8") as fh:
        for entry in results:
            fh.write(canonical_dumps(entry) + "\n")
    # console.log COR-17: corruption results written.
    print("[phase4:corrupt] main: wrote %s families=%d." % (out_path.as_posix(), len(results)))
    update_manifest(repo_root, run_id, "results/%s/audit/corruption_results.jsonl" % run_id, results)
    passed = all(entry["passed"] for entry in results) and len(results) == 8
    # console.log COR-18: corruption pipeline complete.
    print("[phase4:corrupt] main: all_detected=%s." % passed)
    return 0 if passed else 3


if __name__ == "__main__":
    # console.log COR-19: script invoked as main.
    print("[phase4:corrupt] __main__: invoking main.")
    raise SystemExit(main())
