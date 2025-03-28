import os
from typing import Dict, Any, Optional, Callable
from pathlib import Path
from tqdm import tqdm

from .src.wanikani_client import WanikaniClient
from .src.data_processor import DataProcessor
from .src.sql_generator import SQLGenerator

def import_vocabulary(
    api_key: Optional[str] = None,
    output_dir: Optional[str] = None,
    progress_callback: Optional[Callable[[str, float], None]] = None
) -> Dict[str, Any]:
    """Import vocabulary from Wanikani and generate SQL migration.
    
    Args:
        api_key: Wanikani API key. If not provided, will try to get from WANIKANI_API_KEY env var
        output_dir: Directory to write SQL migration to. If not provided, uses current directory
        progress_callback: Optional callback function to report progress. Takes message and percentage
        
    Returns:
        Dictionary with import statistics:
        {
            'kanji_count': Number of kanji imported,
            'vocab_count': Number of vocabulary items imported,
            'user_level': User's current level,
            'output_file': Path to generated migration file
        }
    """
    # Get API key from environment if not provided
    if not api_key:
        api_key = os.getenv('WANIKANI_API_KEY')
        if not api_key:
            raise ValueError("No API key provided. Either pass api_key parameter or set WANIKANI_API_KEY environment variable")
    
    # Set up output directory
    if not output_dir:
        output_dir = os.getcwd()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    def report_progress(msg: str, percentage: float):
        """Helper to report progress if callback is provided."""
        # Round all percentages to nearest 5%
        percentage = round(percentage / 5) * 5
        if progress_callback:
            progress_callback(msg, percentage)

    # Initialize client with progress mapping
    def wanikani_progress(percentage: float):
        """Map Wanikani progress (0-100) to overall progress (20-80)."""
        mapped = 20 + (percentage * 60)  # Scale to 20-80% range
        report_progress("Fetching data from Wanikani...", mapped)

    client = WanikaniClient(api_key, wanikani_progress)
    
    # Get user info (0-20%)
    report_progress("Checking user level...", 0)
    user_info = client.get_user_info()
    user_level = user_info["data"]["level"]
    report_progress(f"Found user level {user_level}", 20)
    
    # Get subjects (20-80% handled by wanikani_progress callback)
    subjects = client.get_subjects(types=["kanji", "vocabulary"])
    
    # Process data (80-95%)
    report_progress("Processing data...", 80)
    processor = DataProcessor(user_level)
    filtered_subjects = processor.filter_by_level(subjects)
    
    kanji_items = []
    vocab_items = []
    
    total_items = len(filtered_subjects)
    processed_items = 0
    
    # Process in batches for smoother progress updates
    for subject in filtered_subjects:
        if subject["object"] == "kanji":
            kanji_items.append(processor.transform_kanji(subject))
        elif subject["object"] == "vocabulary":
            vocab_items.append(processor.transform_vocabulary(subject))
        
        processed_items += 1
        
        # Update progress during processing (80-95%)
        if processed_items == total_items // 2:  # Report at 50%
            report_progress("Processing data...", 85)
        elif processed_items == total_items:  # Report at 100%
            report_progress("Processing data...", 90)
    
    # Generate SQL (90-100%)
    report_progress("Generating SQL migration...", 90)
    generator = SQLGenerator()
    output_file = output_path / "migration.sql"
    
    # Generate SQL and write to file
    migration_sql = generator.generate_migration_script(kanji_items, vocab_items)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(migration_sql)
    
    report_progress(f"Import complete! {len(kanji_items)} kanji and {len(vocab_items)} vocabulary items", 100)
    
    return {
        'kanji_count': len(kanji_items),
        'vocab_count': len(vocab_items),
        'user_level': user_level,
        'output_file': str(output_file)
    }

def main():
    """Command-line entry point with progress bar."""
    # Create progress bar with custom format
    pbar = tqdm(
        total=100,
        desc="Starting...",
        bar_format='{desc:<50} : {percentage:5.0f}%|{bar}|',
        ncols=120
    )
    
    def update_progress(message: str, percentage: float):
        """Update progress bar with current status."""
        pbar.n = percentage
        pbar.set_description_str(message[:50])  # Limit message length for consistent formatting
        pbar.refresh()
    
    try:
        result = import_vocabulary(progress_callback=update_progress)
        pbar.close()
        print("\nImport successful!")
        print(f"Imported {result['kanji_count']} kanji")
        print(f"Imported {result['vocab_count']} vocabulary items")
        print(f"Migration file written to: {result['output_file']}")
    except Exception as e:
        pbar.close()
        print(f"\nError: {str(e)}")
        raise

if __name__ == "__main__":
    main()
