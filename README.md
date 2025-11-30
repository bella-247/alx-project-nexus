Online Poll System Backend
==========================

This repository contains a Django REST backend for an online poll/voting system intended for real-time result computation and scalability.

Quick start (development with Docker)

1. Copy environment file:

```bash
cp .env.example .env
```

2. Build and run with docker-compose.

For a lightweight demo using SQLite (no Postgres required):

```bash
# uses sqlite and redis (optional)
docker compose -f docker-compose.sqlite.yml up --build
```

To run with Postgres (realistic dev environment):

```bash
docker compose up --build
```

If you want Redis caching enabled (recommended for better performance of the results endpoint), copy `.env.example` to `.env` and make sure `REDIS_URL` is set (the default `.env.example` contains `REDIS_URL=redis://redis:6379/1`). The provided `docker-compose.yml` includes a `redis` service, so `docker compose up --build` will start Redis automatically.

To run without Redis, either remove the `redis` service in `docker-compose.yml` or set `REDIS_URL` to an external redis instance.

3. API docs will be at `http://localhost:8000/api/docs`

### Required Environment Variables

Set these in your `.env` file (see `.env.example` if available):

- `SECRET_KEY` or `DJANGO_SECRET_KEY`: Django secret key (required for production)
- `DEBUG` or `DJANGO_DEBUG`: Set to `1` or `True` to enable debug mode (default: enabled for dev)
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts (default: `*` or `localhost`)
- `DATABASE_URL`: Database connection string (Postgres or SQLite). If not set, fallback to PG_* vars or SQLite.
    - `PG_DB`, `PG_USER`, `PG_PASSWORD`, `PG_HOST`, `PG_PORT`: Used if `DATABASE_URL` is not set (for Postgres)
- `REDIS_URL` or `REDIS_HOST`: (Optional) Redis connection string for caching
- `ALLOW_ANONYMOUS_VOTE`: (Optional) Set to `1` to allow unauthenticated voting

Notes
- Use SQLite for simple demos and deployments without a hosted DB (see `docker-compose.sqlite.yml`).
- Use Postgres for realistic development by running the default `docker-compose.yml`.
- If you can't run Docker, edit `polls_project/settings.py` to ensure `DATABASES` uses SQLite.

Endpoints (high level)
- `POST /api/polls/` - create a poll with options
- `GET /api/polls/` - list polls
- `POST /api/polls/{poll_id}/vote/` - cast a vote (provide `voter_id` and `option_id`)
- `GET /api/polls/{poll_id}/results/` - get option counts (real-time)

For full API details and authentication endpoints, see [docs/API.md](docs/API.md).

# alx-project-nexus

## 1. Overview

This repository serves as a documentation hub for my major learnings throughout the **ALX ProDev Backend Engineering Program**. It summarizes the concepts, technologies, challenges, and best practices that shaped my backend development skills.

The goal is to maintain a central reference point where I record what I’ve learned, reflect on difficulties, and track personal progress.

---

## 2. Key Technologies Covered

Here are the major technologies studied during the program:

1. **Python**

   * Core syntax and best practices
   * Object-Oriented Programming (OOP)
   * Error handling and testing
   * Virtual environments and package management

2. **Django**

   * MVT architecture
   * Models, Views, Templates
   * Django ORM operations
   * Authentication and permissions
   * Middleware and signals

3. **REST APIs (Django REST Framework)**

   * Serializers, viewsets, routers
   * Pagination, filtering, throttling
   * JWT and session-based authentication
   * API testing and documentation

4. **GraphQL**

   * Graphene-Django basics
   * Schemas, queries, and mutations
   * Efficient data resolving

5. **Docker**

   * Writing Dockerfiles
   * Building and running containers
   * Docker Compose for multi-service applications
   * Containerizing Django projects

6. **CI/CD**

   * Automated testing
   * Deployment automation
   * GitHub Actions workflows

---

## 3. Important Backend Development Concepts

### 3.1 Database Design

- Normalization and relationships
- Indexing and optimization
- Schema migrations
- PostgreSQL usage and best practices

### 3.2 Asynchronous Programming

* Understanding async/await
* Event loops and concurrency models
* When to apply asynchronous logic in backend systems

### 3.3 Caching Strategies

* Using Redis for caching
* Caching API responses
* Improving response times with in-memory caching
* Cache invalidation techniques

---

## 4. Challenges Faced & Solutions Implemented

1. **Complex ORM queries**
   *Solution:* Broke down queries into smaller parts and compared them to raw SQL for clarity.

2. **Structuring large Django projects**
   *Solution:* Adopted modular architecture and followed Django best practices.

3. **Debugging JWT authentication issues**
   *Solution:* Used Postman, DRF browsable API, and detailed logging.

4. **Difficulties containerizing Django apps**
   *Solution:* Practiced with small standalone Docker projects before containerizing the main app.

---

## 5. Best Practices & Personal Takeaways

1. Write clean, readable, and well-documented code.
2. Break big systems into smaller, manageable modules.
3. Always validate and sanitize data.
4. Use Git properly—commit early, commit often.
5. Communicate clearly and consistently during collaboration.
6. Test thoroughly (unit, integration, edge cases).
7. Keep learning—technologies evolve, fundamentals stay.

---

## 6. Collaboration

### With Whom?

* **ProDev Backend Learners:** Exchange ideas, ask questions, pair-program.
* **ProDev Frontend Learners:** Work closely since they will consume backend APIs.

### Where?

* **Dedicated Discord Channel:** `#ProDevProjectNexus`
  Share updates, ask questions, and follow announcements.

---

## 7. ProDev Tip

During **Week 1**:

1. Announce which project you are working on.
2. Identify frontend learners building the same project.
3. Align API requirements early to ensure smooth collaboration.
