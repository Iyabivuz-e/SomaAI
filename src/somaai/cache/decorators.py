"""Caching decorators using aiocache.

aiocache provides:
- Multi-backend support (Redis, Memcached, in-memory)
- Async-first design
- Key builders and serializers
- Decorator-based caching

Install: uv add aiocache[redis]
"""

from collections.abc import Callable
from functools import wraps

try:
    from aiocache import Cache, cached
    from aiocache.serializers import JsonSerializer

    AIOCACHE_AVAILABLE = True
except ImportError:
    AIOCACHE_AVAILABLE = False
    cached = None

from somaai.cache.config import get_cache_config


def _ensure_aiocache():
    """Raise ImportError if aiocache is not installed."""
    if not AIOCACHE_AVAILABLE:
        raise ImportError(
            "aiocache is required for caching decorators. "
            "Install with: uv add aiocache[redis]"
        )


def _build_key(func_name: str, *args, **kwargs) -> str:
    """Build a cache key from function name and arguments."""
    config = get_cache_config()
    key_parts = [config.namespace, func_name]

    # Add positional args (skip 'self' if present)
    for arg in args:
        if hasattr(arg, "__class__") and arg.__class__.__name__ in ("self", "cls"):
            continue
        key_parts.append(str(arg)[:50])  # Truncate long args

    # Add keyword args
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}={str(v)[:50]}")

    return ":".join(key_parts)


def cached_query(
    ttl: int | None = None,
    key_builder: Callable | None = None,
):
    """Cache decorator for query responses.

    Usage:
        @cached_query(ttl=3600)
        async def generate_response(query: str, context: list) -> str:
            ...
    """
    _ensure_aiocache()
    config = get_cache_config()

    return cached(
        ttl=ttl or config.query_ttl,
        cache=Cache.REDIS,
        endpoint=config.redis_url.split("://")[1].split(":")[0]
        if "://" in config.redis_url
        else "localhost",
        port=int(config.redis_url.split(":")[-1].split("/")[0])
        if ":" in config.redis_url
        else 6379,
        namespace=f"{config.namespace}:query",
        serializer=JsonSerializer(),
        key_builder=key_builder
        or (lambda f, *a, **kw: _build_key(f.__name__, *a, **kw)),
    )


def cached_embedding(
    ttl: int | None = None,
    key_builder: Callable | None = None,
):
    """Cache decorator for embedding operations.

    Usage:
        @cached_embedding()
        async def embed_text(text: str) -> list[float]:
            ...
    """
    _ensure_aiocache()
    config = get_cache_config()

    return cached(
        ttl=ttl or config.embedding_ttl,
        cache=Cache.REDIS,
        endpoint=config.redis_url.split("://")[1].split(":")[0]
        if "://" in config.redis_url
        else "localhost",
        port=int(config.redis_url.split(":")[-1].split("/")[0])
        if ":" in config.redis_url
        else 6379,
        namespace=f"{config.namespace}:embed",
        serializer=JsonSerializer(),
        key_builder=key_builder
        or (lambda f, *a, **kw: _build_key(f.__name__, *a, **kw)),
    )


def cached_retrieval(
    ttl: int | None = None,
    key_builder: Callable | None = None,
):
    """Cache decorator for retrieval results.

    Usage:
        @cached_retrieval(ttl=1800)
        async def retrieve_documents(query: str, top_k: int = 10) -> list[dict]:
            ...
    """
    _ensure_aiocache()
    config = get_cache_config()

    return cached(
        ttl=ttl or config.retrieval_ttl,
        cache=Cache.REDIS,
        endpoint=config.redis_url.split("://")[1].split(":")[0]
        if "://" in config.redis_url
        else "localhost",
        port=int(config.redis_url.split(":")[-1].split("/")[0])
        if ":" in config.redis_url
        else 6379,
        namespace=f"{config.namespace}:retrieval",
        serializer=JsonSerializer(),
        key_builder=key_builder
        or (lambda f, *a, **kw: _build_key(f.__name__, *a, **kw)),
    )


# Fallback in-memory cache for development without Redis
class SimpleCache:
    """Simple in-memory cache fallback when Redis is unavailable."""

    def __init__(self):
        self._cache = {}

    def cached(self, ttl: int = 3600):
        """Simple caching decorator."""

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                key = _build_key(func.__name__, *args, **kwargs)
                if key in self._cache:
                    return self._cache[key]
                result = await func(*args, **kwargs)
                self._cache[key] = result
                return result

            return wrapper

        return decorator

    def clear(self):
        """Clear all cached items."""
        self._cache.clear()


# Fallback cache instance
fallback_cache = SimpleCache()
