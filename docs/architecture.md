# SomaAI Architecture

## Overview

SomaAI is built as a modular, async-first application designed for scalability. It uses a hybrid storage approach (Redis + PostgreSQL + Qdrant) and an asynchronous job queue for heavy lifting.

## Core Components

### 1. API Layer (FastAPI)
- **Endpoints:** RESTful v1 API with Pydantic validation.
- **Middleware:** Redis-backed Rate Limiting, CORS, Observability.
- **Auth:** API Key barrier for protected routes.

### 2. RAG Module (Intelligence)
- **Pipeline:** `Retriever` -> `Reranker` -> `Generator`.
- **Optimization:** Caches embeddings (1h) and high-confidence responses (24h) in Redis (db/2).
- **Fallback:** Gracefully handles missing context with "insufficient context" responses.

### 3. Ingest Module (Data)
- **Pipeline:** Load -> Chunk -> Filter -> Enrich -> Vector Store.
- **Performance:** Batched processing (50 chunks) and SHA-256 deduplication.
- **Scaling:** Uses `aiofiles` and chunked upload protocol for large files.

### 4. Job System (Async)
- **Backend:** ARQ (Redis db/1) for tasks like `ingest_document`, `generate_quiz`.
- **Worker:** Separate process, scalable via Docker replicas.
- **Persistence:** Job status/result stored in PostgreSQL `jobs` table.

## Data Storage

### PostgreSQL (Persistent State)
- Users, Profiles, Messages, Feedback, Jobs
- Indexed for query performance

### Redis (Hot State)
- **db/0:** Session data (Chat history, Upload sessions), Rate Limits
- **db/1:** Background Job Queue
- **db/2:** RAG Cache (Embeddings, Responses)

### Qdrant (Vector Knowledge)
- Stores document chunks and embeddings (768d)
- Payload filtering by `grade`, `subject`
