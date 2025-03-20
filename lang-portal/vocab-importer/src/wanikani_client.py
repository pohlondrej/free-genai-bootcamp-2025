import os
import json
import requests
from typing import Dict, Any, List

class WanikaniClient:
    BASE_URL = "https://api.wanikani.com/v2"
    API_REVISION = "20170710"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Wanikani-Revision": self.API_REVISION
        }

    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information to verify API access."""
        response = requests.get(
            f"{self.BASE_URL}/user",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_subjects(self, types: List[str] = None) -> List[Dict[str, Any]]:
        """Get all subjects from WaniKani API, handling pagination.
        
        Args:
            types: List of subject types to fetch (e.g., ["kanji", "vocabulary"])
        """
        params = {}
        if types:
            params["types"] = ",".join(types)

        all_subjects = []
        next_url = f"{self.BASE_URL}/subjects"
        page = 1

        while next_url:
            print(f"\nFetching page {page}...")
            response = requests.get(
                next_url,
                headers=self.headers,
                params=params if next_url == f"{self.BASE_URL}/subjects" else None
            )
            response.raise_for_status()
            data = response.json()
            
            subjects = data["data"]
            all_subjects.extend(subjects)
            
            # Show last item of this page
            if subjects:
                last_item = subjects[-1]
                print(f"Last item on page {page}: Type={last_item['object']}, Level={last_item['data']['level']}, Character={last_item['data']['characters']}")
            
            # Update next_url for pagination
            next_url = data["pages"]["next_url"]
            page += 1
        
        print(f"\nTotal subjects collected: {len(all_subjects)}")
        return all_subjects
