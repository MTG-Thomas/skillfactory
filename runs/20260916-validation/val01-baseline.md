Incident: Docs deploy preview 404 for /guides/* routes
Date: 2026-08-28 11:05-12:30 EDT
Impact: All /guides/* routes returned 404 in deploy preview.
Cause: Base-path change in vite.config without updating preview rewrite rules.
Detection: Reviewer click-through. No link-check in CI.
Mitigation: Fixed rewrite rules and redeployed at 12:30 EDT.
Follow-up: Add preview link-check job. Status pending.