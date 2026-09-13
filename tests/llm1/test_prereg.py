"""LLM1 L1 tests: preregistration math, locks, and frozen artifacts."""

import json
from pathlib import Path


# console.log L1P-01: test module import confirms prereg checks are active.
print("[test:llm1-prereg] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
PRE = REPO_ROOT / "llm1" / "preregistration"


def test_episode_count():
    """(135 + 16) x 4 x 3 equals 1812 per model."""
    # console.log L1P-02: episode math entry.
    print("[test:llm1-prereg] test_episode_count: entry.")
    count = json.loads((PRE / "episode_count.json").read_text(encoding="utf-8"))
    assert (count["track_n"] + count["track_f_subset"]) * count["freezes"] * count["repeats"] == 1812
    assert count["episodes_per_model"] == 1812
    schedule = json.loads((PRE / "execution_schedule.json").read_text(encoding="utf-8"))
    assert len(schedule["entries"]) == 3 * 1812
    # console.log L1P-03: episode math verified.
    print("[test:llm1-prereg] test_episode_count: passed.")


def test_worst_case_fits():
    """Conservative worst case stays within the science budget."""
    # console.log L1P-04: budget test entry.
    print("[test:llm1-prereg] test_worst_case_fits: entry.")
    projection = json.loads((PRE / "full_run_cost_projection.json").read_text(encoding="utf-8"))
    assert projection["fits"] is True and projection["total_worst_case"] <= 18.50
    budget = json.loads((PRE / "interaction_budget.json").read_text(encoding="utf-8"))
    assert budget["MAX_API_TURNS_PER_EPISODE"] == 12
    # console.log L1P-05: budget verified.
    print("[test:llm1-prereg] test_worst_case_fits: passed.")


def test_locks_frozen():
    """Roster, providers, population, schedule, estimand and all-false claims frozen."""
    # console.log L1P-06: locks test entry.
    print("[test:llm1-prereg] test_locks_frozen: entry.")
    roster = json.loads((PRE / "model_roster.json").read_text(encoding="utf-8"))
    assert [m["slug"] for m in roster["models"]] == ["z-ai/glm-4.7-flash", "qwen/qwen3.7-flash", "deepseek/deepseek-v4-flash"]
    assert all(m["temperature"] == 0 for m in roster["models"])
    predicates = json.loads((PRE / "claim_predicates.json").read_text(encoding="utf-8"))
    assert all(value is False for value in predicates["predicates"].values())
    estimand = json.loads((PRE / "primary_estimand.json").read_text(encoding="utf-8"))
    assert estimand["contrast"] == "F000 vs F010" and estimand["promotion_ban"] is True
    population = json.loads((PRE / "population_rule.json").read_text(encoding="utf-8"))
    assert population["design"] == "FULL" and population["subset"] is None
    # console.log L1P-07: locks verified.
    print("[test:llm1-prereg] test_locks_frozen: passed.")
