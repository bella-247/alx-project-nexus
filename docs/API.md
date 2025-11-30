# API & Setup Guide

This document provides quick setup steps and the main API endpoints for the Online Poll System backend.

## Development (SQLite)

1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and start server

```bash
python manage.py migrate
python manage.py runserver
```

3. API docs (OpenAPI + Swagger)

Visit: `http://127.0.0.1:8000/api/docs/`

## Important endpoints

- `POST /api/polls/` - Create a poll
  - body: {"title":"...","description":"...","expires_at":"<ISO datetime>","options":["A","B"]}

- `GET /api/polls/<poll_id>/` - Poll detail with options
- `POST /api/votes/` - Cast a vote
  - body: {"poll":"<poll_uuid>","option":"<option_uuid>","voter_id":"<identifier>"}

- `GET /api/polls/<poll_id>/results/` - Returns option vote counts and total votes. This endpoint uses a short-lived cache for performance and is invalidated automatically when votes or options change.

## Notes on duplicate prevention

The backend enforces one vote per `voter_id` per poll using a unique constraint on `(poll, voter_id)`. Choose a `voter_id` scheme appropriate to your app (user id, session id, hashed ip+ua, etc.).

## Docker

You can run the project using SQLite (recommended for lightweight demos and low-cost hosting) or Postgres (for realistic development).

- SQLite (no DB service required):

```bash
# uses sqlite and redis (optional)
docker compose -f docker-compose.sqlite.yml up --build
```

- Postgres (dev):

```bash
docker compose up --build
```

See `.env.example` to configure `DATABASE_URL`. Leave it empty to use SQLite.
