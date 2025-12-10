"""
Chapter Generator Module

Handles the generation of individual chapters for long-form reports.
Uses CrewAI or direct LLM calls to generate chapter content with
structured reference output.
"""
import os
import asyncio
from typing import Dict, List, Tuple, Optional
from litellm import completion

from ai_engine.utils import parse_chapter_output, generate_chapter_prompt
from ai_engine.pre_search import pre_search, format_research_data


async def generate_single_chapter(
    topic: str, 
    chapter_info: Dict,
    previous_summary: str = "",
    search_count: int = 10
) -> Tuple[str, List[Dict]]:
    """
    Generate a single chapter with research data and structured references.
    
    Args:
        topic: The main report topic
        chapter_info: Dict with 'title' and 'focus' keys
        previous_summary: Summary of previous chapters for context continuity
        search_count: Number of search results to fetch
        
    Returns:
        Tuple of (chapter_content, list_of_references)
    """
    import chainlit as cl
    
    chapter_title = chapter_info.get('title', '章节')
    chapter_focus = chapter_info.get('focus', '')
    
    # Construct search query from chapter context
    search_query = f"{topic} {chapter_focus}"
    
    # Perform pre-search for this chapter
    search_data = await cl.make_async(lambda: pre_search(search_query, count=search_count))()
    research_context = format_research_data(search_query, search_data)
    
    # Build the generation prompt
    base_prompt = generate_chapter_prompt(topic, chapter_info, previous_summary)
    
    full_prompt = f"""
{base_prompt}

【搜索资料】
以下是关于本章主题的搜索结果，请基于这些真实来源撰写内容：

{research_context}
"""
    
    # Call LLM to generate chapter
    try:
        response = await cl.make_async(lambda: completion(
            model="openai/" + os.getenv("ARK_MODEL_ENDPOINT", "ep-20250603140551-tp9lt"),
            messages=[{"role": "user", "content": full_prompt}],
            api_key=os.getenv("ARK_API_KEY"),
            base_url=os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
            max_tokens=2000
        ))()
        
        raw_output = response.choices[0].message.content.strip()
        
        # Parse the output to extract content and references
        content, refs = parse_chapter_output(raw_output)
        
        # If no refs were parsed, try to use search data refs as fallback
        if not refs and search_data.get('raw_data'):
            refs = []
            for item in search_data['raw_data'][:5]:
                refs.append({
                    "id": item.get('ref_id', '[Ref-1]'),
                    "url": item.get('url', ''),
                    "title": item.get('title', '参考来源')
                })
        
        return content, refs
        
    except Exception as e:
        error_msg = f"章节生成失败: {str(e)}"
        return error_msg, []


async def generate_report_outline(topic: str) -> List[Dict]:
    """
    Generate a structured outline for the report.
    
    Args:
        topic: The report topic
        
    Returns:
        List of chapter info dicts with 'title' and 'focus' keys
    """
    import chainlit as cl
    
    outline_prompt = f"""
请为以下主题生成一份详细的行业分析报告大纲：

主题：{topic}

要求：
1. 生成 4-6 个章节
2. 每个章节有明确的标题和研究重点
3. 章节之间逻辑递进，覆盖行业分析的核心维度
4. 输出 JSON 数组格式

输出格式（严格遵守）：
[
  {{"title": "1. 章节标题", "focus": "本章研究重点关键词"}},
  {{"title": "2. 章节标题", "focus": "本章研究重点关键词"}},
  ...
]

只输出 JSON 数组，不要其他内容。
"""
    
    try:
        response = await cl.make_async(lambda: completion(
            model="openai/" + os.getenv("ARK_MODEL_ENDPOINT", "ep-20250603140551-tp9lt"),
            messages=[{"role": "user", "content": outline_prompt}],
            api_key=os.getenv("ARK_API_KEY"),
            base_url=os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
            max_tokens=1000
        ))()
        
        raw_output = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        import json
        import re
        
        # Try to find JSON array in the response
        json_match = re.search(r'\[[\s\S]*\]', raw_output)
        if json_match:
            outline = json.loads(json_match.group())
            return outline
        else:
            # Fallback to default outline
            return get_default_outline(topic)
            
    except Exception as e:
        print(f"Outline generation failed: {e}")
        return get_default_outline(topic)


def get_default_outline(topic: str) -> List[Dict]:
    """Return a default outline structure if LLM generation fails."""
    return [
        {"title": "1. 行业宏观概况", "focus": f"{topic} 市场规模 发展历程 政策环境"},
        {"title": "2. 竞争格局分析", "focus": f"{topic} 主要企业 市场份额 竞争态势"},
        {"title": "3. 技术发展趋势", "focus": f"{topic} 核心技术 创新突破 技术瓶颈"},
        {"title": "4. 消费者与市场洞察", "focus": f"{topic} 用户画像 消费趋势 需求痛点"},
        {"title": "5. 未来展望与建议", "focus": f"{topic} 发展预测 投资机会 战略建议"}
    ]


def summarize_chapter(content: str, max_length: int = 200) -> str:
    """
    Create a brief summary of a chapter for context continuity.
    
    Args:
        content: The chapter content
        max_length: Maximum summary length
        
    Returns:
        Brief summary string
    """
    # Simple extraction: take the first paragraph or truncate
    lines = content.split('\n')
    summary_lines = []
    current_length = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if current_length + len(line) > max_length:
            break
        summary_lines.append(line)
        current_length += len(line)
    
    return ' '.join(summary_lines)[:max_length] + "..."
