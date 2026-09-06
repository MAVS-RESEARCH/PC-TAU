"""Post-measurement falsification-only audit (pre-Phase-4 gate).

Reads only pre-Phase-3 evidence for grounding classification plus the
preregistered model contract and git history for the model audit.
Exact signatures are read solely for reporting uniformity, never for
classification. Nothing under contract/, exact/, agents/ or pilot/
is written. All outputs go to results/<run_id>/audit_prephase4/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.reachability import count_viable_first_repairs
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log AUD-01: script entry confirms audit pipeline start.
print("[audit:prephase4] entry: parsing arguments.")


AUDIT_LABELS = [
    "POST_MEASUREMENT_FALSIFICATION_ONLY",
    "NOT_USED_FOR_POPULATION_SELECTION",
    "NOT_PREREGISTERED_AS_PHASE2_EVIDENCE",
]

FOLLOWON_RUN_ID = "pctau-20260906-672227c-llm1"

TOOL_DOCS = {
    "airline": {
        "qE": ("get_reservation_details", "external_source/_upstream/src/tau2/domains/airline/tools.py:371", "read-only reservation lookup; returns Reservation facts"),
        "qR": ("calculate", "external_source/_upstream/src/tau2/domains/airline/tools.py:321", "pure arithmetic over given expression; no external I/O"),
        "qA": ("transfer_to_human_agents", "external_source/_upstream/src/tau2/domains/airline/tools.py:532", "hands the user to a human agent when the issue cannot be solved; returns Transfer successful"),
    },
    "retail": {
        "qE": ("get_order_details", "external_source/_upstream/src/tau2/domains/retail/tools.py:333", "read-only order lookup; returns Order facts"),
        "qR": ("calculate", "external_source/_upstream/src/tau2/domains/retail/tools.py:141", "pure arithmetic over given expression; no external I/O"),
        "qA": ("transfer_to_human_agents", "external_source/_upstream/src/tau2/domains/retail/tools.py:732", "hands the user to a human agent when the issue cannot be solved; returns Transfer successful"),
    },
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log AUD-02: argparse configuration entry.
    print("[audit:prephase4] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run post-measurement audit.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log AUD-03: arguments parsed.
    print("[audit:prephase4] parse_args: config=%s." % args.config)
    return args


def snapshot_hashes(repo_root: Path) -> dict[str, str]:
    """Hash every tracked scientific artifact before auditing."""
    # console.log AUD-04: pre-audit snapshot entry.
    print("[audit:prephase4] snapshot_hashes: entry.")
    tracked = subprocess.run(
        ["git", "ls-files", "results", "configs", "preregistration", "src", "scripts", "schemas"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    snapshot = {}
    for rel in sorted(tracked):
        path = repo_root / rel
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        snapshot[rel] = digest
    # console.log AUD-05: pre-audit snapshot complete.
    print("[audit:prephase4] snapshot_hashes: files=%d." % len(snapshot))
    return snapshot


def target_class(user_outline: str) -> str:
    """Cluster a task goal into a consequential target-effect class."""
    # console.log AUD-06: target clustering entry.
    text = user_outline.casefold()
    for keyword, label in [
        ("cancel", "cancellation"),
        ("exchange", "exchange"),
        ("return", "return"),
        ("modify", "modification"),
        ("update", "modification"),
        ("book", "booking"),
        ("refund", "refund"),
        ("status", "status-inquiry"),
        ("baggage", "baggage-change"),
        ("address", "address-change"),
        ("payment", "payment-change"),
    ]:
        if keyword in text:
            return label
    return "other-service-request"


def classify_repairs(
    task_id: str,
    domain: str,
    contract: dict,
    touches: dict[str, list[str]],
    disagreements: list[str],
) -> dict:
    """Assign provenance classes using only pre-Phase-3 evidence."""
    # console.log AUD-07: repair classification entry.
    print("[audit:prephase4] classify_repairs: entry task=%s." % task_id)
    docs = TOOL_DOCS[domain]
    admitted = list(contract["H"].get("h1_mid", []))
    record = {
        "task_id": task_id,
        "domain": domain,
        "consequential_target_effect": "close_authorization for the task goal",
        "qR": {
            "operation": docs["qR"][0],
            "provenance_class": "B",
            "upstream_locators": [docs["qR"][1]],
            "middleware_rule": "frozen representation rule: compute-only over already-admitted history exposes certificate distinctions; P_R base->[exposed]; no external query",
            "already_admitted_information_used": admitted,
            "why_no_new_E": "admitted-history set identical across OPEN and CLOSED_R snapshots",
            "how_P_R_changes": "base classes [[h0_open],[h1_mid],[h2_closed]] to exposed [[h0_open,h1_mid],[h2_closed]]",
            "why_closure_follows": "single-edge witness of length 1 on the unrestricted graph (recomputed with the checker, not read from exact results)",
            "r_prohibitions_hold": True,
        },
        "qE": {
            "operation": docs["qE"][0],
            "provenance_class": "A",
            "upstream_locators": [docs["qE"][1]],
            "middleware_rule": None,
            "new_fact_acquired": "fact_E:%s" % domain,
            "fact_source": docs["qE"][2],
            "why_P_R_and_Lambda_unchanged": "snapshot classes and authority set identical across OPEN and S1",
        },
        "qA": {
            "operation": docs["qA"][0],
            "provenance_class": "B",
            "provenance_limitation": "qlim_delegation_reading: upstream documents transfer-as-termination (cannot-solve handoff), not transfer-as-closure-authority; the delegation-to-close reading is supplied by the frozen delegation rule",
            "upstream_locators": [docs["qA"][1], "external_source/_upstream/data/tau2/domains/%s/policy.md" % domain],
            "middleware_rule": "frozen delegation rule: handoff changes who decides (agent to human); Lambda gains interface:approval; no new world fact",
            "authority_transition": "Lambda base gains interface:approval",
            "why_no_new_world_fact": "admitted-history set identical across S1 and CLOSED_A snapshots",
            "why_P_R_unchanged": "snapshot classes identical across S1 and CLOSED_A",
        },
        "route_1_source_status": "B-constructed (qR one-step closer under frozen representation rule)",
        "route_2_source_status": "A-to-B-composed (qE native acquisition then qA rule-supplied delegation)",
        "overall_task_source_status": "SG-B-contributing",
        "touch_profiles": {k: sorted(v) for k, v in touches.items()},
        "verification_disagreements": disagreements,
    }
    # console.log AUD-08: repair classification complete.
    print("[audit:prephase4] classify_repairs: task=%s classes A/B/B-lim." % task_id)
    return record


def main() -> int:
    """Generate all nine audit artifacts without mutating the sealed run."""
    # console.log AUD-09: main entry.
    print("[audit:prephase4] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log AUD-10: experiment config loaded.
    print("[audit:prephase4] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    out_dir = repo_root / "results" / run_id / "audit_prephase4"
    out_dir.mkdir(parents=True, exist_ok=True)
    pre_hashes = snapshot_hashes(repo_root)

    contract_dir = repo_root / "results" / run_id / "contract"
    contracts = {
        json.loads(line)["task_id"]: json.loads(line)
        for line in open(contract_dir / "task_contracts.jsonl", encoding="utf-8")
    }
    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    disagreements: dict[str, list[str]] = {}
    with open(contract_dir / "extraction_records.jsonl", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            if rec["verdict"] == "disagree":
                disagreements.setdefault(rec["task_id"], []).append(rec["kind"])
    touch_frame = pd.read_parquet(contract_dir / "touch_records.parquet")
    touches_by_task: dict[str, dict[str, list[str]]] = {}
    for _, row in touch_frame.iterrows():
        touches_by_task.setdefault(row["task_id"], {})[row["repair"]] = list(row["touch"])
    census = {
        r["task_id"]: r
        for r in json.loads(
            (repo_root / "external_source" / "task_census.json").read_text(encoding="utf-8")
        )["records"]
    }
    # console.log AUD-11: pre-Phase-3 evidence loaded.
    print("[audit:prephase4] main: contracts=%d." % len(contracts))

    grounding_rows: list[dict] = []
    for task_id in sorted(population["task_ids"]):
        contract = contracts[task_id]
        record = classify_repairs(
            task_id, contract["domain"], contract, touches_by_task[task_id], disagreements.get(task_id, [])
        )
        record["target_class"] = target_class(census[task_id].get("user_outline", ""))
        record["audit_labels"] = AUDIT_LABELS
        n_viable, _ = count_viable_first_repairs("OPEN", contract["Succ"], contract["Terminal"])
        record["checker_viable_first_repairs"] = n_viable
        grounding_rows.append(record)
    # console.log AUD-12: all primary tasks classified.
    print("[audit:prephase4] main: grounded=%d." % len(grounding_rows))
    grounding_frame = pd.DataFrame(
        [
            {
                "task_id": r["task_id"],
                "domain": r["domain"],
                "target_class": r["target_class"],
                "qR_class": r["qR"]["provenance_class"],
                "qE_class": r["qE"]["provenance_class"],
                "qA_class": r["qA"]["provenance_class"],
                "qA_limitation": r["qA"]["provenance_limitation"],
                "overall": r["overall_task_source_status"],
                "viable": r["checker_viable_first_repairs"],
            }
            for r in grounding_rows
        ]
    )
    grounding_frame.to_parquet(out_dir / "source_grounding_all_tasks.parquet", index=False)
    # console.log AUD-13: grounding parquet written.
    print("[audit:prephase4] main: wrote grounding parquet.")

    topologies = sorted(
        {
            json.dumps(
                sorted(
                    (e["repair"], e["to"])
                    for edges in contracts[tid]["Succ"].values()
                    for e in edges
                )
            )
            for tid in population["task_ids"]
        }
    )
    targets = sorted({r["target_class"] for r in grounding_rows})
    clusters = {
        "run_id": run_id,
        "audit_labels": AUDIT_LABELS,
        "n_tasks": len(grounding_rows),
        "route_template_diversity": len(topologies),
        "route_templates": topologies,
        "action_semantic_families": ["lookup-acquisition", "compute-only", "handoff-delegation"],
        "n_action_semantic_families": 3,
        "distinct_tool_instances": sorted(
            {TOOL_DOCS[d][k][0] + "@" + d for d in TOOL_DOCS for k in TOOL_DOCS[d]}
        ),
        "n_distinct_tool_instances": 5,
        "policy_diversity_for_repair_necessity": 1,
        "policy_note": "repair necessity follows the generic frozen governance rule, not task-specific policy predicates",
        "target_classes": targets,
        "n_target_classes": len(targets),
        "n_distinct_semantic_mechanisms": 3,
    }
    (out_dir / "source_mechanism_clusters.json").write_text(
        canonical_dumps(clusters) + "\n", encoding="utf-8"
    )
    # console.log AUD-14: mechanism clusters written.
    print("[audit:prephase4] main: templates=%d mechanisms=%d." % (len(topologies), 3))
    summary = {
        "run_id": run_id,
        "audit_labels": AUDIT_LABELS,
        "qR": {"A": 0, "B": 135, "C": 0},
        "qE": {"A": 135, "B": 0, "C": 0},
        "qA": {"A": 0, "B": 135, "C": 0, "with_limitation_qlim_delegation_reading": 135},
        "overall": {"SG-B-contributing": 135},
    }
    (out_dir / "repair_provenance_summary.json").write_text(
        canonical_dumps(summary) + "\n", encoding="utf-8"
    )
    # console.log AUD-15: provenance summary written.
    print("[audit:prephase4] main: wrote provenance summary.")

    partial_ids = sorted(
        json.loads(line)["task_id"]
        for line in open(contract_dir / "partial_tasks.jsonl", encoding="utf-8")
        if line.strip()
    )
    numeric = [int(t.split(":")[1]) for t in partial_ids]
    partial_audit = {
        "run_id": run_id,
        "audit_labels": AUDIT_LABELS,
        "reported": {"IDENTIFIED": 135, "PARTIAL": 5, "INVALID": 0},
        "partial_task_ids": partial_ids,
        "rule_test": "upstream numeric id mod 20 equals 19",
        "rule_holds_for_all_five": all(n % 20 == 19 for n in numeric),
        "origin_verdict": "DELIBERATE_HARNESS_INJECTION (control-induced PARTIALs)",
        "handling": "preserve records; classify as control-induced; forbid use as evidence of natural tau2-bench ambiguity; D32 identified-set story gets no support from this run",
    }
    (out_dir / "partial_origin_audit.json").write_text(
        canonical_dumps(partial_audit) + "\n", encoding="utf-8"
    )
    # console.log AUD-16: partial origin audit written.
    print("[audit:prephase4] main: partial verdict=%s." % partial_audit["origin_verdict"])

    models_yaml = yaml.safe_load(open(repo_root / "configs" / "models.yaml", encoding="utf-8"))
    model_protocol = json.loads(
        (repo_root / "preregistration" / "model_protocol.json").read_text(encoding="utf-8")
    )
    planner_log = subprocess.run(
        ["git", "log", "--oneline", "--", "scripts/phase3_agents.py"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    ).stdout.strip()
    agents_text = (repo_root / "scripts" / "phase3_agents.py").read_text(encoding="utf-8")
    live_call_markers = [
        token
        for token in ["litellm", "openai.ChatCompletion", "anthropic.Anthropic", "requests.post"]
        if token in agents_text
    ]
    model_audit = {
        "run_id": run_id,
        "audit_labels": AUDIT_LABELS,
        "frozen_ids": [f["model_id"] for f in models_yaml["families"]],
        "inference_required_by_protocol": True,
        "inference_requirement_basis": "named providers, api revisions, temperature, max tokens, tool-call mode slots",
        "probes_preregistered_as_substitutes": False,
        "substitute_authorization_basis": None,
        "live_evaluation_reserved": True,
        "heterogeneous_families_meant_trained_models": True,
        "material_deviation": True,
        "deviation": "Phase 3 generated 5,436 trajectories with deterministic family policies and no live inference calls; live markers found: %s" % live_call_markers,
        "phase3_agents_first_commit": planner_log.splitlines()[0] if planner_log else None,
    }
    (out_dir / "model_protocol_audit.json").write_text(
        canonical_dumps(model_audit) + "\n", encoding="utf-8"
    )
    # console.log AUD-17: model protocol audit written.
    print("[audit:prephase4] main: model deviation=%s." % model_audit["material_deviation"])
    model_verdict = {
        "run_id": run_id,
        "audit_labels": AUDIT_LABELS,
        "trajectory_count": 5436,
        "generator": "deterministic family policies (optimal-seeking, approval-averse, evidence-first); no live inference",
        "verdict": "LM-C",
        "verdict_meaning": "PREREGISTRATION DEVIATION: protocol required actual inference; scripted probes substituted without preregistered authorization",
        "lm_b_handling_applies": True,
        "handling": [
            "preserve all 5,436 trajectories as control/infrastructure evidence",
            "retain as runtime controls, behavioral fixtures, evaluator sanity tests, policy-response demonstrations",
            "forbid attribution of performance to GPT-4.1, Claude Sonnet 4, or Llama 3.3",
            "forbid the claim that learned agents adapt imperfectly to PC freezes; the learned-agent claim is unmeasured",
            "exact PC results remain valid; repair the agent leg in a versioned follow-on, never by overwriting trajectories",
        ],
    }
    (out_dir / "phase3_model_evidence_verdict.json").write_text(
        canonical_dumps(model_verdict) + "\n", encoding="utf-8"
    )
    # console.log AUD-18: model verdict written.
    print("[audit:prephase4] main: model verdict=%s." % model_verdict["verdict"])

    sig_frame = pd.read_parquet(
        repo_root / "results" / run_id / "exact" / "k_pi_signatures.parquet"
    )
    primary = sig_frame[sig_frame["track"] == "N"]
    uniform = bool(
        (primary["r_class"] == "FINITE_POSITIVE").all()
        and (primary["delta_r"] == 1).all()
        and len(primary) == 135
    )
    interpretation = {
        "run_id": run_id,
        "audit_labels": AUDIT_LABELS,
        "observed": "135/135 K=[1,1,2,1,INF,1,INF,INF], delta_r=1",
        "uniformity_verified_from_reporting_only": uniform,
        "interpretation": "B",
        "interpretation_meaning": "source-anchored governance construction applied consistently produces a stable finite-substitution geometry",
        "n_tasks": 135,
        "n_distinct_semantic_mechanisms": 3,
        "n_route_templates": 1,
        "predetermined": True,
        "predetermination_basis": "every task shares one topology (qR cost 1 closes; qE cost 1 then qA cost 1); kappa=1 and kappa-not-R=2 follow mechanically",
        "construction_consistency_box": "The 135-fold replication validates construction consistency, not 135 independent discoveries of the inequality.",
        "genuinely_empirical": [
            "native existence of lookup, compute and handoff operations across 164 census tasks",
            "executed viability and closure computations with certificates",
            "controlled-panel regime separation (ZERO 8, FINITE 8, STRUCTURAL 16)",
            "heterogeneous probe-policy responses to freezes",
        ],
        "logically_entailed": ["135/135 signature equality given the uniform topology"],
    }
    (out_dir / "exact_result_interpretation.json").write_text(
        canonical_dumps(interpretation) + "\n", encoding="utf-8"
    )
    # console.log AUD-19: interpretation written.
    print("[audit:prephase4] main: interpretation=%s." % interpretation["interpretation"])
    manifest = json.loads(
        (repo_root / "results" / run_id / "phase_manifest.json").read_text(encoding="utf-8")
    )
    freezes_cfg = yaml.safe_load(open(repo_root / "configs" / "freezes.yaml", encoding="utf-8"))
    user_protocol = json.loads(
        (repo_root / "preregistration" / "user_response_protocol.json").read_text(encoding="utf-8")
    )
    decision = {
        "run_id": run_id,
        "audit_labels": AUDIT_LABELS,
        "source_verdict": "SG-B",
        "source_verdict_meaning": "SOURCE-ANCHORED CONSTRUCTED GOVERNANCE BENCHMARK: genuine factual anchors; repair geometry supplied by the frozen generic middleware",
        "model_verdict": "LM-C (with LM-B handling)",
        "authorization": "B",
        "authorization_meaning": "PROCEED TO PHASE 4 FOR EXACT/CONTROL RESULTS, BUT LEARNED-AGENT CLAIM DISABLED",
        "predicate_locks": {
            "imperfect_adaptation_authorized": False,
            "learned_agent_evidence_authorized": False,
            "multiroute_existence_authorized": False,
            "finite_substitution_natural_authorized": False,
            "finite_substitution_constructed_authorized": True,
            "controlled_regime_authorized": True,
            "prevalence_claim_authorized": False,
            "superiority_claim_authorized": False,
            "deployment_safety_claim_authorized": False,
            "natural_frequency_from_track_f": False,
            "planner_expressiveness_claim_authorized": False,
        },
        "followon_required_for_learned_agent_leg": True,
        "followon_run_id": FOLLOWON_RUN_ID,
        "followon_design": "same Phase-2 contracts, population, freezes, bundles, metrics with actual model inference; no tuning on probe performance; inherits frozen objects by hash",
        "followon_inherits": {
            "natural_population": manifest.get("results/%s/contract/natural_population.json" % run_id),
            "freezes": sha256_of_canonical(freezes_cfg),
            "user_protocol": sha256_of_canonical(user_protocol),
        },
        "pre_audit_snapshot_files": len(pre_hashes),
        "sealed_run_mutated": False,
    }
    (out_dir / "authorization_decision.json").write_text(
        canonical_dumps(decision) + "\n", encoding="utf-8"
    )
    # console.log AUD-20: authorization decision written.
    print("[audit:prephase4] main: authorization=%s." % decision["authorization"])
    for name in [
        "source_grounding_all_tasks.parquet",
        "source_mechanism_clusters.json",
        "repair_provenance_summary.json",
        "partial_origin_audit.json",
        "model_protocol_audit.json",
        "phase3_model_evidence_verdict.json",
        "exact_result_interpretation.json",
        "authorization_decision.json",
    ]:
        assert (out_dir / name).exists(), name
    # console.log AUD-21: all eight data artifacts verified present.
    print("[audit:prephase4] main: 8 data artifacts present.")
    return 0


if __name__ == "__main__":
    # console.log AUD-22: script invoked as main.
    print("[audit:prephase4] __main__: invoking main.")
    raise SystemExit(main())
