from mcp.server.fastmcp import FastMCP
from services.top_movers import get_top_gainers_losers

# Initialize FastMCP server for top movers
mcp = FastMCP("top_movers")

@mcp.tool()
async def get_top_gainers_losers_mcp() -> str:
    """Get the top 5 gainers and losers."""
    data = get_top_gainers_losers()
    if data and 'top_gainers' in data and 'top_losers' in data:
        return f"Top Gainers: {data['top_gainers']}\nTop Losers: {data['top_losers']}"
    else:
        return "Could not retrieve top gainers and losers."

if __name__ == "__main__":
    print("Starting top movers MCP server...")
    mcp.run(transport='stdio')
    print("Top movers MCP server is running...")