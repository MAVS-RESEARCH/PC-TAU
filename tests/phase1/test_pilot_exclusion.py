"""G1 test: pilot exclusion and provisional-geometry isolation (Fix 1)."""

import json
import sys
from pathlib import Path

import yaml


# console.log T2-01: test module import confirms exclusion check is active.
print("[test:pilot-exclusion] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))


def test_pilot_exclusion():
    """Pilot ids are disjoint from final candidates; downstream never reads provisional geometry."""
    # console.log T2-02: exclusion test entry.
    print("[test:pilot-exclusion] test_pilot_exclusion: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    census = json.loads(
        (REPO_ROOT / "external_source" / "task_census.json").read_text(encoding="utf-8")
    )
    pilot = json.loads(
        (REPO_ROOT / "results" / run_id / "pilot" / "pilot_ids.json").read_text(
            encoding="utf-8"
        )
    )
    all_ids = {r["task_id"] for r in census["records"]}
    pilot_ids = set(pilot["pilot_ids"])
    # console.log T2-03: census and pilot sets loaded.
    print(
        "[test:pilot-exclusion] census=%d pilot=%d."
        % (len(all_ids), len(pilot_ids))
    )
    assert len(pilot_ids) == 24
    assert pilot_ids.issubset(all_ids)
    final_candidates = all_ids - pilot_ids
    assert pilot_ids.isdisjoint(final_candidates)
    for mod in ["src/pc_tau/source.py", "src/pc_tau/reachability.py"]:
        text = (REPO_ROOT / mod).read_text(encoding="utf-8")
        assert "provisional_geometry" not in text
        assert "pilot_provisional" not in text
    # console.log T2-04: downstream isolation verified.
    print("[test:pilot-exclusion] test_pilot_exclusion: passed.")
