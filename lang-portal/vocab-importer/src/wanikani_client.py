import requests
from typing import List, Dict, Any, Optional, Callable

class WanikaniClient:
    """Client for interacting with the Wanikani API."""
    
    BASE_URL = "https://api.wanikani.com/v2"
    
    def __init__(self, api_key: str, progress_callback: Optional[Callable[[float], None]] = None):
        """Initialize client with API key and optional progress callback.
        
        Args:
            api_key: Wanikani API key
            progress_callback: Optional callback for reporting progress (0-100)
        """
        self.headers = {
            "Authorization": f"Bearer {api_key}"
        }
        self.progress_callback = progress_callback
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get user information from Wanikani API."""
        response = requests.get(f"{self.BASE_URL}/user", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_subjects(self, types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Get subjects from Wanikani API with pagination.
        
        Args:
            types: Optional list of subject types to filter by (e.g. ["kanji", "vocabulary"])
            
        Returns:
            List of subject dictionaries
        """
        params = {}
        if types:
            params["types"] = ",".join(types)
        
        next_url = f"{self.BASE_URL}/subjects"
        subjects = []
        
        # Get first page to determine total pages
        response = requests.get(next_url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Process first page
        subjects.extend(data["data"])
        next_url = data["pages"].get("next_url")
        total_count = data["total_count"]
        
        # Get total pages from headers
        total_pages = max(1, int(total_count / 1000))
        current_page = 1
        
        # Report initial progress
        if self.progress_callback:
            self.progress_callback((current_page / total_pages))
        
        # Get remaining pages
        while next_url:
            response = requests.get(
                next_url,
                headers=self.headers,
                params=params if next_url == f"{self.BASE_URL}/subjects" else None
            )
            response.raise_for_status()
            data = response.json()
            
            subjects.extend(data["data"])
            next_url = data["pages"].get("next_url")
            
            # Update progress
            current_page += 1
            if self.progress_callback:
                self.progress_callback((current_page / total_pages))
        
        return subjects
