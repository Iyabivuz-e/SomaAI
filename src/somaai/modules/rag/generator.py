"""RAG generator."""


class BaseGenerator:
    """Abstract base class for RAG context-based generators."""

    async def generate(self, query: str, context: list[str]) -> str:
        """Generate a response based on the query and provided context."""
        pass


class AnalogyGenerator(BaseGenerator):
    """Generates explanations using analogies derived from context."""

    async def generate(self, query: str, context: list[str]) -> str:
        pass


class RealWorldUseCaseGenerator(BaseGenerator):
    """Generates practical, real-world application scenarios."""

    async def generate(self, query: str, context: list[str]) -> str:
        pass


class CombinedGenerator(BaseGenerator):
    """Synthesizes multiple generation strategies into a unified response."""

    async def generate(self, query: str, context: list[str]) -> str:
        pass
