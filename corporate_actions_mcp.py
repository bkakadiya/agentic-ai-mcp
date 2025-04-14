from mcp.server.fastmcp import FastMCP
from services.corporate_actions import get_dividends, get_stock_splits

# Initialize FastMCP server for corporate actions
mcp = FastMCP("corporate_actions")

@mcp.tool()
async def get_dividends_info_mcp(symbol: str) -> str:
    """Get dividend history for a stock."""
    data = get_dividends(symbol)
    if data:
        return f"Dividend history for {symbol}: {data}"
    else:
        return f"Could not retrieve dividend history for {symbol}."

@mcp.tool()
async def get_splits_info_mcp(symbol: str) -> str:
    """Get stock split history for a stock."""
    data = get_stock_splits(symbol)
    if data:
        return f"Stock split history for {symbol}: {data}"
    else:
        return f"Could not retrieve stock split history for {symbol}."

if __name__ == "__main__":
    print("Starting corporate actions MCP server...")
    mcp.run(transport='stdio')
    print("Corporate actions MCP server is running...")