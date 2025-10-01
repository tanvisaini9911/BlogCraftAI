# BlogCraftAI

BlogCraftAI is a teaching-ready reference implementation that mirrors the 30-hour training program outlined in the curriculum. It provides a production-grade Django stack with AI integrations, responsive templates, automation samples, and exhaustive tests so that learners can explore every branch with confidence.

## Table of Contents
- [Feature Overview](#feature-overview)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Use Case Outcomes](#use-case-outcomes)
- [Key API Endpoints](#key-api-endpoints)
- [AI Prompt Engineering Toolkit](#ai-prompt-engineering-toolkit)
- [Automation Blueprints](#automation-blueprints)
- [Testing Strategy](#testing-strategy)

## Feature Overview
| Branch | Highlights |
| --- | --- |
| Main | Onboarding template, resource checklist, communication guidelines. |
| Django | Modular project (`accounts`, `blog`, `ai`), PostgreSQL-ready config, JWT auth, audited logging. |
| Prompt Engineering | `AiSuggestionService` with structured prompts, timeout handling, schema validation, unit tests. |
| Frontend | Responsive Django templates, accessibility support, SEO insights panel, pagination, dashboards. |
| BlogCraftAI | Unified architecture diagram, environment configuration, observability hooks, deployment-ready static handling. |
| AI Agents | n8n and Make.com automation JSON blueprints for editorial workflows. |

## Architecture
- **Backend:** Django 5 + Django REST Framework powering authentication, blog CRUD, and AI endpoints. Custom user model enforces email logins and profile metadata.
- **Database:** Ships with SQLite for local development and environment-driven PostgreSQL configuration for staging/production.
- **Frontend:** Server-rendered templates styled with a responsive utility sheet. Components are WCAG-conscious, keyboard navigable, and optimised for Lighthouse/PageSpeed budgets.
- **AI Layer:** `AiSuggestionService` encapsulates prompt engineering contracts, input validation, resilience strategies, and JSON parsing into `SeoSuggestion` dataclasses.
- **Automation:** Reusable workflow definitions demonstrate how to orchestrate BlogCraftAI APIs from n8n and Make.com for scheduling, enrichment, and notifications.

## Getting Started
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Apply migrations**
   ```bash
   cd backend
   python manage.py migrate
   ```
3. **Create a superuser (optional but recommended)**
   ```bash
   python manage.py createsuperuser
   ```
4. **Run the development server**
   ```bash
   python manage.py runserver
   ```
5. **Access the app** at `http://127.0.0.1:8000/`

Environment variables such as `POSTGRES_DB`, `AI_PROVIDER_URL`, and JWT lifetimes can be configured via the shell or a `.env` file to align with deployment targets.

## Use Case Outcomes
- ✅ Learners can register, authenticate via JWT, and manage their profile through the `/accounts` endpoints and UI flows.
- ✅ Editors create, publish, edit, and archive posts with tag management, reaction tracking, and permissioned API access.
- ✅ Visitors browse, search, and filter posts, while responsive templates guarantee accessible navigation and descriptive SEO metadata.
- ✅ AI-assisted SEO suggestions surface on post detail pages and through the `/api/seo-suggestions/` endpoint with graceful degradation on provider errors.
- ✅ Automation teams can plug BlogCraftAI into scheduling systems using the provided n8n and Make.com workflow blueprints.

## Key API Endpoints
| Endpoint | Method | Description |
| --- | --- | --- |
| `/accounts/register/` | POST | Create a new user account. |
| `/accounts/token/` | POST | Obtain JWT access and refresh tokens. |
| `/accounts/profile/` | GET/PATCH | Retrieve or update the authenticated user profile. |
| `/api/posts/` | GET/POST | List or create blog posts (supports filtering, search, ordering). |
| `/api/posts/{slug}/publish/` | POST | Publish a draft post (author/staff only). |
| `/api/comments/` | POST | Add a public comment to a post. |
| `/api/reactions/` | POST | Upsert user reactions (like/dislike) on posts. |
| `/api/seo-suggestions/` | POST | Generate AI SEO suggestions for content drafts. |

Authenticated requests use Bearer tokens issued by SimpleJWT. Throttling, pagination, and filtering follow DRF conventions to stay predictable for learners.

## AI Prompt Engineering Toolkit
- `backend/ai/services.py` encodes the guardrails, schema validation, retry-safe HTTP access, and structured responses required to integrate large language models responsibly.
- `backend/ai/prompts/seo_optimization.md` documents the canonical prompt, guardrails, and testing checklist used in class to critique prompt design decisions.
- Comprehensive tests in `backend/tests/test_ai_service.py` simulate success, timeout, and malformed payload scenarios to encourage defensive programming.

## Automation Blueprints
- `automations/n8n_content_publish.json` schedules daily reviews of draft posts, publishes approved entries, and sends Slack notifications.
- `automations/make_scenario_blueprint.json` shows how to receive Airtable briefs, seed drafts, request AI suggestions, and push a Teams update—all without writing custom code.

## Testing Strategy
Run the full suite with:
```bash
pytest
```
The suite covers API contracts, permission boundaries, AI error handling, and HTML rendering smoke tests. Test fixtures rely on `factory_boy` for expressive setup and include negative as well as failure simulations (timeouts, validation errors).