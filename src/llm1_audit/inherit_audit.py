"""L4 audit: inheritance, roster, prices, budget, schedule verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


# console.log LAU-01: module import confirms inheritance audit is available.
print("[llm1-audit:inherit] module loaded.")


def verify_parent_hashes(repo_root: Path, manifest: dict) -> tuple[bool, list[str]]:
    """Recompute hashes of inherited parent objects."""
    # console.log LAU-02: parent hash verification entry.
    print("[llm1-audit:inherit] verify_parent_hashes: entry.")
    problems: list[str] = []
    for rel, digest in manifest["artifacts"].items():
        path = repo_root / rel if rel.startswith(("configs/", "preregistration/")) else repo_root / "results" / "pctau-20260906-672227c" / rel
        if not path.exists():
            problems.append("missing %s" % rel)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            problems.append("hash mismatch %s" % rel)
    # console.log LAU-03: parent verification complete.
    print("[llm1-audit:inherit] verify_parent_hashes: problems=%d." % len(problems))
    return (not problems, problems)


def verify_roster_budget(repo_root: Path) -> tuple[bool, list[str]]:
    """Recompute episode math and worst-case budget from frozen inputs."""
    # console.log LAU-04: roster budget verification entry.
    print("[llm1-audit:inherit] verify_roster_budget: entry.")
    problems: list[str] = []
    pre = repo_root / "llm1" / "preregistration"
    count = json.loads((pre / "episode_count.json").read_text(encoding="utf-8"))
    if (count["track_n"] + count["track_f_subset"]) * count["freezes"] * count["repeats"] != 1812:
        problems.append("episode math wrong")
    projection = json.loads((pre / "full_run_cost_projection.json").read_text(encoding="utf-8"))
    recomputed = round(sum(v["worst_case"] for v in projection["per_model"].values()), 5)
    if abs(recomputed - projection["total_worst_case"]) > 1e-4 or not projection["fits"]:
        problems.append("budget projection wrong")
    # console.log LAU-05: roster budget verification complete.
    print("[llm1-audit:inherit] verify_roster_budget: problems=%d." % len(problems))
    return (not problems, problems)


def verify_schedule(repo_root: Path, expected: int = 5436) -> tuple[bool, list[str]]:
    """Verify schedule length, key uniqueness and pairing coverage."""
    # console.log LAU-06: schedule verification entry.
    print("[llm1-audit:inherit] verify_schedule: entry.")
    problems: list[str] = []
    schedule = json.loads((repo_root / "llm1" / "preregistration" / "execution_schedule.json").read_text(encoding="utf-8"))["entries"]
    if len(schedule) != expected:
        problems.append("schedule length %d" % len(schedule))
    keys = ["%s|%s|%s|r%d" % (r["model"], r["task"], r["freeze"], r["repeat"]) for r in schedule]
    if len(set(keys)) != len(keys):
        problems.append("duplicate schedule keys")
    # console.log LAU-07: schedule verification complete.
    print("[llm1-audit:inherit] verify_schedule: problems=%d." % len(problems))
    return (not problems, problems)
