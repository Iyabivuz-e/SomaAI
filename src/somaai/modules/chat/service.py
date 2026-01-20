"""Chat module service."""


class ChatService:
    """Chat service."""

    async def process_message(self, message: str) -> str:
        """Process a chat message."""
        return f"Response to: {message}"
