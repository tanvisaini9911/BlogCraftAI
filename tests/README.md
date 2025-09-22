# Tests Directory

The current stage of the project focuses on curriculum and documentation assets. Automated test implementation will begin once code lands on each branch. Until then, this directory documents how test suites must be organized and links to branch-specific quality plans.

## Track-Specific Quality Plans

| Track | Quality Plan |
| --- | --- |
| Django | [`tracks/django/assessments.md`](../tracks/django/assessments.md) |
| Prompt Engineering | [`tracks/prompt_engineering/assessments.md`](../tracks/prompt_engineering/assessments.md) |
| Frontend | [`tracks/frontend/assessments.md`](../tracks/frontend/assessments.md) |
| BlogCraftAI | [`tracks/blogcraftai/assessments.md`](../tracks/blogcraftai/assessments.md) |
| AI Agents | [`tracks/ai_agents/assessments.md`](../tracks/ai_agents/assessments.md) |

## Expected Structure Once Code Is Added

Create subdirectories per branch containing:
- `unit/` for fast-running isolated tests.
- `integration/` for service and database scenarios.
- `e2e/` for full workflow validation (Playwright, Cypress, etc.).
- A local `README.md` summarizing coverage, tooling, and execution commands.

Maintain coverage reports and CI configuration references here to keep quality expectations transparent across branches.