import wikipediaapi
import requests
import logging
from typing import Dict, List
from common.llms import LLMProvider

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        
    except Exception as e:
        logger.error(f"Wikipedia search failed: {e}")
        return []

async def search_wikipedia(topic: str, llm_provider: LLMProvider, language: str = "en") -> Dict[str, str]:
    """Search Wikipedia for a topic and return the summary.
    
    Args:
        topic: The topic to search for
        llm_provider: LLM provider to use for processing
        language: The Wikipedia language code (default: en)
        
    Returns:
        Dict containing:
        - title: The article title
        - summary: The article summary or error message
    """
    # First search for matching articles
    titles = search_wikipedia_api(topic)
    if not titles:
        return {
            "title": topic,
            "summary": "No Wikipedia articles found for this topic."
        }
    
    # Get the first article's content
    wiki = wikipediaapi.Wikipedia(language)
    page = wiki.page(titles[0])
    
    if not page.exists():
        return {
            "title": topic,
            "summary": "Wikipedia article not found."
        }
    
    # Get the summary and clean it up using LLM
    summary = page.summary[:1000]  # First 1000 chars
    if not summary:
        return {
            "title": page.title,
            "summary": "No summary available."
        }
    
    # Process the summary with LLM to make it more readable
    try:
        response = await llm_provider.call(f"Please summarize this Wikipedia excerpt in a clear and concise way:\n\n{summary}")
        if isinstance(response, dict) and "summary" in response:
            processed_summary = response["summary"]
        else:
            processed_summary = summary
    except Exception as e:
        logger.error(f"Failed to process summary with LLM: {e}")
        processed_summary = summary
    
    return {
        "title": page.title,
        "summary": processed_summary
    }

if __name__ == "__main__":
    # Test the function
    test_topics = ["Mount Fuji", "Singularity", "Python", "quantum"]
    try:
        from common.llms import LLMFactory
        import asyncio
        
        async def test():
            llm = LLMFactory.create()
            for topic in test_topics:
                print(f"\nSearching for: {topic}")
                result = await search_wikipedia(topic, llm)
                print(f"Title: {result['title']}")
                print(f"Summary: {result['summary']}")
        
        asyncio.run(test())
    except Exception as e:
        print(f"Error: {e}")
