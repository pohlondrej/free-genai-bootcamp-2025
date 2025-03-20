import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import requests

from main import import_vocabulary
from src.wanikani_client import WanikaniClient

def test_import_vocabulary_with_api_key(
    temp_output_dir,
    mock_wanikani_api_key,
    mock_user_info,
    mock_subjects
):
    """Test importing vocabulary with explicit API key."""
    # Mock requests.get to return our paginated responses
    mock_responses = iter(mock_subjects)
    def mock_get(*args, **kwargs):
        return next(mock_responses)

    # Run the import
    with patch.object(WanikaniClient, 'get_user_info', return_value=mock_user_info), \
         patch('requests.get', side_effect=mock_get):
        
        result = import_vocabulary(
            api_key=mock_wanikani_api_key,
            output_dir=str(temp_output_dir)
        )
        
        # Verify the results
        assert result['kanji_count'] == 1
        assert result['vocab_count'] == 1
        assert result['user_level'] == 3
        
        # Check that the file was created
        output_file = Path(result['output_file'])
        assert output_file.exists()
        assert output_file.name == 'migration.sql'
        
        # Verify SQL content
        sql_content = output_file.read_text(encoding='utf-8')
        assert 'CREATE TABLE IF NOT EXISTS kanji' in sql_content
        assert 'CREATE TABLE IF NOT EXISTS words' in sql_content
        assert "INSERT INTO kanji" in sql_content
        assert "INSERT INTO words" in sql_content
        assert "'一'" in sql_content
        assert "'一つ'" in sql_content

def test_import_vocabulary_with_env_var(
    temp_output_dir,
    mock_wanikani_api_key,
    mock_user_info,
    mock_subjects,
    monkeypatch
):
    """Test importing vocabulary using environment variable."""
    # Set up environment
    monkeypatch.setenv('WANIKANI_API_KEY', mock_wanikani_api_key)
    
    # Mock requests.get to return our paginated responses
    mock_responses = iter(mock_subjects)
    def mock_get(*args, **kwargs):
        return next(mock_responses)
    
    # Run the import
    with patch.object(WanikaniClient, 'get_user_info', return_value=mock_user_info), \
         patch('requests.get', side_effect=mock_get):
        
        # Run the import without explicit API key
        result = import_vocabulary(output_dir=str(temp_output_dir))
        
        # Verify the results
        assert result['kanji_count'] == 1
        assert result['vocab_count'] == 1
        assert Path(result['output_file']).exists()

def test_import_vocabulary_no_api_key(temp_output_dir, monkeypatch):
    """Test that import fails properly when no API key is provided."""
    # Clear any existing API key from environment
    monkeypatch.delenv('WANIKANI_API_KEY', raising=False)
    
    with pytest.raises(ValueError) as exc_info:
        import_vocabulary(output_dir=str(temp_output_dir))
    assert "No API key provided" in str(exc_info.value)

def test_import_vocabulary_creates_output_dir(
    tmp_path,
    mock_wanikani_api_key,
    mock_user_info,
    mock_subjects
):
    """Test that output directory is created if it doesn't exist."""
    output_dir = tmp_path / "new_dir" / "subdir"
    assert not output_dir.exists()
    
    # Mock requests.get to return our paginated responses
    mock_responses = iter(mock_subjects)
    def mock_get(*args, **kwargs):
        return next(mock_responses)
    
    # Run the import
    with patch.object(WanikaniClient, 'get_user_info', return_value=mock_user_info), \
         patch('requests.get', side_effect=mock_get):
        
        result = import_vocabulary(
            api_key=mock_wanikani_api_key,
            output_dir=str(output_dir)
        )
        
        assert output_dir.exists()
        assert Path(result['output_file']).exists()

def test_import_vocabulary_progress_reporting(
    temp_output_dir,
    mock_wanikani_api_key,
    mock_user_info,
    mock_subjects
):
    """Test that progress is reported correctly during import."""
    progress_updates = []
    
    def progress_callback(message: str, percentage: float):
        progress_updates.append((message, percentage))
    
    # Mock requests.get to return our paginated responses
    mock_responses = iter(mock_subjects)
    def mock_get(*args, **kwargs):
        return next(mock_responses)
    
    # Run the import with progress reporting
    with patch.object(WanikaniClient, 'get_user_info', return_value=mock_user_info), \
         patch('requests.get', side_effect=mock_get):
        
        result = import_vocabulary(
            api_key=mock_wanikani_api_key,
            output_dir=str(temp_output_dir),
            progress_callback=progress_callback
        )
    
    # Verify progress updates
    assert len(progress_updates) >= 5  # At least initial, user level, subjects, processing, and complete
    
    # Check initial update
    assert progress_updates[0] == ("Checking user level...", 0)
    
    # Check user level found
    assert progress_updates[1] == ("Found user level 3", 20)
    
    # Check some subject updates happened between 20-80%
    subject_updates = [
        update for update in progress_updates 
        if update[0] == "Fetching data from Wanikani..."
    ]
    assert len(subject_updates) > 0
    for _, percentage in subject_updates:
        assert 20 <= percentage <= 80
        assert percentage % 5 == 0  # Should be rounded to nearest 5%
    
    # Check processing updates
    processing_updates = [
        update for update in progress_updates 
        if update[0] == "Processing data..."
    ]
    assert len(processing_updates) > 0
    assert all(update[1] in [80, 85, 90] for update in processing_updates)
    
    # Check SQL generation
    sql_update = next(
        update for update in progress_updates 
        if update[0] == "Generating SQL migration..."
    )
    assert sql_update[1] == 90
    
    # Check completion message
    final_update = progress_updates[-1]
    assert "Import complete!" in final_update[0]
    assert "1 kanji" in final_update[0]
    assert "1 vocabulary" in final_update[0]
    assert final_update[1] == 100
    
    # Verify output
    assert result['kanji_count'] == 1
    assert result['vocab_count'] == 1
    assert Path(result['output_file']).exists()
