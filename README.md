# BlueSentra

Coastal environmental intelligence platform for West Africa.
Architecture decisions are recorded as ADRs in the project's Engineering Foundation document.

## Layout

```text
backend/    Django + DRF + GeoDjango modular monolith
frontend/   React + TypeScript (added in the next setup step)
docker-compose.yml
```

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

The API is served at `http://localhost:8000/api/v1/`, with documentation at `/api/v1/docs/`.

## Quality checks (from `backend/`)

```bash
ruff check . && ruff format --check . && mypy . && python manage.py check && pytest
pytest -m spatial     # needs PostGIS (provided by docker compose)
```

See `CONTRIBUTING.md` for the Git workflow.
