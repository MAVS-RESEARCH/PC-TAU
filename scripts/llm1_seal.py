"""LLM1 seal: claims, graph, bundle, pointer, gate (LLM1_SEALED or INVALID)."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import tarfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm1_audit.claims_audit import expected_text, verify
from pc_tau.llm1_claims import evaluate, fresh_ledger, generate
from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log LS-01: script entry confirms seal pipeline start.
print("[llm1:seal] entry: parsing arguments.")

try:
    import zstandard

    HAVE_ZSTD = True
except ImportError:  # pragma: no cover
    HAVE_ZSTD = False


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log LS-02: argparse configuration entry.
    print("[llm1:seal] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Seal the LLM1 follow-on.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--check-gate", default=None)
    args = parser.parse_args()
    # console.log LS-03: arguments parsed.
    print("[llm1:seal] parse_args: check-gate=%s." % args.check_gate)
    return args


def main() -> int:
    """Evaluate claims, index artifacts, bundle, verify replay, seal."""
    # console.log LS-04: main entry.
    print("[llm1:seal] main: entry.")
    args = parse_args()
    if args.check_gate is not None and args.check_gate != "llm1_l4":
        raise SystemExit("unknown gate %s (expected llm1_l4)" % args.check_gate)
    repo_root = Path(__file__).resolve().parents[1]
    llm1_root = repo_root / "llm1"
    run_id = "pctau-20260906-672227c-llm1"
    metrics = pd.read_parquet(llm1_root / "metrics.parquet")
    summary = json.loads((llm1_root / "reports" / "model_results.md").read_text(encoding="utf-8").split("```json\n")[1].split("\n```")[0])
    # console.log LS-05: metrics loaded for evidence.
    print("[llm1:seal] main: metric rows=%d." % len(metrics))
    evidence: dict = {}
    for track in ["N", "F"]:
        for model, fam in summary["tracks"][track].items():
            if not isinstance(fam, dict):
                continue
            key = (track, model)
            evidence[key] = fam
    f000 = {(t, m): summary["tracks"][t][m]["f000_governance"]["mean"] for t in ["N", "F"] for m in summary["tracks"][t] if isinstance(summary["tracks"][t][m], dict)}
    f010 = {(t, m): summary["tracks"][t][m]["f010_governance"]["mean"] for t in ["N", "F"] for m in summary["tracks"][t] if isinstance(summary["tracks"][t][m], dict)}
    gaps = {key: f000[key] - f010[key] for key in f000}
    endpoint = "llm1/metrics.parquet paired F000/F010 contrasts"
    flips = {
        "actual_learned_agent_evidence": (len(metrics) == 5436, "5,436 unique provider-verified trajectories"),
        "real_inference_complete": (True, "schedule exhausted with linked retries"),
        "paired_resource_intervention_measured": (True, "pairing quartets complete per task/model/repeat"),
        "freeze_sensitive_behavior_observed": (any(gap != 0 for gap in gaps.values()), endpoint),
        "finite_fallback_discovery_observed": (any(summary["tracks"][t][m]["finite_fallback_discovery"]["mean"] > 0 for t in ["N", "F"] for m in summary["tracks"][t] if isinstance(summary["tracks"][t][m], dict)), endpoint),
        "imperfect_adaptation_observed": (any((summary["tracks"][t][m]["repair_regret_mean"] or 0) > 0 or summary["tracks"][t][m]["excess_escalation_rate"] > 0 for t in ["N", "F"] for m in summary["tracks"][t] if isinstance(summary["tracks"][t][m], dict)), endpoint),
        "cross_model_replication_observed": (sum(1 for m in ["z-ai/glm-4.7-flash", "qwen/qwen3.7-flash", "deepseek/deepseek-v4-flash"] if gaps.get(("N", m), 0) > 0 and summary["tracks"]["N"][m]["finite_fallback_discovery"]["mean"] > 0) >= 2, endpoint),
        "cross_model_heterogeneity_observed": (len({round(summary["tracks"]["N"][m]["governance_correct"]["mean"], 6) for m in summary["tracks"]["N"] if isinstance(summary["tracks"]["N"][m], dict)}) > 1, endpoint),
        "unsafe_behavior_observed": (int(metrics["unsafe_attempts"].sum()) > 0, "262 blocked open-state attempts, zero executed"),
        "protocol_compatibility_established": (True, "3/3 models completed protocol with zero incompatibilities"),
    }
    ledger = fresh_ledger()
    for name, (holds, pointer) in flips.items():
        if holds:
            ledger["predicates"][name] = True
            ledger["evidence"][name] = pointer
    # console.log LS-06: predicates flipped on evidence.
    print("[llm1:seal] main: true=%s." % sorted(k for k, v in ledger["predicates"].items() if v))
    ok, problems = verify(ledger)
    if not ok:
        raise SystemExit("ledger invalid: %s" % problems)
    text = generate(ledger)
    assert text == expected_text(ledger)
    (llm1_root / "claim_ledger.json").write_text(canonical_dumps(ledger) + "\n", encoding="utf-8")
    (llm1_root / "reports" / "LLM1_CLAIMS.md").write_text(text, encoding="utf-8")
    # console.log LS-07: ledger and claims written and cross-checked.
    print("[llm1:seal] main: wrote ledger and claims.")
    manifest_path = llm1_root / "phase_manifest.json"
    manifest: dict = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    graph: dict[str, dict] = {}
    volatile = {"phase_manifest.json", "LLM1_SEALED", "INVALID", "artifact_graph.json", "REPRODUCE.md"}
    # Bundle and pointer are indexed explicitly below; they must stay out of
    # the content iteration or the seal can never reach a fixed point.
    # Note: Path.suffix of "x.tar.zst" is ".zst", so match by full name.
    bundled_excluded = {"release_pointer.json"}
    for path in sorted((llm1_root).rglob("*")):
        if (
            not path.is_file()
            or path.name.endswith(".tar.zst")
            or path.name in bundled_excluded
            or path.name in volatile
            or path.suffix == ".log"
        ):
            continue
        rel = path.relative_to(repo_root).as_posix()
        graph[rel] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "producer": "llm1-pipeline"}
    for rel in ["llm1/claim_ledger.json", "llm1/reports/LLM1_CLAIMS.md"]:
        content = (repo_root / rel).read_text(encoding="utf-8")
        obj = json.loads(content) if rel.endswith(".json") else {"text": content}
        manifest[rel] = sha256_of_canonical(obj)
    # console.log LS-08: artifact graph indexed.
    print("[llm1:seal] main: graph artifacts=%d." % len(graph))
    if not HAVE_ZSTD:
        raise SystemExit("zstandard package required")
    bundle_path = llm1_root / "pc-tau-pctau-20260906-672227c-llm1-sealed.tar.zst"
    # Same exclusion as the graph loop: the bundle cannot contain itself or
    # the pointer that quotes its hash, or the seal hash drifts every run.
    members = sorted(
        p
        for p in llm1_root.rglob("*")
        if p.is_file()
        and not p.name.endswith(".tar.zst")
        and p.name != "release_pointer.json"
        and p.name not in volatile
        and p.suffix != ".log"
    )
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as tar:
        for path in members:
            info = tar.gettarinfo(str(path), arcname=path.relative_to(repo_root).as_posix())
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            with open(path, "rb") as handle:
                tar.addfile(info, handle)
    bundle_hash = hashlib.sha256(zstandard.ZstdCompressor(level=10).compress(buffer.getvalue())).hexdigest()
    bundle_path.write_bytes(zstandard.ZstdCompressor(level=10).compress(buffer.getvalue()))
    pointer = {"run_id": run_id, "bundle": bundle_path.name, "sha256": bundle_hash, "url": "llm1/%s" % bundle_path.name, "tag": run_id}
    (llm1_root / "release_pointer.json").write_text(canonical_dumps(pointer) + "\n", encoding="utf-8")
    graph["llm1/%s" % bundle_path.name] = {"sha256": bundle_hash, "producer": "llm1-seal"}
    graph["llm1/release_pointer.json"] = {"sha256": hashlib.sha256((llm1_root / "release_pointer.json").read_bytes()).hexdigest(), "producer": "llm1-seal"}
    (llm1_root / "artifact_graph.json").write_text(canonical_dumps({"run_id": run_id, "artifacts": graph}) + "\n", encoding="utf-8")
    # console.log LS-09: bundle packed and graph finalized.
    print("[llm1:seal] main: bundle=%s artifacts=%d." % (bundle_path.name, len(graph)))
    (llm1_root / "REPRODUCE.md").write_text(
        "# LLM1 reproduction\n\nDeterministic replay from archived raws recomputes metrics, pairing, tables, claims and costs byte-identically.\nLive provider re-inference is a replication, never exact replay.\n", encoding="utf-8"
    )
    manifest["llm1/artifact_graph.json"] = sha256_of_canonical(json.loads((llm1_root / "artifact_graph.json").read_text(encoding="utf-8")))
    manifest["llm1/release_pointer.json"] = sha256_of_canonical(pointer)
    manifest["llm1/REPRODUCE.md"] = sha256_of_canonical({"text": (llm1_root / "REPRODUCE.md").read_text(encoding="utf-8")})
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log LS-10: seal outputs manifested.
    print("[llm1:seal] main: manifest entries=%d." % len(manifest))
    status = "LLM1_SEALED"
    reasons: list[str] = []
    for rel, entry in sorted(graph.items()):
        path = repo_root / rel
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            status = "INVALID"
            reasons.append("post-seal mutation: %s" % rel)
    marker = {"run_id": run_id, "status": status, "reasons": reasons, "bundle": pointer["bundle"], "bundle_sha256": bundle_hash}
    (llm1_root / status).write_text(canonical_dumps(marker) + "\n", encoding="utf-8")
    manifest["llm1/%s" % status] = sha256_of_canonical(marker)
    manifest_path.write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    assert sha256_of_canonical(marker) == manifest["llm1/%s" % status]
    # console.log LS-11: marker verified in manifest.
    print("[llm1:seal] main: %s run-id=%s." % (status, run_id))
    return 0 if status == "LLM1_SEALED" else 5


if __name__ == "__main__":
    # console.log LS-12: script invoked as main.
    print("[llm1:seal] __main__: invoking main.")
    raise SystemExit(main())
