"""Quiz generation endpoint schemas."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class DifficultyLevel(str, Enum):
    """Quiz difficulty levels."""
    
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuizStatus(str, Enum):
    """Quiz generation status."""
    
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class DownloadVariant(str, Enum):
    """Quiz download variants."""
    
    QUESTIONS = "questions"
    QUESTIONS_ANSWERS = "questions_answers"


class DownloadFormat(str, Enum):
    """Quiz download formats."""
    
    PDF = "pdf"
    DOCX = "docx"


class QuizGenerateRequest(BaseModel):
    """Request body for POST /api/v1/quiz/generate.
    
    Teacher inputs for quiz generation.
    """
    
    topic_ids: List[str] = Field(..., min_length=1, description="Topic IDs to generate questions from")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level")
    num_questions: int = Field(..., ge=1, le=50, description="Number of questions to generate")
    include_answer_key: bool = Field(True, description="Include detailed answers with citations")


class QuizItemCitation(BaseModel):
    """Citation for a quiz item answer."""
    
    doc_id: str = Field(..., description="Source document ID")
    doc_title: str = Field(..., description="Document title")
    page_number: int = Field(..., description="Page number")
    excerpt: str = Field(..., description="Relevant excerpt")


class QuizItemResponse(BaseModel):
    """Single quiz question with answer.
    
    Represents one question in a generated quiz.
    """
    
    item_id: str = Field(..., description="Quiz item ID")
    order: int = Field(..., description="Question order (1-indexed)")
    question: str = Field(..., description="Question text")
    answer: Optional[str] = Field(None, description="Answer text (if include_answer_key)")
    answer_citations: Optional[List[QuizItemCitation]] = Field(None, description="Answer source citations")


class QuizResponse(BaseModel):
    """Response for GET /api/v1/quiz/{quiz_id}.
    
    Full quiz details including all items.
    """
    
    quiz_id: str = Field(..., description="Unique quiz ID")
    status: QuizStatus = Field(..., description="Generation status")
    topic_names: List[str] = Field(default_factory=list, description="Topic names included")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level")
    num_questions: int = Field(..., description="Requested number of questions")
    items: List[QuizItemResponse] = Field(default_factory=list, description="Quiz items (if completed)")
    created_at: datetime = Field(..., description="Creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    error: Optional[str] = Field(None, description="Error message if failed")


class QuizDownloadParams(BaseModel):
    """Query params for GET /api/v1/quiz/{quiz_id}/download.
    
    Controls download format and content.
    """
    
    variant: DownloadVariant = Field(DownloadVariant.QUESTIONS, description="Content variant")
    format: DownloadFormat = Field(DownloadFormat.PDF, description="File format")
