# WorkPlan_LLM1.md — Real Learned-Agent Follow-on (reserved run pctau-20260906-672227c-llm1)

Parent: pctau-20260906-672227c, SEALED with reasons []. This is a new, separately preregistered experiment, not a parent phase. Sole purpose: answer whether actual trained tool-using models interact with the frozen PC resource geometry. Result-neutral: positive, null, boring or failed outcomes all valid. No tuning toward any outcome at any point.

Parent reconstruction (verified from the sealed repo before writing this plan): PC-TAU proved exact 8-cell freezing over 135 constructed Track-N tasks (135/135 FINITE_POSITIVE, K=[1,1,2,1,INF,1,INF,INF], delta_R 1) plus a 32-task controlled panel, with 5,436 paired probe episodes. It did not prove native multi-route realization (SG-B: 1 shared topology, 3 mechanism families), natural PARTIAL ambiguity (5 PARTIALs are control-induced), or anything about learned models (LM-C: trajectories are scripted probes). Phase 4 sealed 3 constructed claims; learned-agent and native predicates stay false. LLM1 may answer only the fixed-geometry behavior question. It cannot promote SG-B to SG-A.

## L1 — Inheritance, Secret Lock, Calibration, Model/Provider Lock, Budget, Preregistration

Exit LLM1_PREREGISTERED or STOP. Firewall: no scientific-population model calls; calibration only on permanently excluded pilot tasks.

Files:
```text
llm1/implementation_assistance.json
llm1/parent_inheritance_manifest.json
llm1/preregistration/calibration_protocol.json
llm1/preregistration/model_candidates.json
llm1/preregistration/model_roster.json
llm1/preregistration/provider_lock.json
llm1/preregistration/openrouter_price_snapshot.json
llm1/preregistration/token_calibration.json
llm1/preregistration/episode_count.json
llm1/preregistration/full_run_cost_projection.json
llm1/preregistration/interaction_budget.json
llm1/preregistration/population_rule.json
llm1/preregistration/execution_schedule.json
llm1/preregistration/retry_policy.json
llm1/preregistration/live_protocol.json
llm1/preregistration/primary_estimand.json
llm1/preregistration/claim_predicates.json
llm1/preregistration/nonclaims.json
llm1/configs/live_models.yaml
.env (local only, never tracked) + .env.example (key name only)
llm1/LLM1_PREREGISTERED
```

Code: `scripts/llm1_inherit.py` (hash-verify parent seal/pointer/bundle/population/contracts/repairs/touch/exact/bundles/metrics/tools; write inheritance manifest; STOP on mismatch), `scripts/llm1_calibrate.py` (excluded-pilot episodes only; records auth/transport/tokens/cost, never success metrics for selection), `scripts/llm1_discover.py` (live catalog query; slug/availability/tool-support/pricing/limits per candidate), `scripts/llm1_budget.py` (episode math, worst-case compiler with no cache savings, fair caps from calibration p95, roster fit vs $18.50), `scripts/llm1_preregister.py` (--check-gate llm1_l1: hashes valid, secrets safe per §6 scans, no scientific calls yet, prices live, roster/provider/prompts/tools/budget/population/schedule/retry/estimand/claims frozen, worktree clean except ignored secrets).
Calibration set (frozen): first 2 sorted IDs per domain from the excluded pilot set → airline:1, airline:11, retail:17, retail:29; 4 tasks x 4 freezes x 1 repeat = 16 episodes per candidate, non-scientific.
Episode math: (135 + 16) x 4 x 3 = 1,812 per model. Budget envelope: calibration $0.50, scientific $18.50, retry $0.50, reserve $0.50; hard cap $20.00, external ceiling $21.00. Roster: 3 heterogeneous families preferred over FULL population each; 4th only if worst-case fits; 2 acceptable; 1 marks SINGLE_MODEL_LIMITED. Primary contrast F000 vs F010 (kappa 1 vs 2, both finite); endpoints ordered: governance-correct completion, repair regret, excess escalation, finite-fallback discovery, then discovery/optimal/adaptation/unsafe. F100/F001 matched comparisons. Execution order frozen by fixed-seed hash over model/task/repeat/freeze preserving pairing. Pre-request kill switch before every send. Cost ledger append-only with provider-reported cost as truth. All 10 claim predicates init FALSE; permanent nonclaims carried over.

Tests `tests/llm1/`: parent seal/hash inheritance, pilot exclusion, population/freeze/tool identity, 6 secret scans (ignored/untracked/example-clean/no-tracked/no-results/no-bundle secret + redaction), preregistration ordering/timing (first scientific request after prereg commit), all-false init, frozen schedule/roster/provider/population/prompt hashes, episode math, live prices, reasoning counted, worst-case fit, fair envelope, no cache savings, multi-turn accounting, unresolved-transport reserve, overspend block, drift fail-closed, cost reconciliation, total <= $20.

## L2 — Real Learned-Model Inference

Exit LIVE_INFERENCE_COMPLETE or INVALID. Every scientific trajectory originates from an actual OpenRouter provider response; scripted/mock/copied/cached/hand-written/replayed turns forbidden. Per model x task x freeze x repeat: frozen bundle, condition, tools, common protocol, cost guard, real send, raw archive BEFORE scoring, runtime-processed tool loop until terminal/escalation/refusal/limits, full raw episode retained with hashes, provider IDs, token/cost fields. Transport-only retries under the frozen rule with linked attempts; one resolved trajectory per logical key. 1,812 accounted episodes per model, no filtering of refusals/failures/budget stops. Files: llm1/raw/api_requests.jsonl, api_responses.jsonl, episodes.jsonl, cost_ledger.jsonl, transport_attempts.jsonl, llm1/trajectories.parquet, llm1/paired_runs.parquet.

## L3 — Metric Reconstruction and Paired Behavioral Analysis

Exit LIVE_MEASURED or INVALID. After inference only: 8 metrics (governance-correct, regret, excess escalation, finite-fallback discovery, discovery, optimal rate, adaptation, unsafe) scored against exact parent K_Pi with inherited definitions. Pairing task/model/repeat with freeze as intervention; primary F000 vs F010; F100/F001 matched; models/domains/tracks/repeats reported separately, never one accuracy number. Task-context bootstrap CIs labeled as context variation under shared mechanism, never prevalence. All nulls/failures retained. Files: llm1/metrics.parquet, llm1/reports/model_results.md, freeze_effects.md, cost_report.md.

## L4 — Independent Audit, Falsification, Claims, Seal

Exit LLM1_SEALED or INVALID. Independent package rebuilds all 20 listed items (inheritance, population, roster, provider, prices, budget, hashes, schedule, provenance, identities, parsing, ordering, terminals, tokens, costs, pairing, metrics, statistics, predicates) with disagree-capable code. Corruption families A-X (scripted-trajectory swap, mock, duplicate IDs/keys, provider/slug/freeze/call/result changes, episode deletion incl. budget stops, E/R/A and K_Pi leaks, contract/population/schedule changes, unevidenced flips, cost tampering, overspend block, .env/header in bundle, silent fallback, price drift, retry-ledger edits) must all fail closed. Cost audit reconciles to raw responses with total <= $20. Deterministic replay from archived raws; live re-inference explicitly a replication. Predicates flip only on machine-checkable evidence (list of 10, all false init; replication needs >=2 families). Files: llm1/audit/* (independent_metrics, independent_costs, provider/provenance verification, corruption_results, audit.json), llm1/claim_ledger.json, llm1/artifact_graph.json, llm1/phase_manifest.json, llm1/REPRODUCE.md, llm1/reports/LLM1_CLAIMS.md, deterministic bundle + pointer, llm1/LLM1_SEALED.

## Traceability and gates

Parent sections map: SG-B/LM-C/135-vs-3/PARTIAL/probe findings → L1 inheritance checks; K=[1,1,2,1,INF,1,INF,INF] → primary contrast; Authorization B locks → claim predicates; follow-on ID reserved → this plan. Gate commands mirror the parent dispatcher with llm1_ prefix. Any post-observation redesign forces a new invalidated attempt, never a silent patch.
