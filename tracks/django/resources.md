# Django Track Resources & Tooling

## Core Toolchain

- **Python 3.11** – managed via `pyenv` + `poetry` for dependency locking.
- **PostgreSQL 15** – local development through Docker Compose with persistent volumes.
- **Redis 7** – optional cache and task broker, also provisioned in Docker Compose.
- **Django 5 / Django REST Framework 3.15** – backend foundation.
- **djangorestframework-simplejwt** – JWT authentication flows with refresh rotation.
- **Celery 5 + Redis** – asynchronous task processing for notifications and indexing.
- **pytest + coverage + pytest-django + pytest-factoryboy** – automated testing stack.
- **Sentry** – application monitoring and error tracking.
- **GitHub Actions** – CI/CD pipelines, vulnerability scans, and artifact storage.

## Reference Documentation

| Topic | Link |
| --- | --- |
| Django settings management | <https://docs.djangoproject.com/en/5.0/topics/settings/> |
| DRF viewsets & routers | <https://www.django-rest-framework.org/api-guide/viewsets/> |
| Simple JWT configuration | <https://django-rest-framework-simplejwt.readthedocs.io/en/latest/> |
| PostgreSQL performance tuning | <https://www.postgresql.org/docs/current/performance-tips.html> |
| Celery reliability patterns | <https://docs.celeryq.dev/en/stable/userguide/tasks.html> |
| drf-spectacular schema generation | <https://drf-spectacular.readthedocs.io/en/latest/> |
| GitHub Actions security hardening | <https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions> |

## Sample Configuration Snippets

### `docker-compose.yml`

```yaml
services:
  app:
    build: .
    command: poetry run python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    env_file: .env.local
    depends_on:
      - db
      - redis
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: blogcraftai
      POSTGRES_USER: blogcraftai
      POSTGRES_PASSWORD: changeme
    volumes:
      - postgres_data:/var/lib/postgresql/data
  redis:
    image: redis:7
volumes:
  postgres_data:
```

### `.env.local`

```bash
DJANGO_SETTINGS_MODULE=config.settings.local
DATABASE_URL=postgres://blogcraftai:changeme@db:5432/blogcraftai
REDIS_URL=redis://redis:6379/0
SECRET_KEY=generate-a-unique-secret
ALLOWED_HOSTS=localhost,127.0.0.1
SENTRY_DSN=
```

### `pyproject.toml` (excerpt)

```toml
[tool.poetry.dependencies]
python = "^3.11"
django = "^5.0"
djangorestframework = "^3.15"
djangorestframework-simplejwt = "^5.3"
psycopg[binary] = "^3.1"
celery = "^5.3"
redis = "^5.0"
```

## Suggested Reading Sequence

1. Complete the Django + DRF tutorials to refresh fundamentals.
2. Study the BlogCraftAI domain overview from the main branch to align on product context.
3. Review DevOps guidelines for Render.com to anticipate deployment constraints.
4. Practice writing schema-first serializers before implementing viewsets.
5. Revisit security best practices (OWASP Top 10) ahead of auth configuration.

## Collaboration Tools

- Shared ER diagram workspace (e.g., dbdiagram.io) for iterative modeling.
- Slack/Teams channel with GitHub integration for CI notifications.
- Confluence/Notion space to store runbooks, ADRs, and decisions.

