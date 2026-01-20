"""Background task definitions.

Contains the actual task logic for background jobs.
Tasks are executed by the worker process.
"""

from typing import Any


async def ingest_document_task(job_id: str, doc_id: str) -> None:
    """Process document ingestion.

    Executed as a background job after document upload.

    Steps:
        1. Load document from storage
        2. Extract text and metadata
        3. Split into chunks
        4. Generate embeddings for chunks
        5. Store chunks and embeddings in vector DB
        6. Update document status

    Args:
        job_id: Job ID for progress updates
        doc_id: Document ID to process

    Updates:
        - Job progress (0-100%)
        - Job status (running -> completed/failed)
        - Document processed_at timestamp
    """
    pass


async def generate_quiz_task(job_id: str, quiz_id: str) -> None:
    """Generate quiz questions.

    Executed as a background job after quiz generation request.

    Steps:
        1. Load topics and related chunks from DB
        2. Construct prompt with topic content
        3. Call LLM to generate questions
        4. Parse and validate generated questions
        5. Extract citations for answer keys
        6. Store quiz items in DB
        7. Update quiz status

    Args:
        job_id: Job ID for progress updates
        quiz_id: Quiz ID to generate

    Updates:
        - Job progress (0-100%)
        - Job status (running -> completed/failed)
        - Quiz status and items
    """
    pass


# Task registry for dynamic dispatch
TASK_REGISTRY: dict[str, Any] = {
    "ingest_document": ingest_document_task,
    "generate_quiz": generate_quiz_task,
}
