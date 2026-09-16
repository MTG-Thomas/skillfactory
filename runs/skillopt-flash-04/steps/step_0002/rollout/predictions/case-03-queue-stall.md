**Incident: worker-3 queue stall / poison message loop — 2026-09-05**

**Summary:** On 2026-09-05, worker-3’s queue depth grew from 0 to 40,000 messages between 02:10 UTC and 06:40 UTC. The visible failure was a consumer restart loop; the root cause was unbounded retry of an 8 MB poison message with no dead-letter routing and no payload guard. Service was restored by manually draining the poison message to DLQ; queue depth recovered by 07:15 UTC.

**Impact:** Production message processing on worker-3 stalled for about 4.5 hours, producing a 40k-message backlog. Work items remained queued; no user data loss was reported.

**Timeline (UTC):**
- 02:10: Queue depth began increasing on worker-3.
- 02:10–06:40: Consumer restart loop continued as the 8 MB poison message was retried without backoff and OOM-killed the consumer each pass.
- 04:05: Queue-depth alert fired, about 2 hours after growth started.
- 06:40: Poison message manually drained to DLQ; backlog began recovering.
- 07:15: Queue depth fully recovered.

**Root Cause:** The poison message exceeded the consumer’s usable memory. There was no max-payload guard to reject it early, no DLQ to absorb the failed message, and retry was configured as unlimited. The same message was redelivered immediately after each OOM kill, causing the consumer restart loop and preventing queue drain. The restart loop was the first broken workflow; the root cause was the combination of missing payload guard, unlimited retry, and no dead-letter routing.

**Detection Gap:** The queue-depth alert fired late and provided no visibility into repeated message-level failures. There was no poison-message counter or consumer-restart alert to signal the delivery loop until the backlog had grown large.

**Corrective Actions:**
- Completed: Manually drained the poison message to DLQ and recovered queue depth (OPS-209).
- Pending: Add a max-payload guard so oversized messages are rejected before processing.
- Pending: Configure automatic DLQ routing for messages exceeding a delivery limit.
- Pending: Add a poison-message counter / consumer-restart alert for near-real-time detection of repeated failures.
- Deferred: None formally deferred. Revisit queue-depth alert threshold/timing after the direct poison-message alert is in place.

**Lessons:**
- Unlimited retry without a DLQ turns a single oversized message into a service outage.
- Monitor delivery-failure counters at the message level, not only aggregate queue depth.
- Validate payload size at the consumer boundary before OOM is possible.