---
marp: true
theme: default
paginate: true
backgroundColor: #f8f9fa
---

<h1 style="font-size:72px;color : aqua;"> Online Poll System Backend </h1>

**Django REST API for Real-Time Polls**

*ALX ProDev Backend Engineering Project*

---

## Agenda

1. Project Overview
2. ERD & Data Model
3. Key Endpoints & Features
4. Tools & Best Practices
5. Deployment Summary
6. Q&A

---

## Project Overview

- Online poll/voting system backend
- Real-time result computation
- Scalable, containerized with Docker
- JWT authentication and anonymous voting support
- Designed for extensibility and collaboration

---

## ERD & Data Model

![bg right:45%](https://raw.githubusercontent.com/plantuml-stdlib/Cicon-PlantUML/master/database.png)

**Entities:**
- **User**: Registered voter (optional, supports anonymous)
- **Poll**: Question, description, expiration, options
- **Option**: Belongs to a poll, stores text and order
- **Vote**: Links voter (user or identifier) to poll option

---

**Rationale:**
- UUIDs for all IDs (scalable, secure)
- Unique constraint on (poll, voter_id) to prevent duplicate votes
- Options as separate model for flexibility
- Votes reference both poll and option for efficient queries

---

## Key Endpoints

- `POST /api/polls/` — Create poll
- `GET /api/polls/` — List polls
- `GET /api/polls/{poll_id}/` — Poll details
- `POST /api/votes/` — Cast vote
- `GET /api/polls/{poll_id}/results/` — Poll results
- Auth: `/api/register/`, `/api/login/`, `/api/me/`

**Features:**
- Real-time results with Redis caching
- Duplicate vote prevention
- JWT authentication & optional anonymous voting
- OpenAPI/Swagger docs

---

## Tools, Frameworks

- **Django** & **Django REST Framework**: Core backend and API
- **PostgreSQL / SQLite**: Database support
- **Redis**: Caching for fast results
- **Docker**: Containerization for easy deployment
- **JWT**: Secure authentication
- **Testing**: Unit and integration tests
- **CI/CD**: Automated workflows (if configured)

---

## Best Practices

- **Best Practices**:
  - Modular, readable code
  - Data validation and security
  - Clear documentation

---

## Deployment Summary

- **Docker Compose**: For local and production-like environments
- **Environment Variables**: `.env` file for secrets and config
- **API Docs**: Auto-generated at `/api/docs`
- **Database**: SQLite / PostgreSQL
- **Redis**: Optional, for caching poll results
- **Hosting**: Render

---

<!-- _class: lead -->

# Thank You!

**Questions?**

_Contact: [Your Name] | [Your Email]_
