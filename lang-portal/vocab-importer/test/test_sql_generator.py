import pytest
from sql_generator import SQLGenerator

def test_generate_kanji_insert():
    generator = SQLGenerator()
    
    kanji_data = {
        "id": 440,
        "kanji_level": "WK_1",
        "symbol": "一",
        "meanings": "One",
        "primary_reading": "いち",
        "primary_reading_type": "onyomi"
    }
    
    expected_sql = (
        "INSERT INTO kanji (id, kanji_level, symbol, meanings, primary_reading, primary_reading_type) "
        "VALUES (440, 'WK_1', '一', 'One', 'いち', 'onyomi')"
    )
    
    assert generator.generate_kanji_insert(kanji_data) == expected_sql

def test_generate_vocabulary_insert():
    generator = SQLGenerator()
    
    vocab_data = {
        "id": 2467,
        "word_level": "WK_1",
        "japanese": "一つ",
        "kana": "ひとつ",
        "romaji": "hitotsu",
        "english": "One Thing"
    }
    
    expected_sql = (
        "INSERT INTO words (id, word_level, japanese, kana, romaji, english) "
        "VALUES (2467, 'WK_1', '一つ', 'ひとつ', 'hitotsu', 'One Thing')"
    )
    
    assert generator.generate_vocabulary_insert(vocab_data) == expected_sql

def test_sql_string_escaping():
    generator = SQLGenerator()
    
    vocab_data = {
        "id": 2468,
        "word_level": "WK_1",
        "japanese": "人生",
        "kana": "じんせい",
        "romaji": "jinsei",
        "english": "One's Life"  # Contains a single quote
    }
    
    expected_sql = (
        "INSERT INTO words (id, word_level, japanese, kana, romaji, english) "
        "VALUES (2468, 'WK_1', '人生', 'じんせい', 'jinsei', 'One''s Life')"
    )
    
    assert generator.generate_vocabulary_insert(vocab_data) == expected_sql

def test_generate_migration_script():
    generator = SQLGenerator()
    
    kanji_list = [
        {
            "id": 440,
            "kanji_level": "WK_1",
            "symbol": "一",
            "meanings": "One",
            "primary_reading": "いち",
            "primary_reading_type": "onyomi"
        }
    ]
    
    vocab_list = [
        {
            "id": 2467,
            "word_level": "WK_1",
            "japanese": "一つ",
            "kana": "ひとつ",
            "romaji": "hitotsu",
            "english": "One Thing"
        }
    ]
    
    script = generator.generate_migration_script(kanji_list, vocab_list)
    
    # Check for table creation
    assert "CREATE TABLE IF NOT EXISTS kanji" in script
    assert "CREATE TABLE IF NOT EXISTS words" in script
    
    # Check for inserts
    assert "INSERT INTO kanji" in script
    assert "INSERT INTO words" in script
    
    # Check for specific values
    assert "'一'" in script
    assert "'ひとつ'" in script
    assert "'One Thing'" in script
