import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf
from calculator import calculate, calculator_function
from get_time import get_current_time, get_current_time_function
from get_stock_price import get_stock_price, get_stock_price_function

# Load environment variables from .env file
load_dotenv()

# Access the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    print("\n\nFinal response:")
    print(second_response.choices[0].message.content)
else:
    # The model chose to respond directly
    print("\n\nDirect response (no function call):")
    print(assistant_message.content)





# end 

