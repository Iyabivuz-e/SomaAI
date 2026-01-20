"""Job queue management.

Provides Redis-backed job queue with sync fallback for testing.
"""

from typing import Any, Dict, Optional

from somaai.contracts.jobs import JobStatus, JobResponse


async def enqueue_job(
    task_name: str,
    payload: Dict[str, Any],
) -> str:
    """Enqueue a background job.
    
    Creates a job record and adds it to the queue for processing.
    
    Args:
        task_name: Name of the task to execute (e.g., 'ingest_document', 'generate_quiz')
        payload: Task-specific payload data
        
    Returns:
        job_id: Unique job identifier for tracking
        
    Behavior:
        - If QUEUE_BACKEND=redis: Adds job to Redis queue
        - If QUEUE_BACKEND=sync: Executes job synchronously (for testing)
    """
    pass


async def get_job_status(job_id: str) -> Optional[JobResponse]:
    """Get current status of a job.
    
    Args:
        job_id: Job identifier from enqueue_job
        
    Returns:
        JobResponse with current status, progress, and result
        None if job not found
    """
    pass


async def update_job_status(
    job_id: str,
    status: JobStatus,
    progress_pct: int = 0,
    result_id: Optional[str] = None,
    error: Optional[str] = None,
) -> None:
    """Update job status (called by workers).
    
    Args:
        job_id: Job identifier
        status: New status
        progress_pct: Progress percentage (0-100)
        result_id: Result ID if completed (e.g., doc_id, quiz_id)
        error: Error message if failed
    """
    pass


async def get_pending_jobs(limit: int = 10) -> list:
    """Get pending jobs for processing (used by worker).
    
    Args:
        limit: Maximum number of jobs to fetch
        
    Returns:
        List of job records ready for processing
    """
    pass
