# WorkPlan.md — PC-TAU Multi-Route Perceptive Closure Benchmark for Tool-Using Agents

**Spec:** Implementation Specification v0.1 (15 pages, §§1–6.3).
**Repo:** https://github.com/MAVS-RESEARCH/PC-TAU (clone verified 2026-09-06; only `LICENSE` present).
**Upstream source target:** https://github.com/sierra-research/tau2-bench (existence verified 2026-09-06; domains `mock/airline/retail/telecom/banking_knowledge`, text half-duplex + voice full-duplex).
**Status:** Planning sealed; no scientific results exist yet.
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

1. **Result-independent eligibility (anti-cherry-picking).** Natural-track inclusion (§P1.3, §P2.5) may inspect only source-grounded structure (consequential effect, open certificate, ≥2 legal repairs, ≥2 touch-distinct profiles, finite exact graph, provenance, non-pilot). It is **forbidden** to inspect `Delta_R`, `K_Pi`, or model success. Violation = hard STOP (§5.1).
2. **Pilot is throwaway.** Exactly 24 tasks (12 airline + 12 retail), IDs permanently excluded from final population (§P1.1). Pilot may inform design; never enters paper results. This is the "training set" that is **never tested on**.
3. **Frozen semantic user bundles.** Generated/sealed before the sealed run; paraphrase may vary under fixed seed but facts/willingness/authorization content are invariant across matched freezes (§P1.4, §P3.4). Prevents simulator drift tuning.
4. **Paired repeats.** 3 paired repeats per task/model/primary-freeze; same initial DB, goal, bundle/seed, model config, admitted facts — only freeze mask changes (§P3.3). Repeats quantify instability, not population size (§P3.6).
5. **ENTIRELY different test benchmarks:**
   - Exact 8-cell lattice (F000–F111) is ground truth; model-facing runs use only 4 primary cells (F000, F100, F010, F001). Models never see the full lattice during evaluation.
   - Controlled Track F (32 tasks, 8 per regime, balanced **by design**) is a **separate mechanistic benchmark**; never used to estimate natural frequency (§2, §P2.6). Natural Track N (60–96 target, min 40) is the only prevalence-relevant population, and even there **no prevalence claim** is allowed.
   - 8 deliberate corruption families (§P4.2) + semantic-refactoring audit (§P4.3) act as adversarial benchmarks: any tuning that breaks invariance, leaks labels/truth, or splits atomic actions must fail closed.
   - Independent audit planner (§P4.1) is a separately written exhaustive algorithm that recomputes every F000–F111 value from serialized frozen evidence without importing production modules. Agreement is required for SEAL.
6. **No successful-run filtering.** Every null, zero, infinite, failure, escalation, underidentified case is retained in tables (§4.3, §P3 outputs). Bootstrap CIs are over tasks, never over seeds as independent tasks; `K_Pi` gets no CIs because it is exact (§P3.6).
7. **Claim locks.** 5 allowed claims each require prespecified evidence (§P4.4); 5 permanent nonclaims are literal-false locked and fail the gate if emitted (§P4.5, `src/pc_tau/claims.py` + `src/pc_tau_audit/claims_audit.py`).

If a future contributor proposes actual training (e.g. distilling a repair policy), it must be preregistered as a new Track with a disjoint task split, disjoint seeds, and the same 8-family corruption + independent-planner gate before any claim. No such training is in scope for v0.1.

### 0.4 Scale contract (spec §2.1)

| Stage | Target | Role |
|---|---|---|
| Pilot | 24 throwaway (12 airline, 12 retail) | Feasibility only; never paper results |
| Natural final (Track N) | Target 60–96 MULTI_ACTION; **minimum 40 across ≥2 domains** | Primary exact + learned-agent evidence |
| Controlled panel (Track F) | 32 tasks: 8 R-zero, 8 R-finite, 8 R-structural, 8 E/R-complementary | Exact regime coverage; learned-agent subset may be prespecified balanced 16 if cost-constrained; never natural incidence |
| Agent episodes | 3 families × 3 repeats × 4 primary freezes | 2,160 episodes at 60 natural tasks; exact solver still runs all 8 freezes |

Telecom is a **preregistered fallback only**: activates exactly once if airline+retail yield <40 under the same source-only census; if still <40, STOP rather than weaken eligibility (§P1.3).

### 0.5 Regimes, baselines, nondegeneracy (spec §§1.2–1.3, 2.2–2.3)

E/R/A operational meaning + hard firewalls:

- **E (admitted evidence):** facts crossing sealed admission boundary (user answers, read-only tool outputs, identity, reservation/order facts, confirmations, provenance). E-only repair may acquire a new admitted fact but **may not** alter certificate mapping or authority.
- **R (certificate representation):** which distinctions among already-admitted histories are decision-bearing. R-only repair computes **only** from already-admitted H; may not query user/external DB/unavailable value.
- **A (epistemic authority):** which sources/attestations/approvals/predicates/interfaces are admissible. A-only repair changes authority **without** adding a world fact or changing P_R.

`Touch(q)` is **derived, never authored**: E iff H changes across a positive-support successor; R iff certificate partition P_R changes; A iff Lambda changes. Mixed touch frozen atomically unless source exposes a decomposition.

Nondegeneracy gate (before any freeze value): MULTI_ACTION (≥2 independently legal repairs from same open state) + touch diversity (≥2 distinct derived profiles) + open initial certificate + source/provenance sufficiency + exact tractability. Desired geometry: finite substitution (e.g. kappa=1, kappa^{-R}=2 or 3); structural finite-to-infinite retained but benchmark must not depend on delete-the-sole-closer.

Regimes: R-zero (`Delta_R=0`), R-finite (`0<Delta_R<∞`), R-structural (kappa finite, kappa^{-R}=∞), E/R-complementary (neither E-only nor R-only closes, governed composition does). A-mediated retained when natural; never forced.

Baselines: reject-on-open, evidence-only resolver, untyped generic repair, PC exact oracle (reference for regret, not an agent baseline).

### 0.6 Repository layout to be built (spec §4)

```text
PC-TAU/
  configs/experiment.yaml  costs.yaml  models.yaml  freezes.yaml (spec: freeze_lattice.yaml)  claims.yaml
  schemas/task.schema.json  semantic_fact.schema.json  contract.schema.json  repair.schema.json
          touch.schema.json  freeze_result.schema.json  agent_run.schema.json  audit.schema.json
  src/pc_tau/source.py  semantics.py  repairs.py  touch.py  planner.py  freeze.py  runtime.py  metrics.py  claims.py
  src/pc_tau_audit/source_audit.py  contract_audit.py  touch_audit.py  planner_audit.py  run_audit.py  claims_audit.py
  scripts/phase1_*.py  phase2_*.py  phase3_*.py  phase4_*.py  run_pc_tau.py
  tests/unit/  phase1/  phase2/  phase3/  phase4/  metamorphic/
  external_source/  results/<run_id>/  WorkPlan.md  Path.md
  preregistration/  contract/  audit/  reports/
```

Note: spec P1 names `configs/freeze_lattice.yaml`; layout §4 names `freezes.yaml`. Both will be created with `freezes.yaml` canonical and `freeze_lattice.yaml` kept as a byte-identical symlink/copy for spec fidelity (hashed; mismatch fails G1).

Runtime discipline (§4.3): one named run dir per sealed attempt; safe cleaner removes only an explicitly named **unsealed** run; hash every paper-influencing artifact (sha256); canonical JSON (sort_keys, separators, utf-8); timestamps in logs only, never in scientific hashes; exact solver CPU-only, no GPU; model identity + generation params frozen and hashed.

Logging discipline (§4.2): Path.md append-only; every phase records files, commands, hashes, run IDs, tests, deviations, rejected attempts, WorkPlan-follows yes/no; planning/pilot/sealed/paper-transformations visibly distinct.

Tech: Python `>=3.12,<3.14` (matches tau2-bench), `uv` sync, deps `pyyaml`, `jsonschema`, `pyarrow`+`pandas` (parquet), `pytest`. No torch/GPU for exact path. Model calls via LiteLLM-compatible APIs or local inference, exact IDs + revisions hashed into `configs/models.yaml` before Phase 3.

### 0.7 Traceability (how "nothing omitted" is verified)

Each phase section below ends with `Covers spec:` + explicit section list. After Phase 4, §5 (gates/stops/done) and §6 (D32/external refs) are mapped. Verification commands: `pytest`, `python scripts/run_pc_tau.py --check-gate g1|g2|g3|g4`, `python scripts/phase4_verify_claims.py`, clean-checkout reproduce. Any spec row without a file+test+gate entry fails review.

Stale-results rule (user requirement): clone contained **zero** result artifacts (verified: only LICENSE). `results/`, `contract/`, `audit/`, `reports/` start empty and git-ignored except seal markers (`*_SEALED`, `PHASE3_COMPLETE`, `SEALED`, `CONTRACT_SEALED`). Safe cleaner `scripts/clean_run.py --run-id <unsealed>` is the only deleter; it refuses sealed IDs. After each phase, only new artifacts from that phase exist; Path.md logs the cleaner invocations (including no-ops).

Commit/push rule (user requirement): after **each** phase gate passes, commit with message `phase<N>: <gate> <run-id> <short-hash>` and push to `origin/main` without being asked. Planning commit (`docs: WorkPlan.md + Path.md setup`) is pushed immediately after verification.

---

## Phase 1 — Source Lock, Pilot, and Preregistration (spec §Phase 1, P1.1–P1.4)

**Exit:** `PREREGISTERED` or `STOP`. **Firewall:** no final task inclusion from freeze outcomes; no K_Pi; pilot disposable.

### 1.1 Scope

Pin the upstream tau-family source immutably; run a 24-task throwaway pilot to prove MULTI_ACTION + finite-substitution feasibility on ordinary CPU with a defensible E/R/A operational firewall; preregister a result-independent final-task rule + fallback rule; seal cost/model/user/claim configs for all four phases. Nothing in this phase may compute a final K_Pi or run a learned-agent evaluation.

### 1.2 Files to be made (exact)

```text
external_source/source_manifest.json      # URL, commit SHA, source-tree hash, dep lock, env identity, license
external_source/task_census.json          # airline+retail (+telecom only if fallback triggers) task inventory
external_source/pilot/*                   # 12 airline + 12 retail pilot IDs, selection rule, provisional gate logs (excluded forever)
configs/experiment.yaml                   # domains, splits, run-id scheme, determinism, phase gates
configs/costs.yaml                        # unit-intervention primary; optional native-cost only if source-defensible pre-results
configs/models.yaml                       # 3 heterogeneous families, exact IDs + API revisions + gen params + sha256
configs/freezes.yaml + freeze_lattice.yaml# 8-cell lattice F000–F111; primary model-facing F000,F100,F010,F001 flagged
configs/claims.yaml                       # allowed-claim templates + literal-false nonclaim locks
preregistration/eligibility_rule.json     # machine-readable required/forbidden/fallback rule (P1.3)
preregistration/model_protocol.json       # roster, repeats=3, pairing keys, tool-naming (no E/R/A labels), safety gate
preregistration/user_response_protocol.json # bundle freeze + seed-controlled paraphrase, invariance clause
preregistration/nonclaims.json            # 5 nonclaims verbatim
reports/phase1_preregistration.json       # gate evidence: pilot yield, source hashes, config hashes, PREREGISTERED/STOP
schemas/task.schema.json                  # validates task_census + pilot records
```

### 1.3 Code to be produced and how to code it

- `src/pc_tau/source.py` — `pin_source(url, rev)`: clone tau2-bench at pinned commit into `external_source/_upstream/` (git-ignored except manifest), record `commit_sha`, `tree_hash = sha256(sorted file hashes)`, `dep_lock (uv.lock hash + python version)`, `env_identity (os, cpu, python -V)`, `license + attribution`. `census(domain)`: enumerate tasks via upstream `data/` + `src/tau2/domains/` loaders without importing agent logic; emit `task_id, domain, policy_locator, tool_surface, db_schema, user_schema, eval_criteria`. `select_pilot()`: deterministic sample (seed in experiment.yaml) of exactly 12+12 from dev-only split or explicit pilot IDs; write exclusion list used by all later phases. How: stdlib + pyyaml + hashlib; no LLM calls; no E/R/A strings in this module (enforced by unit test grepping for `Touch`/`kappa`).
- `scripts/phase1_pin_source.py`, `scripts/phase1_census.py`, `scripts/phase1_pilot.py`, `scripts/phase1_preregister.py`, `scripts/run_pc_tau.py` (dispatcher + `--check-gate g1`), `scripts/clean_run.py` (safe cleaner).
- Pilot gate logic (in `phase1_pilot.py`): provisional governance gate instruments open-state enumeration using only source policy/task-state/API semantics/user channels; rejects any repair justified by PC labels/desired Delta_R/observed freeze; checks (a) ≥8/24 MULTI_ACTION with ≥1 domain viable, (b) ≥1 finite-fallback case, (c) E/R/A actions validatable by operational constraints (unit test: an R-action that reads external state is rejected), (d) exhaustive solvability on CPU (timeout guard, node budget). GO/STOP table from spec pp.4–5 implemented as `gate()` returning `PREREGISTERED` or `STOP` with reasons.
- Configs: `costs.yaml` sets `primary: unit_intervention_cost: 1` per repair step; `secondary_native` left `null` unless source cost semantics found pre-results (with locator). `models.yaml` fixes 3 families (e.g. `family-a: gpt-4.1-YYYYMMDD`, `family-b: claude-*-YYYYMMDD`, `family-c: llama-*-local-Q8`) — exact IDs chosen at implementation time, then hashed; `repeats: 3`, `primary_freezes: [F000,F100,F010,F001]`. `freezes.yaml` enumerates all 8 masks as `{E:bool,R:bool,A:bool}` with canonical names F000–F111.
- Tests `tests/phase1/`: `test_source_pin_hash.py` (re-hash equals manifest), `test_pilot_exclusion.py` (pilot IDs never in census-derived final candidate query), `test_eligibility_no_freeze_ref.py` (static AST grep: eligibility module never imports freeze/planner/metrics), `test_provisional_gate_rejects_pc_justification.py`. Plus `tests/unit/test_canonical_json.py`.

How to code (style): small pure functions, deterministic (`PYTHONHASHSEED`, sorted keys), type hints, no framework bloat; every writer emits canonical JSON + sidecar `.sha256`.

### 1.4 Benchmarks / models / anti-overfitting for this phase

No training; no model evaluation. The "benchmark" is the pilot go/no-go gate itself. Brutal-difference property: pilot tasks are **never** reused as test tasks (exclusion list enforced in code + audit re-check). Eligibility rule is sealed **before** any K_Pi exists, so tuning to Delta_R is structurally impossible (verified by import-grep test + git log ordering: preregistration commit precedes any freeze-result commit).

### 1.5 Exit gate G1

`PREREGISTERED` iff: pilot passes (≥8/24, ≥1 finite substitution, firewall + CPU ok), source immutable (re-hash match), final eligibility result-independent, fallback sealed, all 4-phase configs sealed, zero final K_Pi / model trajectories exist (filesystem scan in `phase1_preregister.py --check-gate g1`). Else `STOP` with reasons in `reports/phase1_preregistration.json`. Log everything to Path.md §P1.

**Covers spec:** §2 (source foundation/tracks), §P1.1–P1.4, §5.2 G1, §6.2 (tau2-bench URL), §6.3 lines 1–2 ("do not scale first; prove pilot"), §4 layout (configs/external_source/preregistration/reports), §4.1 `source.py`, §4.3 cleaner discipline.

---

## Phase 2 — Semantic Contract and Multi-Route Extraction (spec §Phase 2, P2.1–P2.6)

**Exit:** `CONTRACT_SEALED` / `PARTIAL` / `STOP`. **Firewall:** no freeze values, no learned-agent evaluation; touch derived from source-grounded semantics only.

### 2.1 Scope

For every final-candidate task: two-pass semantic extraction (source facts → contract compilation), enforce admission/representation/authority boundaries + no self-signaling, support contract families (IDENTIFIED/PARTIAL/INVALID), mechanically derive touch with validation, apply result-blind multi-route eligibility, then build the separate 32-task controlled factorial panel after freezing the transformation family.

### 2.2 Files to be made (exact)

```text
contract/semantic_facts.jsonl      # Pass A records + exact source locators (policy predicate, tool effect, provenance)
contract/task_contracts.jsonl      # Pass B: U_H,H,P_R,Lambda,omega,Q,Succ+,Terminal,A_Pi,costs,atomicity,provenance
contract/contract_families.jsonl   # C(Omega) family per task + status IDENTIFIED|PARTIAL|INVALID + disagreement refs
contract/repair_actions.jsonl      # legal repairs with preconditions + successor semantics + source justification
contract/touch_records.parquet     # derived Touch(q) per positive-support successor (H/P_R/Lambda diffs)
contract/route_classification.parquet # |Q_legal|, distinct touches, open/closed, exact-solvable flag
contract/natural_population.json   # sealed Track N IDs (≥40, ≥2 domains, no pilots) + contract hashes
contract/controlled_panel.json     # Track F 32 IDs (8×4 regimes) + transformation-family hash, flagged balanced-by-design
contract/failure_cards.jsonl       # INVALID + excluded candidates with reasons; missing card fails audit
contract/CONTRACT_SEALED           # marker with run-id + root hash (or PARTIAL/STOP marker)
schemas/semantic_fact.schema.json  # validates Pass A
schemas/contract.schema.json       # validates U_H/H/P_R/Lambda/omega/Q/Succ+/Terminal/A_Pi
schemas/repair.schema.json         # validates repair_actions
schemas/touch.schema.json          # validates touch_records (no manual label field allowed)
```

### 2.3 Code to be produced and how to code it

- `src/pc_tau/semantics.py` — `extract_facts(task)`: parse upstream policy predicates, task facts, tool/API effects, provenance, confirmation/auth requirements, user-available facts; emit locators (`file:line` + upstream commit SHA). `compile_contract(facts)`: build `U_H` (universe), `H` (admitted history set w/ provenance), `P_R` (canonical partition of H for certificate — implement as deterministic canonicalizer: sort + normalize value renames that preserve equivalence), `Lambda` (admissible sources/attestations/approvals/predicates/interfaces), `omega` (certificate predicate), `Q` (repair candidates), `Succ+` (positive-support successors with pre/post states), `Terminal`, `A_Pi` (target effect), `costs` (from costs.yaml), `atomicity` (source decomposition or atomic). Forbidden: any import of freeze/planner/agent code (enforced by test). Contract families: `family(task)` returns single contract or finite/symbolic `C(Omega)` (list of completions + constraint expr); status logic per §P2.3.
- `src/pc_tau/repairs.py` — `legal_repairs(contract)`: source-grounded extraction with per-repair `justification` (policy clause + tool semantic + user channel) and `successor` function; atomicity preserved (E+R stays atomic unless source exposes E-only subaction as separate tool path).
- `src/pc_tau/touch.py` — `derive_touch(pre, post)`: compare `H` (set diff on canonical fact ids) → E; compare canonical `P_R` equivalence (not raw syntax) → R; compare canonical `Lambda` → A; return union. **Reject paths:** manual `resource_label` field in inputs raises `ValueError`; R-only candidate that touches user/external DB or reads unadmitted value rejected; E-only that mutates P_R rejected; A-only that adds world fact rejected. Tested by `tests/phase2/test_touch_rejects.py` with 6+ adversarial cases from §P4.2 boundary family.
- `scripts/phase2_extract.py`, `phase2_compile.py`, `phase2_touch.py`, `phase2_eligibility.py`, `phase2_controlled_panel.py`, gate `run_pc_tau.py --check-gate g2`.
- Eligibility predicate (exact code, no Delta_R/K_Pi refs):
  `status==IDENTIFIED and initial_cert==OPEN and len(Q_legal)>=2 and len(set(Touch(q)))>=2 and provenance_complete and exact_solvable and id not in pilot_ids`.
- Controlled panel: freeze `transform_family` (4 geometry templates: R-zero/finite/structural/E-R-complementary) with hash, then synthesize 8+8+8+8 from **non-pilot templates**; label `balanced_by_design: true`, `estimates_natural_frequency: false`.
- Tests `tests/phase2/`: provenance completeness (100% repairs have locators), no-manual-touch (schema rejects `label` field), R-firewall (external-read R rejected), E-firewall, A-firewall, atomicity (E+R not splittable), pilot-exclusion, family status agreement, `test_eligibility_blind.py` (AST + runtime assert: eligibility never reads freeze/metrics outputs).

### 2.4 Benchmarks / models / anti-overfitting for this phase

No training; no freeze planning; no population filtering on Delta_R (code-level import ban + audit re-check). PARTIAL tasks retained in sensitivity appendix, never forced to a preferred label — prevents boundary-tuning overfit. Controlled panel built **after** transformation family frozen, from non-pilot templates, so regime coverage cannot leak into natural selection. Touch is mechanically recomputed, never hand-typed, so post-hoc typing overfit is impossible.

### 2.5 Exit gate G2

`CONTRACT_SEALED` iff: 100% provenance for retained repairs, zero manual touch, point-identified natural population ≥40 MULTI_ACTION across ≥2 domains, controlled panel separately flagged, failure cards for every INVALID/excluded, contract identities immutable (hashes), and filesystem scan proves zero freeze results / model trajectories exist. Else `PARTIAL` (if disagreement remains but IDENTIFIED core ≥40) or `STOP`. Log to Path.md §P2.

**Covers spec:** §§1.2–1.3 (E/R/A, touch, nondegeneracy), §P2.1–P2.6, §5.2 G2, §4.1 `semantics.py`/`repairs.py`/`touch.py`, §6.3 lines 3 ("freeze rules; derive semantics").

---

## Phase 3 — Exact Freeze Benchmark and Learned-Agent Evaluation (spec §Phase 3, P3.1–P3.6)

**Exit:** `MEASURED`. **Firewall:** population + semantics immutable; exact PC first, model trajectories second.

### 3.1 Scope

Compute the full 8-cell exact counterfactual on the sealed population with structural infinity + independent cross-check + same-instance checks; then evaluate 3 fixed model families under 4 matched primary freezes with paired repeats, frozen user bundles, blinded tool naming, and a hard safety gate; compute paired metrics with task-level bootstrap; retain all finite/infinite/failure rows.

### 3.2 Files to be made (exact)

```text
results/<run-id>/exact/freeze_results.parquet       # all 8 cells per task/contract/cost: kappa, tied optima, branch cost, cert status, inf cert
results/<run-id>/exact/k_pi_signatures.parquet      # K_Pi vectors + Delta_R + R class (ZERO/FINITE_POSITIVE/STRUCTURAL/UNDERIDENTIFIED)
results/<run-id>/exact/planner_certificates/        # per-row infinity/unreachability certificates
results/<run-id>/exact/independent_crosscheck.json  # second-planner agreement report (must be 100%)
results/<run-id>/agents/trajectories.jsonl          # raw model trajectories (tool calls, user turns, gate decisions)
results/<run-id>/agents/paired_runs.parquet         # task/model/condition/repeat pairing manifest + seed/bundle/model-version keys
results/<run-id>/agents/metrics.parquet             # 7 metrics per task/model/condition + aggregates by regime/family
results/<run-id>/controls/control_results.jsonl     # reject-on-open, evidence-only, untyped-generic runs
results/<run-id>/reports/phase3_summary.json        # regime distribution, adaptation, regret, violations (honest zeros kept)
results/<run-id>/PHASE3_COMPLETE                    # marker
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
- `scripts/phase3_exact.py`, `phase3_crosscheck.py` (second exhaustive planner — **separately implemented** BFS enumerator on serialized graph, no shared code with planner.py beyond schemas), `phase3_agents.py` (3 families × 3 repeats × 4 freezes; 2,160 episodes at 60 tasks), `phase3_metrics.py`, `phase3_controls.py`.
- Tests `tests/phase3/`: `test_infinity_structural.py` (sentinel banned, cycle→INF cert), `test_tied_optima_kept.py`, `test_crosscheck_agreement.py` (100% row match), `test_same_instance.py` (only mask differs), `test_no_label_leak.py` (agent-visible strings contain no E/R/A/mask), `test_safety_gate_zero_exec.py`, `test_pairing_identity.py`, `test_bootstrap_over_tasks.py`, `test_all_rows_retained.py` (inject null/inf/failure, assert present in summary).

### 3.4 Model specifics + brutal disjoint benchmarks (user requirement)

Training: **none** (evaluation-only; IDs + revisions + gen params frozen in `configs/models.yaml`, hashed pre-Phase 3). Resultant benchmarks: `k_pi_signatures.parquet` (exact), `metrics.parquet` (paired agent behavior), `phase3_summary.json` (regime-stratified). Brutal-difference testing: (a) exact 8-cell vs agent 4-cell asymmetry; (b) Track F balanced panel as a **different benchmark** from Track N (mechanistic coverage only); (c) pilot never in N or F; (d) corruption families (§P4.2) + refactoring audit (§P4.3) re-test every agent-facing claim; (e) independent crosscheck planner must agree on **every** scientific row. Anti-overfitting: paired design + frozen bundles + no successful-run filtering + no prevalence/superiority claims + model-as-probe framing.

### 3.5 Exit gate G3

`MEASURED` iff: exact lattice 100% allocated (8 cells × retained tasks × completions), crosscheck 100% agree, zero same-instance mutations, every model run traceable to sealed task/contract/freeze identity (pairing manifest join succeeds), all null/infinite/failed rows retained. Log to Path.md §P3.

**Covers spec:** §§2.1–2.3 (scale/regimes/baselines), §§P3.1–P3.6, §5.2 G3, §4.1 `planner.py`/`freeze.py`/`runtime.py`/`metrics.py`, §6.1 (high-value finite-substitution pattern sought honestly), §6.3 lines 4–5 ("solve K_Pi exactly; test learned agents").

---

## Phase 4 — Independent Audit, Falsification, Claims, and Seal (spec §Phase 4, P4.1–P4.6)

**Exit:** `SEALED` or `INVALID`. **Firewall:** no scientific mutation; independent code rebuilds and validates or fails the result; may invalidate, never improve by changing the benchmark.

### 4.1 Scope

Rebuild everything from frozen serialized evidence with a **separate audit package** (forbidden imports); run 8 control/corruption families + semantic-refactoring audit; mechanically constrain paper language via claim ledger + nonclaim locks; seal a one-command-reproducible release or mark INVALID with failure preserved.

### 4.2 Files to be made (exact)

```text
src/pc_tau/claims.py               # allowed-claim templates + evidence-class checker + nonclaim literal-false locks
src/pc_tau_audit/source_audit.py   # rehash source; reconstruct IDs from eligibility rule; verify pilot exclusion + fallback logic
src/pc_tau_audit/contract_audit.py # rebuild H,P_R,Lambda,omega,legal set,atomicity,family status from source facts
src/pc_tau_audit/touch_audit.py    # recompute Touch from successor semantics; full-record compare
src/pc_tau_audit/planner_audit.py  # separately written exhaustive F000–F111 recompute
src/pc_tau_audit/run_audit.py      # recompute closure/route/regret/escalation/violations/pairing/aggregation from raw trajs
src/pc_tau_audit/claims_audit.py   # verify every paper number/sentence vs claim ledger + allowed evidence class
audit/independent_source.json
audit/independent_contracts.jsonl
audit/independent_touch.parquet
audit/independent_exact_results.parquet
audit/independent_agent_metrics.parquet
audit/corruption_results.jsonl     # all 8 families: injected → detected (fail-closed proof)
reports/CLAIMS.md                  # only evidence-supported sentences
reports/REPRODUCE.md               # one-command reproduction
reports/benchmark_report.md        # full report incl. regime distribution (honest zeros), Track N vs F split
reports/failure_cards.jsonl        # consolidated (contract + measurement + audit failures)
reports/audited_tables/            # frozen paper tables
reports/claim_ledger.json          # claim → evidence pointers
reports/artifact_graph.json        # every artifact + hash + producer
reports/audit.json                 # layer-by-layer equality report
schemas/audit.schema.json
SEALED (or INVALID + failure record)
```

### 4.3 Code to be produced and how to code it

- Audit boundary: `src/pc_tau_audit/*` **must not** import `pc_tau.semantics/touch/freeze/planner/metrics(aggregation)/claims`. Enforce via `tests/phase4/test_no_prod_import.py` (AST import scan) + runtime `sys.modules` guard in `run_audit.py`. Audit consumes only canonical serialized evidence (`external_source/*`, `contract/*`, `results/<run-id>/*`).
- Layer recomputations (§P4.1 table): source rehash + ID reconstruction from `eligibility_rule.json`; contract rebuild (H/P_R/Lambda/omega/legal/atomicity/family); touch recompute + full compare (mismatch → INVALID); exhaustive planner rerun for all 8 cells (different algorithm text than `planner.py`: e.g. iterative-deepening enumerator vs recursive minimax — agreement required); metrics recompute from `trajectories.jsonl`; claims verify (every number/sentence in CLAIMS.md + benchmark_report tables must resolve to ledger entries with allowed evidence class).
- Corruption suite `scripts/phase4_corrupt.py` (8 families, each with inject→expect-detect):
  1. Semantic invariance (value rename, history reorder, action reorder, irrelevant metadata, id rename → K_Pi invariant; change → detect).
  2. Boundary violations (R reads external; E edits P_R; A adds fact → reject).
  3. Freeze integrity (illegal E+R split; wrong action in F010; cross-condition base mutation → detect).
  4. Information leakage (evaluator truth into omega/tool response → detect+invalidate).
  5. Planner integrity (wrong finite row, dropped infinity, numeric sentinel, tied-optimum omission → detect).
  6. Population integrity (pilot leak, post-Delta_R selection, missing failure card → detect).
  7. Agent-run integrity (seed/bundle/version mismatch, truncated traj, missing tool result → detect).
  8. Claim integrity (hand-strengthened sentence, prevalence/superiority/deployment-readiness → fail claim gate).
- Refactoring audit `scripts/phase4_refactor.py`: harmless source-preserving rewrites must leave K_Pi invariant; genuinely boundary-changing source-consistent alternatives must flip task to PARTIAL/identified-set, never forced label.
- Claims `src/pc_tau/claims.py`: 5 allowed (§P4.4: multi-route exists ≥1 Track N MULTI_ACTION + matched freezes; finite substitution ≥1 finite-positive premium; imperfect adaptation via paired runs; controlled regimes via Track F only; typing invariance via all refactoring checks agree) + 5 permanent nonclaims (§P4.5: no prevalence, no planner-expressiveness, no family superiority/safety, no balanced-panel-as-frequency, no zero-unauthorized-means-safe). Nonclaims implemented as literal string blacklists + evidence-class checks; violation fails seal.
- Seal `scripts/phase4_seal.py`: index every artifact into `artifact_graph.json` (path→sha256→producer→inputs), verify post-seal mutation zero (re-hash), run clean-checkout reproduce (`git clone` fresh + `python scripts/run_pc_tau.py --reproduce <run-id>` → identical seal hash). `REPRODUCE.md` documents the single command. On any inequality/undetected corruption/unindexed artifact → `INVALID` + preserved failure record (never deleted by cleaner).
- Tests `tests/phase4/` + `tests/metamorphic/`: import-ban, layer-equality on golden fixtures, all-8-corruption-detected, refactor-invariance vs PARTIAL-flip, claim-lock negatives (each nonclaim string must fail), reproduce-idempotence (two runs → same seal hash, timestamps excluded).

### 4.4 Models / brutal benchmarks / anti-overfitting for this phase

No training. The "brutal benchmark" **is** Phase 4: the entire Phase 3 result is re-tested by independently written code on disjoint implementation paths plus deliberately corrupted inputs. Agent behavior is re-derived from raw trajectories (not from Phase 3 aggregates), so any Phase 3 aggregation overfit is exposed. Claim locks prevent tuning paper language to attractive figures.

### 4.5 Exit gate G4 + Definition of Done + Hard stops

`SEALED` iff (§5.2 G4): independent source/contract/touch/planner/metrics equality; all corruption families detected; claim locks pass; full artifact graph; clean reproduction identical. Else `INVALID`.

Definition of Done (§5.3, all must hold; checked by `phase4_seal.py --check-gate g4`): ≥40 Track N MULTI_ACTION (≥2 domains, pre-Delta_R); full K_Pi + ZERO/FINITE_POSITIVE/STRUCTURAL/UNDERIDENTIFIED per primary task; honest regime distribution (no guaranteed counts); Track F 4-regime balanced-by-design; 3 families × F000/F100/F010/F001 paired with raw trajs; 6 agent metrics vs oracle; independent reproduction of typing+freezes+metrics; all corruptions fail closed; zero prevalence/superiority/deployment claims; one-command clean-checkout reproduce. Success even if many `Delta_R=0` (discrimination, not manufactured necessity).

Hard stops (§5.1 — STOP/INVALID immediately): inclusion depends on Delta_R/K_Pi/model outcome; <40 natural even after fallback; manual post-result typing overrides; audit disagreement; label/truth leak to model-visible channel; approximation needed for main population; N/F tracks mixed in analysis. Each maps to an automated check + Path.md entry.

**Covers spec:** §§P4.1–P4.6, §§5.1–5.3, §4.1 `claims.py` + audit modules, §4.2–4.3 (ledger + runtime discipline), §6 (D32 legs table: Polaris/Natural/Controlled/theory + must-not-claims; §6.1 high-value pattern; §6.2 refs; §6.3 line 6 "let independent code try to break it").

---

## Appendix A. D32 integration (spec §6, not a phase)

- Polaris leg: historical single-route existence (source-locked, reconstructed, frozen, audited). Must not claim multi-route/substitution/agent behavior/prevalence.
- PC-TAU Natural: same-instance multi-route + freeze-changed geometry + imperfect adaptation. Must not claim prevalence/universal safety.
- PC-TAU Controlled: zero/finite/structural/complementarity distinguished. Must not claim natural frequency.
- D32 theory: when E/R/A invariant under declared semantics vs when identified-set required. Must not claim arbitrary refactorings preserve labels.
Implementation: `reports/benchmark_report.md` gets a D32 section with exactly these 4 rows; `claims_audit.py` rejects any sentence violating the must-not-claim column.

## Appendix B. Verification that WorkPlan covers everything

Spec → WorkPlan: cover §Mission→0.1; §1→0.1; §1.1→0.1; §1.2→0.5+Phase 2; §1.3→0.5+Phase 2; §2→0.4+Phase 1; §2.1→0.4; §2.2→0.5; §2.3→0.5+Phase 3; §3→0.2; Phase 1→§Phase 1; Phase 2→§Phase 2; Phase 3→§Phase 3; Phase 4→§Phase 4; §4→0.6; §4.1→phase code sections; §4.2→Path.md; §4.3→0.6; §5.1→Phase 4.5; §5.2→phase gates; §5.3→Phase 4.5; §6→Appendix A; §6.1→Phase 3; §6.2→Phase 1 + refs; §6.3→phase gates in order. Method: `grep` each spec header against this file (reviewer check in Path.md §0).

## Appendix C. Commands (canonical)

```bash
python scripts/phase1_pin_source.py --config configs/experiment.yaml
python scripts/phase1_census.py && python scripts/phase1_pilot.py && python scripts/phase1_preregister.py --check-gate g1
python scripts/phase2_extract.py && python scripts/phase2_compile.py && python scripts/phase2_touch.py && python scripts/phase2_eligibility.py && python scripts/phase2_controlled_panel.py
python scripts/run_pc_tau.py --check-gate g2
python scripts/phase3_exact.py --run-id <id> && python scripts/phase3_crosscheck.py --run-id <id> && python scripts/phase3_agents.py --run-id <id> && python scripts/phase3_metrics.py --run-id <id> && python scripts/phase3_controls.py --run-id <id>
python scripts/phase4_corrupt.py --run-id <id> && python scripts/phase4_refactor.py --run-id <id> && python scripts/run_audit.py --run-id <id> && python scripts/phase4_verify_claims.py --run-id <id> && python scripts/phase4_seal.py --run-id <id> --check-gate g4
pytest -q
python scripts/run_pc_tau.py --reproduce <id>   # clean-checkout one-command path
python scripts/clean_run.py --run-id <unsealed-id>  # only deleter; refuses sealed IDs
```
