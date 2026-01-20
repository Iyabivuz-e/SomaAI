"""RAG retriever."""


class Retriever:
    """Document retriever."""

    async def retrieve(self, query: str, top_k: int = 15) -> list[dict]:
        """Retrieve relevant documents."""
        return []
