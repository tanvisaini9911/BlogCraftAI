# Prompt Engineering Curriculum (40 Hours)

## Day 1 – Foundations & Responsible AI (8h)

| Time | Topic | Format | Deliverables |
| --- | --- | --- | --- |
| 09:00 – 09:45 | Track kickoff, AI governance overview, success metrics | Lecture | Program charter, measurement plan |
| 09:45 – 11:00 | Prompt engineering fundamentals: roles, instructions, delimiters | Workshop | Prompt taxonomy with examples |
| 11:00 – 12:30 | Bias, fairness, and content policy guardrails | Case Study | Risk register, guardrail requirements |
| 13:30 – 14:30 | Hugging Face ecosystem tour, model cards, licensing | Demo | Candidate model comparison matrix |
| 14:30 – 16:00 | Prompt evaluation frameworks (BLEU, ROUGE, qualitative rubrics) | Lab | Evaluation sheet + sample dataset |
| 16:00 – 17:00 | Retro, Q&A, parking lot | Discussion | Updated backlog |

## Day 2 – Model Operations (8h)

| Time | Topic | Format | Deliverables |
| --- | --- | --- | --- |
| 09:00 – 10:15 | Running quantized models locally with `transformers` + `bitsandbytes` | Live Coding | Notebook verifying inference |
| 10:15 – 12:00 | Serving strategies: FastAPI microservice vs. Hugging Face Inference Endpoints | Architecture Review | Decision log |
| 13:00 – 14:00 | Tokenization internals, prompt length optimization, caching | Lab | Token budget calculator script |
| 14:00 – 15:30 | Embeddings with `sentence-transformers` for context retrieval | Workshop | Vector store seeds (FAISS/pgvector) |
| 15:30 – 17:00 | Monitoring model performance, drift detection | Lab | Grafana dashboard skeleton |

## Day 3 – API Implementation (8h)

| Time | Topic | Format | Deliverables |
| --- | --- | --- | --- |
| 09:00 – 10:30 | Designing `/api/ai/suggest` contract, JSON schema, error codes | Design Studio | API spec, schema definitions |
| 10:30 – 12:00 | Building async service layer with retries, exponential backoff | Pair Programming | `ai.services.suggester` module |
| 13:00 – 14:30 | Integrating moderation filters, forbidden terms list, regex heuristics | Lab | Configurable guardrail policies |
| 14:30 – 15:30 | Response ranking using embeddings + similarity scoring | Workshop | Reranking pipeline |
| 15:30 – 17:00 | Logging, tracing, and analytics (OpenTelemetry, custom dashboards) | Lab | Structured logging pipeline |

## Day 4 – Quality Engineering (8h)

| Time | Topic | Format | Deliverables |
| --- | --- | --- | --- |
| 09:00 – 10:30 | Unit testing with mocks/stubs, property-based testing for prompts | Lecture + Lab | `tests/unit/test_prompts.py` skeleton |
| 10:30 – 12:00 | Negative testing: schema violations, forbidden terms, adversarial prompts | Lab | Test dataset + automated assertions |
| 13:00 – 14:15 | Failure simulations: API timeouts, rate limiting, circuit breaker patterns | Chaos Lab | Resilience test scripts |
| 14:15 – 15:30 | Load testing and latency budgeting | Lab | k6 scenario capturing P95 metrics |
| 15:30 – 17:00 | Human-in-the-loop evaluation workflows | Workshop | Feedback loop pipeline |

## Day 5 – Capstone Integration (8h)

| Time | Topic | Format | Deliverables |
| --- | --- | --- | --- |
| 09:00 – 10:30 | Connect AI endpoint to Blog editor (HTMX + fetch fallback) | Integration Lab | Working “Suggest SEO” button prototype |
| 10:30 – 12:00 | Observability and alerting runbooks | Lab | PagerDuty/Alertmanager playbook |
| 13:00 – 14:30 | Capstone build time: extend endpoint for outline + title suggestions | Team Sprint | PR with tests, docs |
| 14:30 – 15:30 | Security & compliance review (PII scrubbers, audit logs) | Checklist Review | Compliance report |
| 15:30 – 17:00 | Capstone demos, quality gate sign-off, retrospective | Presentations | Demo video, improvement backlog |

## Optional Deep Dives

- Fine-tuning pipelines with LoRA/PEFT.
- Automated evaluation harness (G-Eval, Promptfoo).
- Multi-model orchestration and fallback policies.

