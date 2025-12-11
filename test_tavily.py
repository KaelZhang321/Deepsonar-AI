#!/usr/bin/env python3
"""
Tavily API Test Script
Run: conda activate deepsonar && python test_tavily.py
"""
import os
import sys

# Try official SDK first
try:
    from tavily import TavilyClient
    USE_SDK = True
except ImportError:
    print("⚠️ tavily-python not installed. Run: pip install tavily-python")
    USE_SDK = False
    import requests

API_KEY = os.getenv("TAVILY_API_KEY", "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")

def test_with_sdk():
    """Test using official SDK"""
    print("🔍 Testing Tavily with official SDK...")
    client = TavilyClient(api_key=API_KEY)
    response = client.search("AI industry trends 2024", max_results=3)
    
    print(f"✅ SUCCESS!")
    if response.get("answer"):
        print(f"Answer: {response['answer'][:150]}...")
    print(f"Results: {len(response.get('results', []))}")
    for r in response.get("results", [])[:3]:
        print(f"  - {r.get('title', 'N/A')[:60]}")
    return True

def test_with_requests():
    """Test using raw HTTP requests"""
    print("🔍 Testing Tavily with HTTP requests...")
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": API_KEY,
            "query": "AI industry trends 2024",
            "max_results": 3,
            "search_depth": "basic",
            "include_answer": True
        },
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS!")
        if data.get("answer"):
            print(f"Answer: {data['answer'][:150]}...")
        print(f"Results: {len(data.get('results', []))}")
        for r in data.get("results", [])[:3]:
            print(f"  - {r.get('title', 'N/A')[:60]}")
        return True
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    print(f"API Key: {API_KEY[:20]}...")
    print()
    
    try:
        if USE_SDK:
            test_with_sdk()
        else:
            test_with_requests()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
