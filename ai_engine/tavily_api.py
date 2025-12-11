"""
Tavily Search API Integration (Official SDK)

Tavily is a search API optimized for LLMs and AI agents.
This module provides search functionality with higher priority than Bocha.

Uses official tavily-python SDK: pip install tavily-python
"""
import os
from typing import Dict, List, Any, Optional


def tavily_search(
    query: str,
    max_results: int = 10,
    search_depth: str = "advanced",
    include_answer: bool = True,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform a search using Tavily Search API (official SDK).
    
    Args:
        query: Search query
        max_results: Maximum number of results (1-20)
        search_depth: "basic" for fast, "advanced" for comprehensive
        include_answer: Whether to include AI-generated answer
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
    
    try:
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=api_key)
        
        response = client.search(
            query=query,
            max_results=min(max_results, 20),
            search_depth=search_depth,
            include_answer=include_answer
        )
        
        return {
            "success": True,
            "answer": response.get("answer", ""),
            "results": response.get("results", []),
            "query": response.get("query", query),
            "response_time": response.get("response_time", 0)
        }
        
    except ImportError:
        # Fallback to REST API if SDK not installed
        return _tavily_search_rest(query, max_results, search_depth, include_answer, api_key)
    except Exception as e:
        return {
            "success": False,
            "error": f"Tavily API error: {str(e)}",
            "results": []
        }


def _tavily_search_rest(
    query: str,
    max_results: int,
    search_depth: str,
    include_answer: bool,
    api_key: str
) -> Dict[str, Any]:
    """
    Fallback: Tavily search using REST API directly.
    """
    import requests
    
    api_url = "https://api.tavily.com/search"
    
    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": min(max_results, 20),
        "search_depth": search_depth,
        "include_answer": include_answer
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
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Tavily REST API error: {str(e)}",
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
