# SomaAI

An AI-enabled digital platform designed to improve teaching and learning across Rwanda. SomaAI provides students with practice materials and explanatory support based on official national resources, and provides teachers with rapid, practical assistance for preparing quizzes, tests, and clear explanations of complex topics.

## Features

**Student Mode:**
- Grade + subject selection for contextual learning
- Ask questions and receive RAG-powered answers
- Answers include citations with document links and page numbers
- Optional analogies and real-world context explanations

**Teacher Mode:**
- All student features plus enhanced defaults
- Quiz generation from curriculum topics
- Download quizzes as PDF (questions only or with answer keys)
- Feedback system for response quality improvement

**Core Capabilities:**
- RAG-Based Retrieval using official curriculum materials
- Semantic caching for faster repeated queries
- Multi-language support (English, Kinyarwanda and French in progress)

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI (Python 3.10+) |
| **Database** | PostgreSQL (NeonDB in production) |
| **Vector Store** | Qdrant |
| **Cache/Queue** | Redis |
| **Package Manager** | [uv](https://github.com/astral-sh/uv) |

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (recommended for full stack)

### Installation

```bash
# Clone the repository
git clone https://github.com/Rwanda-AI-Network/SomaAI.git
cd SomaAI

# Install dependencies
uv sync

# Copy environment variables
cp .env.example .env
```

### Running with Docker (Recommended)

```bash
# Start all services (app + postgres + redis + qdrant)
make docker

# Or use docker-compose directly
docker-compose -f docker/docker-compose.yml up --build
```

**Services started:**
- App: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Qdrant: http://localhost:6333/dashboard

### Running Locally

```bash
# Ensure external services are running (postgres, redis, qdrant)
# Then start the dev server
make dev
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/chat/ask` | POST | Ask a question (student/teacher) |
| `/api/v1/chat/messages/{id}` | GET | Get message details |
| `/api/v1/chat/messages/{id}/citations` | GET | Get source citations |
| `/api/v1/meta/grades` | GET | List grade levels |
| `/api/v1/meta/subjects` | GET | List subjects |
| `/api/v1/meta/topics` | GET | List curriculum topics |
| `/api/v1/teacher/profile` | GET/POST | Teacher profile settings |
| `/api/v1/quiz/generate` | POST | Generate quiz |
| `/api/v1/quiz/{id}` | GET | Get quiz details |
| `/api/v1/quiz/{id}/download` | GET | Download quiz as PDF |
| `/api/v1/docs/{id}` | GET | Get document metadata |
| `/api/v1/docs/{id}/view` | GET | View document page |
| `/api/v1/ingest` | POST | Upload curriculum document |
| `/api/v1/feedback` | POST | Submit response feedback |

## Development

```bash
# Install dependencies
make install

# Install with all optional dependencies
uv sync --extra all

# Run development server
make dev

# Run linting
make lint

# Run tests
make test

# Clean build artifacts
make clean
```

## Available Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install dependencies with uv |
| `make dev` | Run development server |
| `make lint` | Run linting (ruff + mypy) |
| `make test` | Run tests |
| `make docker` | Run with Docker (postgres + redis + qdrant) |
| `make docker-stop` | Stop Docker containers |

## Project Structure

```
src/somaai/
├── api/v1/endpoints/  # REST API endpoints
├── contracts/         # Pydantic request/response schemas
├── cache/             # Redis caching layer
├── db/                # SQLAlchemy models & migrations
├── jobs/              # Background job queue
├── modules/
│   ├── chat/          # Chat with citations
│   ├── docs/          # Document viewing
│   ├── feedback/      # Response ratings
│   ├── ingest/        # Document ingestion
│   ├── meta/          # Grades, subjects, topics
│   ├── quiz/          # Quiz generation
│   ├── rag/           # Retrieval & generation
│   ├── teacher/       # Teacher profiles
│   └── knowledge/     # Embeddings & vector storage
├── providers/         # LLM, storage adapters
└── tests/             # Test suite
```

## Database

**Development:** PostgreSQL via Docker
```bash
# Included in docker-compose
make docker
```

**Production:** [NeonDB](https://neon.tech) (Serverless PostgreSQL)
```bash
# Set in .env
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.neon.tech/somaai
```

## Documentation

- [API Documentation](docs/api.md)
- [Architecture Overview](docs/architecture.md)
- [Contributing Guide](CONTRIBUTING.md)

## License

Apache-2.0 license - see [LICENSE](LICENSE) for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.