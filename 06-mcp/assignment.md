# Assignment: Model Context Protocol (MCP)

## Overview

In this assignment, you'll practice connecting AI agents to external services using the Model Context Protocol (MCP). You'll work with MCP servers, integrate their tools with agents, and build multi-service applications.

---

## Challenge 1: Connect to Context7 MCP Server

**Objective**: Set up and use the Context7 MCP server to retrieve library documentation.

**Requirements**:
1. Connect to the public Context7 server at `https://mcp.context7.com/mcp`
2. List all available tools from the server
3. Create an agent that uses Context7 tools
4. Query for documentation about a JavaScript library of your choice (e.g., "How do I use Express.js middleware?")
5. Display the response with proper formatting

**Expected Output**:
```
 Available Tools from Context7:
   • resolve-library-id: Convert library name to Context7 ID
   • get-library-docs: Retrieve library documentation

 User: How do I use Express.js middleware?
 Agent: [Detailed documentation about Express.js middleware from Context7]
```

**Hints**:
- Use `MultiServerMCPClient` from `langchain_mcp_adapters.client`
- Use `streamable_http` transport for Context7
- Remember to use `async/await` since MCP operations are asynchronous

---

## Challenge 2: Build a Multi-Tool Agent with MCP

**Objective**: Combine MCP tools with manually created tools in a single agent.

**Requirements**:
1. Connect to Context7 MCP server (for documentation)
2. Create a custom calculator tool manually (like you did with agents)
3. Create an agent that has access to both MCP tools AND your custom tool
4. Test with queries that require different tools:
   - "What is 125 * 8?" (should use calculator)
   - "How do I use React hooks?" (should use Context7)
   - "Calculate 50 + 25, then look up documentation for the result" (should use both)

**Expected Output**:
```
️  Multi-Tool Agent (MCP + Custom Tools)

 User: What is 125 * 8?
 Agent: 125 × 8 = 1000

 User: How do I use React hooks?
 Agent: [Documentation from Context7 about React hooks]

 User: Calculate 50 + 25, then look up docs for that number
 Agent: 50 + 25 = 75. [Searches for "75" in documentation if relevant]
```

**Hints**:
- Combine tools: `all_tools = [*mcp_tools, calculator_tool]`
- The agent will automatically select the right tool based on the query
- Clear tool descriptions help the agent make better choices

---

## Challenge 3 (Bonus): Multi-Server Integration

**Objective**: Connect to multiple MCP servers simultaneously and use tools from all of them.

**Requirements**:
1. Connect to Context7 for documentation
2. Connect to another MCP server of your choice (see MCP Registry: https://github.com/mcp)
3. Create an agent that can use tools from both servers
4. Demonstrate the agent using tools from different servers in the same conversation

**Example Configuration**:
```python
client = MultiServerMCPClient(
    {
        "context7": {
            "transport": "streamable_http",
            "url": "https://mcp.context7.com/mcp"
        },
        # Add another server here
        "myServer": {
            "transport": "streamable_http",
            "url": "https://your-server-url.com/mcp"
        }
    }
)
```

**Expected Output**:
```
 Multi-Server MCP Agent

 Available Tools:
   From context7:
   • resolve-library-id
   • get-library-docs

   From myServer:
   • [list of tools from your second server]

 User: [Query that uses tools from different servers]
 Agent: [Coordinated response using multiple servers]
```

**Hints**:
- All tools from all servers become available to the agent
- The agent selects tools based on descriptions, regardless of which server they come from
- You can find available MCP servers at the [MCP Registry](https://github.com/mcp)

---

##  Learning Objectives Covered

After completing these challenges, you will have:
-  Connected to external MCP servers using Streamable HTTP transport
-  Integrated MCP tools with LangChain agents
-  Combined MCP tools with manually created tools
-  Worked with multiple MCP servers simultaneously
-  Built production-ready MCP integrations

---

##  Solution

Check [`solution/`](./solution/) for reference implementations of all challenges.

**Note**: Try to solve the challenges yourself before looking at the solutions!

---

## Need Help?

- **Agent fundamentals**: Review [Getting Started with Agents](../05-agents/README.md)

---

##  Tips for Success

1. **Start Simple**: Begin with Challenge 1 to understand the basics
2. **Clear Descriptions**: Good tool descriptions help the agent choose correctly
3. **Error Handling**: Always wrap MCP calls in try-except blocks
4. **Async/Await**: Remember MCP operations are asynchronous
5. **Test Incrementally**: Test each tool individually before combining them

---

##  Common Issues

### "Failed to connect to MCP server"
- Check your internet connection
- Verify the server URL is correct
- Ensure the server is running (for local servers)

### "Tool not found"
- Verify tools were fetched: `print(await client.get_tools())`
- Check tool names match what the server provides
- Ensure MCP client is properly initialized

### "Agent doesn't use the right tool"
- Improve tool descriptions to be more specific
- Check that tools are properly bound to the agent
- Verify the query clearly indicates which tool to use

---

[← Back to Model Context Protocol (MCP)](./README.md)
