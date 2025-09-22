# AI Agents & Automation Track

The AI Agents branch introduces orchestration platforms such as n8n and Make.com to automate BlogCraftAI workflows—content ingestion, publication, notifications, and monitoring. Learners design resilient, auditable automations that integrate with the Django backend, AI services, and third-party tools.

## Learning Outcomes

1. Compare automation platforms (n8n, Make.com, Zapier) and select the appropriate tool for use cases.
2. Design secure workflows handling authentication, secrets, and governance.
3. Integrate BlogCraftAI APIs with external services (CMS, Slack, Analytics) via webhooks.
4. Implement error handling, retries, compensation logic, and audit logging within automations.
5. Deploy and monitor automation infrastructure with version control and CI/CD.
6. Build automated test harnesses simulating upstream/downstream failures.

## Prerequisites

- Familiarity with REST APIs, webhooks, and JSON payloads.
- Completion of Django and Prompt Engineering tracks for context on core services.
- Basic understanding of containerization (Docker) and networking.

## Documentation Map

| File | Description |
| --- | --- |
| `curriculum.md` | Agenda covering platform evaluation, workflow design, deployment. |
| `resources.md` | Tooling list, integration references, security guidance. |
| `assessments.md` | Automation QA plan, failure simulation requirements, and governance checklist. |
| `templates/` | Workflow specification template, RACI chart, runbook. |

## Facilitation Notes

- Encourage cross-functional participation (Engineering, Content Ops, Legal).
- Run scenario-based drills to test escalation paths and audit requirements.
- Emphasize maintainability: version-controlled workflow definitions and code reviews.

