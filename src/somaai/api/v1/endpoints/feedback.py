"""Feedback endpoints."""

from fastapi import APIRouter, HTTPException

from somaai.contracts.feedback import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse)
async def submit_feedback(
    data: FeedbackRequest,
):
    """Submit feedback for an AI response.
    
    Request body:
    - message_id: Required - ID of message being rated
    - is_useful: Required - boolean rating
    - text: Optional - detailed feedback text
    - tags: Optional - list of feedback categories
    
    Returns:
    - 400 if message_id is missing or invalid
    - 200 with feedback_id on success
    
    Used by teachers to rate response quality.
    """
    pass
