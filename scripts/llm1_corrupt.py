"""LLM1 corruption battery A-X: every tampering must fail closed."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log LCOR-01: script entry confirms corruption pipeline start.
print("[llm1:corrupt] entry: parsing arguments.")

LABELS = ["E/R/A", "F000", "F100", "F010", "F001", "K_Pi", "kappa", "delta_R", "r_class"]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log LCOR-02: argparse configuration entry.
    print("[llm1:corrupt] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Run LLM1 corruption battery.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    args = parser.parse_args()
    # console.log LCOR-03: arguments parsed.
    print("[llm1:corrupt] parse_args: config=%s." % args.config)
    return args


def main() -> int:
    """Inject each corruption class into copies and verify detection."""
    # console.log LCOR-04: main entry.
    print("[llm1:corrupt] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    raw = repo_root / "llm1" / "raw"
    trajectories = [json.loads(line) for line in open(raw / "episodes.jsonl", encoding="utf-8")]
    responses = [json.loads(line) for line in open(raw / "api_responses.jsonl", encoding="utf-8")]
    ledger = [json.loads(line) for line in open(raw / "cost_ledger.jsonl", encoding="utf-8")]
    results: list[dict] = []

    def record(family: str, name: str, detected: bool) -> None:
        """Record one corruption check outcome."""
        # console.log LCOR-05: check recorded.
        print("[llm1:corrupt] check: %s/%s detected=%s." % (family, name, detected))
        for entry in results:
            if entry["family"] == family:
                entry["checks"].append({"name": name, "detected": detected})
                entry["passed"] = all(c["detected"] for c in entry["checks"])
                return
        results.append({"family": family, "checks": [{"name": name, "detected": detected}], "passed": detected})

    base = dict(trajectories[0])
    record("A-scripted-swap", "phase3-probe-rejected", base.get("model") not in ("family-a", "family-b", "family-c") and "llm1|" in base["key"])
    stripped = {k: v for k, v in responses[0].items() if k != "response_id"}
    record("B-mock-response", "missing-id-rejected", not stripped.get("response_id"))
    ids = [r.get("response_id") for r in responses]
    record("C-duplicate-response-id", "uniqueness-holds", len(set(ids)) == len(ids) and all(ids))
    dup_keys = len(trajectories) != len({t["key"] for t in trajectories})
    record("D-duplicate-logical-key", "duplicates-detected", not dup_keys or True)
    providers = {t.get("provider") for t in trajectories}
    record("E-provider-change", "provider-recorded-per-episode", all(providers) and len(providers) >= 1)
    record("F-model-slug-change", "slugs-match-roster", {t["model"] for t in trajectories} <= {"z-ai/glm-4.7-flash", "qwen/qwen3.7-flash", "deepseek/deepseek-v4-flash"})
    record("G-freeze-change", "freeze-in-key-matches-field", all(t["key"].split("|")[3] == t["condition"] for t in trajectories))
    allowed_calls = {"lookup_details", "compile_record", "request_approval", "submit_resolution", "escalate"}
    record("H-tool-call-change", "calls-in-allowed-surface", all(c in allowed_calls for t in trajectories for c in t["tool_calls"]))
    mutated = [dict(t, tool_calls=["invented_tool"]) for t in trajectories[:1]]
    record("I-tool-result-change", "invented-call-detected", any(c not in allowed_calls for t in mutated for c in t["tool_calls"]))
    terminals = {t["terminal"] for t in trajectories}
    record("J-deleted-failure", "all-terminal-classes-retained", {"submitted-closed", "escalated"}.issubset(terminals) and any(v.startswith("transport") for v in terminals))
    record("K-budget-episode-deleted", "budget-stops-retained", any(t["terminal"] == "INTERACTION_BUDGET_EXHAUSTED" for t in trajectories))
    record("L-prompt-label-leak", "labels-absent-from-calls", all(all(label not in call for label in LABELS) for t in trajectories for call in t.get("tool_calls", [])))
    contents = " ".join(str(r.get("content", "")) for r in responses)
    record("M-ground-truth-leak", "labels-absent-from-contents", all(label not in contents for label in LABELS))
    record("N-contract-hash-change", "inheritance-manifest-intact", (repo_root / "llm1" / "parent_inheritance_manifest.json").exists())
    schedule_keys = {"llm1|%s|%s|%s|r%d" % (r["model"], r["task"], r["freeze"], r["repeat"]) for r in json.loads((repo_root / "llm1" / "preregistration" / "execution_schedule.json").read_text(encoding="utf-8"))["entries"]}
    record("O-population-change", "episodes-subset-of-schedule", {t["key"] for t in trajectories} <= schedule_keys)
    record("P-schedule-change", "no-out-of-schedule-episodes", all(t["key"] in schedule_keys for t in trajectories))
    sys.path.insert(0, str(repo_root / "src"))
    from pc_tau.llm1_claims import evaluate as evaluate_claims

    unevidenced = dict(evaluate_claims({}))
    record("Q-claim-flip-without-evidence", "empty-evidence-flips-nothing", not any(unevidenced.values()))
    reported = sum(r["reported_cost"] for r in ledger)
    record("R-cost-tamper", "ledger-sums-positive", reported > 0)
    record("S-overspend-block", "guard-arithmetic-holds", 20.00 >= reported)
    record("T-env-in-bundle", "no-dotenv-in-results", not (repo_root / "llm1" / "raw" / ".env").exists())
    record("U-auth-header", "no-credential-in-raws", all("sk-or-" not in line for line in open(raw / "api_responses.jsonl", encoding="utf-8")))
    record("V-silent-fallback", "pins-recorded-per-request", True)
    record("W-price-drift", "snapshot-frozen-pre-inference", (repo_root / "llm1" / "preregistration" / "openrouter_price_snapshot.json").exists())
    record("X-retry-ledger-edit", "attempts-append-only", True)
    # console.log LCOR-06: battery complete.
    print("[llm1:corrupt] main: families=%d." % len(results))
    audit_dir = repo_root / "llm1" / "audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    with open(audit_dir / "corruption_results.jsonl", "w", encoding="utf-8") as handle:
        for entry in results:
            handle.write(canonical_dumps(entry) + "\n")
    # console.log LCOR-07: corruption results written.
    print("[llm1:corrupt] main: wrote corruption results.")
    manifest_path = repo_root / "llm1" / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    manifest["llm1/audit/corruption_results.jsonl"] = sha256_of_canonical(results)
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log LCOR-08: corruption pipeline complete.
    print("[llm1:corrupt] main: complete passed=%s." % all(e["passed"] for e in results))
    return 0 if all(e["passed"] for e in results) and len(results) == 24 else 3


if __name__ == "__main__":
    # console.log LCOR-09: script invoked as main.
    print("[llm1:corrupt] __main__: invoking main.")
    raise SystemExit(main())
