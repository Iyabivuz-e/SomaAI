"""Tests for chat endpoints."""

import pytest
from httpx import AsyncClient


class TestChatEndpoints:
    """Test cases for /api/v1/chat endpoints."""

    @pytest.mark.asyncio
    async def test_ask_returns_required_fields(self, client: AsyncClient):
        """POST /chat/ask should return message_id, response, sufficiency, citations."""
        pass

    @pytest.mark.asyncio
    async def test_ask_requires_query(self, client: AsyncClient):
        """POST /chat/ask without query returns 422."""
        pass

    @pytest.mark.asyncio
    async def test_ask_requires_grade_and_subject(self, client: AsyncClient):
        """POST /chat/ask without grade/subject returns 422."""
        pass

    @pytest.mark.asyncio
    async def test_ask_student_mode(self, client: AsyncClient):
        """POST /chat/ask with user_role=student works correctly."""
        pass

    @pytest.mark.asyncio
    async def test_ask_teacher_mode(self, client: AsyncClient):
        """POST /chat/ask with user_role=teacher includes profile defaults."""
        pass

    @pytest.mark.asyncio
    async def test_get_message_returns_details(self, client: AsyncClient):
        """GET /chat/messages/{id} returns full message details."""
        pass

    @pytest.mark.asyncio
    async def test_get_message_not_found(self, client: AsyncClient):
        """GET /chat/messages/{invalid_id} returns 404."""
        pass

    @pytest.mark.asyncio
    async def test_get_citations_returns_list(self, client: AsyncClient):
        """GET /chat/messages/{id}/citations returns citation list."""
        pass
