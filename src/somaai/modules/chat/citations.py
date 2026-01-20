"""Chat citation extraction and management."""

from somaai.contracts.chat import CitationResponse


class CitationExtractor:
    """Extracts and formats citations from retrieved chunks.

    Links AI responses to source documents for transparency
    and verification.
    """

    async def extract_citations(
        self,
        chunks: list[dict],
        top_k: int = 5,
    ) -> list[CitationResponse]:
        """Extract citations from retrieved chunks.

        Args:
            chunks: Retrieved document chunks with metadata
            top_k: Maximum citations to include

        Returns:
            List of formatted citations with doc info and page numbers

        Process:
            1. Sort chunks by relevance score
            2. Deduplicate by doc_id + page
            3. Format with view URLs
        """
        pass

    async def get_message_citations(
        self,
        message_id: str,
    ) -> list[CitationResponse]:
        """Get citations for a previously saved message.

        Args:
            message_id: Message identifier

        Returns:
            Citations associated with the message
        """
        pass

    async def save_citations(
        self,
        message_id: str,
        citations: list[CitationResponse],
    ) -> None:
        """Persist citations for a message.

        Args:
            message_id: Message identifier
            citations: Citations to save
        """
        pass

    def _format_view_url(
        self,
        doc_id: str,
        page_number: int,
    ) -> str:
        """Generate stable view URL for a citation.

        Args:
            doc_id: Document identifier
            page_number: Page number

        Returns:
            URL to view the cited page
        """
        pass
