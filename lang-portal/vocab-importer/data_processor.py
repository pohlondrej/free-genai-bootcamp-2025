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
        
        # Print summary for debugging
        kanji_count = sum(1 for s in filtered if s["object"] == "kanji")
        vocab_count = sum(1 for s in filtered if s["object"] == "vocabulary")
        print(f"\nFiltered subjects summary (level <= {self.user_level}):")
        print(f"Kanji: {kanji_count}")
        print(f"Vocabulary: {vocab_count}")
        
        return filtered
