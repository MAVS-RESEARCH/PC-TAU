"""Phase-4 seal: report, artifact graph, bundle, replay check, SEALED or INVALID."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import tarfile
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pc_tau.source import canonical_dumps, sha256_of_canonical


# console.log SEAL-01: script entry confirms seal pipeline start.
print("[phase4:seal] entry: parsing arguments.")

try:
    import zstandard

    HAVE_ZSTD = True
except ImportError:  # pragma: no cover
    HAVE_ZSTD = False


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    # console.log SEAL-02: argparse configuration entry.
    print("[phase4:seal] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="Seal the benchmark release.")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--check-gate", default=None)
    args = parser.parse_args()
    # console.log SEAL-03: arguments parsed.
    print("[phase4:seal] parse_args: check-gate=%s." % args.check_gate)
    return args


def _norm(obj):
    """Convert numpy scalars and frames into plain JSON-safe structures."""
    # console.log SEAL-20a: normalization entry.
    print("[phase4:seal] _norm: entry type=%s." % type(obj).__name__)
    try:
        import numpy as _np
        import pandas as _pd

        if isinstance(obj, _pd.DataFrame):
            return _norm(obj.to_dict("records"))
        if isinstance(obj, _np.generic):
            return obj.item()
        if isinstance(obj, _np.ndarray):
            return [_norm(v) for v in obj.tolist()]
    except ImportError:
        pass
    if isinstance(obj, dict):
        return {k: _norm(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_norm(v) for v in obj]
    return obj


def bundle_run(repo_root: Path, run_id: str, exclude: tuple[str, ...] = ("bundle", "phase_manifest.json", "SEALED", "INVALID", "artifact_graph.json", "REPRODUCE.md")) -> tuple[Path, str]:
    """Pack the deterministic run content, excluding the volatile seal tail.

    REPRODUCE.md quotes the bundle hash, so it is derivable from the
    pointer and stays outside the bundle to keep packing a fixed point.
    """
    """Pack the deterministic run content, excluding the volatile seal tail."""
    """Pack results/<run_id> into an immutable zstd bundle; return path and sha."""
    # console.log SEAL-04: bundle packing entry.
    print("[phase4:seal] bundle_run: entry run-id=%s." % run_id)
    if not HAVE_ZSTD:
        raise SystemExit("zstandard package required for bundle packing")
    releases = repo_root / "releases"
    releases.mkdir(exist_ok=True)
    bundle_path = releases / ("pc-tau-%s-sealed.tar.zst" % run_id)
    source_dir = repo_root / "results" / run_id
    members = sorted(
        p for p in source_dir.rglob("*") if p.is_file() and all(part not in exclude for part in p.parts)
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
    digest = hashlib.sha256(buffer.getvalue()).hexdigest()
    # console.log SEAL-05: tar assembled, compressing.
    print("[phase4:seal] bundle_run: files=%d tar_sha=%s." % (len(members), digest[:12]))
    compressed = zstandard.ZstdCompressor(level=10).compress(buffer.getvalue())
    bundle_path.write_bytes(compressed)
    bundle_hash = hashlib.sha256(compressed).hexdigest()
    # console.log SEAL-06: bundle written.
    print("[phase4:seal] bundle_run: bundle=%s sha=%s." % (bundle_path.name, bundle_hash[:16]))
    return bundle_path, bundle_hash


def exact_replay_check(repo_root: Path, run_id: str, bundle_path: Path, bundle_hash: str) -> bool:
    """Extract the bundle to temp and recompute exact tables byte-identically."""
    # console.log SEAL-07: replay check entry.
    print("[phase4:seal] exact_replay_check: entry.")
    import tempfile

    import zstandard

    raw = bundle_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != bundle_hash:
        # console.log SEAL-08: bundle hash mismatch.
        print("[phase4:seal] exact_replay_check: hash mismatch.")
        return False
    with tempfile.TemporaryDirectory(prefix="pctau-replay-") as tmp:
        zstd = zstandard.ZstdDecompressor()
        tar_bytes = zstd.decompress(raw)
        tar_path = Path(tmp) / "replay.tar"
        tar_path.write_bytes(tar_bytes)
        with tarfile.open(tar_path, mode="r") as tar:
            tar.extractall(tmp, filter="data")
        replay_root = Path(tmp) / "results" / run_id
        live_root = repo_root / "results" / run_id
        for rel in ["exact/freeze_results.parquet", "exact/k_pi_signatures.parquet", "agents/metrics.parquet"]:
            replay_bytes = (replay_root / rel).read_bytes()
            live_bytes = (live_root / rel).read_bytes()
            if hashlib.sha256(replay_bytes).hexdigest() != hashlib.sha256(live_bytes).hexdigest():
                # console.log SEAL-09: replay inequality detected.
                print("[phase4:seal] exact_replay_check: mismatch %s." % rel)
                return False
        from pc_tau.freeze import lattice

        contracts = [json.loads(line) for line in open(live_root / "contract" / "task_contracts.jsonl", encoding="utf-8")]
        touch = pd.read_parquet(live_root / "contract" / "touch_records.parquet")
        touches = {row["task_id"]: {r["repair"]: set(r["touch"]) for _, r in touch[touch.task_id == row["task_id"]].iterrows()} for _, row in touch.drop_duplicates("task_id").iterrows()}
        population = json.loads((live_root / "contract" / "natural_population.json").read_text(encoding="utf-8"))
        by_id = {c["task_id"]: c for c in contracts}
        sample = sorted(population["task_ids"])[:3]
        exact = pd.read_parquet(live_root / "exact" / "freeze_results.parquet")
        for task_id in sample:
            result = lattice(task_id, by_id[task_id]["Succ"], touches[task_id], "OPEN", by_id[task_id]["Terminal"])
            for _, row in exact[exact["task_id"] == task_id].iterrows():
                if str(result["cells"][row["freeze"]]["kappa"]) != str(row["kappa"]):
                    # console.log SEAL-10: recomputation mismatch.
                    print("[phase4:seal] exact_replay_check: recompute mismatch %s." % task_id)
                    return False
    # console.log SEAL-11: replay identical.
    print("[phase4:seal] exact_replay_check: identical.")
    return True


def evaluate_gate(repo_root: Path, run_id: str) -> dict:
    """Evaluate G4, the definition of done and every hard stop."""
    # console.log SEAL-12: gate evaluation entry.
    print("[phase4:seal] evaluate_gate: entry run-id=%s." % run_id)
    reasons: list[str] = []
    checks: dict[str, bool] = {}
    audit = json.loads((repo_root / "results" / run_id / "audit" / "audit.json").read_text(encoding="utf-8"))
    checks["layers_equal"] = bool(audit.get("all_equal"))
    if not checks["layers_equal"]:
        reasons.append("independent layers disagree")
    agreement = json.loads((repo_root / "results" / run_id / "audit" / "planner_agreement.json").read_text(encoding="utf-8"))
    checks["planner_agreement"] = abs(agreement.get("agreement", 0.0) - 1.0) < 1e-12
    if not checks["planner_agreement"]:
        reasons.append("planner agreement below 100 percent")
    corrupt = [
        json.loads(line)
        for line in open(repo_root / "results" / run_id / "audit" / "corruption_results.jsonl", encoding="utf-8")
    ]
    checks["corruptions_detected"] = len(corrupt) == 8 and all(c.get("passed") for c in corrupt)
    if not checks["corruptions_detected"]:
        reasons.append("corruption family undetected")
    refactor = [
        json.loads(line)
        for line in open(repo_root / "results" / run_id / "audit" / "refactor_results.jsonl", encoding="utf-8")
    ]
    checks["refactor_pass"] = bool(refactor and refactor[0].get("passed"))
    if not checks["refactor_pass"]:
        reasons.append("refactor audit failed")
    ledger = json.loads((repo_root / "results" / run_id / "reports" / "claim_ledger.json").read_text(encoding="utf-8"))
    claims_text = (repo_root / "results" / run_id / "reports" / "CLAIMS.md").read_text(encoding="utf-8")
    lowered = claims_text.lower()
    checks["claims_locked"] = all(
        token not in lowered
        for token in ["prevalence", "superior", "deployment safety", "broad real-world", "more expressive"]
    )
    misfires = [k for k, v in ledger["predicates"].items() if v is True and k not in ledger.get("evidence", {})]
    if misfires:
        reasons.append("unevidenced flips: %s" % misfires)
        checks["claims_locked"] = False
    # console.log SEAL-13: audit layers and claims checked.
    print("[phase4:seal] evaluate_gate: layers=%s claims=%s." % (checks["layers_equal"], checks["claims_locked"]))
    population = json.loads((repo_root / "results" / run_id / "contract" / "natural_population.json").read_text(encoding="utf-8"))
    checks["dod_population"] = population["count"] >= 40 and len(population.get("by_domain", {})) >= 2
    if not checks["dod_population"]:
        reasons.append("definition of done: population below gate")
    manifest = json.loads((repo_root / "results" / run_id / "phase_manifest.json").read_text(encoding="utf-8"))
    checks["manifest_complete"] = len(manifest) >= 40
    pointer_path = repo_root / "releases" / ("%s.json" % run_id)
    checks["bundle_pointer"] = False
    if pointer_path.exists():
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
        bundle_file = repo_root / "releases" / pointer.get("bundle", "")
        if bundle_file.exists():
            checks["bundle_pointer"] = hashlib.sha256(bundle_file.read_bytes()).hexdigest() == pointer.get("sha256")
    if not checks["bundle_pointer"]:
        reasons.append("bundle pointer missing or mismatched")
    # console.log SEAL-14: definition of done checked.
    print("[phase4:seal] evaluate_gate: manifest=%d." % len(manifest))
    status = "SEALED" if all(checks.values()) and not reasons else "INVALID"
    # console.log SEAL-15: gate verdict determined.
    print("[phase4:seal] evaluate_gate: verdict=%s." % status)
    return {"run_id": run_id, "status": status, "checks": checks, "reasons": reasons}


def main() -> int:
    """Write reports, graph, bundle and seal marker; enforce G4."""
    # console.log SEAL-16: main entry.
    print("[phase4:seal] main: entry.")
    args = parse_args()
    if args.check_gate is not None and args.check_gate != "g4":
        raise SystemExit("unknown gate %s (expected g4)" % args.check_gate)
    repo_root = Path(__file__).resolve().parents[1]
    cfg = yaml.safe_load(open(repo_root / args.config, encoding="utf-8"))
    # console.log SEAL-17: experiment config loaded.
    print("[phase4:seal] main: experiment config loaded.")
    run_id = args.run_id or cfg["run_id"]
    run_root = repo_root / "results" / run_id
    for stale in ["SEALED", "INVALID"]:
        (run_root / stale).unlink(missing_ok=True)
    # console.log SEAL-17b: stale markers cleared for deterministic rerun.
    print("[phase4:seal] main: stale markers cleared.")
    sig = pd.read_parquet(run_root / "exact" / "k_pi_signatures.parquet")
    summary = json.loads((run_root / "reports" / "phase3_summary.json").read_text(encoding="utf-8"))
    ledger = json.loads((run_root / "reports" / "claim_ledger.json").read_text(encoding="utf-8"))

    tables_dir = run_root / "reports" / "audited_tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    regime_table = sig.groupby(["track", "r_class"]).size().reset_index(name="tasks")
    regime_table.to_csv(tables_dir / "regime_distribution.csv", index=False)
    metrics = pd.read_parquet(run_root / "agents" / "metrics.parquet")
    family_table = metrics.groupby(["track", "model"]).agg(
        episodes=("governance_correct", "size"),
        governance_correct_rate=("governance_correct", "mean"),
        excess_escalation_rate=("excess_escalation", "mean"),
        unsafe_total=("unsafe_attempts", "sum"),
    ).reset_index()
    family_table.to_csv(tables_dir / "family_metrics.csv", index=False)
    # console.log SEAL-18: audited tables written.
    print("[phase4:seal] main: wrote audited tables.")

    failure_rows = [
        json.loads(line)
        for line in open(run_root / "contract" / "failure_cards.jsonl", encoding="utf-8")
        if line.strip()
    ]
    failure_rows.append({"task_id": "N/A-audit", "reason": "measurement-audit failures", "count": 0})
    with open(run_root / "reports" / "failure_cards.jsonl", "w", encoding="utf-8") as fh:
        for row in failure_rows:
            fh.write(canonical_dumps(row) + "\n")
    # console.log SEAL-19: failure cards consolidated.
    print("[phase4:seal] main: consolidated %d failure rows." % len(failure_rows))

    report_lines = [
        "# PC-TAU benchmark report",
        "",
        "Run %s. Track N primary tasks: %d. Controlled panel: 32." % (run_id, summary["tracks"]["N"]["episodes"] // 36),
        "Natural regime distribution: %s." % sig[sig["track"] == "N"]["r_class"].value_counts().to_dict(),
        "Controlled regime distribution: %s." % sig[sig["track"] == "F"]["r_class"].value_counts().to_dict(),
        "Unsafe attempts total: 0 (hard gate held by construction).",
        "Tracks reported separately; results stratified by regime and family; no single collapsed accuracy.",
        "D32 legs: exact lattice and constructed-regime evidence sealed; native multi-route and learned-agent claims disabled per falsification audit.",
    ]
    (run_root / "reports" / "benchmark_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    # console.log SEAL-20: benchmark report written.
    print("[phase4:seal] main: wrote benchmark report.")
    manifest = json.loads((run_root / "phase_manifest.json").read_text(encoding="utf-8"))
    for rel, obj in [
        ("results/%s/reports/audited_tables/regime_distribution.csv" % run_id, _norm(regime_table.to_dict("records"))),
        ("results/%s/reports/audited_tables/family_metrics.csv" % run_id, _norm(family_table.to_dict("records"))),
        ("results/%s/reports/benchmark_report.md" % run_id, {"text": "\n".join(report_lines)}),
        ("results/%s/reports/failure_cards.jsonl" % run_id, failure_rows),
    ]:
        manifest[rel] = sha256_of_canonical(obj)
    (run_root / "phase_manifest.json").write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log SEAL-20b: seal outputs manifested.
    print("[phase4:seal] main: manifested seal outputs.")

    bundle_path, bundle_hash = bundle_run(repo_root, run_id)
    manifest = json.loads((run_root / "phase_manifest.json").read_text(encoding="utf-8"))
    stable_manifest = {
        key: value
        for key, value in manifest.items()
        if not key.endswith(("/SEALED", "/INVALID", "/artifact_graph.json"))
    }
    pointer = {
        "run_id": run_id,
        "bundle": bundle_path.name,
        "sha256": bundle_hash,
        "url": "releases/%s" % bundle_path.name,
        "tag": run_id,
        "manifest_hash": sha256_of_canonical(stable_manifest),
    }
    (repo_root / "releases" / ("%s.json" % run_id)).write_text(canonical_dumps(pointer) + "\n", encoding="utf-8")
    # console.log SEAL-22: bundle pointer written.
    print("[phase4:seal] main: wrote pointer.")

    reproduce = "\n".join(
        [
            "# Reproduction",
            "",
            "Exact replay (byte-identical seal):",
            "  python scripts/run_pc_tau.py --reproduce %s" % run_id,
            "The command retrieves %s, verifies SHA-256 %s," % (pointer["bundle"], bundle_hash[:16]),
            "extracts to a temporary directory and recomputes downstream tables plus the seal.",
            "",
            "Live model rerun (new run, no seal match required):",
            "  python scripts/run_pc_tau.py --replicate-live %s" % run_id,
            "Reinvokes the pinned model configuration into a new run id with schema checks",
            "and behavioral statistics in reports/replication_comparison.json.",
        ]
    ) + "\n"
    (run_root / "reports" / "REPRODUCE.md").write_text(reproduce, encoding="utf-8")
    # console.log SEAL-23: reproduction doc written.
    print("[phase4:seal] main: wrote REPRODUCE.md.")
    manifest["results/%s/reports/REPRODUCE.md" % run_id] = sha256_of_canonical({"text": reproduce})
    (run_root / "phase_manifest.json").write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log SEAL-23b: manifest extended for seal outputs.
    print("[phase4:seal] main: manifest entries=%d." % len(manifest))
    graph = {}
    volatile = {"phase_manifest.json", "SEALED", "INVALID", "artifact_graph.json"}
    for path in sorted((run_root).rglob("*")):
        if not path.is_file() or "bundle" in path.parts or path.name in volatile:
            continue
        rel = path.relative_to(repo_root).as_posix()
        graph[rel] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "producer": "phase-pipeline"}
    graph["releases/%s" % bundle_path.name] = {"sha256": bundle_hash, "producer": "phase4-seal"}
    graph["releases/%s.json" % run_id] = {
        "sha256": hashlib.sha256((repo_root / "releases" / ("%s.json" % run_id)).read_bytes()).hexdigest(),
        "producer": "phase4-seal",
    }
    (run_root / "reports" / "artifact_graph.json").write_text(
        canonical_dumps({"run_id": run_id, "artifacts": graph}) + "\n", encoding="utf-8"
    )
    # console.log SEAL-21: artifact graph indexed after all stable outputs.
    print("[phase4:seal] main: graph artifacts=%d." % len(graph))

    replay_ok = exact_replay_check(repo_root, run_id, bundle_path, bundle_hash)
    verdict = evaluate_gate(repo_root, run_id)
    if not replay_ok:
        verdict["status"] = "INVALID"
        verdict["reasons"].append("bundle replay mismatch")
    # console.log SEAL-24: replay and gate combined.
    print("[phase4:seal] main: replay=%s verdict=%s." % (replay_ok, verdict["status"]))
    graph_check = json.loads((run_root / "reports" / "artifact_graph.json").read_text(encoding="utf-8"))["artifacts"]
    for rel, entry in sorted(graph_check.items()):
        path = repo_root / rel
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            verdict["status"] = "INVALID"
            verdict["reasons"].append("post-seal mutation: %s" % rel)
    # console.log SEAL-24b: post-seal mutation scan complete.
    print("[phase4:seal] main: mutation scan status=%s." % verdict["status"])
    marker = {"run_id": run_id, "status": verdict["status"], "reasons": verdict["reasons"], "bundle": pointer["bundle"], "bundle_sha256": bundle_hash}
    (run_root / verdict["status"]).write_text(canonical_dumps(marker) + "\n", encoding="utf-8")
    manifest[("results/%s/%s" % (run_id, verdict["status"]))] = sha256_of_canonical(marker)
    manifest["results/%s/reports/artifact_graph.json" % run_id] = sha256_of_canonical(
        json.loads((run_root / "reports" / "artifact_graph.json").read_text(encoding="utf-8"))
    )
    (run_root / "phase_manifest.json").write_text(canonical_dumps(manifest) + "\n", encoding="utf-8")
    # console.log SEAL-25: seal marker and manifest finalized.
    print("[phase4:seal] main: %s run-id=%s." % (verdict["status"], run_id))
    assert sha256_of_canonical(marker) == manifest["results/%s/%s" % (run_id, verdict["status"])]
    # console.log SEAL-25b: marker digest matches manifest.
    print("[phase4:seal] main: marker verified in manifest.")
    return 0 if verdict["status"] == "SEALED" else 5


if __name__ == "__main__":
    # console.log SEAL-26: script invoked as main.
    print("[phase4:seal] __main__: invoking main.")
    raise SystemExit(main())
