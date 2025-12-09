"""
PreSearch Module - Bypass CrewAI Tool Calling Issues

This module implements a pre-search strategy that fetches search results
BEFORE the crew runs, injecting them into task descriptions.

This bypasses CrewAI's tool calling mechanism which has compatibility
issues with certain LLM APIs (like Volcengine ARK).
"""
import os
import requests
from typing import Optional


def pre_search(query: str, count: int = 20) -> dict:
    """
    Perform a web search before crew execution.
    
    Args:
        query: The search query
        count: Number of results to fetch
        
    Returns:
        Dict with search_results (formatted string) and references (list)
    """
    api_key = os.getenv("BOCHA_API_KEY", "sk-accd71cb3f8b48789e34040d18337912")
    api_url = "https://api.bocha.cn/v1/web-search"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "freshness": "noLimit",
        "summary": True,
        "count": count
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        web_pages = data.get("data", {}).get("webPages", {}).get("value", [])
        
        if not web_pages:
            return {
                "search_results": f"未找到与 '{query}' 相关的搜索结果。请基于您的专业知识进行分析。",
                "references": [],
                "raw_data": []
            }
        
        # Format results
        results = []
        references = []
        raw_data = []
        
        for i, page in enumerate(web_pages, 1):
            ref_id = f"[Ref-{i}]"
            title = page.get("name", "无标题")
            snippet = page.get("snippet", "")
            url = page.get("url", "")
            
            # Truncate snippet for context management
            short_snippet = snippet[:300] + "..." if len(snippet) > 300 else snippet
            
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
            "raw_data": raw_data
        }
        
    except Exception as e:
        return {
            "search_results": f"搜索失败：{str(e)}。请基于您的专业知识进行分析。",
            "references": [],
            "raw_data": []
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
    output = f"## 「{topic}」相关搜索资料（共 {len(search_data['references'])} 条真实来源）\n\n"
    output += "【重要警告】以下是真实的搜索结果和URL，报告中必须使用这些真实链接，禁止编造假链接！\n\n"
    output += search_data["search_results"]
    output += "\n\n---\n\n## 【必须使用的参考文献】（真实URL，禁止修改）\n\n"
    for ref in search_data["references"]:
        output += f"- {ref}\n"
    output += "\n【强制要求】报告结尾的参考文献必须原样复制上述列表，不得编造 example.com 等假链接！\n"
    
    return output


def save_search_to_db(keyword: str, search_data: dict):
    """Save search results to database."""
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
        
        SearchResult.objects.create(
            keyword=keyword,
            results_count=len(search_data["raw_data"]),
            results_json=search_data["raw_data"],
            formatted_results=formatted,
            search_source="bocha"
        )
    except Exception as e:
        print(f"Database save error: {e}")
