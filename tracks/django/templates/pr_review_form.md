# Pull Request Review Form – Django Branch

## Summary Validation
- [ ] Problem statement and solution summary completed.
- [ ] Linked issue / user story referenced.

## Code Quality
- [ ] Tests demonstrate new behaviour (unit + integration).
- [ ] `mypy`, `ruff`, and `black` formatting confirmed in CI logs.
- [ ] No direct database queries in views; use services/repositories.

## Security & Compliance
- [ ] JWT scopes validated, new endpoints documented in RBAC matrix.
- [ ] Secrets remain in environment variables; no plaintext credentials committed.
- [ ] Audit trail coverage updated for sensitive actions.

## Documentation
- [ ] README, ADRs, and runbooks updated.
- [ ] OpenAPI schema regenerated and versioned.

## Rollout
- [ ] Feature flags default safe-off in production.
- [ ] Migration/rollback strategy described.
- [ ] Monitoring dashboards updated with new metrics.

Reviewer Signature: ______________________

