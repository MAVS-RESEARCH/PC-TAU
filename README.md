# PC-TAU — Multi-Route Perceptive Closure Benchmark for Tool-Using Agents

Compact, decisive learned-agent benchmark over pinned tau-family customer-service tasks. Unresolved authorization states expose multiple legal repair routes; exact E/R/A resource freezes change the repair geometry; agents must adapt without seeing resource labels.

- Upstream: `sierra-research/tau2-bench` pinned at `672227c6b6676edc20d57ea53b7000262aae77b9` (cloned under `external_source/_upstream/`, git-ignored; identity sealed in `external_source/source_manifest.json`).
- Sealed run: `pctau-20260906-672227c`. Gates: PREREGISTERED → CONTRACT_SEALED → MEASURED → SEALED (reasons []).
- Plan: `WorkPlan.md` (4 firewall-separated phases plus 14 documented review fixes). Ledger: `Path.md` (append-only per-phase entries).

## Result (sealed)

- Track N (135 primary IDENTIFIED tasks, airline + retail): 135/135 FINITE_POSITIVE, `K=[1,1,2,1,INF,1,INF,INF]`, `delta_R=1`. Freezing R moves cost 1 → 2 without destroying closure.
- Track F (32 controlled, balanced by design): ZERO 8, FINITE 8, STRUCTURAL 16.
- Probes (deterministic stand-ins, 5,436 paired episodes): family-a governance 1.0 regret 0.0; family-b 0.75 with excess escalation under R-freezes; family-c 0.75 regret 0.333. Unsafe attempts: 0.
- Sealed claims (3): finite substitution in constructed contracts; controlled-regime reproduction; typing invariance under the frozen refactoring class.
- Disabled: native multi-route realization, mechanism generality, natural PARTIAL ambiguity, all learned-agent claims (LM-C deviation recorded; follow-on `pctau-20260906-672227c-llm1` reserved), all prevalence/superiority/safety claims. See `results/pctau-20260906-672227c/audit_prephase4/POST_MEASUREMENT_AUDIT.md`.
- Audit: 5/5 independent layers equal, planner agreement 100% on 1,080 cells, 8/8 corruption families fail closed, bundle-verified replay byte-identical.

## Layout

```text
configs/            experiment, costs, models, freezes (single canonical), claims (all-false init)
preregistration/    eligibility rule, model/user protocols, nonclaims
schemas/            JSON schemas for tasks, facts, contracts, repairs, touch, results, ledger, audit
src/pc_tau/         source, reachability, semantics, repairs, touch, planner, freeze, runtime, metrics, claims
src/pc_tau_audit/   independent rebuild package (import-bounded, reachability excepted)
scripts/            phase1_*, phase2_*, phase3_*, phase4_*, run_audit.py, run_pc_tau.py dispatcher
tests/              unit, phase1-4, metamorphic, audit
external_source/    manifest + census (upstream clone ignored)
results/<run_id>/   pilot, contract, exact, agents, controls, audit, reports, markers, phase_manifest.json
releases/           pointer JSON (tracked) + sealed .tar.zst bundle (release asset, git-ignored)
```

## Reproduction

Requires Python >=3.12 with `pyyaml`, `jsonschema`, `pandas`, `pyarrow`, `pytest`, `zstandard`.

```bash
python scripts/run_pc_tau.py --reproduce pctau-20260906-672227c   # bundle-verified exact replay, byte-identical seal
python scripts/run_pc_tau.py --replicate-live pctau-20260906-672227c  # new-run replication record, no seal matching
pytest -q                              # full suite, 49 passed at seal
python scripts/run_pc_tau.py --check-gate g4 --config configs/experiment.yaml  # re-verify the seal gate
```

The bundle (`releases/pc-tau-pctau-20260906-672227c-sealed.tar.zst`, SHA-256 in `releases/pctau-20260906-672227c.json`) plus the sealed commit contain every input needed; upstream re-clones via URL + SHA in `external_source/source_manifest.json`.

## Status

Complete and sealed. No open phases. Outstanding: the reserved real-model follow-on (same contracts/population/freezes/bundles/metrics + actual inference), which alone can unlock the disabled learned-agent predicates.
