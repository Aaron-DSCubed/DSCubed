from calculator import calculate, calculator_function
from get_time import get_current_time, get_current_time_function
from get_stock_price import get_stock_price, get_stock_price_function
import json

# Check if the model wants to call a function
def tool_call_function(assistant_message, messages, client):
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






