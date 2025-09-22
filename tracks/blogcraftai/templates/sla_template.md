# Service Level Agreement Template

## Service Overview
- **Service:** BlogCraftAI Platform
- **Owner:** Platform Engineering
- **Customers:** Editorial team, Marketing, External readers

## Service Hours
- Production availability target: 24/7 with planned maintenance windows Sundays 02:00–04:00 UTC.

## SLOs
| Metric | Target | Measurement |
| --- | --- | --- |
| Availability | 99.5% monthly | Uptime robot + synthetic checks |
| API Latency | P95 < 400ms | Prometheus histogram `http_request_duration_seconds` |
| AI Suggest Latency | P95 < 1.5s | Custom metric `ai_suggest_duration_seconds` |
| Error Rate | < 1% 5xx responses | Prometheus counter |

## Incident Response
- Page on-call within 5 minutes of SEV-1 alert.
- Provide status update every 15 minutes until resolution.
- Conduct RCA within 48 hours; publish findings to knowledge base.

## Change Management
- Deployments via GitHub Actions with approval gates.
- All changes recorded in change log with rollback plan.
- Feature flags used to control risky releases.

## Reporting
- Weekly summary emailed to stakeholders with SLO burn-down, incidents, upcoming changes.
- Quarterly review meeting to adjust targets and resources.

