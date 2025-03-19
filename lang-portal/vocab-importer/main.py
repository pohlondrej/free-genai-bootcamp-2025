import os
from wanikani_client import WanikaniClient
from data_processor import DataProcessor

def main():
    api_key = os.environ["WANIKANI_API_KEY"]
    client = WanikaniClient(api_key)
    
    try:
        # Get user info first
        user_info = client.get_user_info()
        print("Successfully connected to Wanikani!")
        print(f"Username: {user_info['data']['username']}")
        print(f"Level: {user_info['data']['level']}")

        # Initialize data processor with user's level
        processor = DataProcessor(user_info["data"]["level"])

        # Fetch all subjects
        print("\nFetching kanji and vocabulary subjects...")
        subjects = client.get_subjects(types=["kanji", "vocabulary"])
        
        # Filter subjects by level
        filtered_subjects = processor.filter_by_level(subjects)
        
        # Print summary of all collected data for comparison
        print("\nAll subjects summary (before filtering):")
        kanji_count = sum(1 for s in subjects if s["object"] == "kanji")
        vocab_count = sum(1 for s in subjects if s["object"] == "vocabulary")
        print(f"Total kanji: {kanji_count}")
        print(f"Total vocabulary: {vocab_count}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
