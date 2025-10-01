# AI Agents Resources & Tooling

## Platforms & Deployment

- **n8n** – self-host via Docker or Render; supports JS function nodes for custom logic.
- **Make.com** – SaaS with advanced connectors; ensure data residency compliance.
- **Temporal / Prefect** – optional for code-first orchestrations requiring complex state.
- **PostgreSQL / Redis** – backing stores for workflow state and rate limiting.
- **HashiCorp Vault / Doppler** – centralized secrets management.

## Integrations

| Integration | Purpose | Notes |
| --- | --- | --- |
| BlogCraftAI REST API | Manage posts, comments, notifications | Use service accounts with scoped tokens |
| Slack / Teams | Editorial notifications, incident comms | Sign secrets to verify webhooks |
| Google Sheets / Airtable | Content calendar synchronization | Enforce schema validation before writes |
| Analytics (GA4, Plausible) | Publish performance summaries | Rate limit to avoid API quotas |
| CMS (WordPress, Ghost) | Cross-publishing to external sites | Monitor for duplicate publication |

## Security Practices

- Enforce least privilege credentials; rotate API keys quarterly.
- Store secrets using platform-provided vaults; avoid embedding in workflow JSON.
- Log every outbound call with correlation IDs for auditing.
- Implement IP allowlists and webhook signature verification.
- Regularly review platform audit logs and export to SIEM.

## Testing Toolkit

- **n8n CLI** – export/import workflows, run integration tests.
- **pytest** – simulate webhook events against local tunnel (ngrok, Cloudflare Tunnels).
- **Hoverfly / WireMock** – mock third-party APIs for failure testing.
- **k6** – load testing on webhook endpoints.
- **Chaos Mesh** – fault injection on Kubernetes-deployed automations.

## Workflow Repository Structure

```
automations/
  README.md
  workflows/
    content_ingest.json
    seo_alerts.json
  tests/
    test_content_ingest.py
    fixtures/
      rss_feed.xml
  docs/
    content_ingest_runbook.md
```

## Governance

- Establish Automation Review Board (ARB) for approvals.
- Maintain RACI chart for each workflow (Author, Reviewer, Operator, Stakeholder).
- Track data retention policies; purge logs containing PII after 30 days.
- Document compliance with regulations (GDPR, CCPA) when processing user data.

