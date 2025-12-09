from ai_engine.bocha_api import bocha_ai_search, parse_bocha_response
import json

def test_search():
    print("Testing Bocha AI Search...")
    query = "天空为什么是蓝色的"
    
    # Test non-stream mode
    response = bocha_ai_search(query, count=5, answer=True, stream=False)
    
    if response.get("code") != 200:
        print(f"Error: {response}")
        return
        
    print("Raw response received.")
    
    parsed = parse_bocha_response(response)
    
    print(f"\nAI Answer: {parsed['answer'][:100]}...")
    print(f"Web Sources: {len(parsed['web_sources'])}")
    if parsed['web_sources']:
        print(f"First Source: {parsed['web_sources'][0].get('name')}")
        
    print(f"Modal Cards: {len(parsed['modal_cards'])}")
    if parsed['modal_cards']:
        print(f"First Card Type: {parsed['modal_cards'][0].get('type')}")
        
    print("\nTest passed!")

if __name__ == "__main__":
    test_search()
