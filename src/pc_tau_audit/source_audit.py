"""Audit layer: source rehash, ID reconstruction, pilot exclusion, fallback logic."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any


# console.log AUDS-01: module import confirms source audit is available.
print("[audit:source] module loaded.")


def rehash_source(upstream_dir: Path) -> dict[str, Any]:
    """Independently rehash the pinned upstream tree (different code text)."""
    # console.log AUDS-02: rehash entry.
    print("[audit:source] rehash_source: entry.")
    commit = subprocess.run(
        ["git", "-C", str(upstream_dir), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    names: list[str] = []
    digests: dict[str, str] = {}
    for base, dirs, files in os.walk(upstream_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        for name in sorted(files):
            full = Path(base) / name
            rel = full.relative_to(upstream_dir).as_posix()
            names.append(rel)
            buffer = hashlib.sha256()
            with open(full, "rb") as handle:
                for chunk in iter(lambda: handle.read(65536), b""):
                    buffer.update(chunk)
            digests[rel] = buffer.hexdigest()
    names.sort()
    payload = json.dumps(
        {"files": names, "hashes": digests}, sort_keys=True, separators=(",", ":")
    )
    tree = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    # console.log AUDS-03: rehash complete.
    print("[audit:source] rehash_source: commit=%s files=%d." % (commit[:12], len(names)))
    return {"commit_sha": commit, "tree_hash": tree, "file_count": len(names)}


def reconstruct_ids(census_records: list[dict], seed: int, per_domain: int) -> dict[str, list[str]]:
    """Reconstruct pilot IDs from the preregistered rule (independent text)."""
    # console.log AUDS-04: reconstruction entry.
    print("[audit:source] reconstruct_ids: entry seed=%d." % seed)
    import random

    by_domain: dict[str, list[str]] = {}
    for record in census_records:
        by_domain.setdefault(record["domain"], []).append(record)
    selection: dict[str, list[str]] = {}
    for domain in sorted(by_domain):
        train = sorted(r["task_id"] for r in by_domain[domain] if r["split"] == "train")
        pool = train if len(train) >= per_domain else sorted(r["task_id"] for r in by_domain[domain])
        engine = random.Random(seed + sum(ord(c) for c in domain))
        shuffled = list(pool)
        engine.shuffle(shuffled)
        selection[domain] = sorted(shuffled[:per_domain])
    # console.log AUDS-05: reconstruction complete.
    print("[audit:source] reconstruct_ids: complete.")
    return selection


def check_fallback(population_count: int, domain_count: int, telecom_used: bool) -> bool:
    """Verify the N<40 OR domains<2 trigger was applied correctly."""
    # console.log AUDS-06: fallback check entry.
    print("[audit:source] check_fallback: entry N=%d domains=%d." % (population_count, domain_count))
    should_activate = population_count < 40 or domain_count < 2
    ok = telecom_used == should_activate
    # console.log AUDS-07: fallback check complete.
    print("[audit:source] check_fallback: ok=%s." % ok)
    return ok
