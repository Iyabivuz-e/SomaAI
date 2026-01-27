"""Dependency injection."""

from fastapi import Header, Request

from somaai.providers.llm import LLMClient
from somaai.settings import Settings, settings
from somaai.utils.ids import generate_short_id


def get_settings() -> Settings:
    """Get settings."""
    return settings


def get_llm_dep(request: Request) -> LLMClient:
    """Get LLM dependency."""
    return request.app.state.llm


def get_actor_id(x_actor_id: str | None = Header(None, alias="X-Actor-Id")) -> str:
    """Get actor ID from request header.

    If no actor ID is provided, generate a temporary one.
    Frontend should persist and send the actor ID.

    Args:
        x_actor_id: Actor ID from X-Actor-Id header

    Returns:
        Actor ID (provided or generated)
    """
    if x_actor_id and x_actor_id.strip():
        return x_actor_id.strip()

    # Generate temporary ID if not provided
    # This allows API testing without frontend
    return f"anon_{generate_short_id()}"
