from mcp.server.fastmcp import FastMCP
from services.stock_data import get_time_series, search_ticker

# Initialize FastMCP server for stock data
mcp = FastMCP("stock_data")

@mcp.tool()
async def get_stock_time_series_mcp(symbol: str, interval: str = 'daily', adjusted: bool = False, outputsize: str = 'compact') -> str:
    """Get historical time series data for a stock.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL)
        interval: Time interval (daily, weekly, monthly)
        adjusted: Whether to get adjusted daily data
        outputsize: Size of the output (compact or full)
    """
    data = get_time_series(symbol, interval, adjusted, outputsize)
    if data:
        return f"Time series data for {symbol} ({interval}): {data}"
    else:
        return f"Could not retrieve time series data for {symbol}."

@mcp.tool()
async def search_stocks_mcp(query: str) -> str:
    """Search for stock tickers based on a query.

    Args:
        query: Keywords to search for (e.g., Apple)
    """
    data = search_ticker(query)
    if data and 'bestMatches' in data:
        return f"Search results for '{query}': {data['bestMatches']}"
    else:
        return f"Could not find any stocks matching '{query}'."

if __name__ == "__main__":
    print("Starting stock data MCP server...")
    mcp.run(transport='stdio')
    print("Stock data MCP server is running...")