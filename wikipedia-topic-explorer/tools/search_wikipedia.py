import wikipediaapi
from typing import Dict

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
        
        # Search for the page
        page = wiki.page(topic)
        
        if not page.exists():
            return {
                "title": topic,
                "summary": f"No Wikipedia article found for '{topic}'"
            }
            
        # Get first few paragraphs (up to 500 characters) to keep it concise
        summary = page.summary[:500]
        if len(page.summary) > 500:
            summary = summary.rsplit('.', 1)[0] + '.'  # Trim to last complete sentence
            
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
    result = search_wikipedia("Mount Fuji")
    print(result)
