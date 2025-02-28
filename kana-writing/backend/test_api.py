import pytest
from fastapi.testclient import TestClient
from main import app
from kana_dict import KANA_WORDS

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_random_word():
    response = client.get("/word/random")
    assert response.status_code == 200
    data = response.json()
    
    assert "word" in data
    word = data["word"]
    assert "kana" in word
    assert "romaji" in word
    
    # Verify word exists in our dictionary
    assert any(w["kana"] == word["kana"] for w in KANA_WORDS)
