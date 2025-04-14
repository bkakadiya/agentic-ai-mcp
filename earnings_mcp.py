from mcp.server.fastmcp import FastMCP
from services.earnings import get_earnings

# Initialize FastMCP server for earnings
mcp = FastMCP("earnings")

@mcp.tool()
async def get_earnings_data_mcp(symbol: str) -> str:
    """Get quarterly and annual earnings details for a company."""
    data = get_earnings(symbol)
    if data:
        return f"Earnings data for {symbol}: {data}"
    else:
        return f"Could not retrieve earnings data for {symbol}."

if __name__ == "__main__":
    print("Starting earnings MCP server...")
    mcp.run(transport='stdio')
    print("Earnings MCP server is running...")