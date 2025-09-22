# BlogCraftAI Learning Paths

BlogCraftAI is a structured training program that guides learners from non-technical onboarding to delivering a production-ready AI-assisted blogging platform. The repository now hosts full curricula, resources, and quality gates for every planned branch, enabling teams to execute specialization tracks sequentially or in parallel.

## Repository Structure

- `curriculum/non_technical_starter.md` – 30-hour facilitator-ready agenda for non-technical participants.
- `resources/` – Shared resource library used across tracks.
- `roadmap/branch_blueprints.md` – High-level scope documents summarizing each technical branch.
- `templates/` – Business and planning templates reused by facilitators.
- `tracks/` – Dedicated documentation packages for each technical branch (Django, Prompt Engineering, Frontend, BlogCraftAI, AI Agents).
- `tests/` – Testing strategy overview and links to branch-specific quality plans.

## Track Overview

### Main Branch – Non-Technical Starter
- Focus: Product vision, stakeholder alignment, and content operations fundamentals.
- Outcome: Participants craft learning plans and understand how each technical branch contributes to the platform.
- Key Assets: [Agenda](curriculum/non_technical_starter.md), [Resource kits](resources/), facilitator checklists.

### Django Backend Track (`tracks/django`)
- Focus: Project scaffolding (`accounts`, `blog`, `api`), PostgreSQL integration, JWT auth, CRUD APIs with permissions.
- Outcome: Production-ready Django services with 90%+ automated test coverage and deployment pipelines.
- Key Assets: [Curriculum](tracks/django/curriculum.md), [Resources](tracks/django/resources.md), [Assessments](tracks/django/assessments.md), [Templates](tracks/django/templates/).

### Prompt Engineering Track (`tracks/prompt_engineering`)
- Focus: Prompt design fundamentals, schema validation, guardrails, and `/api/ai/suggest` implementation with Hugging Face models.
- Outcome: Safe, observable AI suggestion service that handles retries, forbidden terms, and latency SLAs.
- Key Assets: [Curriculum](tracks/prompt_engineering/curriculum.md), [Resources](tracks/prompt_engineering/resources.md), [Assessments](tracks/prompt_engineering/assessments.md), [Templates](tracks/prompt_engineering/templates/).

### Frontend Experience Track (`tracks/frontend`)
- Focus: Accessible Django Template frontend with Bootstrap 5 and HTMX, covering authentication, post list/detail, comments, editor with “Suggest SEO”.
- Outcome: Responsive UI meeting Lighthouse 90+ benchmarks with comprehensive component, accessibility, and e2e tests.
- Key Assets: [Curriculum](tracks/frontend/curriculum.md), [Resources](tracks/frontend/resources.md), [Assessments](tracks/frontend/assessments.md), [Templates](tracks/frontend/templates/).

### BlogCraftAI Full-Stack Track (`tracks/blogcraftai`)
- Focus: Integrating backend, frontend, AI, and ops into the full production platform (Django 5, DRF, PostgreSQL, HTMX, Render.com).
- Outcome: Deployment-ready BlogCraftAI application with SLO monitoring, runbooks, and governance artifacts.
- Key Assets: [Curriculum](tracks/blogcraftai/curriculum.md), [Resources](tracks/blogcraftai/resources.md), [Assessments](tracks/blogcraftai/assessments.md), [Templates](tracks/blogcraftai/templates/).

### AI Agents Track (`tracks/ai_agents`)
- Focus: n8n/Make.com automations connecting BlogCraftAI with external systems, including governance and failure simulations.
- Outcome: Auditable automation workflows with CI/CD, monitoring, and compliance documentation.
- Key Assets: [Curriculum](tracks/ai_agents/curriculum.md), [Resources](tracks/ai_agents/resources.md), [Assessments](tracks/ai_agents/assessments.md), [Templates](tracks/ai_agents/templates/).

## Required Resources by Track

| Track | Core Tooling |
| --- | --- |
| Non-Technical Starter | Collaboration suite (Miro, Docs), sample personas, analytics snapshots |
| Django | Python 3.11, Django 5, DRF, PostgreSQL, Redis, pytest, GitHub Actions |
| Prompt Engineering | Hugging Face models, transformers, guardrails, httpx/tenacity, monitoring stack |
| Frontend | Django Templates, Bootstrap 5, HTMX, Vite, Jest, Playwright, Lighthouse |
| BlogCraftAI | Full integrated stack + Render.com, Gunicorn, WhiteNoise, OpenTelemetry |
| AI Agents | n8n/Make.com, Vault, automation testing harness, workflow repositories |

## Getting Started

1. Choose the track that aligns with your team’s readiness.
2. Review the corresponding curriculum and resources within `tracks/`.
3. Prepare environments and tooling outlined in each track’s resource guide.
4. Follow assessment guides to ensure quality gates are met before graduation.
5. Update this README with additional outcomes as new cohorts complete the tracks.

## Testing & Quality Expectations

- Each track includes an `assessments.md` file detailing required automated tests, failure simulations, and acceptance criteria.
- The [tests directory](tests/README.md) describes how to organize branch-specific test suites once code is implemented.
- Maintain 90%+ coverage across critical services, enforce linting, and document deviations via ADRs.

## License

This project is licensed under the [MIT License](LICENSE).
