"""
Lab 5 Example: Multi-Tool Agent with Manual Loop

Run: python 05-agents/samples/multi_tool_agent_manual.py
"""

import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


class CalculatorInput(BaseModel):
    """Input for calculator."""

    expression: str = Field(description="Math expression")


class WeatherInput(BaseModel):
    """Input for weather."""

    city: str = Field(description="City name")


class SearchInput(BaseModel):
    """Input for search."""

    query: str = Field(description="Search query")


@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """Perform mathematical calculations."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


@tool(args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    weather = {
        "Seattle": "62°F, cloudy",
        "Paris": "18°C, sunny",
        "Tokyo": "24°C, rainy",
    }
    return weather.get(city, "Weather data unavailable")


@tool(args_schema=SearchInput)
def search(query: str) -> str:
    """Search for information on the web."""
    return f'Search results for "{query}": [Simulated results]'


def main():
    print("️ Multi-Tool Agent Demo (Manual Loop)\n")
    print("=" * 80 + "\n")

    model = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY"),
    )

    model_with_tools = model.bind_tools([calculator, get_weather, search])

    queries = [
        "What is 50 * 25?",
        "What's the weather in Tokyo?",
        "Search for information about TypeScript",
    ]

    for query in queries:
        print(f'Query: "{query}"')

        response = model_with_tools.invoke(query)

        if response.tool_calls and len(response.tool_calls) > 0:
            tool_call = response.tool_calls[0]
            print(f"  → Agent chose: {tool_call['name']}")
            print(f"  → With args: {tool_call['args']}")

        print("─" * 80 + "\n")

    print("=" * 80 + "\n")
    print(" Key Concepts:")
    print("   • Agents automatically select appropriate tools")
    print("   • Tool descriptions guide selection")
    print("   • Multiple specialized tools enable complex tasks")


if __name__ == "__main__":
    main()
