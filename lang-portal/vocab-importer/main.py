import os
from pathlib import Path
from typing import Dict, Optional
from src.wanikani_client import WanikaniClient
from src.data_processor import DataProcessor
from src.sql_generator import SQLGenerator

def import_vocabulary(api_key: Optional[str] = None, output_dir: Optional[str] = None) -> Dict:
    """Import vocabulary from Wanikani and generate SQL migration script.
    
    Args:
        api_key: Wanikani API key. If not provided, will try to get from WANIKANI_API_KEY env var
        output_dir: Directory to write migration.sql to. If not provided, uses current directory
        
    Returns:
        Dictionary with import statistics:
        {
            'kanji_count': Number of kanji imported,
            'vocab_count': Number of vocabulary items imported,
            'user_level': User's current level,
            'output_file': Path to generated migration file
        }
        
    Raises:
        ValueError: If no API key is provided or found in environment
    """
    # Get API key from parameter or environment
    api_key = api_key or os.getenv("WANIKANI_API_KEY")
    if not api_key:
        raise ValueError("No API key provided and WANIKANI_API_KEY environment variable is not set")

    # Set up output directory
    output_dir = output_dir or os.getcwd()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    client = WanikaniClient(api_key)
    
    # Get user info to determine level
    user_info = client.get_user_info()
    user_level = user_info["data"]["level"]
    print(f"Processing data for user level: {user_level}")
    
    # Initialize processor with user's level
    processor = DataProcessor(user_level)
    
    # Get and filter subjects
    subjects = client.get_subjects(types=["kanji", "vocabulary"])
    filtered_subjects = processor.filter_by_level(subjects)
    
    # Separate and transform kanji and vocabulary
    kanji_items = []
    vocab_items = []
    
    for subject in filtered_subjects:
        if subject["object"] == "kanji":
            kanji_items.append(processor.transform_kanji(subject))
        elif subject["object"] == "vocabulary":
            vocab_items.append(processor.transform_vocabulary(subject))
    
    # Generate SQL migration
    generator = SQLGenerator()
    migration_sql = generator.generate_migration_script(kanji_items, vocab_items)
    
    # Write to file
    output_file = output_path / "migration.sql"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(migration_sql)
    
    print(f"\nMigration script written to {output_file}")
    print(f"Total kanji: {len(kanji_items)}")
    print(f"Total vocabulary: {len(vocab_items)}")
    
    return {
        'kanji_count': len(kanji_items),
        'vocab_count': len(vocab_items),
        'user_level': user_level,
        'output_file': str(output_file)
    }

def main():
    """Command line entry point."""
    try:
        import_vocabulary()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
