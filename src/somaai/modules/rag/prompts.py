"""Prompt templates for RAG generation."""

from somaai.modules.rag.types import RAGInput


def build_answer_prompt(inp: RAGInput, context_snippets: list[str]) -> str:
    """Build prompt for answer generation.

    Args:
        inp: RAG input with query and context
        context_snippets: Retrieved text snippets to use as context

    Returns:
        Formatted prompt for LLM
    """
    context = "\n\n".join(
        f"[Source {i+1}]: {snippet}" for i, snippet in enumerate(context_snippets)
    )

    role_context = (
        f"You are answering for a {inp.user_role.value}."
        if inp.user_role
        else "You are an educational assistant."
    )

    prompt = f"""You are SomaAI, an educational assistant for Rwanda's curriculum.

{role_context}

Grade Level: {inp.grade.value}
Subject: {inp.subject.value}

Context from curriculum materials:
{context}

Student Question: {inp.query}

Please provide a clear, accurate answer based on the context above.
Keep it appropriate for {inp.grade.value} level.
If the context doesn't contain enough information, say so honestly.

Answer:"""

    return prompt


def build_analogy_prompt(inp: RAGInput, answer: str) -> str:
    """Build prompt for analogy generation.

    Args:
        inp: RAG input with query context
        answer: The main answer to create analogy for

    Returns:
        Formatted prompt for analogy generation
    """
    prompt = f"""Given this educational answer:
"{answer}"

For a {inp.grade.value} {inp.subject.value} student, create a simple analogy
or comparison that helps explain this concept in everyday terms.

Keep it brief (2-3 sentences) and relatable to Rwandan students.

Analogy:"""

    return prompt


def build_realworld_prompt(inp: RAGInput, answer: str) -> str:
    """Build prompt for real-world application.

    Args:
        inp: RAG input with query context
        answer: The main answer to create real-world context for

    Returns:
        Formatted prompt for real-world application
    """
    prompt = f"""Given this educational concept:
"{answer}"

Explain a practical real-world application of this concept that {inp.grade.value}
students in Rwanda would find relevant.

Focus on examples from daily life, local context, or future careers.
Keep it brief (2-3 sentences).

Real-world application:"""

    return prompt
