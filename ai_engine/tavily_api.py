"""
Tavily Search API Integration

Tavily is a search API optimized for LLMs and AI agents.
This module provides search functionality with higher priority than Bocha.
"""
import os
import requests
from typing import Dict, List, Any, Optional


def tavily_search(
    query: str,
    max_results: int = 10,
    search_depth: str = "advanced",
    include_answer: bool = True,
    include_raw_content: bool = False,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform a search using Tavily Search API.
    
    Args:
        query: Search query
        max_results: Maximum number of results (1-20)
        search_depth: "basic" for fast, "advanced" for comprehensive
        include_answer: Whether to include AI-generated answer
        include_raw_content: Whether to include raw page content
        api_key: Optional API key override
        
    Returns:
        Dict containing search results and metadata
    """
    if not api_key:
        api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key:
        return {
            "success": False,
            "error": "TAVILY_API_KEY not configured",
            "results": []
        }
    
    api_url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": min(max_results, 20),
        "search_depth": search_depth,
        "include_answer": include_answer,
        "include_raw_content": include_raw_content
    }
    
    try:
        response = requests.post(
            api_url,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "success": True,
            "answer": data.get("answer", ""),
            "results": data.get("results", []),
            "query": data.get("query", query),
            "response_time": data.get("response_time", 0)
        }
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Tavily API timeout",
            "results": []
        }
    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "error": f"Tavily API HTTP error: {e.response.status_code}",
            "results": []
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Tavily API error: {str(e)}",
            "results": []
        }


def parse_tavily_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse Tavily response into a standardized format compatible with Bocha.
    
    Returns:
        Dict with:
        - web_sources: List of parsed webpage objects (same format as Bocha)
        - answer: The AI summary answer
    """
    if not response_data.get("success"):
        return {
            "web_sources": [],
            "answer": "",
            "raw_messages": []
        }
    
    web_sources = []
    results = response_data.get("results", [])
    
    for result in results:
        # Convert Tavily format to Bocha-compatible format
        web_sources.append({
            "name": result.get("title", ""),
            "url": result.get("url", ""),
            "snippet": result.get("content", ""),
            "raw_content": result.get("raw_content", "")
        })
    
    return {
        "web_sources": web_sources,
        "answer": response_data.get("answer", ""),
        "raw_messages": results
    }
