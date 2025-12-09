"""
Simplified test for CrewAI with 火山引擎 ARK API.

This test uses a minimal configuration without tools to verify LLM integration.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI environment variables for compatibility
api_key = os.getenv("ARK_API_KEY")
base_url = os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
model_endpoint = os.getenv("ARK_MODEL_ENDPOINT", "ep-20251123151038-946rh")

os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_API_BASE"] = base_url

print(f"Testing CrewAI with ARK API...")
print(f"Model: {model_endpoint}")
print("-" * 50)

from crewai import Agent, Task, Crew, LLM

# Create LLM instance
llm = LLM(
    model=f"openai/{model_endpoint}",
    base_url=base_url,
    api_key=api_key,
    temperature=0.7,
)

# Create a simple agent WITHOUT tools
analyst = Agent(
    role="Business Analyst",
    goal="Analyze business topics and provide insights",
    backstory="You are an experienced business analyst with expertise in market analysis.",
    llm=llm,
    tools=[],  # No tools - pure LLM response
    verbose=True,
    allow_delegation=False,
)

# Create a simple task
task = Task(
    description="Briefly describe what artificial intelligence is and its business applications in 3-5 sentences.",
    expected_output="A concise description of AI and its business uses.",
    agent=analyst,
)

# Create and run the crew
crew = Crew(
    agents=[analyst],
    tasks=[task],
    verbose=True,
)

print("\n🚀 Running CrewAI...")
try:
    result = crew.kickoff()
    print("\n" + "=" * 50)
    print("✅ SUCCESS!")
    print("=" * 50)
    print(f"Result: {result}")
except Exception as e:
    print("\n" + "=" * 50)
    print("❌ FAILED!")
    print("=" * 50)
    print(f"Error: {e}")
