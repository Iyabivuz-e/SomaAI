"""Meta service for curriculum metadata operations."""

from typing import List, Optional

from somaai.contracts.meta import GradeResponse, SubjectResponse, TopicResponse


class MetaService:
    """Service for curriculum metadata operations.
    
    Provides access to grades, subjects, and topics data
    from the Rwanda Education Board curriculum.
    """
    
    async def get_grades(self) -> List[GradeResponse]:
        """Get all available grade levels.
        
        Returns:
            List of grades (P1-P6, S1-S6) with display names
            
        Order:
            Returns grades in ascending order (P1, P2, ..., S6)
        """
        pass
    
    async def get_subjects(
        self,
        grade: Optional[str] = None,
    ) -> List[SubjectResponse]:
        """Get subjects available for a grade.
        
        Args:
            grade: Grade ID to filter by (optional)
            
        Returns:
            List of subjects available for the grade
            Returns all subjects if grade is None
        """
        pass
    
    async def get_topics(
        self,
        grade: str,
        subject: str,
    ) -> List[TopicResponse]:
        """Get topics for a grade and subject combination.
        
        Args:
            grade: Grade ID (required)
            subject: Subject ID (required)
            
        Returns:
            List of topics as a tree structure (with children)
            
        Structure:
            Topics are hierarchical - main topics contain sub-topics
        """
        pass
    
    async def get_topic_by_id(self, topic_id: str) -> Optional[TopicResponse]:
        """Get a single topic by ID.
        
        Args:
            topic_id: Topic ID
            
        Returns:
            Topic details or None if not found
        """
        pass
    
    async def get_topics_by_ids(
        self,
        topic_ids: List[str],
    ) -> List[TopicResponse]:
        """Get multiple topics by IDs.
        
        Args:
            topic_ids: List of topic IDs
            
        Returns:
            List of topics (in same order as input IDs)
        """
        pass
