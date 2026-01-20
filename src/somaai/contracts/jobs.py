"""Background job schemas."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Background job status."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobResponse(BaseModel):
    """Response for job status endpoints.
    
    Used by ingest jobs, quiz generation, etc.
    """
    
    job_id: str = Field(..., description="Unique job ID")
    status: JobStatus = Field(..., description="Current job status")
    progress_pct: int = Field(0, ge=0, le=100, description="Progress percentage (0-100)")
    result_id: Optional[str] = Field(None, description="Result ID when completed (e.g., doc_id, quiz_id)")
    error: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(..., description="Job creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Processing start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional job metadata")
