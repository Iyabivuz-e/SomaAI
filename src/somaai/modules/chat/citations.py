"""Chat citation extraction and management."""

from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from somaai.contracts.chat import CitationResponse
from somaai.db.models import Chunk, MessageCitation
from somaai.utils.ids import generate_id


class CitationManager:
    """Manages citations for chat messages.

    Handles extraction from chunks, persistence, and retrieval.
    """

    def __init__(self, db: AsyncSession):
        """Initialize with database session."""
        self.db = db

    def extract_from_rag(self, rag_chunks: list[dict]) -> list[CitationResponse]:
        """Extract citations from RAG result chunks.

        Args:
            rag_chunks: List of chunk dictionaries from RAG pipeline

        Returns:
            List of formatted CitationResponse objects
        """
        citations = []
        for chunk in rag_chunks:
            # Skip chunks missing required metadata
            if not chunk.get("doc_id") or not chunk.get("page_start"):
                continue

            citations.append(
                CitationResponse(
                    doc_id=chunk["doc_id"],
                    doc_title=chunk.get("doc_title", "Unknown Document"),
                    page_start=chunk["page_start"],
                    page_end=chunk.get("page_end", chunk["page_start"]),
                    chunk_preview=chunk.get("snippet", "")[:200],
                    view_url=self._format_view_url(
                        chunk["doc_id"], chunk["page_start"]
                    ),
                    relevance_score=chunk.get("score", 0.0),
                )
            )
        return citations

    async def save_citations(
        self,
        message_id: str,
        rag_chunks: list[dict],
    ) -> None:
        """Save citations to database linking message to chunks.

        Args:
            message_id: ID of the message
            rag_chunks: Original RAG chunks containing chunk_ids
        """
        # Map doc_id+page to chunk_id from rag_chunks
        # This assumes citations order matches rag_chunks order or we can map them
        # For simplicity, we'll iterate rag_chunks which have the chunk_id needed for DB

        for idx, chunk_data in enumerate(rag_chunks):
            # Skip if chunk_id is missing (e.g., in mock mode)
            chunk_id = chunk_data.get("chunk_id")
            if not chunk_id:
                continue

            # Create DB record
            citation_db = MessageCitation(
                id=generate_id(),
                message_id=message_id,
                chunk_id=chunk_id,
                relevance_score=chunk_data.get("score", 0.0),
                order=idx,
                snippet=chunk_data.get("snippet", ""),
            )
            self.db.add(citation_db)

    async def get_for_message(self, message_id: str) -> list[CitationResponse]:
        """Retrieve citations for a specific message.

        Args:
            message_id: ID of the message

        Returns:
            List of CitationResponse objects, sorted by order
        """
        result = await self.db.execute(
            select(MessageCitation)
            .options(selectinload(MessageCitation.chunk).selectinload(Chunk.document))
            .where(MessageCitation.message_id == message_id)
            .order_by(MessageCitation.order)
        )
        citations_db = result.scalars().all()

        return [
            CitationResponse(
                doc_id=cit.chunk.document.id,
                doc_title=cit.chunk.document.title,
                page_start=cit.chunk.page_start,
                page_end=cit.chunk.page_end,
                chunk_preview=cast(str, cit.snippet)[:200] if cit.snippet else "",
                view_url=self._format_view_url(
                    cit.chunk.document.id, cit.chunk.page_start
                ),
                relevance_score=cast(float, cit.relevance_score),
            )
            for cit in citations_db
        ]

    def _format_view_url(self, doc_id: str, page_number: int) -> str:
        """Generate stable view URL for a citation."""
        return f"/api/v1/docs/{doc_id}/view?page={page_number}"
