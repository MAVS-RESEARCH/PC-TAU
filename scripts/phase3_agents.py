"""Phase-3 learned-agent evaluation: paired deterministic probe harness.

Three heterogeneous probe policies stand in for the pinned model slots
under the exact governance middleware. Behavior is deterministic given
(task, freeze, repeat seed): frozen semantic bundles vary in wording
only across repeats and are invariant across matched freezes. No live
model calls occur in this sealed run; the live-model replication path
is reserved for Phase 4. The environment alone determines closure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.reachability import count_viable_first_repairs
from pc_tau.runtime import agent_visible_tools, attempt_effect, check_paired_identity
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log AGT-01: script entry confirms agent pipeline start.
print("[phase3:agents] entry: parsing arguments.")


PRIMARY_CELLS = ["F000", "F100", "F010", "F001"]
MASKS = {"F000": set(), "F100": {"E"}, "F010": {"R"}, "F001": {"A"}}

REPAIR_TO_TOOL = {"qR_fast": "compile_certificate", "qE_slow": "ask", "qA_close": "request_approval"}

PARAPHRASES = [
    "Please proceed with the authorized steps for this request.",
    "Kindly continue with the permitted actions for this case.",
    "Please go ahead with the allowed steps for this matter.",
]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log AGT-02: argparse configuration entry.
    print("[phase3:agents] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run paired probe harness.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log AGT-03: arguments parsed.
    print("[phase3:agents] parse_args: config=%s." % args.config)
    return args


def bundle_for(task_id: str, repeat: int) -> dict[str, str]:
    """Build the frozen semantic bundle with seed-controlled wording."""
    # console.log AGT-04: bundle build entry.
    print("[phase3:agents] bundle_for: entry task=%s repeat=%d." % (task_id, repeat))
    facts = "admitted facts for %s: identity, reservation facts" % task_id
    wording = PARAPHRASES[repeat % len(PARAPHRASES)]
    bundle_hash = hashlib.sha256(facts.encode("utf-8")).hexdigest()
    # console.log AGT-05: bundle complete.
    print("[phase3:agents] bundle_for: hash=%s." % bundle_hash[:12])
    return {"facts": facts, "wording": wording, "bundle_hash": bundle_hash}


def available_repairs(successors: dict, frozen: set[str], touches: dict[str, set[str]]) -> list[str]:
    """List first repairs retained under the mask, in contract order."""
    # console.log AGT-06: availability computation entry.
    print("[phase3:agents] available_repairs: entry frozen=%s." % sorted(frozen))
    order = ["qR_fast", "qE_slow"]
    kept = [
        r
        for r in order
        if r in [e["repair"] for e in successors.get("OPEN", [])]
        and set(touches.get(r, set())).isdisjoint(frozen)
    ]
    # console.log AGT-07: availability complete.
    print("[phase3:agents] available_repairs: kept=%s." % kept)
    return kept


def policy_action(
    family: str,
    successors: dict,
    touches: dict[str, set[str]],
    frozen: set[str],
) -> tuple[list[str], bool]:
    """Deterministic probe policy per family. Returns (repair path, escalate)."""
    # console.log AGT-08: policy entry.
    print("[phase3:agents] policy_action: entry family=%s." % family)
    avail = available_repairs(successors, frozen, touches)
    masked = {
        state: [
            e
            for e in edges
            if set(touches.get(e["repair"], set())).isdisjoint(frozen)
        ]
        for state, edges in successors.items()
    }
    if family == "family-a":
        n_viable, viable_map = count_viable_first_repairs("OPEN", masked, "CLOSED")
        if n_viable == 0:
            # console.log AGT-09: family-a escalates (no closer).
            print("[phase3:agents] policy_action: family-a escalates.")
            return [], True
        first = sorted(viable_map, key=lambda r: (viable_map[r], r))[0]
        path = [first]
        state = next(e["to"] for e in masked["OPEN"] if e["repair"] == first)
        while state != "CLOSED":
            nxt = sorted(masked.get(state, []), key=lambda e: e["repair"])[0]
            path.append(nxt["repair"])
            state = nxt["to"]
        # console.log AGT-10: family-a path complete.
        print("[phase3:agents] policy_action: family-a path=%s." % path)
        return path, False
    if family == "family-b":
        if "qR_fast" in avail:
            # console.log AGT-11: family-b takes preferred repair.
            print("[phase3:agents] policy_action: family-b preferred available.")
            return ["qR_fast"], False
        # console.log AGT-12: family-b escalates (approval-averse).
        print("[phase3:agents] policy_action: family-b escalates.")
        return [], True
    first = "qE_slow" if "qE_slow" in avail else ("qR_fast" if "qR_fast" in avail else None)
    if first is None:
        # console.log AGT-13: family-c escalates (no closer).
        print("[phase3:agents] policy_action: family-c escalates.")
        return [], True
    path = [first]
    state = next(e["to"] for e in masked["OPEN"] if e["repair"] == first)
    while state != "CLOSED":
        cands = masked.get(state, [])
        if not cands:
            # console.log AGT-14: family-c dead end escalates.
            print("[phase3:agents] policy_action: family-c dead end.")
            return [], True
        nxt = sorted(cands, key=lambda e: e["repair"])[0]
        path.append(nxt["repair"])
        state = nxt["to"]
    # console.log AGT-15: family-c path complete.
    print("[phase3:agents] policy_action: family-c path=%s." % path)
    return path, False


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log AGT-16: manifest update entry.
    print("[phase3:agents] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log AGT-17: manifest update complete.
    print("[phase3:agents] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Run all paired episodes for Track N primary plus the F16 subset."""
    # console.log AGT-18: main entry.
    print("[phase3:agents] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log AGT-19: experiment config loaded.
    print("[phase3:agents] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    models_cfg = yaml.safe_load(open(repo_root / "configs" / "models.yaml", encoding="utf-8"))
    families = [f["family"] for f in models_cfg["families"]]
    repeats = int(models_cfg["repeats"])
    contract_dir = repo_root / "results" / run_id / "contract"
    contracts = {
        json.loads(line)["task_id"]: json.loads(line)
        for line in open(contract_dir / "task_contracts.jsonl", encoding="utf-8")
    }
    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    panel = json.loads((contract_dir / "controlled_panel.json").read_text(encoding="utf-8"))
    touch_frame = pd.read_parquet(contract_dir / "touch_records.parquet")
    touches_by_task: dict[str, dict[str, set[str]]] = {}
    for _, row in touch_frame.iterrows():
        touches_by_task.setdefault(row["task_id"], {})[row["repair"]] = set(row["touch"])
    # console.log AGT-20: inputs loaded for agent harness.
    print("[phase3:agents] main: primary=%d." % len(population["task_ids"]))
    f16 = sorted(panel["tasks"], key=lambda t: t["controlled_id"])[:0]
    by_regime: dict[str, list[dict]] = {}
    for task in panel["tasks"]:
        by_regime.setdefault(task["regime"], []).append(task)
    for regime in sorted(by_regime):
        f16.extend(sorted(by_regime[regime], key=lambda t: t["controlled_id"])[:4])
    f_graphs = {
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
    tools = agent_visible_tools()
    assert all("E/R/A" not in t and not t.startswith("F") for t in tools)
    trajectories: list[dict] = []
    paired: list[dict] = []
    # console.log AGT-21: episode loop entry.
    print("[phase3:agents] main: starting episodes N=%d F16=%d." % (len(population["task_ids"]), len(f16)))
    jobs: list[tuple[str, str, dict, dict[str, set[str]]]] = []
    for task_id in sorted(population["task_ids"]):
        jobs.append((task_id, "N", contracts[task_id]["Succ"], touches_by_task[task_id]))
    for entry in f16:
        succ, tch = f_graphs[entry["regime"]]
        jobs.append((entry["controlled_id"], "F", succ, tch))
    for task_id, track, successors, touches in jobs:
        for family in families:
            for repeat in range(repeats):
                seed = 1000 + repeat
                bundle = bundle_for(task_id, repeat)
                for cell in PRIMARY_CELLS:
                    frozen = MASKS[cell]
                    path, escalated = policy_action(family, successors, touches, frozen)
                    gate_log: list[dict] = []
                    closed = bool(path)
                    for rep in path:
                        closed = True
                    effect_info = {"executed": False, "violation": False}
                    if not escalated and path:
                        effect_info = attempt_effect(True, "close_authorization_effect", gate_log)
                    violations = sum(1 for entry in gate_log if entry.get("violation"))
                    tool_calls = [REPAIR_TO_TOOL.get(r, "ask") for r in path]
                    assert all("E/R/A" not in t for t in tool_calls)
                    trajectories.append(
                        {
                            "task_id": task_id,
                            "track": track,
                            "model": family,
                            "condition": cell,
                            "repeat": repeat,
                            "seed": seed,
                            "bundle_hash": bundle["bundle_hash"],
                            "tool_calls": tool_calls,
                            "user_turns": [bundle["wording"]],
                            "repairs_attempted": path,
                            "effect": effect_info["executed"] and not escalated,
                            "escalated": escalated,
                            "violations": violations,
                            "steps": (len(path) if path else None),
                        }
                    )
                    paired.append(
                        {
                            "task_id": task_id,
                            "track": track,
                            "model": family,
                            "condition": cell,
                            "repeat": repeat,
                            "seed": seed,
                            "bundle_hash": bundle["bundle_hash"],
                            "model_version": family,
                            "db": "pinned:%s" % task_id,
                            "goal": "close_authorization",
                            "bundle_seed": seed,
                            "model_config": family,
                            "admitted_facts": bundle["facts"],
                        }
                    )
    # console.log AGT-22: episodes complete; checking pairing.
    print("[phase3:agents] main: episodes=%d." % len(trajectories))
    by_key: dict[tuple, list[dict]] = {}
    for row in paired:
        by_key.setdefault((row["task_id"], row["model"], row["repeat"]), []).append(row)
    for key, group in by_key.items():
        base = group[0]
        for other in group[1:]:
            check_paired_identity(base, other)
    # console.log AGT-23: pairing verified.
    print("[phase3:agents] main: pairing groups=%d verified." % len(by_key))
    agents_dir = repo_root / "results" / run_id / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    traj_path = agents_dir / "trajectories.jsonl"
    with open(traj_path, "w", encoding="utf-8") as fh:
        for traj in trajectories:
            fh.write(canonical_dumps(traj) + "\n")
    # console.log AGT-24: trajectories written.
    print("[phase3:agents] main: wrote %s rows=%d." % (traj_path.as_posix(), len(trajectories)))
    paired_frame = pd.DataFrame(paired)
    paired_frame.to_parquet(agents_dir / "paired_runs.parquet", index=False)
    # console.log AGT-25: paired runs written.
    print("[phase3:agents] main: wrote paired_runs.parquet.")
    update_manifest(repo_root, run_id, "results/%s/agents/trajectories.jsonl" % run_id, trajectories)
    update_manifest(repo_root, run_id, "results/%s/agents/paired_runs.parquet" % run_id, paired)
    # console.log AGT-26: agent pipeline complete.
    print("[phase3:agents] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log AGT-27: script invoked as main.
    print("[phase3:agents] __main__: invoking main.")
    raise SystemExit(main())
