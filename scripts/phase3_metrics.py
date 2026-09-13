"""Phase-3 metrics: seven paired metrics plus bootstrap summaries."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.metrics import bootstrap_mean_ci, repair_regret, summarize_episode
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log METR-01: script entry confirms metrics pipeline start.
print("[phase3:metrics] entry: parsing arguments.")


PRIMARY_CELLS = ["F000", "F100", "F010", "F001"]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log METR-02: argparse configuration entry.
    print("[phase3:metrics] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Compute paired metrics.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log METR-03: arguments parsed.
    print("[phase3:metrics] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log METR-04: manifest update entry.
    print("[phase3:metrics] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log METR-05: manifest update complete.
    print("[phase3:metrics] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Join exact ground truth with trajectories into metrics and summary."""
    # console.log METR-06: main entry.
    print("[phase3:metrics] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log METR-07: experiment config loaded.
    print("[phase3:metrics] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    exact = pd.read_parquet(repo_root / "results" / run_id / "exact" / "freeze_results.parquet")
    sig = pd.read_parquet(repo_root / "results" / run_id / "exact" / "k_pi_signatures.parquet")
    trajectories = [
        json.loads(line)
        for line in open(repo_root / "results" / run_id / "agents" / "trajectories.jsonl", encoding="utf-8")
    ]
    # console.log METR-08: inputs loaded for metrics.
    print(
        "[phase3:metrics] main: exact=%d sig=%d trajs=%d."
        % (len(exact), len(sig), len(trajectories))
    )
    kappa_of: dict[tuple[str, str], int | None] = {}
    tied_of: dict[tuple[str, str], list] = {}
    for _, row in exact.iterrows():
        kappa_of[(row["task_id"], row["freeze"])] = (
            None if row["kappa"] == "INF" else int(row["kappa"])
        )
        tied_of[(row["task_id"], row["freeze"])] = list(row["tied_optimal_initial_repairs"])
    sig_by_task = {row["task_id"]: row for _, row in sig.iterrows()}
    metric_rows: list[dict] = []
    for traj in trajectories:
        key = (traj["task_id"], traj["condition"])
        kappa = kappa_of.get(key)
        finite = kappa is not None
        found = bool(traj["repairs_attempted"]) and finite
        optimal = (
            bool(traj["repairs_attempted"])
            and traj["repairs_attempted"][0] in tied_of.get(key, [])
            and traj["steps"] == kappa
            if finite
            else False
        )
        preferred = {"family-a": None, "family-b": "qR_fast", "family-c": "qE_slow"}[traj["model"]]
        adapted = (
            (not finite and traj["escalated"])
            or (
                finite
                and traj["repairs_attempted"]
                and (preferred is None or traj["repairs_attempted"][0] != preferred)
                and found
            )
            or (finite and preferred is None and found)
        )
        governance_correct = (traj["effect"] and finite) or (traj["escalated"] and not finite)
        regret = repair_regret(traj["steps"], kappa)
        record = summarize_episode(
            found, optimal, adapted, traj["escalated"], finite, traj["violations"], governance_correct, regret
        )
        record.update(
            {
                "task_id": traj["task_id"],
                "track": traj["track"],
                "model": traj["model"],
                "condition": traj["condition"],
                "repeat": traj["repeat"],
                "r_class": sig_by_task[traj["task_id"]]["r_class"] if traj["track"] == "N" else sig_by_task[traj["task_id"]]["r_class"],
            }
        )
        metric_rows.append(record)
    # console.log METR-09: per-episode metrics computed.
    print("[phase3:metrics] main: metric rows=%d." % len(metric_rows))
    metric_frame = pd.DataFrame(metric_rows)
    agents_dir = repo_root / "results" / run_id / "agents"
    metric_frame.to_parquet(agents_dir / "metrics.parquet", index=False)
    # console.log METR-10: metrics parquet written.
    print("[phase3:metrics] main: wrote metrics.parquet.")
    summary: dict = {"run_id": run_id, "tracks": {}}
    for track in ["N", "F"]:
        sub = metric_frame[metric_frame["track"] == track]
        track_entry: dict = {
            "episodes": int(len(sub)),
            "regime_distribution": sig[sig["track"] == track]["r_class"].value_counts().to_dict(),
        }
        for family in sorted(sub["model"].unique()):
            fam = sub[sub["model"] == family]
            discovery = bootstrap_mean_ci([float(v) for v in fam["route_discovery"]])
            optimal_ci = bootstrap_mean_ci([float(v) for v in fam["optimal_route"]])
            regrets = [float(v) for v in fam["repair_regret"] if v is not None and v == v]
            track_entry[family] = {
                "route_discovery": discovery,
                "optimal_route": optimal_ci,
                "repair_regret_mean": ((sum(regrets) / len(regrets)) if regrets else None),
                "excess_escalation_rate": float(fam["excess_escalation"].mean()) if len(fam) else 0.0,
                "unsafe_attempts_total": int(fam["unsafe_attempts"].sum()) if len(fam) else 0,
                "governance_correct_rate": float(fam["governance_correct"].mean()) if len(fam) else 0.0,
            }
        summary["tracks"][track] = track_entry
    # console.log METR-11: summary assembled per track and family.
    print("[phase3:metrics] main: summary tracks=%s." % sorted(summary["tracks"]))
    reports_dir = repo_root / "results" / run_id / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "phase3_summary.json").write_text(canonical_dumps(summary) + "\n", encoding="utf-8")
    # console.log METR-12: summary written.
    print("[phase3:metrics] main: wrote phase3_summary.json.")
    update_manifest(repo_root, run_id, "results/%s/agents/metrics.parquet" % run_id, metric_rows)
    update_manifest(repo_root, run_id, "results/%s/reports/phase3_summary.json" % run_id, summary)
    # console.log METR-13: metrics pipeline complete.
    print("[phase3:metrics] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log METR-14: script invoked as main.
    print("[phase3:metrics] __main__: invoking main.")
    raise SystemExit(main())
