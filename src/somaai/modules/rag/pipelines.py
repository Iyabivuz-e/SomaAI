"""RAG pipelines for question answering.

Combines retrieval, reranking, and generation for curriculum-based Q&A.
Includes security, observability, and fallback strategies.
Uses Decimal for precise score handling in critical operations.
"""

from __future__ import annotations

import time
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from somaai.modules.rag.generator import CombinedGenerator
from somaai.modules.rag.reranker import get_reranker
from somaai.modules.rag.retriever import Retriever
from somaai.utils.ids import generate_id
from somaai.utils.observability import log_rag_request
from somaai.utils.security import sanitize_query

if TYPE_CHECKING:
    from somaai.settings import Settings


class RAGPipeline:
    """Complete RAG pipeline for educational Q&A.

    Combines:
    - Input sanitization for security
    - Retrieval with grade/subject filtering and fallback
    - Cross-encoder reranking (singleton)
    - LLM generation with citations
    - Observability logging
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize pipeline components.

        Args:
            settings: Application settings
        """
        self._settings = settings
        self.retriever = Retriever(settings)
        self.generator = CombinedGenerator(settings)

    @property
    def settings(self):
        """Get settings."""
        if self._settings is None:
            from somaai.settings import settings
            self._settings = settings
        return self._settings

    @property
    def reranker(self):
        """Get singleton reranker."""
        return get_reranker()

    async def run(
        self,
        query: str,
        grade: str = "S1",
        subject: str = "general",
        user_role: str = "student",
        session_id: str | None = None,
        preferences: dict | None = None,
    ) -> dict:
        """Execute the full RAG pipeline.

        Args:
            query: User's question
            grade: Grade level (e.g., "S1", "P6")
            subject: Subject (e.g., "mathematics", "biology")
            user_role: 'student' or 'teacher'
            session_id: Optional session for context
            preferences: Dict with 'enable_analogy' and 'enable_realworld'

        Returns:
            Complete response matching ChatResponse schema
        """
        start_time = time.time()
        preferences = preferences or {}
        include_analogy = preferences.get("enable_analogy", False)
        include_realworld = preferences.get("enable_realworld", False)

        try:
            # 0. Check response cache
            from somaai.cache.rag import get_response_cache
            cache = get_response_cache()
            cached_response = await cache.get(query, grade, subject)
            if cached_response:
                logger.info(f"Returning cached response for: {query[:50]}...")
                return cached_response

            # 1. Sanitize input for security
            clean_query = sanitize_query(query)

            # 2. Retrieve with fallback strategy
            docs = await self.retriever.retrieve_with_fallback(
                query=clean_query,
                grade=grade,
                subject=subject,
                top_k=20,
            )

            # 3. Rerank for relevance (uses singleton)
            # Use Decimal for precise min_score threshold
            ranked_docs = await self.reranker.rerank(
                query=clean_query,
                documents=docs,
                top_k=5,
                min_score=Decimal("0.1"),
            )

            # 4. Check if we have sufficient context
            if not ranked_docs:
                return self._insufficient_context_response(query, grade, subject)

            # 5. Generate response
            result = await self.generator.generate(
                query=clean_query,
                context=[doc.get("content", "") for doc in ranked_docs],
                grade=grade,
                user_role=user_role,
                include_analogy=include_analogy,
                include_realworld=include_realworld,
                retrieved_docs=ranked_docs,  # Pass for citation validation
            )

            # 6. Build citations (returns tuple: citations_list, chunks_map)
            citations, chunks_map = self._build_citations(ranked_docs)

            # 7. Build response
            response = {
                "message_id": generate_id(),
                "answer": result.get("answer", ""),
                "sufficiency": result.get("sufficiency", "sufficient"),
                "is_grounded": result.get("is_grounded", True),
                "confidence": result.get("confidence", 0.7),
                "citations": citations,
                "chunks_map": chunks_map,  # For persistence in chat endpoint
                "analogy": result.get("analogy"),
                "realworld_context": result.get("realworld_context"),
                "created_at": datetime.utcnow(),
            }

            # 8. Cache response if high quality
            await cache.set(query, grade, subject, response)

            # 9. Log for observability
            latency_ms = (time.time() - start_time) * 1000
            log_rag_request(
                query=query,
                grade=grade,
                subject=subject,
                docs_retrieved=len(docs),
                docs_reranked=len(ranked_docs),
                latency_ms=latency_ms,
                success=True,
            )

            return response

        except Exception as e:
            # Log failure
            latency_ms = (time.time() - start_time) * 1000
            log_rag_request(
                query=query,
                grade=grade,
                subject=subject,
                docs_retrieved=0,
                docs_reranked=0,
                latency_ms=latency_ms,
                success=False,
                error=str(e),
            )
            raise

    def _insufficient_context_response(
        self,
        query: str,
        grade: str,
        subject: str,
    ) -> dict:
        """Generate response when no relevant documents found.

        Args:
            query: Original query
            grade: Grade level
            subject: Subject

        Returns:
            Response indicating insufficient context
        """
        return {
            "message_id": generate_id(),
            "answer": (
                f"I couldn't find relevant curriculum content for your question "
                f"about {subject} at the {grade} level. Please try:\n"
                f"1. Rephrasing your question\n"
                f"2. Checking if this topic is covered in the curriculum\n"
                f"3. Asking a more specific question"
            ),
            "sufficiency": "insufficient",
            "citations": [],
            "analogy": None,
            "realworld_context": None,
            "created_at": datetime.utcnow(),
        }

    def _format_context(self, docs: list[dict]) -> str:
        """Format documents into context string.

        Args:
            docs: Retrieved and reranked documents

        Returns:
            Formatted context string with sources
        """
        parts = []
        for doc in docs:
            meta = doc.get("metadata", {})
            title = meta.get("title", "Source")
            page = meta.get("page_start", "?")
            content = doc.get("content", "")
            parts.append(f"[{title}, Page {page}]\n{content}")
        return "\n---\n".join(parts)

    def _build_citations(self, docs: list[dict]) -> tuple[list[dict], dict[str, str]]:
        """Build citations matching CitationResponse schema.

        Delegates to CitationExtractor for single source of truth.

        Args:
            docs: Retrieved documents with metadata

        Returns:
            Tuple of (list of citation dicts, chunks_map for persistence)
        """
        from somaai.modules.chat.citations import get_citation_extractor

        extractor = get_citation_extractor()
        citations, chunks_map = extractor.extract_citations(docs, top_k=len(docs))

        # Convert to dicts for response (CitationResponse -> dict)
        return [cit.model_dump() for cit in citations], chunks_map

    async def ask(
        self,
        question: str,
        grade: str,
        subject: str,
        user_role: str = "student",
        preferences: dict | None = None,
    ) -> dict:
        """Convenience method matching API contract.

        Args:
            question: User's question
            grade: Grade level
            subject: Subject
            user_role: User role
            preferences: Response preferences

        Returns:
            ChatResponse-compatible dict
        """
        return await self.run(
            query=question,
            grade=grade,
            subject=subject,
            user_role=user_role,
            preferences=preferences,
        )

    async def health_check(self) -> dict:
        """Check pipeline health.

        Returns:
            Health status dict
        """
        retriever_health = await self.retriever.health_check()
        reranker_available = self.reranker.is_available

        return {
            "status": "healthy" if retriever_health.get("status") == "healthy" else "degraded",
            "retriever": retriever_health,
            "reranker": {"available": reranker_available},
        }
