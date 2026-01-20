"""LLM provider."""


class LLMProvider:
    """LLM provider interface."""

    async def generate(self, prompt: str) -> str:
        """Generate a response."""
        return "Generated response"

    async def generate_stream(self, prompt: str):
        """Generate a streaming response."""
        yield "Generated"
        yield " response"

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings."""
        return [[0.0] * 768 for _ in texts]
