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


class BochaWebSearchTool(BaseTool):
    """
    Map-Reduce 智能搜索工具 - 使用博查AI搜索并自动总结每条结果。
    
    实现 Map-Reduce 模式：
    1. Map: 对每条搜索结果调用 LLM 进行独立总结
    2. Reduce: 聚合所有总结返回给 Agent
    
    这样可以极大减少 Token 消耗，防止上下文溢出。
    """

    name: str = "Bocha Web Search"
    description: str = (
        "使用博查AI进行网页搜索，自动总结每条结果。"
        "返回精简的摘要和引用编号，可用于报告中的学术引用。"
        "输入应为搜索关键词字符串。"
    )

    def _run(self, query: str) -> str:
        """
        Execute a web search with Map-Reduce summarization.

        Args:
            query: The search query string

        Returns:
            Summarized search results with citation numbers
        """
        import os
        import requests
        
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
            "count": 5  # Reduced count since we're summarizing each
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            web_pages = data.get("data", {}).get("webPages", {}).get("value", [])
            
            if not web_pages:
                return f"未找到与 '{query}' 相关的搜索结果。"
            
            # === Map-Reduce Pattern ===
            aggregated_results = []
            results_for_db = []
            reference_list = []
            
            for i, page in enumerate(web_pages, 1):
                ref_id = f"[Ref-{i}]"
                title = page.get("name", "无标题")
                raw_snippet = page.get("snippet", "")
                site_name = page.get("siteName", "")
                url = page.get("url", "")
                
                # === MAP PHASE: Summarize each result with LLM ===
                summary = self._summarize_snippet(raw_snippet, title)
                
                # Store for database (full data)
                results_for_db.append({
                    "ref_id": ref_id,
                    "index": i,
                    "title": title,
                    "snippet": raw_snippet,
                    "summary": summary,
                    "site_name": site_name,
                    "url": url
                })
                
                # Reference entry
                reference_list.append(f"{ref_id} {title}, 链接: {url}")
                
                # Compact format for LLM (summarized)
                entry = (
                    f"来源 ID: {ref_id}\n"
                    f"标题: {title}\n"
                    f"链接: {url}\n"
                    f"关键事实: {summary}"
                )
                aggregated_results.append(entry)
            
            # === REDUCE PHASE: Aggregate all summaries ===
            output_for_llm = f"=== 搜索「{query}」共 {len(web_pages)} 条结果（已自动总结）===\n\n"
            output_for_llm += "【提示】使用 [Ref-N] 引用来源，报告结尾附参考文献。\n\n"
            output_for_llm += "\n\n----------------\n\n".join(aggregated_results)
            output_for_llm += "\n\n----------------\n\n"
            output_for_llm += "【参考文献模板】\n"
            for ref in reference_list:
                output_for_llm += f"  - {ref}\n"
            
            # Save to database
            try:
                full_output = f"## 搜索「{query}」找到 {len(web_pages)} 条结果\n\n"
                for item in results_for_db:
                    full_output += f"{item['ref_id']}\n标题: {item['title']}\n摘要: {item['snippet']}\n链接: {item['url']}\n\n---\n\n"
                self._save_search_result(query, web_pages, full_output, results_for_db)
            except Exception as save_error:
                print(f"Warning: Failed to save search result: {save_error}")
            
            return output_for_llm
            
        except requests.exceptions.Timeout:
            return f"搜索超时，请稍后重试。关键词：{query}"
        except requests.exceptions.RequestException as e:
            return f"搜索请求失败：{str(e)}。请检查网络连接。"
        except Exception as e:
            return f"搜索出错：{str(e)}。请使用已有知识继续分析。"
    
    def _summarize_snippet(self, snippet: str, title: str) -> str:
        """
        Map Phase: Summarize a single snippet using LLM.
        
        Args:
            snippet: The raw text to summarize
            title: The title for context
            
        Returns:
            A concise 2-sentence summary
        """
        if not snippet or len(snippet) < 50:
            return snippet if snippet else "无详细内容"
        
        try:
            import os
            from crewai import LLM
            
            # Use the same ARK LLM for summarization
            summarizer = LLM(
                model=f"openai/{os.environ.get('ARK_MODEL_ENDPOINT', 'ep-20250103154042-lzccq')}",
                api_key=os.environ.get("ARK_API_KEY"),
                base_url=os.environ.get("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
                max_tokens=150  # Keep summaries short
            )
            
            # Micro-prompt for fast summarization
            micro_prompt = (
                f"请用2句话总结以下内容的关键事实（保持客观，不要废话）：\n"
                f"标题：{title}\n"
                f"内容：{snippet[:500]}"
            )
            
            # Call LLM for summarization
            result = summarizer.call(messages=[{"role": "user", "content": micro_prompt}])
            
            if result and len(result) > 10:
                return result.strip()[:200]  # Limit summary length
            else:
                # Fallback to truncation if LLM fails
                return snippet[:150] + "..." if len(snippet) > 150 else snippet
                
        except Exception as e:
            # Fallback: simple truncation if summarization fails
            print(f"Summarization fallback: {e}")
            return snippet[:150] + "..." if len(snippet) > 150 else snippet
    
    def _save_search_result(self, keyword: str, web_pages: list, formatted: str, results_json: list):
        """Save search result to database."""
        try:
            import os
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
            
            SearchResult.objects.create(
                keyword=keyword,
                results_count=len(web_pages),
                results_json=results_json,
                formatted_results=formatted,
                search_source="bocha"
            )
        except Exception as e:
            print(f"Database save error: {e}")


class BochaAISearchTool(BaseTool):
    """
    Bocha AI Search Tool - Search with AI-generated answers and structured cards.
    """
    name: str = "Bocha AI Search"
    description: str = (
        "使用博查AI进行智能搜索，提供直接答案、引用来源和垂域结构化数据（如医药百科、统计数据等）。"
        "适合需要精准回答或专业百科信息的查询。"
        "输入应为搜索关键词字符串。"
    )

    def _run(self, query: str) -> str:
        """
        Execute an AI search.

        Args:
            query: The search query

        Returns:
            AI generated answer with references
        """
        try:
            from ai_engine.bocha_api import bocha_ai_search, parse_bocha_response
            
            raw_response = bocha_ai_search(query, count=10, answer=True, stream=False)
            parsed = parse_bocha_response(raw_response)
            
            web_sources = parsed.get("web_sources", [])
            answer = parsed.get("answer", "")
            cards = parsed.get("modal_cards", [])
            
            # Save to DB (optional, reusing existing logic if relevant but structure differs)
            # For now just format output for Agent
            
            output = f"【智能回答】\n{answer}\n\n"
            
            if cards:
                output += "【专业卡片信息】\n"
                for card in cards:
                    card_type = card.get("type", "")
                    card_data = card.get("data", [])
                    # Simple dump for card data, could be refined
                    output += f"- 类型: {card_type}\n  内容: {str(card_data)[:500]}...\n"
                output += "\n"
            
            output += "【参考来源】\n"
            for i, source in enumerate(web_sources, 1):
                name = source.get("name", "无标题")
                url = source.get("url", "")
                snippet = source.get("snippet", "")
                output += f"{i}. {name} ({url})\n   摘要: {snippet[:200]}...\n"
            return output
            
        except Exception as e:
            return f"AI Search failed: {str(e)}"


class DeepReadTool(BaseTool):
    """
    Deep Web Reader Tool - Read full web page content and summarize it.
    
    Priority order:
    1. Jina AI Reader (free, no key required) - DEFAULT
    2. Firecrawl (if API key set)
    3. Basic BeautifulSoup crawler (fallback)
    """
    name: str = "Deep Web Reader"
    description: str = (
        "深度阅读指定 URL 的完整网页内容，提取并总结核心信息。"
        "适用于需要深入了解某个具体网页内容的场景。"
        "输入应为完整的 URL 地址。"
    )

    def _run(self, url: str) -> str:
        """
        Read and summarize web page content.

        Args:
            url: The URL to read

        Returns:
            Summarized content from the web page
        """
        import os
        
        crawl_method = "other"
        raw_content = ""
        summary = ""
        success = False
        error_msg = ""
        
        # =====================
        # Method 1: Jina AI Reader (FREE, Default)
        # =====================
        try:
            content = self._jina_read(url)
            if content and len(content) > 100:
                raw_content = content
                crawl_method = "jina"
                summary = self._summarize_content(url, content)
                success = True
                self._save_to_db(url, raw_content, summary, crawl_method, success)
                return summary
        except Exception as e:
            print(f"Jina Reader error: {e}")
            error_msg = str(e)
        
        # =====================
        # Method 2: Firecrawl (if API key available)
        # =====================
        firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
        
        if firecrawl_key:
            try:
                from firecrawl import FirecrawlApp
                app = FirecrawlApp(api_key=firecrawl_key)
                
                scrape_result = app.scrape_url(url, params={'formats': ['markdown']})
                content = scrape_result.get('markdown', '')
                
                if content:
                    raw_content = content
                    crawl_method = "firecrawl"
                    summary = self._summarize_content(url, content)
                    success = True
                    self._save_to_db(url, raw_content, summary, crawl_method, success)
                    return summary
                    
            except ImportError:
                pass
            except Exception as e:
                print(f"Firecrawl error: {e}")
                error_msg = str(e)
        
        # =====================
        # Method 3: Basic BeautifulSoup crawler (Fallback)
        # =====================
        try:
            content = self._basic_crawl(url)
            if content:
                raw_content = content
                crawl_method = "beautifulsoup"
                summary = self._summarize_content(url, content)
                success = True
                self._save_to_db(url, raw_content, summary, crawl_method, success)
                return summary
            
            # Save failure
            self._save_to_db(url, "", "", crawl_method, False, "No content returned")
            return f"Failed to read content from {url}"
            
        except Exception as e:
            self._save_to_db(url, "", "", crawl_method, False, str(e))
            return f"Failed to read {url}: {str(e)}"

    def _save_to_db(self, url: str, raw_content: str, summary: str, 
                    method: str, success: bool, error_msg: str = ""):
        """Save crawl result to database."""
        try:
            import sys
            import os
            from pathlib import Path
            
            backend_dir = Path(__file__).resolve().parent.parent / "backend"
            if str(backend_dir) not in sys.path:
                sys.path.insert(0, str(backend_dir))
            
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
            
            import django
            if not django.apps.apps.ready:
                django.setup()
            
            from apps.reports.models import CrawledContent
            
            CrawledContent.objects.create(
                url=url[:2000],  # Respect max_length
                raw_content=raw_content[:50000] if raw_content else "",  # Limit size
                summary=summary,
                content_length=len(raw_content) if raw_content else 0,
                crawl_method=method,
                success=success,
                error_message=error_msg
            )
        except Exception as e:
            print(f"Database save error: {e}")

    def _jina_read(self, url: str) -> str:
        """
        Use Jina AI Reader (free) to convert URL to Markdown.
        Simply prefix the URL with https://r.jina.ai/
        """
        import requests
        
        jina_url = f"https://r.jina.ai/{url}"
        
        headers = {
            "Accept": "text/markdown",
            "User-Agent": "Mozilla/5.0 (compatible; DeepSonar/1.0)"
        }
        
        response = requests.get(jina_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        return response.text

    def _basic_crawl(self, url: str) -> str:
        """Basic fallback crawler using requests and BeautifulSoup."""
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator="\n", strip=True)
        
        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines[:200])  # Limit to first 200 lines

    def _summarize_content(self, url: str, content: str) -> str:
        """Summarize long content using LLM."""
        import os
        from litellm import completion
        
        # If content is short, return as-is
        if len(content) < 1500:
            return f"【来源: {url}】\n\n{content}"
        
        # Truncate for summarization (context limit protection)
        truncated = content[:8000]
        
        try:
            summary_prompt = f"""
请将以下网页内容总结为 500 字以内的精华摘要，保留关键数据、观点和结论：

---
{truncated}
---

要求：
1. 保留具体数字和数据
2. 保留关键人名、公司名
3. 提炼核心观点和结论
4. 使用简洁的要点形式
"""
            
            response = completion(
                model=os.getenv("ARK_MODEL_ENDPOINT", "openai/ep-20250603140551-tp9lt"),
                messages=[{"role": "user", "content": summary_prompt}],
                api_key=os.getenv("ARK_API_KEY"),
                base_url=os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
                max_tokens=800
            )
            
            summary = response.choices[0].message.content.strip()
            return f"【来源: {url}】\n\n{summary}"
            
        except Exception as e:
            # If summarization fails, return truncated content
            return f"【来源: {url}】\n\n{truncated[:1500]}..."


# Instantiate tools for easy import
search_tool = DuckDuckGoSearchTool()
crawler_tool = WebCrawlerTool()
bocha_search_tool = BochaWebSearchTool()
deep_read_tool = DeepReadTool()
