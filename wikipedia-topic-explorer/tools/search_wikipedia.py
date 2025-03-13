import wikipediaapi
import requests
from typing import Dict, List

def search_wikipedia_api(query: str) -> List[str]:
    """Search Wikipedia using the search API.
    
    Args:
        query: Search query
        
    Returns:
        List of page titles matching the query
    """
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 5  # Get top 5 results
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract page titles from search results
        results = data.get("query", {}).get("search", [])
        return [result["title"] for result in results]
        
    except Exception:
        return []

def search_wikipedia(topic: str, language: str = "en") -> Dict[str, str]:
    """Search Wikipedia for a topic and return the summary.
    
    Args:
        topic: The topic to search for
        language: The Wikipedia language code (default: en)
        
    Returns:
        Dict containing:
        - title: The article title
        - summary: The article summary or error message
    """
    try:
        # Initialize Wikipedia API
        wiki = wikipediaapi.Wikipedia(
            language=language,
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent="WikipediaTopicExplorer/1.0"
        )
        
        # First try direct page access
        page = wiki.page(topic)
        
        # If page doesn't exist or is a disambiguation page, try search API
        if not page.exists() or "may refer to:" in page.summary.lower():
            # Get search results
            search_results = search_wikipedia_api(topic)
            
            if not search_results:
                return {
                    "title": topic,
                    "summary": f"No Wikipedia articles found for '{topic}'"
                }
            
            # Try each result until we find a good one
            for title in search_results:
                page = wiki.page(title)
                if not page.exists() or "may refer to:" in page.summary.lower():
                    continue
                    
                # Found a good article
                break
            else:
                # No good articles found
                return {
                    "title": topic,
                    "summary": f"Could not find a suitable article for '{topic}'"
                }
        
        # Get first few paragraphs (up to 500 characters)
        summary = page.summary[:500]
        if len(page.summary) > 500:
            summary = summary.rsplit('.', 1)[0] + '.'
            
        return {
            "title": page.title,
            "summary": summary
        }
        
    except Exception as e:
        return {
            "title": topic,
            "summary": f"Error fetching Wikipedia article: {str(e)}"
        }

if __name__ == "__main__":
    # Test the function
    test_topics = ["Mount Fuji", "Singularity", "Python", "quantum"]
    for topic in test_topics:
        print(f"\nTesting: {topic}")
        result = search_wikipedia(topic)
        print(f"Title: {result['title']}")
        print(f"Summary: {result['summary'][:100]}...")
