"""PC-TAU dispatcher: run phase pipelines and gate checks (WorkPlan App. C)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


# console.log RUN-01: dispatcher entry confirms argument parsing start.
print("[run:dispatcher] entry: parsing arguments.")


def parse_args() -> argparse.Namespace:
    """Parse dispatcher arguments."""
    # console.log RUN-02: argparse configuration entry.
    print("[run:dispatcher] parse_args: configuring parser.")
    parser = argparse.ArgumentParser(description="PC-TAU phase dispatcher.")
    parser.add_argument("--check-gate", default=None, help="g1|g2|g3|g4")
    parser.add_argument("--config", default="configs/experiment.yaml")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--reproduce", default=None)
    parser.add_argument("--replicate-live", default=None)
    args = parser.parse_args()
    # console.log RUN-03: arguments parsed.
    print("[run:dispatcher] parse_args: check-gate=%s." % args.check_gate)
    return args


def run_script(repo_root: Path, name: str, extra: list[str]) -> int:
    """Invoke a phase script as a subprocess."""
    # console.log RUN-04: subprocess invocation entry.
    print("[run:dispatcher] run_script: invoking %s." % name)
    cmd = [sys.executable, str(repo_root / "scripts" / name)] + extra
    proc = subprocess.run(cmd, cwd=str(repo_root))
    # console.log RUN-05: subprocess complete.
    print("[run:dispatcher] run_script: %s exit=%d." % (name, proc.returncode))
    return proc.returncode


def main() -> int:
    """Dispatch phase pipelines, gate checks and reproduction paths."""
    # console.log RUN-06: main entry.
    print("[run:dispatcher] main: entry.")
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    extra = ["--config", args.config]
    if args.run_id:
        extra += ["--run-id", args.run_id]
    if args.check_gate == "g1":
        # console.log RUN-07: delegating to Phase-1 gate.
        print("[run:dispatcher] main: delegating to g1.")
        return run_script(repo_root, "phase1_preregister.py", extra + ["--check-gate", "g1"])
    if args.check_gate == "g2":
        # console.log RUN-07b: delegating to Phase-2 gate.
        print("[run:dispatcher] main: delegating to g2.")
        return run_script(repo_root, "phase2_gate.py", extra + ["--check-gate", "g2"])
    if args.check_gate == "g3":
        # console.log RUN-07c: delegating to Phase-3 gate.
        print("[run:dispatcher] main: delegating to g3.")
        return run_script(repo_root, "phase3_gate.py", extra + ["--check-gate", "g3"])
    if args.check_gate == "g4":
        # console.log RUN-07d: delegating to Phase-4 seal gate.
        print("[run:dispatcher] main: delegating to g4.")
        return run_script(repo_root, "phase4_seal.py", extra + ["--check-gate", "g4"])
    if args.reproduce:
        # console.log RUN-09: exact replay via bundle pointer.
        print("[run:dispatcher] main: exact replay %s." % args.reproduce)
        return run_script(repo_root, "phase4_seal.py", ["--config", args.config, "--run-id", args.reproduce])
    if args.replicate_live:
        # console.log RUN-10: live replication path.
        print("[run:dispatcher] main: live replication %s." % args.replicate_live)
        return run_script(repo_root, "phase4_replicate_live.py", ["--config", args.config, "--run-id", args.replicate_live])
    raise SystemExit("specify --check-gate g4, --reproduce <id> or --replicate-live <id> (Phase 4 scope)")


if __name__ == "__main__":
    # console.log RUN-08: dispatcher invoked as main.
    print("[run:dispatcher] __main__: invoking main.")
    raise SystemExit(main())
