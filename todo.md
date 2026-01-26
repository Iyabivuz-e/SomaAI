Todo:::::


 
 
 30
        request: FeedbackRequest,
        actor_id: str | None = None,
    ) -> FeedbackResponse:
Copilot AI
yesterday

actor_id is typed as str | None and passed directly into the Feedback model, but the actor_id column is declared nullable=False, so calling this service with actor_id=None would violate the DB constraint. Either make actor_id a required str in the service API (matching the DB schema) or add defensive handling for None (e.g., generate a fallback or raise a clear error) to keep the type annotation and runtime behavior consistent.
