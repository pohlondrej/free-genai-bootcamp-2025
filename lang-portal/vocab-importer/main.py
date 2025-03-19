import os
from wanikani_client import WanikaniClient

def main():
    api_key = os.environ["WANIKANI_API_KEY"]
    client = WanikaniClient(api_key)
    
    try:
        # Get user info first
        user_info = client.get_user_info()
        print("Successfully connected to Wanikani!")
        print(f"Username: {user_info['data']['username']}")
        print(f"Level: {user_info['data']['level']}")

        # Try fetching subjects
        print("\nFetching kanji and vocabulary subjects...")
        subjects = client.get_subjects(types=["kanji", "vocabulary"])
        
        # Print summary of collected data
        kanji_count = sum(1 for s in subjects if s["object"] == "kanji")
        vocab_count = sum(1 for s in subjects if s["object"] == "vocabulary")
        print(f"\nSummary:")
        print(f"Total kanji: {kanji_count}")
        print(f"Total vocabulary: {vocab_count}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
