"""
Audio Storage Service for AI News Broadcaster.
Handles audio file storage and retrieval for broadcasted news.
"""

import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
import aiofiles

from app.core.config import settings


class AudioStorageService:
    """Service for managing audio files for broadcasts."""
    
    def __init__(self):
        # For local development - store in a local directory
        self.storage_path = Path("./audio_files")
        self.storage_path.mkdir(exist_ok=True)
        
    async def save_audio_file(self, file: UploadFile, broadcast_id: int) -> str:
        """
        Save an audio file and return its URL.
        
        Args:
            file: The uploaded audio file
            broadcast_id: ID of the broadcast this audio belongs to
            
        Returns:
            URL of the saved audio file
        """
        # Generate unique filename
        file_extension = file.filename.split(".")[-1] if file.filename else "mp3"
        filename = f"broadcast_{broadcast_id}_{uuid.uuid4().hex}.{file_extension}"
        
        # Save file locally for development
        file_path = self.storage_path / filename
        
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        # Return local URL (in production, this would be a cloud storage URL)
        return f"/audio/{filename}"
        
    def get_audio_url(self, broadcast_id: int) -> str:
        """
        Get the URL of an audio file for a broadcast.
        
        Args:
            broadcast_id: ID of the broadcast
            
        Returns:
            URL of the audio file or empty string if not found
        """
        # In a real implementation, this would check cloud storage
        return f"/audio/broadcast_{broadcast_id}_*.mp3"
        
    def cleanup_old_files(self, days_to_keep: int = 7) -> None:
        """
        Clean up old audio files (not implemented for local development).
        
        Args:
            days_to_keep: Number of days to keep files
        """
        # In production, this would clean up old files from cloud storage
        pass


# Global instance
audio_storage_service = AudioStorageService()