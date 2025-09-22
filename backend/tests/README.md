# Test Suite Overview

This directory aggregates automated tests for BlogCraftAI. The suite is grouped by feature area:

- `test_accounts_api.py`: API coverage for registration, authentication, and profile management.
- `test_blog_api.py`: CRUD, permission, and validation checks for posts, comments, tags, and reactions.
- `test_blog_views.py`: Smoke tests for HTML templates ensuring accessibility affordances and error handling.
- `test_ai_service.py`: Prompt-engineering service validation including success responses and resilience scenarios (timeouts, malformed data).

All tests run with `pytest` and rely on Django's testing tools alongside factories for ergonomic setup. The suite targets critical paths, edge cases, and failure simulations to provide high confidence in system behaviour.
