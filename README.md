> ICLR reviewers: start with FOR_REVIEWERS.md.

# PC-TAU — Multi-Route Perceptive Closure Benchmark for Tool-Using Agents

PC-TAU contains: (i) a deterministic exact constructed benchmark for resource-freeze geometry over pinned tau-family customer-service tasks, and (ii) a separately preregistered completed provider-backed LLM1 follow-on for descriptive fallback realizability. Unresolved authorization states expose multiple legal repair routes; exact E/R/A resource freezes change the repair geometry.

- Upstream: `sierra-research/tau2-bench` pinned at `672227c6b6676edc20d57ea53b7000262aae77b9` (cloned under `external_source/_upstream/`, git-ignored; identity sealed in `external_source/source_manifest.json`).
- Sealed parent run: `pctau-20260906-672227c`. Gates: PREREGISTERED → CONTRACT_SEALED → MEASURED → SEALED (reasons []).
- Sealed LLM1 follow-on: `pctau-20260906-672227c-llm1` (status `LLM1_SEALED`). Supporting/descriptive evidence only; not a parent phase.
- Plan: `WorkPlan.md` (4 firewall-separated phases plus 14 documented review fixes). Ledger: `Path.md` (append-only per-phase entries).

## Result (sealed)

- Track N (135 primary IDENTIFIED tasks, airline + retail): 135/135 FINITE_POSITIVE, `K=[1,1,2,1,INF,1,INF,INF]`, `delta_R=1`. Freezing R moves cost 1 → 2 without destroying closure.
- Track F (32 controlled, balanced by design): ZERO 8, FINITE 8, STRUCTURAL 16.
- Parent probes (deterministic scripted stand-ins, 5,436 paired episodes; NOT learned-model evidence): family-a governance 1.0 regret 0.0; family-b 0.75 with excess escalation under R-freezes; family-c 0.75 regret 0.333. Unsafe attempts: 0.
- Sealed parent claims (3): finite substitution in constructed contracts; controlled-regime reproduction; typing invariance under the frozen refactoring class.
- LLM1 (separate 5,436 provider-backed scheduled cells; descriptive fallback realizability only): actual trained models evaluated via live inference with paired F000/F010 contrasts; finite-fallback discovery with imperfect adaptation observed; cross-model replication with heterogeneity; 262 blocked open-state attempts, zero executed. Does NOT prove a causal freeze effect, prevalence, universal safety, or architecture superiority. `llm1/reports/LLM1_CLAIMS.md` preserves the sealed experiment's historical predicate terminology; the manuscript reads it narrowly as descriptive fallback realizability because F000 and F010 resolve on different subsets. See `llm1/reports/LLM1_CLAIMS.md`.
- Disabled: native multi-route realization, mechanism generality, natural PARTIAL ambiguity, all parent learned-agent claims (LM-C deviation recorded), and all prevalence/superiority/safety claims in both legs. See `results/pctau-20260906-672227c/audit_prephase4/POST_MEASUREMENT_AUDIT.md`.
- Audit: parent 5/5 independent layers equal, planner agreement 100% on 1,080 cells, 8/8 corruption families fail closed, bundle-verified replay byte-identical. LLM1 deterministic replay from archived raws recomputes downstream metrics byte-identically (see `llm1/REPRODUCE.md`).

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
llm1/               separately preregistered provider-backed follow-on (sealed run, archived raws, metrics, audit, reports)
releases/           pointer JSON (tracked) + sealed .tar.zst bundle (release asset, git-ignored)
```

## Reproduction

Requires Python >=3.12 with `pyyaml`, `jsonschema`, `pandas`, `pyarrow`, `pytest`, `zstandard`.

```bash
python scripts/run_pc_tau.py --reproduce pctau-20260906-672227c   # sealed-output replay / reseal verification, not a full Phase 1-3 rerun
python scripts/run_pc_tau.py --replicate-live pctau-20260906-672227c  # replication record helper only; zero provider calls, no seal matching
pytest -q                              # expected anonymous-snapshot baseline: 66 passed, 4 environment-only failures (see ANONYMIZATION_REPORT.json)
python scripts/run_pc_tau.py --check-gate g4 --config configs/experiment.yaml  # re-verify the seal gate
```

For LLM1 archived-raw deterministic replay versus fresh-provider replication (never byte-identical), see `llm1/REPRODUCE.md`. Ordinary review requires no API keys or provider access.

The bundle (`releases/pc-tau-pctau-20260906-672227c-sealed.tar.zst`, SHA-256 in `releases/pctau-20260906-672227c.json`) plus the sealed commit contain every input needed; upstream re-clones via URL + SHA in `external_source/source_manifest.json`.

## Status

Complete and sealed (parent `SEALED` + LLM1 `LLM1_SEALED`). No open phases. PC-TAU = controlled geometry; LLM1 = learned fallback realizability (descriptive only).
