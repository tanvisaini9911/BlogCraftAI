# Django Track Curriculum (40 Hours)

## Day 1 – Environment & Foundations (8h)

| Time | Topic | Format | Key Deliverables |
| --- | --- | --- | --- |
| 09:00 – 09:45 | Orientation, architecture overview, branching strategy | Lecture + Q&A | Shared understanding of branch goals and deliverables |
| 09:45 – 11:00 | Tooling setup: Python 3.11, Poetry/virtualenv, Docker, VS Code devcontainers | Guided Lab | Local dev environment with reproducible `Makefile` commands |
| 11:00 – 12:30 | Django project bootstrap (`blogcraftai`), settings modularization, `.env` handling | Live Coding | Repository scaffold with `config/settings/{base,local,staging,production}.py` |
| 13:30 – 14:30 | PostgreSQL integration, connection pooling, migrations workflow | Lecture + Demo | Connection strings managed via `.env`, `docker-compose` stack running |
| 14:30 – 16:00 | Creating core apps (`accounts`, `blog`, `api`), app registry, signals | Lab | Apps registered, `apps.py` instrumented with AppConfig patterns |
| 16:00 – 17:00 | Wrap-up, retrospective, parking lot review | Discussion | Updated backlog, risk log |

## Day 2 – Domain Modeling & Admin UX (8h)

| Time | Topic | Format | Key Deliverables |
| --- | --- | --- | --- |
| 09:00 – 10:30 | Domain modeling workshop (User, Post, Comment, Tag, AuditLog) | Collaborative Design | ER diagram, validation rules, cascade strategy |
| 10:30 – 12:00 | Implementing models, constraints, indexes, audit mixins | Pair Programming | Models with `clean()` methods, slug generation, soft delete fields |
| 13:00 – 14:15 | Migration authoring, data seeding, fixture strategy | Hands-on Lab | `loaddata` fixtures, management commands (`seed_demo_content`) |
| 14:15 – 15:30 | Django admin customization: list filters, inline comments, custom actions | Live Coding | Role-sensitive admin dashboards with search, analytics widgets |
| 15:30 – 17:00 | Observability: logging, Sentry, health check endpoints | Lab + Review | Structured logging config, `/healthz` endpoint, uptime dashboards |

## Day 3 – Authentication, Permissions & APIs (8h)

| Time | Topic | Format | Key Deliverables |
| --- | --- | --- | --- |
| 09:00 – 10:15 | JWT authentication deep dive (`djangorestframework-simplejwt`) | Lecture + Demo | Access/refresh tokens, rotation, blacklist enabled |
| 10:15 – 12:00 | Permissions, throttling, rate limits, audit trails | Lab | Custom permission classes, IP-based throttles, audit logging middleware |
| 13:00 – 14:30 | CRUD APIs for posts/comments, nested serializers, pagination | Live Coding | DRF viewsets with filtering, search, ordering |
| 14:30 – 15:30 | Async tasks for notifications (Celery or Django-Q) | Workshop | Task queue configured, `notify_subscribers` workflow |
| 15:30 – 17:00 | API documentation with `drf-spectacular`, schema linting, client generation | Lab | Published OpenAPI spec, client SDK stub |

## Day 4 – Quality Engineering & Resilience (8h)

| Time | Topic | Format | Key Deliverables |
| --- | --- | --- | --- |
| 09:00 – 10:30 | pytest architecture, fixtures, factories (Factory Boy), coverage gates | Lecture + Demo | `pytest.ini`, `conftest.py`, coverage >= 90% enforced |
| 10:30 – 12:00 | Unit tests for models, serializers, permissions | Pair Lab | Table-driven tests covering edge cases, property-based tests |
| 13:00 – 14:15 | Integration tests: database failover, API timeout simulations | Lab | Chaos scripts, patching with `responses` & `pytest-mock` |
| 14:15 – 15:30 | Contract tests with `schemathesis`, Postman/Newman pipelines | Hands-on | CI job executing contract suite on OpenAPI schema |
| 15:30 – 17:00 | Security testing: OWASP ZAP baseline scan, auth hardening checklist | Lab + Review | ZAP report triaged, security backlog prioritized |

## Day 5 – Deployment & Capstone Sprint (8h)

| Time | Topic | Format | Key Deliverables |
| --- | --- | --- | --- |
| 09:00 – 10:30 | CI/CD with GitHub Actions, reusable workflows, environment promotion | Lecture + Demo | Pipelines for lint/test/build/deploy, manual approval gates |
| 10:30 – 12:00 | Infrastructure as Code primer (Terraform/Ansible) for Render.com | Workshop | Render service manifests, secrets management guide |
| 13:00 – 14:30 | Capstone sprint: implement feature backlog (draft autosave API, moderation queue) | Team Lab | Feature branch PRs with passing pipelines |
| 14:30 – 15:30 | Performance profiling, query optimization, caching (Redis) | Lab | Identified N+1 queries resolved, caching metrics |
| 15:30 – 17:00 | Capstone demos, peer reviews, retrospective, next steps | Presentations | Demo recordings, peer feedback, action plan |

## Optional Extension Labs

- Multi-tenant support and organization-level RBAC.
- WebSockets/Server-Sent Events for live editing indicators.
- Blue/green deployments and database migration playbooks.

