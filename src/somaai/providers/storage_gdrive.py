"""Google Drive storage backend (stub).

Placeholder for Google Drive integration.
Requires service account credentials.
"""

from typing import BinaryIO

from somaai.providers.storage import StorageBackend


class GDriveStorage(StorageBackend):
    """Google Drive storage backend.

    Stores files in Google Drive using service account authentication.
    Suitable for production deployments requiring shared storage.

    Configuration env vars:
        - GDRIVE_CREDENTIALS_PATH: Path to service account JSON
        - GDRIVE_FOLDER_ID: Root folder ID for storage
    """

    def __init__(
        self,
        credentials_path: str | None = None,
        folder_id: str | None = None,
    ):
        """Initialize Google Drive storage.

        Args:
            credentials_path: Path to service account credentials JSON
            folder_id: Google Drive folder ID as root
        """
        pass

    async def save(self, file: BinaryIO, path: str) -> str:
        """Upload file to Google Drive.

        Args:
            file: File-like object to upload
            path: Virtual path (used as filename/folder structure)

        Returns:
            Google Drive file ID
        """
        pass

    async def get(self, path: str) -> bytes | None:
        """Download file from Google Drive.

        Args:
            path: File ID or virtual path

        Returns:
            File content as bytes, or None if not found
        """
        pass

    async def get_url(self, path: str, expires_in: int = 3600) -> str | None:
        """Get shareable URL for Google Drive file.

        Args:
            path: File ID or virtual path
            expires_in: Ignored (Drive links don't expire)

        Returns:
            Shareable URL for the file
        """
        pass

    async def delete(self, path: str) -> bool:
        """Delete file from Google Drive.

        Args:
            path: File ID or virtual path

        Returns:
            True if deleted, False if not found
        """
        pass

    async def exists(self, path: str) -> bool:
        """Check if file exists in Google Drive.

        Args:
            path: File ID or virtual path

        Returns:
            True if file exists
        """
        pass
