"""Metadata endpoint schemas."""

from typing import List, Optional

from pydantic import BaseModel, Field


class GradeResponse(BaseModel):
    """Grade level metadata.
    
    Returned by GET /api/v1/meta/grades.
    """
    
    id: str = Field(..., description="Grade ID (e.g., 'P1', 'S3')")
    name: str = Field(..., description="Display name (e.g., 'Primary 1', 'Senior 3')")
    display_order: int = Field(..., description="Sort order for UI")
    level: str = Field(..., description="Level category (primary/secondary)")


class SubjectResponse(BaseModel):
    """Subject metadata.
    
    Returned by GET /api/v1/meta/subjects.
    """
    
    id: str = Field(..., description="Subject ID")
    name: str = Field(..., description="Display name")
    display_order: int = Field(..., description="Sort order for UI")
    icon: Optional[str] = Field(None, description="Icon identifier for UI")


class TopicResponse(BaseModel):
    """Topic metadata.
    
    Returned by GET /api/v1/meta/topics.
    Topics are hierarchical and tied to grade+subject.
    """
    
    id: str = Field(..., description="Topic ID")
    name: str = Field(..., description="Topic name")
    grade: str = Field(..., description="Grade ID")
    subject: str = Field(..., description="Subject ID")
    parent_id: Optional[str] = Field(None, description="Parent topic ID (for sub-topics)")
    children: List["TopicResponse"] = Field(default_factory=list, description="Child topics")
    document_count: int = Field(0, description="Number of documents covering this topic")


# Required for self-referencing model
TopicResponse.model_rebuild()
