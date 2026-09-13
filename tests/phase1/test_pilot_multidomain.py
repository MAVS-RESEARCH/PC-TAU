"""G1 test: pilot multi-domain yield meets the strengthened gate (Fix 8)."""

import json
from pathlib import Path

import yaml


# console.log T5-01: test module import confirms multidomain check is active.
print("[test:pilot-multidomain] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_pilot_multidomain():
    """At least 8 viable tasks overall and at least 2 per domain, plus one fallback."""
    # console.log T5-02: multidomain test entry.
    print("[test:pilot-multidomain] test_pilot_multidomain: entry.")
    cfg = yaml.safe_load(open(REPO_ROOT / "configs" / "experiment.yaml", encoding="utf-8"))
    run_id = cfg["run_id"]
    gate = json.loads(
        (REPO_ROOT / "results" / run_id / "pilot" / "gate_log.json").read_text(
            encoding="utf-8"
        )
    )
    rows = gate["rows"]
    viable = [r for r in rows if r["multi_action_viable"]]
    # console.log T5-03: viable rows counted.
    print("[test:pilot-multidomain] viable=%d/%d." % (len(viable), len(rows)))
    assert len(viable) >= 8
    for domain in ["airline", "retail"]:
        count = sum(1 for r in viable if r["domain"] == domain)
        # console.log T5-04: per-domain count checked.
        print("[test:pilot-multidomain] domain=%s viable=%d." % (domain, count))
        assert count >= 2
    assert sum(1 for r in rows if r["finite_fallback"]) >= 1
    # console.log T5-05: multidomain gate verified.
    print("[test:pilot-multidomain] test_pilot_multidomain: passed.")
