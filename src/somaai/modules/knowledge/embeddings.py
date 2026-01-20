"""Embeddings module."""


class EmbeddingModel:
    """Embedding model interface."""

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for texts."""
        pass
