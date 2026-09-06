"""Phase-2 Pass A: frozen-protocol source extraction (Fix 2)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.semantics import EXTRACTION_RULES, extract_facts
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log EXT-01: script entry confirms extraction pipeline start.
print("[phase2:extract] entry: parsing arguments.")


TOOL_LOCATORS = {
    "airline": {
        "get_reservation_details": "external_source/_upstream/src/tau2/domains/airline/tools.py:371",
        "calculate": "external_source/_upstream/src/tau2/domains/airline/tools.py:321",
        "transfer_to_human_agents": "external_source/_upstream/src/tau2/domains/airline/tools.py:532",
    },
    "retail": {
        "get_order_details": "external_source/_upstream/src/tau2/domains/retail/tools.py:333",
        "calculate": "external_source/_upstream/src/tau2/domains/retail/tools.py:141",
        "transfer_to_human_agents": "external_source/_upstream/src/tau2/domains/retail/tools.py:732",
    },
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log EXT-02: argparse configuration entry.
    print("[phase2:extract] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Extract Pass-A semantic facts.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    # console.log EXT-03: arguments parsed.
    print("[phase2:extract] parse_args: config=%s." % args.config)
    return args


def update_manifest(repo_root: Path, run_id: str, rel_path: str, obj: object) -> str:
    """Append file hash to run manifest."""
    # console.log EXT-04: manifest update entry.
    print("[phase2:extract] update_manifest: entry %s." % rel_path)
    manifest_path = repo_root / "results" / run_id / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    digest = sha256_of_canonical(obj)
    manifest[rel_path] = digest
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log EXT-05: manifest update complete.
    print("[phase2:extract] update_manifest: %s -> %s." % (rel_path, digest[:12]))
    return digest


def main() -> int:
    """Extract facts for all non-pilot candidates and freeze the protocol."""
    # console.log EXT-06: main entry.
    print("[phase2:extract] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log EXT-07: experiment config loaded.
    print("[phase2:extract] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    upstream_sha = cfg["upstream"]["commit_sha"]
    census = json.loads(
        (repo_root / "external_source" / "task_census.json").read_text(encoding="utf-8")
    )
    pilot = json.loads(
        (repo_root / "results" / run_id / "pilot" / "pilot_ids.json").read_text(
            encoding="utf-8"
        )
    )
    excluded = set(pilot["pilot_ids"])
    # console.log EXT-08: census and exclusion list loaded.
    print(
        "[phase2:extract] main: census=%d excluded=%d."
        % (len(census["records"]), len(excluded))
    )
    candidates = [r for r in census["records"] if r["task_id"] not in excluded]
    facts: list[dict] = []
    for rec in candidates:
        domain = rec["domain"]
        surface = rec["tool_surface"][:8]
        locators = TOOL_LOCATORS.get(domain, {})
        facts.extend(extract_facts(rec, surface, locators, upstream_sha))
    # console.log EXT-09: extraction complete for all candidates.
    print(
        "[phase2:extract] main: extracted facts=%d candidates=%d."
        % (len(facts), len(candidates))
    )
    contract_dir = repo_root / "results" / run_id / "contract"
    contract_dir.mkdir(parents=True, exist_ok=True)
    facts_path = contract_dir / "semantic_facts.jsonl"
    with open(facts_path, "w", encoding="utf-8") as fh:
        for fact in facts:
            fh.write(canonical_dumps(fact) + "\n")
    # console.log EXT-10: semantic facts written.
    print("[phase2:extract] main: wrote %s." % facts_path.as_posix())
    protocol = {
        "run_id": run_id,
        "frozen": True,
        "rules": EXTRACTION_RULES,
        "llm_extractor": None,
        "llm_prompt_hash": None,
        "llm_note": "rule-based source-only extractor; no LLM used; prompt concept not applicable",
        "verifiers": ["alternate-normalizer second path (semantics.verify_facts)"],
        "upstream_sha": upstream_sha,
    }
    protocol_path = contract_dir / "extraction_protocol.json"
    protocol_path.write_text(canonical_dumps(protocol) + "\n", encoding="utf-8")
    # console.log EXT-11: extraction protocol frozen and written.
    print("[phase2:extract] main: wrote %s." % protocol_path.as_posix())
    update_manifest(
        repo_root, run_id, "results/%s/contract/semantic_facts.jsonl" % run_id, facts
    )
    update_manifest(
        repo_root, run_id, "results/%s/contract/extraction_protocol.json" % run_id, protocol
    )
    # console.log EXT-12: extraction pipeline complete.
    print("[phase2:extract] main: complete run-id=%s." % run_id)
    return 0


if __name__ == "__main__":
    # console.log EXT-13: script invoked as main.
    print("[phase2:extract] __main__: invoking main.")
    raise SystemExit(main())
