import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf
import calculator



# Load environment variables from .env file
load_dotenv()

# Access the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_current_time(timezone_str: str) -> datetime:
    """Returns the current local date and 24-hour time (datetime object) in the specified timezone."""
    try:
        return datetime.now(ZoneInfo(timezone_str))
    except Exception as e:
        raise ValueError(f"Invalid timezone '{timezone_str}': {e}")

get_current_time_function = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Returns the current local time in the specified timezone",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone_str": {
                    "type": "string",
                    "description": "The IANA timezone name, e.g., 'Asia/Tokyo', 'America/New_York'"
                }
            },
            "required": ["timezone_str"]
        }
    }
}


# Get stock price function
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

# Example usage:
price = get_stock_price("AAPL")
print(f"AAPL price: {price}")





# Create a conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's 241 multiplied by 18?"},
    {"role": "user", "content": "What is the current time in Tokyo?"},
    {"role": "user", "content": "What is the current stock price of Tesla?"}
]

# Get the model's response with the calculator function available
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=[calculator_function, get_current_time_function, get_stock_price_function],
    tool_choice="auto",
    temperature=0.7,
    max_tokens=150
)

# Process the response
assistant_message = response.choices[0].message
messages.append(assistant_message.model_dump())

# Check if the model wants to call a function
if assistant_message.tool_calls:
    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name

        if function_name == "calculate":
            # Parse the function arguments
            arguments = json.loads(tool_call.function.arguments)
            operation = arguments.get("operation")
            x = arguments.get("x")
            y = arguments.get("y")

            print(f"Function call: calculate({operation}, {x}, {y})")

            # Call the function
            result = calculate(operation, x, y)

                # Add the function result to the conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(result)
            })

            print(f"Function result: {result}")

        elif function_name == "get_current_time":
            # Parse the function arguments
            arguments = json.loads(tool_call.function.arguments)
            timezone_str = arguments.get("timezone_str")

            print(f"Function call: get_current_time({timezone_str})")

            # Call the function
            result = get_current_time(timezone_str)

            # Add the function result to the conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(result)
            })

            print(f"Function result: {result}")

        elif function_name == "get_stock_price":
            # Parse the function arguments
            arguments = json.loads(tool_call.function.arguments)
            ticker = arguments.get("ticker")

            print(f"Function call: get_stock_price({ticker})")

            # Call the function
            result = get_stock_price(ticker)

            # Add the function result to the conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(result)
            })

            print(f"Function result: {result}")

    # Get a new response from the model with the function result
    second_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Print the final response
    print("\\nFinal response:")
    print(second_response.choices[0].message.content)
else:
    # The model chose to respond directly
    print("\\nDirect response (no function call):")
    print(assistant_message.content)





# end 

