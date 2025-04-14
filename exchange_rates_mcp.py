from mcp.server.fastmcp import FastMCP
from services.exchange_rates import (
    get_exchange_rate,
    get_currency_time_series,
    get_digital_currency_exchange_rate,
    get_digital_currency_time_series
)

# Initialize FastMCP server for exchange rates
mcp = FastMCP("exchange_rates")

@mcp.tool()
async def get_fx_rate_mcp(from_currency: str, to_currency: str) -> str:
    """Get the real-time exchange rate for a currency pair."""
    data = get_exchange_rate(from_currency, to_currency)
    if data and 'Realtime Currency Exchange Rate' in data:
        return f"Exchange rate {from_currency}/{to_currency}: {data['Realtime Currency Exchange Rate']}"
    else:
        return f"Could not retrieve exchange rate for {from_currency}/{to_currency}."

@mcp.tool()
async def get_currency_time_series_mcp(from_currency: str, to_currency: str, interval: str = 'daily', outputsize: str = 'compact') -> str:
    """Get historical time series data for a currency pair."""
    data = get_currency_time_series(from_currency, to_currency, interval, outputsize)
    if data:
        return f"Currency time series {from_currency}/{to_currency} ({interval}): {data}"
    else:
        return f"Could not retrieve time series data for {from_currency}/{to_currency}."

@mcp.tool()
async def get_crypto_rate_mcp(symbol: str, market: str) -> str:
    """Get the real-time exchange rate for a digital currency pair."""
    data = get_digital_currency_exchange_rate(symbol, market)
    if data and 'Realtime Currency Exchange Rate' in data:
        return f"Crypto exchange rate {symbol}/{market}: {data['Realtime Currency Exchange Rate']}"
    else:
        return f"Could not retrieve exchange rate for {symbol}/{market}."

@mcp.tool()
async def get_digital_currency_time_series_mcp(symbol: str, market: str, interval: str = 'daily', outputsize: str = 'compact') -> str:
    """Get historical time series data for a digital currency pair."""
    data = get_digital_currency_time_series(symbol, market, interval, outputsize)
    if data:
        return f"Digital currency time series {symbol}/{market} ({interval}): {data}"
    else:
        return f"Could not retrieve time series data for {symbol}/{market}."

if __name__ == "__main__":
    print("Starting exchange rates MCP server...")
    mcp.run(transport='stdio')
    print("Exchange rates MCP server is running...")