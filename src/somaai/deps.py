"""Dependency injection."""

from collections.abc import Generator
from somaai.settings import Settings, settings
from somaai.providers.llm import LLMClient
from fastapi import Request

def get_settings() -> Settings:
    """Get settings."""
    return settings

def get_llm_dep(request: Request) -> LLMClient:
    """Get LLM dependency."""
    return request.app.state.llm

def get_db() -> Generator:
    """Get database session."""
    #TODO: implement database session and yield it here
    yield None