"""SomaAI API Contracts (Pydantic schemas).

This module contains all request/response schemas used by the API.
Centralizing contracts ensures consistency across endpoints.
"""

from somaai.contracts.common import (
    PaginatedResponse,
    UserRole,
    GradeLevel,
    Subject,
)
from somaai.contracts.errors import (
    ErrorResponse,
    ValidationErrorResponse,
)
from somaai.contracts.chat import (
    ChatRequest,
    ChatResponse,
    MessageResponse,
    CitationResponse,
)
from somaai.contracts.docs import (
    DocumentResponse,
    DocumentViewResponse,
    IngestRequest,
    IngestJobResponse,
)
from somaai.contracts.quiz import (
    QuizGenerateRequest,
    QuizResponse,
    QuizItemResponse,
    QuizDownloadParams,
)
from somaai.contracts.teacher import (
    TeacherProfileRequest,
    TeacherProfileResponse,
)
from somaai.contracts.feedback import (
    FeedbackRequest,
    FeedbackResponse,
)
from somaai.contracts.meta import (
    GradeResponse,
    SubjectResponse,
    TopicResponse,
)
from somaai.contracts.jobs import (
    JobStatus,
    JobResponse,
)

__all__ = [
    # Common
    "PaginatedResponse",
    "UserRole",
    "GradeLevel",
    "Subject",
    # Errors
    "ErrorResponse",
    "ValidationErrorResponse",
    # Chat
    "ChatRequest",
    "ChatResponse",
    "MessageResponse",
    "CitationResponse",
    # Docs
    "DocumentResponse",
    "DocumentViewResponse",
    "IngestRequest",
    "IngestJobResponse",
    # Quiz
    "QuizGenerateRequest",
    "QuizResponse",
    "QuizItemResponse",
    "QuizDownloadParams",
    # Teacher
    "TeacherProfileRequest",
    "TeacherProfileResponse",
    # Feedback
    "FeedbackRequest",
    "FeedbackResponse",
    # Meta
    "GradeResponse",
    "SubjectResponse",
    "TopicResponse",
    # Jobs
    "JobStatus",
    "JobResponse",
]
