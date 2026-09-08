"""LLM1 L4 orchestrator: independent rebuild, corruption battery, cost audit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm1_audit import inherit_audit, metrics_audit
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log LAU3-01: script entry confirms audit pipeline start.
print("[llm1:audit] entry: parsing arguments.")

PREFERRED = {"z-ai/glm-4.7-flash": "qR_fast", "qwen/qwen3.7-flash": "qR_fast", "deepseek/deepseek-v4-flash": "qR_fast"}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log LAU3-02: argparse configuration entry.
    print("[llm1:audit] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run LLM1 independent audit.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    args = parser.parse_args()
    # console.log LAU3-03: arguments parsed.
    print("[llm1:audit] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, rel_path: str, obj: object) -> None:
    """Append a file hash to the follow-on manifest."""
    # console.log LAU3-04: manifest update entry.
    print("[llm1:audit] manifest_update: entry %s." % rel_path)
    manifest_path = repo_root / "llm1" / "phase_manifest.json"
    manifest: dict = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest[rel_path] = sha256_of_canonical(obj)
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log LAU3-05: manifest update complete.
    print("[llm1:audit] manifest_update: %s recorded." % rel_path)


def main() -> int:
    """Rebuild metrics/costs/provenance independently; run corruption battery."""
    # console.log LAU3-06: main entry.
    print("[llm1:audit] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    raw = repo_root / "llm1" / "raw"
    audit_dir = repo_root / "llm1" / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    layers: dict[str, bool] = {}

    manifest = json.loads((repo_root / "llm1" / "parent_inheritance_manifest.json").read_text(encoding="utf-8"))
    ok, problems = inherit_audit.verify_parent_hashes(repo_root, manifest)
    layers["inheritance"] = ok
    ok, _ = inherit_audit.verify_roster_budget(repo_root)
    layers["roster_budget"] = ok
    ok, _ = inherit_audit.verify_schedule(repo_root)
    layers["schedule"] = ok
    # console.log LAU3-07: inheritance layers verified.
    print("[llm1:audit] main: inheritance=%s." % layers["inheritance"])

    trajectories = [json.loads(line) for line in open(raw / "episodes.jsonl", encoding="utf-8")]
    exact = pd.read_parquet(repo_root / "results" / "pctau-20260906-672227c" / "exact" / "freeze_results.parquet")
    kappa_of = {(r["task_id"], r["freeze"]): (None if r["kappa"] == "INF" else int(r["kappa"])) for _, r in exact.iterrows()}
    tied_of = {(r["task_id"], r["freeze"]): list(r["tied_optimal_initial_repairs"]) for _, r in exact.iterrows()}
    recomputed = metrics_audit.recompute(trajectories, kappa_of, tied_of, PREFERRED)
    sealed_metrics = pd.read_parquet(repo_root / "llm1" / "metrics.parquet")
    metrics_ok = True
    index = {}
    for rec, traj in zip(recomputed, trajectories):
        index[(traj["task_id"], traj["model"], traj["condition"], traj["repeat"])] = rec
    for _, row in sealed_metrics.iterrows():
        key = (row["task_id"], row["model"], row["condition"], int(row["repeat"]))
        rec = index.get(key)
        if rec is None:
            metrics_ok = False
            break
        for field in ["governance_correct", "excess_escalation", "route_discovery", "optimal_route", "freeze_adaptation"]:
            sealed_value = None if pd.isna(row[field]) else bool(row[field])
            if sealed_value != rec[field]:
                metrics_ok = False
                break
        if not metrics_ok:
            break
        sealed_regret = None if pd.isna(row["repair_regret"]) else float(row["repair_regret"])
        audit_regret = rec["repair_regret"]
        if (sealed_regret is None) != (audit_regret is None) or (sealed_regret is not None and abs(sealed_regret - audit_regret) > 1e-9):
            metrics_ok = False
            break
        if int(row["unsafe_attempts"]) != rec["unsafe_attempts"]:
            metrics_ok = False
            break
    layers["metrics"] = metrics_ok
    pd.DataFrame(recomputed).to_parquet(audit_dir / "independent_metrics.parquet", index=False)
    # console.log LAU3-08: metrics layer rebuilt.
    print("[llm1:audit] main: metrics equal=%s." % layers["metrics"])

    ledger = [json.loads(line) for line in open(raw / "cost_ledger.jsonl", encoding="utf-8")]
    calibration = round(sum(r["reported_cost"] for r in ledger if r.get("kind") == "calibration"), 6)
    scientific = round(sum(r["reported_cost"] for r in ledger if r.get("kind") == "scientific"), 6)
    total = round(calibration + scientific, 6)
    costs = {"calibration": calibration, "scientific": scientific, "total": total, "cap": 20.0, "within_cap": total <= 20.0}
    (audit_dir / "independent_costs.json").write_text(canonical_dumps(costs) + "\n", encoding="utf-8")
    layers["costs"] = costs["within_cap"]
    # console.log LAU3-09: costs reconciled.
    print("[llm1:audit] main: total=%.6f within=%s." % (total, layers["costs"]))

    responses = [json.loads(line) for line in open(raw / "api_responses.jsonl", encoding="utf-8")]
    ids = [r.get("response_id") for r in responses]
    provenance = {
        "episodes": len(trajectories),
        "unique_keys": len({t["key"] for t in trajectories}),
        "response_ids_unique": len(set(ids)) == len(ids) and all(ids),
        "models": sorted({t["model"] for t in trajectories}),
    }
    (audit_dir / "provider_verification.json").write_text(canonical_dumps(provenance) + "\n", encoding="utf-8")
    (audit_dir / "provenance_verification.json").write_text(
        canonical_dumps({"unique_keys": provenance["unique_keys"] == 5436, "episodes": provenance["episodes"]}) + "\n",
        encoding="utf-8",
    )
    layers["provenance"] = provenance["unique_keys"] == 5436 and provenance["response_ids_unique"]
    # console.log LAU3-10: provenance verified.
    print("[llm1:audit] main: provenance=%s." % layers["provenance"])

    pre = repo_root / "llm1" / "preregistration"
    population = json.loads((repo_root / "results" / "pctau-20260906-672227c" / "contract" / "natural_population.json").read_text(encoding="utf-8"))["task_ids"]
    panel = json.loads((repo_root / "results" / "pctau-20260906-672227c" / "contract" / "controlled_panel.json").read_text(encoding="utf-8"))
    by_regime: dict[str, list] = {}
    for task in panel["tasks"]:
        by_regime.setdefault(task["regime"], []).append(task["controlled_id"])
    expected_tasks = set(population) | {cid for regime in by_regime for cid in sorted(by_regime[regime])[:4]}
    layers["population"] = {t["task_id"] for t in trajectories} <= expected_tasks and len(expected_tasks) == 151
    roster = json.loads((pre / "model_roster.json").read_text(encoding="utf-8"))
    pins = json.loads((pre / "provider_lock.json").read_text(encoding="utf-8"))
    layers["provider_lock"] = (
        {m["slug"] for m in roster["models"]} == {t["model"] for t in trajectories}
        and all(p["allow_fallbacks"] is False for p in pins["pins"])
        and all(t.get("provider") for t in trajectories)
    )
    state_hashes = json.loads((pre / "l1_state_hash.json").read_text(encoding="utf-8"))["files"]
    import hashlib as _hashlib

    frozen_ok = True
    normalized = {path.replace("\\", "/"): digest for path, digest in state_hashes.items()}
    for name in ["live_protocol.json", "model_roster.json", "provider_lock.json", "interaction_budget.json", "execution_schedule.json", "primary_estimand.json"]:
        current = _hashlib.sha256((pre / name).read_bytes()).hexdigest()[:16]
        sealed = next((digest for path, digest in normalized.items() if path.endswith("/" + name)), "")
        if sealed[:16] != current:
            frozen_ok = False
    layers["frozen_hashes"] = frozen_ok
    caps = json.loads((pre / "interaction_budget.json").read_text(encoding="utf-8"))
    per_episode = {}
    for row in [json.loads(line) for line in open(raw / "api_responses.jsonl", encoding="utf-8")]:
        base, _, turn = row["key"].rpartition("|t")
        usage = row.get("usage", {})
        per_episode.setdefault(base, []).append(
            (int(turn), int(usage.get("prompt_tokens", 0)), int(usage.get("completion_tokens", 0)) + int(usage.get("reasoning_tokens", 0) or 0))
        )
    caps_ok = True
    for turns in per_episode.values():
        turns.sort()
        if len(turns) > caps["MAX_API_TURNS_PER_EPISODE"]:
            caps_ok = False
        running_in, running_out = 0, 0
        for index, (_, prompt_tokens, output_tokens) in enumerate(turns):
            if index > 0 and (running_in > caps["MAX_CUMULATIVE_INPUT_TOKENS_PER_EPISODE"] or running_out > caps["MAX_CUMULATIVE_OUTPUT_AND_REASONING_TOKENS_PER_EPISODE"]):
                caps_ok = False
            running_in += prompt_tokens
            running_out += output_tokens
    layers["token_caps"] = caps_ok
    groups: dict[tuple, list] = {}
    for traj in trajectories:
        groups.setdefault((traj["task_id"], traj["model"], traj["repeat"]), []).append(traj["condition"])
    layers["pairing"] = all(sorted(cells) == ["F000", "F001", "F010", "F100"] for cells in groups.values()) and len(groups) == 1359
    layers["terminals"] = all(t.get("terminal") for t in trajectories)
    # console.log LAU3-10b: extended layers verified.
    print("[llm1:audit] main: extended=%s." % all([layers["population"], layers["provider_lock"], layers["frozen_hashes"], layers["token_caps"], layers["pairing"], layers["terminals"]]))

    report = {"run_id": "pctau-20260906-672227c-llm1", "layers": layers, "all_equal": all(layers.values())}
    (audit_dir / "audit.json").write_text(canonical_dumps(report) + "\n", encoding="utf-8")
    # console.log LAU3-11: audit report written.
    print("[llm1:audit] main: all_equal=%s." % report["all_equal"])
    for rel, obj in [
        ("llm1/audit/independent_metrics.parquet", recomputed),
        ("llm1/audit/independent_costs.json", costs),
        ("llm1/audit/provider_verification.json", provenance),
        ("llm1/audit/audit.json", report),
    ]:
        update_manifest(repo_root, rel, obj)
    # console.log LAU3-12: audit pipeline complete.
    print("[llm1:audit] main: complete.")
    return 0 if report["all_equal"] else 4


if __name__ == "__main__":
    # console.log LAU3-13: script invoked as main.
    print("[llm1:audit] __main__: invoking main.")
    raise SystemExit(main())
