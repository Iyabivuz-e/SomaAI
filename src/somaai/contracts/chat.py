"""Chat endpoint schemas."""

from datetime import datetime

from pydantic import BaseModel, Field

from somaai.contracts.common import GradeLevel, Subject, UserRole


class ChatRequest(BaseModel):
    """Request body for POST /api/v1/chat/ask.

    Used by both students and teachers to ask questions.
    """

    query: str = Field(
        ..., min_length=1, max_length=2000, description="User's question"
    )
    grade: GradeLevel = Field(..., description="Grade level for context")
    subject: Subject = Field(..., description="Subject for context")
    session_id: str | None = Field(
        None, description="Conversation session ID for context"
    )
    user_role: UserRole = Field(default=UserRole.STUDENT, description="User role")
    enable_analogy: bool | None = Field(None, description="Include analogy in response")
    enable_realworld: bool | None = Field(
        None, description="Include real-world context"
    )


class CitationResponse(BaseModel):
    """Citation reference in a response.

    Links response content to source documents.
    """

    doc_id: str = Field(..., description="Source document ID")
    doc_title: str = Field(..., description="Document title/filename")
    page_number: int = Field(..., description="Page number in document")
    chunk_preview: str = Field(
        ..., max_length=200, description="Preview of cited content"
    )
    view_url: str = Field(..., description="URL to view the source page")
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance score (0-1)")


class ChatResponse(BaseModel):
    """Response body for POST /api/v1/chat/ask.

    Contains the AI-generated answer with citations.
    """

    message_id: str = Field(..., description="Unique message ID for reference")
    response: str = Field(..., description="AI-generated answer")
    sufficiency: bool = Field(
        ..., description="Whether context was sufficient for answer"
    )
    citations: list[CitationResponse] = Field(
        default_factory=list, description="Source citations"
    )
    analogy: str | None = Field(None, description="Analogy explanation if enabled")
    realworld_context: str | None = Field(
        None, description="Real-world application if enabled"
    )
    created_at: datetime = Field(..., description="Response timestamp")


class MessageResponse(BaseModel):
    """Full message details for GET /api/v1/chat/messages/{message_id}.

    Includes complete message history and metadata.
    """

    message_id: str = Field(..., description="Unique message ID")
    session_id: str | None = Field(
        None, description="Session ID if part of conversation"
    )
    user_role: UserRole = Field(..., description="Role of user who asked")
    query: str = Field(..., description="Original question")
    response: str = Field(..., description="AI-generated answer")
    sufficiency: bool = Field(..., description="Whether context was sufficient")
    grade: GradeLevel = Field(..., description="Grade level context")
    subject: Subject = Field(..., description="Subject context")
    citations: list[CitationResponse] = Field(
        default_factory=list, description="Source citations"
    )
    created_at: datetime = Field(..., description="Message timestamp")
