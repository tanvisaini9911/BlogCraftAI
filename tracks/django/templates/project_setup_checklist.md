# Django Project Setup Checklist

- [ ] Clone repository and checkout `Django` branch.
- [ ] Copy `.env.example` to `.env.local`; fill secrets via password manager.
- [ ] Install dependencies using `poetry install --no-root`.
- [ ] Run `pre-commit install` to enable linting hooks.
- [ ] Launch infrastructure with `docker compose up -d db redis`.
- [ ] Execute `poetry run python manage.py migrate`.
- [ ] Seed demo content using `poetry run python manage.py seed_demo_content`.
- [ ] Create superuser (`poetry run python manage.py createsuperuser`).
- [ ] Verify `/admin` login, confirm custom dashboards render correctly.
- [ ] Execute `poetry run pytest --maxfail=1 --disable-warnings -q` and ensure green suite.
- [ ] Generate OpenAPI schema `poetry run python manage.py spectacular --file schema.yaml`.
- [ ] Commit infrastructure diagrams and update runbooks.

