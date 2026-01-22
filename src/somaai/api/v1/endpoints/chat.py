"""Chat endpoints for student and teacher interactions."""

from fastapi import APIRouter

from somaai.contracts.chat import (
    ChatRequest,
    ChatResponse,
    CitationResponse,
    MessageResponse,
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
async def ask_question(data: ChatRequest):
    """Ask a question and get an AI-generated answer.

    Works for both students and teachers:
    - Students: Basic RAG with optional analogy/realworld
    - Teachers: Defaults from profile, feedback support, analogy/realworld enabled by default

    Request body:
    - query: The question to answer
    - grade: Grade level for context(what grade is the student or teacher teaching)
    - subject: Subject for context
    - session_id: Optional conversation session
    - user_role: "student" or "teacher"
    - enable_analogy: Include analogy explanation(optional for students but default for teachers)
    - enable_realworld: Include real-world context(optional for students but default for teachers)

    Response:
    - message_id: ID for reference/feedback
    - response: AI-generated answer
    - sufficiency: Whether enough context was found
    - citations: Source document references
    - analogy: Analogy explanation (if enabled)
    - realworld_context: Real-world application (if enabled)

    If insufficient context:
    - sufficiency = false
    - response contains fallback message
    """
    pass


@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: str):
    """Get a specific message by ID.

    Returns full message details including:
    - Original query and response
    - Grade and subject context
    - All citations

    Returns 404 if message not found.
    """
    pass


@router.get("/messages/{message_id}/citations", response_model=list[CitationResponse])
async def get_message_citations(message_id: str):
    """Get citations for a message.

    Returns list of source citations with:
    - doc_id: Source document ID
    - doc_title: Document title
    - page_number: Page number
    - chunk_content: Relevant excerpt
    - view_url: Link to view the page

    Used for "show sources" functionality.

    Returns 404 if message not found.
    """
    pass
