"""LLM1 preregistration compiler: roster, budget, schedule, estimand, locks."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps


# console.log PREG-01: script entry confirms preregistration start.
print("[llm1:prereg] entry: parsing arguments.")

ROSTER = [
    {"family": "z-ai", "slug": "z-ai/glm-4.7-flash", "provider": "Venice"},
    {"family": "qwen", "slug": "qwen/qwen3.7-flash", "provider": "Alibaba"},
    {"family": "deepseek", "slug": "deepseek/deepseek-v4-flash", "provider": "Baidu"},
]
PROVIDER_RULE = "status-0 endpoint at exact catalog price with maximum 30m uptime; applied uniformly before results"
CAPS = {
    "MAX_API_TURNS_PER_EPISODE": 12,
    "MAX_CUMULATIVE_INPUT_TOKENS_PER_EPISODE": 10000,
    "MAX_CUMULATIVE_OUTPUT_AND_REASONING_TOKENS_PER_EPISODE": 2000,
    "MAX_COMPLETION_TOKENS_PER_TURN": 512,
}
SCIENCE_BUDGET = 18.50


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log PREG-02: argparse configuration entry.
    print("[llm1:prereg] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Compile LLM1 preregistration.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    args = parser.parse_args()
    # console.log PREG-03: arguments parsed.
    print("[llm1:prereg] parse_args: config=%s." % args.config)
    return args


def quantiles(values: list) -> dict:
    """Median, p95, max and mean of a value list."""
    # console.log PREG-04: quantile entry.
    print("[llm1:prereg] quantiles: entry n=%d." % len(values))
    ordered = sorted(values)
    count = len(ordered)
    result = {
        "median": ordered[count // 2],
        "p95": ordered[min(count - 1, int(count * 0.95))],
        "max": ordered[-1],
        "mean": statistics.mean(ordered),
    }
    # console.log PREG-05: quantiles complete.
    print("[llm1:prereg] quantiles: complete.")
    return result


def main() -> int:
    """Build every L1 artifact from calibration data and live snapshots."""
    # console.log PREG-06: main entry.
    print("[llm1:prereg] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    pre_dir = repo_root / "llm1" / "preregistration"
    episodes = [json.loads(line) for line in open(repo_root / "llm1" / "raw" / "calibration_episodes.jsonl", encoding="utf-8")]
    assert len(episodes) == 48, "calibration incomplete"
    by_model: dict[str, list] = collections.defaultdict(list)
    for episode in episodes:
        by_model[episode["model"]].append(episode)
    assert all(len(group) == 16 for group in by_model.values())
    # console.log PREG-07: calibration completeness verified.
    print("[llm1:prereg] main: calibration models=%d." % len(by_model))
    token_calibration = {}
    for model in sorted(by_model):
        group = by_model[model]
        token_calibration[model] = {
            "turns": quantiles([e["turns"] for e in group]),
            "input_tokens": quantiles([e["usage"]["prompt"] for e in group]),
            "output_reasoning_tokens": quantiles([e["usage"]["completion"] + e["usage"]["reasoning"] for e in group]),
            "cost": quantiles([e["usage"]["cost"] for e in group]),
        }
    (pre_dir / "token_calibration.json").write_text(canonical_dumps(token_calibration) + "\n", encoding="utf-8")
    # console.log PREG-08: token calibration written.
    print("[llm1:prereg] main: wrote token_calibration.json.")

    catalog = {c["slug"]: c for c in json.loads((pre_dir / "model_candidates.json").read_text(encoding="utf-8"))["candidates"]}
    endpoints = json.loads(open(repo_root / "llm1_endpoints.json", encoding="utf-8").read())
    snapshot = {"captured_at": catalog and None, "models": {}}
    for entry in ROSTER:
        slug = entry["slug"]
        assert slug in catalog, "roster slug missing from live catalog"
        rows = [e for e in endpoints.get(slug, []) if e["provider_name"] == entry["provider"]]
        assert rows, "pinned provider missing from live endpoints"
        snapshot["models"][slug] = {
            "provider": entry["provider"],
            "prompt_price": catalog[slug]["prompt_price"],
            "completion_price": catalog[slug]["completion_price"],
            "context_length": catalog[slug]["context_length"],
            "endpoint_status": rows[0]["status"],
            "endpoint_uptime": rows[0]["uptime"],
        }
    snapshot["captured_at"] = json.loads((pre_dir / "model_candidates.json").read_text(encoding="utf-8"))["captured_at"]
    snapshot["source_hash"] = hashlib.sha256(json.dumps(snapshot["models"], sort_keys=True).encode()).hexdigest()
    (pre_dir / "openrouter_price_snapshot.json").write_text(canonical_dumps(snapshot) + "\n", encoding="utf-8")
    # console.log PREG-09: price snapshot written.
    print("[llm1:prereg] main: wrote price snapshot.")

    projection = {"per_model": {}, "science_budget": SCIENCE_BUDGET}
    total = 0.0
    for entry in ROSTER:
        prices = snapshot["models"][entry["slug"]]
        per_episode = CAPS["MAX_CUMULATIVE_INPUT_TOKENS_PER_EPISODE"] * float(prices["prompt_price"]) + CAPS["MAX_CUMULATIVE_OUTPUT_AND_REASONING_TOKENS_PER_EPISODE"] * float(prices["completion_price"])
        worst = 1812 * per_episode
        projection["per_model"][entry["slug"]] = {
            "episodes": 1812,
            "input_cap": CAPS["MAX_CUMULATIVE_INPUT_TOKENS_PER_EPISODE"],
            "output_cap": CAPS["MAX_CUMULATIVE_OUTPUT_AND_REASONING_TOKENS_PER_EPISODE"],
            "per_episode_worst": per_episode,
            "worst_case": worst,
        }
        total += worst
    projection["total_worst_case"] = total
    projection["fits"] = total <= SCIENCE_BUDGET
    (pre_dir / "full_run_cost_projection.json").write_text(canonical_dumps(projection) + "\n", encoding="utf-8")
    # console.log PREG-10: cost projection written.
    print("[llm1:prereg] main: worst-case=%.4f fits=%s." % (total, projection["fits"]))
    assert projection["fits"], "roster does not fit the science budget"

    (pre_dir / "episode_count.json").write_text(
        canonical_dumps({"track_n": 135, "track_f_subset": 16, "freezes": 4, "repeats": 3, "episodes_per_model": 1812}) + "\n",
        encoding="utf-8",
    )
    (pre_dir / "interaction_budget.json").write_text(canonical_dumps({**CAPS, "derivation": "ceil(1.25 x max-model p95) rounded up; non-binding on calibration maxima except turns raised 8 to 12", "fair": "one common envelope for all roster models"}) + "\n", encoding="utf-8")
    (pre_dir / "model_roster.json").write_text(
        canonical_dumps(
            {
                "models": [
                    {**entry, "temperature": 0, "reasoning": "provider defaults; no explicit budget control exposed", "max_completion_tokens_per_turn": 512, "tool_choice": "auto", "parallel_tools": False}
                    for entry in ROSTER
                ],
                "rejected_fourth": "no fourth model added; 3-model full-population design preferred per brief",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (pre_dir / "provider_lock.json").write_text(
        canonical_dumps(
            {
                "pins": [
                    {"slug": e["slug"], "provider": e["provider"], "allow_fallbacks": False, "require_parameters": True}
                    for e in ROSTER
                ],
                "rule": PROVIDER_RULE,
                "substitution_policy": "mid-run unavailability marks the model run incomplete; replacement needs a new documented run, never silent substitution",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (pre_dir / "population_rule.json").write_text(
        canonical_dumps({"design": "FULL", "episodes_per_model": 1812, "same_population_all_models": True, "subset": None, "track_f_subset": 16}) + "\n",
        encoding="utf-8",
    )
    population = json.loads((repo_root / "results" / "pctau-20260906-672227c" / "contract" / "natural_population.json").read_text(encoding="utf-8"))["task_ids"]
    panel = json.loads((repo_root / "results" / "pctau-20260906-672227c" / "contract" / "controlled_panel.json").read_text(encoding="utf-8"))
    by_regime: dict[str, list] = {}
    for task in panel["tasks"]:
        by_regime.setdefault(task["regime"], []).append(task["controlled_id"])
    f16 = sorted(cid for regime in sorted(by_regime) for cid in sorted(by_regime[regime])[:4])
    assert len(f16) == 16
    sequence = []
    for model in sorted(e["slug"] for e in ROSTER):
        for task in sorted(population) + sorted(f16):
            for repeat in range(3):
                for cell in ["F000", "F100", "F010", "F001"]:
                    key = hashlib.sha256(("llm1-schedule-v1|%s|%s|%d|%s" % (model, task, repeat, cell)).encode()).hexdigest()
                    sequence.append({"model": model, "task": task, "repeat": repeat, "freeze": cell, "key": key})
    sequence.sort(key=lambda row: row["key"])
    for index, row in enumerate(sequence):
        row["seq"] = index
    assert len(sequence) == 3 * 1812
    (pre_dir / "execution_schedule.json").write_text(canonical_dumps({"seed_rule": "sha256(llm1-schedule-v1|model|task|repeat|freeze) sorted; pairing preserved", "entries": sequence}) + "\n", encoding="utf-8")
    # console.log PREG-11: schedule written.
    print("[llm1:prereg] main: schedule entries=%d." % len(sequence))
    (pre_dir / "retry_policy.json").write_text(
        canonical_dumps({"allowed": ["timeout", "connection failure", "429", "provider 5xx", "documented transient infrastructure failure"], "forbidden": ["bad reasoning", "wrong tool", "refusal", "escalation", "failure", "inconvenient answer", "high regret"], "ambiguous_timeout_rule": "preserve attempt, reserve worst-case cost, link attempts, count one trajectory", "duplicate_rule": "duplicate response IDs or logical keys fail the audit"}) + "\n",
        encoding="utf-8",
    )
    (pre_dir / "primary_estimand.json").write_text(
        canonical_dumps({"contrast": "F000 vs F010", "basis": "kappa 1 vs 2, both finite", "ordered_endpoints": ["governance-correct completion", "repair regret", "excess escalation", "finite-fallback discovery"], "secondary": ["route discovery", "optimal-route rate", "freeze adaptation", "unsafe attempts"], "comparisons": ["F000 vs F100", "F000 vs F001"], "promotion_ban": True}) + "\n",
        encoding="utf-8",
    )
    predicates = ["actual_learned_agent_evidence", "real_inference_complete", "paired_resource_intervention_measured", "freeze_sensitive_behavior_observed", "finite_fallback_discovery_observed", "imperfect_adaptation_observed", "cross_model_replication_observed", "cross_model_heterogeneity_observed", "unsafe_behavior_observed", "protocol_compatibility_established"]
    (pre_dir / "claim_predicates.json").write_text(canonical_dumps({"predicates": {name: False for name in predicates}}) + "\n", encoding="utf-8")
    (pre_dir / "nonclaims.json").write_text(
        canonical_dumps({"nonclaims": ["natural native multi-route prevalence", "135 independent native mechanisms", "natural PARTIAL ambiguity", "SG-A status", "universal agent failure", "universal agent success", "safety", "deployment safety", "alignment", "prevalence/frequency in real systems", "superiority over all agent methods", "frontier-model universality", "PC greater expressiveness than generic planning", "native finite substitution throughout tau2-bench"]}) + "\n",
        encoding="utf-8",
    )
    # console.log PREG-12: locks and schedule written.
    print("[llm1:prereg] main: locks written.")
    (repo_root / "llm1" / "configs" / "live_models.yaml").write_text(
        "roster:\n- z-ai/glm-4.7-flash\n- qwen/qwen3.7-flash\n- deepseek/deepseek-v4-flash\ntemperature: 0\n", encoding="utf-8"
    )
    state = {"phase": "L1-uncommitted", "artifacts": sorted(p.name for p in pre_dir.iterdir())}
    (pre_dir / "l1_state.json").write_text(canonical_dumps(state) + "\n", encoding="utf-8")
    # console.log PREG-13: preregistration pipeline complete (uncommitted).
    print("[llm1:prereg] main: complete; commit separately.")
    return 0


if __name__ == "__main__":
    # console.log PREG-14: script invoked as main.
    print("[llm1:prereg] __main__: invoking main.")
    raise SystemExit(main())
