# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
# Start development server
uvicorn src.main:app --reload

# Or via FastAPI CLI
fastapi dev src/main.py

# Start with explicit settings
uvicorn src.main:app --host 0.0.0.0 --port 8000 --loop uvloop
```

## Database Migrations (Alembic)

```bash
alembic upgrade head        # Apply all migrations
alembic downgrade -1        # Roll back one migration
alembic revision --autogenerate -m "description"  # Generate migration
```

## Dependencies

```bash
pip install -r requirements.txt
```

## Architecture

**Stack:** FastAPI + Uvicorn (ASGI), PostgreSQL via asyncpg, SQLAlchemy 2.0 async ORM, Alembic migrations, Pydantic v2 settings/validation.

**Entry point:** `src/main.py` — initializes the FastAPI app, async SQLAlchemy engine, and session factory.

**Configuration:** `config/fastapi/base.py` defines a `Settings` class (Pydantic `BaseSettings`) that loads from `.env`. Access settings via the `settings` singleton imported from that module. `config/fastapi/production.py` is reserved for production overrides.

**Database session:** `async_session` factory (created in `main.py`) produces `AsyncSession` instances. Use FastAPI dependency injection to provide sessions to route handlers.

**Key patterns:**
- Async-first: all DB operations use `AsyncSession` and `await`; uvloop is the event loop implementation
- UUIDs as primary keys (PostgreSQL UUID type via `sqlalchemy.dialects.postgresql`)
- Pydantic v2 models for request/response validation; `EmailStr` for email fields
- `APIRouter` for organizing route groups; mount routers onto the main `app`
- Environment-based config only — no hardcoded credentials; all secrets via `.env`
