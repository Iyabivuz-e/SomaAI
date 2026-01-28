"""Factory for creating RAG pipeline instances."""

from somaai.modules.rag.pipelines import BaseRAGPipeline, MockRAGPipeline
from somaai.providers.llm import LLMClient
from somaai.settings import Settings


def get_rag_pipeline(settings: Settings, llm: LLMClient) -> BaseRAGPipeline:
    """Create RAG pipeline based on settings."""
    _backend = (settings.llm_backend or "mock").lower()

    # For now, always return MockRAGPipeline
    # Later can add: if backend == "openai": return OpenAIRAGPipeline(llm)
    return MockRAGPipeline(llm=llm)
