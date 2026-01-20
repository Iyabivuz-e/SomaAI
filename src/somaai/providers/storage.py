"""Storage backend abstraction.

Provides unified interface for file storage with multiple backend support.
"""

from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageBackend(ABC):
    """Abstract base class for storage backends.

    Implement this interface to add new storage backends.
    """

    @abstractmethod
    async def save(self, file: BinaryIO, path: str) -> str:
        """Save a file to storage.

        Args:
            file: File-like object to save
            path: Destination path/key

        Returns:
            Full storage path/URL of saved file
        """
        pass

    @abstractmethod
    async def get(self, path: str) -> bytes | None:
        """Retrieve file content from storage.

        Args:
            path: Storage path/key

        Returns:
            File content as bytes, or None if not found
        """
        pass

    @abstractmethod
    async def get_url(self, path: str, expires_in: int = 3600) -> str | None:
        """Get a URL to access the file.

        Args:
            path: Storage path/key
            expires_in: URL expiration time in seconds (for signed URLs)

        Returns:
            Accessible URL for the file, or None if not found
        """
        pass

    @abstractmethod
    async def delete(self, path: str) -> bool:
        """Delete a file from storage.

        Args:
            path: Storage path/key

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def exists(self, path: str) -> bool:
        """Check if a file exists in storage.

        Args:
            path: Storage path/key

        Returns:
            True if file exists
        """
        pass


def get_storage() -> StorageBackend:
    """Get configured storage backend.

    Returns storage backend based on STORAGE_BACKEND env var:
        - 'local': LocalStorage
        - 'gdrive': GDriveStorage

    Returns:
        Configured StorageBackend instance

    Raises:
        ValueError: If STORAGE_BACKEND is not recognized
    """
    pass
