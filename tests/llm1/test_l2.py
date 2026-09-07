"""LLM1 L2 tests: live provenance, pairing structure, blinded naming."""

import json
from pathlib import Path


# console.log L2T-01: test module import confirms L2 checks are active.
print("[test:llm1-l2] module loaded.")

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW = REPO_ROOT / "llm1" / "raw"
BLINDED = {"lookup_details", "compile_record", "request_approval", "submit_resolution", "escalate"}


def test_live_provenance():
    """Every episode has real provider evidence with unique keys and IDs."""
    # console.log L2T-02: provenance test entry.
    print("[test:llm1-l2] test_live_provenance: entry.")
    episodes = [json.loads(line) for line in open(RAW / "episodes.jsonl", encoding="utf-8")]
    responses = [json.loads(line) for line in open(RAW / "api_responses.jsonl", encoding="utf-8")]
    assert len(episodes) == 5436
    assert len({e["key"] for e in episodes}) == 5436
    assert all(r.get("response_id") for r in responses)
    assert len({r["response_id"] for r in responses}) == len(responses)
    # console.log L2T-03: provenance verified.
    print("[test:llm1-l2] test_live_provenance: passed.")


def test_no_scripted_markers():
    """No probe-harness or internal-repair names appear in trajectories."""
    # console.log L2T-04: marker test entry.
    print("[test:llm1-l2] test_no_scripted_markers: entry.")
    episodes = [json.loads(line) for line in open(RAW / "episodes.jsonl", encoding="utf-8")]
    for episode in episodes:
        for call in episode["tool_calls"]:
            assert call in BLINDED, call
            assert not call.startswith("qR_") and not call.startswith("qE_") and not call.startswith("qA_")
    # console.log L2T-05: naming verified blinded.
    print("[test:llm1-l2] test_no_scripted_markers: passed.")


def test_pairing_structure():
    """Each task/model/repeat group carries exactly the four freezes."""
    # console.log L2T-06: pairing test entry.
    print("[test:llm1-l2] test_pairing_structure: entry.")
    episodes = [json.loads(line) for line in open(RAW / "episodes.jsonl", encoding="utf-8")]
    groups: dict[tuple, list] = {}
    for episode in episodes:
        groups.setdefault((episode["model"], episode["task_id"], episode["key"].split("|")[-1]), []).append(episode["condition"])
    assert groups
    assert all(sorted(cells) == ["F000", "F001", "F010", "F100"] for cells in groups.values())
    # console.log L2T-07: pairing verified.
    print("[test:llm1-l2] test_pairing_structure: passed.")
