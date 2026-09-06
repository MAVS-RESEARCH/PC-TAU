"""G1 test: provisional gate rejects outcome-justified and firewall-violating repairs."""

import sys
from pathlib import Path


# console.log T4-01: test module import confirms rejection check is active.
print("[test:provisional-reject] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def test_provisional_gate_rejects_pc_justification():
    """Bad justifications and bad resource behavior must fail validation."""
    # console.log T4-02: rejection test entry.
    print("[test:provisional-reject] test_provisional_gate_rejects_pc_justification: entry.")
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "phase1_pilot", str(REPO_ROOT / "scripts" / "phase1_pilot.py")
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    bad_label = {
        "qX": {
            "touch": ["R"],
            "tool": "calculate",
            "locator": "x",
            "justification": "chosen for desired Delta_R sign",
            "reads_external": False,
            "reads_unadmitted": False,
            "alters_mapping": False,
            "adds_fact": False,
        }
    }
    ok, problems = module.validate_firewall(bad_label)
    # console.log T4-03: outcome-justified repair checked.
    print("[test:provisional-reject] outcome-justified ok=%s." % ok)
    assert not ok and problems

    bad_r = {
        "qR": {
            "touch": ["R"],
            "tool": "calculate",
            "locator": "x",
            "justification": "policy + tool + channel",
            "reads_external": True,
            "reads_unadmitted": False,
            "alters_mapping": False,
            "adds_fact": False,
        }
    }
    ok_r, _ = module.validate_firewall(bad_r)
    # console.log T4-04: external-reading R repair checked.
    print("[test:provisional-reject] external-R ok=%s." % ok_r)
    assert not ok_r

    bad_e = {
        "qE": {
            "touch": ["E"],
            "tool": "lookup",
            "locator": "x",
            "justification": "policy + tool + channel",
            "reads_external": False,
            "reads_unadmitted": False,
            "alters_mapping": True,
            "adds_fact": True,
        }
    }
    ok_e, _ = module.validate_firewall(bad_e)
    assert not ok_e
    bad_a = {
        "qA": {
            "touch": ["A"],
            "tool": "approval",
            "locator": "x",
            "justification": "policy + tool + channel",
            "reads_external": False,
            "reads_unadmitted": False,
            "alters_mapping": False,
            "adds_fact": True,
        }
    }
    ok_a, _ = module.validate_firewall(bad_a)
    assert not ok_a
    # console.log T4-05: all firewall rejections verified.
    print("[test:provisional-reject] test_provisional_gate_rejects_pc_justification: passed.")
