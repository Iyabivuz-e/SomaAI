"""Feedback service for response ratings."""

from somaai.contracts.feedback import FeedbackResponse


class FeedbackService:
    """Service for managing response feedback.

    Collects teacher feedback on AI-generated responses
    for quality improvement and analytics.
    """

    async def submit_feedback(
        self,
        message_id: str,
        is_useful: bool,
        text: str | None = None,
        tags: list[str] | None = None,
    ) -> FeedbackResponse:
        """Submit feedback for a message.

        Args:
            message_id: Message ID being rated (required)
            is_useful: Whether the response was useful
            text: Optional detailed feedback text
            tags: Optional feedback categories/tags

        Returns:
            Created feedback record

        Raises:
            ValueError: If message_id doesn't exist
        """
        pass

    async def get_feedback_for_message(
        self,
        message_id: str,
    ) -> FeedbackResponse | None:
        """Get feedback for a specific message.

        Args:
            message_id: Message ID

        Returns:
            Feedback record or None if not submitted
        """
        pass

    async def get_feedback_stats(
        self,
        days: int = 30,
    ) -> dict:
        """Get aggregate feedback statistics.

        Args:
            days: Number of days to include

        Returns:
            Stats dict with:
            - total_feedback: count
            - useful_pct: percentage marked useful
            - common_tags: most common feedback tags
        """
        pass
