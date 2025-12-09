import os
import json
import requests
from typing import Dict, List, Any, Optional, Generator

def bocha_ai_search(
    query: str,
    count: int = 10,
    freshness: str = "noLimit",
    answer: bool = True,
    stream: bool = False,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Perform a search using Bocha AI Search API.
    
    Args:
        query: Search query
        count: Number of search results (max 50)
        freshness: Time range (oneDay, oneWeek, oneMonth, oneYear, noLimit)
        answer: Whether to generate LLM answer
        stream: Whether to stream results (False returns collected full response)
        api_key: Optional API key override
        
    Returns:
        Dict containing processing 'messages' and other metadata.
    """
    # Use environment variable if key not provided
    if not api_key:
        api_key = os.getenv("BOCHA_API_KEY", "sk-accd71cb3f8b48789e34040d18337912")
        
    api_url = "https://api.bocha.cn/v1/ai-search"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "freshness": freshness,
        "answer": answer,
        "stream": stream,
        "count": count
    }
    
    try:
        response = requests.post(
            api_url, 
            json=payload, 
            headers=headers, 
            timeout=60,
            stream=stream
        )
        response.raise_for_status()
        
        if stream:
            # For stream mode, we'd typically yield generators, but here we'll 
            # collect everything for simplicity in the current architecture
            # unless specific stream usage is needed.
            # Implementing a collector for stream mode:
            collected_messages = []
            final_answer = ""
            
            for line in response.iter_lines():
                if not line:
                    continue
                    
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data:"):
                    json_str = decoded_line[5:] # content after "data:"
                    try:
                        data = json.loads(json_str)
                        event = data.get("event")
                        
                        if event == "message":
                            msg = data.get("message", {})
                            collected_messages.append(msg)
                            # Accumulate answer if it's a text answer
                            if msg.get("type") == "answer" and msg.get("content_type") == "text":
                                final_answer += msg.get("content", "")
                                
                        elif event == "done":
                            break
                        elif event == "error":
                            return {"error": data.get("error_information", {}), "code": 500}
                    except json.JSONDecodeError:
                        continue
                        
            return {
                "code": 200,
                "messages": collected_messages,
                "full_answer": final_answer
            }
            
        else:
            # Non-stream mode returns the full JSON
            return response.json()
            
    except Exception as e:
        return {
            "code": 500,
            "msg": f"Request failed: {str(e)}",
            "messages": []
        }

def parse_bocha_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the raw Bocha AI Search response into structured data.
    
    Returns:
        Dict with:
        - web_sources: List of parsed webpage objects
        - answer: The AI summary answer
        - modal_cards: Structured data cards (medical, baike, etc.)
        - raw_messages: Original messages
    """
    messages = response_data.get("messages", [])
    
    web_sources = []
    modal_cards = []
    answer_parts = []
    
    for msg in messages:
        msg_type = msg.get("type")
        content_type = msg.get("content_type")
        content_str = msg.get("content", "")
        
        # Parse Answer
        if msg_type == "answer" and content_type == "text":
            answer_parts.append(content_str)
            continue
            
        # Parse Sources (Webpages, Images, Cards)
        if msg_type == "source":
            # Content is typically JSON string for sources
            try:
                if isinstance(content_str, str) and (content_str.startswith("{") or content_str.startswith("[")):
                    content_data = json.loads(content_str)
                else:
                    content_data = content_str
            except json.JSONDecodeError:
                content_data = content_str
                
            if content_type == "webpage":
                web_sources.append(content_data)
                
            elif content_type in ["baike_pro", "medical_common", "medical_pro", "weather_china", "weather_international"]:
                # These are modal cards, usually lists of objects
                modal_cards.append({
                    "type": content_type,
                    "data": content_data
                })
                
    full_answer = "".join(answer_parts)
    
    return {
        "web_sources": web_sources,
        "answer": full_answer,
        "modal_cards": modal_cards,
        "raw_messages": messages
    }
