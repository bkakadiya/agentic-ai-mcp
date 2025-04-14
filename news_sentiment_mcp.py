from mcp.server.fastmcp import FastMCP
from services.news_sentiment import get_news_sentiment

# Initialize FastMCP server for news sentiment
mcp = FastMCP("news_sentiment")

@mcp.tool()
async def get_financial_news_mcp(tickers: str = None, topics: str = None, time_from: str = None, time_to: str = None, sort: str = 'latest') -> str:
    """Get news and sentiment related to financial markets or specific tickers.

    Args:
        tickers: Comma-separated list of tickers (e.g., AAPL,GOOG)
        topics: Specific news topics (e.g., technology, earnings)
        time_from: Start date for news (YYYY-MM-DD)
        time_to: End date for news (YYYY-MM-DD)
        sort: Sort order ('latest', 'earliest')
    """
    data = get_news_sentiment(tickers=tickers, topics=topics, time_from=time_from, time_to=time_to, sort=sort)
    if data and 'feed' in data:
        return f"Financial news: {data['feed']}"
    else:
        return "Could not retrieve financial news."

if __name__ == "__main__":
    print("Starting news sentiment MCP server...")
    mcp.run(transport='stdio')
    print("News sentiment MCP server is running...")