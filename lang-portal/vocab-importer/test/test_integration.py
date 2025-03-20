import os
import pytest
from pathlib import Path
from unittest.mock import patch
from src.wanikani_client import WanikaniClient
from main import import_vocabulary

def test_import_vocabulary_with_api_key(
    temp_output_dir,
    mock_wanikani_api_key,
    mock_user_info,
    mock_subjects
):
    """Test importing vocabulary with explicit API key."""
    # Mock the API responses
    with patch.object(WanikaniClient, 'get_user_info', return_value=mock_user_info), \
         patch.object(WanikaniClient, 'get_subjects', return_value=mock_subjects):
        
        # Run the import
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
    
    # Mock the API responses
    with patch.object(WanikaniClient, 'get_user_info', return_value=mock_user_info), \
         patch.object(WanikaniClient, 'get_subjects', return_value=mock_subjects):
        
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
    
    # Mock the API responses
    with patch.object(WanikaniClient, 'get_user_info', return_value=mock_user_info), \
         patch.object(WanikaniClient, 'get_subjects', return_value=mock_subjects):
        
        result = import_vocabulary(
            api_key=mock_wanikani_api_key,
            output_dir=str(output_dir)
        )
        
        assert output_dir.exists()
        assert Path(result['output_file']).exists()
