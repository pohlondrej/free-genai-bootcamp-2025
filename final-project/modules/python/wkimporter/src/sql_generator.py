from typing import List, Dict, Any
from pydantic import BaseModel

class Group(BaseModel):
    id: int
    name: str

KANJI_GROUP_ID = 1
VOCAB_GROUP_ID = 2
LEVEL_GROUP_ID = 100
KANJI_LEVEL_GROUP_ID = 200
VOCAB_LEVEL_GROUP_ID = 300

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

    def _parse_level(self, level_str: str) -> int:
        """Parse a level string that might have a prefix like 'WK_'.
        
        Args:
            level_str: Level string to parse (e.g., 'WK_1')
            
        Returns:
            Integer level number
        """
        return int(level_str.split('_')[-1])

    def generate_kanji_insert(self, kanji_data: Dict[str, Any]) -> str:
        """Generate SQL INSERT statement for a kanji.
        
        Args:
            kanji_data: Transformed kanji data dictionary
            
        Returns:
            SQL INSERT statement as a string
        """
        return (
            "INSERT INTO kanji (id, kanji_level, symbol, primary_meaning, primary_reading, primary_reading_type) "
            f"VALUES ({kanji_data['id']}, '{self._escape_sql_string(kanji_data['kanji_level'])}', "
            f"'{self._escape_sql_string(kanji_data['symbol'])}', '{self._escape_sql_string(kanji_data['primary_meaning'])}', "
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

    def generate_group_insert(self, user_level: int) -> str:
        """Generate SQL INSERT statement for a group.
        
        Args:
            user_level: Current level of the user
            
        Returns:
            SQL INSERT statement as a string
        """

        # Initialize groups list with base Wanikani groups
        groups = [
            Group(id=KANJI_GROUP_ID, name="Wanikani Kanji"),
            Group(id=VOCAB_GROUP_ID, name="Vocabulary"),
        ]

        # Add Wanikani level groups
        for i in range(1, user_level + 1):
            groups.append(Group(id=i+LEVEL_GROUP_ID, name=f"Wanikani Level {i}"))

        # Add separate kanji level groups
        for i in range(1, user_level + 1):
            groups.append(Group(id=i+KANJI_LEVEL_GROUP_ID, name=f"Wanikani Kanji Level {i}"))

        # Add separate vocabulary level groups
        for i in range(1, user_level + 1):
            groups.append(Group(id=i+VOCAB_LEVEL_GROUP_ID, name=f"Wanikani Vocabulary Level {i}"))

        # Generate SQL INSERT statements to insert groups
        values = [f"({g.id}, '{self._escape_sql_string(g.name)}')" for g in groups]
        return "INSERT INTO groups (id, name) VALUES " + ", ".join(values)

    def generate_all_kanji_group_insert(self, kanji_list: List[Dict[str, Any]]) -> str:
        """Generate SQL INSERT statement for all kanji to the kanji group.
        
        Args:
            kanji_list: List of transformed kanji data
            
        Returns:
            SQL INSERT statement as a string
        """
        if not kanji_list:
            return ""
            
        values = [f"({KANJI_GROUP_ID}, 'kanji', {k['id']})" for k in kanji_list]
        return "INSERT INTO group_items (group_id, item_type, item_id) VALUES " + ",\n".join(values)

    def generate_all_vocabulary_group_insert(self, vocab_list: List[Dict[str, Any]]) -> str:
        """Generate SQL INSERT statement for all vocabulary to the vocabulary group.
        
        Args:
            vocab_list: List of transformed vocabulary data
            
        Returns:
            SQL INSERT statement as a string
        """
        if not vocab_list:
            return ""
            
        values = [f"({VOCAB_GROUP_ID}, 'word', {v['id']})" for v in vocab_list]
        return "INSERT INTO group_items (group_id, item_type, item_id) VALUES " + ",\n".join(values)

    def generate_level_group_insert(self, user_level: int, kanji_list: List[Dict[str, Any]], vocab_list: List[Dict[str, Any]]) -> str:
        """Generate SQL INSERT statement for level groups.
        
        Args:
            user_level: Current level of the user
            kanji_list: List of transformed kanji data
            vocab_list: List of transformed vocabulary data
            
        Returns:
            SQL INSERT statement as a string
        """
        values = []
        
        # Add kanji to their respective level groups
        for kanji in kanji_list:
            level = self._parse_level(kanji['kanji_level'])
            if level <= user_level:
                group_id = LEVEL_GROUP_ID + level
                values.append(f"({group_id}, 'kanji', {kanji['id']})")
        
        # Add vocabulary to their respective level groups
        for vocab in vocab_list:
            level = self._parse_level(vocab['word_level'])
            if level <= user_level:
                group_id = LEVEL_GROUP_ID + level
                values.append(f"({group_id}, 'word', {vocab['id']})")
        
        if not values:
            return ""  # Return empty string if no values to insert
            
        return (
            "INSERT INTO group_items (group_id, item_type, item_id) VALUES " +
            ",\n".join(values)
        )

    def generate_kanji_level_group_insert(self, user_level: int, kanji_list: List[Dict[str, Any]]) -> str:
        """Generate SQL INSERT statement for kanji level groups.
        
        Args:
            user_level: Current level of the user
            kanji_list: List of transformed kanji data
            
        Returns:
            SQL INSERT statement as a string
        """
        values = []
        
        # Add kanji to their respective level groups
        for kanji in kanji_list:
            level = self._parse_level(kanji['kanji_level'])
            if level <= user_level:
                group_id = KANJI_LEVEL_GROUP_ID + level
                values.append(f"({group_id}, 'kanji', {kanji['id']})")
        
        if not values:
            return ""  # Return empty string if no values to insert
            
        return (
            "INSERT INTO group_items (group_id, item_type, item_id) VALUES " +
            ",\n".join(values)
        )

    def generate_vocabulary_level_group_insert(self, user_level: int, vocab_list: List[Dict[str, Any]]) -> str:
        """Generate SQL INSERT statement for vocabulary level groups.
        
        Args:
            user_level: Current level of the user
            vocab_list: List of transformed vocabulary data
            
        Returns:
            SQL INSERT statement as a string
        """
        values = []
        
        # Add vocabulary to their respective level groups
        for vocab in vocab_list:
            level = self._parse_level(vocab['word_level'])
            if level <= user_level:
                group_id = VOCAB_LEVEL_GROUP_ID + level
                values.append(f"({group_id}, 'word', {vocab['id']})")
        
        if not values:
            return ""  # Return empty string if no values to insert
            
        return (
            "INSERT INTO group_items (group_id, item_type, item_id) VALUES " +
            ",\n".join(values)
        )

    def generate_migration_script(self, user_level: int, kanji_list: List[Dict[str, Any]], vocab_list: List[Dict[str, Any]]) -> str:
        """Generate a complete SQL migration script for both kanji and vocabulary.
        
        Args:
            user_level: Current level of the user
            kanji_list: List of transformed kanji data
            vocab_list: List of transformed vocabulary data
            
        Returns:
            Complete SQL migration script as a string
        """
        # Start with table creation
        script = """
-- Insert kanji data
"""
        # Add kanji inserts
        for kanji in kanji_list:
            script += self.generate_kanji_insert(kanji) + ";\n"
        
        script += "\n-- Insert vocabulary data\n"
        # Add vocabulary inserts
        for vocab in vocab_list:
            script += self.generate_vocabulary_insert(vocab) + ";\n"
        
        # Add groups
        script += "\n-- Insert groups\n"
        script += self.generate_group_insert(user_level) + ";\n"

        # Add kanji to groups
        script += "\n-- Insert kanji to groups\n"
        script += self.generate_all_kanji_group_insert(kanji_list) + ";\n"

        # Add vocabulary to groups
        script += "\n-- Insert vocabulary to groups\n"
        script += self.generate_all_vocabulary_group_insert(vocab_list) + ";\n"

        # Add level groups
        script += "\n-- Insert level groups\n"
        script += self.generate_level_group_insert(user_level, kanji_list, vocab_list) + ";\n"
        
        # Add kanji level groups
        script += "\n-- Insert kanji level groups\n"
        script += self.generate_kanji_level_group_insert(user_level, kanji_list) + ";\n"
        
        # Add vocabulary level groups
        script += "\n-- Insert vocabulary level groups\n"
        script += self.generate_vocabulary_level_group_insert(user_level, vocab_list) + ";\n"
        
        return script
