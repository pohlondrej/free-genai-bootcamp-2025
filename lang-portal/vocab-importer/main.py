import os
from wanikani_client import WanikaniClient
from data_processor import DataProcessor
from sql_generator import SQLGenerator

def main():
    # Get API key from environment
    api_key = os.getenv("WANIKANI_API_KEY")
    if not api_key:
        raise ValueError("WANIKANI_API_KEY environment variable is not set")

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
    output_file = "migration.sql"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(migration_sql)
    
    print(f"\nMigration script written to {output_file}")
    print(f"Total kanji: {len(kanji_items)}")
    print(f"Total vocabulary: {len(vocab_items)}")

if __name__ == "__main__":
    main()
