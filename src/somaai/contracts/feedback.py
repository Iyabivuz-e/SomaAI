"""Feedback endpoint schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    """Request body for POST /api/v1/feedback.
    
    Teacher feedback on AI-generated responses.
    """
    
    message_id: str = Field(..., description="Message ID being rated (required)")
    is_useful: bool = Field(..., description="Was the response useful?")
    text: Optional[str] = Field(None, max_length=1000, description="Optional feedback text")
    tags: Optional[List[str]] = Field(None, description="Optional feedback tags")


class FeedbackResponse(BaseModel):
    """Response for POST /api/v1/feedback.
    
    Confirms feedback was recorded.
    """
    
    feedback_id: str = Field(..., description="Unique feedback ID")
    message_id: str = Field(..., description="Associated message ID")
    is_useful: bool = Field(..., description="Usefulness rating")
    created_at: datetime = Field(..., description="Feedback timestamp")
