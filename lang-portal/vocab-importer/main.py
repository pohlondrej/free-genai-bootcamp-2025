import os
from pathlib import Path
from typing import Dict, Optional, Callable

from src.wanikani_client import WanikaniClient
from src.data_processor import DataProcessor
from src.sql_generator import SQLGenerator

def import_vocabulary(
    api_key: Optional[str] = None, 
    output_dir: Optional[str] = None, 
    progress_callback: Optional[Callable[[str, float], None]] = None
) -> Dict:
    """Import vocabulary from Wanikani and generate SQL migration script.
    
    Args:
        api_key: Wanikani API key. If not provided, will try to get from WANIKANI_API_KEY env var
        output_dir: Directory to write migration.sql to. If not provided, uses current directory
        progress_callback: Optional callback function to report progress. Takes message and percentage
        
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
    
    def report_progress(msg: str, percentage: float):
        """Helper to report progress if callback is provided."""
        if progress_callback:
            progress_callback(msg, percentage)

    # Initialize client with progress mapping
    def wanikani_progress(percentage: float):
        """Map Wanikani progress (0-100) to overall progress (20-80)."""
        mapped_progress = 20 + (percentage * 0.6)  # 0.6 = (80-20)/100
        report_progress("Fetching kanji and vocabulary...", mapped_progress)

    client = WanikaniClient(api_key, wanikani_progress)
    
    # Get user info (0-20%)
    report_progress("Checking user level...", 0)
    user_info = client.get_user_info()
    user_level = user_info["data"]["level"]
    print(f"Processing data for user level: {user_level}")
    report_progress(f"Found user level {user_level}", 20)
    
    # Get subjects (20-80% handled by wanikani_progress callback)
    subjects = client.get_subjects(types=["kanji", "vocabulary"])
    
    # Process data and generate SQL (80-100%)
    report_progress("Processing data...", 80)
    processor = DataProcessor(user_level)
    filtered_subjects = processor.filter_by_level(subjects)
    
    kanji_items = []
    vocab_items = []
    
    for subject in filtered_subjects:
        if subject["object"] == "kanji":
            kanji_items.append(processor.transform_kanji(subject))
        elif subject["object"] == "vocabulary":
            vocab_items.append(processor.transform_vocabulary(subject))
    
    report_progress("Generating SQL migration...", 90)
    generator = SQLGenerator()
    output_file = output_path / "migration.sql"
    
    # Generate SQL and write to file
    migration_sql = generator.generate_migration_script(kanji_items, vocab_items)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(migration_sql)
    
    report_progress(f"Import complete! Imported {len(kanji_items)} kanji and {len(vocab_items)} vocabulary items", 100)
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
