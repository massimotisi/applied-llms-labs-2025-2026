"""
Lab 6 Example 3: Multi-Server MCP Integration

This example shows how to connect to MULTIPLE MCP servers simultaneously.
The agent gets tools from all servers and intelligently chooses which to use.

Servers used:
- Context7: Documentation tools (HTTP, remote)
- Local Calculator: Math tools (stdio, local subprocess)

The power of MCP: One client, many servers, unified interface!

Run: python 06-mcp/code/03_mcp_multi_server.py
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

load_dotenv()

SCRIPT_DIR = Path(__file__).parent


async def main():
    print(" Connecting to multiple MCP servers...\n")

    # Path to the local calculator server
    server_path = SCRIPT_DIR / "servers" / "stdio_calculator_server.py"

    # Create MCP client connected to MULTIPLE servers
    client = MultiServerMCPClient(
        {
            # Server 1: Context7 (remote, HTTP)
            "context7": {
                "transport": "streamable_http",
                "url": "https://mcp.context7.com/mcp",
            },
            # Server 2: Local Calculator (local, stdio)
            "calculator": {
                "transport": "stdio",
                "command": "python",
                "args": [str(server_path)],
            },
        }
    )

    try:
        # 1. Get tools from ALL connected servers
        print(" Fetching tools from all servers...")
        tools = await client.get_tools()

        print(f" Retrieved {len(tools)} total tools from 2 servers:\n")

        # Group and display tools by server
        context7_tools = [
            t for t in tools if "library" in t.name or "resolve" in t.name
        ]
        calc_tools = [
            t for t in tools if t.name in ("calculate", "convert_temperature")
        ]

        print(" From Context7 (Documentation):")
        for tool in context7_tools:
            print(f"   • {tool.name}: {tool.description}")

        print("\n From Local Calculator:")
        for tool in calc_tools:
            print(f"   • {tool.name}: {tool.description}")
        print()

        # 2. Create model
        model = ChatOpenAI(
            model=os.getenv("AI_MODEL"),
            base_url=os.getenv("AI_ENDPOINT"),
            api_key=os.getenv("AI_API_KEY"),
        )

        # 3. Create agent with tools from ALL servers
        agent = create_agent(model, tools)  # Tools from multiple servers!

        # 4. Test 1: Agent uses CALCULATOR tool
        print("Test 1: Math question (should use calculator)\n")
        math_query = "What is 25 * 4 + 100?"
        print(f" User: {math_query}")

        math_response = await agent.ainvoke({"messages": [("human", math_query)]})
        print(f" Agent: {math_response['messages'][-1].content}\n")

        # 5. Test 2: Agent uses CONTEXT7 tool
        print("Test 2: Documentation question (should use Context7)\n")
        docs_query = "How do I use FastAPI to create a REST API? Get documentation."
        print(f" User: {docs_query}")

        docs_response = await agent.ainvoke({"messages": [("human", docs_query)]})
        print(f" Agent: {docs_response['messages'][-1].content}\n")

        # 6. Test 3: Agent uses BOTH tools in sequence!
        print("Test 3: Combined question (should use BOTH tools)\n")
        combined_query = (
            "Calculate 15 * 8, then look up Python documentation about "
            "async/await if the result is greater than 100"
        )
        print(f" User: {combined_query}")

        combined_response = await agent.ainvoke(
            {"messages": [("human", combined_query)]}
        )
        print(f" Agent: {combined_response['messages'][-1].content}\n")

        print(" Key Concepts:")
        print("   • MultiServerMCPClient connects to multiple servers at once")
        print("   • Agent receives tools from ALL connected servers")
        print("   • Agent automatically chooses the right tool for each task")
        print("   • Mix different transport types (HTTP + stdio)")
        print("   • MCP provides unified interface across all servers")
        print("   • Scale to dozens of servers without changing agent code!\n")

        print(" Real-World Use Cases:")
        print("   • GitHub (code) + Calendar (scheduling) + Database (data)")
        print("   • Documentation (Context7) + Calculator (math) + Weather (API)")
        print("   • Internal tools + External services in one agent")

    except Exception as e:
        print(f" Error with multi-server MCP: {e}")
        if hasattr(e, "message"):
            print(f"   Message: {e.message}")

    finally:
        print("\n All MCP connections closed")


if __name__ == "__main__":
    asyncio.run(main())
