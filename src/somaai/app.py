"""FastAPI application factory."""

from fastapi import FastAPI

from somaai.api.router import api_router
from somaai.health import health_router
from somaai.middleware import setup_middleware
from somaai.settings import settings
from somaai.providers.llm import get_llm
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan."""
    ## We create the LLM instance here to ensure it's ready when needed.
    app.state.llm = get_llm(settings)

    try:
        yield
    finally:
        app.state.llm = None

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
        lifespan=lifespan,
    )

    setup_middleware(app)
    app.include_router(health_router)
    app.include_router(api_router, prefix="/api")

    return app
