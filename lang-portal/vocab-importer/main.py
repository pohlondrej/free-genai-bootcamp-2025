import os
from wanikani_client import WanikaniClient

def main():
    api_key = os.environ["WANIKANI_API_KEY"]
    client = WanikaniClient(api_key)
    
    try:
        user_info = client.get_user_info()
        print("Successfully connected to Wanikani!")
        print(f"Username: {user_info['data']['username']}")
        print(f"Level: {user_info['data']['level']}")
    except Exception as e:
        print(f"Error connecting to Wanikani: {e}")

if __name__ == "__main__":
    main()
