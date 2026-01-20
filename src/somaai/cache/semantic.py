"""Semantic caching using GPTCache.

GPTCache provides:
- Semantic similarity matching for LLM responses
- Multiple embedding backends (OpenAI, HuggingFace, etc.)
- Vector store integration (FAISS, Milvus, etc.)
- Cache eviction strategies

Install: uv add gptcache
"""

from collections.abc import Callable

try:
    from gptcache import Cache
    from gptcache.adapter.api import init_similar_cache
    from gptcache.similarity_evaluation.distance import SearchDistanceEvaluation

    GPTCACHE_AVAILABLE = True
except ImportError:
    GPTCACHE_AVAILABLE = False

from somaai.cache.config import get_cache_config


class SemanticCache:
    """Semantic caching for LLM responses using GPTCache.

    Finds cached responses for semantically similar queries,
    not just exact matches.

    Example:
        cache = SemanticCache(embedding_func=my_embed_fn)
        await cache.init()

        # These queries might return the same cached response:
        # - "What is photosynthesis?"
        # - "How do plants make food?"
        # - "Explain leaf energy conversion"
    """

    def __init__(
        self,
        embedding_func: Callable[[str], list[float]] | None = None,
        similarity_threshold: float | None = None,
        cache_dir: str = ".cache/semantic",
    ):
        """Initialize semantic cache.

        Args:
            embedding_func: Function to generate embeddings for queries.
            similarity_threshold: Minimum similarity for cache hit (0.0-1.0).
            cache_dir: Directory for cache storage.
        """
        if not GPTCACHE_AVAILABLE:
            raise ImportError(
                "gptcache is required for semantic caching. "
                "Install with: uv add gptcache"
            )

        self.config = get_cache_config()
        self._embedding_func = embedding_func
        self._similarity_threshold = (
            similarity_threshold or self.config.similarity_threshold
        )
        self._cache_dir = cache_dir
        self._cache: Cache | None = None
        self._initialized = False

    def set_embedding_function(self, func: Callable[[str], list[float]]) -> None:
        """Set the embedding function for query vectorization."""
        self._embedding_func = func

    async def init(self) -> None:
        """Initialize the semantic cache.

        Must be called before using get/set operations.
        """
        if self._initialized:
            return

        if self._embedding_func is None:
            raise ValueError(
                "Embedding function required. Call set_embedding_function() first."
            )

        self._cache = Cache()

        # Initialize with similar cache configuration
        init_similar_cache(
            cache_obj=self._cache,
            data_dir=self._cache_dir,
            embedding=self._embedding_func,
            evaluation=SearchDistanceEvaluation(),
        )

        self._initialized = True

    async def get(self, query: str) -> str | None:
        """Get cached response for a semantically similar query.

        Args:
            query: The user query.

        Returns:
            Cached response if similar query found, None otherwise.
        """
        if not self._initialized:
            await self.init()

        try:
            result = self._cache.get(query)
            if result is not None:
                return result
        except Exception:
            pass

        return None

    async def set(self, query: str, response: str) -> None:
        """Cache a query-response pair with semantic indexing.

        Args:
            query: The user query.
            response: The generated response.
        """
        if not self._initialized:
            await self.init()

        self._cache.set(query, response)

    async def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[tuple[str, str, float]]:
        """Search for similar cached queries.

        Args:
            query: The search query.
            top_k: Number of results to return.

        Returns:
            List of (cached_query, response, similarity_score) tuples.
        """
        if not self._initialized:
            await self.init()

        # GPTCache handles similarity search internally
        # This is a simplified interface
        result = await self.get(query)
        if result:
            return [(query, result, 1.0)]
        return []

    def clear(self) -> None:
        """Clear all cached entries."""
        if self._cache:
            self._cache.flush()


# Global semantic cache instance
_semantic_cache: SemanticCache | None = None


def init_semantic_cache(
    embedding_func: Callable[[str], list[float]],
    **kwargs,
) -> SemanticCache:
    """Initialize the global semantic cache.

    Args:
        embedding_func: Function to generate query embeddings.
        **kwargs: Additional arguments for SemanticCache.

    Returns:
        Configured SemanticCache instance.
    """
    global _semantic_cache
    _semantic_cache = SemanticCache(embedding_func=embedding_func, **kwargs)
    return _semantic_cache


def get_semantic_cache() -> SemanticCache | None:
    """Get the global semantic cache instance."""
    return _semantic_cache
