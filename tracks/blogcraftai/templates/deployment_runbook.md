# Deployment Runbook – BlogCraftAI

## Pre-Deploy Checklist
- [ ] Confirm CI pipeline green on target commit.
- [ ] Review release notes and migration list.
- [ ] Validate feature flags default safe state.
- [ ] Ensure database backups completed within last 24 hours.

## Deployment Steps
1. Trigger GitHub Actions workflow `deploy-staging`.
2. Monitor build logs; verify container pushed to GHCR.
3. Run Render deploy hook; wait for health checks to pass.
4. Execute database migrations using Render shell: `python manage.py migrate`.
5. Seed feature toggles and default roles.
6. Smoke test critical endpoints `/healthz`, `/api/posts/`, `/editor/`.

## Post-Deploy Verification
- [ ] Run Playwright smoke suite (`pnpm test:e2e --config smoke.config.ts`).
- [ ] Execute Lighthouse CI against staging base URL.
- [ ] Check Grafana dashboard for error spikes and latency.
- [ ] Announce deployment completion in #launches channel.

## Rollback Procedure
- Trigger GitHub Actions workflow `rollback-staging` with previous release tag.
- Restore database from point-in-time backup if schema-breaking change occurred.
- Update status page and notify stakeholders.

