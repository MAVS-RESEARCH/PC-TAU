"""P2 test: pilot exclusion and provisional invisibility hold in Phase 2."""

import json
from pathlib import Path

import yaml


# console.log P2T05-01: test module import confirms exclusion check is active.
print("[test:p2-pilot-exclusion] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_pilot_exclusion_p2():
    """No pilot id in primary, sidecar or panel; no provisional reads."""
    # console.log P2T05-02: exclusion test entry.
    print("[test:p2-pilot-exclusion] test_pilot_exclusion_p2: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    contract_dir = REPO_ROOT / "results" / run_id / "contract"
    pilot = set(
        json.loads((REPO_ROOT / "results" / run_id / "pilot" / "pilot_ids.json").read_text(encoding="utf-8"))[
            "pilot_ids"
        ]
    )
    population = json.loads((contract_dir / "natural_population.json").read_text(encoding="utf-8"))
    assert pilot.isdisjoint(population["task_ids"])
    partials = [json.loads(line)["task_id"] for line in open(contract_dir / "partial_tasks.jsonl", encoding="utf-8") if line.strip()]
    assert pilot.isdisjoint(partials)
    panel = json.loads((contract_dir / "controlled_panel.json").read_text(encoding="utf-8"))
    for task in panel["tasks"]:
        assert task["base_task_id"] not in pilot and task["non_pilot_base"] is True
    # console.log P2T05-03: population and panel exclusion verified.
    print("[test:p2-pilot-exclusion] populations clean.")
    for rel in ["src/pc_tau/semantics.py", "src/pc_tau/repairs.py", "src/pc_tau/touch.py", "scripts/phase2_eligibility.py"]:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        assert "provisional_geometry" not in text and "pilot_provisional" not in text
    # console.log P2T05-04: provisional invisibility verified.
    print("[test:p2-pilot-exclusion] test_pilot_exclusion_p2: passed.")
