# Incident Note: Worker-3 Queue Stall Due to Poison Message Loop

## Summary

On `worker-3`, a poison message with an 8 MB payload caused a consumer restart loop from 02:10 UTC onward. The consumer was OOM-killed on each delivery attempt and the message was retried indefinitely with no backoff, causing the queue depth to grow from 0 to 40,000 messages. Service was restored by manually draining the poison message to the DLQ at 06:40 UTC; queue depth recovered by 07:15 UTC.

## Impact

- `worker-3` consumers were unavailable for the affected period.
- Queue backlog reached 40,000 messages.
- Dependent processing was delayed until the queue drained.
- No messages were lost.

## Timeline

All times UTC.

- **02:10** — Queue depth began growing on `worker-3`; poison message entered the queue and triggered OOM-killed consumer restarts.
- **04:05** — Queue-depth alert fired, ~2 hours after backlog growth started.
- **06:40** — Operator drained the poison message to the DLQ (OPS-209); restart loop stopped.
- **07:15** — Queue depth recovered to 0.

## Root Cause

The first visible broken workflow was the consumer restart loop, but the root cause was the retry architecture: `retry=unlimited`, no backoff, and no dead-letter routing. An oversized message with no max-payload guard reached the consumer, was OOM-killed on each attempt, and was then redelivered forever because there was no poison-message route or retry limit. This prevented the worker from processing the rest of the queue.

## Detection Gap

- The only health signal was queue depth, which fired 2 hours after the backlog began.
- There was no poison-message counter or alert for repeated consumer crashes / OOM-killed deliveries.
- There was no monitor for retry-loop behavior or oversized payloads.

## Corrective Actions

### Completed

- Manually drained the poison message to the DLQ and verified queue recovery (OPS-209).

### Pending

- Add a max-payload guard to reject/route oversized messages before consumer processing.
- Configure automatic dead-letter routing for messages that exceed retry limits.
- Add a poison-message counter alert to detect repeated failed deliveries.

### Deferred

- None.

## Lessons

- Unlimited retries without a DLQ turn a single bad message into an infinite failure loop.
- A consumer restart loop is a symptom; the underlying issue is often missing message-size validation, retry limits, or poison routing.
- Queue-depth alerts can be slow; direct poison-message/consumer-crash signals provide earlier detection.