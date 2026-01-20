"""Local filesystem storage backend."""

from typing import BinaryIO, Optional

from somaai.providers.storage import StorageBackend


class LocalStorage(StorageBackend):
    """Local filesystem storage backend.
    
    Stores files in a local directory specified by STORAGE_LOCAL_PATH.
    Suitable for development and single-server deployments.
    """
    
    def __init__(self, base_path: str = "./uploads"):
        """Initialize local storage.
        
        Args:
            base_path: Base directory for file storage
        """
        pass
    
    async def save(self, file: BinaryIO, path: str) -> str:
        """Save file to local filesystem.
        
        Creates parent directories if needed.
        
        Args:
            file: File-like object to save
            path: Relative path within base_path
            
        Returns:
            Full path to saved file
        """
        pass
    
    async def get(self, path: str) -> Optional[bytes]:
        """Read file from local filesystem.
        
        Args:
            path: Relative path within base_path
            
        Returns:
            File content as bytes, or None if not found
        """
        pass
    
    async def get_url(self, path: str, expires_in: int = 3600) -> Optional[str]:
        """Get URL to access local file.
        
        For local storage, returns a file:// URL or API endpoint URL.
        
        Args:
            path: Relative path within base_path
            expires_in: Ignored for local storage
            
        Returns:
            URL to access the file
        """
        pass
    
    async def delete(self, path: str) -> bool:
        """Delete file from local filesystem.
        
        Args:
            path: Relative path within base_path
            
        Returns:
            True if deleted, False if not found
        """
        pass
    
    async def exists(self, path: str) -> bool:
        """Check if file exists on local filesystem.
        
        Args:
            path: Relative path within base_path
            
        Returns:
            True if file exists
        """
        pass
