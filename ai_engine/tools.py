"""
Custom tools for CrewAI agents.

This module defines tools that agents can use to perform actions,
such as searching the web or crawling websites for data.
"""
from typing import Optional
from crewai.tools import BaseTool
from pydantic import Field


class DuckDuckGoSearchTool(BaseTool):
    """
    Tool for searching the web using DuckDuckGo.

    This is a wrapper around the duckduckgo-search library
    that provides web search capabilities to agents.
    """

    name: str = "DuckDuckGo Search"
    description: str = (
        "Search the web using DuckDuckGo. "
        "Use this tool when you need to find current information about "
        "a topic, company, market trends, or any other web-searchable data. "
        "Input should be a search query string."
    )

    def _run(self, query: str) -> str:
        """
        Execute a web search using DuckDuckGo.

        Args:
            query: The search query string

        Returns:
            Search results as a formatted string
        """
        try:
            from duckduckgo_search import DDGS
            import time

            results = []
            
            # Try with different configurations
            try:
                with DDGS() as ddgs:
                    # Fetch top 5 search results with timeout
                    search_results = list(ddgs.text(
                        query, 
                        max_results=5,
                        region="wt-wt",  # Worldwide
                    ))
                    
                    for result in search_results:
                        results.append(
                            f"Title: {result.get('title', 'N/A')}\n"
                            f"URL: {result.get('href', 'N/A')}\n"
                            f"Summary: {result.get('body', 'N/A')}\n"
                        )
            except Exception as e:
                # If first attempt fails, try with a small delay
                time.sleep(1)
                with DDGS() as ddgs:
                    search_results = list(ddgs.text(query, max_results=3))
                    for result in search_results:
                        results.append(
                            f"Title: {result.get('title', 'N/A')}\n"
                            f"URL: {result.get('href', 'N/A')}\n"
                            f"Summary: {result.get('body', 'N/A')}\n"
                        )

            if results:
                return "\n---\n".join(results)
            
            # If still no results, return a helpful message
            return (
                f"No search results found for '{query}'. "
                "This might be due to network restrictions or rate limiting. "
                "The agent should proceed with available knowledge."
            )

        except ImportError:
            return (
                "Error: duckduckgo-search library not installed. "
                "Please install it with: pip install duckduckgo-search"
            )
        except Exception as e:
            # Return error but allow agent to continue
            return (
                f"Search temporarily unavailable for '{query}': {str(e)}. "
                "Please proceed with analysis using available knowledge."
            )



class WebCrawlerTool(BaseTool):
    """
    Placeholder tool for web crawling using Crawl4AI.

    This is a placeholder implementation that will be expanded
    when Crawl4AI is fully integrated.
    """

    name: str = "Web Crawler"
    description: str = (
        "Crawl a specific webpage to extract its content. "
        "Use this tool when you need to read the full content of a webpage. "
        "Input should be a valid URL."
    )
    max_content_length: int = Field(
        default=5000,
        description="Maximum length of crawled content to return"
    )

    def _run(self, url: str) -> str:
        """
        Crawl a webpage and extract its content.

        Args:
            url: The URL to crawl

        Returns:
            Webpage content as a string
        """
        try:
            # Placeholder: Attempt to use Crawl4AI if available
            # For MVP, fall back to a simple requests-based approach
            import requests
            from html import unescape
            import re

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Basic HTML cleanup (remove scripts, styles, tags)
            content = response.text
            content = re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL)
            content = re.sub(r"<style[^>]*>.*?</style>", "", content, flags=re.DOTALL)
            content = re.sub(r"<[^>]+>", " ", content)
            content = unescape(content)
            content = re.sub(r"\s+", " ", content).strip()

            # Truncate if too long
            if len(content) > self.max_content_length:
                content = content[: self.max_content_length] + "..."

            return content or "No content extracted from the page."

        except Exception as e:
            return f"Crawl error for {url}: {str(e)}"


# Instantiate tools for easy import
search_tool = DuckDuckGoSearchTool()
crawler_tool = WebCrawlerTool()
