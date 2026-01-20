"""Chroma vector store implementation."""

from somaai.modules.knowledge.vectorstore import VectorStore


class ChromaStore(VectorStore):
    """Chroma vector store."""

    async def add(self, texts: list[str], embeddings: list[list[float]]) -> None:
        """Add documents to Chroma."""
        pass

    async def search(self, embedding: list[float], top_k: int = 5) -> list[dict]:
        """Search Chroma for similar documents."""
        return []

    async def delete(self, ids: list[str]) -> None:
        """Delete documents from Chroma."""
        pass
