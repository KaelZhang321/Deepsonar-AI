"""
Reference Manager and Document Assembly Utilities

This module provides tools for generating ultra-long documents through
a "Divide and Conquer" approach, with intelligent reference deduplication.
"""
import re
from typing import Dict, List, Tuple, Optional


class GlobalReferenceManager:
    """
    Manages references across multiple document chapters.
    
    Solves the problem of conflicting reference IDs when different chapters
    use [Ref-1], [Ref-2], etc. independently. This class:
    1. Tracks all unique URLs globally
    2. Assigns a single global ID to each unique URL
    3. Rewrites chapter content to use global IDs
    4. Generates a unified bibliography at the end
    """
    
    def __init__(self):
        # URL -> Global ID mapping for deduplication
        self.url_map: Dict[str, int] = {}
        self.next_id: int = 1
        # Final reference list with metadata
        self.global_refs: List[Dict] = []

    def process_chapter_content(self, content: str, chapter_refs: List[Dict]) -> str:
        """
        Process a single chapter's content and rewrite its references.
        
        Args:
            content: The chapter markdown text with [Ref-N] citations
            chapter_refs: List of reference metadata, e.g.:
                [{"id": "[Ref-1]", "url": "https://...", "title": "..."}]
        
        Returns:
            Content with [Ref-N] replaced by globally unique IDs
        """
        # Build local -> global ID mapping
        local_to_global: Dict[str, str] = {}

        for ref in chapter_refs:
            local_tag = ref.get('id', '')  # e.g., "[Ref-1]"
            url = ref.get('url', '')
            title = ref.get('title', '无标题')

            if not local_tag or not url:
                continue

            # Core deduplication: reuse existing global ID if URL already seen
            if url in self.url_map:
                global_id = self.url_map[url]
            else:
                # New URL, assign new global ID
                global_id = self.next_id
                self.url_map[url] = global_id
                self.next_id += 1
                self.global_refs.append({
                    "id": global_id,
                    "url": url,
                    "title": title
                })
            
            local_to_global[local_tag] = f"[Ref-{global_id}]"

        # Replace all [Ref-N] patterns in content
        def replace_match(match):
            tag = match.group(0)
            return local_to_global.get(tag, tag)

        new_content = re.sub(r"\[Ref-\d+\]", replace_match, content)
        return new_content

    def get_final_bibliography(self) -> str:
        """Generate the final unified bibliography in Markdown format."""
        if not self.global_refs:
            return ""
            
        lines = ["\n---\n\n## 参考文献 (References)\n"]
        for ref in self.global_refs:
            lines.append(f"- [Ref-{ref['id']}] {ref['title']}, 链接: {ref['url']}")
        return "\n".join(lines)

    def get_ref_count(self) -> int:
        """Return the total number of unique references."""
        return len(self.global_refs)


def parse_chapter_output(raw_output: str) -> Tuple[str, List[Dict]]:
    """
    Parse LLM chapter output to extract content and structured references.
    
    Expected format from LLM:
    ```
    [Chapter content with [Ref-1], [Ref-2] citations...]
    
    ---REFS---
    [Ref-1] | https://example.com | Title One
    [Ref-2] | https://another.com | Title Two
    ```
    
    Args:
        raw_output: Raw LLM output string
        
    Returns:
        Tuple of (content_text, list_of_reference_dicts)
    """
    if "---REFS---" not in raw_output:
        # LLM didn't follow format, try to extract refs from text
        return raw_output.strip(), extract_refs_from_text(raw_output)
    
    parts = raw_output.split("---REFS---", 1)
    content_part = parts[0].strip()
    refs_part = parts[1].strip() if len(parts) > 1 else ""
    
    refs_list = []
    for line in refs_part.split('\n'):
        line = line.strip()
        if not line or '|' not in line:
            continue
        try:
            segments = line.split('|')
            if len(segments) >= 3:
                local_id = segments[0].strip()  # [Ref-1]
                url = segments[1].strip()
                title = segments[2].strip()
                refs_list.append({"id": local_id, "url": url, "title": title})
        except Exception:
            continue
    
    return content_part, refs_list


def extract_refs_from_text(text: str) -> List[Dict]:
    """
    Fallback: Extract references from text using regex patterns.
    
    Looks for patterns like:
    - [Ref-1] Title, 链接: https://...
    - [1] https://... - Title
    """
    refs = []
    
    # Pattern 1: [Ref-N] Title, 链接: URL
    pattern1 = r'\[Ref-(\d+)\]\s*([^,\n]+),?\s*链接:\s*(https?://[^\s\n]+)'
    for match in re.finditer(pattern1, text):
        refs.append({
            "id": f"[Ref-{match.group(1)}]",
            "title": match.group(2).strip(),
            "url": match.group(3).strip()
        })
    
    # Pattern 2: [Ref-N] URL
    if not refs:
        pattern2 = r'\[Ref-(\d+)\]\s*(https?://[^\s\n]+)'
        for match in re.finditer(pattern2, text):
            refs.append({
                "id": f"[Ref-{match.group(1)}]",
                "title": "参考来源",
                "url": match.group(2).strip()
            })
    
    return refs


def generate_chapter_prompt(topic: str, chapter_info: Dict, 
                           previous_summary: str = "") -> str:
    """
    Generate the prompt for writing a single chapter.
    
    Args:
        topic: The main report topic
        chapter_info: Dict with 'title' and 'focus' keys
        previous_summary: Optional summary of previous chapters for context
    """
    context_block = ""
    if previous_summary:
        context_block = f"""
【前文摘要】
{previous_summary}

"""
    
    return f"""
你正在撰写一份关于「{topic}」的深度分析报告。

{context_block}【当前任务】
撰写章节：{chapter_info.get('title', '章节')}
核心关注点：{chapter_info.get('focus', '综合分析')}

【写作要求】
1. 深度分析，内容详实，字数约 800-1200 字
2. 必须使用 [Ref-1], [Ref-2] 等格式进行引用标注
3. 引用必须来自真实的搜索结果，禁止编造链接
4. 使用专业但易懂的语言，适合企业高管阅读

【输出格式】
先输出章节正文，然后用分隔符 "---REFS---" 隔开，最后列出本章参考文献：

[正文内容...]

---REFS---
[Ref-1] | https://真实URL | 标题
[Ref-2] | https://真实URL | 标题
"""
