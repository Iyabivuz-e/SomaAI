"""Chat module service."""

from somaai.contracts.chat import ChatRequest, ChatResponse


class ChatService:
    """Chat service."""

    async def process_message(self, message: str) -> str:
        """Process a chat message."""
        return f"Response to: {message}"

    async def ask(self, data: ChatRequest) -> ChatResponse:
        """Process a chat message."""
        return ChatResponse()

    async def get_message(self, session_id: str) -> ChatResponse:
        """Get messages for a session."""
        return ChatResponse()

    async def get_message_citations(
        self, message_id: str, actor_id: str
    ) -> ChatResponse:
        """Get citations for a message."""
        return ChatResponse()
