from typing import List, Dict, Any

class SQLGenerator:
    def __init__(self):
        """Initialize SQL Generator."""
        pass

    def _escape_sql_string(self, value: str) -> str:
        """Escape single quotes in SQL strings.
        
        Args:
            value: String to escape
            
        Returns:
            Escaped string
        """
        return value.replace("'", "''")

    def generate_kanji_insert(self, kanji_data: Dict[str, Any]) -> str:
        """Generate SQL INSERT statement for a kanji.
        
        Args:
            kanji_data: Transformed kanji data dictionary
            
        Returns:
            SQL INSERT statement as a string
        """
        return (
            "INSERT INTO kanji (id, kanji_level, symbol, meanings, primary_reading, primary_reading_type) "
            f"VALUES ({kanji_data['id']}, '{self._escape_sql_string(kanji_data['kanji_level'])}', "
            f"'{self._escape_sql_string(kanji_data['symbol'])}', '{self._escape_sql_string(kanji_data['meanings'])}', "
            f"'{self._escape_sql_string(kanji_data['primary_reading'])}', '{self._escape_sql_string(kanji_data['primary_reading_type'])}')"
        )

    def generate_vocabulary_insert(self, vocab_data: Dict[str, Any]) -> str:
        """Generate SQL INSERT statement for a vocabulary item.
        
        Args:
            vocab_data: Transformed vocabulary data dictionary
            
        Returns:
            SQL INSERT statement as a string
        """
        return (
            "INSERT INTO words (id, word_level, japanese, kana, romaji, english) "
            f"VALUES ({vocab_data['id']}, '{self._escape_sql_string(vocab_data['word_level'])}', "
            f"'{self._escape_sql_string(vocab_data['japanese'])}', '{self._escape_sql_string(vocab_data['kana'])}', "
            f"'{self._escape_sql_string(vocab_data['romaji'])}', '{self._escape_sql_string(vocab_data['english'])}')"
        )

    def generate_migration_script(self, kanji_list: List[Dict[str, Any]], vocab_list: List[Dict[str, Any]]) -> str:
        """Generate a complete SQL migration script for both kanji and vocabulary.
        
        Args:
            kanji_list: List of transformed kanji data
            vocab_list: List of transformed vocabulary data
            
        Returns:
            Complete SQL migration script as a string
        """
        # Start with table creation
        script = """
-- Create kanji table
CREATE TABLE IF NOT EXISTS kanji (
    id INTEGER PRIMARY KEY,
    kanji_level TEXT NOT NULL,
    symbol TEXT NOT NULL,
    meanings TEXT NOT NULL,
    primary_reading TEXT NOT NULL,
    primary_reading_type TEXT NOT NULL
);

-- Create words table
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,
    word_level TEXT NOT NULL,
    japanese TEXT NOT NULL,
    kana TEXT NOT NULL,
    romaji TEXT NOT NULL,
    english TEXT NOT NULL
);

-- Insert kanji data
"""
        # Add kanji inserts
        for kanji in kanji_list:
            script += self.generate_kanji_insert(kanji) + ";\n"
        
        script += "\n-- Insert vocabulary data\n"
        # Add vocabulary inserts
        for vocab in vocab_list:
            script += self.generate_vocabulary_insert(vocab) + ";\n"
        
        return script
