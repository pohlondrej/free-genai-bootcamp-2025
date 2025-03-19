import os
import requests
from typing import Dict, Any

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
