"""
Test script for 火山引擎 ARK API.

Run this to verify the API connection is working correctly.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API configuration
api_key = os.getenv("ARK_API_KEY")
base_url = os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
model_endpoint = os.getenv("ARK_MODEL_ENDPOINT", "ep-20251123151038-946rh")

print(f"Testing ARK API...")
print(f"Base URL: {base_url}")
print(f"Model: {model_endpoint}")
print(f"API Key: {api_key[:10]}..." if api_key else "API Key: NOT SET")
print("-" * 50)

# Create client
client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

# Test 1: Simple chat completion
print("\n[Test 1] Simple chat completion...")
try:
    response = client.chat.completions.create(
        model=model_endpoint,
        messages=[
            {"role": "user", "content": "用一句话介绍人工智能是什么？"}
        ],
        max_tokens=200,
    )
    print(f"✅ Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: With system prompt
print("\n[Test 2] With system prompt...")
try:
    response = client.chat.completions.create(
        model=model_endpoint,
        messages=[
            {"role": "system", "content": "You are a helpful business analyst."},
            {"role": "user", "content": "What is AI?"}
        ],
        max_tokens=200,
    )
    print(f"✅ Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("Tests completed!")
