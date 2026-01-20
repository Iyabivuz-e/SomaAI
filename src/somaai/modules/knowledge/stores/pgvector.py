"""PGVector store implementation."""

from somaai.modules.knowledge.vectorstore import VectorStore


class PGVectorStore(VectorStore):
    """PGVector store."""

    async def add(self, texts: list[str], embeddings: list[list[float]]) -> None:
        """Add documents to PGVector."""
        pass

    async def search(self, embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search PGVector for similar documents."""
        return []

    async def delete(self, ids: list[str]) -> None:
        """Delete documents from PGVector."""
        pass
