"""File utilities."""

import os
from pathlib import Path


def ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_file_extension(filename: str) -> str:
    """Get file extension."""
    return os.path.splitext(filename)[1].lower()


def get_file_size(path: str) -> int:
    """Get file size in bytes."""
    return os.path.getsize(path)


def get_all_files(directory: str) -> list[str]:
    """Get all files in a directory."""
    return [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]


def get_all_directories(directory: str) -> list[str]:
    """Get all directories in a directory."""
    return [
        d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))
    ]
