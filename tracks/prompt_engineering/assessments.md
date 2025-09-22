# Prompt Engineering Assessments & Quality Controls

## Iteration Checkpoints

1. **Prompt Design Review**
   - Provide at least three prompt templates (system/developer/user) with documented intent and guardrails.
   - Conduct bias audit using evaluation dataset; document mitigations.
2. **Model Evaluation**
   - Record latency, token usage, and quality scores across candidate models.
   - Select production model via decision matrix approved by peers.
3. **API Compliance**
   - `/api/ai/suggest` responses pass JSON schema validation and include `safety_flags` metadata.
   - Guardrails prevent submission of forbidden terms; violation attempts logged with correlation IDs.
4. **Observability Sign-off**
   - Dashboards covering latency, error rate, and guardrail triggers published.
   - Alerts configured for timeout rate > 5%, queue backlog > threshold, or safety flag spikes.
5. **Resilience Testing**
   - Replay suite covers network failures, model restart, GPU exhaustion, and fallback activation.

## Automated Testing Requirements

| Suite | Tooling | Focus | Target |
| --- | --- | --- | --- |
| Unit | `pytest`, `pytest-asyncio`, `unittest.mock` | Prompt formatters, schema validators, guardrail filters | 95% coverage |
| Integration | `respx` / `responses`, Docker Compose (model service) | End-to-end endpoint behaviour | 90% coverage |
| Adversarial | Custom dataset runner | Toxicity, prompt injection, forbidden terms | Zero leaks |
| Performance | `k6`, `locust`, `prometheus` | P95 < 1.5s, throughput 20 req/s | SLA compliance |
| Chaos | `pytest` + fault injection scripts | Timeouts, circuit breaker, fallback | Automatic recovery |

### Example Test Skeleton

```python
@pytest.mark.asyncio
async def test_retry_then_success(mock_inference_client, suggest_payload):
    mock_inference_client.generate.side_effect = [httpx.TimeoutException("boom"), {"title": "...", "meta_description": "...", "keywords": ["ai", "blog"]}]
    response = await suggest(suggest_payload)
    assert response.status == 200
    assert response.body["retry_count"] == 1

@pytest.mark.parametrize("forbidden_term", ["casino", "lottery"])
def test_guardrail_blocks_forbidden_terms(forbidden_term, suggest_payload):
    suggest_payload["draft"] += f" {forbidden_term}"
    with pytest.raises(ForbiddenTermError):
        guardrails.validate(suggest_payload)
```

## Capstone Acceptance Criteria

- End-to-end demo: author drafts a post, presses “Suggest SEO”, receives validated suggestions within SLA.
- Logs capture prompt, response, latency, guardrail outcomes with redaction of sensitive data.
- Automated evaluation pipeline scores suggestions vs. reference dataset; results stored for regression tracking.
- Incident response drill executed; team rotates on-call duties with documented outcomes.

## Peer Feedback Rubric

| Dimension | Outstanding | Satisfactory | Needs Work |
| --- | --- | --- | --- |
| Prompt Quality | Clear instructions, zero hallucinations, high relevance | Minor adjustments required | Off-topic or policy violations |
| Safety | Comprehensive guardrails, continuous monitoring | Guardrails in place, limited monitoring | Missing guardrails or logging |
| Performance | Consistent SLA compliance under load | Minor latency spikes resolved | Frequent timeouts or bottlenecks |
| Documentation | Detailed runbooks, diagrams, prompt catalog | README and API docs | Sparse notes, outdated diagrams |

