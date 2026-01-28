"""Chat module service."""

from datetime import datetime
from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from somaai.contracts.chat import (
    ChatRequest,
    ChatResponse,
    CitationResponse,
    MessageResponse,
    Preferences,
)
from somaai.contracts.common import GradeLevel, Subject, Sufficiency, UserRole
from somaai.db.models import Message, TeacherProfile
from somaai.modules.chat.citations import CitationManager
from somaai.modules.rag.pipelines import RAGPipeline
from somaai.utils.ids import generate_id
from somaai.utils.time import utc_now


class ChatService:
    """Chat service."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize ChatService with database session.
        Args:
            db: Async database session for persistence
        """
        self.db = db
        self.rag_pipeline = RAGPipeline()
        self.citation_manager = CitationManager(db)

    async def ask(
        self,
        data: ChatRequest,
        actor_id: str,
    ) -> ChatResponse:
        """Process a chat message and generate AI response.
        Flow:
        1. Normalize question (strip whitespace)
        2. Determine effective preferences (teacher defaults from profile)
        3. Run RAG pipeline (retrieve → generate)
        4. Save to DB (message + citations)
        5. Return ChatResponse
        Args:
            data: Chat request with question, grade, subject, preferences
            actor_id: Actor identifier (user or anonymous)
        Returns:
            ChatResponse with answer, citations, and optional enhancements
        """
        # 1. Normalize question
        question = data.question.strip()
        # 2. Determine effective preferences
        effective_preferences = await self._resolve_preferences(
            user_role=data.user_role,
            request_preferences=data.preferences,
            actor_id=actor_id,
        )
        # 3. Run RAG pipeline (retrieve → generate)
        rag_result = await self._run_rag_pipeline(
            question=question,
            grade=data.grade.value,
            subject=data.subject.value,
            preferences=effective_preferences,
        )
        # 4. Generate message ID and timestamp
        message_id = generate_id()
        created_at = utc_now()
        # 5. Save message to DB
        message = Message(
            id=message_id,
            session_id=data.session_id,
            actor_id=actor_id,
            user_role=data.user_role.value,
            question=question,
            answer=rag_result["answer"],
            sufficiency=rag_result["sufficiency"],
            grade=data.grade.value,
            subject=data.subject.value,
            analogy=(
                rag_result.get("analogy")
                if effective_preferences.enable_analogy
                else None
            ),
            realworld_context=(
                rag_result.get("realworld_context")
                if effective_preferences.enable_realworld
                else None
            ),
            created_at=created_at,
        )
        self.db.add(message)

        # 6. Handle Citations via Manager
        chunks = rag_result.get("retrieved_chunks", [])
        citations_response = self.citation_manager.extract_from_rag(chunks)
        await self.citation_manager.save_citations(
            message_id=message_id, rag_chunks=chunks
        )

        await self.db.flush()

        # Commit happens automatically via session context manager in deps
        # 7. Return ChatResponse
        return ChatResponse(
            message_id=message_id,
            answer=rag_result["answer"],
            sufficiency=Sufficiency(rag_result["sufficiency"]),
            citations=citations_response,
            analogy=(
                rag_result.get("analogy")
                if effective_preferences.enable_analogy
                else None
            ),
            realworld_context=(
                rag_result.get("realworld_context")
                if effective_preferences.enable_realworld
                else None
            ),
            created_at=created_at,
        )

    async def _resolve_preferences(
        self,
        user_role: UserRole,
        request_preferences: Preferences,
        actor_id: str,
    ) -> Preferences:
        """Resolve effective preferences based on user role and profile.
        For teachers:
        - Default analogy+realworld to True unless request explicitly disables
        - OR use teacher profile settings if available
        For students:
        - Use request preferences as-is
        Args:
            user_role: Student or Teacher
            request_preferences: Preferences from the request
            actor_id: Actor identifier for profile lookup
        Returns:
            Resolved Preferences object
        """
        if user_role == UserRole.STUDENT:
            # Students use request preferences as-is
            return request_preferences
        # Teacher: check profile for defaults
        profile = await self._get_teacher_profile(actor_id)
        if profile:
            # Use profile defaults, but request can override to disable
            enable_analogy = (
                request_preferences.enable_analogy
                if request_preferences.enable_analogy is not None
                else cast(bool, profile.analogy_enabled)
            )
            enable_realworld = (
                request_preferences.enable_realworld
                if request_preferences.enable_realworld is not None
                else cast(bool, profile.realworld_enabled)
            )
        else:
            # No profile: default to True for teachers unless request disables
            enable_analogy = (
                request_preferences.enable_analogy
                if request_preferences.enable_analogy is not None
                else True
            )
            enable_realworld = (
                request_preferences.enable_realworld
                if request_preferences.enable_realworld is not None
                else True
            )
        return Preferences(
            enable_analogy=enable_analogy,
            enable_realworld=enable_realworld,
        )

    async def _get_teacher_profile(self, actor_id: str) -> TeacherProfile | None:
        """Get teacher profile from database.
        Args:
            actor_id: Teacher's actor ID
        Returns:
            TeacherProfile or None if not found
        """
        result = await self.db.execute(
            select(TeacherProfile).where(TeacherProfile.teacher_id == actor_id)
        )
        return result.scalar_one_or_none()

    async def _run_rag_pipeline(
        self,
        question: str,
        grade: str,
        subject: str,
        preferences: Preferences,
    ) -> dict:
        """Run the RAG pipeline to generate an answer.
        Args:
            question: Normalized user question
            grade: Grade level for filtering
            subject: Subject for filtering
            preferences: Effective preferences for generation
        Returns:
            Dict with keys:
            - answer: Generated response text
            - sufficiency: "sufficient" or "insufficient"
            - retrieved_chunks: List of chunk metadata for citations
            - analogy: Optional analogy text
            - realworld_context: Optional real-world context text
        """
        # TODO: Enhance RAG pipeline to accept grade/subject filters
        # and return structured result with chunk metadata
        # For now, use existing pipeline
        answer = await self.rag_pipeline.run(question)
        # Determine sufficiency based on whether we got a meaningful answer
        # This should ideally come from the pipeline itself
        sufficiency = "sufficient" if answer and len(answer) > 50 else "insufficient"
        # TODO: Implement analogy and realworld generation in pipeline
        analogy = None
        realworld_context = None
        if preferences.enable_analogy:
            # TODO: Call AnalogyGenerator
            analogy = None
        if preferences.enable_realworld:
            # TODO: Call RealWorldUseCaseGenerator
            realworld_context = None
        # TODO: Return actual retrieved chunks from pipeline
        # For now returning empty list - pipeline needs enhancement
        retrieved_chunks: list[dict] = []
        return {
            "answer": answer
            or "I couldn't find enough information to answer your question.",
            "sufficiency": sufficiency,
            "retrieved_chunks": retrieved_chunks,
            "analogy": analogy,
            "realworld_context": realworld_context,
        }

    async def get_message(
        self,
        message_id: str,
        actor_id: str,
    ) -> MessageResponse | None:
        """Get a specific message by ID.
        Args:
            message_id: Message identifier
            actor_id: Actor ID for access control
        Returns:
            MessageResponse or None if not found
        """
        result = await self.db.execute(
            select(Message).where(
                Message.id == message_id, Message.actor_id == actor_id
            )
        )
        message = result.scalar_one_or_none()

        if not message:
            return None

        # Delegate citation retrieval to manager
        citations = await self.citation_manager.get_for_message(message_id)

        return MessageResponse(
            message_id=cast(str, message.id),
            session_id=cast(str | None, message.session_id),
            user_role=UserRole(cast(str, message.user_role)),
            question=cast(str, message.question),
            answer=cast(str, message.answer),
            sufficiency=Sufficiency(cast(str, message.sufficiency)),
            grade=GradeLevel(cast(str, message.grade)),
            subject=Subject(cast(str, message.subject)),
            citations=citations,
            created_at=cast(datetime, message.created_at),
        )

    async def get_message_citations(
        self,
        message_id: str,
        actor_id: str,
    ) -> list[CitationResponse] | None:
        """Get citations for a message.
        Args:
            message_id: Message identifier
            actor_id: Actor ID for access control
        Returns:
            List of CitationResponse or None if message not found
        """
        # First verify message ownership
        result = await self.db.execute(
            select(Message).where(
                Message.id == message_id, Message.actor_id == actor_id
            )
        )
        if not result.scalar_one_or_none():
            return None

        return await self.citation_manager.get_for_message(message_id)
