"""Common schemas shared across the API."""

from enum import Enum
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class UserRole(str, Enum):
    """User role in the system."""
    
    STUDENT = "student"
    TEACHER = "teacher"


class GradeLevel(str, Enum):
    """Rwanda education grade levels."""
    
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"
    P6 = "P6"
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"
    S5 = "S5"
    S6 = "S6"


class Subject(str, Enum):
    """Curriculum subjects."""
    
    MATHEMATICS = "mathematics"
    ENGLISH = "english"
    KINYARWANDA = "kinyarwanda"
    FRENCH = "french"
    SCIENCE = "science"
    SOCIAL_STUDIES = "social_studies"
    ICT = "ict"
    ENTREPRENEURSHIP = "entrepreneurship"


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper.
    
    Used for list endpoints that support pagination.
    """
    
    items: List[T] = Field(..., description="List of items in current page")
    total: int = Field(..., description="Total number of items")
    page: int = Field(1, description="Current page number (1-indexed)")
    page_size: int = Field(20, description="Number of items per page")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")
