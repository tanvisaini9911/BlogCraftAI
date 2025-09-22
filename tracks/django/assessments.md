# Django Track Assessments & Quality Gates

## Module Checkpoints

1. **Environment Validation**
   - `poetry install` + `poetry run pytest` succeed on fresh clone.
   - Docker Compose stack launches without manual intervention.
   - Health check endpoint returns 200 within 30 seconds of startup.
2. **Domain Modeling Review**
   - Models adhere to naming conventions, include audit timestamps, and implement business rules in `clean()`.
   - Database schema reviewed via generated ER diagram and migration diff.
3. **API Readiness**
   - CRUD endpoints pass contract tests derived from OpenAPI schema.
   - Permissions matrix validated via automated tests (admin/editor/contributor/reader roles).
4. **Security Hardening**
   - JWT tokens configured with rotation, refresh token blacklisting, and short-lived access tokens.
   - OWASP ASVS checklist reviewed; medium/high findings resolved.
5. **Operational Excellence**
   - Logging, tracing, and metrics integrated with Sentry/Grafana.
   - Runbook drafted for database failover and token revocation incidents.

## Automated Test Suite Requirements

| Layer | Tooling | Coverage Expectations | Failure Scenarios |
| --- | --- | --- | --- |
| Unit | `pytest`, `pytest-mock`, `factory_boy` | ≥ 95% for models, serializers, utils | Validation errors, slug collisions, permission denial |
| Integration | `pytest-django`, Docker Compose services | ≥ 85% of API pathways | Database outage, Redis unavailability, external email provider timeout |
| Contract | `schemathesis`, `pytest` | 100% endpoints enforced | Schema drift, missing fields, invalid status codes |
| Performance | `locust` or `k6` | P95 < 300ms for CRUD endpoints | Load spike, concurrent comment creation |
| Security | `bandit`, `safety`, OWASP ZAP baseline | Zero high severity findings | XSS attempt via comments, CSRF bypass |

### Example Test Matrix (abbreviated)

```python
class TestPostApiPermissions:
    def test_editor_can_publish(self, api_client, editor_user, draft_post):
        response = api_client.post("/api/posts/{id}/publish/".format(id=draft_post.id))
        assert response.status_code == 200
        assert response.json()["status"] == "published"

    def test_reader_cannot_create(self, api_client, reader_user, post_payload):
        response = api_client.post("/api/posts/", post_payload)
        assert response.status_code == 403

class TestCommentModerationWorkflow:
    def test_comment_queue_drains_on_retry(self, celery_app, comment_factory):
        # simulate transient error on first try
        with patch("comments.tasks.publish_comment") as publish_comment:
            publish_comment.side_effect = [TimeoutError(), None]
            task_id = enqueue_comment(comment_factory())
            result = AsyncResult(task_id)
        assert result.state == states.SUCCESS
```

## Capstone Project Rubric

| Dimension | Exceeds Expectations | Meets Expectations | Needs Improvement |
| --- | --- | --- | --- |
| Architecture | Modular apps, domain services, dependency inversion | Django apps with clear separation of concerns | Monolithic views, duplicated logic |
| Security | Implements MFA, audit logging, proactive anomaly detection | JWT auth with rotation and blacklisting | Plain-session auth, missing validations |
| Documentation | ADRs, ER diagrams, runbooks, API changelog | README, OpenAPI schema, setup docs | Missing setup steps or API docs |
| Testing | CI-enforced coverage > 90%, chaos scripts integrated | Unit + integration tests with coverage report | Sparse or failing tests |
| Delivery | Automated deploy to staging, rollback tested | Manual deploy instructions validated | No deployment path |

## Peer Review Checklist

- [ ] Pull request adheres to template, includes screenshots/logs of passing pipelines.
- [ ] Code follows black/isort formatting and mypy static typing (where applicable).
- [ ] Secrets managed via `.env` and never committed.
- [ ] Database migrations reviewed, reversible, and idempotent.
- [ ] Observability instrumentation meets agreed SLOs.

