# Case 03 — Worker queue stall (poison message loop)

## Input (evidence)
- Queue depth grew 0 -> 40k msgs 2026-09-05 02:10-06:40 UTC on worker-3.
- Symptom: consumer restart loop; poison message with 8 MB payload retried without backoff, OOM-killed each pass.
- Cause chain: no max-payload guard, no dead-letter routing, retry=unlimited.
- Detection: queue-depth alert fired 04:05 UTC (2h late); no poison-message counter.
- Mitigation: drained poison msg to DLQ 06:40 UTC, depth recovered by 07:15 UTC.
- Pending: payload limit, DLQ auto-route, poison counter alert. Completed: manual drain OPS-209.

## Task
Same shape contract. Distinguish first broken workflow (restarts) from root cause
(unbounded retry + no DLQ). Corrective actions must split completed/pending/deferred.
