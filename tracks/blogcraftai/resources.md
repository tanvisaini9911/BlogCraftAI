# BlogCraftAI Integrated Resources

## Stack Overview

| Layer | Technology | Notes |
| --- | --- | --- |
| Backend | Python 3.11, Django 5, DRF | Structured modular apps, typed services |
| Database | PostgreSQL 15 (pgvector extension) | Primary store for content & embeddings |
| Cache/Queue | Redis 7 | Caching, Celery broker, rate limiting |
| Frontend | Django Templates, HTMX, Bootstrap 5 | Server-driven UI with progressive enhancement |
| AI | Hugging Face Transformers (Mistral-7B/Llama 3), sentence-transformers | Suggestion + recommendation engines |
| Ops | Render.com, Gunicorn, WhiteNoise, GitHub Actions | Deployment + static asset serving |
| Testing | pytest, Playwright, Lighthouse CI, drf-spectacular | Automated quality gates |

## Infrastructure Diagram (textual)

```
[Client]
   | HTTPS (Cloudflare optional)
[Render Load Balancer]
   |--> [Gunicorn + Django App Container]
         |--> [PostgreSQL Database (Managed)]
         |--> [Redis Cache]
         |--> [AI Inference Service (TGI) -> GPU Node]
         |--> [Background Workers (Celery)]
         |--> [Static Assets via WhiteNoise]
         |--> [Observability Stack: Prometheus -> Grafana, Sentry]
```

## Environment Configuration

- `.env` variants: `local`, `staging`, `production`; managed via Doppler/1Password.
- Secrets: `DJANGO_SECRET_KEY`, `DATABASE_URL`, `REDIS_URL`, `HF_TOKEN`, `SENTRY_DSN`, `RENDER_SERVICE_ID`.
- Feature flags: LaunchDarkly or `django-waffle` to gate AI features, editor enhancements, experimental flows.

## Deployment Pipeline

1. **CI Stage** – Lint (`ruff`, `black`), type check (`mypy`), tests (`pytest`, `playwright`), docs (`mkdocs build`).
2. **Build Stage** – Container image via GitHub Actions, push to GHCR.
3. **Deploy Stage** – Render.com deploy hook triggered; migrations run via release command.
4. **Post-Deploy** – Smoke tests, Lighthouse run, synthetic monitoring update.

## Observability & SLOs

- **Availability SLO:** 99.5% monthly uptime for core app, 99% for AI endpoint.
- **Latency SLO:** P95 < 400ms for CRUD APIs, P95 < 1.5s for AI suggestions.
- **Error Budget:** 0.5% downtime/month; track via SLO dashboard.
- **Telemetry:** OpenTelemetry traces -> OTLP collector -> Grafana Cloud/Tempo.

## Compliance & Security

- Enforce HTTPS everywhere; HSTS preloading.
- Content Security Policy restricting script sources to self + hashed inline.
- Database encryption at rest + rotated credentials.
- Secrets scanning via GitHub Advanced Security + pre-commit `detect-secrets`.

## Documentation References

- ADR template in `/templates/` for architectural decisions.
- Runbooks for incidents, release process, and database maintenance.
- API documentation generated using `drf-spectacular` served at `/api/schema/` & `/docs/`.

