# SpendTrackr

SpendTrackr is a **backend service for multi-tenant expense management**, inspired by platforms like Alaan, Brex, Ramp, etc.

It lets companies:

- Sign up and create an organization
- Create admin and employee users
- Issue virtual “cards” to employees (planned)
- Record transactions and manage approvals (planned)
- View spend summaries and reports (planned)

The goal is to demonstrate **realistic fintech backend design** using:

- **FastAPI**
- **MySQL (Cloud SQL–friendly)**
- **SQLAlchemy 2.x**
- **Redis**
- **JWT auth**
- **Docker + uv** for local development

---

## Tech Stack

- **Language:** Python 3.11+
- **Web Framework:** FastAPI
- **ORM:** SQLAlchemy 2.x
- **Database:** MySQL 8 (via Docker, Cloud SQL–friendly)
- **Cache:** Redis
- **Auth:** JWT (via `python-jose`) + password hashing (`passlib[bcrypt_sha256]`)
- **Dependency & Env Management:** [uv](https://github.com/astral-sh/uv), `pydantic-settings`, `.env`
- **Containerization:** Docker + docker-compose

---

## Project Structure

```bash
src/
  spendtrackr/
    __init__.py
    main.py              # FastAPI app entrypoint
    core/
      __init__.py
      config.py          # Settings & env loading (DB, JWT, Redis, etc.)
      security.py        # Password hashing, JWT helpers
      dependencies.py    # FastAPI dependencies (DB session, current user, admin)
    db/
      __init__.py
      base.py            # SQLAlchemy Base
      session.py         # Engine + SessionLocal / get_db dependency
      migrations/        # (reserved for Alembic)
    apps/
      auth/
        __init__.py
        models.py        # (if needed later)
        schemas.py       # Signup/Login/Token schemas
        routes.py        # /auth endpoints (signup, login, me)
        service.py       # Business logic for auth
      companies/
        __init__.py
        models.py        # Company ORM model
        schemas.py       # Company Pydantic schemas
        service.py       # Company-related logic (if needed)
      users/
        __init__.py
        models.py        # User ORM model + roles
        schemas.py       # User Pydantic schemas
        service.py       # User-related logic (if needed)
      # Planned:
      # cards/
      # transactions/
      # reports/
    utils/
      __init__.py        # Shared helpers (future)
