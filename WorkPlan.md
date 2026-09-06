# WorkPlan.md — PC-TAU Multi-Route Perceptive Closure Benchmark for Tool-Using Agents

**Spec:** Implementation Specification v0.1 (15 pages, §§1–6.3).
**Repo:** https://github.com/MAVS-RESEARCH/PC-TAU (clone verified 2026-09-06; only `LICENSE` present).
**Upstream source target:** https://github.com/sierra-research/tau2-bench (existence verified 2026-09-06; domains `mock/airline/retail/telecom/banking_knowledge`, text half-duplex + voice full-duplex).
**Status:** Planning patched 2026-09-06 with 10 review fixes (Fix 1–10, see Appendix B); no scientific results exist yet. Frozen for implementation: implement exactly this; stop on failed gates; do not improvise scientific semantics.
**Companion ledger:** `Path.md` (append-only; every phase records files, commands, hashes, run IDs, tests, deviations, WorkPlan-follows yes/no).

## 0. Global decisions (read before any phase)

### 0.1 Mission (spec cover + §1)

Build a compact but decisive learned-agent benchmark in which unresolved authorization states expose **multiple natural repair routes**, exact **E/R/A resource freezes** change the repair geometry, and learned agents must adapt **without being shown the resource labels**.

Single experiment question: when a learned tool-using agent proposes an effect that is not yet authorized, and the same unresolved state exposes multiple legal repairs, which governed resource must remain mutable for authorization closure?

Primary estimand: for each sealed task, exact resource-freezing signature `K_Pi = (kappa_Pi^{-S})` over all `S ⊆ {E,R,A}`. **Environment determines closure; model behavior never defines the signature.**

Benchmark architecture (spec §1.1, 6-step loop):

```text
1 User/task → 2 Learned agent → 3 Governance gate → 4 Legal repair set → 5 Recompute certificate → 6 Effect or escalate
```

If proposed effect is already closed it executes. If authorization is open, agent may only invoke legal repairs. After every repair the evaluator recomputes the certificate. No effect executes while open.

Polaris relationship: complement, not modify. Polaris remains the sealed, externally engineered, highly audited **single-route existence case**. PC-TAU supplies the missing **multi-route learned-agent realization**. Never mutate any sealed Polaris run; Polaris pipeline is only an engineering-pattern donor (source locks, exact planners, independent audit, corruption testing, claim ledgers, sealing).

### 0.2 Why exactly 4 phases (4–6 allowed; 4 chosen)

The user authorized 4–6 phases, freely scaled to complexity, and excused 5–6 if workload is small. The workload here is **large**, but the spec already partitions all scientific work into **4 firewall-separated phases** (§3: PREREGISTERED → CONTRACT_SEALED/PARTIAL/STOP → MEASURED → SEALED/INVALID). Adding a 5th/6th phase would split an atomic gate (e.g. separating audit from seal, or pilot from preregistration) and create a silent-rewrite risk across the firewall.

Decision: **4 phases, 1:1 with spec §§Phase 1–4.** Scaffolding (repo layout, configs skeleton, schemas, test harness, one-command runner, cleaner) is done **inside Phase 1**, not as a separate phase, so no scientific gate is diluted. Phase count is therefore minimal *and* complete.

Phase firewall (spec §3, red box): selection rules, semantic boundaries, costs, route eligibility, model roster, metrics, nonclaims must be frozen **before** downstream results exist. A later phase may **invalidate** an earlier assumption but may **never silently rewrite** it. Every cross-phase change requires a failure card + Path.md deviation entry + re-gate.

### 0.3 Model-training and anti-overfitting policy (user requirement → spec mapping)

The user requires: for every model to be trained, give specifics + resultant benchmarks, and brutally test each model on benchmarks **ENTIRELY different** from training benchmarks plus other anti-overfitting actions.

**Spec fact: PC-TAU trains zero models.** The three heterogeneous model families (§2.1, §P1.4, §P3.3) are **evaluation-only robustness probes, not a leaderboard and not training targets**. There is no gradient update, no fine-tuning, no prompt-tuning on K_Pi. Exact `K_Pi` is computed by the environment solver before any model trajectory is examined.

What replaces "training benchmarks" and how overfitting/tuning is still brutally prevented:

1. **Result-independent eligibility (anti-cherry-picking).** Natural-track inclusion (§P1.3, §P2.5) may inspect only source-grounded structure (consequential effect, open certificate, ≥2 legal repairs with Fix-3 viable-route multiplicity, ≥2 touch-distinct profiles, finite exact graph, verified provenance, non-pilot). It is **forbidden** to inspect `Delta_R`, `K_Pi`, or model success. Violation = hard STOP (§5.1).
2. **Pilot is throwaway (Fix 1).** Exactly 24 tasks (12 airline + 12 retail), IDs permanently excluded from final population (§P1.1). Pilot MAY compute provisional pilot-only closures/freezes to prove finite substitution; these live in `results/<run_id>/pilot/` only, never enter paper results, and inform interface design only. This is the "training set" that is **never tested on**.
3. **Frozen semantic user bundles.** Generated/sealed before the sealed run; paraphrase may vary under fixed seed but facts/willingness/authorization content are invariant across matched freezes (§P1.4, §P3.4). Prevents simulator drift tuning.
4. **Paired repeats.** 3 paired repeats per task/model/primary-freeze; same initial DB, goal, bundle/seed, model config, admitted facts — only freeze mask changes (§P3.3). Repeats quantify instability, not population size (§P3.6).
5. **ENTIRELY different test benchmarks:**
   - Exact 8-cell lattice (F000–F111) is ground truth; model-facing runs use only 4 primary cells (F000, F100, F010, F001). Models never see the full lattice during evaluation.
   - Controlled Track F (32 tasks, 8 per regime, balanced **by design**) is a **separate mechanistic benchmark**; never used to estimate natural frequency (§2, §P2.6). Natural Track N (60–96 target, min 40) is the only prevalence-relevant population, and even there **no prevalence predicate is authorized**.
   - 8 deliberate corruption families (§P4.2) + frozen-class semantic-refactoring audit (§P4.3/Fix 4) act as adversarial benchmarks: any tuning that breaks invariance, leaks truth into ω, or splits atomic actions must fail closed.
   - Sole independent audit planner (§P4.1/Fix 7) recomputes every F000–F111 value from serialized frozen evidence without importing production modules. 100% agreement required for SEAL.
6. **No successful-run filtering.** Every null, zero, infinite, failure, escalation, underidentified case is retained in tables (§4.3, §P3 outputs). Bootstrap CIs are over tasks, never over seeds as independent tasks; `K_Pi` gets no CIs because it is exact (§P3.6).
7. **Claim locks (Fix 10).** Structured predicate ledger (`claim_ledger.json` with `*_authorized: true/false`); `CLAIMS.md` generated only from authorized predicates; 5 permanent nonclaim predicates stay false (`src/pc_tau/claims.py` + `src/pc_tau_audit/claims_audit.py`). Paraphrase cannot bypass because locks are predicate-level, not keyword-level.

If a future contributor proposes actual training (e.g. distilling a repair policy), it must be preregistered as a new Track with a disjoint task split, disjoint seeds, and the same 8-family corruption + independent-planner gate before any claim. No such training is in scope for v0.1.

### 0.4 Scale contract (spec §2.1)

| Stage | Target | Role |
|---|---|---|
| Pilot | 24 throwaway (12 airline, 12 retail; GO needs ≥2 viable-route tasks per domain + ≥1 provisional finite fallback) | Feasibility + multi-domain viability evidence only; never paper results |
| Natural final (Track N) | Target 60–96 viable-route MULTI_ACTION; **minimum 40 across ≥2 domains** | Primary exact + learned-agent evidence |
| Controlled panel (Track F) | 32 tasks: 8 R-zero, 8 R-finite, 8 R-structural, 8 E/R-complementary | Exact regime coverage; learned-agent subset may be prespecified balanced 16 if cost-constrained; never natural incidence |
| Agent episodes | 3 families × 3 repeats × 4 primary freezes | 2,160 episodes at 60 natural tasks; exact solver still runs all 8 freezes |

Telecom is a **preregistered fallback only (Fix 8)**: activates exactly once iff `N<40 OR #eligible_domains<2` under the same source-only census (covers the airline-45/retail-0 trap); if still `N<40 OR domains<2`, STOP rather than weaken eligibility (§P1.3).

### 0.5 Regimes, baselines, nondegeneracy (spec §§1.2–1.3, 2.2–2.3)

E/R/A operational meaning + hard firewalls (Fix-5 formal types: `U_H` universe; `H:U_H→ℋ` admitted-evidence map; `P_R⊆U_H×U_H` representation equivalence; `Λ` authority set; `ω` observation channel; `Cert` closure predicate):

- **E (admitted evidence):** facts crossing sealed admission boundary (user answers, read-only tool outputs, identity, reservation/order facts, confirmations, provenance). E-only repair may acquire a new admitted fact but **may not** alter certificate mapping or authority.
- **R (certificate representation):** which distinctions among already-admitted histories are decision-bearing (`P_R` equivalence). R-only repair computes **only** from already-admitted H; may not query user/external DB/unavailable value.
- **A (epistemic authority):** which sources/attestations/approvals/predicates/interfaces are admissible (`Λ`). A-only repair changes authority **without** adding a world fact or changing P_R.

`Touch(q)` is **derived, never authored**: E iff H changes across a positive-support successor; R iff `P_R` equivalence changes; A iff Λ changes. Mixed touch frozen atomically unless source exposes a decomposition.

Nondegeneracy gate (before any final freeze value; Fix 3 strengthened): viable-route MULTI_ACTION (≥2 distinct first repairs **each on some unrestricted finite closure path** from the same open state) + touch diversity (≥2 distinct derived profiles) + open initial certificate + source/provenance sufficiency + verification (Fix 2) + exact tractability. Desired geometry: finite substitution (e.g. kappa=1, kappa^{-R}=2 or 3); structural finite-to-infinite retained but benchmark must not depend on delete-the-sole-closer. A legal-but-never-closing second button does not satisfy MULTI_ACTION.

Regimes: R-zero (`Delta_R=0`), R-finite (`0<Delta_R<∞`), R-structural (kappa finite, kappa^{-R}=∞), E/R-complementary (neither E-only nor R-only closes, governed composition does). A-mediated retained when natural; never forced.

Baselines: reject-on-open, evidence-only resolver, untyped generic repair, PC exact oracle (reference for regret, not an agent baseline).

### 0.6 Repository layout to be built (spec §4) — simplified run-scoped artifacts (Fix 9)

```text
PC-TAU/
  configs/experiment.yaml  costs.yaml  models.yaml  freezes.yaml  claims.yaml
  schemas/task.schema.json  semantic_fact.schema.json  contract.schema.json  repair.schema.json
          touch.schema.json  freeze_result.schema.json  agent_run.schema.json  audit.schema.json
          extraction.schema.json  refactoring.schema.json  claim_ledger.schema.json
  src/pc_tau/source.py  semantics.py  repairs.py  touch.py  planner.py  freeze.py  runtime.py  metrics.py  claims.py
  src/pc_tau_audit/source_audit.py  contract_audit.py  touch_audit.py  planner_audit.py  run_audit.py  claims_audit.py
  scripts/phase1_*.py  phase2_*.py  phase3_*.py  phase4_*.py  run_pc_tau.py
  tests/unit/  phase1/  phase2/  phase3/  phase4/  metamorphic/
  external_source/source_manifest.json  task_census.json  pilot/   # immutable source material (outside runs)
  preregistration/eligibility_rule.json  model_protocol.json  user_response_protocol.json  nonclaims.json
  results/<run_id>/
    pilot/                    # Phase 1 provisional pilot-only geometry (throwaway, never scientific)
    contract/                 # Phase 2 sealed contracts + extraction + refactoring-class freeze
    exact/ agents/ controls/  # Phase 3 exact + learned-agent evidence
    audit/ reports/           # Phase 4 independent rebuild + paper artifacts
    phase_manifest.json       # per-file sha256 for every scientific artifact in this run (no .sha256 sidecars)
    PHASE3_COMPLETE  CONTRACT_SEALED  SEALED (or INVALID)
  reports/artifact_graph.json -> results/<run_id>/reports/artifact_graph.json (canonical copy; no duplication)
  WorkPlan.md  Path.md
```

Artifact simplification rule (Fix 9): all scientific artifacts are run-scoped under `results/<run_id>/`. Only immutable source/preregistration/config/schema/src/script/test material lives outside. There are no per-file `.sha256` sidecars; `phase_manifest.json` (all hashes + producers) and final `reports/artifact_graph.json` are the sole hash indexes. Canonical freeze file is exactly one name: `configs/freezes.yaml` (F000–F111). The spec-layout name `freeze_lattice.yaml` is **not** created (no symlink/copy; Windows-safe); `phase_manifest.json` records `canonical_freeze_file: configs/freezes.yaml` to resolve the spec naming divergence. G1 fails if a second freeze file appears.

Runtime discipline (§4.3): one named run dir `results/<run_id>/` per sealed attempt, created at Phase 1 start; safe cleaner `scripts/clean_run.py --run-id <unsealed>` removes only that explicitly named unsealed run and refuses sealed IDs; hash every paper-influencing artifact into `phase_manifest.json` / `artifact_graph.json` (sha256, no sidecars); canonical JSON (sort_keys, separators, utf-8); timestamps in logs only, never in scientific hashes; exact solver CPU-only, no GPU; model identity + generation params frozen and hashed. Reproduction is split (Fix 6): `run_pc_tau.py --reproduce <run-id>` = exact artifact replay from archived raw trajectories (byte-identical tables + seal); `run_pc_tau.py --replicate-live <run-id>` = new live model rerun (same IDs/config, new run-id, schema-checked, statistics compared, seal NOT required to match).

Logging discipline (§4.2): Path.md append-only; every phase records files, commands, hashes, run IDs, tests, deviations, rejected attempts, WorkPlan-follows yes/no; planning/pilot/sealed/paper-transformations visibly distinct.

Tech: Python `>=3.12,<3.14` (matches tau2-bench), `uv` sync, deps `pyyaml`, `jsonschema`, `pyarrow`+`pandas` (parquet), `pytest`. No torch/GPU for exact path. Model calls via LiteLLM-compatible APIs or local inference, exact IDs + revisions hashed into `configs/models.yaml` before Phase 3.

### 0.7 Traceability (how "nothing omitted" is verified)

Each phase section below ends with `Covers spec:` + explicit section list. After Phase 4, §5 (gates/stops/done) and §6 (D32/external refs) are mapped. Verification commands: `pytest`, `python scripts/run_pc_tau.py --check-gate g1|g2|g3|g4`, `python scripts/phase4_verify_claims.py`, exact-replay `python scripts/run_pc_tau.py --reproduce <id>`, live-rerun `python scripts/run_pc_tau.py --replicate-live <id>`, clean-checkout reproduce. Any spec row without a file+test+gate entry fails review. Review-fix verification: `grep -n "Fix [0-9]" WorkPlan.md` must hit all 10 fixes; `grep -n "freeze_lattice.yaml" WorkPlan.md` must hit only the Fix-9 canonical-file note (no creation).

Stale-results rule (user requirement): clone contained **zero** result artifacts (verified: only LICENSE). `results/` starts empty and git-ignored except via `phase_manifest.json` + seal markers (`CONTRACT_SEALED`, `PHASE3_COMPLETE`, `SEALED`). Safe cleaner `scripts/clean_run.py --run-id <unsealed>` is the only deleter; it refuses sealed IDs. After each phase, only new artifacts from that phase exist under the same `results/<run_id>/`; Path.md logs the cleaner invocations (including no-ops).

Commit/push rule (user requirement): after **each** phase gate passes, commit with message `phase<N>: <gate> <run-id> <short-hash>` and push to `origin/main` without being asked. Planning commit (`docs: WorkPlan.md + Path.md setup`) is pushed immediately after verification.

---

## Phase 1 — Source Lock, Pilot, and Preregistration (spec §Phase 1, P1.1–P1.4)

**Exit:** `PREREGISTERED` or `STOP`. **Firewall (Fix 1):** no final task inclusion from freeze outcomes; **no final-population `K_Pi` before G2**; pilot disposable. **Explicit exception:** Phase 1 MAY compute **provisional pilot-only closure/freeze geometry** (e.g. checking `kappa=1, kappa^{-R}=2`) on **permanently excluded pilot tasks only**, using a provisional solver. These results are exploratory, live only in `results/<run_id>/pilot/`, are never used as scientific results, never enter Track N/F, and may affect **interface design only** (governance-gate shape, repair-enumeration plumbing). Any final-population freeze value existing before G2 fails G1.

### 1.1 Scope

Pin the upstream tau-family source immutably; run a 24-task throwaway pilot to prove MULTI_ACTION + finite-substitution feasibility on ordinary CPU with a defensible E/R/A operational firewall; preregister a result-independent final-task rule + fallback rule; seal cost/model/user/claim configs for all four phases. Nothing in this phase may compute a **final-population** K_Pi or run a learned-agent evaluation. Provisional pilot-only freezes/closures are allowed **only** under the Fix-1 exception above (excluded IDs, `results/<run_id>/pilot/` confinement, design-only use).

### 1.2 Files to be made (exact)

```text
external_source/source_manifest.json      # URL, commit SHA, source-tree hash, dep lock, env identity, license
external_source/task_census.json          # airline+retail (+telecom only if fallback triggers) task inventory
results/<run_id>/pilot/pilot_ids.json     # 12 airline + 12 retail pilot IDs + selection rule (excluded forever)
results/<run_id>/pilot/provisional_geometry.jsonl  # FIX-1 pilot-only closures/freezes (exploratory, never scientific)
results/<run_id>/pilot/gate_log.json      # provisional gate enumeration + CPU/timeout evidence
results/<run_id>/reports/phase1_preregistration.json  # gate evidence: pilot yield, source/config hashes, PREREGISTERED/STOP
results/<run_id>/phase_manifest.json      # hashes for all Phase-1 outputs (no sidecars)
configs/experiment.yaml                   # domains, splits, run-id scheme, determinism, phase gates
configs/costs.yaml                        # unit-intervention primary; optional native-cost only if source-defensible pre-results
configs/models.yaml                       # 3 heterogeneous families, exact IDs + API revisions + gen params + sha256
configs/freezes.yaml                      # FIX-9 single canonical 8-cell lattice F000–F111; primary F000,F100,F010,F001 flagged
configs/claims.yaml                       # FIX-10 authorized-predicate defaults (all nonclaim predicates false)
preregistration/eligibility_rule.json     # machine-readable required/forbidden/fallback rule incl. FIX-3 viable-route + FIX-8 fallback trigger
preregistration/model_protocol.json       # roster, repeats=3, pairing keys, tool-naming (no E/R/A labels), safety gate
preregistration/user_response_protocol.json # bundle freeze + seed-controlled paraphrase, invariance clause
preregistration/nonclaims.json            # 5 nonclaims verbatim + FIX-10 predicate mapping
schemas/task.schema.json                  # validates task_census + pilot records
```

### 1.3 Code to be produced and how to code it

- `src/pc_tau/source.py` — `pin_source(url, rev)`: clone tau2-bench at pinned commit into `external_source/_upstream/` (git-ignored except manifest), record `commit_sha`, `tree_hash = sha256(sorted file hashes)`, `dep_lock (uv.lock hash + python version)`, `env_identity (os, cpu, python -V)`, `license + attribution`. `census(domain)`: enumerate tasks via upstream `data/` + `src/tau2/domains/` loaders without importing agent logic; emit `task_id, domain, policy_locator, tool_surface, db_schema, user_schema, eval_criteria`. `select_pilot()`: deterministic sample (seed in experiment.yaml) of exactly 12+12 from dev-only split or explicit pilot IDs; write exclusion list used by all later phases. How: stdlib + pyyaml + hashlib; no LLM calls; no E/R/A strings in this module (enforced by unit test grepping for `Touch`/`kappa`).
- `scripts/phase1_pin_source.py`, `scripts/phase1_census.py`, `scripts/phase1_pilot.py`, `scripts/phase1_preregister.py`, `scripts/run_pc_tau.py` (dispatcher + `--check-gate g1`), `scripts/clean_run.py` (safe cleaner).
- Pilot gate logic (in `phase1_pilot.py`, Fix 1 + Fix 3 + Fix 8): provisional governance gate instruments open-state enumeration using only source policy/task-state/API semantics/user channels; rejects any repair justified by PC labels/desired Delta_R/observed **final** freeze. It MAY run a **provisional exact closure/freezing solver on pilot graphs only** to check finite substitution (e.g. `kappa=1, kappa^{-R}=2`); outputs confined to `results/<run_id>/pilot/provisional_geometry.jsonl`, tagged `provisional:true, excluded:true`, never read by Phase 2+ code (import-guard + audit re-check). Checks (a) ≥8/24 pilot tasks with defensible MULTI_ACTION under the **strengthened viable-route rule** (Fix 3: ≥2 distinct first repairs each on some unrestricted finite closure path — pilot version computed provisionally) with **multi-domain evidence: ≥2 such tasks in EACH of airline and retail** (Fix 8; replaces "≥1 domain viable"), (b) ≥1 pilot task with legitimate provisional finite fallback when one resource class is unavailable, (c) E/R/A actions validatable by operational constraints (unit test: an R-action that reads external state is rejected), (d) exhaustive solvability on CPU (timeout guard, node budget). GO/STOP table from spec pp.4–5 implemented as `gate()` returning `PREREGISTERED` or `STOP` with reasons; pilot GO does not imply any final-population claim.
- Configs: `costs.yaml` sets `primary: unit_intervention_cost: 1` per repair step; `secondary_native` left `null` unless source cost semantics found pre-results (with locator). `models.yaml` fixes 3 families (e.g. `family-a: gpt-4.1-YYYYMMDD`, `family-b: claude-*-YYYYMMDD`, `family-c: llama-*-local-Q8`) — exact IDs chosen at implementation time, then hashed; `repeats: 3`, `primary_freezes: [F000,F100,F010,F001]`. `freezes.yaml` (single canonical file, Fix 9) enumerates all 8 masks as `{E:bool,R:bool,A:bool}` with canonical names F000–F111. `eligibility_rule.json` encodes Fix-3 viable-route predicate + Fix-8 fallback trigger `activate_telecom_iff (N<40 OR eligible_domains<2)` (Fix 8; replaces "<40 only"), single activation, same source-only census, else STOP.
- Tests `tests/phase1/`: `test_source_pin_hash.py` (re-hash equals manifest), `test_pilot_exclusion.py` (pilot IDs never in final candidate query + Phase 2+ never reads `pilot/provisional_geometry.jsonl`), `test_eligibility_no_freeze_ref.py` (static AST grep: eligibility module never imports freeze/planner/metrics; pilot provisional solver is a separately namespaced `pilot_provisional_*` module never imported by `repairs/semantics/freeze/planner`), `test_provisional_gate_rejects_pc_justification.py`, `test_pilot_multidomain.py` (≥2 viable-route tasks per domain required for GO), `test_single_freeze_file.py` (no `freeze_lattice.yaml` present), `test_manifest_hashes.py` (every Phase-1 output in `phase_manifest.json`). Plus `tests/unit/test_canonical_json.py`.

How to code (style): small pure functions, deterministic (`PYTHONHASHSEED`, sorted keys), type hints, no framework bloat; every writer emits canonical JSON and appends its sha256 to `results/<run_id>/phase_manifest.json` (Fix 9: no sidecars).

### 1.4 Benchmarks / models / anti-overfitting for this phase

No training; no model evaluation. The "benchmark" is the pilot go/no-go gate itself. Brutal-difference property: pilot tasks are **never** reused as test tasks (exclusion list enforced in code + audit re-check; provisional geometry never imported downstream). Eligibility rule is sealed **before** any final K_Pi exists, so tuning to Delta_R is structurally impossible (verified by import-grep test + git log ordering: preregistration commit precedes any final freeze-result commit). Fix-1 clarification: pilot-only provisional freezes are the **only** K-like values allowed before G2, and they are design-only.

### 1.5 Exit gate G1

`PREREGISTERED` iff: pilot passes (≥8/24 viable-route MULTI_ACTION with ≥2 per domain, ≥1 provisional finite substitution, firewall + CPU ok), source immutable (re-hash match), final eligibility result-independent (Fix-3 predicate + Fix-8 trigger sealed), fallback sealed, all 4-phase configs sealed, single freeze file, manifest complete, and **zero final-population K_Pi / model trajectories exist** (filesystem scan in `phase1_preregister.py --check-gate g1` allows only `results/<run_id>/pilot/provisional_*`). Else `STOP` with reasons in `results/<run_id>/reports/phase1_preregistration.json`. Log everything to Path.md §P1.

**Covers spec:** §2 (source foundation/tracks), §P1.1–P1.4, §5.2 G1, §6.2 (tau2-bench URL), §6.3 lines 1–2 ("do not scale first; prove pilot"), §4 layout (configs/external_source/preregistration/run-scoped reports), §4.1 `source.py`, §4.3 cleaner discipline. Review fixes in this phase: Fix 1 (pilot-provisional), Fix 3 (viable-route pilot), Fix 8 (multidomain pilot + `N<40 OR domains<2` trigger), Fix 9 (run-scoped + single `freezes.yaml` + manifest), Fix 10 (predicate defaults).

---

## Phase 2 — Semantic Contract and Multi-Route Extraction (spec §Phase 2, P2.1–P2.6)

**Exit:** `CONTRACT_SEALED` / `PARTIAL` / `STOP`. **Firewall:** no freeze values, no learned-agent evaluation; touch derived from source-grounded semantics only. Pilot provisional geometry from Phase 1 is invisible here (import ban).

### 2.1 Scope

For every final-candidate task, execute **source extraction → independent verification → contract compilation** (Fix 2 frozen protocol): extract source facts with locators/fragment-hashes/rules/confidence, independently verify (second extractor/verifier; disagreement → PARTIAL, never post-result manual resolution), then compile the formal contract `U_H, H:U_H→ℋ, P_R⊆U_H×U_H, Λ, ω` (Fix 5) with admission/representation/authority boundaries + no self-signaling. Support contract families (IDENTIFIED/PARTIAL/INVALID), mechanically derive touch with validation, apply strengthened result-blind viable-route multi-route eligibility (Fix 3), freeze the semantic-refactoring/boundary-policy class for Phase 4 (Fix 4), then build the separate 32-task controlled factorial panel after freezing the transformation family. All outputs run-scoped under `results/<run_id>/contract/` (Fix 9).

### 2.2 Files to be made (exact)

```text
results/<run_id>/contract/semantic_facts.jsonl      # Pass A records + locator + quoted-fragment hash + rule + confidence (Fix 2)
results/<run_id>/contract/extraction_records.jsonl  # Fix-2 per-fact verification: second-extraction/verifier verdict, disagreements
results/<run_id>/contract/extraction_protocol.json  # Fix-2 frozen protocol: rules, prompt (if LLM used, prompt-frozen, source-only), verifiers
results/<run_id>/contract/task_contracts.jsonl      # Pass B: U_H,H,P_R,Lambda,omega,Q,Succ+,Terminal,A_Pi,costs,atomicity,provenance (Fix-5 math)
results/<run_id>/contract/contract_families.jsonl   # C(Omega) family per task + status IDENTIFIED|PARTIAL|INVALID + disagreement refs
results/<run_id>/contract/repair_actions.jsonl      # legal repairs with preconditions + successor semantics + source justification
results/<run_id>/contract/touch_records.parquet     # derived Touch(q) per positive-support successor (H/P_R/Lambda diffs)
results/<run_id>/contract/route_classification.parquet # |Q_legal|, distinct touches, viable-route flags, open/closed, exact-solvable
results/<run_id>/contract/natural_population.json   # sealed Track N IDs (≥40, ≥2 domains, no pilots) + contract hashes
results/<run_id>/contract/controlled_panel.json     # Track F 32 IDs (8×4 regimes) + transformation-family hash, balanced-by-design
results/<run_id>/contract/semantic_boundary_policy.json  # Fix-4 sealed admission/representation/authority + family rules
results/<run_id>/contract/admissible_refactorings.json   # Fix-4 frozen refactoring class for Phase-4 audit (Phase 3 cannot touch)
results/<run_id>/contract/contract_family_rules.json    # Fix-4 competing-completion rules → PARTIAL vs IDENTIFIED logic
results/<run_id>/contract/failure_cards.jsonl       # INVALID + excluded candidates with reasons; missing card fails audit
results/<run_id>/contract/CONTRACT_SEALED           # marker with run-id + root hash (or PARTIAL/STOP marker)
results/<run_id>/phase_manifest.json                # extended with Phase-2 hashes (no sidecars)
schemas/semantic_fact.schema.json  # validates Pass A incl. locator/fragment-hash/rule/confidence (Fix 2)
schemas/extraction.schema.json     # validates extraction_records + protocol freeze (Fix 2)
schemas/refactoring.schema.json    # validates admissible_refactorings + boundary policy (Fix 4)
schemas/contract.schema.json       # validates U_H/H/P_R/Lambda/omega/Q/Succ+/Terminal/A_Pi with Fix-5 types
schemas/repair.schema.json         # validates repair_actions
schemas/touch.schema.json          # validates touch_records (no manual label field allowed)
```

### 2.3 Code to be produced and how to code it

- `src/pc_tau/semantics.py` — formal contract math (Fix 5, never shorthand-mutated): `U_H` = common history universe (all source-possible histories); `H: U_H → ℋ` = admitted-evidence map (which histories are admitted with provenance; moving an already-admitted fact between components creates no new E); `P_R ⊆ U_H×U_H` = representation equivalence (which distinctions among admitted histories are decision-bearing for certification; syntax/value renames preserving equivalence are not R — implement canonicalizer: sort + normalize equivalence-preserving renames); `Λ` = authority set (admissible sources/attestations/approvals/predicates/interfaces; field existence alone is not authority); `ω` = **controller-visible observation/information channel** (Fix 5: NOT the certificate predicate; evaluator-truth leakage is defined as truth reaching `ω` or model-visible tool responses); certificate/closure predicate = separate `Cert` (closed/open) recomputed by the evaluator. `extract_facts(task)` (Fix 2 frozen protocol `source extraction → independent verification → contract compilation`): for every semantic fact emit `locator (file:line + upstream SHA) + quoted/source-normalized fragment + fragment_hash + extraction_rule_id + confidence/status`; then `verify_facts` runs an independent second extraction or verifier (different code path/prompt; if an LLM extractor is used it is pre-freeze, prompt-frozen, source-only, blinded to all `K_Pi/Delta_R/model` outputs — prompt hash sealed in `extraction_protocol.json`); any disagreement → task marked PARTIAL (never manual post-result resolution). `compile_contract(verified_facts)`: build `U_H,H,P_R,Λ,ω,Cert,Q,Succ+,Terminal,A_Pi,costs,atomicity` with provenance. Forbidden: any import of freeze/planner/agent code + any read of `results/<run_id>/pilot/provisional_*` (enforced by test). Contract families: `family(task)` returns single contract or finite/symbolic `C(Omega)`; status logic per §P2.3; boundary alternatives governed by frozen `contract_family_rules.json` (Fix 4).
- `src/pc_tau/repairs.py` — `legal_repairs(contract)`: source-grounded extraction with per-repair `justification` (policy clause + tool semantic + user channel) and `successor` function; atomicity preserved (E+R stays atomic unless source exposes E-only subaction as separate tool path).
- `src/pc_tau/touch.py` — `derive_touch(pre, post)`: compare `H` (set diff on canonical fact ids) → E; compare canonical `P_R` equivalence (not raw syntax) → R; compare canonical `Lambda` → A; return union. **Reject paths:** manual `resource_label` field in inputs raises `ValueError`; R-only candidate that touches user/external DB or reads unadmitted value rejected; E-only that mutates P_R rejected; A-only that adds world fact rejected. Tested by `tests/phase2/test_touch_rejects.py` with 6+ adversarial cases from §P4.2 boundary family.
- `scripts/phase2_extract.py`, `phase2_verify.py` (Fix 2 independent verification), `phase2_compile.py`, `phase2_touch.py`, `phase2_eligibility.py`, `phase2_freeze_refactor_policy.py` (Fix 4: seals `semantic_boundary_policy.json + admissible_refactorings.json + contract_family_rules.json` with hashes before any freeze), `phase2_controlled_panel.py`, gate `run_pc_tau.py --check-gate g2`.
- Strengthened eligibility predicate (Fix 3, exact code, no Delta_R/K_Pi/model refs — checked before any freeze):
  `status==IDENTIFIED and initial_cert==OPEN and len(Q_legal)>=2 and len(set(Touch(q)))>=2 and viable_first_repairs>=2 and provenance_complete and verified (second-extraction agree or PARTIAL-split) and exact_solvable and id not in pilot_ids`, where `viable_first_repairs = |{q in Q_legal : exists finite unrestricted (F000) closure path starting with q}|` computed with the production planner under the zero-freeze mask only. This means multiple **viable repair routes**, not merely multiple available buttons; a legal-but-never-closing `q2` does not count. Hostile "degenerate button" attack is thereby blocked without inspecting any freeze outcome.
- Controlled panel: freeze `transform_family` (4 geometry templates: R-zero/finite/structural/E-R-complementary) with hash, then synthesize 8+8+8+8 from **non-pilot templates**; label `balanced_by_design: true`, `estimates_natural_frequency: false`.
- Tests `tests/phase2/`: provenance completeness (100% repairs have locators + fragment hashes + rule ids), extraction freeze (protocol + prompt hash sealed before compilation; extractor never imports freeze/metrics/agent outputs), second-extraction agreement (injected disagreement → PARTIAL, never forced label), no-manual-touch (schema rejects `label` field), R-firewall (external-read R rejected), E-firewall, A-firewall, atomicity (E+R not splittable), pilot-exclusion + pilot-provisional invisibility, family status agreement, `test_eligibility_blind.py` (AST + runtime assert: eligibility reads only F000-viability, never Delta_R/K_Pi/freeze outputs), `test_viable_routes.py` (single-closer + dead-button graph fails eligibility; two-viable-route graph passes), `test_refactor_policy_frozen.py` (3 Fix-4 files exist + hashed at G2; Phase-3 code never writes them), `test_omega_channel.py` (omega is observation channel; truth-in-omega fixture detected as leak; `P_R` is `U_H×U_H` equivalence, not "partition of H-object"), `test_single_freeze_file.py`, `test_manifest_hashes.py`.

### 2.4 Benchmarks / models / anti-overfitting for this phase

No training; no freeze planning; no population filtering on Delta_R (code-level import ban + audit re-check). PARTIAL tasks retained in sensitivity appendix, never forced to a preferred label — prevents boundary-tuning overfit. Fix-2 anti-manufacturing: every fact carries locator + fragment hash + rule + confidence + independent verifier verdict, so "authors manually manufactured repair semantics" is refuted by re-extraction. Controlled panel built **after** transformation family frozen, from non-pilot templates, so regime coverage cannot leak into natural selection. Touch is mechanically recomputed, never hand-typed. Fix-4: refactoring class frozen here, so Phase 4 cannot choose perturbations the classification survives.

### 2.5 Exit gate G2

`CONTRACT_SEALED` iff: 100% provenance + verification for retained repairs, zero manual touch, formal `U_H/H/P_R/Λ/ω/Cert` types valid, point-identified natural population ≥40 viable-route MULTI_ACTION across ≥2 domains (Fix 3), controlled panel separately flagged, Fix-4 refactoring class sealed + hashed, failure cards for every INVALID/excluded, contract identities immutable (manifest hashes), and filesystem scan proves zero final freeze results / model trajectories exist. Else `PARTIAL` (if disagreement remains but IDENTIFIED core ≥40) or `STOP`. Log to Path.md §P2.

**Covers spec:** §§1.2–1.3 (E/R/A, touch, nondegeneracy), §P2.1–P2.6, §5.2 G2, §4.1 `semantics.py`/`repairs.py`/`touch.py`, §6.3 lines 3 ("freeze rules; derive semantics"). Review fixes in this phase: Fix 2 (extraction→verification→compilation), Fix 3 (viable-route eligibility), Fix 4 (refactoring-class freeze), Fix 5 (`U_H/H/P_R/Λ/ω/Cert` math), Fix 9 (run-scoped contract + manifest).

---

## Phase 3 — Exact Freeze Benchmark and Learned-Agent Evaluation (spec §Phase 3, P3.1–P3.6)

**Exit:** `MEASURED`. **Firewall:** population + semantics immutable; exact PC first, model trajectories second.

### 3.1 Scope

Compute the full 8-cell exact counterfactual on the sealed population with the **single production planner** (structural infinity + certificates + same-instance checks; Fix 7: no second implementation in this phase); then evaluate 3 fixed model families under 4 matched primary freezes with paired repeats, frozen user bundles, blinded tool naming, and a hard safety gate; compute paired metrics with task-level bootstrap; retain all finite/infinite/failure rows and archive raw trajectories for Fix-6 exact replay. Population, semantics, extraction verification, and Fix-4 refactoring class are immutable here.

### 3.2 Files to be made (exact)

```text
results/<run_id>/exact/freeze_results.parquet       # all 8 cells per task/contract/cost: kappa, tied optima, branch cost, cert status, inf cert
results/<run_id>/exact/k_pi_signatures.parquet      # K_Pi vectors + Delta_R + R class (ZERO/FINITE_POSITIVE/STRUCTURAL/UNDERIDENTIFIED)
results/<run_id>/exact/planner_certificates/        # per-row infinity/unreachability certificates
results/<run_id>/exact/planner_selftest.json        # Fix-7 production-planner synthetic-graph tests (no second implementation here)
results/<run_id>/agents/trajectories.jsonl          # raw model trajectories (archived for Fix-6 exact replay; never regenerated for seal)
results/<run_id>/agents/paired_runs.parquet         # task/model/condition/repeat pairing manifest + seed/bundle/model-version keys
results/<run_id>/agents/metrics.parquet             # 7 metrics per task/model/condition + aggregates by regime/family
results/<run_id>/controls/control_results.jsonl     # reject-on-open, evidence-only, untyped-generic runs
results/<run_id>/reports/phase3_summary.json        # regime distribution, adaptation, regret, violations (honest zeros kept)
results/<run_id>/PHASE3_COMPLETE                    # marker
results/<run_id>/phase_manifest.json                # extended with Phase-3 hashes
schemas/freeze_result.schema.json                   # validates freeze_results rows
schemas/agent_run.schema.json                       # validates trajectories + pairing keys
```

### 3.3 Code to be produced and how to code it

- `src/pc_tau/planner.py` — `solve(graph, forbidden_mask)`: positive-support AND-OR minimax closure. Represent infinity as a dedicated `INF = StructuralInfinity()` singleton (never a numeric sentinel like 999999 — unit test asserts `INF != 10**18` and arithmetic rules). Return `(kappa, tied_optimal_initial_repairs[], branch_cost, terminal_status, certificate)`. Exhaustively enumerates finite repair graph (BFS/DFS with memo + cycle → infinity cert); records all tied optima (omission fails cross-check). CPU-only.
- `src/pc_tau/freeze.py` — `lattice(task_contract)`: for each of F000,F100,F010,F001,F110,F101,F011,F111 retain repair iff `Touch(q) ∩ frozen_set == ∅` (atomic: E+R removed by R-freeze unless E-only subaction exists). Emit same-instance manifests proving only the mask differs within a task/contract/cost group (hash base instance once, hash each masked view). Classify `Delta_R = kappa^{-R}-kappa` if both finite else structural categorical; `R_class ∈ {ZERO,FINITE_POSITIVE,STRUCTURAL,UNDERIDENTIFIED}`; route diversity counts; fallback premium per freeze; pairwise/mixed interaction flags.
- `src/pc_tau/runtime.py` — governance middleware around the learned agent + tool env: exposes task-level tools (`lookup, ask, bind, compile_certificate, request_approval`, never E/R/A labels — string-scan test fails on leak); blocks effectful API calls unless exact certificate CLOSED (open-state attempts logged as violations, `executed_unauthorized == 0` invariant asserted after every episode); recomputes certificate after every repair; enforces paired identity (same DB/goal/bundle-seed/model-config/admitted-facts; only mask changes; mismatch raises).
- `src/pc_tau/metrics.py` — exact summaries + paired agent metrics: governance-correct completion, repair regret (`agent_cost - kappa_Pi` finite only), route discovery rate, optimal-route rate, freeze adaptation (switch to valid fallback when preferred class frozen), excess escalation, unsafe attempt rate. Stats: no CIs on K_Pi; paired task-level differences + bootstrap CIs over tasks (resample tasks, not seeds); report Track N and Track F separately; stratify by regime × family; never collapse to single accuracy.
- Baselines in `runtime.py`/`controls/`: `reject_on_open` (abstain/escalate immediately), `evidence_only` (E repairs only), `untyped_generic` (all legal repairs, no E/R/A semantics, no K_Pi), `pc_oracle` (env optimum for regret reference).
- User simulation: bundles from `preregistration/user_response_protocol.json` materialized pre-run; paraphrase via seeded template (seed in paired manifest); semantic invariance asserted by hash of fact-set across freezes.
- `scripts/phase3_exact.py` (production planner only; Fix 7), `phase3_agents.py` (3 families × 3 repeats × 4 freezes; 2,160 episodes at 60 tasks), `phase3_metrics.py`, `phase3_controls.py`. There is deliberately **no** `phase3_crosscheck.py` (Fix 7: one production + one audit planner total). The independent audit planner (`src/pc_tau_audit/planner_audit.py`) may be developed and unit-tested on synthetic graphs before the sealed run, but its authoritative F000–F111 comparison runs in Phase 4. Phase 3 must not read or write the Fix-4 refactoring files.
- Tests `tests/phase3/`: `test_infinity_structural.py` (sentinel banned, cycle→INF cert), `test_tied_optima_kept.py`, `test_planner_synthetic.py` (Fix-7: production planner on hand-solved graphs incl. finite-substitution + structural cases), `test_same_instance.py` (only mask differs), `test_no_label_leak.py` (agent-visible strings contain no E/R/A/mask; omega-leak fixture fails), `test_safety_gate_zero_exec.py`, `test_pairing_identity.py`, `test_bootstrap_over_tasks.py`, `test_all_rows_retained.py` (inject null/inf/failure, assert present in summary), `test_trajectories_archived.py` (Fix-6: raw trajs immutable, hashed in manifest for exact replay).

### 3.4 Model specifics + brutal disjoint benchmarks (user requirement)

Training: **none** (evaluation-only; IDs + revisions + gen params frozen in `configs/models.yaml`, hashed pre-Phase 3). Resultant benchmarks: `k_pi_signatures.parquet` (exact), `metrics.parquet` (paired agent behavior), `phase3_summary.json` (regime-stratified). Brutal-difference testing: (a) exact 8-cell vs agent 4-cell asymmetry; (b) Track F balanced panel as a **different benchmark** from Track N (mechanistic coverage only); (c) pilot never in N or F (provisional geometry invisible); (d) corruption families (§P4.2) + frozen-class refactoring audit (§P4.3/Fix 4) re-test every agent-facing claim; (e) sole independent audit planner comparison happens in Phase 4 on frozen serialized graphs (Fix 7). Anti-overfitting: paired design + frozen bundles + viable-route eligibility (Fix 3) + no successful-run filtering + no prevalence/superiority claims + model-as-probe framing.

### 3.5 Exit gate G3

`MEASURED` iff: exact lattice 100% allocated (8 cells × retained tasks × completions) with valid certificates, synthetic planner self-tests pass, zero same-instance mutations, every model run traceable to sealed task/contract/freeze identity (pairing manifest join succeeds), all null/infinite/failed rows retained, raw trajectories archived + manifested for Fix-6 exact replay, and Fix-4 refactoring files untouched (hashes equal G2 values). Log to Path.md §P3.

**Covers spec:** §§2.1–2.3 (scale/regimes/baselines), §§P3.1–P3.6, §5.2 G3, §4.1 `planner.py`/`freeze.py`/`runtime.py`/`metrics.py`, §6.1 (high-value finite-substitution pattern sought honestly), §6.3 lines 4–5 ("solve K_Pi exactly; test learned agents"). Review fixes in this phase: Fix 1 (pilot invisible), Fix 4 (refactor files untouched), Fix 5 (ω-leak precise), Fix 6 (trajectory archiving for replay), Fix 7 (single production planner), Fix 9 (run-scoped exact/agents).

---

## Phase 4 — Independent Audit, Falsification, Claims, and Seal (spec §Phase 4, P4.1–P4.6)

**Exit:** `SEALED` or `INVALID`. **Firewall:** no scientific mutation; independent code rebuilds and validates or fails the result; may invalidate, never improve by changing the benchmark.

### 4.1 Scope

Rebuild everything from frozen serialized evidence with a **separate audit package** (forbidden imports); run 8 control/corruption families + semantic-refactoring audit; mechanically constrain paper language via claim ledger + nonclaim locks; seal a one-command-reproducible release or mark INVALID with failure preserved.

### 4.2 Files to be made (exact)

```text
src/pc_tau/claims.py               # Fix-10 predicate ledger + CLAIMS.md generator (only authorized predicates emit)
src/pc_tau_audit/source_audit.py   # rehash source; reconstruct IDs from eligibility rule; verify pilot exclusion + fallback logic
src/pc_tau_audit/contract_audit.py # rebuild H,P_R,Lambda,omega,Cert,legal set,atomicity,family status from verified source facts
src/pc_tau_audit/touch_audit.py    # recompute Touch from successor semantics; full-record compare
src/pc_tau_audit/planner_audit.py  # Fix-7 SOLE independent exhaustive F000–F111 recompute (authoritative comparison here)
src/pc_tau_audit/run_audit.py      # recompute closure/route/regret/escalation/violations/pairing/aggregation from raw trajs
src/pc_tau_audit/claims_audit.py   # Fix-10 verify predicates + evidence pointers (no keyword blacklists)
results/<run_id>/audit/independent_source.json
results/<run_id>/audit/independent_contracts.jsonl
results/<run_id>/audit/independent_touch.parquet
results/<run_id>/audit/independent_exact_results.parquet
results/<run_id>/audit/independent_agent_metrics.parquet
results/<run_id>/audit/corruption_results.jsonl     # all 8 families: injected → detected (fail-closed proof)
results/<run_id>/audit/planner_agreement.json       # Fix-7 production vs audit planner 100% agreement report
results/<run_id>/reports/CLAIMS.md                  # Fix-10 generated ONLY from authorized predicates
results/<run_id>/reports/REPRODUCE.md               # Fix-6 two-path doc: exact replay (byte-identical) vs live rerun (new run-id)
results/<run_id>/reports/benchmark_report.md        # full report incl. regime distribution (honest zeros), Track N vs F split
results/<run_id>/reports/failure_cards.jsonl        # consolidated (contract + measurement + audit failures)
results/<run_id>/reports/audited_tables/            # frozen paper tables
results/<run_id>/reports/claim_ledger.json          # Fix-10 structured predicates + claim → evidence pointers (see §4.3)
results/<run_id>/reports/artifact_graph.json        # every artifact + hash + producer (Fix-9 sole graph index)
results/<run_id>/reports/audit.json                 # layer-by-layer equality report
results/<run_id>/phase_manifest.json                # final manifest (all phases)
results/<run_id>/SEALED (or INVALID + failure record)
schemas/audit.schema.json
schemas/claim_ledger.schema.json  # Fix-10 predicate schema
```

### 4.3 Code to be produced and how to code it

- Audit boundary: `src/pc_tau_audit/*` **must not** import `pc_tau.semantics/touch/freeze/planner/metrics(aggregation)/claims`. Enforce via `tests/phase4/test_no_prod_import.py` (AST import scan) + runtime `sys.modules` guard in `run_audit.py`. Audit consumes only canonical serialized evidence (`external_source/*`, `preregistration/*`, `results/<run_id>/contract/*`, `results/<run_id>/exact/*`, `results/<run_id>/agents/*`) plus frozen Fix-4 policy files; it never reads pilot provisional geometry as science.
- Layer recomputations (§P4.1 table): source rehash + ID reconstruction from `eligibility_rule.json` (incl. Fix-3 viable-route + Fix-8 `N<40 OR domains<2` trigger); contract rebuild (`U_H,H,P_R,Λ,ω,Cert`, legal, atomicity, family with Fix-5 types); touch recompute + full compare (mismatch → INVALID); **Fix-7 authoritative planner comparison**: `planner_audit.py` (different algorithm text than `planner.py`, e.g. iterative-deepening enumerator vs recursive minimax) recomputes all 8 cells; `audit/planner_agreement.json` must be 100% (any row mismatch → INVALID); metrics recompute from `trajectories.jsonl`; claims verify via Fix-10 predicates.
- Corruption suite `scripts/phase4_corrupt.py` (8 families, each with inject→expect-detect):
  1. Semantic invariance (value rename, history reorder, action reorder, irrelevant metadata, id rename → K_Pi invariant; change → detect).
  2. Boundary violations (R reads external; E edits P_R; A adds fact → reject).
  3. Freeze integrity (illegal E+R split; wrong action in F010; cross-condition base mutation → detect).
  4. Information leakage (evaluator truth into **ω (observation channel)** or model-visible tool response → detect+invalidate; Fix-5 precise).
  5. Planner integrity (wrong finite row, dropped infinity, numeric sentinel, tied-optimum omission → detect).
  6. Population integrity (pilot leak incl. provisional geometry promoted to science, post-Delta_R selection, missing failure card, single-domain N≥40 without telecom trigger → detect).
  7. Agent-run integrity (seed/bundle/version mismatch, truncated traj, missing tool result → detect).
  8. Claim integrity (unauthorized predicate emission: prevalence/superiority/deployment-readiness/natural-frequency-from-F → fail claim gate; Fix-10).
- Refactoring audit `scripts/phase4_refactor.py` (Fix 4: executes **only** the Phase-2-frozen `admissible_refactorings.json` + `semantic_boundary_policy.json` + `contract_family_rules.json`; designing new perturbations here fails the gate): harmless source-preserving rewrites in the frozen class must leave K_Pi invariant; genuinely boundary-changing source-consistent alternatives in the frozen class must flip task to PARTIAL/identified-set, never forced label. Any result-driven choice of perturbations is a hard INVALID.
- Claims `src/pc_tau/claims.py` (Fix 10 logical locks, Polaris-style — no keyword blacklists): structured ledger, e.g.
  ```json
  {"prevalence_claim_authorized": false, "superiority_claim_authorized": false,
   "deployment_safety_claim_authorized": false, "natural_frequency_from_track_f": false,
   "planner_expressiveness_claim_authorized": false, "multiroute_existence_authorized": true,
   "finite_substitution_authorized": true, "imperfect_adaptation_authorized": true,
   "controlled_regime_authorized": true, "typing_invariance_authorized": true}
  ```
  `CLAIMS.md` is **generated only from authorized predicates** (generator refuses to emit unauthorized sentences even if hand-written text is injected; paraphrase bypass like "broad real-world frequency" cannot pass because authorization is predicate-level, not string-level). 5 allowed (§P4.4) map to true predicates with required evidence pointers; 5 permanent nonclaims (§P4.5) map to permanently false predicates. Violation fails seal.
- Seal `scripts/phase4_seal.py`: index every artifact into `reports/artifact_graph.json` + `phase_manifest.json` (path→sha256→producer→inputs), verify post-seal mutation zero (re-hash), then Fix-6 two-path reproduction: (a) **exact replay** `run_pc_tau.py --reproduce <run-id>` from archived `trajectories.jsonl` + frozen contracts (must be byte-identical tables + identical seal hash; clean fresh clone tested); (b) **live rerun** `run_pc_tau.py --replicate-live <run-id>` reinvokes same model IDs/config into a **new** run-id (schema-checked, behavioral statistics compared in `reports/replication_comparison.json`; trajectories/seal NOT required to match — provider nondeterminism is expected). `REPRODUCE.md` documents both. On any exact-replay inequality/undetected corruption/unindexed artifact/unauthorized predicate → `INVALID` + preserved failure record (never deleted by cleaner).
- Tests `tests/phase4/` + `tests/metamorphic/`: import-ban, layer-equality on golden fixtures, planner-agreement 100% (`planner_agreement.json`), all-8-corruption-detected, frozen-class-only refactoring (unlisted perturbation → gate failure), refactor-invariance vs PARTIAL-flip, Fix-10 claim-lock negatives (each unauthorized predicate must fail even under paraphrase; generator test: unauthorized input yields no output sentence), exact-replay idempotence (two replays → same seal hash, timestamps excluded) + live-rerun schema test (new run-id, no seal-match requirement).

### 4.4 Models / brutal benchmarks / anti-overfitting for this phase

No training. The "brutal benchmark" **is** Phase 4: the entire Phase 3 result is re-tested by the sole independently written planner + deliberately corrupted inputs drawn from the Phase-2-frozen refactoring class. Agent behavior is re-derived from archived raw trajectories (not from Phase 3 aggregates), so any Phase 3 aggregation overfit is exposed. Fix-10 predicate locks prevent tuning paper language to attractive figures (paraphrase cannot bypass). Fix-6: exact replay brutally tests determinism; live rerun separately tests robustness to provider nondeterminism.

### 4.5 Exit gate G4 + Definition of Done + Hard stops

`SEALED` iff (§5.2 G4): independent source/contract/touch/planner/metrics equality (Fix-7 agreement 100%); all corruption families detected; Fix-4 frozen-class-only refactoring passes; Fix-10 predicate locks pass; full artifact graph + manifest; **Fix-6 exact replay identical from clean checkout**. Else `INVALID`.

Definition of Done (§5.3, all must hold; checked by `phase4_seal.py --check-gate g4`): ≥40 Track N viable-route MULTI_ACTION (≥2 domains, pre-Delta_R, Fix 3); full K_Pi + ZERO/FINITE_POSITIVE/STRUCTURAL/UNDERIDENTIFIED per primary task; honest regime distribution (no guaranteed counts); Track F 4-regime balanced-by-design; 3 families × F000/F100/F010/F001 paired with raw trajs archived; 6 agent metrics vs oracle; independent reproduction of typing+freezes+metrics; all corruptions fail closed; Fix-10 zero unauthorized predicates emitted; **Fix-6 exact-replay one-command clean-checkout reproduce + separately documented live-rerun path**. Success even if many `Delta_R=0` (discrimination, not manufactured necessity).

Hard stops (§5.1 — STOP/INVALID immediately): inclusion depends on Delta_R/K_Pi/model outcome; <40 natural **or <2 eligible domains** even after Fix-8 fallback (`N<40 OR domains<2` triggers telecom once; still failing → STOP, never weaken eligibility); manual post-result typing/extraction-resolution overrides (incl. Fix-2 disagreement forced to IDENTIFIED); audit disagreement (incl. planner mismatch); label/truth leak into ω or model-visible channel (Fix-5); approximation needed for main population; N/F tracks mixed in analysis; Fix-4 refactoring class created/modified after G2; Fix-6 exact-replay mismatch; unauthorized predicate emission. Each maps to an automated check + Path.md entry.

**Covers spec:** §§P4.1–P4.6, §§5.1–5.3, §4.1 `claims.py` + audit modules, §4.2–4.3 (ledger + runtime discipline), §6 (D32 legs table: Polaris/Natural/Controlled/theory + must-not-claims; §6.1 high-value pattern; §6.2 refs; §6.3 line 6 "let independent code try to break it"). Review fixes in this phase: Fix 4 (frozen-class execution), Fix 5 (ω-leak + `P_R` equivalence), Fix 6 (exact-vs-live split), Fix 7 (sole audit planner + agreement), Fix 8 (fallback + population-integrity check), Fix 9 (run-scoped audit/reports + graph), Fix 10 (predicate locks).

---

## Appendix A. D32 integration (spec §6, not a phase)

- Polaris leg: historical single-route existence (source-locked, reconstructed, frozen, audited). Must not claim multi-route/substitution/agent behavior/prevalence.
- PC-TAU Natural: same-instance multi-route + freeze-changed geometry + imperfect adaptation. Must not claim prevalence/universal safety.
- PC-TAU Controlled: zero/finite/structural/complementarity distinguished. Must not claim natural frequency.
- D32 theory: when E/R/A invariant under declared semantics vs when identified-set required. Must not claim arbitrary refactorings preserve labels.
Implementation: `results/<run_id>/reports/benchmark_report.md` gets a D32 section with exactly these 4 rows; `claims_audit.py` enforces predicate authorizations (Fix 10) and rejects any emission violating the must-not-claim column, even under paraphrase.

## Appendix B. Verification that WorkPlan covers everything

Spec → WorkPlan: cover §Mission→0.1; §1→0.1; §1.1→0.1; §1.2→0.5+Phase 2 (Fix-5 types); §1.3→0.5+Phase 2 (Fix-3 viable-route); §2→0.4+Phase 1 (Fix-8 fallback); §2.1→0.4 (Fix-8 pilot + trigger); §2.2→0.5; §2.3→0.5+Phase 3; §3→0.2; Phase 1→§Phase 1 (Fix-1 provisional); Phase 2→§Phase 2 (Fix-2 extraction, Fix-4 refactor freeze, Fix-5 math); Phase 3→§Phase 3 (Fix-7 two planners, Fix-6 replay archiving); Phase 4→§Phase 4 (Fix-4 execution, Fix-6 split, Fix-7 agreement, Fix-10 predicates); §4→0.6 (Fix-9 run-scoped); §4.1→phase code sections; §4.2→Path.md; §4.3→0.6 (Fix-6 split, Fix-9 manifests); §5.1→Phase 4.5 (Fix-8 trigger, Fix-4/6/10 stops); §5.2→phase gates; §5.3→Phase 4.5 (Fix-6 DoD); §6→Appendix A; §6.1→Phase 3; §6.2→Phase 1 + refs; §6.3→phase gates in order. Method: `grep` each spec header against this file (reviewer check in Path.md §0). Review patch (10 fixes, 2026-09-06): Fix 1 pilot-provisional, Fix 2 extraction protocol, Fix 3 viable-route, Fix 4 refactor-class freeze, Fix 5 ω/P_R, Fix 6 exact-vs-live, Fix 7 two planners, Fix 8 fallback trigger + pilot domains, Fix 9 run-scoped artifacts, Fix 10 predicate locks.

## Appendix C. Commands (canonical)

```bash
python scripts/phase1_pin_source.py --config configs/experiment.yaml
python scripts/phase1_census.py && python scripts/phase1_pilot.py && python scripts/phase1_preregister.py --check-gate g1
python scripts/phase2_extract.py && python scripts/phase2_verify.py && python scripts/phase2_compile.py && python scripts/phase2_touch.py && python scripts/phase2_eligibility.py && python scripts/phase2_freeze_refactor_policy.py && python scripts/phase2_controlled_panel.py
python scripts/run_pc_tau.py --check-gate g2
python scripts/phase3_exact.py --run-id <id> && python scripts/phase3_agents.py --run-id <id> && python scripts/phase3_metrics.py --run-id <id> && python scripts/phase3_controls.py --run-id <id>
python scripts/phase4_corrupt.py --run-id <id> && python scripts/phase4_refactor.py --run-id <id> && python scripts/run_audit.py --run-id <id> && python scripts/phase4_verify_claims.py --run-id <id> && python scripts/phase4_seal.py --run-id <id> --check-gate g4
pytest -q
python scripts/run_pc_tau.py --reproduce <id>        # Fix-6 exact artifact replay (byte-identical seal)
python scripts/run_pc_tau.py --replicate-live <id>   # Fix-6 live model rerun (new run-id, schema + stats only)
python scripts/clean_run.py --run-id <unsealed-id>  # only deleter; refuses sealed IDs
```
