"""Document ingestion endpoints.

Ingest = {upload, chunk, embed, store}
"""

from fastapi import APIRouter, File, Form, UploadFile

from somaai.contracts.common import GradeLevel, Subject
from somaai.contracts.docs import IngestJobResponse
from somaai.contracts.jobs import JobResponse

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("", response_model=IngestJobResponse)
async def ingest_document(
    file: UploadFile = File(..., description="Document file (PDF, DOCX)"),
    grade: GradeLevel = Form(..., description="Grade level"),
    subject: Subject = Form(..., description="Subject"),
    title: str = Form(None, description="Document title (optional)"),
):
    """Upload and ingest a curriculum document.

    Accepts file upload with metadata.
    Processing runs as a background job.

    Steps:
    1. Validate file type
    2. Save to storage
    3. Create document record
    4. Enqueue ingestion job

    Returns:
    - job_id: Background job ID for tracking
    - doc_id: Document ID (immediate)
    - status: "pending"

    Ingestion job will:
    - Extract text from document
    - Split into chunks
    - Generate embeddings
    - Store in vector database
    """
    pass


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_ingest_job_status(job_id: str):
    """Get ingestion job status.

    Returns:
    - job_id
    - status: pending | running | completed | failed
    - progress_pct: 0-100
    - result_id: doc_id when completed
    - error: Error message if failed

    Poll this endpoint to track ingestion progress.

    Returns 404 if job not found.
    """
    pass
