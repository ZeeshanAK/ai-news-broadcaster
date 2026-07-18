import pytest
from unittest.mock import AsyncMock, patch
from fastapi import UploadFile
from app.services.audio_storage import audio_storage_service


@pytest.mark.asyncio
async def test_save_audio_file():
    """Test saving an audio file"""
    
    # Mock upload file
    mock_file = AsyncMock()
    mock_file.filename = "test_audio.mp3"
    mock_file.read = AsyncMock(return_value=b"fake audio content")
    
    # Test saving audio file
    with patch('aiofiles.open'):
        url = await audio_storage_service.save_audio_file(mock_file, 1)
        
        assert url is not None
        assert url.startswith("/audio/")
        assert "broadcast_1_" in url


def test_get_audio_url():
    """Test getting audio URL"""
    
    url = audio_storage_service.get_audio_url(1)
    
    assert url is not None
    assert url.startswith("/audio/")


def test_cleanup_old_files():
    """Test cleanup functionality (should not error)"""
    
    # This should not raise any exceptions
    audio_storage_service.cleanup_old_files()