from typing import List, Dict, Any

class DataProcessor:
    def __init__(self, user_level: int):
        """Initialize processor with user's current level.
        
        Args:
            user_level: Current level of the user
        """
        self.user_level = user_level

    def filter_by_level(self, subjects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter subjects to only include items at or below user's level.
        
        Args:
            subjects: List of subjects from Wanikani API
            
        Returns:
            List of filtered subjects
        """
        filtered = [
            subject for subject in subjects
            if (subject["data"]["level"] <= self.user_level 
                and subject["data"]["hidden_at"] is None)
        ]
        
        return filtered

    def transform_kanji(self, kanji: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a kanji subject into the format needed for SQL generation.
        
        Args:
            kanji: A kanji subject from Wanikani API
            
        Returns:
            Dictionary with only the needed fields in the correct format
        """
        # Find primary meaning
        primary_meaning = next(
            meaning["meaning"] for meaning in kanji["data"]["meanings"]
            if meaning["primary"]
        )
        
        # Find primary reading and its type
        primary_reading = next(
            reading for reading in kanji["data"]["readings"]
            if reading["primary"]
        )
        
        return {
            "id": kanji["id"],
            "kanji_level": f"WK_{kanji['data']['level']}",
            "symbol": kanji["data"]["characters"],
            "meanings": primary_meaning,
            "primary_reading": primary_reading["reading"],
            "primary_reading_type": primary_reading["type"]
        }

    def transform_vocabulary(self, vocabulary: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a vocabulary subject into the format needed for SQL generation.
        
        Args:
            vocabulary: A vocabulary subject from Wanikani API
            
        Returns:
            Dictionary with only the needed fields in the correct format
        """
        # Find primary meaning (english)
        primary_meaning = next(
            meaning["meaning"] for meaning in vocabulary["data"]["meanings"]
            if meaning["primary"]
        )
        
        # Find primary reading (kana)
        primary_reading = next(
            reading for reading in vocabulary["data"]["readings"]
            if reading["primary"]
        )
        
        return {
            "id": vocabulary["id"],
            "word_level": f"WK_{vocabulary['data']['level']}",
            "japanese": vocabulary["data"]["characters"],
            "kana": primary_reading["reading"],
            "romaji": "",  # We'll need to implement romaji conversion
            "english": primary_meaning
        }
