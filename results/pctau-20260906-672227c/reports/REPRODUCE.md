# Reproduction

Exact replay (byte-identical seal):
  python scripts/run_pc_tau.py --reproduce pctau-20260906-672227c
The command retrieves pc-tau-pctau-20260906-672227c-sealed.tar.zst, verifies SHA-256 e0d52191fe6d170c,
extracts to a temporary directory and recomputes downstream tables plus the seal.

Live model rerun (new run, no seal match required):
  python scripts/run_pc_tau.py --replicate-live pctau-20260906-672227c
Reinvokes the pinned model configuration into a new run id with schema checks
and behavioral statistics in reports/replication_comparison.json.
