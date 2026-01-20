"""Tests for feedback endpoint."""

import pytest
from httpx import AsyncClient


class TestFeedbackEndpoint:
    """Test cases for /api/v1/feedback endpoint."""

    @pytest.mark.asyncio
    async def test_submit_feedback_success(self, client: AsyncClient):
        """POST /feedback with valid data returns feedback_id."""
        pass

    @pytest.mark.asyncio
    async def test_submit_feedback_requires_message_id(self, client: AsyncClient):
        """POST /feedback without message_id returns 400."""
        pass

    @pytest.mark.asyncio
    async def test_submit_feedback_invalid_message_id(self, client: AsyncClient):
        """POST /feedback with non-existent message_id returns 400."""
        pass

    @pytest.mark.asyncio
    async def test_submit_feedback_requires_is_useful(self, client: AsyncClient):
        """POST /feedback without is_useful returns 422."""
        pass

    @pytest.mark.asyncio
    async def test_submit_feedback_with_text_and_tags(self, client: AsyncClient):
        """POST /feedback with optional text and tags succeeds."""
        pass
