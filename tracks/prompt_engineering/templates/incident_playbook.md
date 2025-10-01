# AI Suggestion Service Incident Playbook

## Trigger
Describe alert condition (e.g., timeout rate > 5%, guardrail violations surge).

## Immediate Actions
1. Acknowledge alert in PagerDuty / OpsGenie.
2. Inform channel #ai-ops with incident commander + scribe.
3. Enable fallback model and throttle new feature usage if necessary.

## Investigation Checklist
- [ ] Review inference service logs and GPU metrics.
- [ ] Inspect queue depth and request latency histograms.
- [ ] Validate upstream dependencies (database, Redis, external APIs).
- [ ] Run smoke test against `/api/ai/suggest` health endpoint.

## Mitigation Options
- Redeploy previous stable model checkpoint.
- Increase replicas and GPU memory allocations.
- Disable optional features (outline suggestions) to reduce load.
- Trigger circuit breaker to reject new requests with friendly message.

## Post-Incident
- Conduct RCA within 24 hours, document timeline, contributing factors, corrective actions.
- Update guardrails, prompts, or infrastructure settings accordingly.
- Schedule regression tests to verify issue resolution.

