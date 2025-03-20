from typing import Dict, List, Any, Optional, Callable
import requests

class WanikaniClient:
    BASE_URL = "https://api.wanikani.com/v2"

    def __init__(self, api_key: str, progress_callback: Optional[Callable[[float], None]] = None):
        """Initialize Wanikani client.
        
        Args:
            api_key: Wanikani API key
            progress_callback: Optional callback function that takes a float (0-100) to report progress
        """
        self.headers = {
            "Authorization": f"Bearer {api_key}"
        }
        self.progress_callback = progress_callback

    def get_user_info(self) -> Dict[str, Any]:
        """Get user information from Wanikani API."""
        response = requests.get(
            f"{self.BASE_URL}/user",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_subjects(self, types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get all subjects from Wanikani API.
        
        Args:
            types: Optional list of subject types to filter by (e.g. ["kanji", "vocabulary"])
            
        Returns:
            List of subjects
        """
        params = {"types": ",".join(types)} if types else None
        next_url = f"{self.BASE_URL}/subjects"
        subjects = []
        total_pages = None
        current_page = 0

        while next_url:
            print(f"\nFetching page {current_page + 1}...")
            response = requests.get(
                next_url,
                headers=self.headers,
                params=params if next_url == f"{self.BASE_URL}/subjects" else None
            )
            response.raise_for_status()
            data = response.json()

            # Get total pages from first response
            if total_pages is None:
                total_count = int(response.headers.get('X-Total-Count', 0))
                per_page = int(response.headers.get('X-Per-Page', 1000))
                total_pages = (total_count + per_page - 1) // per_page
                current_page = 1
            else:
                current_page += 1

            # Report progress if callback is provided
            if self.progress_callback and total_pages > 0:
                progress = (current_page / total_pages) * 100
                self.progress_callback(progress)

            subjects.extend(data["data"])
            next_url = data["pages"]["next_url"]

            # Print last item for debugging
            if subjects:
                last_item = subjects[-1]
                print(f"Last item on page {current_page}: Type={last_item['object']}, Level={last_item['data']['level']}, Character={last_item['data']['characters']}")

        print(f"\nTotal subjects collected: {len(subjects)}")
        return subjects
