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
    Perform a robust AI search before crew execution using Bocha AI Search.
    
    Args:
        query: The search query
        count: Number of results to fetch
        
    Returns:
        Dict with search_results (formatted string) and references (list)
    """
    try:
        from ai_engine.bocha_api import bocha_ai_search, parse_bocha_response
        
        # Use AI search which provides better context and direct answers
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
                "raw_data": []
            }
        
        # Format results
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
            title = page.get("name", "无标题")
            snippet = page.get("snippet", "")
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
            "raw_data": raw_data
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
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


def save_search_to_db(keyword: str, search_data: dict, report=None):
    """
    Save search results to database with optional report association.
    
    Args:
        keyword: The search keyword
        search_data: Dict containing raw_data, search_results, references
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
        
        SearchResult.objects.create(
            keyword=keyword,
            report=report,
            results_count=len(search_data["raw_data"]),
            results_json=search_data["raw_data"],
            formatted_results=formatted,
            search_source="bocha"
        )
    except Exception as e:
        print(f"Database save error: {e}")
