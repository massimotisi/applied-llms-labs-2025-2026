"""
Example 3: Manual ReAct Loop (Understanding the Pattern)

This example demonstrates implementing the ReAct (Reasoning + Acting) loop
manually to understand what create_agent() does under the hood.

The ReAct pattern:
1. Thought: What should I do next?
2. Action: Use a specific tool
3. Observation: What did the tool return?
4. (Repeat 1-3 as needed)
5. Final Answer: Respond to the user
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()




class CalculatorInput(BaseModel):
    """Input for calculator tool."""

    expression: str = Field(
        description="The mathematical expression to evaluate (e.g., '25 * 17')"
    )


class IsPrimeInput(BaseModel):
    """Input for is_prime tool."""

    number: int = Field(description="The number to check for primality")


@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """Perform mathematical calculations.
    Use this when you need to calculate mathematical expressions."""
    try:
        # Use Python's eval with restricted builtins for safer evaluation
        allowed_names = {"abs": abs, "round": round, "min": min, "max": max, "pow": pow}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


@tool(args_schema=IsPrimeInput)
def is_prime(number: int) -> str:
    """Check if a number is prime.
    Use this when you need to determine if a number is a prime number."""
    if number < 2:
        return "False (less than 2)"
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return f"False (divisible by {i})"
    return "True"


# --- Manual ReAct Loop Implementation ---


def run_react_loop(query: str, tools: list, max_iterations: int = 5):
    """
    Manually implement the ReAct loop.

    This function demonstrates the core ReAct pattern:
    - Call the model with messages
    - If the model requests tool calls, execute them
    - Add tool results to messages
    - Repeat until no more tool calls or max iterations reached

    Args:
        query: The user's question
        tools: List of tools available to the agent
        max_iterations: Maximum number of reasoning iterations

    Returns:
        The final response content from the model
    """
    # Initialize the model
    model = ChatOpenAI(
        model=os.getenv("AI_MODEL"),
        base_url=os.getenv("AI_ENDPOINT"),
        api_key=os.getenv("AI_API_KEY"),
    )

    # Create tool lookup dictionary for easy access
    tools_by_name = {t.name: t for t in tools}


    model_with_tools = model.bind_tools(tools)

    # Initialize messages with the user query
    messages = [HumanMessage(content=query)]

    for iteration in range(max_iterations):
        print(f"\n--- Iteration {iteration + 1} ---")

        # Step 1: Call the model (Thought phase)
        response = model_with_tools.invoke(messages)
        messages.append(response)

        # Step 2: Check if there are tool calls (Decision point)
        if not response.tool_calls:
            print("No more tool calls - Final answer ready")
            return response.content

        # Step 3: Execute each tool call (Action + Observation phase)
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"Action: {tool_name}({tool_args})")

            # Execute the tool
            try:
                tool_result = tools_by_name[tool_name].invoke(tool_args)
            except Exception as e:
                tool_result = f"Error executing tool: {e}"

            print(f"Observation: {tool_result}")

            # Add tool result to messages (so model can see it in next iteration)
            messages.append(
                ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"])
            )

    return "Max iterations reached without final answer"




def main():
    print("=" * 60)
    print(" Manual ReAct Loop Implementation")
    print("=" * 60)

    # Define available tools
    tools = [calculator, is_prime]

    # Test query that requires multiple tool calls
    query = "Calculate 25 * 17, then tell me if the result is a prime number"

    print(f"\n Query: {query}")
    print("-" * 60)

    # Run the manual ReAct loop
    result = run_react_loop(query, tools)

    print("\n" + "=" * 60)
    print(f" Final Answer: {result}")
    print("=" * 60)



if __name__ == "__main__":
    main()
