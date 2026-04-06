# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Licican** is a web platform for discovering and tracking IT public procurement opportunities in the Canary Islands. It aggregates and classifies licitaciones (tenders) from official bulletins (BOC, BOP, BOE) and presents them with filtering, alerting, and pipeline tracking features.

## Commands

```bash
# Development
make run              # Start app locally (auto-selects port)
make docker-db-up     # Start only PostgreSQL (useful for local dev with DB)
make docker-up        # Full stack with Docker Compose

# Tests
make test             # Run pytest suite (verbose)
make coverage         # Run tests with coverage report
PYTHONPATH=src python3 -m pytest tests/test_foo.py -v  # Run a single test file

# Direct run (without make)
PYTHONPATH=src python3 -m licican.app
```

All Python commands require `PYTHONPATH=src` to resolve the `licican` package.

## Architecture

### Tech Stack
- **Backend:** Pure Python 3.12+ WSGI app (no web framework like Flask/Django)
- **Database:** PostgreSQL via psycopg2; file-based fallback controlled by `LICICAN_CATALOG_BACKEND` env var
- **Frontend:** HTML generated programmatically in Python (no templating engine like Jinja2 — templates are `.py` files)
- **Auth:** Custom session/CSRF implementation in `src/licican/auth/`

### Request Lifecycle
`src/licican/app.py` → `src/licican/web/router.py` → `src/licican/web/handlers/*.py` → business logic modules → `src/licican/postgres_catalog.py`

Handlers return responses built with `src/licican/web/responses.py`. HTML is assembled by calling functions in `src/licican/web/templates/*.py`.

### Key Modules
| Module | Responsibility |
|--------|----------------|
| `opportunity_catalog.py` | Core business logic for browsing/filtering opportunities |
| `postgres_catalog.py` | All SQL queries and DB access |
| `alerts.py` | Alert creation and early-warning tracking |
| `ti_classification.py` | Rules that classify tenders as IT-related |
| `atom_consolidation.py` | Parses and consolidates Atom/XML feeds from bulletin sources |
| `pipeline.py` | Tracks procurement pipeline stages |
| `access.py` | Role-based access control (RBAC) |
| `auth/` | Session management, CSRF, rate limiting |

### Configuration
Copy `.env.example` to `.env`. Key variables:
- `DB_*` — PostgreSQL connection params
- `LICICAN_CATALOG_BACKEND` — `postgres` or `file`
- `FILTRO_NUTS_PREFIXES` / `FILTRO_GEO_KEYWORDS` — geographic filters for classifying local tenders
- `BASE_PATH` — URL prefix if deployed behind a reverse proxy

### Database
Schema and migrations live in `bbdd/`. The PostgreSQL container used in Docker is defined in `docker-compose.yml`. Use `make docker-psql` to open a psql session.

## Project Documentation

Product artifacts (backlog, user stories, functional specs, roadmap) are in `product-manager/`. Role-specific agent workflows are documented in `product-manager/AGENTS.md`.
