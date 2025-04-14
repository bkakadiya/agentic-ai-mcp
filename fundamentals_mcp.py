from mcp.server.fastmcp import FastMCP
from services.fundamentals import get_company_overview, get_etf_profile

# Initialize FastMCP server for fundamentals
mcp = FastMCP("fundamentals")

@mcp.tool()
async def get_company_info_mcp(symbol: str) -> str:
    """Get company overview and fundamental data."""
    data = get_company_overview(symbol)
    if data:
        return f"Company info for {symbol}: {data}"
    else:
        return f"Could not retrieve company information for {symbol}."

@mcp.tool()
async def get_etf_details_mcp(symbol: str) -> str:
    """Get ETF profile and holdings."""
    data = get_etf_profile(symbol)
    if data:
        return f"ETF details for {symbol}: {data}"
    else:
        return f"Could not retrieve ETF details for {symbol}."

if __name__ == "__main__":
    print("Starting fundamentals MCP server...")
    mcp.run(transport='stdio')
    print("Fundamentals MCP server is running...")