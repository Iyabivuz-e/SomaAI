"""RAG pipelines."""

from somaai.modules.rag.generator import CombinedGenerator
from somaai.modules.rag.retriever import Retriever


class RAGPipeline:
    """RAG pipeline."""

    def __init__(self) -> None:
        """Initialize pipeline."""
        self.retriever = Retriever()
        self.generator = CombinedGenerator()

    async def run(self, query: str) -> str:
        """Run the RAG pipeline."""
        documents = await self.retriever.retrieve(query)
        context = [doc.get("content", "") for doc in documents]
        response = await self.generator.generate(query, context)
        return response or ""
