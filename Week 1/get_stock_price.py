# Get stock price function
import yfinance as yf

def get_stock_price(ticker: str) -> float | None:
    """Returns the latest stock price for the given ticker symbol."""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            return data["Close"].iloc[-1]
        else:
            print("No data available for", ticker)
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
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