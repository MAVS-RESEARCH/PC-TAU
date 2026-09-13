# LLM1 sealed claims (evidence-derived predicates)

- Actual trained models were evaluated through provider-verified live inference under the sealed PC-TAU resource interventions.
  Evidence: 5,436 unique provider-verified trajectories
- All 5,436 scheduled episodes are accounted for with genuine provider responses.
  Evidence: schedule exhausted with linked retries
- Paired freeze interventions were measured with task, model, repeat and bundle held fixed.
  Evidence: pairing quartets complete per task/model/repeat
- Removal of the R-touching optimal repair altered learned-agent behavior under finite fallback.
  Evidence: llm1/metrics.parquet paired F000/F010 contrasts
- Learned agents discovered the finite fallback route under the R freeze.
  Evidence: llm1/metrics.parquet paired F000/F010 contrasts
- Learned agents adapted imperfectly: excess cost or escalation relative to the exact oracle.
  Evidence: llm1/metrics.parquet paired F000/F010 contrasts
- The primary freeze effect replicated across independently evaluated model families.
  Evidence: llm1/metrics.parquet paired F000/F010 contrasts
- Model families differed in freeze response.
  Evidence: llm1/metrics.parquet paired F000/F010 contrasts
- Open-state submit attempts were observed and blocked with zero unauthorized executions.
  Evidence: 262 blocked open-state attempts, zero executed
- All roster models executed the common semantic protocol without incompatibility.
  Evidence: 3/3 models completed protocol with zero incompatibilities
