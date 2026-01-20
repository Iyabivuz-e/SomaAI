"""RAG prompts."""

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. Answer questions based on the provided context."
)

QUERY_PROMPT = """Context: {context}

Question: {question}

Answer:"""
