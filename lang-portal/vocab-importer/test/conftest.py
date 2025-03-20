import pytest
from pathlib import Path
from unittest.mock import MagicMock

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary directory for test outputs."""
    output_dir = tmp_path / "vocab_importer_test"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

@pytest.fixture
def mock_wanikani_api_key():
    """Mock API key for testing."""
    return "test_api_key_12345"

@pytest.fixture
def mock_user_info():
    """Mock user info response."""
    return {
        "data": {
            "level": 3,
            "username": "test_user"
        }
    }

@pytest.fixture
def mock_subjects():
    """Mock paginated subjects response."""
    # First page response
    response1 = MagicMock()
    response1.headers = {
        'X-Total-Count': '2',
        'X-Per-Page': '1',
        'X-Current-Page': '1'
    }
    response1.json.return_value = {
        "data": [{
            "id": 1,
            "object": "kanji",
            "data": {
                "level": 1,
                "characters": "一",
                "meanings": [{"meaning": "One", "primary": True}],
                "readings": [{"reading": "いち", "primary": True, "type": "onyomi"}],
                "hidden_at": None
            }
        }],
        "pages": {
            "next_url": "page2"
        }
    }
    
    # Second page response
    response2 = MagicMock()
    response2.headers = {
        'X-Total-Count': '2',
        'X-Per-Page': '1',
        'X-Current-Page': '2'
    }
    response2.json.return_value = {
        "data": [{
            "id": 2467,
            "object": "vocabulary",
            "data": {
                "level": 1,
                "characters": "一つ",
                "meanings": [{"meaning": "One Thing", "primary": True}],
                "readings": [{"reading": "ひとつ", "primary": True}],
                "hidden_at": None
            }
        }],
        "pages": {
            "next_url": None
        }
    }
    
    return [response1, response2]
