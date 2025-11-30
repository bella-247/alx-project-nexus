# API Reference

This document describes the API endpoints for the Online Poll System backend.

## Polls Endpoints

- `POST /api/polls/` — Create a poll  
  - body: `{"title": "...", "description": "...", "expires_at": "<ISO datetime>", "options": ["A", "B"]}`

- `GET /api/polls/<poll_id>/` — Poll detail with options

- `POST /api/votes/` — Cast a vote  
  - body: `{"poll": "<poll_uuid>", "option": "<option_uuid>", "voter_id": "<identifier>"}`

- `GET /api/polls/<poll_id>/results/` — Returns option vote counts and total votes. This endpoint uses a short-lived cache for performance and is invalidated automatically when votes or options change.

### Duplicate Vote Prevention

The backend enforces one vote per `voter_id` per poll using a unique constraint on `(poll, voter_id)`. Choose a `voter_id` scheme appropriate to your app (user id, session id, hashed ip+ua, etc.).

## Authentication & User Endpoints

- `POST /api/register/` — Register a new user  
  - body: `{"email": "...", "name": "...", "password": "..."}`
  - response: `{"id": "...", "email": "...", "name": "..."}`
  - No authentication required.

- `POST /api/login/` — Obtain JWT access and refresh tokens, plus user info  
  - body: `{"email": "...", "password": "..."}`
  - response: `{"access": "<jwt>", "refresh": "<jwt>", "user": {"id": "...", "email": "...", "name": "...", "avatar": "...", "created_at": "...", "updated_at": "..."}}`
  - No authentication required.

- `POST /api/token/refresh/` — Refresh JWT access token  
  - body: `{"refresh": "<refresh_token>"}`
  - response: `{"access": "<new_access_token>"}`
  - No authentication required.

- `GET /api/me/` — Get current authenticated user's info  
  - headers: `Authorization: Bearer <access_token>`
  - response: `{"id": "...", "email": "...", "name": "...", "avatar": "...", "created_at": "...", "updated_at": "..."}`
  - Requires authentication.

---

For setup instructions, Docker usage, and project overview, see [README.md](../README.md).
