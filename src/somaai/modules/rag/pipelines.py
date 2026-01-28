"""RAG pipelines for answer generation."""

from typing import Protocol

from somaai.modules.rag.mock_retriever import MockRetriever
from somaai.modules.rag.prompts import (
    build_analogy_prompt,
    build_answer_prompt,
    build_realworld_prompt,
)
from somaai.modules.rag.types import RAGInput, RAGResult
from somaai.providers.llm import LLMClient


class BaseRAGPipeline(Protocol):
    """Protocol for RAG pipeline implementations."""

    async def run(self, inp: RAGInput) -> RAGResult:
        """Execute RAG pipeline.

        Args:
            inp: RAG input with query and context

        Returns:
            RAG result with answer and citations
        """
        ...


class MockRAGPipeline:
    """Mock RAG pipeline using in-memory chunks and LLM."""

    def __init__(self, llm: LLMClient, top_k: int = 3):
        """Initialize mock pipeline.

        Args:
            llm: LLM client for generation
            top_k: Number of chunks to retrieve
        """
        self.llm = llm
        self.retriever = MockRetriever(top_k=top_k)

    async def run(self, inp: RAGInput) -> RAGResult:
        """Execute mock RAG pipeline.

        Args:
            inp: RAG input with query and context

        Returns:
            RAG result with answer, chunks, and optional enhancements
        """
        # 1. Retrieve chunks
        chunks = await self.retriever.retrieve(inp)

        # 2. Build answer prompt
        context_snippets = [chunk.snippet for chunk in chunks]
        answer_prompt = build_answer_prompt(inp, context_snippets)

        # 3. Generate answer
        answer = await self.llm.generate(answer_prompt)

        # 4. Determine sufficiency
        sufficiency = (
            "sufficient" if chunks and len(answer.strip()) > 30 else "insufficient"
        )

        # 5. Generate optional enhancements
        analogy = None
        if inp.enable_analogy and answer:
            analogy_prompt = build_analogy_prompt(inp, answer)
            analogy = await self.llm.generate(analogy_prompt)

        realworld_context = None
        if inp.enable_realworld and answer:
            realworld_prompt = build_realworld_prompt(inp, answer)
            realworld_context = await self.llm.generate(realworld_prompt)

        return RAGResult(
            answer=(
                answer
                or "I couldn't find enough information to answer your question."
            ),
            sufficiency=sufficiency,
            retrieved_chunks=chunks,
            analogy=analogy,
            realworld_context=realworld_context,
        )
