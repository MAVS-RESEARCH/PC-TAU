"""Phase-1 upstream source locking, task census and pilot selection.

Scope is limited to immutable source material. This module records
repository identity, enumerates tasks from upstream data files, and
selects throwaway pilot identifiers. It performs no closure analysis,
no freeze analysis and no learned-agent work.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


# console.log SRC-01: module import confirms source utilities are available.
print("[phase1:source] module loaded: pin/census/pilot utilities ready.")


def canonical_dumps(obj: Any) -> str:
    """Serialize to canonical JSON (sorted keys, compact separators, utf-8)."""
    # console.log SRC-02: canonical serialization entry.
    print("[phase1:source] canonical_dumps: serializing object with sorted keys.")
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    # console.log SRC-03: canonical serialization complete.
    print("[phase1:source] canonical_dumps: complete, length=%d." % len(text))
    return text


def sha256_of_canonical(obj: Any) -> str:
    """SHA-256 of the canonical JSON encoding of obj."""
    # console.log SRC-04: canonical hash entry.
    print("[phase1:source] sha256_of_canonical: hashing canonical encoding.")
    digest = hashlib.sha256(canonical_dumps(obj).encode("utf-8")).hexdigest()
    # console.log SRC-05: canonical hash complete.
    print("[phase1:source] sha256_of_canonical: digest=%s." % digest[:12])
    return digest


def sha256_of_file(path: Path) -> str:
    """SHA-256 of raw file bytes."""
    # console.log SRC-06: file hash entry.
    print("[phase1:source] sha256_of_file: hashing %s." % path.name)
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    digest = h.hexdigest()
    # console.log SRC-07: file hash complete.
    print("[phase1:source] sha256_of_file: %s digest=%s." % (path.name, digest[:12]))
    return digest


def _git(args: list[str], cwd: Path) -> str:
    """Run a git command and return stripped stdout."""
    # console.log SRC-08: git subprocess entry.
    print("[phase1:source] _git: running git %s." % " ".join(args))
    out = subprocess.run(
        ["git"] + args, cwd=str(cwd), capture_output=True, text=True, check=True
    )
    result = out.stdout.strip()
    # console.log SRC-09: git subprocess complete.
    print("[phase1:source] _git: complete, output length=%d." % len(result))
    return result


def pin_source(
    url: str,
    expected_rev: str,
    upstream_dir: Path,
    repo_root: Path,
) -> dict[str, Any]:
    """Record immutable upstream identity without importing upstream code.

    Reads commit SHA from the cloned directory, hashes the source tree
    (sorted relative paths, excluding .git), hashes uv.lock, and records
    environment identity, license text reference and attribution.
    """
    # console.log SRC-10: pin_source entry.
    print("[phase1:source] pin_source: entry url=%s rev=%s." % (url, expected_rev[:7]))
    commit_sha = _git(["rev-parse", "HEAD"], upstream_dir)
    if commit_sha != expected_rev:
        raise ValueError(
            "upstream HEAD %s does not match expected %s" % (commit_sha, expected_rev)
        )
    # console.log SRC-11: commit SHA verified.
    print("[phase1:source] pin_source: commit SHA verified %s." % commit_sha[:12])
    files: list[str] = []
    per_file: dict[str, str] = {}
    for root, dirs, names in os.walk(upstream_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        for name in sorted(names):
            full = Path(root) / name
            rel = full.relative_to(upstream_dir).as_posix()
            files.append(rel)
            per_file[rel] = sha256_of_file(full)
    files.sort()
    # console.log SRC-12: source tree enumeration complete.
    print("[phase1:source] pin_source: enumerated %d files for tree hash." % len(files))
    tree_payload = {
        "files": files,
        "hashes": per_file,
    }
    tree_hash = sha256_of_canonical(tree_payload)
    # console.log SRC-13: tree hash complete.
    print("[phase1:source] pin_source: tree_hash=%s." % tree_hash[:16])
    uv_lock = upstream_dir / "uv.lock"
    dep_lock = {
        "uv_lock_sha256": sha256_of_file(uv_lock) if uv_lock.exists() else None,
        "python_version": sys.version.split()[0],
        "pyproject": "external_source/_upstream/pyproject.toml",
    }
    env_identity = {
        "os": platform.platform(),
        "python": sys.version.replace("\n", " "),
    }
    license_path = upstream_dir / "LICENSE"
    license_text = license_path.read_text(encoding="utf-8") if license_path.exists() else ""
    manifest = {
        "url": url,
        "commit_sha": commit_sha,
        "tree_hash": tree_hash,
        "file_count": len(files),
        "dep_lock": dep_lock,
        "env_identity": env_identity,
        "license_file": "external_source/_upstream/LICENSE",
        "license_head": license_text[:500],
        "attribution": "Sierra Research tau2-bench; see upstream LICENSE and citation in WorkPlan Appendix.",
        "repo_root": repo_root.as_posix(),
    }
    # console.log SRC-14: pin_source manifest assembled.
    print("[phase1:source] pin_source: manifest assembled with %d files." % len(files))
    return manifest


def _tool_surface(tool_path: Path) -> list[str]:
    """Parse top-level tool function names via regex (no import)."""
    # console.log SRC-15: tool surface parse entry.
    print("[phase1:source] _tool_surface: parsing %s." % tool_path.name)
    text = tool_path.read_text(encoding="utf-8")
    names = sorted(set(re.findall(r"def (\w+)", text)))
    # console.log SRC-16: tool surface parse complete.
    print("[phase1:source] _tool_surface: found %d functions." % len(names))
    return names


def census(
    upstream_dir: Path,
    domains: list[str],
) -> list[dict[str, Any]]:
    """Enumerate tasks for the given domains from upstream data files.

    For each task emit identifiers, locators, tool surface, database
    outline, user outline and upstream evaluation criteria. No agent
    logic is imported.
    """
    # console.log SRC-17: census entry.
    print("[phase1:source] census: entry domains=%s." % ",".join(domains))
    records: list[dict[str, Any]] = []
    for domain in sorted(domains):
        task_file = upstream_dir / "data" / "tau2" / "domains" / domain / "tasks.json"
        split_file = (
            upstream_dir / "data" / "tau2" / "domains" / domain / "split_tasks.json"
        )
        tool_file = upstream_dir / "src" / "tau2" / "domains" / domain / "tools.py"
        db_file = upstream_dir / "data" / "tau2" / "domains" / domain / "db.json"
        # console.log SRC-18: domain file paths resolved.
        print("[phase1:source] census: resolved paths for domain=%s." % domain)
        tasks = json.loads(task_file.read_text(encoding="utf-8"))
        splits: dict[str, Any] = {}
        if split_file.exists():
            splits = json.loads(split_file.read_text(encoding="utf-8"))
        tools = _tool_surface(tool_file) if tool_file.exists() else []
        db_keys: list[str] = []
        if db_file.exists() and db_file.stat().st_size < 50_000_000:
            try:
                db_text = db_file.read_text(encoding="utf-8")
                db_obj = json.loads(db_text)
                if isinstance(db_obj, dict):
                    db_keys = sorted(db_obj.keys())[:50]
            except Exception:
                db_keys = ["unparsed"]
        # console.log SRC-19: domain metadata loaded.
        print(
            "[phase1:source] census: domain=%s tasks=%d tools=%d."
            % (domain, len(tasks), len(tools))
        )
        split_of: dict[str, str] = {}
        for split_name, ids in splits.items():
            if isinstance(ids, list):
                for tid in ids:
                    split_of[str(tid)] = split_name
        for task in tasks:
            tid = str(task.get("id"))
            records.append(
                {
                    "task_id": "%s:%s" % (domain, tid),
                    "domain": domain,
                    "upstream_id": tid,
                    "split": split_of.get(tid, "unknown"),
                    "policy_locator": "external_source/_upstream/src/tau2/domains/%s/tools.py"
                    % domain,
                    "task_locator": "external_source/_upstream/data/tau2/domains/%s/tasks.json#%s"
                    % (domain, tid),
                    "tool_surface": tools,
                    "db_outline": db_keys,
                    "user_outline": str(
                        (task.get("user_scenario") or {}).get("instructions")
                        or task.get("user_scenario")
                        or ""
                    )[:500],
                    "eval_criteria": task.get("evaluation_criteria"),
                }
            )
    records.sort(key=lambda r: (r["domain"], r["upstream_id"]))
    # console.log SRC-20: census complete.
    print("[phase1:source] census: complete records=%d." % len(records))
    return records


def select_pilot(
    records: list[dict[str, Any]],
    seed: int,
    per_domain: int = 12,
) -> dict[str, Any]:
    """Deterministic pilot selection of per_domain ids per domain.

    Selects from the development-only (train) split where available,
    otherwise from all records, using a seeded shuffle over sorted ids.
    """
    # console.log SRC-21: select_pilot entry.
    print(
        "[phase1:source] select_pilot: entry seed=%d per_domain=%d." % (seed, per_domain)
    )
    by_domain: dict[str, list[str]] = {}
    for rec in records:
        by_domain.setdefault(rec["domain"], []).append(rec["task_id"])
    selection: dict[str, list[str]] = {}
    for domain in sorted(by_domain):
        train_ids = sorted(
            r["task_id"]
            for r in records
            if r["domain"] == domain and r["split"] == "train"
        )
        pool = train_ids if len(train_ids) >= per_domain else sorted(by_domain[domain])
        # console.log SRC-22: pilot pool resolved per domain.
        print(
            "[phase1:source] select_pilot: domain=%s pool=%d (train=%d)."
            % (domain, len(pool), len(train_ids))
        )
        rng = random.Random(seed + sum(ord(c) for c in domain))
        shuffled = list(pool)
        rng.shuffle(shuffled)
        selection[domain] = shuffled[:per_domain]
    pilot_ids = sorted([tid for ids in selection.values() for tid in ids])
    result = {
        "seed": seed,
        "per_domain": per_domain,
        "selection_rule": "sorted train-split ids, seeded shuffle per domain (seed + domain ordinal sum), first N per domain; train split is the development-only split",
        "by_domain": {k: sorted(v) for k, v in sorted(selection.items())},
        "pilot_ids": pilot_ids,
        "excluded_forever": pilot_ids,
    }
    # console.log SRC-23: select_pilot complete.
    print("[phase1:source] select_pilot: complete total=%d." % len(pilot_ids))
    return result
