"""
PreSearch Module - Multi-Source Search with Fallback

This module implements a pre-search strategy that fetches search results
BEFORE the crew runs, injecting them into task descriptions.

Search Priority:
1. Tavily (primary) - optimized for AI agents
2. Bocha (fallback) - Chinese search with AI answers

This bypasses CrewAI's tool calling mechanism which has compatibility
issues with certain LLM APIs (like Volcengine ARK).
"""
import os
import requests
from typing import Optional


def pre_search(query: str, count: int = 20) -> dict:
    """
    Perform a robust AI search before crew execution.
    
    Search Priority:
    1. Tavily Search API (if TAVILY_API_KEY configured)
    2. Bocha AI Search (fallback)
    
    Args:
        query: The search query
        count: Number of results to fetch
        
    Returns:
        Dict with search_results (formatted string), references (list), 
        raw_data (list), and search_source (str)
    """
    # Try Tavily first (higher priority)
    tavily_result = _try_tavily_search(query, count)
    if tavily_result.get("raw_data"):
        print(f"✅ Tavily search returned {len(tavily_result['raw_data'])} results")
        return tavily_result
    
    # Fallback to Bocha
    print("⚠️ Tavily search failed or returned no results, falling back to Bocha...")
    bocha_result = _try_bocha_search(query, count)
    return bocha_result


def _try_tavily_search(query: str, count: int) -> dict:
    """
    Try searching with Tavily API.
    
    Returns:
        Dict with search results or empty dict on failure
    """
    try:
        from ai_engine.tavily_api import tavily_search, parse_tavily_response
        
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            print("⚠️ TAVILY_API_KEY not configured, skipping Tavily search")
            return {"search_results": "", "references": [], "raw_data": []}
        
        print(f"🔍 Trying Tavily search for: {query[:50]}...")
        
        raw_response = tavily_search(
            query,
            max_results=min(count, 20),
            search_depth="advanced",
            include_answer=True,
            api_key=api_key
        )
        
        if not raw_response.get("success"):
            print(f"⚠️ Tavily search failed: {raw_response.get('error', 'Unknown error')}")
            return {"search_results": "", "references": [], "raw_data": []}
        
        parsed = parse_tavily_response(raw_response)
        web_sources = parsed.get("web_sources", [])
        ai_answer = parsed.get("answer", "")
        
        if not web_sources and not ai_answer:
            return {"search_results": "", "references": [], "raw_data": []}
        
        return _format_search_results(web_sources, ai_answer, query, "tavily")
        
    except Exception as e:
        print(f"⚠️ Tavily search exception: {e}")
        return {"search_results": "", "references": [], "raw_data": []}


def _try_bocha_search(query: str, count: int) -> dict:
    """
    Try searching with Bocha API (fallback).
    
    Returns:
        Dict with search results
    """
    try:
        from ai_engine.bocha_api import bocha_ai_search, parse_bocha_response
        
        print(f"🔍 Trying Bocha search for: {query[:50]}...")
        
        raw_response = bocha_ai_search(
            query, 
            count=count, 
            answer=True,
            stream=False
        )
        
        parsed = parse_bocha_response(raw_response)
        web_sources = parsed.get("web_sources", [])
        ai_answer = parsed.get("answer", "")
        
        if not web_sources and not ai_answer:
            return {
                "search_results": f"未找到与 '{query}' 相关的搜索结果。请基于您的专业知识进行分析。",
                "references": [],
                "raw_data": [],
                "search_source": "none"
            }
        
        return _format_search_results(web_sources, ai_answer, query, "bocha")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "search_results": f"搜索失败：{str(e)}。请基于您的专业知识进行分析。",
            "references": [],
            "raw_data": [],
            "search_source": "error"
        }


def _format_search_results(web_sources: list, ai_answer: str, query: str, source: str) -> dict:
    """
    Format search results into a standardized structure.
    
    Args:
        web_sources: List of webpage results
        ai_answer: AI-generated answer/summary
        query: Original search query
        source: Search source name (tavily/bocha)
        
    Returns:
        Formatted dict with search_results, references, raw_data, search_source
    """
    results = []
    references = []
    raw_data = []
    
    # Add AI Answer as the first "source" of insight
    if ai_answer:
        results.append(
            "【AI 智能综述】\n"
            f"{ai_answer}\n"
        )
    
    for i, page in enumerate(web_sources, 1):
        ref_id = f"[Ref-{i}]"
        # Handle both Tavily (name) and Bocha (name) field names
        title = page.get("name", page.get("title", "无标题"))
        snippet = page.get("snippet", page.get("content", ""))
        url = page.get("url", "")
        
        # Truncate snippet for context management
        short_snippet = snippet[:350] + "..." if len(snippet) > 350 else snippet
        
        results.append(
            f"来源 {ref_id}\n"
            f"标题: {title}\n"
            f"内容: {short_snippet}\n"
            f"链接: {url}"
        )
        
        references.append(f"{ref_id} {title}, 链接: {url}")
        
        raw_data.append({
            "ref_id": ref_id,
            "title": title,
            "snippet": snippet,
            "url": url
        })
    
    search_results = "\n\n---\n\n".join(results)
    
    return {
        "search_results": search_results,
        "references": references,
        "raw_data": raw_data,
        "search_source": source
    }


def format_research_data(topic: str, search_data: dict) -> str:
    """
    Format search data into a research context for tasks.
    
    Args:
        topic: The research topic
        search_data: Dict from pre_search()
        
    Returns:
        Formatted research context string
    """
    source_name = search_data.get("search_source", "unknown")
    output = f"## 「{topic}」相关搜索资料（共 {len(search_data['references'])} 条真实来源，来自 {source_name.upper()}）\n\n"
    output += "【重要警告】以下是真实的搜索结果和URL，报告中必须使用这些真实链接，禁止编造假链接！\n\n"
    output += search_data["search_results"]
    output += "\n\n---\n\n## 【必须使用的参考文献】（真实URL，禁止修改）\n\n"
    for ref in search_data["references"]:
        output += f"- {ref}\n"
    output += "\n【强制要求】报告结尾的参考文献必须原样复制上述列表，不得编造 example.com 等假链接！\n"
    
    return output


def save_search_to_db(keyword: str, search_data: dict, report=None):
    """
    Save search results to database with optional report association.
    
    Args:
        keyword: The search keyword
        search_data: Dict containing raw_data, search_results, references, search_source
        report: Optional Report instance to associate with the search result
    """
    try:
        import sys
        from pathlib import Path
        
        backend_dir = Path(__file__).resolve().parent.parent / "backend"
        if str(backend_dir) not in sys.path:
            sys.path.insert(0, str(backend_dir))
        
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
        
        import django
        if not django.apps.apps.ready:
            django.setup()
        
        from apps.reports.models import SearchResult
        
        formatted = f"关键词: {keyword}\n\n{search_data['search_results']}"
        search_source = search_data.get("search_source", "bocha")
        
        SearchResult.objects.create(
            keyword=keyword,
            report=report,
            results_count=len(search_data["raw_data"]),
            results_json=search_data["raw_data"],
            formatted_results=formatted,
            search_source=search_source
        )
    except Exception as e:
        print(f"Database save error: {e}")
