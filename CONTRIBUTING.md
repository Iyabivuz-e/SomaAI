# Contributing to SomaAI

Thank you for your interest in contributing to SomaAI. This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (recommended for full development environment)

### Local Development Setup

**Option 1: Full Stack with Docker (Recommended)**

```bash
# Clone and enter the repository
git clone https://github.com/Rwanda-AI-Network/SomaAI.git
cd SomaAI

# Copy environment variables
cp .env.example .env

# Start all services (postgres, redis, qdrant, app)
make docker
```

This starts:
- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`
- Qdrant on `http://localhost:6333`
- App on `http://localhost:8000`

**Option 2: Local Python Development**

```bash
# Install dependencies
make install

# Or with all optional dependencies
uv sync --extra all

# Start external services separately, then:
make dev
```

## Project Architecture

```
src/somaai/
├── api/v1/endpoints/  # REST API endpoints
├── contracts/         # Pydantic schemas (requests/responses)
├── cache/             # Caching layer (Redis-backed)
├── db/                # Database models (SQLAlchemy)
├── jobs/              # Background tasks (Redis queue)
├── modules/           # Business logic
│   ├── chat/          # Chat + citations
│   ├── docs/          # Document viewing
│   ├── feedback/      # Response ratings
│   ├── ingest/        # Document ingestion
│   ├── meta/          # Grades, subjects, topics
│   ├── quiz/          # Quiz generation
│   ├── rag/           # RAG pipeline
│   ├── teacher/       # Teacher profiles
│   └── knowledge/     # Embeddings & vectors
├── providers/         # External service adapters
└── tests/             # Test suite
```

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/add-quiz-generation` - New features
- `fix/retrieval-accuracy` - Bug fixes
- `docs/api-documentation` - Documentation updates

### Making Changes

1. Create a new branch from `main`
2. Make your changes
3. Run linting and tests:
   ```bash
   make lint
   make test
   ```
4. Commit your changes with a clear message
5. Push and open a Pull Request

### Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check linting
make lint

# Or directly
uv run ruff check src/
uv run ruff format src/
```

### Testing

Write tests for new functionality:

```bash
# Run all tests
make test

# Run specific test file
uv run pytest src/somaai/tests/test_chat.py -v

# Run with coverage
uv run pytest --cov=somaai
```

### Database Migrations

We use Alembic for database migrations:

```bash
# Generate a new migration
uv run alembic revision --autogenerate -m "Add new table"

# Apply migrations
uv run alembic upgrade head

# Rollback
uv run alembic downgrade -1
```

### Available Make Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install dependencies with uv |
| `make dev` | Run development server |
| `make lint` | Run linting (ruff + mypy) |
| `make test` | Run tests |
| `make docker` | Run with Docker (postgres + redis + qdrant) |
| `make docker-stop` | Stop Docker containers |
| `make clean` | Clean build artifacts |

## Adding New Features

### Adding a New Endpoint

1. Create schema in `contracts/`
2. Create service in `modules/{module}/service.py`
3. Create endpoint in `api/v1/endpoints/{module}.py`
4. Register router in `api/v1/router.py`
5. Add tests in `tests/test_{module}.py`

### Adding a New Module

```
modules/new_module/
├── __init__.py      # Exports
├── service.py       # Business logic
└── (other files)    # As needed
```

## Pull Request Guidelines

Before submitting a PR:

- [ ] Code follows the project style guidelines (ruff passes)
- [ ] All tests pass locally
- [ ] New functionality includes tests
- [ ] Documentation is updated if needed
- [ ] PR description clearly explains the changes

### Educational Content Guidelines

When contributing features that affect educational content:

- Ensure alignment with Rwanda Education Board (REB) curriculum standards
- Test with both English and Kinyarwanda content where applicable
- Consider accessibility for all students and teachers

## Reporting Issues

When reporting bugs, please include:

- Steps to reproduce the issue
- Expected vs actual behavior
- Environment details (OS, Python version, Docker version)
- Relevant logs or error messages

## Database Strategy

| Environment | Database |
|-------------|----------|
| Development | PostgreSQL (Docker) |
| Production | NeonDB (serverless Postgres) |

Both use the same SQLAlchemy models and Alembic migrations.

## Questions?

For questions or discussions, please open an issue or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the Apache-2.0 license.
