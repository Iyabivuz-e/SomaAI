"""Qdrant vector store implementation."""

from somaai.modules.knowledge.vectorstore import VectorStore


class QdrantStore(VectorStore):
    """Qdrant vector store."""

    async def add(self, texts: list[str], embeddings: list[list[float]]) -> None:
        """Add documents to Qdrant."""
        pass

    async def search(self, embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search Qdrant for similar documents."""
        return []

    async def delete(self, ids: list[str]) -> None:
        """Delete documents from Qdrant."""
        pass
