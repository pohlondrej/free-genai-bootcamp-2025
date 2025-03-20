import pytest
from pathlib import Path

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary directory for test outputs."""
    output_dir = tmp_path / "vocab_importer_test"
    output_dir.mkdir()
    return output_dir

@pytest.fixture
def mock_wanikani_api_key():
    """Mock Wanikani API key for testing."""
    return "test_api_key_12345"

@pytest.fixture
def mock_user_info():
    """Mock user info response from Wanikani API."""
    return {
        "data": {
            "level": 3,
            "username": "test_user"
        }
    }

@pytest.fixture
def mock_subjects():
    """Mock subjects response from Wanikani API."""
    return [
        {
            "id": 440,
            "object": "kanji",
            "data": {
                "level": 1,
                "characters": "一",
                "meanings": [{"meaning": "One", "primary": True}],
                "readings": [{"reading": "いち", "primary": True, "type": "onyomi"}],
                "hidden_at": None
            }
        },
        {
            "id": 2467,
            "object": "vocabulary",
            "data": {
                "level": 1,
                "characters": "一つ",
                "meanings": [{"meaning": "One Thing", "primary": True}],
                "readings": [{"reading": "ひとつ", "primary": True}],
                "hidden_at": None
            }
        }
    ]
