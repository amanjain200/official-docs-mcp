from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Shared Context Server")

# This is only in-memory storage.
# It is erased whenever the server process stops.
context_store: dict[str, list[str]] = {}


@mcp.tool()
async def share_context(agent: str, content: str) -> dict:
    """Store context received from a specified agent."""

    if agent not in context_store:
        context_store[agent] = []

    context_store[agent].append(content)

    return {
        "result": f"Context stored from {agent}: {content}"
    }


@mcp.tool()
async def retrieve_context(query: str) -> dict:
    """Retrieve stored context entries containing the query text."""

    matching = []

    for agent, contents in context_store.items():
        for content in contents:
            if query.lower() in content.lower():
                matching.append(
                    {
                        "agent": agent,
                        "content": content,
                    }
                )

    if not matching:
        return {
            "result": f"No context found matching query: {query}"
        }

    return {"result": matching}


@mcp.tool()
async def list_all_context() -> dict[str, list[str]]:
    """Return all currently stored agent context."""

    return context_store


if __name__ == "__main__":
    # Uses the stdio transport by default
    mcp.run()
