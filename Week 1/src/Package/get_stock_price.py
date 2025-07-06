# Get stock price function
import yfinance as yf
from rich.console import Console
import asyncio

console = Console()

async def get_stock_price(ticker: str) -> float | None:
    """
    Returns the latest stock price for the given ticker symbol.

    Args:
        ticker: The ticker symbol of the stock, e.g., 'AAPL', 'TSLA'

    Returns:
        The price of the stock as a float
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            return data["Close"].iloc[-1]
        else:
            console.print(f"[italic red](System Message) No data available for {ticker}[/italic red]")
            return None
    except Exception as e:
        console.print(f"[italic red](System Message) Error fetching data: {e}[/italic red]")        
        return None

get_stock_price_function = {
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "Returns the latest stock price for the given ticker symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The ticker symbol of the stock, e.g., 'AAPL', 'TSLA'"
                }
            },
            "required": ["ticker"]
        }
    }
}